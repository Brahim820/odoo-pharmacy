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
  "name"                 :  "Website Collection Page",
  "summary"              :  "Manage multiple product collection pages for your e-commerce website.",
  "category"             :  "Website",
  "version"              :  "1.1.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Collection-Page.html",
  "description"          :  """https://webkul.com/blog/odoo-website-collection-page/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_collectional_page&version=10.0&lifetime=60&lout=1&custom_url=/collections",
  "depends"              :  ['website_sale','website_webkul_addons',],
  "data"                 :  [
                             'security/collectional_security_view.xml',
                             'security/ir.model.access.csv',
                             'view/website_collectional_page.xml',
                             'view/templates.xml',
                             'data/wk_operator.xml',
                             'view/website_collectional_page_config.xml',
                             'view/webkul_addons_config_views.xml',
                             'view/collections_page_n_group_template.xml',
                            ],
  "demo"                 :  [
                             'demo/wk_collection_demo_data.xml',
                            ],
  "css"                  :  ['static/src/css/collection.css'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  69,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
