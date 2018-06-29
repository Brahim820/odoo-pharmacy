# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
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


from odoo import models,fields,api,_
from odoo.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)

class MarketplaceConfigSettings(models.TransientModel):
    _inherit = 'marketplace.config.settings'

    comm_type = fields.Selection([
        # ('default','Default'),
        ('product','Product'),
        ('category','Category'),
        ('seller','Seller')],
        string= 'Commission Type',
        default = 'product',
        required = True,
    )
    category_comm = fields.Selection([('minimum','Minimum'),('maximum','Maximum')], string="Category Commission", default="minimum")
    comm_method = fields.Selection([
        ('percent','Percent(%)'),
        ('fix','Fixed'),
        ('percent_and_fix','% + Fixed'),
        ('fix_and_percent','Fixed + %')],
        string=" Commission Method",
        default='fix',
        required=True,
    )
    fix_commission = fields.Float(string= 'Fix Commission')
    # currency_id = fields.Many2one('res.currency')

    @api.one
    def set_default_values(self):
        res = super(MarketplaceConfigSettings, self).set_default_values()
        self.env['ir.values'].sudo().set_default('marketplace.config.settings', 'comm_type', self.comm_type)
        self.env['ir.values'].sudo().set_default('marketplace.config.settings', 'category_comm', self.category_comm)
        self.env['ir.values'].sudo().set_default('marketplace.config.settings', 'comm_method', self.comm_method)
        self.env['ir.values'].sudo().set_default('marketplace.config.settings', 'fix_commission', self.fix_commission)
        # self.env['ir.values'].sudo().set_default('marketplace.config.settings', 'currency_id', self.currency_id.id)
        return res

    @api.model
    def get_default_values(self, fields=None):
        res = super(MarketplaceConfigSettings, self).get_default_values()
        comm_type = self.env['ir.values'].sudo().get_default('marketplace.config.settings', 'comm_type')
        category_comm = self.env['ir.values'].sudo().get_default('marketplace.config.settings', 'category_comm')
        comm_method = self.env['ir.values'].sudo().get_default('marketplace.config.settings', 'comm_method')
        fix_commission = self.env['ir.values'].sudo().get_default('marketplace.config.settings', 'fix_commission')
        # currency_id = self.env['ir.values'].sudo().get_default('marketplace.config.settings', 'currency_id') or self.set_default_currency().id
        res.update(
            {
                'comm_type'     :   comm_type,
                'category_comm' :   category_comm,
                'comm_method'   :   comm_method,
                'fix_commission'    :   fix_commission,
                # 'currency_id'       :   currency_id,
            }
        )
        return res

    @api.multi
    def execute(self):
        res = super(MarketplaceConfigSettings, self).execute()
        for rec in self:
            if rec.fix_commission < 0:
                raise Warning(_("Fix Commission should be greater than 0."))
            all_seller_objs = rec.env["res.partner"].search(
                [("seller", "=", True), ("state", "=", "approved")])
            for seller_obj in all_seller_objs:
                if not seller_obj.set_seller_wise_settings:
                    vals = {
                        "comm_method": rec.comm_method,
                        "fix_commission": rec.fix_commission,
                        # "mp_config_currency_id":rec.currency_id,
                    }
                    seller_obj.write(vals)
        return res

    # @api.model
    # def set_default_currency(self):
    #     user_obj = self.env["res.users"].browse(self._uid)
    #     if user_obj:
    #         currency_id = user_obj.company_id.currency_id.id
    #         return self.env["res.currency"].search([('id', '=', currency_id)])[0]
