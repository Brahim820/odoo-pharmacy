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

class MarketplaceConfigSettings(models.TransientModel):
    _inherit = "marketplace.config.settings"

    group_seller_profile_tabs = fields.Boolean(
        group='odoo_marketplace.marketplace_seller_group',
        implied_group='marketplace_seller_profile_tabs.mp_seller_profile_tab_group',
        string="Allow seller for custom profile Tabs.",
        help="Allow seller to create additional profile tabs to display extra on website."
    )

    @api.one
    def set_default_values(self):
        super(MarketplaceConfigSettings, self).set_default_values()
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'group_seller_profile_tabs', self.group_seller_profile_tabs)
        return True


    @api.model
    def get_default_values(self, fields=None):
        res = super(MarketplaceConfigSettings, self).get_default_values(fields)
        group_seller_profile_tabs = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'group_seller_profile_tabs')
        res.update({"group_seller_profile_tabs" : group_seller_profile_tabs})
        return res

    @api.multi
    def execute(self):
        for rec in self:
            # Update All Seller Setting
            all_seller_objs = rec.env["res.partner"].search(
                [("seller", "=", True), ("state", "=", "approved")])
            for seller_obj in all_seller_objs:
                if not seller_obj.set_seller_wise_settings:
                    vals = {
                        "group_seller_profile_tabs": rec.group_seller_profile_tabs,
                    }
                    seller_obj.write(vals)
        return super(MarketplaceConfigSettings, self).execute()
