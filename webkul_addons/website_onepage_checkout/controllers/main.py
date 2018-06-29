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

    def _get_mandatory_billing_fields(self):
        return request.website.show_required_address_fields('billing')

    def _get_mandatory_shipping_fields(self):
        return request.website.show_required_address_fields('shipping')


    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        if not request.env['onepage.checkout.config'].search([('is_active', '=', True)]):
            return super(WebsiteSale, self).checkout(**post)

        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            return request.redirect('/shop/address')

        for f in self._get_mandatory_billing_fields():
            if not order.partner_id[f]:
                return request.redirect('/shop/address?partner_id=%d' % order.partner_id.id)

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

        onepage_config_values = request.env['onepage.checkout.config'].get_config_settings_values()
        values.update(onepage_config_values)
        values.update(request.website.get_install_modules())
        return request.render("website_onepage_checkout.onepage_checkout", values)

    def onepage_checkout_redirection(self, order):
        if not order or order.state != 'draft':
            request.session['sale_order_id'] = None
            request.session['sale_transaction_id'] = None
            values = {'url':'/shop', 'success': False}
            return values

        tx = request.env.context.get('website_sale_transaction')
        if tx and tx.state != 'draft':
            values = {'url':'/shop/payment/confirmation/%s' % order.id, 'success': False}

            return values


    @http.route(['/shop/onepage/confirm_order'], type='json', auth="public", website=True)
    def onepage_confirm_address(self, **post):
        SaleOrder = request.env['sale.order']
        order = request.website.sale_get_order()
        if not order:
            return [False, '/shop']

        redirection = self.onepage_checkout_redirection(order)
        if redirection:
            return [False, redirection]
        # update delivery methods
        order.onchange_partner_shipping_id()
        order.order_line._compute_tax_id()
        request.session['sale_last_order_id'] = order.id
        request.website.sale_get_order(update_pricelist=True)

        render_values = {'website_sale_order': order}
        render_values['errors'] = SaleOrder._get_errors(order)
        render_values.update(SaleOrder._get_website_data(order))
        render_result = request.env['ir.ui.view'].render_template("website_onepage_checkout.onepage_deliver_method", render_values)
        # update order amounts
        rml_obj = report_sxw.rml_parse(request.cr, SUPERUSER_ID, request.env['product.product']._name, context=request.context)
        price_digits = rml_obj.get_digits(dp='Product Price')
        price_values = {
            'success': True,
            'order_total': rml_obj.formatLang(order.amount_total, digits=price_digits),
            'order_subtotal': rml_obj.formatLang(order.amount_subtotal, digits=price_digits),
            'order_total_taxes': rml_obj.formatLang(order.amount_tax, digits=price_digits),
            'order_total_delivery': rml_obj.formatLang(order.amount_delivery, digits=price_digits)
        }
        return [True, price_values, render_result]

    def change_delivery_option(self, order, carrier_id):
        if not order or not carrier_id:
            return {'success': False}
        if not request.context.get('order_id'):
            request.context = dict(request.context, order_id=order.id)
        order._check_carrier_quotation(force_carrier_id=carrier_id)
        updated_order = request.website.sale_get_order()
        rml_obj = report_sxw.rml_parse(request.cr, SUPERUSER_ID, request.env['product.product']._name, context=request.context)
        price_digits = rml_obj.get_digits(dp='Product Price')
        values = {
            'success': True,
            'order_total': rml_obj.formatLang(order.amount_total, digits=price_digits),
            'order_subtotal': rml_obj.formatLang(order.amount_subtotal, digits=price_digits),
            'order_total_taxes': rml_obj.formatLang(order.amount_tax, digits=price_digits),
            'order_total_delivery': rml_obj.formatLang(order.amount_delivery, digits=price_digits)
        }
        return values

    @http.route(['/shop/checkout/delivery_option'], type='json', auth="public", website=True )
    def change_delivery(self , carrier_id=None, **post):
        order = request.website.sale_get_order()
        return self.change_delivery_option(order, int(carrier_id))


# Responsible Developer:- Sunny Kumar Yadav #