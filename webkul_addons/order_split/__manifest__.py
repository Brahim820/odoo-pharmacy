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
  "name"                 :  "Order Split",
  "summary"              :  "Allows Order Splitting According to Product(s) Availability.",
  "category"             :  "Sales Management",
  "version"              :  "0.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "maintainer"           :  "Prakash Kumar",
  "website"              :  "https://store.webkul.com/Odoo-Order-Split.html",
  "description"          :  """""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=order_split&version=10.0",
  "depends"              :  [
                             'stock',
                             'mail',
                            ],
  "data"                 :  [
                             'views/order_split.xml',
                             'wizard/order_split_wizard.xml',
                             'security/ir.model.access.csv',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}