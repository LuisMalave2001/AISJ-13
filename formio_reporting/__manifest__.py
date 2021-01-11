# -*- coding: utf-8 -*-
{
    'name': 'Form.io Reporting',

    'summary': """ Form.io Reporting """,

    'description': """
        Form.io Reporting
    """,

    'author': 'Eduwebgroup',
    'website': 'http://www.eduwebgroup.com',

    'category': 'Extra Tools',
    'version': '1.0',

    'depends': [
        'formio',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/formio_form_report_views.xml',
        'views/formio_form_views.xml',
    ],
}