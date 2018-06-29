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
  "name"                 :  "Odoo Marketplace Seller Collection Page",
  "summary"              :  "Helps seller to create the product collections and show in collection page.",
  "category"             :  "website",
  "sequence"             :  0,
  "version"              :  "1.0.1",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Marketplace-Seller-Collection-Page.html",
  "description"          :  """Helps seller to create the product collections and show in collection page.""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_seller_collection_page&version=10.0&lifetime=120&lout=1&custom_url=/",
  "depends"              :  [
                             'odoo_marketplace',
                             'website_collectional_page',
                            ],
  "data"                 :  [
                              'security/access_control_security.xml',
                              'security/ir.model.access.csv',
                              'views/mp_config_view.xml',
                              'views/mp_seller_view.xml',
                              'views/mp_collection_view.xml',
                              'views/mp_seller_profile_template.xml',
                              'data/mp_seller_collec_data.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
