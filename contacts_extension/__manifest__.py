# -*- coding: utf-8 -*-
{
    'name': "Contacts Extension Arg",

    'summary': """
        Agrega campos de loc argentina en la vista kamban""",

    'description': """
        
    """,

    'author': "Calyx",
    'website': "http://www.calyxservicios.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'l10n_ar_partner', 'l10n_ar_account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner_kanban_view.xml',
        'views/res_company_view.xml',
        'data/data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}