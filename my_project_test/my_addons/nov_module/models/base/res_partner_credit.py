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

    total_so = fields.Float(
        string='Total SO',
        compute='_compute_total_so',
    )

    total_so_payed = fields.Float(
        string='Total SO Payed',
        compute='_compute_total_so',

    )

    total_so_no_payed = fields.Float(
        string='Total SO No Payed',
        compute='_compute_total_so',
    )

    # ------------------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------------------

    @api.model
    def get_selection_state(self):
        return [
            ('draft', _('Draft')),
            ('validated_r_a', _('Validated R.A')),
            ('validated_dg', _('Validation DG')),
        ]

    @api.multi
    def button_validate_dg(self):
        for record in self:
            partner_credit = self.env['res.partner.credit'].search([('company_id','=',record.company_id.id),('partner_id','=',record.partner_id.id),('id','!=',record.id)],limit=1)
            if partner_credit:
                partner_credit.unlink()
            record.write({'state':'validated_dg'})

    @api.multi
    def button_validate_ra(self):
        for record in self:
            record.write({'state':'validated_r_a'})

    @api.model
    def create(self, values):
        seq = self.env['ir.sequence'].next_by_code('partner_credit_limit')
        values.update({
            'name': seq
        })
        return super(ResPartnerCredit, self).create(values)

    @api.multi
    @api.depends('partner_id')
    def _compute_total_so(self):
        for record in self:
            total_so = 0.0
            total_so_payed = 0.0
            total_so_no_payed = 0.0
            related_so = self.env['sale.order'].search([('partner_id','=',record.partner_id.id)])
            for so in related_so:
                total_so += so.amount_total
                if so.invoice_ids:
                    for invoice in so.invoice_ids:
                        if invoice.state=='paid':
                            total_so_payed += invoice.amount_total
                        else:
                            total_so_no_payed += invoice.amount_total
                else:
                    total_so_no_payed += so.amount_total
            record.total_so = total_so
            record.total_so_no_payed = total_so_no_payed
            record.total_so_payed = total_so_payed