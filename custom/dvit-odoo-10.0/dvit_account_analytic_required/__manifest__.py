# -*- coding: utf-8 -*-
# © 2011-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Account Analytic Required',
    'summary': 'Allow setting analytic policy on account instead of account type.',
    'version': '10.0.1.0',
    'category': 'Analytic Accounting',
    'license': 'AGPL-3',
    'author': "DVIT.ME, Akretion,Odoo Community Association (OCA)",
    'website': 'http://dvit.me/',
    'depends': ['account'],
    "images": [
        'static/description/banner.png'
    ],
    'data': ['views/account.xml'],
    'installable': True,
}
