# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

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

    ice = fields.Integer(
        string='ICE',
    )

    rc = fields.Integer(
        string='RC',
    )

    cnss = fields.Integer(
        string='CNSS',
    )

    state = fields.Selection(
        string='State',
        default='no_validated',
        selection='get_selection_state'
    )

    partner_credits_ids = fields.One2many(
        string='Partner Credits',
        required=True,
        comodel_name='res.partner.credit',
        inverse_name='partner_id',
    )

    project_ids = fields.Many2many(
        string='Projects',
        comodel_name='project.project',
        relation='res_partner_project_rel',
        column1='parent_id',
        column2='project_id',
    )


    # ------------------------------------------------------------------------
    # CONSTRAINTS
    # ------------------------------------------------------------------------

    _sql_constraints = [
        ('ice', 'UNIQUE(ice)', 'ICE must be unique!'),
        ('rc', 'UNIQUE(rc)', 'RC must be unique!'),
        ('cnss', 'UNIQUE(cnss)', 'CNSS must be unique!'),
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
            if not record.compte:
                raise ValidationError(_('No compte specified for the client : %s')  % (record.name))
            elif not record.street and \
             not record.city and\
             not record.country_id:
                raise ValidationError(_('No address specified for the client : %s')  % (record.name))
            elif record.compte=="au_compte":
                if not record.ice:
                    raise ValidationError(_('No ICE specified for the client : %s')  % (record.name))
                elif not record.rc:
                    raise ValidationError(_('No RC specified for the client : %s')  % (record.name))
                elif not record.cnss:
                    raise ValidationError(_('No CNSS specified for the client : %s')  % (record.name))
                elif not record.category_id:
                    raise ValidationError(_('No tags specified for the client : %s')  % (record.name))
                elif record.child_ids:
                    for child in record.child_ids:
                        if child.type=='contact':
                            if not child.email:
                                raise ValidationError(_('No email specified for the contact : %s')  % (child.name))
                            elif not child.phone:
                                raise ValidationError(_('No phone specified for the contact : %s')  % (child.name))
                        record.write({'state':'validated'})
            elif record.child_ids:
                for child in record.child_ids:
                    if child.type=='contact':
                        if not child.email:
                            raise ValidationError(_('No email specified for the contact : %s')  % (child.name))
                        elif not child.phone:
                            raise ValidationError(_('No phone specified for the contact : %s')  % (child.name))
                    record.write({'state':'validated'})
            else:
                record.write({'state':'validated'})