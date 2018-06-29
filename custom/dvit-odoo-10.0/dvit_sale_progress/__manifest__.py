# -*- coding: utf-8 -*-
{
    'name': 'Sale progress',
    'summary': 'Tracking of sale order delivery and invoice progress and percentage.',
    'description': """
    Allow Tracking of sale order delivery and invoice progress and percentage
    based on lines' progress for delivered and invoiced qty vs. orderd qty.
    """,
    'version': '10.0.1.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'author': "DVIT.ME",
    'website': 'http://dvit.me/',
    'depends': ['sale','stock'],
    'data': ['views/templates.xml',],
    "images": [
        'static/description/banner.png'
    ],
    'installable': True,
}
