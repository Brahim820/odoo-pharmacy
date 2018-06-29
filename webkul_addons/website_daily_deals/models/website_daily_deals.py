# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
from odoo import api, fields, models, _
from odoo.osv import  osv
from odoo import tools
import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

class product_pricelist_item(models.Model):
	# _name = "product.pricelist.item"
	_inherit = "product.pricelist.item"
	_order = 'website_sequence desc'

	@api.model
	def _defaults_website_sequence(self):
		cr = self._cr
		cr.execute('SELECT MIN(website_sequence)-1 FROM product_pricelist_item')
		next_sequence = cr.fetchone()[0] or 10
		return next_sequence

	my_deals_m2o = fields.Many2one('website.deals', 'Corresponding Deal', help="My Deals")
	other_offers = fields.Char('Offer Name', help="specify the other deals ")
	actual_price = fields.Float(related ='product_tmpl_id.list_price',string='Actual Amount', store=True)
	discounted_amount = fields.Float('Discounted Amount',compute="_get_discounted_amount", store=True )
	discounted_price = fields.Float(related ='product_tmpl_id.price',string='Discounted Price', store=True)
	website_size_x = fields.Integer('Size X',default=2)
	website_size_y = fields.Integer('Size Y',default=2)
	website_sequence = fields.Integer('Sequence', default=_defaults_website_sequence, help="Determine the display order in the Website E-commerce")

	@api.depends('fixed_price','percent_price','price_surcharge','price_discount','price_round')
	def _get_discounted_amount(self):
		for record in self:
			qty_uom_id = self._context.get('uom') or record.product_tmpl_id.uom_id.id
			price_uom_id = record.product_tmpl_id.uom_id.id
			qty_in_product_uom = 1
			if qty_uom_id != record.product_tmpl_id.uom_id.id:
				try:
					qty_in_product_uom = self.env['product.uom'].browse([self._context['uom']])._compute_quantity(qty, record.product_tmpl_id.uom_id)
				except UserError:
					# Ignored - incompatible UoM in context, use default product UoM
					pass
			price_uom = self.env['product.uom'].browse([qty_uom_id])
			price = record.product_tmpl_id.list_price
			convert_to_price_uom = (lambda price:  record.product_tmpl_id.uom_id._compute_price(price, price_uom))
			if record.compute_price == 'fixed':
				price = record.fixed_price

			elif record.compute_price == 'percentage':
				price = (price - (price * (record.percent_price / 100))) or 0.0
			else:
				#complete formula
				price_limit = price
				price = (price - (price * (record.price_discount / 100))) or 0.0
				if record.price_round:
					price = tools.float_round(price, precision_rounding=record.price_round)

				if record.price_surcharge:
					price_surcharge = convert_to_price_uom(record.price_surcharge)
					price += price_surcharge

				if record.price_min_margin:
					price_min_margin = convert_to_price_uom(record.price_min_margin)
					price = max(price, price_limit + price_min_margin)

				if record.price_max_margin:
					price_max_margin = convert_to_price_uom(record.price_max_margin)
					price = min(price, price_limit + price_max_margin)
			record.discounted_amount = price

	@api.multi
	def set_sequence_top(self):
		self._cr.execute('SELECT MAX(website_sequence) FROM product_pricelist_item')
		max_sequence = self._cr.fetchone()[0] or 0
		return self.write({'website_sequence': max_sequence + 1})
	@api.multi
	def set_sequence_bottom(self):
		self._cr.execute('SELECT MIN(website_sequence) FROM product_pricelist_item')
		min_sequence = self._cr.fetchone()[0] or 0
		return self.write({'website_sequence': min_sequence -1})

	@api.multi
	def set_sequence_up(self):
		self._cr.execute("""  SELECT id, website_sequence FROM product_pricelist_item
		WHERE website_sequence > %s  ORDER BY website_sequence ASC LIMIT 1""" % (self.website_sequence))
		prev = self._cr.fetchone()
		if prev:
			prev_obj = self.browse(prev[0])
			prev_obj.write({'website_sequence': self.website_sequence})
			return self.write({'website_sequence': prev[1]})
		else:
			return self.set_sequence_top()
	@api.multi
	def set_sequence_down(self):
		self._cr.execute("""  SELECT id, website_sequence FROM product_pricelist_item
		WHERE website_sequence < %s  ORDER BY website_sequence DESC LIMIT 1""" % (self.website_sequence, ))
		next = self._cr.fetchone()
		if next:
			next_obj = self.browse(next[0])
			next_obj.write({'website_sequence': self.website_sequence})
			return self.write({'website_sequence': next[1]})
		else:
			return self.set_sequence_bottom()

	@api.model
	def create(self,vals):
		context = dict(self._context or {})
		if not vals.get('pricelist_id',False) and vals.get('my_deals_m2o'):
			deal_obj = self.env['website.deals'].browse(vals['my_deals_m2o'])
			vals['pricelist_id'] = deal_obj.wk_pricelist.id
		return super(product_pricelist_item , self.with_context(context)).create(vals)

	@api.multi
	def write(self ,vals):
		context = dict(self._context or {})
		if not vals.get('pricelist_id',False) and vals.get('my_deals_m2o'):
			deal_obj = self.env['website.deals'].browse(vals['my_deals_m2o'])
			vals['pricelist_id'] = deal_obj.wk_pricelist.id
		return super(product_pricelist_item, self.with_context(context)).write(vals)

