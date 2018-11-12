# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    # ------------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------------
     
    warehouse_quantities = fields.Text(
        string='Warehouses quantities',
        compute='compute_warehouse_quantities'
    )

    line_supplier_ids = fields.One2many(
        string='Line Suppliers',
        comodel_name='sale.order.line.supplier',
        inverse_name='line_id',
    )

    # ------------------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------------------

    @api.multi
    def compute_warehouse_quantities(self):
        for record in self:
            warehouse_quantities = ''
            for quant in record.product_id.stock_quant_ids:
                related_warehouse = self.env['stock.warehouse'].search([('company_id','=',quant.company_id.id)],limit=1)
                if related_warehouse:
                    warehouse_quantities += 'Quantity' + ' : ' + str(quant.quantity) +  ' /' +'Warehouse' + ' : ' + related_warehouse.name + '\n'
                record.warehouse_quantities = warehouse_quantities

    @api.multi
    def _check_package(self):
        default_uom = self.product_id.uom_id
        pack = self.product_packaging
        qty = self.product_uom_qty
        q = default_uom._compute_quantity(pack.qty, self.product_uom)
        if qty and q and (qty % q):
            newqty = qty - (qty % q) + q
            self.product_uom_qty = newqty
            return {
                'warning': {
                    'title': _('Warning'),
                    'message': _("This product is packaged by %.2f %s. You should sell %.2f %s.") % (pack.qty, default_uom.name, newqty, self.product_uom.name),
                },
            }
        return {}