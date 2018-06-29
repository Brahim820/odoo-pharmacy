# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
from odoo import api, fields, models, _
from odoo import tools
import logging
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
_logger = logging.getLogger(__name__)

class WebsiteDailyDealsConfig(models.TransientModel):
	_inherit = 'res.config.settings'
	_name = 'website.daily.deals.conf'

	@api.multi
	def _get_deals_pricelist(self):
		xid = self.env['ir.model.data'].search([('module', '=', 'website_daily_deals'), ('name', '=', 'wk_deals_pricelist')])
		pricelist = 0
		if xid:
			pricelist = xid.res_id
		return pricelist

	show_page_header = fields.Boolean('Show Page Header', help="show Page header in website.")
	page_header_text = fields.Char('Page Header Text', default="DONT MISS A DEAL THIS TIME", help="Text for the header of the page to be displayed in website")
	item_to_show = fields.Selection([('banner_only','Banner Only'),('products_only','Products Only'), ('both','Both')],'What to Display on Website', default='both', help="choose what you want to display in website.")
	display_products_as = fields.Selection([('grid','Grid'),('slider','Slider')],'How to display Products on Website', default='grid', help="choose how to display the produts in website.")
	wk_pricelist = fields.Many2one('product.pricelist','Pricelist', required=True , help="Choose a pricelist, all the deal products will be added in that pricelist.(A default Deal pricelist will be created.)")
	show_message_before_expiry = fields.Boolean('Show Message before Expiry',help="Do you want to show a message before the expiry date of the deal, if yes then set this true.")
	message_before_expiry = fields.Char('Message before Expiry', help="The message you want to show in the website when deal is about to expire.")
	interval_before = fields.Integer('Time interval before to display message' , help="How much time before the expiry date you want to display the message.")
	unit_of_time = fields.Selection([('minutes','Minutes'),('hours','Hours'),('days','Days'),('weeks','Weeks'),('months','Months')],'Time Unit', default='hours')
	show_message_after_expiry = fields.Boolean('Show Message After Expiry', help="Do you want to show the message after the expiry date of the deal.")
	message_after_expiry = fields.Char('Message After Expiry', help="The message you want to show in the website when deal is expired.")
	
	@api.multi
	def set_default_website_daily_deals_configuration(self):
		ir_values = self.env['ir.values']
		show_page_header = ir_values.sudo().set_default('website.daily.deals.conf', 'show_page_header',
			self.show_page_header)
		page_header_text = ir_values.sudo().set_default('website.daily.deals.conf', 'page_header_text',
			self.page_header_text)
		item_to_show = ir_values.sudo().set_default('website.daily.deals.conf', 'item_to_show',
			self.item_to_show or 'both')
		display_products_as = ir_values.sudo().set_default('website.daily.deals.conf', 'display_products_as',
			self.display_products_as or 'both')
		wk_pricelist = ir_values.sudo().set_default('website.daily.deals.conf', 'wk_pricelist',
			self.wk_pricelist.id)
		show_message_before_expiry = ir_values.sudo().set_default('website.daily.deals.conf', 'show_message_before_expiry',
			self.show_message_before_expiry)
		message_before_expiry = ir_values.sudo().set_default('website.daily.deals.conf', 'message_before_expiry',
			self.message_before_expiry)
		interval_before = ir_values.sudo().set_default('website.daily.deals.conf', 'interval_before',
			self.interval_before)
		unit_of_time = ir_values.sudo().set_default('website.daily.deals.conf', 'unit_of_time',
			self.unit_of_time)
		show_message_after_expiry = ir_values.sudo().set_default('website.daily.deals.conf', 'show_message_after_expiry',
			self.show_message_after_expiry)
		message_after_expiry = ir_values.sudo().set_default('website.daily.deals.conf', 'message_after_expiry',
			self.message_after_expiry)	
		return True

	@api.multi
	def get_default_website_daily_deals_configuration(self, fields):
		ir_values = self.env['ir.values']
		show_page_header = ir_values.sudo().get_default('website.daily.deals.conf', 'show_page_header')
		page_header_text = ir_values.sudo().get_default('website.daily.deals.conf', 'page_header_text')
		item_to_show = ir_values.sudo().get_default('website.daily.deals.conf', 'item_to_show')
		display_products_as = ir_values.sudo().get_default('website.daily.deals.conf', 'display_products_as')
		wk_pricelist = ir_values.sudo().get_default('website.daily.deals.conf', 'wk_pricelist')
		show_message_before_expiry = ir_values.sudo().get_default('website.daily.deals.conf', 'show_message_before_expiry')
		message_before_expiry = ir_values.sudo().get_default('website.daily.deals.conf', 'message_before_expiry')
		interval_before = ir_values.sudo().get_default('website.daily.deals.conf', 'interval_before')
		unit_of_time = ir_values.sudo().get_default('website.daily.deals.conf', 'unit_of_time')
		show_message_after_expiry = ir_values.sudo().get_default('website.daily.deals.conf', 'show_message_after_expiry')
		message_after_expiry = ir_values.sudo().get_default('website.daily.deals.conf', 'message_after_expiry')
		wk_pricelist = wk_pricelist or self._get_deals_pricelist()
		display_products_as = display_products_as or 'grid'
		item_to_show = item_to_show or 'both'
		return{
			'show_page_header':show_page_header,
			'page_header_text':page_header_text,
			'item_to_show':item_to_show,
			'display_products_as':display_products_as,
			'message_before_expiry':message_before_expiry,
			'show_message_before_expiry':show_message_before_expiry,
			'interval_before':interval_before,
			'unit_of_time':unit_of_time,
			'show_message_after_expiry':show_message_after_expiry,
			'message_after_expiry':message_after_expiry,
			'wk_pricelist':wk_pricelist,
			
		}