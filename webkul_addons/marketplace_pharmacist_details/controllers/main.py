from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

import json
import logging

from odoo import http, tools, _
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/distributor_activate'], type='http', auth="public", website=True)
    def distributor_activate(self, **post):
        # check that cart is valid
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        # if form posted
        if 'post_values' in post:
            values = {}
            return request.redirect("/shop/checkout")

        values = {}
        return request.render("marketplace_pharmacist_details.distributor_activate",
                              values)


class CustomerForm(http.Controller):

    @http.route(["/pharmacy/account"], type='http', auth="public", website=True)
    def pharmacy_account(self, **post):
        vals = {}
        sale_order_id = request.session.get('sale_order_id') if request.session.get('sale_order_id') else False
        sale_order_id = request.env['sale.order'].sudo().browse(int(sale_order_id))
        if sale_order_id and sale_order_id.marketplace_seller_id:
            pharmacy_detail = request.env['pharmacist.details'].sudo().search([('customer_id','=', request.env.user.partner_id.id)])
            pharmacy_account_exist = False
            if pharmacy_detail:
                pharmacy_account_exist = request.env['pharmacist.id.details'].sudo().search([
                    ('pharmacist_customer_id','=', pharmacy_detail.id),
                    ('marketplace_seller_id','=', sale_order_id.marketplace_seller_id.id)]
                )
            vals.update({
                "pharmacy_account_exist": True if pharmacy_account_exist else False,
                "marketplace_seller_id":  sale_order_id.marketplace_seller_id,
            })
        return request.render("marketplace_pharmacist_details.pharmacy_account_registration_form", vals)


    @http.route(["/create/pharmacy/account"], type='http', auth="public", website=True)
    def create_pharmacy_account(self, **post):
        name = post.get("name")
        email = post.get("email")
        phone = post.get("phone")
        address = post.get("address")
        marketplace_seller_id = int(post.get("marketplace_seller_id")) if post.get("marketplace_seller_id") else False
        comm_reg = post.get("comm_reg")
        tax_card = post.get("tax_card")

        customer_id = request.env.user.partner_id.id
        pharmacist_customer_details = request.env['pharmacist.details'].sudo().search([('customer_id','=',customer_id)], limit = 1)
        if not pharmacist_customer_details:
            pharmacist_customer_details = request.env['pharmacist.details'].sudo().create({'customer_id': customer_id,})

        values = {
            'name': name,
            'marketplace_seller_id': marketplace_seller_id,
            'pharmacist_customer_id': pharmacist_customer_details.id,
            'street1': address,
            'email': email,
            'phone': phone,
            'tax_card':tax_card,
        }

        try:
            pharmacy_account_id = request.env["pharmacist.id.details"].sudo().create(values)
        except:
            _logger.info("---------------------------- Record Not Created as some mandatory fields Not Found --------------------------")

        return request.redirect("/shop/checkout")
