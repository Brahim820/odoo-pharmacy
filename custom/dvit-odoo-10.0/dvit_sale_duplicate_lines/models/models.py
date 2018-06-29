# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = ["sale.order.line"]

    duplicate = fields.Boolean("duplicate")


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    @api.constrains('order_line')
    def _check_duplicate(self):
        for line in self.order_line:
            if any(l.id != line.id and l.product_id == line.product_id for l in line.order_id.order_line):
                line.duplicate = True
            else:
                line.duplicate = False
