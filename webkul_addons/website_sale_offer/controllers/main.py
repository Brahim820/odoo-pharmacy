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
from odoo.addons.website_sale.controllers.main import WebsiteSale

import logging
_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/pricelist'], type='http', auth="public", website=True)
    def pricelist(self, promo, **post):
        result = super(WebsiteSale, self).pricelist(promo, **post)
        redirect = post.get('r', '/shop/payment')
        # sale_order = request.website.sale_get_order(seller_id= self._get_active_so_seller_id())
        sale_order_id = request.session.get('sale_order_id')
        sale_order = request.env['sale.order'].sudo().browse(
            sale_order_id).exists() if sale_order_id else None
        domain = [('promo_code', '=', promo)]
        sale_offer = False
        if sale_order:
            if sale_order.marketplace_seller_id:
                domain.append(("marketplace_seller_id", "=", sale_order.marketplace_seller_id.id))
            else:
                domain.append(
                    ("marketplace_seller_id", "=", False))
            sale_offer = request.env['sale.offer'].sudo().search(domain, limit=1)
            sale_order.remove_sale_offer()

        acquirers = request.env['payment.acquirer'].search(
            [('website_published', '=', True)]
        )
        _logger.info(
            "-----pricelist------------%r----------------%r------------------%r---", sale_offer, sale_order, acquirers)
        if sale_offer and sale_order:
            sale_offer.apply_offer_on_order(
                sale_order=sale_order,
                payment_acquirer_id=post.get("payment_acquirer_id", False) or acquirers[0].id if acquirers else False,
            )
            return request.redirect("%s?code_applied=1" % redirect)
        return result

    @http.route(['/apply/sale_offer'], type='json', auth="public", website=True)
    def paymnet_sale_offer_json(self, promo_code, payment_acquirer_id, **post):
        if promo_code and payment_acquirer_id:
            post.update({"payment_acquirer_id": payment_acquirer_id})
            self.pricelist(str(promo_code), **post)
            # sale_order = request.website.sale_get_order(seller_id= self._get_active_so_seller_id())
            sale_order_id = request.session.get('sale_order_id')
            sale_order = request.env['sale.order'].sudo().browse(sale_order_id).exists() if sale_order_id else None
            return ({
                "global_discount": format(round(sale_order.global_discount, 2), '.2f'),
                "amount_total": format(round(sale_order.amount_total, 2), '.2f'),
            })

    @http.route(['/shop/cart'], type='http', auth="public", website=True)
    # def cart(self, access_token=None, revive='', **post):
    def cart(self, **post):
        self.pricelist("", **post)
        return super(WebsiteSale, self).cart(**post)

    # @http.route(['/shop/payment'], type='http', auth="public", website=True)
    # def payment(self, **post):
    #     self.pricelist("", **post)
    #     return super(WebsiteSale, self).payment(**post)
