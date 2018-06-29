# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
import logging

from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_base_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return (base_url)


    abandoned_order = fields.Boolean(string = "Is Abandoned Order ?", copy=False)
    abandoned_time = fields.Datetime(string = "Abandoned and mail send time")
    # partner_email = fields.Related('partner_id', 'email', type='char', string='email')
    followup_messages = fields.Integer(string="Number of Follow up Message Send", default=0)
    base_url = fields.Char(string = "Website", default=_get_base_url)

    @api.model
    def website_cart_recovery_main(self, called_manually=False):
        """
            this function called by cron and manually and call two different function for different works
        """
        context = self._context.copy() or {}
        context['send_type'] = 'manually'
        ir_value_obj = self.env['ir.values']
        no_of_folowup_msg_allow = ir_value_obj.sudo().get_defaults('website.cart.recovery.settings')
        res = { i[1]:i[2] for i in no_of_folowup_msg_allow }
        if not called_manually:
            _logger.info("************Info: Send mail function is called by cron**********")
            context['send_type'] = 'cron'
        self.with_context(context).make_order_abandoned( res)
        self.with_context(context).get_abandoned_orders_id(res)
        if context.get('send_type') == 'cron':
            return True

    def make_order_abandoned(self, default_vals = {} ):
        """
            this function mainlly check the condtion of order and make the order abandoned
        """
        sale_order_obj = self.env['sale.order']
        sales_teams = default_vals.get('recovery_sales_teams')
        order_lifetime = default_vals.get('order_lifetime')
        abandoned_ids = []
        context = self._context.copy() or {}
        if not order_lifetime:
            order_lifetime = 0
        if sales_teams:
            current_datetime = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            current_datetime = datetime.strptime(current_datetime, DEFAULT_SERVER_DATETIME_FORMAT)
            diff_datetime = current_datetime - timedelta(hours = order_lifetime)
            diff_datetime = diff_datetime.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            abandoned_ids = sale_order_obj.search([('state', '=', 'draft'), ('team_id', 'in', sales_teams), ('abandoned_order', '=', False), ('order_line', '!=', False),('write_date', '<=', diff_datetime)])
            abandoned_ids.write({'abandoned_order': True, 'abandoned_time': datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

            if context.get('send_type') == 'cron':
                _logger.info("************Cron Info:Succesfully orders make abandoned by Cron**********")
            else:
                _logger.info("++++++++++++Manually Info:Succesfully orders make abandoned Manuallty+++++++++")
        else:
            if context.get('send_type') == 'cron':
                _logger.error("*******Error in Sales Team, Sales Teams Not Found!!!")
            else:
                raise UserError(_("*******Error in Sales Team, Sales Teams Not Found!!!"))

    def get_abandoned_orders_id(self, default_vals = {} ):
        """
            this function send mail using cron schuduled action
        """
        sale_order_obj = self.env['sale.order']
        sales_teams = default_vals.get('recovery_sales_teams')
        followup_mail_count = default_vals.get('followup_mail_count')
        if followup_mail_count in ['one', 'two', 'three']:
            cart_recovery_template_one_time = default_vals.get('cart_recovery_template_one_time')
            if not cart_recovery_template_one_time:
                cart_recovery_template_one_time = 0

            current_datetime = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            current_datetime = datetime.strptime(current_datetime, DEFAULT_SERVER_DATETIME_FORMAT)
            diff_datetime = current_datetime - timedelta(hours = cart_recovery_template_one_time)
            diff_datetime = diff_datetime.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

            ids_for_send_mail = sale_order_obj.search([('state', '=', 'draft'), ('team_id', 'in', sales_teams), ('abandoned_order', '=', True), ('order_line', '!=', False), ('write_date', '<=', diff_datetime), ('followup_messages', '=', 0)])
            self.send_cart_recovery_mail(ids_for_send_mail, 1, default_vals)

        if followup_mail_count in ['two', 'three']:
            cart_recovery_template_two_time = default_vals.get('cart_recovery_template_two_time')
            if not cart_recovery_template_two_time:
                cart_recovery_template_two_time = 0

            current_datetime = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            current_datetime = datetime.strptime(current_datetime, DEFAULT_SERVER_DATETIME_FORMAT)

            diff_datetime = current_datetime - timedelta(hours = cart_recovery_template_two_time)
            diff_datetime = diff_datetime.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

            ids_for_send_mail = sale_order_obj.search([('state', '=', 'draft'), ('team_id', 'in', sales_teams), ('abandoned_order', '=', True), ('order_line', '!=', False), ('write_date', '<=', diff_datetime), ('followup_messages', '=', 1)])
            self.send_cart_recovery_mail(ids_for_send_mail, 2, default_vals)

        if followup_mail_count in ['three']:
            cart_recovery_template_three_time = default_vals.get('cart_recovery_template_three_time')
            if not cart_recovery_template_three_time:
                cart_recovery_template_three_time = 0

            current_datetime = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            current_datetime = datetime.strptime(current_datetime, DEFAULT_SERVER_DATETIME_FORMAT)

            diff_datetime = current_datetime - timedelta(hours = cart_recovery_template_three_time)
            diff_datetime = diff_datetime.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            ids_for_send_mail = sale_order_obj.search([('state', '=', 'draft'), ('team_id', 'in', sales_teams), ('abandoned_order', '=', True), ('order_line', '!=', False), ('write_date', '<=', diff_datetime), ('followup_messages', '=', 2)])
            self.send_cart_recovery_mail(ids_for_send_mail, 3, default_vals)

    def send_cart_recovery_mail(self, vals = [], msg_count = -1, default_vals = {}):
        sale_order_obj = self.env['sale.order']
        ir_model_data_obj = self.env['ir.model.data']
        template = self.env['mail.template']
        if msg_count == 1:
            temp_id = default_vals.get('cart_recovery_email_template_one')
            if temp_id :
                for obj in vals:
                    mail_confirmed = template.browse(temp_id).send_mail(obj.id, True)
                vals.write( {'followup_messages': 1, 'abandoned_time': datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
                _logger.info("############first follow up mail is send to following ids %r", vals)

        elif msg_count == 2:
            temp_id = default_vals.get('cart_recovery_email_template_two')
            if temp_id :
                for obj in vals:
                    mail_confirmed = template.browse(temp_id).send_mail(obj.id, True)
                vals.write({'followup_messages': 2, 'abandoned_time': datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
                _logger.info("############secound follow up mail is send to following ids %r", vals)

        elif msg_count == 3:
            temp_id = default_vals.get('cart_recovery_email_template_three')
            if temp_id :
                for obj in vals:
                    mail_confirmed = template.browse(temp_id).send_mail(obj.id, True)
                vals.write({'followup_messages': 3, 'abandoned_time': datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
                _logger.info("############third follow up mail is send to following ids %r", vals)
