# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
##########################################################################
{
    "name":  "Website Abandoned Cart Recovery",
    "summary":  "Recover your Abandoned Cart by sending Email Notifications to your valuable customers.",
    "category":  "Website",
    "version":  "1.0",
    "sequence":  1,
    "author":  "Webkul Software Pvt. Ltd.",
    "license":  "Other proprietary",
    "website":  "https://store.webkul.com/Odoo-Website-Abandoned-Cart-Recovery.html",
    "description":  """https://webkul.com/blog/tag/odoo-website-abandoned-cart-recovery/""",
    "live_test_url":  "http://odoodemo.webkul.com/?module=website_cart_recovery&version=10.0",
    "depends":  [
        'website_sale',
        'mail',
        'website_webkul_addons',
    ],
    "data":  [
        'edi/website_cart_recovery_edi.xml',
        'data/cart_recovery_settings_cron.xml',
        'views/cart_recovery_inherited_res_config.xml',
        'views/webkul_addons_config_inherit_view.xml',
        'views/inherited_sale_order_view.xml',
        'views/inherited_website_view.xml',
        'views/cart_recovery_server_action_view.xml',
    ],
    "images":  ['static/description/Banner.png'],
    "application":  True,
    "installable":  True,
    "auto_install":  False,
    "price":  59,
    "currency":  "EUR",
    "pre_init_hook":  "pre_init_check",
}
