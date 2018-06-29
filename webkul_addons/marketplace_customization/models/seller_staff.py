# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class SellerStaff(models.Model):
    _name = 'seller.staff'

    def _get_partner_id(self):
        if self.env.user.partner_id.seller:
            return self.env.user.partner_id.id
        else:
            return self.env['res.partner']

    image = fields.Binary("Image")
    name = fields.Char("Name", required=True)
    login = fields.Char("Login", required=True)
    partner_id = fields.Many2one(
        "res.partner",
        "Seller Of Staff",
        default=_get_partner_id,
        required=True,
        domain="[('seller', '=', True), ('state', '=', 'approved')]")
    state = fields.Selection(
        [("draft", "Draft"), ("requested", "Requested"), ("approved", "Approved"),
         ("rejected", "Rejected")],
        default="draft")
    user_id = fields.Many2one("res.users", "User", readonly=True)
    create_date = fields.Datetime("Create Date")

    @api.multi
    def create_seller_staff_user(self):
        for rec in self:
            seller_staff_user = False
            if not rec.user_id:
                user_vals = {
                    "partner_id": rec.partner_id.id,
                    "login": rec.login,
                    "seller_staff_id": rec.id,
                    "groups_id": False,
                }
                seller_staff_user = self.env["res.users"].create(user_vals)

            else:
                rec.user_id.active = True
                seller_staff_user = rec.user_id
            if seller_staff_user:
                rec.user_id = seller_staff_user.id
                rec.assign_seller_group_to_staff()

    @api.multi
    def do_approve(self):
        #First change state to approve and then create res.user record
        non_approve_record = self.filtered(
            lambda o: o.state in ('requested', 'rejected'))
        if non_approve_record:
            non_approve_record.create_seller_staff_user()
            non_approve_record.state = "approved"

    @api.multi
    def assign_seller_group_to_staff(self):
        for obj in self:
            if obj.user_id:
                seller_user = self.env["res.users"].search([('partner_id', '=', self.partner_id.id), ('seller_staff_id', '=', False)], limit=1)
                if seller_user:
                    for group in seller_user.groups_id:
                        group.sudo().write({"users": [(4, obj.user_id.id, 0)]})
                staff_group = self.env.ref(
                    'marketplace_customization.group_marketplace_seller_staff')
                if staff_group:
                    staff_group.sudo().write({"users": [(4, obj.user_id.id, 0)]})

    @api.multi
    def do_request(self):
        self.write({'state': 'requested'})


    @api.multi
    def do_reject(self):
        #First change state to rejected and then maker res.user record inactive
        self.write({'state': 'rejected'})
        for obj in self:
            obj.user_id.active = False


    @api.multi
    def change_password_wizard(self):
        self.ensure_one()
        password_wizard_obj = self.env["change.password.wizard"].create({
            "user_ids" : [(0, 0, {
                'user_id': self.user_id.id,
                'user_login': self.user_id.login,
            })]
        })
        return {
            'name': "Change Password2",
            'type': "ir.actions.act_window",
            'view_type': "form",
            'view_mode': "form",
            'target': "new",
            "res_id": password_wizard_obj.id,
            'res_model': "change.password.wizard",
        }
