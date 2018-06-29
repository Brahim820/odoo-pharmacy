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


from odoo import models, fields, api, _
from odoo.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    comm_method = fields.Selection([
        ('percent','Percent(%)'),
        ('fix','Fixed'),
        ('percent_and_fix','% + Fixed'),
        ('fix_and_percent','Fixed + %')],
        string="Commission Method",
        default = lambda self: self.env['ir.values'].get_default('marketplace.config.settings', 'comm_method'),
        read=['odoo_marketplace.marketplace_draft_seller_group'], write=['odoo_marketplace.marketplace_officer_group'],
        copy=False,
    )
    fix_commission = fields.Float(string= 'Fixed Commission',
        default = lambda self: self.env['ir.values'].get_default('marketplace.config.settings', 'fix_commission'),
        read=['odoo_marketplace.marketplace_draft_seller_group'], write=['odoo_marketplace.marketplace_officer_group'],
        copy=False
    )

    @api.onchange('fix_commission')
    def check_fix_commission(self):
        if self.fix_commission < 0.0:
            raise Warning(_('Fix Commission should be greater than zero.'))

    @api.onchange("set_seller_wise_settings")
    def on_change_seller_wise_settings(self):
        if not self.set_seller_wise_settings:
            res = super(ResPartner, self).on_change_seller_wise_settings()
            vals={}
            vals["comm_method"] = self.env['ir.values'].get_default(
                'marketplace.config.settings', 'comm_method')
            vals["fix_commission"] = self.env['ir.values'].get_default(
                'marketplace.config.settings', 'fix_commission')
            config_setting_obj = self.env[
                'marketplace.config.settings'].sudo().get_default_values()
            self.comm_method = config_setting_obj[
                "comm_method"] if config_setting_obj.has_key("comm_method") else False
            self.fix_commission = config_setting_obj[
                "fix_commission"] if config_setting_obj.has_key("fix_commission") else False
            self.write(vals)
            return res

    @api.multi
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        for rec in self:
            if vals.get("fix_commission") and vals.get("fix_commission", "") < 0.0:
                raise Warning(_("Fix Commission should be greater than 0."))
        return res

    @api.onchange("seller")
    def on_change_seller(self):
        res = super(ResPartner, self).on_change_seller()
        config_setting_obj = self.env[
            'marketplace.config.settings'].sudo().get_default_values()
        self.comm_method = config_setting_obj[
            "comm_method"] if config_setting_obj.has_key("comm_method") else False
        self.fix_commission = config_setting_obj[
            "fix_commission"] if config_setting_obj.has_key("fix_commission") else False
        return res
