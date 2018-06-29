# -*- coding: utf-8 -*-
{
    'name': "PosBoxLess Arabic Restaurant and Kitchen Receipt",

    'summary': """ This module enables arabic printing for Restaurant and Kitchen receipt Using Network Printer(PosBoxlesss).
        """,

    'description': """
        
    """,

    'author': "Ad Mk Joseph",
    'website': "",
    'category': 'Generic Modules',
    'version': '1.0',
    'price': 130.0,
    'currency': 'EUR',
    'depends': ['pos_restaurant', 'point_of_sale'],


    'data': [
        'views/malik.xml',
        'views/malik_v.xml',
    ],
    'images': [
        'static/description/rest_receipt_new.png',
    ],

    'demo': [
        #'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
