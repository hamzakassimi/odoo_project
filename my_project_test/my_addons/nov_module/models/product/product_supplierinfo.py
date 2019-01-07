# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    # ------------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------------
	
    priority = fields.Selection(
        string='Priority',
        selection='get_selection_priority'
    )

    @api.model
    def get_selection_priority(self):
        return [
            ('one', _('1')),
            ('two', _('2')),
            ('three', _('3')),
            ('for', _('4')),
            ('five', _('5')),
            ('six', _('6')),
        ]