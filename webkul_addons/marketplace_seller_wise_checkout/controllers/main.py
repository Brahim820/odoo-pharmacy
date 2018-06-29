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

from odoo import http, tools, _
from odoo.http import request
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo.addons.website.models.website import slug
from odoo.addons.website_sale.controllers.main import TableCompute, QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging
_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):

    @http.route(['/shop/change_pricelist/<model("product.pricelist"):pl_id>'], type='http', auth="public", website=True)
    def pricelist_change(self, pl_id, **post):
        if (pl_id.selectable or pl_id == request.env.user.partner_id.property_product_pricelist) \
                and request.website.is_pricelist_available(pl_id.id):
            request.session['website_sale_current_pl'] = pl_id.id
            request.website.sale_get_order(force_pricelist=pl_id.id)
            seller_so_ids = request.session.get("seller_so_ids")
            seller_so_ids = request.website._get_seller_sale_order_ids(seller_so_ids) or False
            seller_so_ids = request.env['sale.order'].sudo().browse(seller_so_ids)
            if seller_so_ids:
                for o in seller_so_ids:
                    seller_id = o.marketplace_seller_id.id or False
                    request.website.sale_get_order(force_pricelist=pl_id.id, seller_id= seller_id)
        return request.redirect(request.httprequest.referrer or '/shop')

    @http.route(['/shop/pricelist'], type='http', auth="public", website=True)
    def pricelist(self, promo, **post):
        redirect = post.get('r', '/shop/payment')
        pricelist = request.env['product.pricelist'].sudo().search([('code', '=', promo)], limit=1)
        if not pricelist:
            return request.redirect("%s?code_not_available=1" % redirect)
        if pricelist and not request.website.is_pricelist_available(pricelist.id):
            return request.redirect("%s?code_not_available=1" % redirect)

        request.website.sale_get_order(code=promo)
        return request.redirect(redirect)

    @http.route(['/shop/cart'], type='http', auth="public", website=True)
    def cart(self, access_token=None, revive='', **post):
        """
        Main cart management + abandoned cart revival
        access_token: Abandoned cart SO access token
        revive: Revival method when abandoned cart. Can be 'merge' or 'squash'
        """
        request.session['sale_order_id'] = request.session['admin_so'] if request.session.get('admin_so') else None

        order = request.website.sale_get_order()
        values = {}
        if access_token:
            abandoned_order = request.env['sale.order'].sudo().search([('access_token', '=', access_token)], limit=1)
            if not abandoned_order:  # wrong token (or SO has been deleted)
                return request.render('website.404')
            if abandoned_order.state != 'draft':  # abandoned cart already finished
                values.update({'abandoned_proceed': True})
            elif revive == 'squash' or (revive == 'merge' and not request.session['sale_order_id']):  # restore old cart or merge with unexistant
                request.session['sale_order_id'] = abandoned_order.id
                return request.redirect('/shop/cart')
            elif revive == 'merge':
                abandoned_order.order_line.write({'order_id': request.session['sale_order_id']})
                abandoned_order.action_cancel()
            elif abandoned_order.id != request.session['sale_order_id']:  # abandoned cart found, user have to choose what to do
                values.update({'access_token': abandoned_order.access_token})

        if order:
            from_currency = order.company_id.currency_id
            to_currency = order.pricelist_id.currency_id
            compute_currency = lambda price: from_currency.compute(price, to_currency)
        else:
            compute_currency = lambda price: price

        seller_so_ids = request.session.get("seller_so_ids")
        if seller_so_ids:
            seller_so_ids = request.website._get_seller_sale_order_ids(seller_so_ids) or False
            seller_so_ids = request.env['sale.order'].sudo().browse(seller_so_ids)

            # do same for all seller orders
            for o in seller_so_ids:
                from_currency = o.company_id.currency_id
                to_currency = o.pricelist_id.currency_id
                compute_currency = lambda price: from_currency.compute(price, to_currency)

        values.update({
            'website_sale_order': order,
            'compute_currency': compute_currency,
            'suggested_products': [],
            'seller_so_ids':seller_so_ids if seller_so_ids else False,
        })
        if order:
            _order = order
            if not request.env.context.get('pricelist'):
                _order = order.with_context(pricelist=order.pricelist_id.id)
            values['suggested_products'] = _order._cart_accessories()

        if seller_so_ids:
            for o in seller_so_ids:
                _order = o
                if not request.env.context.get('pricelist'):
                    _order = o.with_context(pricelist=o.pricelist_id.id)

        if post.get('type') == 'popover':
            # force no-cache so IE11 doesn't cache this XHR
            return request.render("website_sale.cart_popover", values, headers={'Cache-Control': 'no-cache'})

        return request.render("website_sale.cart", values)

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        prod_obj = request.env['product.product'].sudo().browse(int(product_id))
        seller_id = prod_obj.sudo().marketplace_seller_id.id if prod_obj.sudo().marketplace_seller_id else False
        request.website.sale_get_order(force_create=1, seller_id= seller_id)._cart_update(
            product_id=int(product_id),
            add_qty=float(add_qty),
            set_qty=float(set_qty),
            attributes=self._filter_attributes(**kw),
        )
        return request.redirect("/shop/cart")

    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True):
        prod_obj = request.env['product.product'].browse(int(product_id))
        seller_id = prod_obj.sudo().marketplace_seller_id.id if prod_obj.sudo().marketplace_seller_id else False

        order = request.website.sale_get_order(force_create=1, seller_id= seller_id)
        if order.state != 'draft':
            request.website.sale_reset(order_id= order.id if order.marketplace_seller_id else None)
            admin_qty = request.website.sale_get_order() and request.website.sale_get_order().cart_quantity or 0
            sellers_qty = 0
            seller_so_ids = request.session.get("seller_so_ids")
            if seller_so_ids:
                request.website._get_seller_sale_order_ids(seller_so_ids)
                seller_so_ids = request.env['sale.order'].sudo().browse(seller_so_ids)
                sellers_qty = sum(seller_so_ids.mapped('cart_quantity'))
            total_cart_qty = admin_qty + sellers_qty
            return {'total_cart_qty': total_cart_qty,'no_line':True,}

        value = order._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty)
        if not order.cart_quantity:
            request.website.sale_reset(order_id= order.id if order.marketplace_seller_id else None)
            admin_qty = request.website.sale_get_order() and request.website.sale_get_order().cart_quantity or 0
            sellers_qty = 0
            seller_so_ids = request.session.get("seller_so_ids")
            if seller_so_ids:
                request.website._get_seller_sale_order_ids(seller_so_ids)
                seller_so_ids = request.env['sale.order'].sudo().browse(seller_so_ids)
                sellers_qty = sum(seller_so_ids.mapped('cart_quantity'))
            total_cart_qty = admin_qty + sellers_qty
            return {'total_cart_qty': total_cart_qty, 'no_line':True,}

        order = request.website.sale_get_order(seller_id= seller_id)
        value['cart_quantity'] = order.cart_quantity
        from_currency = order.company_id.currency_id
        to_currency = order.pricelist_id.currency_id

        if not display:
            return value

        # count total cart quantity
        admin_qty = request.website.sale_get_order() and request.website.sale_get_order().cart_quantity or 0
        sellers_qty = 0
        seller_so_ids = request.session.get("seller_so_ids")
        if seller_so_ids:
            request.website._get_seller_sale_order_ids(seller_so_ids)
            seller_so_ids = request.env['sale.order'].sudo().browse(seller_so_ids)
            sellers_qty = sum(seller_so_ids.mapped('cart_quantity'))
        total_cart_qty = admin_qty + sellers_qty
        value['total_cart_qty'] = total_cart_qty
        value['website_sale.cart_lines'] = request.env['ir.ui.view'].render_template("website_sale.cart_lines", {
            'website_sale_order': order,
            'compute_currency': lambda price: from_currency.compute(price, to_currency),
            'suggested_products': order._cart_accessories()
            })
        return value

    @http.route(['/seller/wise/checkout'], type="json", auth="public", website=True)
    def _seller_wise_checkout(self, seller_id):
        seller_id = int(seller_id) if type(seller_id)==int else False
        order = request.website.sale_get_order(seller_id=seller_id)
        if seller_id:
            request.session['sale_order_id'] = order.id
            return None

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        res = super(WebsiteSale, self).payment(**post)
        if post.get('code_not_available'):
            res.qcontext.update({'code_not_available': True,})
        return res
