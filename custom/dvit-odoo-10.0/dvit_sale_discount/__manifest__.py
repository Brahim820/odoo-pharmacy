# -*- coding: utf-8 -*-
{
    'name': 'Sale Discount',
    'version': '1.0',
    'category': 'Sales',
    'summary': "Show Discount Total and Total before Discount on Sales. ",
    'description':"Show Discount Total and Total before Discount on Sales.",
    'license': 'AGPL-3',
    'author': "DVIT.ME",
    'website': 'http://dvit.me/',
    "depends": ['dvit_sale_report'],
    'data': [
        'views/views.xml',
        'views/report.xml',
    ],
    "images": [
        'static/description/banner.png'
    ],
    'installable': True,
}
