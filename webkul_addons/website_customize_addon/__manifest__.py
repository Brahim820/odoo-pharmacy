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
    'name'          :   'Compatibility Module For Sale Offer,Sale Options,One Page Checkout, Comparison Products',
    'author'        :   'Webkul Software Pvt. Ltd.',
    'sequence'      :   1,
    'category'      :   'website',
    'summary'       :   'Making the Website Customize Addon module maintain compatibility of differnt addons.',
    "license"       :   "Other proprietary",
    'version'       :   "1.0.0",
    'description'   :   """Making the Website Customize Addon module maintain compatibility of differnt addons.""",
    'website'       :   "www.webkul.com",
    'depends'       :   [
        'website_sale_options',
        'marketplace_seller_wise_checkout',
        'website_onepage_checkout',
        'website_sale_offer',
        'marketplace_product_price_comparison'
    ],
    'data'          :   [
        'views/inherit_onepage_checkout.xml',
    ],
    'installable'   :   True,
    'application'   :   True,
    'auto_install'  :   True,
    'pre_init_hook' :   'pre_init_check',
}
