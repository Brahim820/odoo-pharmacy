# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################

import werkzeug
import logging
from odoo import models, fields, api, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.addons.payment_cash_on_delivery.controllers.main import WebsiteSale
from odoo.http import request
_logger = logging.getLogger(__name__)
HelpState = _(
    """Allowed  State(s) from COD Availability,For
        Allowing all State just set it to be blank"""
    )
HelpZip =_(
    """Enter comma separated Zip codes like:-
        WC2N,201301,21044,400001,460001,970001,
        For Allowing all zip just set it to be blank!"""
    )

HelpPolicy = _(
    """Enter Policy and Authenticity
        content to be display  on Product Page"""
    )
class WkCODApplicabilityRule(models.Model):
    _name = 'wk.cod.applicability.rule'
    allowed_country_list = fields.Many2one(
        "res.country", required=1, string='Allow Country')
    allowed_state_list = fields.Many2many(
            "res.country.state",
            "wk_payment_acquirer_cod_rule_wk_res_country_state_relation",
            "wk_payment_acquirer_cod_rule",
            "wk_cod_res_country_sate",
            "Allow  State(s)",
            help=HelpState
        )
    zipcode_list = fields.Text(
            string='ZipCodes',
            help=HelpZip
        )
    cod_fk = fields.Many2one("wk.cod")


class WkCOD(models.Model):
    _name = 'wk.cod'
    name = fields.Char(string='Name', default='Default Rule')
    min_order_amount = fields.Float(
            string='Min Order Amount',
            required=1,
            default=100,
            help='Minimum Order Amount for COD Availability'
        )
    max_order_amount = fields.Float(
            string='Max Order Amount',
            required=1,
            default=10000,
            help='Maximum Order Amount for COD Availability'
        )
    exclude_product = fields.Many2many(
            "product.template",
            "wk_payment_acquirer_cod_wk_product_template_relation",
            "wk_payment_acquirer_cod",
            "wk_product_template",
            "Exclude Product(s)",
            help='Exclude Product(s) from COD Availability'
        )
    cod_applicability = fields.One2many(
            comodel_name='wk.cod.applicability.rule',
            inverse_name='cod_fk',
            string='COD Applicability',
            required=1
        )
    show_expected_cod_date = fields.Boolean(
            string='Show Delivered By Date',
            default=True,
            help='Show Expected COD Date Of Delivery on Product Page'
        )
    show_policy = fields.Boolean(
            string='Show Policy',
            default=True,
            help='Show Policy and Authenticity  on Product Page'
        )
    policy_content = fields.Char(
            string='Policy Content',
            default='Order Order Amount Must Be in Between 100€ 100000€',
            help=HelpPolicy)
    cod_availability_message = fields.Char(
        string='Availability Message',
        default='COD AVAILABLE !',
        help='Enter Availability Message  content to be display  on Product Page'
    )
    cod_unavailability_message = fields.Char(
        string='Unavailability Message',
        default='Currently we do not provide COD for this item !',
        help='Enter Availability Message  content to be display  on Product Page'
     )
    cod_unavailability_payment_message = fields.Text(
        string='Unavailability Message on Payment',
        default='Some  product in your cart can not delivered  through Cash On Delivery ',
        help='Enter Unavailability Message  content to be display  on Payment Page'
    )

    @api.one
    @api.constrains('min_order_amount', 'min_order_amount')
    def _check_order_limit(self):
        """	A private method to validate the Order limit!"""
        if self.min_order_amount <= 0 or self.max_order_amount <= 0:
            raise ValidationError(_("Order Limit Can't be Negative"))
        elif self.min_order_amount >= self.max_order_amount:
            raise ValidationError(_("Minimum Order Amount  smaller  than  Maximum   Order Amount"))


    @api.model
    def check_zipcode_list(self, partner_id,  zipcode_list):
        return partner_id.zip if partner_id and partner_id.zip and zipcode_list and (partner_id.zip.strip().upper() in zipcode_list.strip().upper().split(',')) else False

    @api.model
    def check_state_list(self, partner_id,  allowed_state_list):
        code = partner_id and partner_id.state_id.code
        return allowed_state_list.filtered(lambda st: code in st.mapped('code'))

    @api.model
    def check_country_list(self, partner_id):
        # return cod_applicability if partner_id and partner_id.country_id and partner_id.country_id.code in[cod_applicability.allowed_country_list.code for cod_applicability in self.cod_applicability] else False
        code = partner_id and partner_id.country_id.code
        rule = self.cod_applicability.mapped('allowed_country_list.code')
        cod_applicability = self.cod_applicability.filtered(lambda ap: code in ap.mapped('allowed_country_list.code'))
        if cod_applicability:
            return cod_applicability
        return []



