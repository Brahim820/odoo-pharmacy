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
  "name"                 :  "Odoo Marketplace Seller Wise Checkout Demo Home Page",
  "summary"              :  "Odoo Marketplace Seller Wise Checkout demo home page.",
  "category"             :  "hidden",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "license"              :  "Other proprietary",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "website"              :  "https://store.webkul.com",
  "description"          :  "Odoo Marketplace Seller Wise Checkout demo data for testing purpose.",
  "depends"              :  [
                             'marketplace_seller_wise_checkout',
                             'demo_odoo_marketplace'
                            ],
  "data"                 :  [
                             'demo/inherit_demo_home_page_data.xml',
                            ],
  "demo"                 :  [

                            ],
  "installable"          :  True,
  "auto_install"         :  True,
}
