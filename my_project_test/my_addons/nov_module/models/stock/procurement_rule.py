# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


import logging

_logger = logging.getLogger(__name__)

class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    @api.multi
    def _run_buy(self, product_id, product_qty, product_uom, location_id, name, origin, values):
        res = []
        cache = {}
        suppliers = product_id.seller_ids\
            .filtered(lambda r: (not r.company_id or r.company_id == values['company_id']) and (not r.product_id or r.product_id == product_id))
        if not suppliers:
            msg = _('There is no vendor associated to the product %s. Please define a vendor for this product.') % (product_id.display_name,)
            raise UserError(msg)

        supplier = self._make_po_select_supplier(values, suppliers)
        for supp in supplier:
            if supp.min_qty !=0.0:
                product_qty = supp.min_qty
                partner = supp.name

                domain = self._make_po_get_domain(values, partner)

                if domain in cache:
                    po = cache[domain]
                else:
                    po = self.env['purchase.order'].search([dom for dom in domain])
                    po = po[0] if po else False
                    cache[domain] = po
                if not po:
                    vals = self._prepare_purchase_order(product_id, product_qty, product_uom, origin, values, partner)
                    po = self.env['purchase.order'].create(vals)
                    cache[domain] = po
                elif not po.origin or origin not in po.origin.split(', '):
                    if po.origin:
                        if origin:
                            po.write({'origin': po.origin + ', ' + origin})
                        else:
                            po.write({'origin': po.origin})
                    else:
                        po.write({'origin': origin})

                # Create Line
                po_line = False
                for line in po.order_line:
                    if line.product_id == product_id and line.product_uom == product_id.uom_po_id:
                        if line._merge_in_existing_line(product_id, product_qty, product_uom, location_id, name, origin, values):
                            procurement_uom_po_qty = product_uom._compute_quantity(product_qty, product_id.uom_po_id)
                            seller = product_id._select_seller(
                                partner_id=partner,
                                quantity=line.product_qty + procurement_uom_po_qty,
                                date=po.date_order and po.date_order[:10],
                                uom_id=product_id.uom_po_id)

                            price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price, line.product_id.supplier_taxes_id, line.taxes_id, values['company_id']) if seller else 0.0
                            if price_unit and seller and po.currency_id and seller.currency_id != po.currency_id:
                                price_unit = seller.currency_id.compute(price_unit, po.currency_id)

                            po_line = line.write({
                                'product_qty': line.product_qty + procurement_uom_po_qty,
                                'price_unit': price_unit,
                                'move_dest_ids': [(4, x.id) for x in values.get('move_dest_ids', [])]
                            })
                            break
                if not po_line:
                    vals = self._prepare_purchase_order_line(product_id, product_qty, product_uom, values, po, supplier)
                    self.env['purchase.order.line'].create(vals)
        return res


    @api.multi
    def _prepare_purchase_order_line(self, product_id, product_qty, product_uom, values, po, supplier):
        for supp in supplier:
            procurement_uom_po_qty = product_uom._compute_quantity(product_qty, product_id.uom_po_id)
            seller = product_id._select_seller(
                partner_id=supp.name,
                quantity=procurement_uom_po_qty,
                date=po.date_order and po.date_order[:10],
                uom_id=product_id.uom_po_id)

            taxes = product_id.supplier_taxes_id
            fpos = po.fiscal_position_id
            taxes_id = fpos.map_tax(taxes) if fpos else taxes
            if taxes_id:
                taxes_id = taxes_id.filtered(lambda x: x.company_id.id == values['company_id'].id)

            price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price, product_id.supplier_taxes_id, taxes_id, values['company_id']) if seller else 0.0
            if price_unit and seller and po.currency_id and seller.currency_id != po.currency_id:
                price_unit = seller.currency_id.compute(price_unit, po.currency_id)

            product_lang = product_id.with_context({
                'lang': supp.name.lang,
                'partner_id': supp.name.id,
            })
            name = product_lang.display_name
            if product_lang.description_purchase:
                name += '\n' + product_lang.description_purchase

            date_planned = self.env['purchase.order.line']._get_date_planned(seller, po=po).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

            return {
                'name': name,
                'product_qty': procurement_uom_po_qty,
                'product_id': product_id.id,
                'product_uom': product_id.uom_po_id.id,
                'price_unit': price_unit,
                'date_planned': date_planned,
                'orderpoint_id': values.get('orderpoint_id', False) and values.get('orderpoint_id').id,
                'taxes_id': [(6, 0, taxes_id.ids)],
                'order_id': po.id,
                'move_dest_ids': [(4, x.id) for x in values.get('move_dest_ids', [])],
            }

    def _make_po_select_supplier(self, values, suppliers):
        """ Method intended to be overridden by customized modules to implement any logic in the
            selection of supplier.
        """
        print('values',values)
        warehouse_supplier = values['warehouse_id']['supplier_id']
        for supplier in suppliers:
            if supplier.name.id == warehouse_supplier.id and values['warehouse_id']['flag']==True:
                return supplier
            else:
                return suppliers