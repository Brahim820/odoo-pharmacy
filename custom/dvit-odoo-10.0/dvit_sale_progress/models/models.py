# -*- coding: utf-8 -*-

from odoo import _, api, exceptions, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    deliver_prcnt = fields.Float(string="Delivered %",
    compute="calc_prcnt", sotre=True)

    invoice_prcnt = fields.Float(string="Invoiced %",
    compute="calc_prcnt", store=True)

    @api.depends('order_line.qty_delivered','order_line.qty_invoiced')
    def calc_prcnt(self):
        for order in self:
            if not order.order_line:
                continue
            total_qty, dlvrd_qty, invoiced_qty = (0.0,)*3
            for line in order.order_line:
                total_qty += line.product_uom_qty
                dlvrd_qty += line.qty_delivered
                invoiced_qty += line.qty_invoiced

            order.update({
            'invoice_prcnt': (invoiced_qty / total_qty) * 100,
            'deliver_prcnt': (dlvrd_qty / total_qty) * 100,
            })
            
