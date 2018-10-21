# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)
 
class ResPartnerCredit(models.Model):
    _name = 'res.partner.credit'

    # ------------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------------

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner Id',
    )

    partner_credit = fields.Float(
        string='Partner Credit',
    )
    
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company Id',
    )