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
        for supplier in suppliers:
            if supplier.name.id == warehouse_supplier.id and values['warehouse_id']['flag'] == True:
                return supplier
            else:
                raise UserError(_('The vendor associated to your warehouse is not configured in vendors of  your products ,Please define it for your products.'))