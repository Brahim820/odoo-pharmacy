# -*- coding: utf-8 -*-

from odoo import models, fields, api

class dvit_line_no(models.Model):
    _inherit='sale.order.line'
    line_no = fields.Char("No")
