# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    # ------------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------------

    supplier_id = fields.Many2one(
        string='Supplier',
        comodel_name='res.partner',
        domain=[('supplier','=',True)],
    )
    flag = fields.Boolean(
        string='Flag',
    )