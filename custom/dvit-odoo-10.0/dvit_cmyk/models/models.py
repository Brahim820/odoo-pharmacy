# -*- coding: utf-8 -*-
from math import ceil
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    name = fields.Char(default=" ", )

    business_unit_id = fields.Many2one("product.business.unit","Business Unit")
    bunit_group_id = fields.Many2one("product.business.unit.group","Business Unit Group")
    main_group_id = fields.Many2one("product.main.group","Main Group")
    type_type_id = fields.Many2one("product.type.type","Type")
    svc_type_id = fields.Many2one("product.service.type","Service")
    comm_name_id = fields.Many2one("product.comm.name","Comm. Name")
    packing_id = fields.Many2one("product.packing","Product Packing")
    color_id = fields.Many2one("product.color","Color")
    attr_width = fields.Float(string="Width (M)",
        digits=dp.get_precision('Product Unit of Measure'),
        help='In meters',
        default=0.0)
    attr_length = fields.Float(string="Length (M)",
        digits=dp.get_precision('Product Unit of Measure'),
        help='In meters',
        default=0.0)
    attr_area = fields.Float(string="Area (M2)",
        digits=dp.get_precision('Product Unit of Measure'),
        compute="_compute_prod_area",
        store=1,
        readonly=1)

    @api.constrains('attr_length','attr_width','business_unit_id',
        'bunit_group_id','type_type_id','svc_type_id','comm_name_id',
        'packing_id', 'main_group_id','color_id')
    def _set_prod_default_code(self):
        for prod in self:
            prod_name = str(
                (prod.comm_name_id and prod.comm_name_id.name+' ' or '')+\
                (prod.svc_type_id and prod.svc_type_id.name+' ' or '')+\
                (prod.attr_area != 0 and str(prod.attr_width)+'x'+str(int(prod.attr_length))+' ' or '')+\
                (prod.packing_id and prod.packing_id.name or '')
                )

            def_code = str(
                (prod.business_unit_id.code or '')+\
                (prod.bunit_group_id.code or '')+\
                (prod.main_group_id.code or '')+\
                (prod.type_type_id.code or '')+\
                (prod.svc_type_id.code or '')+\
                (prod.packing_id.code or '')+\
                (prod.comm_name_id.code or '')+\
                (prod.attr_area != 0 and str(int(prod.attr_length))+'-'+str(prod.attr_width) or '')+\
                (prod.color_id and '-'+str(prod.color_id.code) or '')
            )

            if prod_name != '':
                prod.name = prod_name
            # if def_code != '':
            prod.default_code = def_code

    @api.depends('attr_length','attr_width')
    def _compute_prod_area(self):
        for prod in self:
            if prod.attr_length > 0 and prod.attr_width > 0:
                prod.attr_area = prod.attr_width * prod.attr_length


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    attr_width = fields.Float(related="product_id.attr_width", readonly=1)
    attr_length = fields.Float(related="product_id.attr_length", readonly=1)
    attr_area = fields.Float(related="product_id.attr_area", readonly=1)
    request_qty = fields.Float("Req. Qty", help="Requested qty for Dimension calculation")

    @api.onchange('request_qty','product_uom','product_id')
    @api.constrains('request_qty','product_uom','product_id')
    def _calc_dimension_qty(self):
        if self.attr_area > 0.0:
            self.product_uom_qty = ceil(self.request_qty * self.product_uom.factor)
        else:
            self.request_qty = 0


class ProductCommName(models.Model):
    _name = 'product.comm.name'
    # _rec_name = 'module.rec_name' # optional
    name = fields.Char("Comm. Name", required=1)
    code = fields.Char("Code", required=1)


class ProductMainGroup(models.Model):
    _name = 'product.main.group'
    # _rec_name = 'module.rec_name' # optional
    name = fields.Char("Main Group", required=1)
    code = fields.Char("Code", required=1)


class ProductTypeType(models.Model):
    _name = 'product.type.type'
    # _rec_name = 'module.rec_name' # optional
    name = fields.Char("Type", required=1)
    code = fields.Char("Code", required=1)


class ProductBusinessUnitGroup(models.Model):
    _name = 'product.business.unit.group'
    # _rec_name = 'module.rec_name' # optional
    name = fields.Char("BU Group", required=1)
    code = fields.Char("Code", required=1)


class ProductBusinessUnit(models.Model):
    _name = 'product.business.unit'
    # _rec_name = 'module.rec_name' # optional
    name = fields.Char("Business Unit", required=1)
    code = fields.Char("Code", required=1)


class ProductPacking(models.Model):
    _name = 'product.packing'
    # _rec_name = 'module.rec_name' # optional
    name = fields.Char("Packing", required=1)
    code = fields.Char("Code", required=1)


class ProductColor(models.Model):
    _name = 'product.color'
    # _rec_name = 'module.rec_name' # optional
    name = fields.Char("Color", required=1)
    code = fields.Char("Code", required=1)


class ProductServiceType(models.Model):
    _name = 'product.service.type'
    # _rec_name = 'module.rec_name' # optional
    name = fields.Char("Service", required=1)
    code = fields.Char("Code", required=1)



# class ResCompany(models.Model):
#     _inherit = 'res.company'
#     seq_fields = fields.Char(string="Field sequences", help='Comma separeted technical field names' )
