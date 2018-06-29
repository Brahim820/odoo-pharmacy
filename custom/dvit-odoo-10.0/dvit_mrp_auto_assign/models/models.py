# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.model
    def create(self, values):
        production = super(MrpProduction, self).create(values)
        prod_man = production.product_id.product_tmpl_id.product_manager and \
        production.product_id.product_tmpl_id.product_manager or production.product_id.categ_id.product_manager
        if prod_man:
          production.user_id = prod_man
        return production
