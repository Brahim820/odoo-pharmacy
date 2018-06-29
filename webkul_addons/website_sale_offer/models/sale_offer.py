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

from odoo import api, fields, models, _ # alphabetically ordered

from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class SaleOffer(models.Model):
    # Private attributes
    _name = 'sale.offer'
    _description = 'Model for sale offers'
    _rec_name = "promo_code"

    # Default methods
    @api.model
    def _set_seller_id(self):
        # if self._context.get('mp_seller_sale_offer'):
        user_obj = self.env['res.users'].sudo().browse(self._uid)
        if user_obj.partner_id and user_obj.partner_id.seller:
            return user_obj.partner_id.id
        return self.env['res.partner']

    # Fields declaration
    name = fields.Char(string='Name')
    promo_code = fields.Char("Voucher Code")
    description = fields.Text("Description")
    order_discount = fields.Float("Discount (%)")
    min_order_amt_so_discount = fields.Float(
        "Order Amount (>)", help="Discount will apply when order amount is greter than this amount. If it is 0.0 then discount will apply on all orders.")
    max_discount_for_so = fields.Float("Max Discount Amount", help="Discount on order will we less than or equal to this amount. If it is 0.0 there will be no limit on discount.")
    payment_acquirer_id = fields.Many2one("payment.acquirer", "Payment Method")
    payment_acquirer_discount = fields.Float("Discount (%)")
    min_order_amt_payment_acq_discount = fields.Float(
        "Order Amount (>)", help="Discount will apply when order amount is greter than given amount. If it is 0.0 then discount will apply on all orders.")
    max_discount_for_payment_acq = fields.Float(
        "Max Discount Amount", help="Discount on order will we less than or equal to this amount. If it is 0.0 there will be no limit on discount.")

    marketplace_seller_id = fields.Many2one(
        "res.partner", string="Seller", default=_set_seller_id, copy=False)


    @api.constrains('promo_code')
    def _check_promo_code_for_offers(self):
        for record in self:
            promo_code_exist_for_pl = self.env['product.pricelist'].search([('code', '=ilike', record.promo_code)])
            code_already_exist = self.search([('promo_code', '=ilike', record.promo_code)])
            if promo_code_exist_for_pl:
                raise ValidationError(
                    _("Promo Code %s is not valid. It has been already used in other pricelist. Please use diffrent Promo Code.") % record.promo_code)
            if len(code_already_exist) > 1:
                raise ValidationError(
                    _("Promo Code %s is not valid. It has been already used in other offer. Please use diffrent Promo Code.") % record.promo_code)

    @api.multi
    def apply_offer_on_order(self, sale_order, payment_acquirer_id=None):
        _logger.info(
            "----------apply_offer_on_order----%r------------------%r-----------------", self, sale_order)
        self.ensure_one()
        # discount_on_order = 0.0  # discount in %
        so_discount_amt = 0.0
        payment_acq_discount_amt = 0.0
        order_level_discount = payment_method_discount = 0.0
        #Check for sale order discount
        if (self.order_discount > 0.0) and (sale_order.amount_total > self.min_order_amt_so_discount):
            _logger.info("---------%r----------%r---------%r-----",
                         self.order_discount, sale_order.amount_total, self.min_order_amt_so_discount)
            discount_amt = sale_order.amount_total * self.order_discount / 100
            _logger.info("---discount_amt----%r---------", discount_amt)
            order_level_discount = self.order_discount
            if self.max_discount_for_so and (discount_amt > self.max_discount_for_so):
                so_discount_amt = self.max_discount_for_so
                _logger.info("------------if--so_discount_amt----%r---------", so_discount_amt)
            else:
                so_discount_amt = discount_amt
                _logger.info(
                    "-----------Else--so_discount_amt----%r---------", so_discount_amt)
        if payment_acquirer_id == self.payment_acquirer_id.id:
            if (self.payment_acquirer_discount > 0.0) and (sale_order.amount_total > self.min_order_amt_payment_acq_discount):
                payment_method_discount = self.payment_acquirer_discount
                pa_discount_amt = sale_order.amount_total * self.payment_acquirer_discount / 100
                if self.max_discount_for_payment_acq and (pa_discount_amt > self.max_discount_for_payment_acq):
                    payment_acq_discount_amt = self.max_discount_for_payment_acq
                else:
                    payment_acq_discount_amt = pa_discount_amt
        _logger.info("----------after----%r--------%r------", so_discount_amt, payment_acq_discount_amt)
        sale_order.with_context(add_sale_offer=True).write(
            {
                "global_discount": so_discount_amt + payment_acq_discount_amt, 
                "applied_sale_offer_id": self.id,
                "order_level_discount": order_level_discount,
                "payment_method_discount": payment_method_discount,
                "order_level_discount_amt": so_discount_amt,
                "payment_method_discount_amt": payment_acq_discount_amt,
            }
        )