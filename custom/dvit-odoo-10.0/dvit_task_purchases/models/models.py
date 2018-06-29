# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class ProjectTask(models.Model):
    _inherit = 'project.task'
    purchase_ids = fields.One2many(string="Purchase Orders",
    comodel_name="purchase.order",
    inverse_name="task_id")

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    task_id = fields.Many2one(string="Task",comodel_name="project.task")
    sale_id = fields.Many2one(string="Sale order", comodel_name="sale.order")

class WizPurchaseOrder(models.TransientModel):
    _name = 'wiz.purchase.order'
    line_ids = fields.One2many(string="Lines",
        comodel_name="wiz.purchase.order.line",
        inverse_name="wiz_id", )
    vendor_id = fields.Many2one(
        string="Vendor",
        comodel_name="res.partner",
        domain="[('supplier', '=', 1)]",
        required=1,  )

    @api.multi
    def add_po(self):
        task_id = self.env['project.task'].browse(self._context.get('active_id'))
        p_vals = {
            'partner_id': self.vendor_id.id,
            'date_planned': datetime.today(),
            }
        po_id = self.env['purchase.order'].sudo().create(p_vals)

        for line in self.line_ids:
            pl_vals = {
                'product_id': line.product_id.id,
                'name': line.name,
                'product_qty': line.product_qty,
                'date_planned': datetime.today(),
                'price_unit': line.product_id.standard_price,
                'product_uom': line.product_uom.id,
                'order_id': po_id.id,
                }
            self.env['purchase.order.line'].sudo().create(pl_vals)
        sale_id = task_id.sale_line_id.order_id and task_id.sale_line_id.order_id or self.env['sale.order'].search([('project_project_id','=',task_id.project_id)])
        if sale_id:
            po_id.sale_id = sale_id
        task_id.purchase_ids += po_id

class WizPurchaseOrderLine(models.TransientModel):
    _name = 'wiz.purchase.order.line'

    wiz_id = fields.Many2one(string="purchase wizard", comodel_name="wiz.purchase.order" )
    product_id = fields.Many2one('product.product', string='Product')
    name = fields.Char( string='Description')
    product_qty = fields.Float( string='Quantity',default=1.0)
    product_uom = fields.Many2one('product.uom', string='UoM',
        domain="[('category_id', '=', product_id.uom_id.category_id)]",)

    @api.onchange('product_id')
    def change_description(self):
        self.name = self.product_id.name
        self.product_uom = self.product_id.uom_po_id
