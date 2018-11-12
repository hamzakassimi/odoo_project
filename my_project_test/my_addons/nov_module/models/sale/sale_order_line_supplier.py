# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class SaleOrderLineSupplier(models.Model):
    _name = 'sale.order.line.supplier'
    _rec_name = 'supplier_id'

    line_id = fields.Many2one(
        string='Order Line',
        comodel_name='sale.order.line',
    )

    supplier_id = fields.Many2one(
        string='Supplier',
        comodel_name='res.partner',
        domain=[('supplier','=',True)],
    )

    qty = fields.Float(
        string='Quantity',
    )