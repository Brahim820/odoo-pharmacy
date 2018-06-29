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
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create_global_product_for_seller(self):
        # create global products for sellers
        all_global_prod_obj = self.env['product.template'].sudo().search(
            [('is_global_product', '=', True), ('website_published', '=', True)])
        for seller_obj in self.search([('seller', '=', True), ('state', '=', 'approved')]):
            for product_obj in all_global_prod_obj:
                if not self.env['product.template'].sudo().search([
                            ('global_product_tmpl_id', '=', product_obj.id),
                            ('marketplace_seller_id', '=', seller_obj.id)
                ]) and product_obj.marketplace_seller_id != seller_obj:
                    vals = {
                        'global_product_tmpl_id': product_obj.id,
                        'name': product_obj.name,
                        'image': product_obj.image,
                        'description_sale': product_obj.description_sale,
                        'list_price': product_obj.list_price,
                        'marketplace_seller_id': seller_obj.id,
                        'status': 'approved',
                        'website_published': True,
                        'warranty': product_obj.warranty,
                        'weight': product_obj.weight,
                        'volume': product_obj.volume,
                    }
                    try:
                        self.env['product.template'].create(vals)
                    except Exception as e:
                        _logger.info(
                            "----------Exception while assiging global product to seller ---%r---------------", e)
            # update the status of seller global product when global product for this seller is created
            try:
                seller_obj.global_prod_status = True
            except Exception as e:
                _logger.info(
                    "----------Exception in upd_status ---%r---------------", e)
