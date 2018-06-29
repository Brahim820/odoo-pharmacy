# -*- coding: utf-8 -*-
{
    'name': "Sale optional lines",

    'summary': """add optional products to sale order""",
    'author': "DVIT.ME",
    'website': "http://dvit.me",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/report.xml',
    ],

}
