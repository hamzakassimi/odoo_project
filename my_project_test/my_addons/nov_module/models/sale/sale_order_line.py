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