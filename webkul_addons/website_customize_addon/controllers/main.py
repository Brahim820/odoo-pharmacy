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

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging
_logger = logging.getLogger(__name__)

class WebsiteSaleOptions(WebsiteSale):

    @http.route(['/shop/cart/update_option'], type='http', auth="public", methods=['POST'], website=True, multilang=False)
    def cart_options_update_json(self, product_id, add_qty=1, set_qty=0, goto_shop=None, lang=None, **kw):
        if lang:
            request.website = request.website.with_context(lang=lang)

        prod_obj = request.env['product.product'].sudo().browse(int(product_id))
        seller_id = prod_obj.sudo().marketplace_seller_id.id if prod_obj.sudo().marketplace_seller_id else False

        order = request.website.sale_get_order(force_create=1, seller_id= seller_id)
        product = request.env['product.product'].browse(int(product_id))

        option_ids = product.optional_product_ids.mapped('product_variant_ids').ids
        optional_product_ids = []
        for k, v in kw.items():
            if "optional-product-" in k and int(kw.get(k.replace("product", "add"))) and int(v) in option_ids:
                optional_product_ids.append(int(v))

        attributes = self._filter_attributes(**kw)

        value = {}
        if add_qty or set_qty:
            value = order._cart_update(
                product_id=int(product_id),
                add_qty=int(add_qty),
                set_qty=int(set_qty),
                attributes=attributes,
                optional_product_ids=optional_product_ids
            )

        # options have all time the same quantity
        for option_id in optional_product_ids:
            order._cart_update(
                product_id=option_id,
                set_qty=value.get('quantity'),
                attributes=attributes,
                linked_line_id=value.get('line_id')
            )

        #for updating the quantity..
        admin_qty = request.website.sale_get_order().cart_quantity or 0
        sellers_qty = 0
        seller_so_ids = request.session.get("seller_so_ids")
        if seller_so_ids:
            request.website._get_seller_sale_order_ids(seller_so_ids)
            seller_so_ids = request.env['sale.order'].sudo().browse(seller_so_ids)
            sellers_qty = sum(seller_so_ids.mapped('cart_quantity'))
        total_cart_qty = admin_qty + sellers_qty

        return str(total_cart_qty)

class WebsiteSale(WebsiteSale):

    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        res = super(WebsiteSale, self).checkout(**post)
        if post.get('code_applied') or post.get('code_not_available'):
            res.qcontext.update({'code_applied': True,
                'code_not_available': True if post.get('code_not_available') else False,})

        return res
