# -*- coding: utf-8 -*-
from math import ceil
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    attr_width = fields.Float(string="Width (M)",
    digits=dp.get_precision('Product Unit of Measure'),
    help='In meters',
    default=0.0)

    attr_length = fields.Float(string="Length (M)",
    digits=dp.get_precision('Product Unit of Measure'),
    help='In meters',
    default=0.0)

    attr_area = fields.Float(string="Area (M2)",
    digits=dp.get_precision('Product Unit of Measure'),
    compute="_compute_prod_area",
    store=1,
    readonly=1)

    @api.depends('attr_length','attr_width')
    def _compute_prod_area(self):
        for prod in self:
            if prod.attr_length > 0 and prod.attr_width > 0:
                prod.attr_area = prod.attr_width * prod.attr_length


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    attr_width = fields.Float(related="product_id.attr_width", readonly=1)
    attr_length = fields.Float(related="product_id.attr_length", readonly=1)
    attr_area = fields.Float(related="product_id.attr_area", readonly=1)
    request_qty = fields.Float("Req. Qty", help="Requested qty for Dimension calculation")

    @api.onchange('request_qty','product_uom','product_id')
    @api.constrains('request_qty','product_uom','product_id')
    def _calc_dimension_qty(self):
        if self.attr_area > 0.0:
            self.product_uom_qty = ceil(self.request_qty * self.product_uom.factor)
        else:
            self.request_qty = 0
