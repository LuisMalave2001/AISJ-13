# -*- coding: utf-8 -*-
{
    'name': 'Admissions Form.io',

    'summary': """ Admissions Form.io """,

    'description': """
        Admissions Form.io
    """,

    'author': 'Eduwebgroup',
    'website': 'http://www.eduwebgroup.com',

    'category': 'Extra Tools',
    'version': '1.0',

    'depends': [
        'base',
        'formio_extends',
        'adm',
        'school_base',
        ],

    'data': [
        'views/adm_application_views.xml',
        'views/adm_inquiry_views.xml',
        'views/adm_application_templates.xml',

        'data/mail_template_data.xml',
        'data/formio_automation_data.xml',
        'data/base_automation_data.xml',
        ],
    }
