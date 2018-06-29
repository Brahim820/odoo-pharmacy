# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit=["sale.order"]
    option_line_ids  = fields.One2many('sale.option.line', 'order_id', string='Optional Products',)

class SaleOptionLine(models.Model):
    _name="sale.option.line"
    order_id=fields.Many2one("sale.order")
    product_id = fields.Many2one("product.product", "product")
    name = fields.Text("Description")
    price_unit = fields.Float("Unit price")
    @api.onchange('product_id')
    def _onchange_discount(self):
        self.price_unit=self.product_id.lst_price
        self.name=self.product_id.name
