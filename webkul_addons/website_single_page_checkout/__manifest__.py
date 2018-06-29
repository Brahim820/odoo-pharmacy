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
  "name"                 :  "Website Single Page Checkout",
  "summary"              :  "Singlepage Checkout for Website",
  "category"             :  "Website",
  "version"              :  "1.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Onepage-Checkout.html",
  "description"          :  """  """,
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_single_page_checkout&version=10.0&custom_url=/shop/checkout",
  "depends"              :  [
                             'website_sale_delivery',
                             'website_webkul_addons',
                            ],
  "data"                 :  [
                             'views/templetes.xml',
                            #  'views/single_page_config_view.xml',
                            #  'data/single_page_checkout_data.xml',
                             'views/webkul_addons_config_inherit_view.xml',
                             'security/ir.model.access.csv',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  99,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}