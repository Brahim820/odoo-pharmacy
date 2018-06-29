# -*- encoding: utf-8 -*-

from odoo import fields, models, api
import odoo.addons.decimal_precision as dp


class product_pack(models.Model):
    _name = 'product.pack.line'
    _rec_name = 'product_id'

    parent_product_id = fields.Many2one(
        'product.product',
        'Parent Product',
        ondelete='cascade',
        required=True
        )
    quantity = fields.Float(
        'Quantity',
        required=True,
        default=1.0,
        digits=dp.get_precision('Product UoS'),
        )
    product_id = fields.Many2one(
        'product.product',
        'Product',
        ondelete='cascade',
        required=True,
        )
    discount = fields.Float(
        'Discount (%)',
        digits=dp.get_precision('Discount'),
        )
    price_unit = fields.Float(
        'Unit Price',
        readonly=True,
        related='product_id.list_price',
        digits=dp.get_precision('Product Price'),
        )
    price_subtotal = fields.Float(
        'Subtotal',
        readonly=True,
        compute='_get_total_line',
        digits=dp.get_precision('Product Price'),
        )

    @api.onchange('product_id','quantity')
    def _get_total_line(self):
        price_subtotal = 0.0
        for line in self:
            line.price_subtotal = line.price_unit * line.quantity
        # return price_subtotal

    def get_sale_order_line_vals(self, line, order):
        self.ensure_one()
        # pack_price = 0.0
        subproduct = self.product_id
        quantity = self.quantity * line.product_uom_qty

        taxes = order.fiscal_position_id.map_tax(subproduct.taxes_id)
        tax_id = [(6, 0, taxes.ids)]

        if subproduct.uom_id:
            uom_id = subproduct.uom_id.id
            uom_qty = quantity
        else:
            uom_id = False
            uom_qty = quantity

        # if pack is fixed price or totlice price we don want amount on
        # pack lines
        if line.product_id.pack_price_type in ['fixed_price']:
            price = 0.0
            discount = 0.0
        elif line.product_id.pack_price_type in ['totalice_price']:
            pricelist = order.pricelist_id.id
            discount = 0.0
            price=0
        else:
            pricelist = order.pricelist_id.id
            price = self.env['product.pricelist'].price_get(subproduct.id, quantity,order.partner_id.id)[pricelist]
            discount = self.discount

        # Obtain product name in partner's language
        if order.partner_id.lang:
            subproduct = subproduct.with_context(
                lang=order.partner_id.lang)
        subproduct_name = subproduct.name
        if subproduct.description_sale:
            subproduct_name += '\n'+subproduct.description_sale
        if subproduct.default_code:
            subproduct_name = '['+subproduct.default_code+'] '+subproduct_name

        vals = {
            'order_id': order.id,
            'name': '%s%s' % (
                '' * (line.pack_depth + 1), subproduct_name
            ),
            # 'delay': subproduct.sale_delay or 0.0,
            'product_id': subproduct.id,
            # 'procurement_ids': (
            #     [(4, x.id) for x in line.procurement_ids]
            # ),
            'price_unit': price,
            'tax_id': tax_id,
            'address_allotment_id': False,
            'product_uom_qty': quantity,
            'product_uom': subproduct.uom_id.id,
            'product_uos_qty': uom_qty,
            'product_uos': uom_id,
            'product_packaging': False,
            'discount': discount,
            'number_packages': False,
            'th_weight': False,
            'state': 'draft',
            'pack_parent_line_id': line.id,
            'pack_depth': line.pack_depth + 1,
        }
        return vals

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
