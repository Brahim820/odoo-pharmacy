# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Egypt CoA - DVIT',
    'version': '10.0.0.2',
    'author': 'DVIT.ME',
    'category': 'Localization',
    'description': """
    Arabic Chart of accounts for Egypt and other Arabic countries .
""",
    'website': 'http://www.dvit.me',
    'depends': ['account', 'l10n_multilang','account_parent'],
    'data': [
        'data/chart_template_data.xml',
        'data/account.account.template.csv',
        'data/chart_data.xml',
        'data/chart_template_data.yml',
    ],
    "images": [
        'static/description/banner.png'
    ],
    'post_init_hook': 'load_translations',
'installable': True,

}
