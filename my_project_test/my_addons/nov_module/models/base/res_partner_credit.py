# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)
 
class ResPartnerCredit(models.Model):
    _name = 'res.partner.credit'
    _rec_name = 'name'

    # ------------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------------
 
    name = fields.Char(
        string='Name',
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
    )

    requested_client_limit = fields.Float(
        string='Requested Client Limit',
    )
    
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
    )

    reason = fields.Text(
        string='Reason Of Request',
        translate=True
    )

    ca_client = fields.Float(
        string='CA Client',
    )

    state = fields.Selection(
        string='State',
        default='draft',
        selection='get_selection_state'
    )

    # ------------------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------------------

    @api.model
    def get_selection_state(self):
        return [
            ('draft', _('Draft')),
            ('validated', _('Validated'))
        ]

    @api.multi
    def button_validate_partner_credit(self):
        for record in self:
            partner_credit = self.env['res.partner.credit'].search([('company_id','=',record.company_id.id),('partner_id','=',record.partner_id.id),('id','!=',record.id)],limit=1)
            if partner_credit:
                partner_credit.unlink()
            record.write({'state':'validated'})

    @api.model
    def create(self, values):
        seq = self.env['ir.sequence'].next_by_code('partner_credit_limit')
        values.update({
            'name': seq
        })
        return super(ResPartnerCredit, self).create(values)