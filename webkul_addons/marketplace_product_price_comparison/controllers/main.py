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

import werkzeug
import odoo
from odoo import http
from odoo.http import request
import base64
from odoo.tools.translate import _
from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug import url_encode
import logging
_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values):
        res = super(WebsiteSale, self)._get_search_domain(search, category, attrib_values)
        config_setting_obj = request.env['marketplace.config.settings'].sudo().get_default_values()
        if not config_setting_obj.get("dispaly_comparison_product") or config_setting_obj.get("dispaly_comparison_product") == "one":
            if not config_setting_obj.get("criteria_to_dispaly_one_product") or config_setting_obj.get("criteria_to_dispaly_one_product") == "default":
                res.append(('global_product_tmpl_id', '=', False))
            elif config_setting_obj.get("criteria_to_dispaly_one_product") in ["low_price", "high_price", 'manual']:
                res.append(('wk_hide_on_web', '=', False))
        return res

    @http.route(["/product/sellers/<int:product_template_id>"], type="http", auth="public", website=True)
    def product_all_seller(self, product_template_id, **post):
        product_template_obj = request.env["product.template"].browse(int(product_template_id))
        if product_template_obj and product_template_obj.seller_product_ids:
            mp_other_seller_products = product_template_obj.seller_product_ids.filtered(lambda p: p.status == 'approved' and p.website_published) + product_template_obj
            mp_other_seller_products = mp_other_seller_products.sorted(key=lambda p: p.website_price)
        if product_template_obj.global_product_tmpl_id and product_template_obj.marketplace_seller_id:
            mp_other_seller_products = product_template_obj.global_product_tmpl_id.seller_product_ids.filtered(lambda p: p.status == 'approved' and p.website_published and p.id != product_template_obj.id) + product_template_obj.global_product_tmpl_id.filtered('website_published') + product_template_obj
            mp_other_seller_products = mp_other_seller_products.sorted(key=lambda p: p.website_price)
        return request.render("marketplace_product_price_comparison.wk_mp_product_other_seller_page", {'product':product_template_obj, 'mp_other_seller_products': mp_other_seller_products})
