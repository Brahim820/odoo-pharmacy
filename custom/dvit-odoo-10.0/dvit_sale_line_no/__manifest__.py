# -*- coding: utf-8 -*-
{
    'name': "sale line no",

    'summary': """Sale line manual number""",

    'author': "DVIT.ME",
    'website': "http://www.dvit.me",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/report.xml',
    ],

}
