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
    'name'          :   'Website Sale Options Seller Wise Checkout',
    'author'        :   'Webkul Software Pvt. Ltd.',
    'sequence'      :   1,
    'category'      :   'website',
    'summary'       :   'Making the Website Sale Options module compatible to Marketplace Seller Wise Checkout to split orders.',
    "license"       :   "Other proprietary",
    'version'       :   "1.0.0",
    'description'   :   """Making the Website Sale Options module compatible to Marketplace Seller Wise Checkout to split orders.""",
    'website'       :   "www.webkul.com",
    'depends'       :   [
        'website_sale_options',
        'marketplace_seller_wise_checkout',
    ],
    'data'          :   [

    ],
    'installable'   :   True,
    'application'   :   True,
    'auto_install'  :   True,
    'pre_init_hook' :   'pre_init_check',
}
