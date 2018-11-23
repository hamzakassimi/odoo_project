# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime
from dateutil.relativedelta import relativedelta

import logging

_logger = logging.getLogger(__name__)

class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    def _make_po_select_supplier(self, values, suppliers):
        """ Method intended to be overridden by customized modules to implement any logic in the
            selection of supplier.
        """
        warehouse_supplier = values['warehouse_id']['supplier_id']
        product_supplier = self.env['product.supplierinfo'].search([('name','=',warehouse_supplier.id)],limit=1)
        if product_supplier:
            if values['warehouse_id']['flag'] == True:
                return product_supplier
            else:
                if 'move_dest_ids' in values.keys():
                    sale_order_line =  values['move_dest_ids']['sale_line_id']
                    related_supplier = self.env['product.supplierinfo'].search([('name','=',sale_order_line.supplier_id.id)],limit=1)
                    if related_supplier:
                        return related_supplier
                    else:
                        raise ValidationError(_('No supplier Defined in the line of sale order!please define.'))
        return super(ProcurementRule,self)._make_po_select_supplier(values,suppliers)