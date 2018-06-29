# -*- coding: utf-8 -*-
{
    'name': "Alternative Product Sale Order",

    'summary': """
      Alternative Product Sale Order""",

    'author': "DVIT.ME",
    'website': "http://www.dvit.com",

    'category': 'sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'views/views.xml',
        'reports/sale_report.xml',
    ],

}
