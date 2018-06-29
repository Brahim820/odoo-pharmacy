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
    "name"              :  "Odoo Marketplace Seller Slider",
    "summary"           :  "This module allows Seller to add multiple banners for their profile page and shop page.",
    "category"          :  "Website",
    "version"           :  "1.0.0",
    "sequence"          :  1,
    "author"            :  "Webkul Software Pvt. Ltd.",
    "license"           :  "Other proprietary",
    "website"           :  "https://store.webkul.com/Odoo-Marketplace-Seller-Slider.html",
    "description"       :  """https://webkul.com/blog/odoo-marketplace-seller-slider/""",
    "live_test_url"     :  "http://odoodemo.webkul.com/?module=marketplace_seller_slider&version=10.0&lifetime=120&lout=1&custom_url=/",
    "depends"           :  [
                            'odoo_marketplace',
    ],
    "data"              :  [
                            'security/ir.model.access.csv',
                            'views/banner_image_view.xml',
                            'wizard/banner_images_wizard_view.xml',
                            'views/seller_or_shop_view.xml',
                            'views/seller_or_shop_template.xml',
    ],
    "demo"              :  [
    ],
    "images"            :  ['static/description/Banner.png'],
    "application"       :  True,
    "installable"       :  True,
    "auto_install"      :  False,
    "price"             :  25,
    "currency"          :  "EUR",
    "pre_init_hook"     :  "pre_init_check",
}
