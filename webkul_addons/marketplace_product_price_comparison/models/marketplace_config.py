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

from odoo.exceptions import except_orm, Warning, RedirectWarning

import logging
_logger = logging.getLogger(__name__)


class MarketplaceConfigSettings(models.TransientModel):
    _inherit = "marketplace.config.settings"

    dispaly_comparison_product = fields.Selection(
        string="Display",
        selection=[
                ('one', 'Only One Comparison Product'),
                ('all', 'All Comparison Products'),
        ],
        help="Select option for comparison products.",
    )
    criteria_to_dispaly_one_product = fields.Selection(
        string="Field name",
        selection=[
                ('default', 'Global Product Only'),
                ('low_price', 'Lowest Price Product'),
                ('high_price', 'Highest Price Product'),
                ('manual', 'Set Product Manually'),
        ],
        help="Criteria to dispaly one product of all comparison products on website."
    )
    on_inactive_global_product = fields.Selection(
        string="On inactive global product action on linked comparison products",
        selection=[
                ('as_a_normal_product', 'Show as a Normal Product'),
                ('inactive_all', 'Inactive all linked comparison products'),
        ],
        help="When global product removed from global product list then what action should be taken on linked comparison products."
    )

    @api.one
    def set_default_values(self):
        super(MarketplaceConfigSettings, self).set_default_values()
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'dispaly_comparison_product', self.dispaly_comparison_product)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'criteria_to_dispaly_one_product', self.criteria_to_dispaly_one_product)
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'on_inactive_global_product', self.on_inactive_global_product)
        return True


    @api.model
    def get_default_values(self, fields=None):
        res = super(MarketplaceConfigSettings, self).get_default_values(fields)
        dispaly_comparison_product = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'dispaly_comparison_product')
        criteria_to_dispaly_one_product = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'criteria_to_dispaly_one_product')
        on_inactive_global_product = self.env['ir.values'].get_default(
            'marketplace.config.settings', 'on_inactive_global_product')
        res.update({
            "dispaly_comparison_product" : dispaly_comparison_product,
            "criteria_to_dispaly_one_product" : criteria_to_dispaly_one_product,
            "on_inactive_global_product" : on_inactive_global_product,
            })
        return res
