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

        return str(order.cart_quantity)
