# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################
from odoo import http
from odoo.tools.translate import _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale(WebsiteSale):
    _codfeedbackUrl='/payment/cash_on_delivery/feedback'
    @http.route([_codfeedbackUrl], type='http', auth='public', website=True)
    def cod_payment(self, **post):
        request.env['payment.transaction'].form_feedback(post, 'cash_on_delivery')
        return request.redirect(post.get('return_url', '/shop/payment/validate'))

    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        res = super(WebsiteSale, self).product(product, category=category, search=search, **kwargs)

        cod_payment = request.env['payment.acquirer'].sudo().search(
            [('provider','=','cash_on_delivery')],limit=1
        ).cod_rule
        is_cod = request.website.is_cod_available(product)
        if is_cod:
            res.qcontext['cod_availability']  =is_cod
            res.qcontext['cod_payment'] =cod_payment
        return res


    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        res = super(WebsiteSale, self).payment(**post)
        acquirers = res.qcontext.get('acquirers',[])
        errors =res.qcontext.get('errors',[])
        for acquirer in filter(lambda ac:ac.provider=='cash_on_delivery',acquirers):
            if not request.website.is_cod_available(payment_acquirer=acquirer):
                acquirers.remove(acquirer)
                errors.append(
                   ((_('Sorry, We are unable to provide Cash On Delivery.')),acquirer.cod_rule.cod_unavailability_payment_message))
        res.qcontext['acquirers'] =acquirers
        res.qcontext['errors'] =errors


        return res
