# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#	See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models
class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	def get_subtotal_cart(self, line):
		if line:
			self_obj = self.browse(line)
			price = self_obj.price_unit
			quantity = self_obj.product_uom_qty
			return price*quantity

	def get_subtotal_deleted(self, line):
		if line:
			# self_obj = self.browse(line)
			price = line.product_id.lst_price
			quantity = line.product_uom_qty
			return price*quantity


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	def get_show_subtotal(self):
		ir_values = self.env['ir.values'].sudo().get_default('advance.website.settings', 'sub_total')
		return ir_values
	def get_minimun_cart_value(self):
		ir_values = self.env['ir.values'].sudo().get_default('advance.website.settings', 'minimum_order_value')
		return ir_values

	@api.model
	def _get_errors(self, order):
		minimum_order_value = self.env['ir.values'].sudo().get_default('advance.website.settings', 'minimum_order_value')
		errors = []
		if order and order.amount_total < minimum_order_value:
			errors.append(['Invalid Cart Value',"A minimum purchase total of %s%s is required to confirm your order, current purchase total is %s%s "%(order.currency_id.symbol ,minimum_order_value, order.currency_id.symbol ,order.amount_total)])
		return errors