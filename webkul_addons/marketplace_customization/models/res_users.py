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
from odoo.exceptions import except_orm, Warning, RedirectWarning
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.seller_staff_id:
                result.append((record.id, record.seller_staff_id.name))
        return result if result else super(ResUsers, self).name_get()

    seller_staff_id = fields.Many2one("seller.staff", "Seller Staff")

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        res = super(ResUsers, self).read(fields, load)
        for obj in self.filtered("seller_staff_id"):
            for data_dict in res:
                if data_dict.get("id", False) == obj.id:
                    data_dict["name"] = obj.seller_staff_id.name
        return res