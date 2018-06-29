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
    'name'          :       'Odoo Marketplace Advance Commission',
    'version'       :       '1.0.2',
    'sequence'      :       1,
    'summary'       :       'Allows admin to set commission for sellers of marketplace.',
    'website'       :       "https://store.webkul.com/Odoo-Marketplace-Advance-Commission.html",
    'description'   :       """https://webkul.com/blog/odoo-marketplace-advance-commission/""",
    'live_test_url' :       "http://odoodemo.webkul.com/?module=marketplace_advance_commission&version=10.0&lifetime=120&lout=1&custom_url=/",
    'author'        :       "Webkul Software Pvt. Ltd.",
    'license'       :       "Other proprietary",
    'depends'       :       [
        'odoo_marketplace',
    ],
    'data'          :       [
        'views/res_partner_views.xml',
        'views/mp_res_config_views.xml',
        'views/mp_seller_view.xml',
        'data/mp_advance_comm_data.xml',
        'views/inherit_website_categ.xml',
        'views/inherit_mp_product_views.xml',
        'views/inherit_seller_payment.xml',
        'wizard/comm_type_info_wizard.xml',
    ],
    # 'demo'          :       [
    #     'demo/mp_advance_comm_demo_data.xml',
    # ],
    'images'        :  ['static/description/Banner.png'],
    'installable'   :       True,
    'application'   :       True,
    'auto_install'  :       False,
    "price"         :       99,
    "currency"      :       "EUR",
    'pre_init_hook' :       'pre_init_check',
}
