# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
from odoo import http
from odoo.http import request
from odoo import SUPERUSER_ID

from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging
_logger = logging.getLogger(__name__)


class website_sale(WebsiteSale):
	
	@http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
	def cart_update(self, product_id, wk_page_url=False, add_qty=1, set_qty=0, **kw):
		url = ''
		ir_values = request.env['ir.values'].sudo().get_default('advance.website.settings', 'redirect_to_cart')
		if ir_values == 'same':
			url = wk_page_url
		else:
			url = "/shop/cart"
		request.website.sale_get_order(force_create=1)._cart_update(
		product_id=int(product_id),
		add_qty=float(add_qty),
		set_qty=float(set_qty),
		attributes=self._filter_attributes(**kw),
		)
		return request.redirect(url)
			
