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
  "name"                 :  "Website Recently Viewed Products",
  "summary"              :  "Display customer`s recent viewed products history.",
  "category"             :  "Website",
  "version"              :  "1.3",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Recently-Viewed-Products.html",
  "description"          :  """https://webkul.com/blog/odoo-website-recently-viewed-products/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_recently_viewed_products&version=10.0",
  "depends"              :  [
                             'website_sale',
                             'website_webkul_addons',
                            ],
  "data"                 :  [
                             'data/config_data.xml',
                             'security/ir.model.access.csv',
                             'views/templates.xml',
                             'views/recently_viewed_config_view.xml',
                             'views/res_users_inherit_view.xml',
                             'views/webkul_addons_config_inherit_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  39,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}