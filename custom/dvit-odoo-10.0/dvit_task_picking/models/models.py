# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    task_id = fields.Many2one(
        string="Task",
        comodel_name="project.task",
    )

class ProjectTask(models.Model):
    _inherit = 'project.task'

    stock_pickings = fields.One2many(
        string="Warehouse Transfers",
        comodel_name="stock.picking",
        inverse_name="task_id",
        )

    is_closed = fields.Boolean(string="Closed", related="stage_id.closed",
        help="Based on stage closed status, \
        to reopen move the task to an open stage." )
