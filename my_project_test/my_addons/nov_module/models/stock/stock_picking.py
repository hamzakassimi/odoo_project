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
        selection='get_selection_additional_state'
    )

    # ------------------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------------------

    @api.model
    def get_selection_additional_state(self):
        return [
            ('good_for_loading', _('Goods for loading')),
            ('good_on_move', _('Goods On Move')),
            ('at_the_carrier', _('At The Carrier')),
        ]