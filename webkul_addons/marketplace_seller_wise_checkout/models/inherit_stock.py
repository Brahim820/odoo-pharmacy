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
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def action_done(self):
        result = super(StockMove, self).action_done()
        for rec in self:
            if rec.state == "done":
                so_obj = self.env["sale.order"].sudo().search([('name', '=', rec.origin)], limit=1)
                if so_obj and so_obj.marketplace_seller_id:
                    all_sol_not_shipped = so_obj.order_line.filtered(lambda l: l.marketplace_state != 'shipped')
                    so_obj.sudo().mp_order_state = "approved" if all_sol_not_shipped else "shipped"
        return result

    @api.multi
    def write(self, values):
        result = super(StockMove, self).write(values)
        for rec in self:
            if rec.state == "cancel":
                so_obj = self.env["sale.order"].sudo().search([('name', '=', rec.origin)], limit=1)
                if so_obj and so_obj.marketplace_seller_id:
                    so_obj.sudo().mp_order_state = "cancel"
        return result