class website(models.Model):
    _inherit = 'website'

    @api.model
    def is_cod_available(self, product=None, payment_acquirer=None):
        cod = request.env['payment.acquirer'].sudo().search(
            [('provider', '=', 'cash_on_delivery')], limit=1)
        order = request.website.sale_get_order()
        recipient = order and order.partner_shipping_id and order.partner_shipping_id or request.env.user.partner_id
        if product and cod.cod_rule:
            return cod.validate_address(recipient) and product.id not in[product_item.id for product_item in cod.cod_rule.exclude_product]
        if payment_acquirer and payment_acquirer.provider == 'cash_on_delivery' and cod.cod_rule:
            product_in_line = set(
                order_line.product_tmpl_id.id for order_line in order.order_line)
            exclude_product = set(
                product_item.id for product_item in cod.cod_rule.exclude_product)
            return cod.validate_address(recipient) and order.amount_total >= cod.cod_rule.min_order_amount and order.amount_total <= cod.cod_rule.max_order_amount and not product_in_line & exclude_product
        return True

    @api.model
    def expected_cod_date(self, product):
        from datetime import date
        from dateutil.relativedelta import relativedelta
        return (date.today() + relativedelta(days=+int(product.sale_delay))).strftime("%d.%m.%Y")


class AcquirerCOD(models.Model):
    _inherit = 'payment.acquirer'

    cod_rule = fields.Many2one("wk.cod", "COD Availability Rule")
    provider = fields.Selection(selection_add=[('cash_on_delivery', 'COD')])
    @api.model
    def validate_address(self, partner_id):
        checkstate = True
        checkzip = True
        cod_applicabilitys = self.cod_rule.check_country_list(partner_id)
        for cod_applicability in cod_applicabilitys:
            if cod_applicability:
                if cod_applicability.allowed_state_list:
                    checkstate = self.cod_rule.check_state_list(
                        partner_id, cod_applicability.allowed_state_list)
                if cod_applicability.zipcode_list:
                    checkzip = self.cod_rule.check_zipcode_list(
                        partner_id, cod_applicability.zipcode_list)
                return checkstate and checkzip
        else:
            return False

    @api.multi
    def cash_on_delivery_get_form_action_url(self):
        self.ensure_one()
        return WebsiteSale._codfeedbackUrl


class TxCOD(models.Model):
    _inherit = 'payment.transaction'
    provider = fields.Selection(
        string='Providers', selection=[('cash_on_delivery','COD')])


    @api.model
    def _cash_on_delivery_form_get_tx_from_data(self,data):
        reference = data.get('reference')
        if not reference:
            error_msg = _('COD: received data with missing reference (%s) or payment has not been captured ' % (
                reference))
            _logger.warning("# %r----%r"%(error_msg, data))
            raise ValidationError(error_msg)
        tx_ids = self.sudo().search([('reference', '=', reference)])
        if not tx_ids or len(tx_ids) > 1:
            message = tx_ids and 'Multiple order found'or 'No order found'
            error_msg = _('COD: Received data for reference %s .%s.' % (
                reference, message))
            _logger.warning(error_msg)
            raise ValidationError(error_msg)
        return tx_ids[0]

    @api.model
    def _cash_on_delivery_form_get_invalid_parameters(self,data):
        invalid_parameters = []
        return invalid_parameters

    @api.model
    def _cash_on_delivery_form_validate(self,  data):
        vals = dict(
                    state='pending',
                    date_validate = fields.datetime.now(),
                )
        if self.acquirer_id.auto_confirm != 'none':
            vals['state'] = 'done'
        return self.write(vals)
