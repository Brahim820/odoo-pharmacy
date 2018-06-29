# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectTask(models.Model):
    _inherit = 'project.task'
    reviewer_id = fields.Many2one('res.users', string='Reviewer')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if order.project_project_id:
                for line in order.order_line:
                    prod_man = line.product_id.product_manager and \
                    line.product_id.product_manager or line.product_id.categ_id.product_manager
                    if prod_man:
                        line_tasks = self.env['project.task'].search([('sale_line_id','=',line.id)])
                        for task in line_tasks:
                            task.reviewer_id = prod_man
                            task.user_id = prod_man
        return res
