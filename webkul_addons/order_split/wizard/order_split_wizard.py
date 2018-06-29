# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
from odoo.tools.translate import _
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class WKSplitTransferWizard(models.TransientModel):
    _name = "wk.split.transfer.wizard"
    _inherit = ['mail.thread']
    item_ids = fields.One2many(
        'wk.stock.transfer_details_item',
        'transfer_id',
        string='Invoice Lines'
    )

    @api.model
    def default_get(self, fields):
        res = super(WKSplitTransferWizard, self).default_get(fields)
        context = self._context or {}
        active_id = context.get('active_id')
        picking_id = self.env['stock.picking'].browse(active_id)
        items = []
        for move_line in picking_id.move_lines:
            if move_line.state == 'done':
                raise ValidationError(
                    _("You can't split transfer having moves already in done state"))
            if move_line.state == 'cancel':
                continue
            if move_line.product_id:
                item = {
                    'product_id': move_line.product_id.id,
                    'quantity': move_line.product_qty,
                    'sourceloc_id': move_line.location_id.id,
                    'destinationloc_id': move_line.location_dest_id.id,
                }
                items.append(item)
        res.update(item_ids=items)
        return res

    @api.multi
    def stock_transfer_picking(self):
        context = self._context or {}
        active_id = context.get('active_id')
        picking_id = self.env['stock.picking'].browse(active_id)
        stock_move_id = picking_id.copy({'backorder_id': active_id})
        msz1 = _("Split picking of <em>%s</em> <b>created</b>.") % (str(active_id))
        stock_move_id.message_post(body=msz1)

        stock_move_id2 = picking_id.copy({'backorder_id': active_id})
        msz2 = _("Split picking of <em>%s</em> <b>created</b>.") % (str(active_id))
        stock_move_id2.message_post(body=msz2)
        picking = stock_move_id
        wizard_obj = self.item_ids
        blank = []
        item1 = 0
        for op in picking.move_lines:
            if item1 < len(wizard_obj):
                item1_id = wizard_obj[item1]
                if item1_id.product_id == op.product_id:
                    if (
                            item1_id.quantity > op.product_uom_qty
                            or item1_id.quantity < 1):
                        raise ValidationError(
                            _("This product quantity is not allowed"))
                    else:
                        op.write({
                            'product_uom_qty': item1_id.quantity,
                            # 'product_uos_qty':item1_id.quantity,
                        })
                        item1 += 1
                else:
                    blank.append(op.id)
            else:
                blank.append(op.id)

        self.env['stock.move'].browse(blank).unlink()
        move_lines_len = stock_move_id.move_lines
        if not len(move_lines_len):
            raise ValidationError(
                _("Orders with no modification is not allowed."))
        picking = stock_move_id2
        wizard_obj = self.item_ids
        item2 = 0
        blank2 = []
        for op in picking.move_lines:
            if item2 < len(wizard_obj):
                item2_id = wizard_obj[item2]
                if item2_id.product_id == op.product_id:
                    if item2_id.quantity == op.product_uom_qty:
                        blank2.append(op.id)
                    else:
                        op.write({
                            'product_uom_qty':op.product_uom_qty - item2_id.quantity,
                            # 'product_uos_qty':op.product_uom_qty - item2_id.quantity,
                            })
                    item2 += 1
                else:
                    op.write({
                        'product_uom_qty': op.product_uom_qty,
                        # 'product_uos_qty': op.product_uos_qty
                        })
            else:
                op.write({
                    'product_uom_qty': op.product_uom_qty,
                    # 'product_uos_qty': op.product_uos_qty
                })
        self.env['stock.move'].browse(blank2).unlink()
        move_lines_len = stock_move_id2.move_lines
        self.env['stock.picking'].browse(active_id).action_cancel()
        if not len(move_lines_len):
            raise ValidationError(
                _("Orders with no modification is not allowed."))
        return {
            'name': _('Split Picking'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'view_id': None,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', [active_id, stock_move_id.id, stock_move_id2.id])],
            'context': context,
        }


class WKStockTransferDetailsItem(models.TransientModel):

    _name = 'wk.stock.transfer_details_item'
    transfer_id = fields.Many2one(
        'wk.split.transfer.wizard',
        'Transfer'
    )
    product_id = fields.Many2one(
        'product.product',
        'Product',
        readonly=True
    )
    quantity = fields.Float(
        'Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        default=1.0
    )
    sourceloc_id = fields.Many2one(
        'stock.location',
        'Source Location',
        readonly=True
    )
    destinationloc_id = fields.Many2one(
        'stock.location',
        'Destination Location',
        readonly=True
    )
