# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    date_order = fields.Datetime(related="order_id.date_order", )


class delivery_period(models.Model):
    _name = 'delivery.period'
    _description = 'Time Periods'

    name = fields.Char(string="Name", )

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    country_id = fields.Many2one(related='partner_id.country_id', readonly=True, store=True)
    state_id = fields.Many2one(related='partner_id.state_id', readonly=True, store=True)
    city_id = fields.Many2one(related='partner_id.city_id', readonly=True, store=True)
    zone_id = fields.Many2one(related='partner_id.zone_id', readonly=True, store=True)
    building_id = fields.Many2one(related='partner_id.building_id', readonly=True, store=True)
    sequence = fields.Integer(related='partner_id.building_id.sequence', readonly=True, store=True)
    floor = fields.Char(related='partner_id.floor', readonly=True, store=True)
    delivery_period = fields.Many2one(string="Delivery Time",comodel_name="delivery.period",)
    delivery_date = fields.Date(string="Delivery Date", )

class ResPartner(models.Model):
    _inherit = 'res.partner'
    building_id= fields.Many2one("res.zone.building", string="Buliding" )
    country_id = fields.Many2one(comodel_name="res.country", string="Country", required=True, )
    city_id = fields.Many2one(comodel_name="res.country.city", string="City", required=True, )
    zone_id = fields.Many2one(comodel_name="res.country.city.zone", string="Zone", required=True, )
    floor = fields.Char(string="Floor" )

class ResCountryState(models.Model):
    _inherit = 'res.country.state'
    city_ids = fields.One2many(
        string="Cities",
        comodel_name="res.country.city",
        inverse_name="state_id",
    )

class ResCountryCity(models.Model):
    _name = 'res.country.city'
    name = fields.Char("City",required=True)
    state_id = fields.Many2one(comodel_name="res.country.state", string="state", required=True, )
    zip_code = fields.Integer("Zip",size=5)
    zone_ids = fields.One2many(
        string="Zones",
        comodel_name="res.country.city.zone",
        inverse_name="city_id",
    )

class ResCountryCityZone(models.Model):
    _name = 'res.country.city.zone'
    city_id = fields.Many2one(comodel_name="res.country.city", string="City", required=True, )
    name = fields.Char("Zone",required=True)
    sequence = fields.Integer("Sequence")
    building_ids = fields.One2many(
        string="Buildings",
        comodel_name="res.zone.building",
        inverse_name="zone_id",
    )

class ResZoneBuilding(models.Model):
    _name = 'res.zone.building'
    _order = 'sequence'
    name = fields.Char('Building No.',required=True)
    zone_id = fields.Many2one(comodel_name="res.country.city.zone", string="Zone" , required=True)
    sequence =fields.Integer("Sequence", default=None, required=True)
