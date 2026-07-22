# -*- coding: utf-8 -*-
{
    'name': "kio_invoice_email_template",

    'summary': "Static customer invoice email template",

    'description': """
Static invoice email template for Samaa Al Awir Vegetables & Fruits Trading LLC.
    """,

    'author': "Samaa Al Awir Vegetables & Fruits Trading LLC",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '17.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['account', 'mail', 'sale'],

    # always loaded
    'data': [
        'data/ir_sequence.xml',
        'data/mail_template.xml',
        'data/server_action.xml',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
