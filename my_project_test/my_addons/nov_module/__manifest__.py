# -*- coding: utf-8 -*-
{
    'name': "nov_module",

    'summary': """
        nov_module""",

    'description': """
        nov_module
    """,

    'author': "Fouzia BENJARRARI",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','sale_management',],

    # always loaded
    'data': [
        #data
        'data/mail_notification_data.xml',

        #security
        'security/ir.model.access.csv',

        #views
        'views/base/res_partner_views.xml',
        'views/stock/stock_warehouse_views.xml',
        'views/sale/sale_order_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}