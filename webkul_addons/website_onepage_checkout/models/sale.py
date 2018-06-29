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
from odoo import api, fields, models
from odoo.addons import decimal_precision


class SaleOrder(models.Model):
    """Overwrites and add Definitions to module: sale."""

    _inherit = 'sale.order'

    amount_subtotal = fields.Float(
        compute='_compute_amount_subtotal',
        digits=decimal_precision.get_precision('Account'),
        string='Subtotal Amount',
        store=True,
        help="The amount without anything.",
        track_visibility='always'
    )

    @api.depends('order_line', 'order_line.price_subtotal')
    def _compute_amount_subtotal(self):
        """compute Function for amount_subtotal."""
        for rec in self:
            line_amount = sum([line.price_subtotal for line in
                               rec.order_line if not line.is_delivery])
            currency = rec.pricelist_id.currency_id
            rec.amount_subtotal = currency.round(line_amount)

# Responsible Developer:- Sunny Kumar Yadav #