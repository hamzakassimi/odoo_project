# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'

    # ------------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------------

    quantity_to_be_prepared = fields.Float(
        string='Qty To Be Prepared',
    )

    is_good = fields.Boolean(
        string='Is good',
        compute='_compute_is_good',
        store=True,
        help="Technical field to make Qty To Be Prepared readonly"
    )

    # ------------------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------------------

    @api.multi
    @api.depends('picking_id','picking_id.additional_state')
    def _compute_is_good(self):
        for record in self:
            if record.picking_id and record.picking_id.additional_state=='good_for_loading':
                record.is_good = True
            else:
                record.is_good = False
