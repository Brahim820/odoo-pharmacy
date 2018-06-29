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

from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError
import logging
from odoo.http import request
_logger = logging.getLogger(__name__)

class account_invoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def calculate_commission(self, list_price, seller_id, invoice_line_obj=None):
        """ Calculates the commission as defined in the marketplace configuration with commission type.
            Param price_unit gives the price after deducting the commission and
            Param comm_factor gives the total commission deducted from list_price """

        price_unit = 0
        comm_factor = 0
        config_setting_obj = self.env[
            'marketplace.config.settings'].sudo().get_default_values()
        comm_type = config_setting_obj.get('comm_type')
        category_comm = config_setting_obj.get('category_comm')
        mp_config_currency = self.env['res.currency'].search([('id','=',config_setting_obj.get('mp_currency_id'))])
        if len(mp_config_currency) == 0 :
            mp_config_currency = self.env['res.currency'].search([('id', '=', self.company_id.currency_id.id)])
        sale_order_obj = self.env['sale.order'].search([('name','=',self.origin)])
        seller_obj = self.env["res.partner"].browse(seller_id)

        if comm_type == 'product' :
            # or comm_type == 'default'
            if invoice_line_obj:
                invoice_line_obj.commission_type = "Product"
                if invoice_line_obj.product_id.comm_method:
                    product = invoice_line_obj.product_id
                    price_unit = self.convert_currency_n_calc_comm(product.comm_method, list_price, invoice_line_obj.quantity, product.percent_commission, product.fix_commission, product.currency_id, sale_order_obj.currency_id, invoice_line_obj)
                    return price_unit

                if invoice_line_obj.product_id.public_categ_ids:
                    comm_list = []
                    for category in invoice_line_obj.product_id.public_categ_ids:
                        if category.comm_method:
                            price = self.convert_currency_n_calc_comm(category.comm_method, list_price, invoice_line_obj.quantity, category.percent_commission, category.fix_commission, mp_config_currency, sale_order_obj.currency_id, invoice_line_obj)
                            comm_list.append(price)
                    if comm_list != []:
                        if category_comm == 'minimum':
                            price_unit = max(comm_list)
                        else:
                            price_unit = min(comm_list)
                        return price_unit

                price_unit = self.convert_currency_n_calc_comm(seller_obj.comm_method, list_price, invoice_line_obj.quantity, seller_obj.commission, seller_obj.fix_commission, mp_config_currency, sale_order_obj.currency_id, invoice_line_obj)
                return price_unit

        if comm_type == 'category':
            if invoice_line_obj:
                invoice_line_obj.commission_type = "Category"
                if invoice_line_obj.product_id.public_categ_ids:
                    comm_list = []
                    for category in invoice_line_obj.product_id.public_categ_ids:
                        if category.comm_method:
                            price = self.convert_currency_n_calc_comm(category.comm_method, list_price, invoice_line_obj.quantity, category.percent_commission, category.fix_commission, mp_config_currency, sale_order_obj.currency_id, invoice_line_obj)
                            comm_list.append(price)
                    if comm_list != []:
                        if category_comm == 'minimum':
                            price_unit = max(comm_list)
                        else:
                            price_unit = min(comm_list)
                        return price_unit

                if invoice_line_obj.product_id.comm_method:
                    product = invoice_line_obj.product_id
                    price_unit = self.convert_currency_n_calc_comm(product.comm_method, list_price, invoice_line_obj.quantity, product.percent_commission, product.fix_commission, product.currency_id, sale_order_obj.currency_id, invoice_line_obj)
                    return price_unit

                price_unit = self.convert_currency_n_calc_comm(seller_obj.comm_method, list_price, invoice_line_obj.quantity, seller_obj.commission, seller_obj.fix_commission, mp_config_currency, sale_order_obj.currency_id, invoice_line_obj)
                return price_unit

        if comm_type == 'seller':
            if invoice_line_obj:
                invoice_line_obj.commission_type = "Seller"
                price_unit = self.convert_currency_n_calc_comm(seller_obj.comm_method, list_price, invoice_line_obj.quantity, seller_obj.commission, seller_obj.fix_commission, mp_config_currency, sale_order_obj.currency_id, invoice_line_obj)
                return price_unit

        if config_setting_obj['invoicing_type'] == "by_customer_and_seller":
            return price_unit
        else:
            return comm_factor

    @api.model
    def convert_currency_n_calc_comm(self, comm_method, list_price, qty, percent_comm, fix_comm, from_currency, to_currency, invoice_line_obj=None):
        fix_comm = from_currency.compute(fix_comm, to_currency)
        price_unit = 0
        if comm_method:

            invoice_line_obj.comm_method = comm_method
            invoice_line_obj.fix_comm = fix_comm
            invoice_line_obj.perc_comm = percent_comm

            # Case Percent commission
            if comm_method == 'percent' :
                comm_factor = (list_price * (percent_comm / 100.0))
                price_unit = list_price - comm_factor

            # Case Fix Commission
            elif comm_method == 'fix' :
                comm_factor = fix_comm * qty
                price_unit = list_price - comm_factor

            # Case Percent+Fix Commission
            elif comm_method == 'percent_and_fix' :
                    percent_comm = (list_price * (percent_comm / 100.0))
                    comm_factor = percent_comm + (fix_comm * qty)
                    price_unit = list_price - comm_factor

            # Case Fix+Percent Commission
            elif comm_method == 'fix_and_percent' :
                    new_price = list_price - (fix_comm * qty)
                    percent_comm = (new_price * (percent_comm / 100.0))
                    comm_factor = percent_comm + fix_comm
                    price_unit = new_price - percent_comm

        return price_unit

    @api.multi
    def create_seller_invoice_new(self):
        for invoice_obj in self:
            sellers = {"seller_ids": {}}
            if invoice_obj.type in ['out_invoice', 'out_refund']:
                for invoice_line_obj in invoice_obj.invoice_line_ids:
                    seller_id = invoice_line_obj.product_id.marketplace_seller_id.id if invoice_line_obj.product_id.marketplace_seller_id else False
                    if seller_id:
                        seller_amount = self.calculate_commission(invoice_line_obj.price_subtotal, seller_id, invoice_line_obj if invoice_line_obj.product_id.marketplace_seller_id else False)
                        invoice_line_obj.seller_commission = invoice_line_obj.price_subtotal - seller_amount
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

    # @api.multi
    # def create_seller_invoice_new(self):
    #     for invoice_obj in self:
    #         sellers = {"seller_ids": {}}
    #         if invoice_obj.type in ['out_invoice', 'out_refund']:
    #             for invoice_line_obj in invoice_obj.invoice_line_ids:
    #                 seller_id = invoice_line_obj.product_id.marketplace_seller_id.id if invoice_line_obj.product_id.marketplace_seller_id else False
    #                 if seller_id:
    #                     if sellers["seller_ids"].has_key(seller_id):
    #                         # ADD all product
    #                         sellers["seller_ids"][seller_id]["invoice_line_payment"].append(
    #                             self.calculate_commission(invoice_line_obj.price_subtotal, seller_id, invoice_line_obj))
    #                     else:
    #                         sellers["seller_ids"] = dict(sellers["seller_ids"], **{seller_id:
    #                                                                                {"invoice_line_payment": [self.calculate_commission(invoice_line_obj.price_subtotal, seller_id, invoice_line_obj)]}})
    #             sellers.update({
    #                 "invoive_type": invoice_obj.type,
    #                 "invoice_id": invoice_obj.id,
    #                 "payment_mode": "order_paid" if invoice_obj.type == "out_invoice" else "order_refund",
    #                 "description": _("Order Invoice Payment") if invoice_obj.type == "out_invoice" else _("Order Invoice Refund"),
    #                 "payment_type": "cr" if invoice_obj.type == "out_invoice" else "dr",
    #                 "state": "draft",
    #                 "memo": invoice_obj.origin,
    #             })
    #             self.create_seller_payment_new(sellers)

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    commission_type = fields.Char("Commission Type", readonly=True)
    comm_method = fields.Char("Commission Method", readonly=True)
    perc_comm = fields.Integer("Percent Commission")
    fix_comm = fields.Integer("Fixed Commission")

    def button_view_comm_details(self):
        if self.comm_method and self.commission_type:
            if self.comm_method == 'percent':
                desc = "Percent Commission" + " : " + str(self.perc_comm) + " %" + " = " + str(self.seller_commission)
            if self.comm_method == 'fix':
                desc = "Fixed Commission" + " : " + str(self.fix_comm) + self.currency_id.symbol + " = " + str(self.seller_commission)
            if self.comm_method == 'percent_and_fix':
                desc = "Percent + Fixed Commission" + " : " + str(self.perc_comm) + " % + " + str(self.fix_comm) + self.currency_id.symbol + " = " + str(self.seller_commission)
            if self.comm_method == 'fix_and_percent':
                desc = "Fix + Percent Commission" + " : "  + str(self.fix_comm) + self.currency_id.symbol + " + " + str(self.perc_comm) + "%" + " = " + str(self.seller_commission)
            desc = desc + " (" + str(self.commission_type) + " Commission)"
        else:
            desc = ''
        view_id= self.env["commtype.desc.wizard"].create({'desc': desc,})
        vals= {
            'name'  :  _("Description of Commission"),
            'view_mode' : 'form',
            'view_type' : 'form',
            'res_model' : 'commtype.desc.wizard',
            'res_id'    : view_id.id,
            'type'  : "ir.actions.act_window",
            'target'    : 'new',
        }
        return vals
