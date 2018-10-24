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
    def _notify_email_overdrawn_partner_credit(self):
        for record in self:
            template = self.env.ref('nov_module.email_template_overdrawn_partner_credit')
            try:
                template.send_mail(record.id,force_send=True)
            except Exception as exp:
                self.env.cr.rollback()
                _logger.error('Failed to Send mail of overdrawn Partner Credit')
                _logger.error(str(exp))
        return True

    @api.multi
    def _action_confirm(self):
        for record in self:
            totals_amount = 0.0
            total_invoices = 0.0
            related_sales = self.env['sale.order'].search([('partner_id','=',record.partner_id.id),('state','=','sale')])
            if record.partner_id.state != 'validated':
                raise ValidationError(_('you can not confirm a sale order for non validated customer'))
            if related_sales:
                for order in related_sales:
                    totals_amount += order.amount_total
                    if order.invoice_ids:
                        for invoice in order.invoice_ids:
                            if invoice.state=='paid':
                                total_invoices += invoice.amount_total
                            else:
                                total_invoices = 0.0
                    else:
                        total_invoices = 0.0
            else:
                totals_amount = 0.0
            amounts = totals_amount + record.amount_total
            total_deduced = amounts - total_invoices
            for credit in record.partner_id.partner_credits_ids:
                if total_deduced >= credit.partner_credit:
                    record._notify_email_overdrawn_partner_credit()
                    raise ValidationError(_('the amount total of partner SOs is great than the customer limit :%s , in the comapny %s ') %(str(credit.partner_credit) ,credit.company_id.name))
            for line in record.order_line:
                if line.discount != 0.0:
                    raise ValidationError(_('You can not confirm so with discount you should first ask for validation  from sale manager'))
        return super(SaleOrder, self)._action_confirm()