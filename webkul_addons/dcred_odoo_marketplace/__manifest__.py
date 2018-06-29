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
  "name"                 :  "Odoo Marketplace Demo Data",
  "summary"              :  "Odoo Marketplace Demo Data for Testing Purpose.",
  "category"             :  "hidden",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "license"              :  "Other proprietary",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "website"              :  "https://store.webkul.com/Odoo-Multi-Vendor-Marketplace.html",
  "description"          :  "Odoo Marketplace demo data for testing purpose.",
  "depends"              :  [
                             'odoo_marketplace'
                            ],
  "data"                 :  [
                            ],
  "demo"                 :  [
                             'demo/mp_seller_demo_data.xml',
                             'demo/mp_product_demo_data.xml',
                             'demo/mp_product_inventory_demo_data.xml',
                             'demo/seller_shop_demo_data.xml',
                             'demo/mp_order_demo_data.xml',
                             'demo/seller_review_demo_data.xml',
                             'demo/mp_t_and_c.xml',
                            ],
  "installable"          :  True,
  "auto_install"         :  True,
  "pre_init_hook"        :  "pre_init_check",
}
