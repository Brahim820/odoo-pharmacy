# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductCat(models.Model):
    _inherit = 'product.category'
    product_manager = fields.Many2one('res.users', string='Product Manager')

    @api.depends('parent_id.product_manager')
    def get_n_set_prod_manager(self):
        for cat in self:
            cat.product_manager = cat.parent_id.product_manager

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    product_manager = fields.Many2one('res.users', string='Product Manager')

    @api.depends('categ_id.product_manager')
    def get_product_manager(self):
        for prod in self:
            prod.product_manager = prod.categ_id.product_manager

class ProductProduct(models.Model):
    _inherit = 'product.product'
    product_manager = fields.Many2one('res.users', string='Product Manager',
    readonly="1", related="product_tmpl_id.product_manager")
