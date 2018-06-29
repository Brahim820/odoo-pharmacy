# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#	See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models
from odoo import tools
import logging

class AdvancedWebsiteSettings(models.TransientModel):
	_inherit = 'res.config.settings'
	_name = 'advance.website.settings'

	
	redirect_to_cart =  fields.Selection([('same','Same Page'),('cart','Cart Summary')], string='Redirect page after adding to cart')
	# delete_option = fields.Boolean(string = 'Show Delete Button In Cart')
	sub_total = fields.Boolean(string = 'Show Subtotal of Order Lines')
	minimum_order_value = fields.Float(string = 'Minimum Cart Value To Validate Order')
	
	@api.multi
	def set_default_fields(self):
		ir_values = self.env['ir.values'].sudo()
		ir_values.set_default('advance.website.settings', 'redirect_to_cart',
			self.redirect_to_cart or 'same')
		# ir_values.set_default('advance.website.settings', 'delete_option',
		# 	self.delete_option)
		ir_values.set_default('advance.website.settings', 'sub_total',
			self.sub_total)
		ir_values.set_default('advance.website.settings', 'minimum_order_value',
			self.minimum_order_value or 1)
		return True

	@api.multi
	def get_default_fields(self , fields):
		ir_values = self.env['ir.values'].sudo()
		redirect_to_cart = ir_values.get_default('advance.website.settings', 'redirect_to_cart')
		# delete_option = ir_values.get_default('advance.website.settings', 'delete_option')
		sub_total = ir_values.get_default('advance.website.settings', 'sub_total')
		minimum_order_value = ir_values.get_default('advance.website.settings', 'minimum_order_value')
		
		return {
			'redirect_to_cart':redirect_to_cart, 
			# 'delete_option':delete_option, 
			'sub_total':sub_total,
			'minimum_order_value':minimum_order_value,
		}
