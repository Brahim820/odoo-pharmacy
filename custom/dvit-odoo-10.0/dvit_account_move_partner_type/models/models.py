# -*- coding: utf-8 -*-

from odoo import models, fields, api


class accountMove(models.Model):
    _inherit = 'account.move'

    partner_type = fields.Selection(string="Partner Type",
                                    selection=[('customer', 'customer'),
                                               ('supplier', 'supplier'),
                                               ('all', 'all') ])

class accountMove(models.Model):
    _inherit = 'account.move.line'

    partner_type = fields.Selection(string="Partner Type",readonly=True,
                                    selection=[('customer', 'customer'),
                                               ('supplier', 'supplier'),
                                               ('all', 'all')])

    @api.onchange('partner_type')
    def _onchange_partner_id(self):
        res = {}
        if self.partner_type=='customer':
            res['domain'] = {'partner_id': [('customer', '=', True)]}
        if self.partner_type=='supplier':
            res['domain'] = {'partner_id': [('supplier', '=', True)]}
        return res
