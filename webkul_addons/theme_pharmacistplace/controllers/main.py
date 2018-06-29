# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging

from odoo import http, tools, _
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.auth_signup.controllers.main import AuthSignupHome

_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/cart'], type='http', auth="public", website=True)
    def cart(self, **post):
        res = super(WebsiteSale, self).cart(**post)

        # Check cart related customized enabled template is activated or not
        try:
            res.qcontext.update({
                'extra_info': request.env.ref('website_sale.extra_info_option').active or False,
                'continue_shopping': request.env.ref('website_sale.continue_shopping').active or False,
                'coupon_code': request.env.ref('website_sale.reduction_code').active or False,
            })
        except Exception as e:
            _logger.info("----Exception on cart page-----%r-----", str(e))

        return res

    @http.route(['/clear/cart'], type='http', auth="public", website=True)
    def clear_cart(self, **post):
        if post.get("cart_so_id"):
            request.env["sale.order.line"].sudo().search(
                [("order_id.id", "=", int(post.get("cart_so_id")))]).unlink()
        return request.redirect("/shop/cart")


class website_account(website_account):

    @http.route(['/my/account'], type='http', auth='user', website=True)
    def details(self, redirect=None, **post):
        res = super(website_account, self).details(redirect, **post)
        res.qcontext.update({"my_profile": True})
        if not len(res.qcontext.keys()) != 1:
            # res.qcontext.update({
            #     'error': {},
            #     'error_message': []
            # })
            return request.redirect('/my/account')
        return request.render("theme_pharmacistplace.theme_pharmacistplace_portal_my_account", res.qcontext)

    # @http.route('/change_password', type='http', auth='user', website=True)
    # def change_password(self, *args, **kw):
    #     values = {
    #         "change_password" : True,
    #     }
    #     return request.render(
    #         "theme_pharmacistplace.theme_pharmacistplace_change_password",
    #         values)


class AuthSignupHome(AuthSignupHome):

    @http.route('/web/reset_password', type='http', auth='public', website=True)
    def web_auth_reset_password(self, *args, **kw):
        res = super(AuthSignupHome, self).web_auth_reset_password(*args, **kw)
        if request.env.user == request.website.user_id or not res.qcontext:
            return res
        res.qcontext.update({
            "change_password": True,
        })
        return request.render(
            "theme_pharmacistplace.theme_pharmacistplace_change_password",
            res.qcontext)
