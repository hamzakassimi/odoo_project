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
            totals_amount = 0.0
            related_sales = self.env['sale.order'].search([('partner_id','=',record.partner_id.id),('state','=','sale')])
            if record.partner_id.state != 'validated':
                raise ValidationError(_('you can not confirm a sale order for non validated customer'))
            if related_sales:
                for so in related_sales:
                    totals_amount += so.amount_total
            else:
                totals_amount = 0.0
            for credit in record.partner_id.partner_credits_ids:
                if (totals_amount + record.amount_total) <= credit.partner_credit:
                    raise ValidationError(_('the amount total of partner SOs is less than the customer limit :%s , in the comapny %s ') %(str(credit.partner_credit) ,credit.company_id.name))
        return super(SaleOrder, self)._action_confirm()