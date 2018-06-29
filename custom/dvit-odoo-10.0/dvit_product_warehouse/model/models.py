
from odoo import api, fields, models

class ProductTmpl(models.Model):
    _inherit = 'product.template'

    warehouse_id = fields.Many2one(
        string="Default warehouse",
        comodel_name="stock.warehouse",
        help="Will be forced in sale, purchase and manufacture orders.",
        )

    @api.depends('categ_id')
    def _set_wh(self):
        for prod in self:
            product.write({'warehouse_id': categ_id.warehouse_id and categ_id.warehouse_id.id,})

class ProductCat(models.Model):
    _inherit = 'product.category'

    warehouse_id = fields.Many2one(
        string="Default warehouse",
        comodel_name="stock.warehouse",
        help="Will be forced in sale, purchase and manufacture orders of products in this category.",
        )

    @api.depends('parent_id')
    def _set_wh(self):
        warehouse_id = parent_id.warehouse_id

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _prepare_procurement_group_by_line(self, line):
        vals = super(SaleOrder, self)._prepare_procurement_group_by_line(line)
        wh_id = line.product_id.product_tmpl_id.warehouse_id or \
            line.product_id.categ_id.warehouse_id

        if wh_id:
            vals['name'] += '/' + wh_id.name
        return vals

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _prepare_order_line_procurement(self, group_id=False):
        values = super(SaleOrderLine, self).\
            _prepare_order_line_procurement(group_id=group_id)
        wh_id = self.product_id.product_tmpl_id.warehouse_id or \
            self.product_id.categ_id.warehouse_id
        if wh_id:
            values['warehouse_id'] = wh_id.id
        return values


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def _create_picking(self):
        StockPicking = self.env['stock.picking']
        for order in self:
            if any([ptype in ['product', 'consu'] for ptype in order.order_line.mapped('product_id.type')]):
                pickings = order.picking_ids.filtered(lambda x: x.state not in ('done','cancel'))
                if not pickings:
                    # we need to create a picking per prod.wh or per po wh
                    for line in order.order_line:
                        # get wh_id of prod or categ_id or PO
                        wh_id = line.product_id.product_tmpl_id.warehouse_id or \
                            line.product_id.categ_id.warehouse_id or \
                            order.picking_type_id.warehouse_id

                        picking = order.picking_ids.filtered(
                        lambda p: p.location_dest_id == wh_id.lot_stock_id)

                        if not picking:
                            res = order._prepare_picking()
                            res.update({
                            'location_dest_id': wh_id.lot_stock_id.id,
                            'picking_type_id': self.env['stock.picking.type'].search([
                                ('code','=',order.picking_type_id.code),
                                ('default_location_dest_id','=',wh_id.lot_stock_id.id)
                                ])[0].id,
                            })
                            picking = StockPicking.create(res)

                        moves = line._create_stock_moves(picking)
                        moves = moves.filtered(lambda x: x.state not in ('done', 'cancel')).action_confirm()
                        moves.action_assign()

                else:
                    picking = pickings[0]
                # moves = order.order_line._create_stock_moves(picking)
                # moves = moves.filtered(lambda x: x.state not in ('done', 'cancel')).action_confirm()
                seq = 0
                for move in sorted(moves, key=lambda move: move.date_expected):
                    seq += 5
                    move.sequence = seq
                moves.force_assign()
                picking.message_post_with_view('mail.message_origin_link',
                    values={'self': picking, 'origin': order},
                    subtype_id=self.env.ref('mail.mt_note').id)
        return True


    # @api.multi
    # def button_confirm(self):
    #     super(PurchaseOrder, self).button_confirm()
    #     stk_pcks = self.env['stock.picking'].search([
    #         # ('purchase_id','=',False),
    #         # ('sale_id','=',False),
    #         ('move_lines','=',False),
    #         ('group_id','=',False),
    #         ('origin','=',self.name),
    #     ])
    #
    #     for order in self:
    #         for pick in stk_pcks:
    #             pick.unlink()
    #
    #     return True



# class PurchaseOrderLine(models.Model):
#     _inherit = 'purchase.order.line'
#
#     @api.multi
#     def _prepare_stock_moves(self, picking):
#         res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
#         wh_id = self.product_id.product_tmpl_id.warehouse_id or \
#             self.product_id.product_tmpl_id.categ_id.warehouse_id
#         if wh_id and picking.location_dest_id != wh_id.lot_stock_id:
#             pick_id = picking.copy()
#             pick_id.update({
#             'location_dest_id': wh_id.lot_stock_id.id,
#             'picking_type_id': self.env['stock.picking.type'].search([
#                 ('code','=','incoming'),
#                 ('default_location_dest_id','=',wh_id.lot_stock_id.id)
#                 ])[0].id,
#             # 'purchase_id': picking.purchase_id.id,
#             })
#             for move in res:
#                 move.update({
#                 'picking_id': pick_id.id,
#                 'warehouse_id': wh_id.id,
#                 'location_dest_id': wh_id.lot_stock_id.id,
#                 'name': move.get('name') + '/' + wh_id.name,
#                 })
#         return res
