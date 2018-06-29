from odoo import models, fields, api


class WizTaskStockLines(models.TransientModel):
    _inherit = "wiz.prod.uom.line"
    qty_m2 = fields.Float(string="Qty M2", readonly=1)

    @api.onchange('qty')
    def update_qty(self):
        self.qty_m2 = self.qty * self.wiz_id.product_id.attr_width


class WizProdUoM(models.TransientModel):
    _inherit = 'wiz.prod.uom'

    ref_uom = fields.Char(default='M2' )
    product_id = fields.Many2one(
        comodel_name='product.template', string='Product', select=True,
        default=lambda self: self.env.context.get('active_id', False))
    attr_area = fields.Float(related="product_id.attr_area", )


    def create_uoms(self):
        product_id = self.product_id
        cat_name = product_id.name.replace(' ','')[:5]
        uom_categ_id = self.env['product.uom.categ'].create({'name':cat_name+'_uoms'})
        ref_uom_id = self.env['product.uom'].create({
        'name': self.ref_uom,
        'uom_type': 'reference',
        'category_id': uom_categ_id.id,
        'rounding': 0.001,
        'factor': 1,
        'factor_inv': 1,
        })
        product_id.write({
        'uom_id': ref_uom_id.id,
        'uom_po_id': ref_uom_id.id,
        })
        for line in self.line_ids:
            if product_id.attr_area != 0.0:
                line.qty_m2 = line.qty * product_id.attr_width
            else:
                line.qty_m2 = line.qty

            self.env['product.uom'].create({
            'name': line.uom,
            'uom_type': line.utype,
            'factor_inv': line.utype == 'bigger' and line.qty_m2 or (1/abs(line.qty_m2)),
            'factor': line.utype == 'smaller' and abs(line.qty_m2) or (1/abs(line.qty_m2)),
            'category_id': uom_categ_id.id,
            'rounding': 0.001,
            })

        return True

    @api.multi
    def add_uoms(self):
        uom_ids = self.create_uoms()

        return True
