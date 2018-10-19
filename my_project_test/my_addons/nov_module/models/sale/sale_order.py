# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # ------------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------------


    # ------------------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------------------

    @api.multi
    def _action_confirm(self):
        for record in self:
            if record.partner_id.state != 'validated':
                raise ValidationError(_('you can not confirm an so for non validated customer'))
            if record.partner_id.limit_customer < record.amount_total:
                raise ValidationError(_('the customer limit is less than the amount total of this SO'))
        return super(SaleOrder, self)._action_confirm()