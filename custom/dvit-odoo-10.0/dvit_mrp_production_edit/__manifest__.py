# -*- coding: utf-8 -*-

{
    "name": "MRP Production edit",
    "version": "10.0.1.0.0",
    "category": "Manufacturing",
    "license": "AGPL-3",
    'summary': 'Allow editing of generated Manufacturing Orders.',
    'description': """
    Allow editing of MRP Orders created from empty BoM,

    To use this module you must define empty BoM for products that

    you want to edit its generated MO.
    """,
    "author": "DVIT.ME",
    "website": "http://dvit.me",
    "depends": ['mrp','dvit_product_cost_bom_auto'],
    "data": ["views/mrp_production_view.xml"],
    "images": [
        'static/description/banner.png'
    ],
    "installable": True,
}
