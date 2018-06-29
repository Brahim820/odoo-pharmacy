
from odoo import models, fields, api, _
import datetime
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    move_raw_ids = fields.One2many(
        'stock.move', 'raw_material_production_id', 'Raw Materials', oldname='move_lines',
        copy=False, domain=[('scrapped', '=', False)])

    def clean_moves(self):
        for production in self:
            for move in production.move_raw_ids:
                move.sudo().do_unreserve()
                move.sudo().write({'state':'draft'})
                move.sudo().action_cancel()
                move.sudo().unlink()
            for move in production.move_finished_ids:
                move.sudo().action_cancel()
                move.sudo().unlink()

    def f_update_order(self):
        for production in self:
            if production.state in ['planned','progress','done']:
                raise UserError(_('You can not update in progress or done orders.'))
                # continue
            # we need to create a temp bom from current config and process it, then delete it
            bom = self.env['mrp.bom']
            bom_line = self.env['mrp.bom.line']
            bom_id = bom.sudo().create({
                'active': False, #this is
                'product_tmpl_id': production.product_tmpl_id.id,
                'product_qty': production.product_qty,
                'product_uom_id': production.product_uom_id.id,
                'routing_id': production.routing_id.id,
                'code': production.bom_id.code,
                })
            for line in production.move_raw_ids:
                bom_line.sudo().create({
                    'product_id': line.product_id.id,
                    'product_qty': line.product_uom_qty,
                    'product_uom_id': line.product_uom.id,
                    'bom_id': bom_id.id,
                    })
            # trigger write on BoM to update product cost if dvit_product_cost_bom_auto is installed
            bom_id.code = ' Auto generated for ' + str(production.name) +' '+ str(fields.Datetime.now())
            #########
            for move in production.move_raw_ids:
                move.sudo().do_unreserve()
                move.sudo().write({'state':'draft'})
                move.sudo().action_cancel()
                move.sudo().unlink()
            for move in production.move_finished_ids:
                move.sudo().action_cancel()
                move.sudo().unlink()
            old_bom = production.bom_id
            production.bom_id = bom_id

            # delete old bom_id if auto generated
            if old_bom.code and 'Auto generated' in old_bom.code and str(production.name) in old_bom.code and not old_bom.active:
                old_bom.sudo().unlink()

            # then recreate the moves again
            production.sudo()._generate_moves()
