import werkzeug
from odoo import SUPERUSER_ID
from odoo import http
from odoo.http import request
from odoo.tools.translate import _

import logging
logger = logging.getLogger(__name__)

def get_pricelist():
	return request.website.get_current_pricelist()

class WebsiteDailyDeals(http.Controller):
	def get_pricelist(self):
		return get_pricelist()

	@http.route(['/daily/deals'], type='http', auth="public", website=True)
	def daily_deals(self, **post):
		values = {}
		context = request.context or {}
		cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
		if not context.get('pricelist'):
			pricelist = self.get_pricelist()
			logger.info('----------------------%r',pricelist)
			# context['pricelist'] = int(pricelist)
		else:
			pricelist = request.env['product.pricelist'].sudo().with_context(context).browse(context['pricelist'])
		from_currency = request.env['res.users'].sudo().with_context(context).browse(request.uid).company_id.currency_id
		to_currency = pricelist.currency_id
		compute_currency = lambda price: request.env['res.currency'].sudo().with_context(context)._compute(from_currency, to_currency, price)
		deals = []
		ids = request.env['website.deals'].sudo().search([])
		for deal in request.env['website.deals'].sudo().get_daily_deals():
			deals.append(deal)
		values={
			'daily_deals': deals,
			'page_header':request.env['website.deals'].sudo()._get_page_header(),
			'pricelist': pricelist,
			'compute_currency': compute_currency,
		}
		return http.request.render("website_daily_deals.daily_deals", values)

	@http.route(['/deal/<model("website.deals"):deal>'], type='http', auth="public", website=True)
	def individual_deal(self, deal=False ,**post):
		context = request.context or {}
		if not context.get('pricelist'):
			pricelist = self.get_pricelist()
			# context['pricelist'] = int(pricelist)
		else:
			pricelist = request.env['product.pricelist'].sudo().with_context(context).browse(context['pricelist'])
		from_currency = request.env['res.users'].sudo().with_context(context).browse(request.uid).company_id.currency_id
		to_currency = pricelist.currency_id
		compute_currency = lambda price: request.env['res.currency'].sudo().with_context(context)._compute(from_currency, to_currency, price)
		deal = request.env['website.deals'].sudo().with_context(context).browse(deal.id)
		values={
			'pricelist': pricelist,
			'compute_currency': compute_currency,
			'individual_deal':deal
		}
		return http.request.render("website_daily_deals.individual_deal", values)
	@http.route(['/deals/change_size'], type='json', auth="public")
	def deals_change_size(self, id, x, y):
		offer_obj = request.env['product.pricelist.item'].sudo().browse(id)
		size = offer_obj.sudo().write({'website_size_x': x, 'website_size_y': y})
		return  size
	
	@http.route(['/deal/change_sequence'], type='json', auth="public")
	def change_sequence(self, id, sequence):
		context = request.context
		offer_obj = request.env['product.pricelist.item'].browse(id)
		if sequence == "top":
			offer_obj.sudo().with_context(context).set_sequence_top()
		elif sequence == "bottom":
			offer_obj.sudo().with_context(context).set_sequence_bottom()
		elif sequence == "up":
			offer_obj.sudo().with_context(context).set_sequence_up()
		elif sequence == "down":
			offer_obj.sudo().with_context(context).set_sequence_down()