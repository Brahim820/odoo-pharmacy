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


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    global_discount = fields.Float(
        "Discount Amount", digits=dp.get_precision('Product Price'), readonly=True)
    applied_sale_offer_id = fields.Many2one("sale.offer", "Applied Offer: ", readonly=True)
    order_level_discount = fields.Float("Order Discount(%)")
    order_level_discount_amt = fields.Float("Order Discount Amount")
    payment_method_discount = fields.Float("Payment Method(%)")
    payment_method_discount_amt = fields.Float("Payment Method Amount")


    @api.depends('order_line.price_total', 'global_discount', 'applied_sale_offer_id')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_total': (amount_untaxed + amount_tax) - order.global_discount,
            })

    @api.multi
    def remove_sale_offer(self):
        for obj in  self:
            # for sol_obj in obj.order_line.filtered("is_complemantory_line"):
            #     sol_obj.unlink()
            obj.write({
                "global_discount": False,
                "applied_sale_offer_id": False,
                "order_level_discount": False,
                "payment_method_discount": False,
                "order_level_discount_amt": False,
                "payment_method_discount_amt": False,
            })

    @api.multi
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, attributes=None, **kwargs):
        _logger.info("-------_cart_update------%r-------------", self)
        self.ensure_one()
        self.remove_sale_offer()
        res =  super(SaleOrder, self)._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, attributes=attributes, **kwargs)
        x = self.add_complemantory_sol()
        _logger.info("-------x------%r-------------", x)
        if x:
            res = super(SaleOrder, self)._cart_update(product_id=product_id, line_id=line_id,
                                                      add_qty=add_qty, set_qty=set_qty, attributes=attributes, **kwargs)
        return res

    @api.multi
    def add_complemantory_sol(self):
        _logger.info("-------add_complemantory_sol-1-----%r-------------", self)
        sol_deleted = False
        # return True
        # self.ensure_one()
        # all_sol_obj = 
        for sol_obj in self.order_line.filtered(lambda sol: sol.is_complemantory_line == False):
            _logger.info("-------add_complemantory_sol----%r------",
                         self.order_line.filtered(lambda sol: sol.com_line_for_sol_id == sol_obj))
            # if not sol_obj.is_complemantory_line:
            for rule_obj in sol_obj.product_id.bogo_offer_rule_ids:
                com_sol = self.order_line.filtered(
                    lambda sol: sol.com_line_for_sol_id == sol_obj and sol.product_id == rule_obj.product_id)
                _logger.info("____com_sol____%r-----------------", com_sol)
                if not com_sol:
                    #Code to add complemantory product
                    _logger.info(
                        "----------rule_obj.offer_type-------%r------------------", rule_obj.free_qty_type)
                    if sol_obj.product_uom_qty >= rule_obj.min_ordered_qty:
                        already_created_com_sol = self.env["sale.order.line"].sudo(
                        ).search([('is_complemantory_line', '=', True), ('com_line_for_sol_id', '=', sol_obj.id)])
                        if rule_obj.free_qty_type == "percentage":
                            qty = int(sol_obj.product_uom_qty *
                                        rule_obj.free_qty / 100)
                            vals = {
                                "product_id": rule_obj.product_id.id,
                                "price_unit": 0.0,
                                "product_uom_qty": qty,
                                "is_complemantory_line": True,
                                "order_id": sol_obj.order_id.id,
                                "com_line_for_sol_id": sol_obj.id,
                                "name": "Bonus Product.",
                            }
                            if already_created_com_sol:
                                already_created_com_sol.write(vals)
                            else:
                                self.env["sale.order.line"].sudo().create(vals)
                        elif rule_obj.free_qty_type == "fixed":
                            vals = {
                                "product_id": rule_obj.product_id.id,
                                "price_unit": 0.0,
                                "product_uom_qty": rule_obj.free_qty,
                                "is_complemantory_line": True,
                                "order_id": sol_obj.order_id.id,
                                "com_line_for_sol_id": sol_obj.id,
                                "name": "Bonus Product.",
                            }
                            if already_created_com_sol:
                                already_created_com_sol.write(vals)
                            else:
                                self.env["sale.order.line"].sudo().create(vals)
                elif com_sol:
                    #Code to update complemantory product qty
                    # for rule_obj in sol_obj.product_id.bogo_offer_rule_ids:
                    for o in com_sol:
                        _logger.info("-----%r----", o)
                        if sol_obj.product_uom_qty >= rule_obj.min_ordered_qty:
                            if rule_obj.free_qty_type == "percentage":
                                qty = int(sol_obj.product_uom_qty *
                                            rule_obj.free_qty / 100)
                                o.product_uom_qty = qty
                            elif rule_obj.free_qty_type == "fixed":
                                o.product_uom_qty = rule_obj.free_qty
                        else:
                            _logger.info("--O Unlink---%r----", o)
                            o.sudo().unlink()
                            sol_deleted = True
                            _logger.info(
                                "--O sol_deleted---%r----", sol_deleted)
                            # self._cr.commit()
        _logger.info("--1 sol_deleted---%r----", sol_deleted)
        return sol_deleted

    @api.multi
    def _prepare_invoice(self):
        invoiceVals = super(SaleOrder, self)._prepare_invoice()
        self.ensure_one()
        if self.global_discount:
            invoiceVals.update({
                'global_discount': self.global_discount,
                'applied_sale_offer_id': self.applied_sale_offer_id.id,
                'order_level_discount': self.order_level_discount,
                'payment_method_discount': self.payment_method_discount,
                "order_level_discount_amt": self.order_level_discount_amt,
                "payment_method_discount_amt": self.payment_method_discount_amt,
            })
        return invoiceVals

    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_complemantory_line = fields.Boolean("Complemantory Order", readonly=True)
    com_line_for_sol_id = fields.Many2one("sale.order.line", "Complemantoery Order For SOL", readonly=True)

    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        if res:
            if not res.is_complemantory_line and res.product_id.pharmacy_discount:
                res.discount = res.product_id.pharmacy_discount
            if res.is_complemantory_line:
                res.price_unit = 0.0
        return res

    @api.multi
    def write(self, vals):
        if len(self) ==1 :
            if not self.is_complemantory_line and self.product_id.pharmacy_discount:
                vals.update({"discount" : self.product_id.pharmacy_discount})
            if self.is_complemantory_line:
                vals.update({"price_unit": 0.0})
        res = super(SaleOrderLine, self).write(vals)
        return res

    @api.multi
    def unlink(self):
        for sol_obj in self:
            if not sol_obj.is_complemantory_line:
                complemantory_sol = self.search([("com_line_for_sol_id", "=", sol_obj.id)])
                if complemantory_sol:
                    self = self + complemantory_sol
        return super(SaleOrderLine, self).unlink()

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        res.update(
            is_complemantory_line=self.is_complemantory_line,
            seller_commission=0.0, #If seller product is in coplemantory sol then no commission
        )
        return res
    
    @api.multi
    def add_complemantory_sol(self):
        self.ensure_one()
        for sol_obj in self:
            if not sol_obj.is_complemantory_line:
                for rule_obj in sol_obj.product_id.bogo_offer_rule_ids:
                    _logger.info(
                        "----------rule_obj.offer_type-------%r------------------", rule_obj.offer_type)
                    if rule_obj.offer_type == "same_product":
                        qty = 0.0
                        if rule_obj.free_qty_type == "percentage":
                            qty = int(sol_obj.product_uom_qty *
                                        rule_obj.free_qty / 100)
                        elif rule_obj.free_qty_type == "fixed":
                            qty = rule_obj.free_qty
                        vals = {
                            "product_id": rule_obj.product_id.id,
                            "price_unit": 0.0,
                            "product_uom_qty": qty,
                            "is_complemantory_line": True,
                            "order_id": sol_obj.order_id.id,
                            "com_line_for_sol_id": sol_obj.id,
                            "name": "Bonus Product.",
                        }
                        self.sudo().create(vals)
                    elif rule_obj.offer_type == "many_product":
                        for obj in rule_obj.free_product_ids:
                            vals = {
                                "product_id": obj.product_id.id,
                                "price_unit": 0.0,
                                "product_uom_qty": obj.free_qty,
                                "is_complemantory_line": True,
                                "order_id": sol_obj.order_id.id,
                                "com_line_for_sol_id": sol_obj.id,
                                "name": "Bonus Product.",
                            }
                            self.sudo().create(vals)
