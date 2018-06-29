# -*- coding: utf-8 -*-
# Copyright 2018 CodeFish ()
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields
from odoo.tools.translate import _


class disease_categories(models.Model):
    _inherit = "x_disease_categories"

    write_date = fields.Datetime(
        string=_("Last Updated on"),
        required=False,
        translate=False,
        readonly=False
    )
    name = fields.Char(
        string=_("Category Name"),
        required=False,
        translate=False,
        readonly=False
    )
    display_name = fields.Char(
        string=_("Display Name"),
        required=False,
        translate=False,
        readonly=True
    )
    write_uid = fields.Many2one(
        string=_("Last Updated by"),
        required=False,
        translate=False,
        readonly=False
    )
    id = fields.Integer(
        string=_("ID"),
        required=False,
        translate=False,
        readonly=True
    )
    parent_category = fields.Many2one(
        string=_("Parent Category	"),
        required=False,
        translate=False,
        readonly=False
    )
    create_date = fields.Datetime(
        string=_("Created on"),
        required=False,
        translate=False,
        readonly=False
    )
    __last_update = fields.Datetime(
        string=_("Last Modified on"),
        required=False,
        translate=False,
        readonly=True
    )
    create_uid = fields.Many2one(
        string=_("Created by"),
        required=False,
        translate=False,
        readonly=False
    )
