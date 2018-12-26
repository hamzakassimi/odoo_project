# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class WizardAddProduct(models.TransientModel):
    _name="wizard.add.product"

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True
    )

    qty = fields.Float(
        string='Quantite',
    )

    @api.multi
    def button_confirm(self):
        self.ensure_one()
        current_company = self.env.user.company_id
        active_rec = self.env['sale.order'].browse(self._context.get('active_id'))
        related_stock_quant = self.env['stock.quant'].search([
            ('product_id','=',self.product_id.id),
            ('company_id','=',current_company.id)
        ],limit=1)
        if related_stock_quant.quantity >0:
            if self.qty <= related_stock_quant.quantity:
                vals = {
                    'order_id':active_rec.id,
                    'product_id':self.product_id.id,
                    'name':self.product_id.display_name,
                    'product_uom_qty':self.qty
                }
                active_rec.order_line = [(0,0,vals)]
            else:
                vals = {
                    'order_id':active_rec.id,
                    'product_id':self.product_id.id,
                    'name':self.product_id.display_name,
                    'product_uom_qty':related_stock_quant.quantity
                }
                active_rec.order_line = [(0,0,vals)]
                need = self.qty - related_stock_quant.quantity
                for vendor in self.product_id.seller_ids:
                    supplier_stock_quant = self.env['stock.quant'].search([
                        ('product_id','=',self.product_id.id),
                        ('company_id','=',vendor.company_id.id)
                    ],limit=1)
                    if supplier_stock_quant.quantity > 0:
                        if need >= supplier_stock_quant.quantity:
                            vals = {
                                'order_id':active_rec.id,
                                'product_id':self.product_id.id,
                                'name':self.product_id.display_name,
                                'product_uom_qty':supplier_stock_quant.quantity,
                                'supplier_id':vendor.name.id
                            }
                            need = need - supplier_stock_quant.quantity
                            active_rec.order_line = [(0,0,vals)]
                        else:
                            vals = {
                                'order_id':active_rec.id,
                                'product_id':self.product_id.id,
                                'name':self.product_id.display_name,
                                'product_uom_qty':need,
                                'supplier_id':vendor.name.id
                            }
                            active_rec.order_line = [(0,0,vals)]
        else:
            for vendor in self.product_id.seller_ids:
                supplier_stock_quant = self.env['stock.quant'].search([
                    ('product_id','=',self.product_id.id),
                    ('company_id','=',vendor.company_id.id)
                ],limit=1)
                need = self.qty
                if supplier_stock_quant.quantity > 0:
                    if need >= supplier_stock_quant.quantity:
                        vals = {
                            'order_id':active_rec.id,
                            'product_id':self.product_id.id,
                            'name':self.product_id.display_name,
                            'product_uom_qty':supplier_stock_quant.quantity,
                            'supplier_id':vendor.name.id
                        }
                        need = need - supplier_stock_quant.quantity
                        active_rec.order_line = [(0,0,vals)]
                    else:
                        vals = {
                            'order_id':active_rec.id,
                            'product_id':self.product_id.id,
                            'name':self.product_id.display_name,
                            'product_uom_qty':need,
                            'supplier_id':vendor.name.id
                        }
                        active_rec.order_line = [(0,0,vals)]
        return True