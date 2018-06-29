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

from odoo import api, fields, models, _  # alphabetically ordered
import logging
_logger = logging.getLogger(__name__)

def _set_product_domain(self):
    _logger.info(
        "-------_set_product_domain-------%r---------------------", self._context)
    # if self._context.get('mp_seller_sale_offer'):
    login_ids = []
    seller_group = self.env['ir.model.data'].get_object_reference(
        'odoo_marketplace', 'marketplace_seller_group')[1]
    officer_group = self.env['ir.model.data'].get_object_reference(
        'odoo_marketplace', 'marketplace_officer_group')[1]
    groups_ids = self.env.user.sudo().groups_id.ids
    if seller_group in groups_ids and officer_group not in groups_ids:
        login_ids.append(self.env.user.sudo().partner_id.id)
        marketplace_seller_id = self.env.user.sudo().partner_id.id
    elif seller_group in groups_ids and officer_group in groups_ids:
        obj = self.env['res.partner'].search([('seller', '=', True)])
        for rec in obj:
            login_ids.append(rec.id)
    domain = {'product_id': [
        ('marketplace_seller_id', 'in', login_ids), ('status', '=', 'approved')]}
    return {'domain': domain}
    # return self.env['product.product']

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pharmacy_discount = fields.Float("Discount (%)")
    bogo_offer_rule_ids = fields.One2many(
        "bogo.offer.rule", "mp_product_tmpl_id", "Bonus Product Offers")


class BogoOfferRule(models.Model):
    # Private attributes
    _name = 'bogo.offer.rule'
    _description = 'Model for bogo(Buy One Get One like offer) offer rule'
    _rec_name = "product_id"

    mp_product_tmpl_id = fields.Many2one(
        "product.template", "Product", required=True)
    min_ordered_qty = fields.Float("Min Ordered Qty", required=True, help="To get bonus product.")
    product_id = fields.Many2one(
        "product.product", "Bonus Product", required=True)
    free_qty = fields.Float("Free Quantity", required=True)
    free_qty_type = fields.Selection(
        [("percentage", "Percentage"), ("fixed", "Fixed")], default="percentage", required=True)
    
    @api.multi
    @api.onchange('product_id')
    def _set_product_template(self):
        return _set_product_domain(self)
