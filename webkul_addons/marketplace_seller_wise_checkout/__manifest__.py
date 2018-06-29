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
    'name'          :   'Odoo Marketplace Seller Wise Checkout',
    'author'        :   'Webkul Software Pvt. Ltd.',
    'sequence'      :   -1,
    'category'      :   'website',
    'summary'       :   'Creates different orders for different seller products in cart.',
    "license"       :   "Other proprietary",
    "version"       :   "1.0.0",
    'description'   :   """https://webkul.com/blog/odoo-marketplace-seller-wise-checkout/""",
    'website'       :   "https://store.webkul.com/Odoo-Marketplace-Seller-Wise-Checkout.html",
    'live_test_url' :   "http://odoodemo.webkul.com/?module=marketplace_seller_wise_checkout&version=10.0&lifetime=120&lout=1&custom_url=/",
    'depends'       :   [
        'odoo_marketplace',
    ],
    'data'          :   [
        'views/inherit_sale_views.xml',
        'views/website_cart_template.xml',
        'views/templates.xml',
        'views/mp_orders_view.xml',
        'views/inherit_mp_order_line_view.xml',
        'views/inherit_product_seller_template.xml',
        'data/mp_checkout_data.xml',
    ],
    "images"               :  ['static/description/Banner.png'],
    "application"          :  True,
    "installable"          :  True,
    "auto_install"         :  False,
    "price"                :  100.0,
    "currency"             :  "EUR",
    "pre_init_hook"        :  "pre_init_check",
    "post_init_hook"       :  "post_init_check",
}
