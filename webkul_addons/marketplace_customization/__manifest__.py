# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

{
    'name':
    'Odoo Marketplace Staff Feature',
    'author':
    'Webkul Software Pvt. Ltd.',
    'sequence':
    1,
    'category':
    'website',
    'summary':
    'This module has the functionality related to second phase customization.',
    "license":
    "Other proprietary",
    'version':
    "1.0.0",
    'description':
    """  """,
    'website':
    "www.webkul.com",
    'depends': [
        'odoo_marketplace',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/seller_staff_view.xml',
        'views/seller_staff_view.xml',
        'views/product_view.xml',
        'views/mo_sol_view.xml',
        'views/template.xml',
    ],
    'installable':
    True,
    'application':
    True,
    'auto_install':
    True,
    'pre_init_hook':
    'pre_init_check',
}
