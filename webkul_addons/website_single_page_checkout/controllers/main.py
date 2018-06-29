# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
from odoo import http, tools, api, _, SUPERUSER_ID
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.report import report_sxw

import logging
_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    # def _get_mandatory_billing_fields(self):
    #     return request.website.show_required_address_fields('billing')

    # def _get_mandatory_shipping_fields(self):
    #     return request.website.show_required_address_fields('shipping')


    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            return request.redirect('/shop/address')

        values = self.checkout_values(**post)
        if post.get('xhr'):
            return 'ok'

        # Check that this option is activated
        extra_step = request.env.ref('website_sale.extra_info_option')
        if extra_step.active:
            values.update({
                'extra_step_active': True,
                'website_sale_order': order,
                'post': post,
                'escape': lambda x: x.replace("'", r"\'")
            })
            values.update(request.env['sale.order']._get_website_data(order))
        result = self.payment(**post)
        values.update(result.qcontext)

        if values['errors']:
            shipping_partner_id = False
            if order:
                if order.partner_shipping_id.id:
                    shipping_partner_id = order.partner_shipping_id.id
                else:
                    shipping_partner_id = order.partner_invoice_id.id

            acquirers = request.env['payment.acquirer'].search(
                [('website_published', '=', True), ('company_id', '=', order.company_id.id)]
            )
            values['acquirers'] = []
            for acquirer in acquirers:
                acquirer_button = acquirer.with_context(submit_class='btn btn-primary', submit_txt=_('Pay Now')).sudo().render(
                    '/',
                    order.amount_total,
                    order.pricelist_id.currency_id.id,
                    values={
                        'return_url': '/shop/payment/validate',
                        'partner_id': shipping_partner_id,
                        'billing_partner_id': order.partner_invoice_id.id,
                    }
                )
                acquirer.button = acquirer_button
                values['acquirers'].append(acquirer)

            values['tokens'] = request.env['payment.token'].search([('partner_id', '=', order.partner_id.id), ('acquirer_id', 'in', acquirers.ids)])
        request.session['sale_last_order_id'] = order.id
        values.update({
            'country': order.partner_id.country_id,
            'countries': request.env["res.country"].get_website_sale_countries(),
            "states": request.env["res.country"].get_website_sale_states(),
        })
        return request.render("website_single_page_checkout.single_page_checkout", values)

    @http.route(['/save_address'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def save_address(self, wk_name, wk_email, wk_phone, wk_street, wk_city, wk_country, wk_state=None, wk_zip=None):
        Partner = request.env['res.partner']
        order = request.website.sale_get_order()
        vals={
            "customer": True,
            "team_id": request.website.salesteam_id and request.website.salesteam_id.id,
            'lang': request.lang if request.lang in request.website.mapped('language_ids.code') else None,
            'parent_id': order.partner_id.commercial_partner_id.id,
            'type': 'delivery',
            "name": str(wk_name),
            "email": str(wk_email),
            "phone": str(wk_phone),
            "street": str(wk_street),
            "city": str(wk_city),
            "zip": str(wk_zip) if wk_zip else False,
            "country_id": int(wk_country),
            "state_id": int(wk_state) if wk_state else False,

        }
        partner_obj = Partner.sudo().create(vals)
        if partner_obj:
            order.partner_shipping_id = partner_obj.id
            return request.env.ref("website_single_page_checkout.test_address").render({'contact':partner_obj},engine='ir.qweb')
        return False
