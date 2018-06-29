{
    'name': 'POS Fixes',
    'summary': 'Point of Sale Fixes: complete stock account moves, mark pos invoices as paid and reconcile them.',
    'description': """
    Fixes included:

    - Fix POS invoices payments by reconciling them automatically on POS session closing to get them paid.

    - Complete the Gr/Ir anglo-saxon journal entries missing in POS. -- ** Update: this fixed in odoo itself now. **

    - Now supports IngAdhoc's Product packs 1- create anglo-saxon for packs.

    ToDo:

    - Improve performance by reconciling invoices per order close not in session close .

     """,
     "license": "AGPL-3",
    'version': '10.0.2.0',
    'category': 'Point of Sale',
    'author': 'DVIT.me',
    'website': 'http://dvit.me',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_voucher',
        'point_of_sale',
        'purchase',
        ],
    'data': ['views.xml'],
    "images": [
        'static/description/banner.png'
    ],
    'installable': True,
    'auto_install': True,
    'application': False,

}
