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

from odoo import api, models, fields, _
import logging
import random
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    marketplace_seller_id = fields.Many2one("res.partner", string="Seller", domain="[('seller','=',True)]")
    mp_order_state = fields.Selection([
        ("new","New"),
        ("approved","Approved") ,
        ("shipped","Shipped"),
        ("cancel","Cancelled")], default="new", copy=False)

    @api.multi
    def button_seller_approve_order(self):
        for rec in self:
            if rec.marketplace_seller_id:
                rec.sudo().action_confirm()
                rec.sudo().write({'mp_order_state':'approved'})

    @api.multi
    def action_cancel(self):
        res = super(SaleOrder,self).action_cancel()
        for rec in self:
            if rec.marketplace_seller_id:
                rec.write({'mp_order_state':'cancel'})
        return res

    @api.multi
    def action_draft(self):
        result = super(SaleOrder,self).action_draft()
        for rec in self:
            if rec.marketplace_seller_id:
                rec.write({'mp_order_state':'new'})
        return result

    @api.multi
    def action_view_delivery(self):
        res = super(SaleOrder, self).action_view_delivery()
        if self._context.get('mp_order'):
            action = self.env.ref('odoo_marketplace.marketplace_stock_picking_action').read()[0]
            pickings = self.mapped('picking_ids')
            if len(pickings) > 1:
                action['domain'] = [('id', 'in', pickings.ids)]
            elif pickings:
                action['views'] = [(self.env.ref('odoo_marketplace.marketplace_picking_stock_modified_form_view').id, 'form')]
                action['res_id'] = pickings.id
            return action
        return res
