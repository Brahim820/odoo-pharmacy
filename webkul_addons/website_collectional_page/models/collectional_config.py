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

class WebsiteCollectionalConfig(models.TransientModel):
    _name = 'website.collectional.page.config'
    _inherit="res.config.settings"

    collectional_page_label = fields.Char(string="Collection Page Link Label", default="Collection", required=True)
    show_collectional_menu = fields.Selection([('header','Show in header'),('footer','Show in footer'),('both', 'Show in header and footer')],
        string="Show Collection Menu", default="header", required=True)

    @api.multi
    def set_collectional_config_settings(self):
        self.env['ir.values'].sudo().set_default('website.collectional.page.config', 'collectional_page_label', self.collectional_page_label)
        self.env['ir.values'].sudo().set_default('website.collectional.page.config', 'show_collectional_menu', self.show_collectional_menu)
        return True

    @api.model
    def get_collectional_config_settings(self):
        collectional_page_label = self.env['ir.values'].sudo().get_default('website.collectional.page.config', 'collectional_page_label')
        show_collectional_menu = self.env['ir.values'].sudo().get_default('website.collectional.page.config', 'show_collectional_menu')
        return {'collectional_page_label':collectional_page_label,
            'show_collectional_menu' : show_collectional_menu,
        }
