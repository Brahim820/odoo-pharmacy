# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
from odoo import api, fields, models, tools, _
from odoo.http import request


class ResPartner(models.Model):
    _inherit = 'res.partner'

    last_order_datails = fields.One2many(related = 'last_website_so_id.order_line', string = 'Order Description', readonly = "1")
