# -*- coding: utf-8 -*-
{
    'name': "Import to FACTS",

    'summary': """ Tool for the importation from ODOO to FACTS """,

    'description': """
        Common models for eduwebgroup school modules
    """,

    'author': "Eduwebgroup",
    'website': "http://www.eduwebgroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Admission',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'school_base', 'mail', 'website', 'contacts', 'adm'],

    # always loaded
    'data': [
        'views/res_config_settings_views.xml',
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    'demo':[]
}
