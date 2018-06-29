# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    purchase_ids = fields.One2many(string="Purchase Orders",comodel_name="purchase.order",
        inverse_name="production_id")
    purchase_req_ids = fields.One2many(string="Purchase Requisitions",comodel_name="purchase.requisition",
        inverse_name="production_id")


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    production_id = fields.Many2one(string="Manufacturing Orders",comodel_name="mrp.production")

class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'
    production_id = fields.Many2one(string="Manufacturing Orders",comodel_name="mrp.production")
