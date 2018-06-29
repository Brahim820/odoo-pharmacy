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

import models
import controllers

from odoo import api, SUPERUSER_ID

def pre_init_check(cr):
    from odoo.service import common
    from odoo.exceptions import Warning
    version_info = common.exp_version()
    server_serie = version_info.get('server_serie')
    if server_serie != '10.0':
        raise Warning('Module support Odoo series 10.0 found {}.'.format(server_serie))
    return True

def post_init_check(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    import logging
    from odoo.exceptions import Warning
    _logger = logging.getLogger(__name__)
    mp_order_menu_obj = env['ir.model.data'].get_object_reference('odoo_marketplace', 'wk_seller_dashboard_menu3_sub_menu2')[1]
    if mp_order_menu_obj:
        mp_order_menu_obj = env['ir.ui.menu'].browse(mp_order_menu_obj)
        mp_order_menu_obj.sudo().write({'name' : 'Order Lines'})
    return True
