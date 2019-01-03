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
        domain=[('state','=','validated_dg')]
    )

    project_ids = fields.Many2many(
        string='Projects',
        comodel_name='project.project',
        relation='res_partner_project_rel',
        column1='parent_id',
        column2='project_id',
    )

    rc_city = fields.Char(
        string='RC City',
    )


    # ------------------------------------------------------------------------
    # CONSTRAINTS
    # ------------------------------------------------------------------------

    _sql_constraints = [
        ('ice', 'UNIQUE(ice)', 'ICE must be unique!'),
        ('rc', 'UNIQUE(rc,rc_city)', 'RC must be unique per city!'),
        ('cnss', 'UNIQUE(cnss)', 'CNSS must be unique!'),
    ]

    # ------------------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------------------

    @api.constrains('rc','cnss','ice')
    def check_ice_cnss_rc(self):
        if self.compte=='au_compte':
            related_ice = self.env['res.partner'].search([('id','!=',self.id),('ice','=',self.ice)])
            related_rc = self.env['res.partner'].search([('id','!=',self.id),('rc','=',self.rc)])
            related_cnss = self.env['res.partner'].search([('id','!=',self.id),('cnss','=',self.cnss)])
            if len(related_ice)>1:
                raise ValidationError(_('ICE must be unique!'))
            if len(related_rc)>1:
                raise ValidationError(_('RC must be unique!'))
            if len(related_cnss)>1:
                raise ValidationError(_('CNSS must be unique!'))
            if len(str(self.rc))!=6:
                raise ValidationError(_('RC cannot be great or less than 6'))
            if len(str(self.cnss))!=6:
                raise ValidationError(_('CNSS cannot be great or less than 6'))

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
                elif not record.child_ids:
                    raise ValidationError(_('No contacts specified for the client : %s')  % (record.name))
                elif record.child_ids:
                    for child in record.child_ids:
                        if child.type=='contact':
                            if not child.email:
                                raise ValidationError(_('No email specified for the contact : %s')  % (child.name))
                            elif not child.phone:
                                raise ValidationError(_('No phone specified for the contact : %s')  % (child.name))
                            elif not child.name:
                                raise ValidationError(_('No name specified for the contact : %s')  % (child.name))
                            record.write({'state':'validated'})
                        elif child.type =='invoice':
                            if not child.email:
                                raise ValidationError(_('No email specified for the contact : %s')  % (child.name))
                            elif not child.phone:
                                raise ValidationError(_('No phone specified for the contact : %s')  % (child.name))
                            elif not child.street and \
                             not child.city and\
                             not child.country_id:
                                raise ValidationError(_('No address specified for the client : %s')  % (child.name))
                            elif not child.name:
                                raise ValidationError(_('No name specified for the contact : %s')  % (child.name))
                            record.write({'state':'validated'})
                        if child.type == 'delivery':
                            if not child.email:
                                raise ValidationError(_('No email specified for the contact : %s')  % (child.name))
                            elif not child.phone:
                                raise ValidationError(_('No phone specified for the contact : %s')  % (child.name))
                            elif not child.street and \
                             not child.city and\
                             not child.country_id:
                                raise ValidationError(_('No address specified for the client : %s')  % (child.name))
                            elif not child.name:
                                raise ValidationError(_('No name specified for the contact : %s')  % (child.name))
                            record.write({'state':'validated'})
                else:
                    record.write({'state':'validated'})
            elif record.compte=="au_comptant":
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