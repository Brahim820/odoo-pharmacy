# -*- coding: utf-8 -*-
{
    'name': 'Integration & enhancement module for sale_report_hide_price ',
    'category': 'Sales Management',
    'author': "DVIT.ME",
    'website': 'http://dvit.me/',
    'version': '10.0.1.0.1',
    'license': 'AGPL-3',
    'summary': 'Integrate sale_report_hide_price and dvit_sale_discount',
    'depends': ['dvit_sale_discount','sale_report_hide_price'],
    'data': [
             'views/report_saleorder.xml'
             ],
    'installable': True,
    'auto_install': True
}
