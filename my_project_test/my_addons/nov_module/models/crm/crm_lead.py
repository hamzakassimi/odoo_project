# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'


    # ------------------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------------------
    
    @api.multi
    def action_set_won(self):
    	project_env = self.env['project.project']
    	for record in self:
    		project_env.create({
    			'name':record.name,
    			'partner_id':record.partner_id.id
    			})
    		return super(CrmLead,self).action_set_won()