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
  "name"                 :  "Theme Pharmacistplace",
  "summary"              :  "Enable Online Multi Vendor Odoo Marketplace For Sellers To Sale Their Product.",
  "category"             :  "Theme/Ecommerce",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Multi-Vendor-Marketplace.html",
  "description"          :  """http://webkul.com/blog/odoo-multi-vendor-marketplace/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=odoo_marketplace&version=10.0&lifetime=120&lout=1&custom_url=/",
  "depends"              :  [
                             'website_sale',
                             'website_wishlist',
                             'website_single_page_checkout',
                            ],
  "data"                 :  [
                             'views/e_commerce_templates.xml',
                             'views/theme_pharmacistplace_templates.xml',
                             'views/website_portal_template.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  299,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
