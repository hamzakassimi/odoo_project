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

    @api.model
    def create(self,values):
        res = super(SaleOrder, self).create(values)
        if res.partner_id.state != 'validated':
            raise ValidationError(_('you can not create a so for non validated customer'))
        return res

    @api.multi
    def write(self,values):
        res =  super(SaleOrder, self).write(values)
        for record in self:
            if record.partner_id.state != 'validated':
                raise ValidationError(_('you can not create a so for non validated customer'))
            return res

