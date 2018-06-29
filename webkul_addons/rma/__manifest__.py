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
  "name"                 :  "Website RMA",
  "summary"              :  "Return merchandise authorization module helps you to manage with product returns.",
  "category"             :  "Website",
  "version"              :  "1.0.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Return-Merchandise-Authorization.html",
  "description"          :  """http://webkul.com/blog/return-merchandise-authorization/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=rma&version=10.0",
  "depends"              :  [
                             'stock',
                             'website_portal_sale',
                             'purchase',
                             'website_mail',
                             'document',
                             'website_sale',
                            ],
  "data"                 :  [
                             'data/rma_config_setting_data.xml',
                             'security/rma_security_view.xml',
                             'security/ir.model.access.csv',
                             'wizard/new_rma_wizard_view.xml',
                             'wizard/purchase_order_wizard_view.xml',
                             'wizard/product_return_view.xml',
                             'wizard/new_delivery_order_view.xml',
                             'wizard/new_mrp_repair_view.xml',
                             'views/res_config_view.xml',
                             'views/templates.xml',
                             'views/rma_view.xml',
                             'views/sequence.xml',
                             'views/sale_order_view.xml',
                             'report/report_rma.xml',
                             'report/rma_report.xml',
                             'data/rma_demo.xml',
                            ],
  "demo"                 :  [
                            'demo/rma_rma_demo_data.xml',
                            'demo/rma_user_demo_data.xml',
  ],
  "css"                  :  [],
  "js"                   :  ['static/src/js/rma.js'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  99,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
