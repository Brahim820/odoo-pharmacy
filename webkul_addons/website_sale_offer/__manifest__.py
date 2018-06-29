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
  "name"                 :  "Website Sale Offers",
  "summary"              :  "Odoo Module Template",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "Webkul store product page url",
  "description"          :  """ """,
  "live_test_url"        :  " ",
  "depends"              :  [
                             'marketplace_advance_commission',
                             'marketplace_seller_wise_checkout',
                            ],
  "data"                 :  [
                            'data/uom_data.xml',
                            'security/sale_offer_security.xml',
                            'security/ir.model.access.csv',
                            'views/sale_offer_views.xml',
                            'views/inherit_sale_view.xml',
                            'views/inherit_product_view.xml',
                            'views/template.xml',
                            'views/inherit_account_invoice_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  100,
  "currency"             :  "EUR",
  # "pre_init_hook"        :  "pre_init_check",
}
