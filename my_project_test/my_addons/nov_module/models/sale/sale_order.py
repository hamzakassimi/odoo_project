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

    project_id = fields.Many2one(
        string='Project',
        comodel_name='project.project',
    )

    warehouse_id = fields.Many2one(
        string='Warehouse',
        required=True,
        comodel_name='stock.warehouse',
    )

    pricelist_id = fields.Many2one(
        string='Pricelist',
        required=True,
        comodel_name='product.pricelist',
    )

    is_public = fields.Boolean(
        string='Is Public',
        default=False,
    )

    # ------------------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------------------

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id_product(self):
        res = {}
        sale_orders = self.env['sale.order'].search([('partner_id','=',self.partner_id.id)])
        product = ''
        if sale_orders:
            for line in sale_orders[0].order_line:
                product += '\n' + line.product_id.name
            msg = _("Those are the last products bought by this customer :" + product)
            res['warning'] = {
                'title': _("Customer Products Reminder!"),
                'message': msg,
            }
        return res

    @api.multi
    @api.onchange('project_id')
    def onchange_project_id(self):
        if self.project_id:
            if self.project_id.pricelist_id.id:
                self.pricelist_id = self.project_id.pricelist_id.id
            if self.project_id.warehouse_id:
                self.warehouse_id = self.project_id.warehouse_id
    
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
            current_company = self.env['res.users'].sudo().browse(self._uid).company_id
            totals_amount = 0.0
            total_invoices = 0.0
            compnies = []
            related_partner_credit = self.env['res.partner.credit'].search([('partner_id','=',record.partner_id.id),('company_id','=',current_company.id)],limit=1)
            related_sales = self.env['sale.order'].search([('partner_id','=',record.partner_id.id),('state','=','sale')])
            if record.partner_id.state != 'validated':
                raise ValidationError(_('you can not confirm a sale order for non validated customer'))
            if record.partner_id.compte=='au_compte':
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
                if not related_partner_credit:
                    raise ValidationError(_('There is no partner credit for this customer in this company,please ask for partner credit !'))
                for credit in record.partner_id.partner_credits_ids:
                    if total_deduced >= credit.requested_client_limit:
                        record._notify_email_overdrawn_partner_credit()
                        raise ValidationError(_('the amount total of partner SOs is great than the customer limit :%s , in the comapny %s ') %(str(credit.requested_client_limit) ,credit.company_id.name))
        return super(SaleOrder, self)._action_confirm()

    @api.model
    def create(self, vals):
        result = super(SaleOrder, self).create(vals)
        public_pricelist = self.env.ref('product.list0')
        if result.project_id:
            if result.project_id.customer_ids:
                if not result.partner_id in result.project_id.customer_ids:
                    raise ValidationError(_('This customer dont figure out in the list of customers of the your project!'))
        if result.partner_id.state=='no_validated' and result.pricelist_id.id != public_pricelist.id:
            result.is_public = True
        for line in result.order_line:
            if line.discount!=0.0:
                result.is_public = True
        return result

    @api.multi
    def write(self,vals):
        public_pricelist = self.env.ref('product.list0')
        if self.project_id:
            if self.project_id.customer_ids:
                if not self.partner_id in self.project_id.customer_ids:
                    raise ValidationError(_('This customer dont figure out in the list of customers of the your project!'))
        if self.partner_id.state=='no_validated' and self.pricelist_id.id != public_pricelist.id:
            vals.update({
                'is_public': True
            })
        else:
            vals.update({
                'is_public': False
            })
        for line in self.order_line:
            if line.discount != 0.0:
                print('+++',line.discount)
                vals.update({
                    'is_public': True
                })
            else:
                vals.update({
                    'is_public': False
                })
        return super(SaleOrder, self).write(vals)

    @api.multi
    def button_validate(self):
        for record in self:
            record.write({'is_public':False})