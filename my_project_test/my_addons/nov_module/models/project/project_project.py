# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class ProjectProject(models.Model):
    _inherit = 'project.project'

     # ------------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------------

    warehouse_id = fields.Many2one(
        string='Warehouse',
        comodel_name='stock.warehouse',
    )

    pricelist_id = fields.Many2one(
        string='Pricelist',
        comodel_name='product.pricelist',
    )

    customer_ids = field_name = fields.One2many(
        string='Related Customers',
        comodel_name='res.partner',
        inverse_name='project_id',
        domain=[('customer','=',True)],
    )