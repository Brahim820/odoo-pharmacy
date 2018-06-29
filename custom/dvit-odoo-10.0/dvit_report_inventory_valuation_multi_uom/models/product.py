# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from lxml import etree


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    available_uom_ids = fields.Many2many('product.uom', string='Available Uom')
    available_uom_domain_ids = fields.Many2many('product.uom', store=False, readonly=True,
                                                compute='_compute_available_uom_domain')

    @api.multi
    @api.depends('uom_id')
    def _compute_available_uom_domain(self):
        for record in self:
            if record.uom_id:
                filter_by = self.env['product.uom'].sudo().search(
                    [('category_id', '=', record.uom_id.category_id.id), ('active', '=', True),
                     ('id', '!=', record.uom_id.id)]).mapped('id')

                record.available_uom_domain_ids = filter_by

    @api.onchange('uom_id')
    def _onchange_uom_id(self):
        super(ProductTemplate, self)._onchange_uom_id()
        if self.uom_id:
            filter_by = self.env['product.uom'].sudo().search(
                [('category_id', '=', self.uom_id.category_id.id), ('active', '=', True),
                 ('id', '!=', self.uom_id.id)]).mapped('id')
            return {'domain': {'available_uom_ids': [('id', 'in', list(filter_by))]},
                    }
