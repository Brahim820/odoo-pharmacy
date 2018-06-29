# -*- coding: utf-8 -*-

{
    "name": "Product Multi UoM with conversion ratio",
    "version": "10.0.1.0.0",
    "category": "Product",
    "license": "AGPL-3",
    'summary': 'product_multi_uom_ratio with product_dimensions',
    'description': """
    Glue module between product_multi_uom_ratio and product_dimensions.
    """,
    "author": "DVIT.ME",
    "website": "http://dvit.me",
    "depends": ['dvit_product_multi_uom_ratio',
                'dvit_product_dimensions'],
    "data": ["wizard/views.xml"],
	 "images": [
    ],
    "installable": True,
    'auto_install': True,
}
