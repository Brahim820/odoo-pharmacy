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

import logging

from odoo import api, fields, models, tools

from odoo.http import request

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = 'website'

    # @api.multi
    # def apply_sale_offer(self, sale_offer_obj, sale_order=None):
    #     if sale_offer_obj and sale_order:
    #         for obj in sale_offer_obj.offer_discount_rule_ids:
    #     if not sale_order and sale_offer_obj
    #         sale_order = request.website.sale_get_order() 
    #     else:
