# -*- coding: utf-8 -*-

from odoo import models, fields, api


class saleOrder(models.Model):
    _inherit = 'sale.order'

    disc_total = fields.Float(string='Total Discount',compute="_discount_all")
    total_b4_disc = fields.Float(string='Total Before Discount',compute="_total_all")

    @api.multi
    @api.depends('order_line.disc_line')
    def _discount_all(self):
        for order in self:
            tot_disc=0
            for line in order.order_line:
                tot_disc += line.disc_line
            order.disc_total=tot_disc

    @api.multi
    @api.depends('order_line.total_line')
    def _total_all(self):
        for order in self:
            tot_all = 0.0
            for line in order.order_line:
                tot_all += line.total_line
            order.total_b4_disc = tot_all

class saleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    disc_line = fields.Float(string='Discount',compute="_discount_line")
    total_line = fields.Float(string='Total',compute="_total_line")

    @api.multi
    @api.depends('price_unit','discount','product_uom_qty')
    def _discount_line(self):
        for line in self:
            line.disc_line=line.price_unit*((line.discount or 0.0)/100.0) * line.product_uom_qty


    @api.multi
    @api.depends('price_unit','product_uom_qty')
    def _total_line(self):
        for line in self:
            line.total_line = line.price_unit * line.product_uom_qty

