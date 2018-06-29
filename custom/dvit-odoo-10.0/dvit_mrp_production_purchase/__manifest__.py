# -*- coding: utf-8 -*-

{
    "name": "MRP Production purchases",
    "version": "10.0.1.0.0",
    "category": "Manufacturing",
    "license": "AGPL-3",
    'summary': 'Allow creating PO with raw materials from Manufacturing Orders.',
    'description': """
    Allow creating PO with raw materials from Manufacturing Orders.
    """,
    "author": "DVIT.ME",
    "website": "http://dvit.me",
    "depends": ['purchase_requisition','sale_stock','mrp','dvit_product_cost_bom_auto'],
    "data": [
             "wizard/wizard.xml",
             "views/templates.xml",
             ],
    "images": [
        'static/description/banner.png'
    ],
    "installable": True,
}
