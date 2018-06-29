# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#	See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import fields, models
from odoo import models
from odoo.tools.translate import _

class website(models.Model):
	_inherit = 'website'

	def check_redirect_to(self, cr, uid, ids, context=None):
		redirect_to_cart = self.env['ir.values'].sudo().get_default('advance.website.settings', 'redirect_to_cart')
		if redirect_to_cart == 'same':
			return 1
		else:
			return 0