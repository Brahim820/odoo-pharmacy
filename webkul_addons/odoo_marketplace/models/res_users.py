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

from odoo import api, fields, models, _
from odoo.tools.translate import _

import logging
_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def signup(self, values, token=None):
        """ """
        context = dict(self._context or {})     
        if values.get('is_seller', False):
            context["is_seller"] = values.get('is_seller', False)
            values.pop("is_seller")
        return super(ResUsers, self.with_context(context)).signup(values, token)

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        user_obj = super(ResUsers, self).copy(default=default)
        if self._context and self._context.get('is_seller'):
            # Set Default fields for seller (i.e: payment_methods, commission,
            # location_id, etc...)
            user_obj.partner_id.write({
                "payment_method": [(4, user_obj.partner_id._set_payment_method())],
                "commission": self.env['ir.values'].get_default('marketplace.config.settings', 'global_commission'),
                "location_id": self.env['ir.values'].get_default('marketplace.config.settings', 'warehouse_location_id') or False,
                "warehouse_id": self.env['ir.values'].get_default('marketplace.config.settings', 'default_warehouse') or False,
                "auto_product_approve": self.env['ir.values'].get_default('marketplace.config.settings', 'auto_product_approve'),
                "seller_payment_limit": self.env['ir.values'].get_default('marketplace.config.settings', 'seller_payment_limit'),
                "next_payment_request": self.env['ir.values'].get_default('marketplace.config.settings', 'next_payment_requset'),
                "auto_approve_qty": self.env['ir.values'].get_default('marketplace.config.settings', 'auto_approve_qty'),
                "show_seller_since": self.env['ir.values'].get_default('marketplace.config.settings', 'seller_since'),
                "show_seller_address": self.env['ir.values'].get_default('marketplace.config.settings', 'shipping_address'),
                "show_product_count": self.env['ir.values'].get_default('marketplace.config.settings', 'product_count'),
                "show_sale_count": self.env['ir.values'].get_default('marketplace.config.settings', 'sale_count'),
                "show_return_policy": self.env['ir.values'].get_default('marketplace.config.settings', 'return_policy'),
                "show_shipping_policy": self.env['ir.values'].get_default('marketplace.config.settings', 'shipping_policy'),
                "show_seller_review": self.env['ir.values'].get_default('marketplace.config.settings', 'seller_review'),
            })
            # Add user to Pending seller group
            user_obj.partner_id.seller = True
            draft_seller_group_id = self.env['ir.model.data'].get_object_reference('odoo_marketplace', 'marketplace_draft_seller_group')[1]
            groups_obj = self.env["res.groups"].browse(draft_seller_group_id)
            if groups_obj:
                for group_obj in groups_obj:
                    group_obj.write({"users": [(4, user_obj.id, 0)]})
        return user_obj
