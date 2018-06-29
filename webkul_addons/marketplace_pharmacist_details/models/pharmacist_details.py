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

from odoo import api, models, fields, _
import logging
_logger = logging.getLogger(__name__)

class PharmacistDetails(models.Model):
    _name = "pharmacist.details"
    _rec_name = "customer_id"

    customer_id = fields.Many2one("res.partner", "Customer", required=True)
    mp_pharmacist_ids = fields.One2many("pharmacist.id.details", "pharmacist_customer_id", string= "Pharmacist Ids")


class PharmacistIdDetails(models.Model):
    _name = "pharmacist.id.details"

    name = fields.Char("Pharmacy Name", required=True)
    email = fields.Char("Email")
    phone = fields.Char("Phone")

    street1 = fields.Char("Street")
    street2 = fields.Char("Street2")
    city = fields.Char("City")
    zipcode = fields.Char("PinCode")
    state_id = fields.Many2one('res.country.state', "State")
    country_id = fields.Many2one('res.country', "Country", related='state_id.country_id')

    comm_registration_file = fields.Binary("Commercial Registration")
    tax_card = fields.Binary("Tax Card")

    pharmacist_id = fields.Char("Pharmacy Id")
    marketplace_seller_id = fields.Many2one("res.partner", "Seller",
        required= True,
        domain="[('seller','=', True),('state','=','approved')]")
    pharmacist_customer_id = fields.Many2one("pharmacist.details", "Pharmacist Customer")

    _sql_constraints = [
        ('unique_pharmacist_id', 'unique(pharmacist_id)', _('There is already a record with this Pharmacist Id.')),
        ('pharmacist_customer_seller_uniq', 'unique (pharmacist_customer_id, marketplace_seller_id)',
        _('There is already a record for this customer with this seller.'))
    ]
