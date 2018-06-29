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
from odoo import tools
import logging
_logger = logging.getLogger(__name__)


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    @api.multi
    def hide_mp_menus_to_user(self, menu_data):
        """ Return the ids of the menu items hide to the user. """
        menu_ids = super(IrUiMenu, self).hide_mp_menus_to_user(menu_data)
        if self.env.user.has_group(
                'odoo_marketplace.marketplace_seller_group'):
            mp_inv_menu_id = self.env.ref(
                'odoo_marketplace.wk_seller_dashboard_menu4_sub_menu2',
                False)
            if mp_inv_menu_id:
                menu_ids.extend((mp_inv_menu_id.id, ))
        if self.env.user.has_group(
                'marketplace_customization.group_marketplace_seller_staff'):
            staff_menu_id = self.env.ref(
                'marketplace_customization.seller_staff_menu', False)
            if staff_menu_id:
                menu_ids.extend((staff_menu_id.id, ))
            # seller_profile_menu_id = self.env.ref(
            #     'odoo_marketplace.wk_seller_dashboard_menu1_sub_menu1', False)
            # if seller_profile_menu_id:
            #     menu_ids.extend((seller_profile_menu_id.id, ))
        return menu_ids