class WebsiteDeals(models.Model):
	_name = 'website.deals'
	_description = 'Website Deals'
	_order = "id desc"

	@api.model
	def _get_default_pricelist(self):
		ir_values = self.env['ir.values']
		wk_pricelist = ir_values.sudo().get_default('website.daily.deals.conf', 'wk_pricelist')
		return wk_pricelist


	name = fields.Char(string = 'Name', required=True)
	title = fields.Char(string = 'Title', required=True, help="title of the deal to show in website")
	description = fields.Text(string = 'Description' , help="description of the deal to show in website")
	start_date = fields.Datetime('Start Date', required=True, default=datetime.now())
	end_date = fields.Datetime('End Date', required=True,default=datetime.now()+ timedelta(days=1))
	banner = fields.Binary('Banner', required=True)
	overide_config = fields.Boolean('Override Default Configuration')
	item_to_show = fields.Selection([('banner_only','Banner Only'),('products_only','Products Only'), ('both','Both')],'What to Display in Website', default='both', help="choose what you want to display in website.")
	show_title = fields.Boolean('Show Title In Website', help="the title will be displayed in the website and it is displayed only if 'What to Display in Website = Products Only'")
	products  = fields.One2many(comodel_name = 'product.pricelist.item', inverse_name ='my_deals_m2o' ,string='Products')
	display_products_as = fields.Selection([('grid','Grid'),('slider','Slider')],'How to display Products in Website', default='grid', help="choose how to display the produts in website.")
	show_message_before_expiry = fields.Boolean('Show Message before Expiry',help="Do you want to show a message before the expiry date of the deal, if yes then set this true.")
	message_before_expiry = fields.Char('Message before Expiry', help="The message you want to show in the website when deal is about to expire.")
	interval_before = fields.Integer('Time interval before to display message' , help="How much time before the expiry date you want to display the message.")
	unit_of_time = fields.Selection([('minutes','Minutes'),('hours','Hours'),('days','Days'),('weeks','Weeks'),('months','Months')],'Time Unit', default='hours')
	show_message_after_expiry = fields.Boolean('Show Message After Expiry', help="Do you want to show the message after the expiry date of the deal.")
	message_after_expiry = fields.Char('Message After Expiry', help="The message you want to show in the website when deal is expired.")
	deal_after_expiration = fields.Selection([('blur','Blur'),('delete','Delete')],'What to do with deal after Expiry', default='blur', help="What do you want to do with deal after expiration.Either you can blur the deals in website or delete a deal from website")
	state = fields.Selection([('draft','Draft'),('validated','In Progress'),('cancel','Cancel')],'State', default='draft')
	wk_pricelist = fields.Many2one('product.pricelist','Pricelist' ,required=True ,default=_get_default_pricelist)

	@api.model
	def create(self,vals):
		if not vals.get('banner'):
			raise UserError('No banner chosen, please choose a banner before saving.')
		return super(WebsiteDeals , self).create(vals)



	@api.multi
	@api.onchange('wk_pricelist')
	def onchange_wk_pricelist(self):
		if self.wk_pricelist:
			self.change_pricelist = False
			if self.products:
				self.products = [[5]]

	@api.multi
	def get_daily_deals(self):
		all_deals = self.search([])
		if all_deals:
			return all_deals
		else:
			return []
	@api.multi
	def set_to_draft(self):
		self.state = 'draft'
				
	@api.model		
	def _get_page_header(self):
		ir_values = self.env['ir.values']
		show_header = ir_values.sudo().get_default('website.daily.deals.conf', 'show_page_header')
		page_header_text = ir_values.sudo().get_default('website.daily.deals.conf', 'page_header_text')
		if show_header:
			return page_header_text
		return False

	@api.model
	def show_deals_banner(self):
		if self.overide_config:
			if self.item_to_show == 'banner_only' or self.item_to_show == 'both':
				return True
		else:
			ir_values = self.env['ir.values']
			config_value = ir_values.sudo().get_default('website.daily.deals.conf', 'item_to_show')
			if config_value == 'banner_only' or config_value == 'both':
				return True
		return False

	@api.model
	def show_all_products(self):
		if self.overide_config:
			if self.item_to_show == 'products_only' or self.item_to_show == 'both':
				return True
		else:
			ir_values = self.env['ir.values']
			config_value = ir_values.sudo().get_default('website.daily.deals.conf', 'item_to_show')
			if config_value == 'products_only' or config_value == 'both':
				return True
		return False

	@api.model
	def _get_display_products_as(self):
		if self.overide_config:
			if self.display_products_as == 'slider':
				return 'slider'
			else:
				return 'grid'
		else:
			ir_values = self.env['ir.values']
			config_value = ir_values.sudo().get_default('website.daily.deals.conf', 'display_products_as')
			if config_value == 'slider':
				return 'slider'
			else:
				return 'grid'
	@api.model
	def _message_before_expiry(self):
		message = ''
		if self.overide_config:
			message = self.message_before_expiry
		else:
			ir_values = self.env['ir.values']
			message = ir_values.sudo().get_default('website.daily.deals.conf', 'message_before_expiry')
		return message

	@api.model
	def _message_after_expiry(self):
		message = ''
		if self.overide_config:
			message = self.message_after_expiry
		else:
			ir_values = self.env['ir.values']
			message = ir_values.sudo().get_default('website.daily.deals.conf', 'message_after_expiry')
		return message
			


	@api.model 
	def _calcualte_time(self,interval_before,unit_of_time):
		expiry_date = self.end_date
		start_from = False
		end_date = self.end_date
		end_date = datetime.strptime(end_date,"%Y-%m-%d %H:%M:%S")
		if unit_of_time == 'minutes':
			start_from = datetime.strptime(expiry_date,"%Y-%m-%d %H:%M:%S") + relativedelta(minutes =- interval_before)
		elif unit_of_time == 'hours':
			start_from = datetime.strptime(expiry_date,"%Y-%m-%d %H:%M:%S") + relativedelta(hours =- interval_before)
		elif unit_of_time == 'days':
			start_from = datetime.strptime(expiry_date,"%Y-%m-%d %H:%M:%S") + relativedelta(days =- interval_before)
		elif unit_of_time == 'months':
			start_from = datetime.strptime(expiry_date,"%Y-%m-%d %H:%M:%S") + relativedelta(months =- interval_before)
		elif unit_of_time == 'weeks':
			start_from = datetime.strptime(expiry_date,"%Y-%m-%d %H:%M:%S") + relativedelta(weeks =- interval_before)
		if datetime.now() >= start_from and datetime.now() < end_date:
			return 'show_msg_before'
		elif datetime.now() >= end_date:
			if self.show_message_after_expiry:
				return 'show_msg_after'
			return False
		else:
			return False

	@api.model
	def _calculate_expiry_message_time(self):
		if self.show_message_before_expiry:
			result =  False
			if self.overide_config:
				interval_before = self.interval_before
				unit_of_time = self.unit_of_time
			else:
				ir_values = self.env['ir.values']
				interval_before = ir_values.sudo().get_default('website.daily.deals.conf', 'interval_before')
				unit_of_time = ir_values.sudo().get_default('website.daily.deals.conf', 'unit_of_time')
			if interval_before and unit_of_time:
				result = self._calcualte_time(interval_before,unit_of_time)
			else:
				raise UserError('Please set the configuration')
			return result

	@api.model
	def _when_to_start_deals(self):
		start_date = self.start_date
		start_date = datetime.strptime(start_date,"%Y-%m-%d %H:%M:%S")
		if datetime.now() >= start_date:
			return True 
		else:
			return False

	@api.model		
	def _show_deal_after_expiration(self):
		end_date = self.end_date
		end_date = datetime.strptime(end_date,"%Y-%m-%d %H:%M:%S")
		if datetime.now() >= end_date:
			if self.deal_after_expiration and  self.deal_after_expiration == 'delete':
				return 'delete'
			else:
				return 'blur'
		else:
			return True

	@api.multi
	def button_validate_the_deal(self):
		start_date = datetime.strptime(self.start_date,"%Y-%m-%d %H:%M:%S")
		end_date = datetime.strptime(self.end_date,"%Y-%m-%d %H:%M:%S")

		if start_date > end_date:
			raise UserError('End date can not be earlier than start date.')
		# elif start_date < datetime.now():
		# 	raise UserError('Start Date should be greater that Current Date.')
		else:
			self.state = 'validated'

	@api.multi
	def cancel_deal(self):
		self.state = 'cancel'

class PricelistItem(models.Model):
	_inherit = "product.pricelist.item"

	@api.model
	def create(self,vals):
		if self._context.get('daily_deals'):
			vals['applied_on'] = '1_product'
		return super(PricelistItem, self).create(vals)