# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import http, tools, _
from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale as Base



class WebsiteSale(Base):
    @route()
    def cart(self, **post):
        result = super(WebsiteSale, self).cart(**post)
        result.qcontext["periods"] = request.env['delivery.period'].search([])
        return result

    @http.route(['/shop/delivery_date'], type='json',
    auth="public", methods=['POST'], website=True)
    def delivery_date(self, **post):
        print '>>>>>>>>> post:', post
        if post.get('delivery_date') and post.get('delivery_period'):
            order = request.website.sale_get_order().sudo()
            redirection = self.checkout_redirection(order)
            if redirection:
                return redirection

            if order and order.id:
                values = {}
                if post.get('delivery_period'):
                    values.update(
                        {'delivery_period': post.get('delivery_period')})


                p_date = datetime.strptime(post.get('delivery_date'), '%m/%d/%Y')
                post_date = datetime.strftime(p_date, '%m/%d/%Y')#str(user_date_format))
                today_date = datetime.strftime(datetime.today(), '%m/%d/%Y')#user_date_format)

                values.update({
                    'delivery_date': post.get('delivery_date')
                    })

                order.write(values)
        return True


    @route()
    def address(self, **kw):
        country = request.website.company_id.country_id
        kw['country_id'] = country.id
        kw['country'] = country.id
        kw['state_id'] = request.env['res.country.state'].sudo().search([('code','=','GZ'),('country_id','=',country.id)]).id
        kw['city'] = 'Giza'
        kw['street'] = 'NA'

        result = super(WebsiteSale, self).address(**kw)


        result.qcontext["cities"] = request.env['res.country.city'].search([])
        result.qcontext["zones"] = []#request.env['res.country.city.zone'].search([])
        result.qcontext["builds"] = [] #request.env['res.zone.building'].search([])
        result.qcontext["city"] = (result.qcontext.get('city_id') != '') and request.env['res.country.city'].sudo().browse(result.qcontext.get('city_id')).name

        return result

    def _checkout_form_save(self, mode, checkout, all_values):
        Partner = request.env['res.partner']
        for val in all_values:
            if hasattr(Partner,val):
                checkout[val] = all_values[val]

        partner_id = super(WebsiteSale, self)._checkout_form_save(mode, checkout, all_values)
        return partner_id

    @http.route(['/shop/zone_info/<model("res.country.city.zone"):zone>'], type='json',
    auth="public", methods=['POST'], website=True)
    def zone_info(self, zone, **kw):
        return dict(
            builds=[(b.id, b.name) for b in zone.building_ids],
        )

    @http.route(['/shop/city_info/<model("res.country.city"):city>'], type='json',
    auth="public", methods=['POST'], website=True)
    def city_info(self, city, **kw):
        return dict(
            zones=[(z.id, z.name) for z in city.zone_ids],
        )

    @http.route(['/shop/state_info/<model("res.country.state"):state>'], type='json',
    auth="public", methods=['POST'], website=True)
    def state_info(self, city, **kw):
        return dict(
            cities=[(cc.id, cc.name) for cc in state.city_ids],
        )
