from odoo import models, fields, api, exceptions, _

from itertools import groupby
from datetime import datetime, timedelta

from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp


class WizTaskStockLines(models.TransientModel):
    _name = "wiz.task.stock.line"
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        )
    product_qty = fields.Float(string="Qty in default UoM", )
    wiz_stock_id = fields.Many2one(
        string="wiz stock",
        comodel_name="wiz.task.stock",
    )
    @api.onchange('product_id')
    def onchange_product_id(self):
        self.product_qty = 1.0 if not self.product_qty and self.product_id \
            else self.product_qty

class WizTaskStock(models.TransientModel):
    _name = 'wiz.task.stock'

    move_lines = fields.One2many(
        string="Products",
        comodel_name="wiz.task.stock.line",
        inverse_name="wiz_stock_id",
    )
    task_id = fields.Many2one(
        comodel_name='project.task', string='Task', select=True,
        default=lambda self: self.env.context.get('active_id', False))
    invoice_state = fields.Selection(
        string="Invoice control",
        selection=[
                ('invoiced', 'Invoiced'),
                ('2binvoiced', 'To Invoice'),
                ('none', 'Not Applicable'),
                ],
    )

    def _prepare_picking(self, task):
        pick_type = self.env['stock.picking.type'].search([('code','=','outgoing')])[0]
        pick_vals = {
            'partner_id': task.partner_id.id,
            'picking_type_id': pick_type.id,
            'task_id': task.id,
            'invoice_state': self.invoice_state,
            'origin': task.name,
            'location_id': pick_type.default_location_src_id.id,
            'location_dest_id': task.partner_id.property_stock_customer.id,
            'analytic_account_id': task.project_id.analytic_account_id.id,
        }
        
        pick_id = self.env['stock.picking'].create(pick_vals)

        move_obj = self.env['stock.move']
        proc_obj = self.env['procurement.order']
        for line in self.move_lines:
            move_vals = {
                'product_id': line.product_id.id,
                'product_uom': line.product_id.uom_id.id,
                'product_uom_qty': line.product_qty,
                'name': task.project_id.name + '>' + task.name,
                'origin': task.project_id.name + '>' + task.name,
                'picking_id': pick_id.id,
                'location_id': pick_id.location_id.id,
                'location_dest_id': pick_id.location_dest_id.id,
            }
            move_id = move_obj.create(move_vals)
            procurement = proc_obj.create(move_id._prepare_procurement_from_move())
            if procurement:
                procurement.run()
            move_obj.action_assign(no_prepare=True)

        return pick_id

    @api.multi
    def add_pick(self):
        pick_id = self._prepare_picking(self.task_id)
        pick_id.action_confirm()

        return pick_id
