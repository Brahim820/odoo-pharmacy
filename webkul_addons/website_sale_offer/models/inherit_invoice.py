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

from odoo import api, fields, models, _  # alphabetically ordered

from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    global_discount = fields.Float(
        "Discount Amount", digits=dp.get_precision('Product Price'))
    applied_sale_offer_id = fields.Many2one("sale.offer", "Applied Offer: ")
    order_level_discount = fields.Float("Order Discount(%)")
    order_level_discount_amt = fields.Float("Order Discount Amount")
    payment_method_discount = fields.Float("Payment Method Discount(%)")
    payment_method_discount_amt = fields.Float("Payment Method Discount Amount")
    total_seller_commission = fields.Float(
        "Total Seller Commission", compute='_compute_seller_commission', store=True)

    @api.one
    @api.depends("invoice_line_ids.seller_commission")
    def _compute_seller_commission(self):
        total_seller_commission = sum(
            line.seller_commission for line in self.invoice_line_ids.filtered(lambda r: r.is_complemantory_line == False))
        if self.order_level_discount:
            total_seller_commission = total_seller_commission - \
                total_seller_commission * self.order_level_discount / 100.0

        if self.payment_method_discount:
            total_seller_commission = total_seller_commission - \
                total_seller_commission * self.payment_method_discount / 100.0

        self.update(
            {"total_seller_commission": total_seller_commission})

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice', 'type', 'global_discount')
    def _compute_amount(self):
        super(AccountInvoice, self)._compute_amount()
        self.update({"amount_total": self.amount_total - self.global_discount})

    @api.multi
    def create_seller_invoice_new(self):
        _logger.info("--------------Website Sale Offers------11111111111111111---------------")
        IrModuleSudo = self.env['ir.module.module'].sudo()
        advance_mp_comm = IrModuleSudo.search([('name', 'in', ['marketplace_advance_commission']), ('state', 'in', [
            'to install', 'installed', 'to upgrade'])])
        for invoice_obj in self:
            sellers = {"seller_ids": {}}
            if invoice_obj.type in ['out_invoice', 'out_refund']:
                for invoice_line_obj in invoice_obj.invoice_line_ids:
                    seller_id = invoice_line_obj.product_id.marketplace_seller_id.id if invoice_line_obj.product_id.marketplace_seller_id else False
                    if seller_id:
                        seller_amount = 0.0
                        if not invoice_line_obj.is_complemantory_line:
                            if advance_mp_comm:
                                seller_amount = self.calculate_commission(
                                    invoice_line_obj.price_subtotal, seller_id, invoice_line_obj if invoice_line_obj.product_id.marketplace_seller_id else False)
                                _logger.info("")
                            else:
                                seller_amount = self.calculate_commission(
                                    invoice_line_obj.price_subtotal, seller_id)
                            # if not invoice_line_obj.is_complemantory_line:
                            invoice_line_obj.seller_commission = invoice_line_obj.price_subtotal - seller_amount
                            if invoice_obj.order_level_discount:
                                seller_amount = seller_amount - seller_amount * invoice_obj.order_level_discount / 100.0
                                invoice_line_obj.seller_commission = invoice_line_obj.seller_commission - \
                                    invoice_line_obj.seller_commission * invoice_obj.order_level_discount / 100.0
                            if invoice_obj.payment_method_discount :
                                seller_amount = seller_amount - seller_amount * \
                                    invoice_obj.payment_method_discount / 100.0
                                invoice_line_obj.seller_commission = invoice_line_obj.seller_commission - \
                                    invoice_line_obj.seller_commission * invoice_obj.payment_method_discount / 100.0

                        if sellers["seller_ids"].get(seller_id, False):
                            # ADD all product
                            sellers["seller_ids"][seller_id]["invoice_line_payment"].append(seller_amount)
                            sellers["seller_ids"][seller_id]["invoice_line_ids"].append(invoice_line_obj.id)
                        else:
                            sellers["seller_ids"].update({
                                    seller_id : {
                                        "invoice_line_payment": [seller_amount],
                                        "invoice_line_ids": [invoice_line_obj.id],
                                    }
                                }
                            )
                sellers.update({
                    "invoive_type": invoice_obj.type,
                    "invoice_id": invoice_obj.id,
                    "invoice_currency": invoice_obj.currency_id,
                    "payment_mode": "order_paid" if invoice_obj.type == "out_invoice" else "order_refund",
                    "description": _("Order Invoice Payment") if invoice_obj.type == "out_invoice" else _("Order Invoice Refund"),
                    "payment_type": "cr" if invoice_obj.type == "out_invoice" else "dr",
                    "state": "draft",
                    "memo": invoice_obj.origin or invoice_obj.name,
                })
                self.create_seller_payment_new(sellers)


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    is_complemantory_line = fields.Boolean("Complemantory Order")

    @api.multi
    def button_view_comm_details(self):
        # res = super(AccountInvoiceLine, self).button_view_comm_details()
        # wizard_id = res.get("res_id")
        # wizard_obj = self.env["commtype.desc.wizard"].browse(wizard_id)
        # if wizard_obj:
        #     new_comm = float(wizard_obj.desc.split("=")[1].rsplit(" ")[0])
        #     if seller_commission != new_comm:

        order_discount = self.invoice_id.order_level_discount
        payment_discount = self.invoice_id.payment_method_discount
        discount = ""
        if order_discount>0.0:
            discount = discount + "Order Level Discount" + " : " + str(order_discount) + "% \n"
        if payment_discount>0.0:
            discount = discount + "Payment Method Discount" + " : " + str(payment_discount) + "% \n"

        if self.comm_method and self.commission_type:
            if self.comm_method == 'percent':
                desc = "Percent Commission" + " : " + \
                    str(self.perc_comm) + " %"
            if self.comm_method == 'fix':
                desc = "Fixed Commission" + " : " + \
                    (self.currency_id.symbol if self.currency_id.position == 'before' else '') + str(self.fix_comm) + (self.currency_id.symbol if self.currency_id.position == 'after' else '')
            if self.comm_method == 'percent_and_fix':
                desc = "Percent + Fixed Commission" + " : " + str(self.perc_comm) + " % + " + (self.currency_id.symbol if self.currency_id.position == 'before' else '') + str(
                    self.fix_comm) + (self.currency_id.symbol if self.currency_id.position == 'after' else '')
            if self.comm_method == 'fix_and_percent':
                desc = "Fix + Percent Commission" + " : " + \
                    (self.currency_id.symbol if self.currency_id.position == 'before' else '') + str(self.fix_comm) + (self.currency_id.symbol if self.currency_id.position == 'after' else '') + " + " + \
                    str(self.perc_comm) + "%"
            desc = desc + " (" + str(self.commission_type) + " Commission) \n"
            desc = desc + discount
            desc = desc + "Final : " + (self.currency_id.symbol if self.currency_id.position == 'before' else '') + str(self.seller_commission) + (self.currency_id.symbol if self.currency_id.position == 'after' else '')
        else:
            desc = ''
        wizard_obj = self.env["commtype.desc.wizard"].create({'desc': desc, })
        vals = {
            'name':  _("Description of Commission"),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'commtype.desc.wizard',
            'res_id': wizard_obj.id,
            'type': "ir.actions.act_window",
            'target': 'new',
        }
        return vals
