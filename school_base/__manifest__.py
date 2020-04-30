# -*- coding: utf-8 -*-
{
    'name': "School Base",

    'summary': """ Common models for eduwebgroup school modules as School Year, Grade Level, etc... """,

    'description': """
        Common models for eduwebgroup school modules
    """,

    'author': "Eduwebgroup",
    'website': "http://www.eduwebgroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '0.4.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'portal',
        'contacts',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/menudata.xml',
        'views/res_partner_view.xml',
        'views/portal_views.xml',
        'views/views.xml'
    ],
}