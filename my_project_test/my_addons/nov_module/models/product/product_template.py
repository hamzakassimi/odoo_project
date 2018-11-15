# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # ------------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------------

    manufacturer = fields.Char(
        string='Manufacturer',
    )

    serie = fields.Char(
        string='Serie',
    )

    Model = fields.Char(
        string='Model',
    )

    specific = fields.Char(
        string='Specific',
    )
