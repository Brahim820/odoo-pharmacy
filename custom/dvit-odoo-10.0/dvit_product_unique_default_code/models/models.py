# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def copy(self, default=None):  # pylint: disable=W0622
        if not default:
            default = {}
        default['default_code'] = ""
        return super(ProductTemplate, self).copy(default=default)

    _sql_constraints = [
        ('default_code_unique', 'UNIQUE(default_code)', 'Internal Reference already exists !'),
    ]


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def copy(self, default=None):  # pylint: disable=W0622
        if not default:
            default = {}
        default['default_code'] = ""
        return super(ProductProduct, self).copy(default=default)

    _sql_constraints = [
        ('default_code_unique', 'UNIQUE(default_code)', 'Internal Reference already exists !'),
    ]
