# -*- encoding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import Warning
import math


class product_product(models.Model):
    _inherit = 'product.product'

    pack_line_ids = fields.One2many(
        'product.pack.line',
        'parent_product_id',
        'Pack Products',
        help='List of products that are part of this pack.'
        )
    used_pack_line_ids = fields.One2many(
        'product.pack.line',
        'product_id',
        'On Packs',
        help='List of packs where product is used.'
        )

    @api.one
    @api.constrains('pack_line_ids')
    def check_recursion(self):
        """
        Check recursion on packs
        """
        pack_lines = self.pack_line_ids
        while pack_lines:
            if self in pack_lines.mapped('product_id'):
                raise Warning(_(
                    'Error! You cannot create recursive packs.\n'
                    'Product id: %s') % self.id)
            pack_lines = pack_lines.mapped('product_id.pack_line_ids')

    @api.multi
    def write(self, vals):
        res = super(product_product, self).write(vals)
        for prod in self:
            if not prod.pack:
                if vals.get('standard_price'):
                    prod.product_tmpl_id.set_parent_pack_price()
                if vals.get('last_purchase_price'):
                    prod.product_tmpl_id.set_parent_pack_price()
            if vals.get('pack_line_ids'):
                prod.product_tmpl_id.set_pack_price_from_childs()
        return res

class product_template(models.Model):
    _inherit = 'product.template'

    pack_price_type = fields.Selection([
        ('components_price', 'Detailed - Components Prices'),
        ('totalice_price', 'Detailed - Totaliced Price'),
        ('fixed_price', 'Detailed - Fixed Price'),
        ('none_detailed_assited_price', 'None Detailed - Assisted Price'),
        ('none_detailed_totaliced_price', 'None Detailed - Totaliced Price'),
    ],
        'Pack Type',
        help="* Detailed - Components Prices: Detail lines with prices on "
        "sales order.\n"
        "* Detailed - Totaliced Price: Detail lines on sales order totalicing "
        "lines prices on pack (don't show component prices).\n"
        "* Detailed - Fixed Price: Detail lines on sales order and use product"
        " pack price (ignore line prices).\n"
        "* None Detailed - Totaliced Price: Do not detail lines on sales order.\n"
        "* None Detailed - Assisted Price: Do not detail lines on sales "
        "order. Assist to get pack price using pack lines."
        )
    pack = fields.Boolean(
        'Pack?',
        help='Is a Product Pack?',
        )
    pack_line_ids = fields.One2many(
        related='product_variant_ids.pack_line_ids'
        )
    used_pack_line_ids = fields.One2many(
        related='product_variant_ids.used_pack_line_ids'
        )

    @api.constrains(
        'product_variant_ids', 'pack_price_type')
    def check_relations(self):
        """
        Check assited packs dont have packs a childs
        """
        # check assited price has no packs child of them
        if self.pack_price_type == 'none_detailed_assited_price':
            child_packs = self.mapped(
                'pack_line_ids.product_id').filtered('pack')
            if child_packs:
                raise Warning(_(
                    'A "None Detailed - Assisted Price Pack" can not have a '
                    'pack as a child!'))

    @api.one
    @api.constrains('company_id', 'product_variant_ids', 'used_pack_line_ids')
    def check_pack_line_company(self):
        """
        Check packs are related to packs of same company
        """
        for line in self.pack_line_ids:
            if line.product_id.company_id != self.company_id:
                raise Warning(_(
                    'Pack lines products company must be the same as the\
                    parent product company'))
        for line in self.used_pack_line_ids:
            if line.parent_product_id.company_id != self.company_id:
                raise Warning(_(
                    'Pack lines products company must be the same as the\
                    parent product company'))

    @api.multi
    def write(self, vals):
        """
        We remove from prod.prod to avoid error
        """
        if vals.get('pack_line_ids', False):
            self.product_variant_ids.write(
                {'pack_line_ids': vals.pop('pack_line_ids')})
        res = super(product_template, self).write(vals)
        for prod in self.filtered(lambda p: p.pack and p.type != 'service'):
        # set type to service if it's a pack
            prod.type = 'service'
        return res

    @api.onchange('pack_line_ids','pack_price_type','pack')
    def set_pack_price_from_childs(self):
        none_detailed_types = [
            'totalice_price',
            'none_detailed_totaliced_price',
            'none_detailed_assited_price']
        # This should work only in case of totalice or assited packs
        for prod in self:
            if prod.pack and prod.type != 'service':
                prod.type = 'service'
            for pline in prod.pack_line_ids.filtered(lambda l: l.product_id.pack):
                pline.product_id.product_tmpl_id.set_pack_price_from_childs()
            if prod.pack and prod.pack_price_type in none_detailed_types:
                standard_price = sum(l.product_id.standard_price * l.quantity for l in prod.pack_line_ids)
                prod.product_variant_ids.write({'standard_price': standard_price})
                prod.standard_price = standard_price
                prod.list_price = sum(l.product_id.list_price * l.quantity for l in prod.pack_line_ids)
                if hasattr(prod,'last_purchase_price'):
                    last_purchase_price = sum(l.product_id.last_purchase_price * l.quantity for l in prod.pack_line_ids)
                    prod.last_purchase_price = last_purchase_price > 0.0 and last_purchase_price or standard_price

    @api.constrains('standard_price','list_price')
    def set_parent_pack_price(self):
        none_detailed_types = [
            'totalice_price',
            'none_detailed_totaliced_price',
            'none_detailed_assited_price']
        for parent_pack in self.used_pack_line_ids:
            prod = parent_pack.parent_product_id.product_tmpl_id
            if not prod.pack_price_type in none_detailed_types:
                continue
            standard_price = sum(l.product_id.standard_price * l.quantity for l in prod.pack_line_ids)
            prod.product_variant_ids.write({'standard_price': standard_price})
            prod.standard_price = standard_price
            prod.list_price = sum(l.product_id.list_price * l.quantity for l in prod.pack_line_ids)
            if hasattr(prod,'last_purchase_price'):
                last_purchase_price = sum(l.product_id.last_purchase_price * l.quantity for l in prod.pack_line_ids)
                prod.last_purchase_price = last_purchase_price > 0.0 and last_purchase_price or standard_price
            for root_pack in parent_pack.parent_product_id.product_tmpl_id.used_pack_line_ids:
                root_pack.product_id.product_tmpl_id.set_parent_pack_price()
