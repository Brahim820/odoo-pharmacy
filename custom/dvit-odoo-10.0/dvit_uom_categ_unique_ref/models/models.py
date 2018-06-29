# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _


class ProductUOM(models.Model):
    _inherit = 'product.uom'

    @api.constrains('category_id','uom_type','factor','factor_inv')
    def check_unique_ref_unit(self):
        uom_ids = self.env['product.uom'].search([
        ('category_id','=',self.category_id.id),'|',
        ('uom_type','=','reference'),
        ('factor','=',1)
        ])
        if len(uom_ids) > 1:
            # raise UserError(
            raise exceptions.ValidationError(_('There is already a reference UoM in this category of units, can not add another one. Please use a bigger or smaller ratio for this unit'))
