# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError

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
            return suppliers[0]