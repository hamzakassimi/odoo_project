# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # ------------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------------

    additional_state = fields.Selection(
        string='Additional States',
        default='waiting',
        selection='get_selection_additional_state',
    )

    carrier_type = fields.Selection(
        string='Carrier Type',
        selection='get_selection_carrier_type',
    )

    warehouse_man_id = fields.Many2one(
        comodel_name='hr.employee',
        string='WarehouseMan',
    )

    charger_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Charger',
    )

    magasinier_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Magasinier',
    )

    clariste_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Clariste',
    )

    ouvrier_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Ouvrier',
    )

    # ------------------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------------------

    @api.model
    def get_selection_additional_state(self):
        return [
            ('waiting', _('Waiting')),
            ('good_for_loading', _('Goods for loading')),
            ('ready',_('Ready')),
            ('good_on_move', _('Goods On Move')),
            ('at_the_carrier', _('At The Carrier')),
            ('received_by_client',_('Recievd By Client')),
        ]

    @api.model
    def get_selection_carrier_type(self):
        return [
            ('by_our_self', _('Par Nos Soins')),
            ('by_carrier', _('Par Transporteur')),
            ('client',_('Client')),
        ]

    @api.multi
    def button_load_goods(self):
        for record in self:
            for move in record.move_lines:
                if move.quantity_to_be_prepared<=move.product_uom_qty and record.carrier_type:
                    return self.write({'additional_state':'good_for_loading'})
                else:
                    raise ValidationError(_('you can not load goods for quantity to be prepared great than initial demand or carrier type not set,please verifie!'))
    
    @api.multi
    def button_ready(self):
        for record in self:
            for move in record.move_lines:
                if move.quantity_done==move.quantity_to_be_prepared:
                    return self.write({'additional_state':'ready'})
                else:
                    raise ValidationError(_('you can not process ready button  if quantity done is not equal to quantity to be prepared'))
    
    @api.multi
    def button_good_on_move(self):
        return self.write({'additional_state':'good_on_move'})

    @api.multi
    def button_at_the_carrier(self):
        return self.write({'additional_state':'at_the_carrier'})

    @api.multi
    def button_received_by_client(self):
        return self.write({'additional_state':'received_by_client'})