# -*- coding: utf-8 -*-
##########################################################################
#
#	Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################

from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):


	@http.route('/my/orders/reorder/<int:order_id>', type='http', auth="public", website=True,)
	def orders_reorder(self, order_id=0):
		orderId = int(order_id)
		orderModel = http.request.env['sale.order']
		orderObj = orderModel.browse(orderId)
		reorderObj = request.website.sale_get_order(force_create=1)
		if http.request.env['ir.module.module'].search(
			[('name', '=', 'delivery')], limit=1).state == 'installed':
			filterFn = lambda l : l.is_delivery == False and l.product_id.active == True and l.product_id.website_published == True
		else:
			filterFn = lambda l : l.product_id.active == True and l.product_id.website_published == True
		for orderLine in orderObj.order_line.sudo().filtered(filterFn):
			reorderObj._cart_update(
				product_id=orderLine.product_id.id,
				add_qty=orderLine.product_uom_qty,
				)
		return request.redirect("/shop/cart")
