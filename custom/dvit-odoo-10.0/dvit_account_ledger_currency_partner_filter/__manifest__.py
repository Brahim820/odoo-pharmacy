# -*- coding: utf-8 -*-

{
    'name' : 'DVIT account ledger currency & partner filter',
    'version' : '10.1.0.2',
    'summary': 'DVIT account ledger currency & partner filter',
    'description': """
Merge 2 modules - Cybrosys partner_ledger_filter and BroadTech partner_ledger_currency
""",
    'category': 'Accounting',
    'license': 'AGPL-3',
    'author': 'DVIT.ME, Cybrosys Techno Solutions, BroadTech IT Solutions Pvt Ltd',
    'website': 'http://www.dvit.me/',
    'depends' : ['account'],
    'data': [
        'views/views.xml',
        ],

    'installable': True,
    'application': False,
    'auto_install': True,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
