# -*- coding: utf-8 -*-
##########################################################################
#
#	Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################

from odoo import api, models, fields


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'

    group_sale_reorder = fields.Boolean("Enable website reorder features",
        implied_group='sale_reorder.group_sale_reorder',
        help="""Allows to user to reorder the existing palced orders """)


class WebsiteReorderSetting(models.Model):
    _name = "website.reorder.setting"
    
    @api.model
    def _wk_reorder_settings(self):
        configModel = self.env['website.config.settings']
        reorderSettingObj = configModel.create({'group_sale_reorder':True})
        reorderSettingObj.execute()
        return True
