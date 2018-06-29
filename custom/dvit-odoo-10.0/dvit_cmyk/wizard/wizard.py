from odoo import models, fields, api


class WizTaskStockLines(models.TransientModel):
    _inherit = "wiz.prod.uom.line"

    attr_area = fields.Float(related="wiz_id.product_id.attr_area", )

    @api.onchange('uom')
    def get_qty(self):
        self.qty = self.wiz_id.product_id.attr_length

    @api.onchange('qty')
    def update_qty(self):
        self.qty_m2 = self.qty * self.wiz_id.product_id.attr_width
