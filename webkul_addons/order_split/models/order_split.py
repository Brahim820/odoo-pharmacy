# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
class stock_picking(models.Model):
	_inherit = 'stock.picking'
	@api.multi
	def split_action(self):
		context =  dict(self._context or {})
		context.update({
		    'active_model': self._name,
		    'active_ids': self.ids,
		    'active_id': len(self.ids) and self.ids[0] or False
		})
		transfer_id = self.env['wk.split.transfer.wizard'].with_context(context).create({})
		return {
				'name':"Split transfer",
				'view_mode': 'form',
				'view_id': False,
				'view_type': 'form',
				'res_model': 'wk.split.transfer.wizard',
				'res_id': transfer_id.id,
				'type': 'ir.actions.act_window',
				'nodestroy': True,
				'target': 'new',
				'domain': '[]',
				'context':context
				}

	