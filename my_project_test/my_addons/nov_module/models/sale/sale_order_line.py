# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime,timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

import logging

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    # ------------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------------
     
    warehouse_quantities = fields.Text(
        string='Warehouses quantities',
    )

    supplier_id = fields.Many2one(
        comodel_name='res.partner',
        string='Supplier',
        domain=[('supplier','=',True)]
    )

    # ------------------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------------------

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