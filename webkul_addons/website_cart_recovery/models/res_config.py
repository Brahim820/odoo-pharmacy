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
from odoo import api, fields, models, _

mail_count = [('one','One'),
              ('two','Two'),
              ('three','Three')]

class WebsiteCartRecoverySettings(models.TransientModel):
    _inherit = 'website.config.settings'
    _name = 'website.cart.recovery.settings'

    @api.model
    def _get_default_cart_recovery_cron_shedular(self):
        cron_id = self.env['ir.model.data'].xmlid_to_object('website_cart_recovery.ir_cron_cart_recovery').id
        return cron_id

    @api.model
    def _get_default_cart_recovery_email_template_one(self):
        temp_id = self.env['ir.model.data'].xmlid_to_object('website_cart_recovery.website_cart_recovery_email_template_one')
        return temp_id.id if temp_id else False

    @api.model
    def _get_default_cart_recovery_email_template_two(self):
        temp_id = self.env['ir.model.data'].xmlid_to_object('website_cart_recovery.website_cart_recovery_email_template_two')
        return temp_id.id if temp_id else False

    @api.model
    def _get_default_cart_recovery_email_template_three(self):
        temp_id = self.env['ir.model.data'].xmlid_to_object('website_cart_recovery.website_cart_recovery_email_template_three')
        return temp_id.id if temp_id else False

    followup_mail_count = fields.Selection(mail_count, string = 'Follow up Mail Count', required = '1', help = """Number of mails to be send for follow up.""")
    order_lifetime = fields.Integer(string='Abandoned Cart Declaration(hrs.)', help = """Set time after when order consider as abandoned""")
    recovery_sales_teams = fields.Many2many('crm.team','cart_sale_team','cart_id','team_id', string='Sales Teams',required = True)
    cart_recovery_cron_shedular = fields.Many2one('ir.cron','Cron Settings', required = True, default=_get_default_cart_recovery_cron_shedular)
    cart_recovery_email_template_one = fields.Many2one('mail.template','First Follow up Email Template',required = True, default=_get_default_cart_recovery_email_template_one)
    cart_recovery_template_one_time =  fields.Integer(string='Send Email After(hrs.)')
    cart_recovery_email_template_two = fields.Many2one('mail.template','Secound Follow up Email Template',required = True, default=_get_default_cart_recovery_email_template_two)
    cart_recovery_template_two_time =  fields.Integer(string='Send Email After(hrs.)')
    cart_recovery_email_template_three = fields.Many2one('mail.template','Third Follow up Email Template',required = True, default=_get_default_cart_recovery_email_template_three)
    cart_recovery_template_three_time =  fields.Integer(string='Send Email After(hrs.)')
    module_website_stock =  fields.Boolean(string="Website Product Stock")
    # check_product_availability = fields.Boolean(string = "Confirm Product Availability", help = """Check Product Availability before Sending Email.(Install Website Stock Module to Enable This Option.)""")

    @api.multi
    def set_cart_recovery_configuration(self):
        ir_values = self.env['ir.values'].sudo()
        ir_values.set_default('website.cart.recovery.settings', 'followup_mail_count', 
        self.followup_mail_count or None)

        ir_values.set_default('website.cart.recovery.settings', 'order_lifetime', 
        self.order_lifetime or None)

        ir_values.set_default('website.cart.recovery.settings', 'recovery_sales_teams', 
        self.recovery_sales_teams and self.recovery_sales_teams.ids or False)

        ir_values.set_default('website.cart.recovery.settings', 'cart_recovery_email_template_one', 
        self.cart_recovery_email_template_one and self.cart_recovery_email_template_one.id or False)

        ir_values.set_default('website.cart.recovery.settings', 'cart_recovery_template_one_time', 
        self.cart_recovery_template_one_time or None)

        ir_values.set_default('website.cart.recovery.settings', 'cart_recovery_email_template_two', 
        self.cart_recovery_email_template_two and self.cart_recovery_email_template_two.id or False)

        ir_values.set_default('website.cart.recovery.settings', 'cart_recovery_template_two_time', 
        self.cart_recovery_template_two_time or None)

        ir_values.set_default('website.cart.recovery.settings', 'cart_recovery_email_template_three', 
        self.cart_recovery_email_template_three and self.cart_recovery_email_template_three.id or False)

        ir_values.set_default('website.cart.recovery.settings', 'cart_recovery_template_three_time', 
        self.cart_recovery_template_three_time or None)
        return True

    @api.multi
    def get_cart_recovery_configuration(self):
        ir_values = self.env['ir.values'].sudo()
        followup_mail_count = ir_values.get_default('website.cart.recovery.settings', 'followup_mail_count')

        order_lifetime = ir_values.get_default('website.cart.recovery.settings', 'order_lifetime')

        recovery_sales_teams = ir_values.get_default('website.cart.recovery.settings', 'recovery_sales_teams')

        cart_recovery_email_template_one = ir_values.get_default('website.cart.recovery.settings', 'cart_recovery_email_template_one')

        cart_recovery_template_one_time = ir_values.get_default('website.cart.recovery.settings', 'cart_recovery_template_one_time')

        cart_recovery_email_template_two = ir_values.get_default('website.cart.recovery.settings', 'cart_recovery_email_template_two')

        cart_recovery_template_two_time = ir_values.get_default('website.cart.recovery.settings', 'cart_recovery_template_two_time')

        cart_recovery_email_template_three = ir_values.get_default('website.cart.recovery.settings', 'cart_recovery_email_template_three')

        cart_recovery_template_three_time = ir_values.get_default('website.cart.recovery.settings', 'cart_recovery_template_three_time')



        return {
            'followup_mail_count':followup_mail_count,
            'order_lifetime':order_lifetime,
            'recovery_sales_teams':recovery_sales_teams,
            'cart_recovery_template_one_time':cart_recovery_template_one_time,
            'cart_recovery_template_two_time':cart_recovery_template_two_time,
            'cart_recovery_template_three_time':cart_recovery_template_three_time,
            'cart_recovery_email_template_three':cart_recovery_email_template_three,
            'cart_recovery_email_template_one':cart_recovery_email_template_one,
            'cart_recovery_email_template_two':cart_recovery_email_template_two
            }