# -*- coding: utf-8 -*-
from odoo import http

# class NovModule(http.Controller):
#     @http.route('/nov_module/nov_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nov_module/nov_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nov_module.listing', {
#             'root': '/nov_module/nov_module',
#             'objects': http.request.env['nov_module.nov_module'].search([]),
#         })

#     @http.route('/nov_module/nov_module/objects/<model("nov_module.nov_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nov_module.object', {
#             'object': obj
#         })