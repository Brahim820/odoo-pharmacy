from odoo.addons.website_sale.controllers.main import WebsiteSale

from odoo.http import request
from odoo import SUPERUSER_ID
from odoo import http

class WebsiteSale(WebsiteSale):
    
    
    @http.route(['/shop/get_products_content'], type='http', auth='public', website=True)
    def get_products_content(self, **post):
        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])
        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)
        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)  
        if post.get('tab_id'):
            tab_data = request.env['multitab.configure'].browse(int(post.get('tab_id')))
            return request.render("theme_stoneware.product_slider_content", {'product_collection':tab_data,'compute_currency': compute_currency})
        return ''    
    
    @http.route(['/shop/get_product_brand_slider'], type='http', auth='public', website=True)
    def get_product_brand_slider(self, **post):
        value = {'header': False,'brands':False}
        if post.get('label'):
            value['header'] = post.get('label')
        if post.get('brand-count'):
            brand_ids=request.env['product.brand'].search([('visible_slider','=',True)])
            if brand_ids:
                value.update({'brands':brand_ids})               
        return request.render("theme_stoneware.brand_slider_content", value)  


    @http.route(['/shop/get_multi_tab_content'], type='http', auth='public', website=True)
    def get_multi_tab_content(self, **post):
        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])
        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)
        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)                
        value = {'obj': False,'compute_currency': compute_currency}
        if post.get('label'):
            value['header'] = post.get('label')
        if post.get('collection_id'):
            collection_data=request.env['collection.configure'].browse(int(post.get('collection_id')))
            value.update({'obj':collection_data})
            return request.render("theme_stoneware.s_collection_configure", value)

        return ""

    @http.route(['/shop/multi_tab_product_snippet'], type='http', auth='public', website=True)
    def multi_tab_product_snippet(self, **post):
        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])
        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)
        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency) 
        value = {'product_obj': False,'compute_currency': compute_currency}
        if post.get('label'):
            value['header'] = post.get('label')
        if post.get('collection_id'):
            collection_data=request.env['collection.configure'].browse(int(post.get('collection_id')))
            value.update({'product_obj':collection_data})
                
        return request.render("theme_stoneware.product_tab_content", value)

      
