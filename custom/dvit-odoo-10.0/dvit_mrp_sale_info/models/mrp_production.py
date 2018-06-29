# -*- coding: utf-8 -*-
# © 2016 Antiun Ingenieria S.L. - Javier Iniesta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    sale_line_id = fields.Many2one(
        'sale.order.line', string='Sale order Line', readonly=True, store=True,
        compute='_get_sale_line')

    sale_id = fields.Many2one('sale.order', string='Sale order', readonly=True,
        store=True, related='sale_line_id.order_id')

    partner_id = fields.Many2one(related='sale_id.partner_id', readonly=True,
        string='Customer', store=True)


    @api.depends('move_finished_ids','move_finished_ids.state')
    def _get_sale_line(self):
        #TODO: this is not the best way to get sale_line_id, find better way.
            # we should write the sale_line_id on MO creation - see mrp/models/procurement.py,make_mo()
            # the proc that creates the MO don't have the sale_line_id, this is the raw mat. proc order,
            # we should find link between raw proc order and finished product proc order.
        for prd in self:
            if not prd.move_finished_ids:
                continue
            if not any(m.move_dest_id for m in prd.move_finished_ids):
                continue
            tgt_procs = prd.procurement_ids[0].group_id.procurement_ids.filtered(\
                lambda p: p.location_id.usage == 'customer' and \
                p.group_id == prd.procurement_ids[0].group_id and \
                p.product_id == prd.product_id and \
                p.name == prd.move_finished_ids[0].move_dest_id.name
                )
            
            if tgt_procs and len(tgt_procs) > 1:
                tgt_proc = tgt_procs[-1] #use the last procurement - normally older were canceled
            else:
                tgt_proc = tgt_procs
            prd.update({'sale_line_id': tgt_proc and tgt_proc.sale_line_id or False,})
