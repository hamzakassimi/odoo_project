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
            if not record.compte:
                raise ValidationError(_('no compte specified for the client : %s')  % (record.name))
            elif not record.street and \
             not record.city and\
             not record.country_id:
                raise ValidationError(_('no adress specified for the client : %s')  % (record.name))
            elif not record.email:
                raise ValidationError(_('no email specified for the client : %s')  % (record.name))
            elif not record.phone:
                raise ValidationError(_('no phone specified for the client : %s')  % (record.name))
            elif not record.ice:
                raise ValidationError(_('no ICE specified for the client : %s')  % (record.name))
            elif not record.rc:
                raise ValidationError(_('no RC specified for the client : %s')  % (record.name))
            elif not record.cnss:
                raise ValidationError(_('no CNSS specified for the client : %s')  % (record.name))
            elif not record.category_id:
                raise ValidationError(_('no tags specified for the client : %s')  % (record.name))
            elif record.child_ids:
                for child in record.child_ids:
                    if child.type=='contact':
                        if not child.compte:
                            raise ValidationError(_('no compte specified for the contact : %s')  % (child.name))
                        elif not child.email:
                            raise ValidationError(_('no email specified for the contact : %s')  % (child.name))
                        elif not child.phone:
                            raise ValidationError(_('no phone specified for the contact : %s')  % (child.name))
                        elif not child.ice:
                            raise ValidationError(_('no ICE specified for the contact : %s')  % (child.name))
                        elif not child.rc:
                            raise ValidationError(_('no RC specified for the contact : %s')  % (child.name))
                        elif not child.cnss:
                            raise ValidationError(_('no CNSS specified for the contact : %s')  % (child.name))
                    elif child.type=='invoice':
                        if not child.compte:
                            raise ValidationError(_('no compte specified for the contact : %s')  % (child.name))
                        elif not child.email:
                            raise ValidationError(_('no email specified for the contact : %s')  % (child.name))
                        elif not child.phone:
                            raise ValidationError(_('no phone specified for the contact : %s')  % (child.name))
                        elif not child.ice:
                            raise ValidationError(_('no ICE specified for the contact : %s')  % (child.name))
                        elif not child.rc:
                            raise ValidationError(_('no RC specified for the contact : %s')  % (child.name))
                        elif not child.cnss:
                            raise ValidationError(_('no CNSS specified for the contact : %s')  % (child.name))
                        elif not child.street and \
                         not child.city and\
                         not child.country_id:
                            raise ValidationError(_('no adress specified for the contact : %s')  % (child.name))
                    elif child.type=='delivery':
                        if not child.compte:
                            raise ValidationError(_('no compte specified for the contact : %s')  % (child.name))
                        elif not child.email:
                            raise ValidationError(_('no email specified for the contact : %s')  % (child.name))
                        elif not child.phone:
                            raise ValidationError(_('no phone specified for the contact : %s')  % (child.name))
                        elif not child.ice:
                            raise ValidationError(_('no ICE specified for the contact : %s')  % (child.name))
                        elif not child.rc:
                            raise ValidationError(_('no RC specified for the contact : %s')  % (child.name))
                        elif not child.cnss:
                            raise ValidationError(_('no CNSS specified for the contact : %s')  % (child.name))
                        elif not child.street and \
                         not child.city and\
                         not child.country_id:
                            raise ValidationError(_('no adress specified for the contact : %s')  % (child.name))
                    record.write({'state':'validated'})
            else:
                record.write({'state':'validated'})