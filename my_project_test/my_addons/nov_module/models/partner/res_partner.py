# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)
 
class ResPartner(models.Model):
    _inherit = 'res.partner'

    # ------------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------------

    compte = fields.Selection(
        string='Compte',
        selection='get_selection_compte'
    )

    ice = fields.Char(
        string='ICE',
    )

    rc = fields.Char(
        string='RC',
    )

    cnss = fields.Char(
        string='CNSS',
    )

    state = fields.Selection(
        string='State',
        default='no_validated',
        selection='get_selection_state'
    )


    # ------------------------------------------------------------------------
    # CONSTRAINTS
    # ------------------------------------------------------------------------

    _sql_constraints = [
        ('ice', 'UNIQUE(ice)', 'ICE must be unique!'),
        ('rc', 'UNIQUE(rc)', 'RC must be unique!'),
    ]

    # ------------------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------------------

    @api.model
    def get_selection_compte(self):
        return [
            ('au_compte', _('Au Compte')),
            ('au_comptant', _('Au Comptant'))
        ]

    @api.model
    def get_selection_state(self):
        return [
            ('no_validated', _('No Validated')),
            ('validated', _('Validated'))
        ]
    
    @api.multi
    def button_validate_partner(self):
        for record in self:
            if not record.:

            return True


