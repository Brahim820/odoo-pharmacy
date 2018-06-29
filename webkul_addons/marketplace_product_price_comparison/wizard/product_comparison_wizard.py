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

from odoo import api, fields, models
import odoo.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class GlobalProductAssignWizard(models.TransientModel):
    _name = "global.product.assign.wizard"
    _description = "Assign global product with seller product."

    @api.model
    def _get_seller_id(self):
        return self.env.user.partner_id.id if self.env.user.partner_id.seller else False

    product_id = fields.Many2one('product.template', string='Global Product', required=True, domain=[('is_global_product', '=', True)])
    currency_id = fields.Many2one('res.currency', related="product_id.currency_id")
    product_name = fields.Char("Product Name", readonly=True)
    initial_qty = fields.Integer("Initial Quantity")
    sale_description = fields.Text("Sale Description")
    list_price = fields.Float("Sale Price", required=True)
    product_image = fields.Binary(string="Product Image")
    warranty = fields.Float("Warranty")
    weight = fields.Float("Weight")
    volume = fields.Float("Volume")
    barcode = fields.Char("Barcode")
    created_product_id = fields.Many2one('product.template', string='Created Product')
    marketplace_seller_id = fields.Many2one("res.partner", "Seller", domain=[('seller', '=', True)], default=_get_seller_id)

    @api.onchange('product_id')
    def onchange_product(self):
        """ """
        if self.product_id:
            self.product_name = self.product_id.name
            self.product_image = self.product_id.image
            self.sale_description = self.product_id.description_sale
            self.list_price = self.product_id.list_price
        else:
            self.product_name = False
            self.product_image = False
            self.sale_description = False


    @api.multi
    def create_seller_comparison_product(self):
        self.ensure_one()
        config_setting_obj = self.env[
            'marketplace.config.settings'].sudo().get_default_values()
        product_vals = {
            'name' : self.product_name,
            'global_product_tmpl_id' : self.sudo().product_id.id,
            'name' : self.product_name,
            'qty' : self.initial_qty,
            'sale_description': self.sale_description,
            'list_price' : self.list_price,
            'image' : self.product_image,
            'warranty' : self.warranty,
            'weight' : self.weight,
            'volume' : self.volume,
            'barcode' : self.barcode,
            'marketplace_seller_id': self.marketplace_seller_id.id if self.marketplace_seller_id else self.env.user.partner_id.id if self.env.user.partner_id.seller else False,
        }
        if not product_vals.get("marketplace_seller_id", False):
            raise Warning(_("Please select seller first."))
        created_product = self.env["product.template"].create(product_vals)
        if created_product:
            created_product.set_pending()
            created_product.public_categ_ids = self.product_id.public_categ_ids

    @api.model
    def create(self, vals):
        if not vals.get("product_name", False) and vals.get("product_id", False):
            product_obj = self.env["product.template"].browse(vals.get("product_id", False))
            vals.update({"product_name": product_obj.name})
        return super(GlobalProductAssignWizard, self).create(vals)

class ManageGlobalProduct(models.TransientModel):
    _name = "manage.global.product"
    _description = "Make product to a global product."

    product_ids = fields.Many2many(
        string="Select Products",
        comodel_name="product.template",
        domain=[('type', '=', 'product'), ('sale_ok', '=', True)],
        help="Select products which you want to make global.",
    )
    action_type = fields.Selection([('make_global', 'Add Product to Global Product List'), ('remove_global', 'Remove Product from Global Product List')], default="make_global", required=True)

    @api.multi
    def create_global_product(self):
        self.ensure_one()
        if self.product_ids:
            self.product_ids.write({'is_global_product' : True, 'mp_display':True})
            self.product_ids.action_on_making_global_product()

    @api.multi
    def remove_global_product(self):
        self.ensure_one()
        if self.product_ids:
            self.product_ids.write({'is_global_product' : False})
            self.product_ids.action_on_removal_global_product()

    @api.onchange("action_type")
    def _onchange_action_type(self):
        vals = {}
        if self.action_type == "remove_global":
            vals['domain'] = {
                "product_ids": [('is_global_product', '=', True)],
            }
            self.product_ids = False
        else:
            vals['domain'] = {
                "product_ids": [('website_published', '=', True), ('type', '=', 'product'), ('sale_ok', '=', True), ('is_global_product', '=', False), ('global_product_tmpl_id', '=', False)],
            }
            self.product_ids = False
        return vals
