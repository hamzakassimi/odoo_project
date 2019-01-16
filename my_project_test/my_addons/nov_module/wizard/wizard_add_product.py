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

    warehouse_quantities = fields.Text(
        string='Warehouses quantities',
    )

    @api.multi
    @api.onchange('product_id')
    def onchage_warehouse_quantities(self):
        for record in self:
            warehouse_quantities = ''
            for quant in record.product_id.stock_quant_ids:
                related_warehouse = self.env['stock.warehouse'].search([('company_id','=',quant.company_id.id)],limit=1)
                if related_warehouse:
                    warehouse_quantities += 'Quantity' + ' : ' + str(quant.quantity) +  ' /' +'Warehouse' + ' : ' + related_warehouse.name + '\n'
                record.warehouse_quantities = warehouse_quantities
            return {
                'warning': {
                    'title': _('Warning'),
                    'message': _("those are the quantities disponible in your warehouses %s.") % (record.warehouse_quantities),
            },
        }

    @api.multi
    def button_confirm(self):
        self.ensure_one()
        current_company = self.env.user.company_id
        active_rec = self.env['sale.order'].browse(self._context.get('active_id'))
        related_stock_quant = self.env['stock.quant'].search([
            ('product_id','=',self.product_id.id),
            ('company_id','=',current_company.id),
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
                first_supplier = self.env['product.supplierinfo'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id),('priority','=','one')],limit=1)
                if first_supplier:
                    first_supplier_stock_quant = self.env['stock.quant'].search([
                        ('product_id','=',self.product_id.id),
                        ('company_id.partner_id','=',first_supplier.name.id)],limit=1)
                    if first_supplier_stock_quant.quantity > 0:
                        if need >= first_supplier_stock_quant.quantity:
                            vals = {
                                'order_id':active_rec.id,
                                'product_id':self.product_id.id,
                                'name':self.product_id.display_name,
                                'product_uom_qty':first_supplier_stock_quant.quantity,
                                'supplier_id':first_supplier.name.id
                            }
                            need = need - first_supplier_stock_quant.quantity
                            active_rec.order_line = [(0,0,vals)]
                            second_supplier = self.env['product.supplierinfo'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id),('priority','=','two')],limit=1)
                            if second_supplier:
                                second_supplier_stock_quant = self.env['stock.quant'].search([
                                    ('product_id','=',self.product_id.id),
                                    ('company_id.partner_id','=',second_supplier.name.id)],limit=1)
                                if second_supplier_stock_quant.quantity > 0:
                                    if need >= second_supplier_stock_quant.quantity:
                                        vals = {
                                            'order_id':active_rec.id,
                                            'product_id':self.product_id.id,
                                            'name':self.product_id.display_name,
                                            'product_uom_qty':second_supplier_stock_quant.quantity,
                                            'supplier_id':second_supplier.name.id
                                        }
                                        need = need - second_supplier_stock_quant.quantity
                                        active_rec.order_line = [(0,0,vals)]
                                        third_supplier = self.env['product.supplierinfo'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id),('priority','=','three')],limit=1)
                                        if third_supplier:
                                            third_supplier_stock_quant = self.env['stock.quant'].search([
                                                ('product_id','=',self.product_id.id),
                                                ('company_id.partner_id','=',third_supplier.name.id)],limit=1)
                                            if third_supplier_stock_quant.quantity > 0:
                                                if need >= third_supplier_stock_quant.quantity:
                                                    vals = {
                                                        'order_id':active_rec.id,
                                                        'product_id':self.product_id.id,
                                                        'name':self.product_id.display_name,
                                                        'product_uom_qty':third_supplier_stock_quant.quantity,
                                                        'supplier_id':third_supplier.name.id
                                                    }
                                                    need = need - third_supplier_stock_quant.quantity
                                                    active_rec.order_line = [(0,0,vals)]
                                                    for_supplier = self.env['product.supplierinfo'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id),('priority','=','for')],limit=1)
                                                    if for_supplier:
                                                        for_supplier_stock_quant = self.env['stock.quant'].search([
                                                            ('product_id','=',self.product_id.id),
                                                            ('company_id.partner_id','=',for_supplier.name.id)],limit=1)
                                                        if for_supplier_stock_quant.quantity > 0:
                                                            if need >= for_supplier_stock_quant.quantity:
                                                                vals = {
                                                                    'order_id':active_rec.id,
                                                                    'product_id':self.product_id.id,
                                                                    'name':self.product_id.display_name,
                                                                    'product_uom_qty':for_supplier_stock_quant.quantity,
                                                                    'supplier_id':for_supplier.name.id
                                                                }
                                                                need = need - for_supplier_stock_quant.quantity
                                                                active_rec.order_line = [(0,0,vals)]
                                                                five_supplier = self.env['product.supplierinfo'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id),('priority','=','five')],limit=1)
                                                                if five_supplier:
                                                                    five_supplier_stock_quant = self.env['stock.quant'].search([
                                                                        ('product_id','=',self.product_id.id),
                                                                        ('company_id.partner_id','=',five_supplier.name.id)],limit=1)
                                                                    if for_supplier_stock_quant.quantity > 0:
                                                                        if need >= for_supplier_stock_quant.quantity:
                                                                            vals = {
                                                                                'order_id':active_rec.id,
                                                                                'product_id':self.product_id.id,
                                                                                'name':self.product_id.display_name,
                                                                                'product_uom_qty':five_supplier_stock_quant.quantity,
                                                                                'supplier_id':five_supplier.name.id
                                                                            }
                                                                            need = need - five_supplier_stock_quant.quantity
                                                                            active_rec.order_line = [(0,0,vals)]
                                                                            six_supplier = self.env['product.supplierinfo'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id),('priority','=','six')],limit=1)
                                                                            if six_supplier:
                                                                                six_supplier_stock_quant = self.env['stock.quant'].search([
                                                                                    ('product_id','=',self.product_id.id),
                                                                                    ('company_id.partner_id','=',six_supplier.name.id)],limit=1)
                                                                                if six_supplier_stock_quant.quantity > 0:
                                                                                    if need >= six_supplier_stock_quant.quantity:
                                                                                        vals = {
                                                                                            'order_id':active_rec.id,
                                                                                            'product_id':self.product_id.id,
                                                                                            'name':self.product_id.display_name,
                                                                                            'product_uom_qty':six_supplier_stock_quant.quantity,
                                                                                            'supplier_id':six_supplier.name.id
                                                                                        }
                                                                                        need = need - six_supplier_stock_quant.quantity
                                                                                        active_rec.order_line = [(0,0,vals)]
                                                                                    else:
                                                                                        if need > 0:
                                                                                            vals = {
                                                                                                'order_id':active_rec.id,
                                                                                                'product_id':self.product_id.id,
                                                                                                'name':self.product_id.display_name,
                                                                                                'product_uom_qty':need,
                                                                                                'supplier_id':six_supplier.name.id
                                                                                            }
                                                                                            active_rec.order_line = [(0,0,vals)]
                                                                        else:
                                                                            if need > 0:
                                                                                vals = {
                                                                                    'order_id':active_rec.id,
                                                                                    'product_id':self.product_id.id,
                                                                                    'name':self.product_id.display_name,
                                                                                    'product_uom_qty':need,
                                                                                    'supplier_id':five_supplier.name.id
                                                                                }
                                                                                active_rec.order_line = [(0,0,vals)]
                                                            else:
                                                                if need > 0:
                                                                    vals = {
                                                                        'order_id':active_rec.id,
                                                                        'product_id':self.product_id.id,
                                                                        'name':self.product_id.display_name,
                                                                        'product_uom_qty':need,
                                                                        'supplier_id':for_supplier.name.id
                                                                    }
                                                                    active_rec.order_line = [(0,0,vals)]
                                                else:
                                                    if need > 0:
                                                        vals = {
                                                            'order_id':active_rec.id,
                                                            'product_id':self.product_id.id,
                                                            'name':self.product_id.display_name,
                                                            'product_uom_qty':need,
                                                            'supplier_id':third_supplier.name.id
                                                        }
                                                        active_rec.order_line = [(0,0,vals)]
                                    else:
                                        if need > 0:
                                            vals = {
                                                'order_id':active_rec.id,
                                                'product_id':self.product_id.id,
                                                'name':self.product_id.display_name,
                                                'product_uom_qty':need,
                                                'supplier_id':second_supplier.name.id
                                            }
                                            active_rec.order_line = [(0,0,vals)]

                        else:
                            if need > 0:
                                vals = {
                                    'order_id':active_rec.id,
                                    'product_id':self.product_id.id,
                                    'name':self.product_id.display_name,
                                    'product_uom_qty':need,
                                    'supplier_id':first_supplier.name.id
                                }
                                active_rec.order_line = [(0,0,vals)]
        else:
            first_supplier = self.env['product.supplierinfo'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id),('priority','=','one')],limit=1)
            if first_supplier:
                first_supplier_stock_quant = self.env['stock.quant'].search([
                    ('product_id','=',self.product_id.id),
                    ('company_id.partner_id','=',first_supplier.name.id)],limit=1)
                if first_supplier_stock_quant.quantity > 0:
                    if need >= first_supplier_stock_quant.quantity:
                        vals = {
                            'order_id':active_rec.id,
                            'product_id':self.product_id.id,
                            'name':self.product_id.display_name,
                            'product_uom_qty':first_supplier_stock_quant.quantity,
                            'supplier_id':first_supplier.name.id
                        }
                        need = need - first_supplier_stock_quant.quantity
                        active_rec.order_line = [(0,0,vals)]
                        second_supplier = self.env['product.supplierinfo'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id),('priority','=','two')],limit=1)
                        if second_supplier:
                            second_supplier_stock_quant = self.env['stock.quant'].search([
                                ('product_id','=',self.product_id.id),
                                ('company_id.partner_id','=',second_supplier.name.id)],limit=1)
                            if second_supplier_stock_quant.quantity > 0:
                                if need >= second_supplier_stock_quant.quantity:
                                    vals = {
                                        'order_id':active_rec.id,
                                        'product_id':self.product_id.id,
                                        'name':self.product_id.display_name,
                                        'product_uom_qty':second_supplier_stock_quant.quantity,
                                        'supplier_id':second_supplier.name.id
                                    }
                                    need = need - second_supplier_stock_quant.quantity
                                    active_rec.order_line = [(0,0,vals)]
                                    third_supplier = self.env['product.supplierinfo'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id),('priority','=','three')],limit=1)
                                    if third_supplier:
                                        third_supplier_stock_quant = self.env['stock.quant'].search([
                                            ('product_id','=',self.product_id.id),
                                            ('company_id.partner_id','=',third_supplier.name.id)],limit=1)
                                        if third_supplier_stock_quant.quantity > 0:
                                            if need >= third_supplier_stock_quant.quantity:
                                                vals = {
                                                    'order_id':active_rec.id,
                                                    'product_id':self.product_id.id,
                                                    'name':self.product_id.display_name,
                                                    'product_uom_qty':third_supplier_stock_quant.quantity,
                                                    'supplier_id':third_supplier.name.id
                                                }
                                                need = need - third_supplier_stock_quant.quantity
                                                active_rec.order_line = [(0,0,vals)]
                                                for_supplier = self.env['product.supplierinfo'].search([('product_tmpl_id','=',self.product_id.product_tmpl_i.id),('priority','=','for')],limit=1)
                                                if for_supplier:
                                                    for_supplier_stock_quant = self.env['stock.quant'].search([
                                                        ('product_id','=',self.product_id.id),
                                                        ('company_id.partner_id','=',for_supplier.name.id)],limit=1)
                                                    if for_supplier_stock_quant.quantity > 0:
                                                        if need >= for_supplier_stock_quant.quantity:
                                                            vals = {
                                                                'order_id':active_rec.id,
                                                                'product_id':self.product_id.id,
                                                                'name':self.product_id.display_name,
                                                                'product_uom_qty':for_supplier_stock_quant.quantity,
                                                                'supplier_id':for_supplier.name.id
                                                            }
                                                            need = need - for_supplier_stock_quant.quantity
                                                            active_rec.order_line = [(0,0,vals)]
                                                            five_supplier = self.env['product.supplierinfo'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id),('priority','=','five')],limit=1)
                                                            if five_supplier:
                                                                five_supplier_stock_quant = self.env['stock.quant'].search([
                                                                    ('product_id','=',self.product_id.id),
                                                                    ('company_id.partner_id','=',five_supplier.name.id)],limit=1)
                                                                if for_supplier_stock_quant.quantity > 0:
                                                                    if need >= for_supplier_stock_quant.quantity:
                                                                        vals = {
                                                                            'order_id':active_rec.id,
                                                                            'product_id':self.product_id.id,
                                                                            'name':self.product_id.display_name,
                                                                            'product_uom_qty':five_supplier_stock_quant.quantity,
                                                                            'supplier_id':five_supplier.name.id
                                                                        }
                                                                        need = need - five_supplier_stock_quant.quantity
                                                                        active_rec.order_line = [(0,0,vals)]
                                                                        six_supplier = self.env['product.supplierinfo'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id),('priority','=','six')],limit=1)
                                                                        if six_supplier:
                                                                            six_supplier_stock_quant = self.env['stock.quant'].search([
                                                                                ('product_id','=',self.product_id.id),
                                                                                ('company_id.partner_id','=',six_supplier.name.id)],limit=1)
                                                                            if six_supplier_stock_quant.quantity > 0:
                                                                                if need >= six_supplier_stock_quant.quantity:
                                                                                    vals = {
                                                                                        'order_id':active_rec.id,
                                                                                        'product_id':self.product_id.id,
                                                                                        'name':self.product_id.display_name,
                                                                                        'product_uom_qty':six_supplier_stock_quant.quantity,
                                                                                        'supplier_id':six_supplier.name.id
                                                                                    }
                                                                                    need = need - six_supplier_stock_quant.quantity
                                                                                    active_rec.order_line = [(0,0,vals)]
                                                                                else:
                                                                                    if need > 0:
                                                                                        vals = {
                                                                                            'order_id':active_rec.id,
                                                                                            'product_id':self.product_id.id,
                                                                                            'name':self.product_id.display_name,
                                                                                            'product_uom_qty':need,
                                                                                            'supplier_id':six_supplier.name.id
                                                                                        }
                                                                                        active_rec.order_line = [(0,0,vals)]
                                                                    else:
                                                                        if need > 0:
                                                                            vals = {
                                                                                'order_id':active_rec.id,
                                                                                'product_id':self.product_id.id,
                                                                                'name':self.product_id.display_name,
                                                                                'product_uom_qty':need,
                                                                                'supplier_id':five_supplier.name.id
                                                                            }
                                                                            active_rec.order_line = [(0,0,vals)]
                                                        else:
                                                            if need > 0:
                                                                vals = {
                                                                    'order_id':active_rec.id,
                                                                    'product_id':self.product_id.id,
                                                                    'name':self.product_id.display_name,
                                                                    'product_uom_qty':need,
                                                                    'supplier_id':for_supplier.name.id
                                                                }
                                                                active_rec.order_line = [(0,0,vals)]
                                            else:
                                                if need > 0:
                                                    vals = {
                                                        'order_id':active_rec.id,
                                                        'product_id':self.product_id.id,
                                                        'name':self.product_id.display_name,
                                                        'product_uom_qty':need,
                                                        'supplier_id':third_supplier.name.id
                                                    }
                                                    active_rec.order_line = [(0,0,vals)]
                                else:
                                    if need > 0:
                                        vals = {
                                            'order_id':active_rec.id,
                                            'product_id':self.product_id.id,
                                            'name':self.product_id.display_name,
                                            'product_uom_qty':need,
                                            'supplier_id':second_supplier.name.id
                                        }
                                        active_rec.order_line = [(0,0,vals)]
                    else:
                        if need > 0:
                            vals = {
                                'order_id':active_rec.id,
                                'product_id':self.product_id.id,
                                'name':self.product_id.display_name,
                                'product_uom_qty':need,
                                'supplier_id':first_supplier.name.id
                            }
                            active_rec.order_line = [(0,0,vals)]
        return True