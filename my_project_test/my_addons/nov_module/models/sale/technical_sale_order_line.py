# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class TechnicalSaleOrderLine(models.Model):
    _name = 'technical.sale.order.line'
    _order = 'technical_sale_id, id'

    # ------------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------------

    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product",
    )

    product_uom_qty = fields.Float(string='Quantity')

    product_uom = fields.Many2one(
        comodel_name = 'product.uom',
        string= "Unit Of Measure",
    )

    price_unit = fields.Float(string='Unit Price')

    tax_id = fields.Many2many(
        comodel_name = 'account.tax', 
        string='Taxes', 
        domain=['|', ('active', '=', False), ('active', '=', True)]
    )

    price_subtotal = fields.Monetary(string='Subtotal')

    price_total = fields.Monetary(string='Total')

    technical_sale_id = fields.Many2one(
        comodel_name = 'sale.order',
        string='Technical Order',
    )

    currency_id = fields.Many2one(
        comodel_name = 'res.currency',
        string='Currency',
    )