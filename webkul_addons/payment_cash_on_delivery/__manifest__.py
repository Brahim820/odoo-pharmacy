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
  "name"                 :  "Website Cash On Delivery",
  "summary"              :  "Provide Cash On Delivery Payment Option for accepting payments to your valuable customers.",
  "category"             :  "Website/Payment Acquirer",
  "version"              :  "0.3",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "maintainer"           :  "Prakash Kumar",
  "website"              :  "https://store.webkul.com/Odoo-Website-COD-Payment-Acquirer.html",
  "license"              :  "Other proprietary",
  "description"          :  """https://webkul.com/blog/tag/odoo-website-cash-on-delivery/
  Provide Cash On Delivery Payment Option for accepting payments to your valuable customers.""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=payment_cash_on_delivery&version=10.0&custom_url=/shop/payment",
  "depends"              :  [
                             'payment',
                             'website_sale',
                             'stock',
                            ],
  "data"                 :  [
                             'views/template.xml',
                             'views/payment_cash_on_delivery.xml',
                             'data/cash_on_delivery.xml',
                             'security/ir.model.access.csv',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  49.0,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}