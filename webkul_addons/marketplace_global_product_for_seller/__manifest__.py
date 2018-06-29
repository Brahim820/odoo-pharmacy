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
    'name'          :   'Odoo Marketplace Auto Assign Global Product to Seller',
    'author'        :   'Webkul Software Pvt. Ltd.',
    'sequence'      :   1,
    'summary'       :   "Module makes the global product for seller",
    "license"       :   "Other proprietary",
    'version'       :   "1.0.0",
    'description'   :   """Module makes the global product for seller""",
    'website'       :   "www.webkul.com",
    'depends'       :   [
        'marketplace_product_price_comparison',
    ],
    'data'          :   [
        'views/global_product_cron_view.xml',
    ],
    'installable'   :   True,
    'application'   :   True,
    # 'auto_install'  :   True,
    'pre_init_hook' :   'pre_init_check',
}
