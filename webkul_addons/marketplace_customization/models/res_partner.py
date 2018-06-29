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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        res = super(ResPartner, self).read(fields, load)
        if self.env.user.has_group(
                'marketplace_customization.group_marketplace_seller_staff'):
            for data_dict in res:
                if data_dict.get("id", False) == self.env.user.partner_id.id:
                    if self.env.user.seller_staff_id:
                        data_dict["name"] = self.env.user.seller_staff_id.name
        return res