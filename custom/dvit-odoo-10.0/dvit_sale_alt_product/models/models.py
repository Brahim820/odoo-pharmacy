# -*- coding: utf-8 -*-

from odoo import models, fields, api



class saleOrdeLine(models.Model):
    _inherit = 'sale.order.line'

    alt_product_id = fields.Many2one("product.product",'Alternative Product')
