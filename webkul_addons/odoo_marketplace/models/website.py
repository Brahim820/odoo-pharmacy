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


from odoo import api, fields, models


class Website(models.Model):
    _inherit = 'website'


    @api.model
    def get_mp_config_settings_values(self):
		res = self.env["marketplace.config.settings"].sudo().get_default_values()
		res2 = self.env["marketplace.config.settings"].sudo().mp_config_translatable()
		result = res.copy()
		result.update(res2)
		return result

    @api.model
    def get_mp_ajax_seller_countries(self):
		countries = self.env['res.country'].sudo().search([])
		return  countries
