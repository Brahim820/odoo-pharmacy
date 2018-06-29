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
from odoo.tools.translate import _

import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _default_location(self):
        """ Set default location """
        user_obj = self.env["res.users"].browse(self._uid)
        if user_obj:
            company_id = user_obj.company_id.id
            location_ids = self.env["stock.location"].sudo().search(
                [("company_id", '=', company_id), ("name", "=", "Stock"), ('usage', '=', 'internal')])
            return location_ids[0] if location_ids else self.env["stock.location"]
        return self.env["stock.location"].sudo().search([('usage', '=', 'internal')])[0]

    @api.multi
    def set_warehouse_data(self):
        self.ensure_one()
        self.location_id = self._default_location().id
