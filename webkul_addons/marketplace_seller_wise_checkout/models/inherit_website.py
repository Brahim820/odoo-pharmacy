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
from odoo import api, fields, models
from odoo.http import request
_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = 'website'

    def _get_seller_sale_order_ids(self, seller_so_ids=[]):
        if seller_so_ids:
            seller_so_obj = request.env['sale.order'].sudo().browse(seller_so_ids).exists()
            seller_so_ids = seller_so_obj.ids
            return seller_so_ids
        return None

    @api.multi
    def sale_get_order(self, force_create=False, code=None, update_pricelist=False, force_pricelist=False, seller_id=False):
        request.session['seller_so_ids'] = self._get_seller_sale_order_ids(request.session.get('seller_so_ids'))
        if seller_id:

            # to change pricelist for public user
            update_pricelist = False
            pricelist_id = request.session.get('website_sale_current_pl') or self.get_current_pricelist().id

            if self.env['product.pricelist'].browse(force_pricelist).exists():
                pricelist_id = force_pricelist
                request.session['website_sale_current_pl'] = pricelist_id
                update_pricelist = True

            partner = self.env.user.partner_id
            seller_so_id = False

            # check if sale order of this seller exist in session
            seller_so_ids = request.session.get('seller_so_ids')
            if seller_so_ids:
                seller_so_obj = request.env['sale.order'].sudo().browse(seller_so_ids).exists()
                seller_so_id = seller_so_obj.filtered(lambda o: o.marketplace_seller_id.id == seller_id)

            # if seller sale order id found in session return order
            if seller_so_id:
                sale_order = request.env['sale.order'].sudo().browse(seller_so_id.id)

                # code for promo code to update pricelist

                if code and code != sale_order.pricelist_id.code:
                    code_pricelist = self.env['product.pricelist'].sudo().search([('code', '=', code)], limit=1)
                    if code_pricelist:
                        pricelist_id = code_pricelist.id
                        update_pricelist = True
                elif code is not None and sale_order.pricelist_id.code:
                    # code is not None when user removes code and click on "Apply"
                    pricelist_id = partner.property_product_pricelist.id
                    update_pricelist = True

                # update the pricelist
                if update_pricelist:
                    request.session['website_sale_current_pl'] = pricelist_id
                    values = {'pricelist_id': pricelist_id}
                    sale_order.write(values)
                    for line in sale_order.order_line:
                        if line.exists():
                            sale_order._cart_update(product_id=line.product_id.id, line_id=line.id, add_qty=0)

                return request.env['sale.order'].sudo().browse(seller_so_id.id)

            # if seller sale order id not found in session then search in all so ids of partner and update in session
            else:
                if partner.sale_order_ids and request.website.partner_id.id != partner.id:
                    seller_so_id = partner.sale_order_ids.filtered(lambda o: o.state == 'draft' and o.marketplace_seller_id.id == seller_id)
                    if seller_so_id:
                        if seller_so_ids:
                            seller_so_ids.append(seller_so_id.id)
                        else:
                            seller_so_ids = [seller_so_id.id]
                        request.session['seller_so_ids'] = seller_so_ids

                        sale_order = request.env['sale.order'].sudo().browse(seller_so_id.id)

                        # code for promo code to update pricelist
                        if code and code != sale_order.pricelist_id.code:
                            code_pricelist = self.env['product.pricelist'].sudo().search([('code', '=', code)], limit=1)
                            if code_pricelist:
                                pricelist_id = code_pricelist.id
                                update_pricelist = True
                        elif code is not None and sale_order.pricelist_id.code:
                            # code is not None when user removes code and click on "Apply"
                            pricelist_id = partner.property_product_pricelist.id
                            update_pricelist = True

                        # update the pricelist
                        if update_pricelist:
                            request.session['website_sale_current_pl'] = pricelist_id
                            values = {'pricelist_id': pricelist_id}
                            sale_order.write(values)
                            for line in sale_order.order_line:
                                if line.exists():
                                    sale_order._cart_update(product_id=line.product_id.id, line_id=line.id, add_qty=0)

                        return request.env['sale.order'].sudo().browse(seller_so_id.id)

            # if no sale order of seller found in session and in previous order of partner then create new so for this seller and update in session
            session_sale_order_id = request.session.get('sale_order_id')
            last_order = partner.last_website_so_id

            # make session and last sale order id false so that a new order can be created for this seller
            request.session['sale_order_id'] = None
            partner.last_website_so_id = False
            seller_so_id = super(Website, self).sale_get_order(force_create, code, update_pricelist, force_pricelist)

            if seller_so_id:
                seller_so_id.marketplace_seller_id = seller_id   # update so with the seller
                if seller_so_ids:
                    seller_so_ids.append(seller_so_id.id)
                else:
                    seller_so_ids = [seller_so_id.id]
                request.session['seller_so_ids'] = seller_so_ids
                # update the last website so id and so id session for admin cart
                request.session['sale_order_id'] = session_sale_order_id
                partner.last_website_so_id = last_order
                return request.env['sale.order'].sudo().browse(seller_so_id.id)

        so = super(Website, self).sale_get_order(force_create, code, update_pricelist, force_pricelist)
        if so and not so.marketplace_seller_id:
            request.session['admin_so'] = request.session['sale_order_id']
        return so


    def sale_reset(self, order_id=None):
        if order_id:
            seller_so_ids = request.session.get('seller_so_ids') or []
            seller_so_ids.remove(order_id) if order_id in seller_so_ids else seller_so_ids
            if seller_so_ids:
                request.session.update({
                    'seller_so_ids': seller_so_ids,
                    'sale_transaction_id': False,
                    'website_sale_current_pl': False,
                })
                return
        else:
            order = request.env['sale.order'].sudo().browse(request.session.get('sale_order_id') or False)
            if order.marketplace_seller_id:
                seller_so_ids = request.session.get('seller_so_ids') or []
                seller_so_ids.remove(order.id) if order.id in seller_so_ids else seller_so_ids
                request.session.update({'seller_so_ids' : seller_so_ids,})
            else:
                request.session.update({'admin_so':None,})
            res = super(Website, self).sale_reset()
            return res
