# -*- coding: utf-8 -*-
#################################################################################
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
#################################################################################
{
  "name"                 :  "Website Product Wishlist",
  "summary"              :  "Add products to your wishlist for later purchase.",
  "category"             :  "Website",
  "version"              :  "1.2",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Product-Wishlist.html",
  "description"          :  """http://webkul.com/blog/odoo-product-wishlist/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_wishlist&version=10.0",
  "depends"              :  [
                             'base',
                             'website_sale',
                            ],
  "data"                 :  [
                             'views/templates.xml',
                             'views/wk_wishlist.xml',
                             'security/ir.model.access.csv',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  39,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}