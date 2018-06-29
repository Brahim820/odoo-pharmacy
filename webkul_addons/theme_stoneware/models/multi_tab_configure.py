
from odoo import models, fields, api

class multitab_configure(models.Model):
    _name = 'multitab.configure'

    name= fields.Char("Group Name")
    product_ids=fields.Many2many("product.template",string="Products",domain=[('website_published','=',True)])
    active=fields.Boolean("Active")

class collection_configure(models.Model):

	_name = 'collection.configure'

	name=fields.Char("Title")
	tab_collection_ids=fields.Many2many('multitab.configure',string="Select Collection")
	active=fields.Boolean("Active")

