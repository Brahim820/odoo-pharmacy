# -*- coding: utf-8 -*-
#################################################################################
#Add Comments About Your Order
#    Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
from odoo import http, SUPERUSER_ID, _
from odoo.http import request
from odoo.addons.website.controllers.main import Website
import logging
_logger = logging.getLogger(__name__)
class WebsiteSale(Website):
    @http.route(['/page/website.sitemap', '/page/sitemap'], type='http', auth="public", website=True)
    def website_sitemap(self, **post):
        FIELDS =[
            'name',
            'parent_id',
            'parent_left',
            'parent_right',
            'url',
            'child_id'
        ]
        domain=[
            ('parent_id','=',None),
            ('website_id','=',request.website.id),
        ]
        menu_ids = request.env['website.menu'].search(domain)
        values = {
            'menu_ids':menu_ids,
            'url_root': request.httprequest.url_root[:-1],
            'host':request.httprequest.host,
        }
        return request.render("website_seo_pro.sitemap", values)