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

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import datetime
from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
from lxml import etree
from openerp.osv.orm import setup_modifiers
import openerp.addons.decimal_precision as dp
import decimal

import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_global_product = fields.Boolean(string="Global Product")
    global_product_tmpl_id = fields.Many2one(
        string="Global Product",
        comodel_name="product.template",
        domain=[('is_global_product', '=', True)],
        help="Related Global product.",
    )
    seller_product_ids = fields.One2many(
        string="Seller Products",
        comodel_name="product.template",
        inverse_name="global_product_tmpl_id",
        domain=[('marketplace_seller_id', '!=', False), ('active', '=', True)],
        help="")
    mp_display = fields.Boolean("Display")
    criteria_to_dispaly_one_product = fields.Selection(
        string="Field name",
        selection=[
                ('default', 'Global Product Only'),
                ('low_price', 'Lowest Price Product'),
                ('high_price', 'Highest Price Product'),
                ('manual', 'Set Product Manually'),
        ],
        help="Criteria to dispaly one product of all comparison products on website.",
        compute="_get_value_from_config"
    )
    wk_hide_on_web = fields.Boolean(
        string="Hide",
        compute='_hide_from_website',
        search='_search_hide_on_web_field',
        help="",
    )

    _sql_constraints = [
        ('seller_single_product_uniq', 'unique (marketplace_seller_id, global_product_tmpl_id)', 'You can not assign new product because you have already assigned an product with this global product.')
    ]

    @api.multi
    @api.depends("mp_display")
    def _hide_from_website(self):
        config_setting_obj = self.env['marketplace.config.settings'].sudo().get_default_values()
        for rec in self:
            if rec.seller_product_ids:
                if not config_setting_obj.get("dispaly_comparison_product") or config_setting_obj.get("dispaly_comparison_product") == "one":
                    if config_setting_obj.get("criteria_to_dispaly_one_product") == "low_price":
                        product_objs = rec + rec.seller_product_ids
                        sorted_product_objs = product_objs.filtered(lambda x: x.website_published).sorted(key=lambda r: r.list_price)
                        for obj in product_objs:
                            obj.wk_hide_on_web = True
                        if sorted_product_objs:
                            if not rec.is_global_product and config_setting_obj.get("on_inactive_global_product", False) == "as_a_normal_product":
                                sorted_product_objs[0].wk_hide_on_web = False
                            elif rec.is_global_product:
                                sorted_product_objs[0].wk_hide_on_web = False
                    elif config_setting_obj.get("criteria_to_dispaly_one_product") == "high_price":
                        product_objs = rec + rec.seller_product_ids
                        sorted_product_objs = product_objs.filtered(lambda x: x.website_published).sorted(key=lambda r: r.list_price)
                        for obj in product_objs:
                            obj.wk_hide_on_web = True
                        if sorted_product_objs:
                            if not rec.is_global_product and config_setting_obj.get("on_inactive_global_product", False) == "as_a_normal_product":
                                sorted_product_objs[len(sorted_product_objs) - 1].wk_hide_on_web = False
                            elif rec.is_global_product:
                                sorted_product_objs[len(sorted_product_objs) - 1].wk_hide_on_web = False
                    elif config_setting_obj.get("criteria_to_dispaly_one_product") == "manual":
                        product_objs = rec + rec.seller_product_ids
                        for obj in product_objs:
                            obj.wk_hide_on_web = True
                        sorted_product_objs = product_objs.filtered(lambda x: x.website_published and x.mp_display)
                        if sorted_product_objs and not rec.is_global_product and config_setting_obj.get("on_inactive_global_product", False) == "as_a_normal_product":
                            for o in sorted_product_objs:
                                o.wk_hide_on_web = False
                        elif sorted_product_objs and rec.is_global_product:
                            for o in sorted_product_objs:
                                o.wk_hide_on_web = False

    @api.multi
    def _search_hide_on_web_field(self, operator, value):
        product_ids = []
        for obj in self.sudo().search([]):
            if not obj.wk_hide_on_web:
                product_ids.append(obj.id)
        return [('id', 'in', product_ids)]

    @api.multi
    @api.depends("mp_display")
    def _get_value_from_config(self):
        for rec in self:
            rec.criteria_to_dispaly_one_product = self.env['ir.values'].sudo().get_default('marketplace.config.settings', 'criteria_to_dispaly_one_product')

    @api.multi
    def set_mp_display(self):
        self.ensure_one()
        if self.is_global_product:
            self.mp_display = True
            for rec in self.seller_product_ids:
                rec.mp_display = False
        elif self.global_product_tmpl_id:
            self.global_product_tmpl_id.mp_display = False
            for obj in self.global_product_tmpl_id.seller_product_ids:
                obj.mp_display = False
            self.mp_display = True
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    @api.multi
    def action_on_removal_global_product(self):
        config_setting_obj = self.env['marketplace.config.settings'].sudo().get_default_values()
        if not config_setting_obj.get("on_inactive_global_product", False) or config_setting_obj.get("on_inactive_global_product", False) == "inactive_all":
            for product in self:
                linked_products = self.search([("global_product_tmpl_id", "=", product.id)])
                for p in linked_products:
                    p.website_published = False
                    p.active = False

    @api.multi
    def action_on_making_global_product(self):
        for product in self:
            linked_products = self.search([("global_product_tmpl_id", "=", product.id), ("active", "=", False)])
            for p in linked_products:
                p.website_published = False
                p.active = True

    @api.multi
    def toggle_global_product(self):
        for rec in self:
            if rec.is_global_product:
                rec.action_on_removal_global_product()
            else:
                rec.action_on_making_global_product()
            rec.is_global_product = not rec.is_global_product

    @api.multi
    @api.constrains('seller_product_ids')
    def _check_seller_product_ids(self):
        for product in self:
            if product.global_product_tmpl_id.global_product_tmpl_id:
                raise ValidationError(_('You cannot assign new product to this product because this product is already assigned with %s product') %product.name)
