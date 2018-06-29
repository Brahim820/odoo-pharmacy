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
  "name"                 :  "Website Reorder",
  "summary"              :  "Website Reorder",
  "category"             :  "Website",
  "version"              :  "1.1.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com",
  "description"          :  """""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=sale_reorder&version=10.0",
  "depends"              :  ['website_sale'],
  "data"                 :  [
                             'security/reorder_security.xml',
                             'views/res_config_view.xml',
                             'views/templates.xml',
                             'views/website_portal_sale_templates.xml',
                            ],
  "demo"                 :  ['data/reorder_demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  29,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}