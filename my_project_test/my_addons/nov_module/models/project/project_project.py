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

    customer_ids = fields.Many2many(
        string='Customers',
        comodel_name='res.partner',
        relation='res_partner_project_rel',
        column1='project_id',
        column2='parent_id',
        domain=[('customer','=',True), ]
    )