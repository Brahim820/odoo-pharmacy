# -*- coding: utf-8 -*-
# Copyright 2018 CodeFish ()
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields
from odoo.tools.translate import _


class disease(models.Model):
    _inherit = "x_disease"

    code = fields.Char(
        string=_("Code"),
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
    extra_Info = fields.Text(
        string=_("Extra Info"),
        required=False,
        translate=False,
        readonly=False
    )
    affected_chromosome = fields.Char(
        string=_("Affected Chromosome	"),
        required=False,
        translate=False,
        readonly=False
    )
    disease_category = fields.Many2one(
        string=_("Disease Category"),
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
    name = fields.Char(
        string=_("Name"),
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
    create_uid = fields.Many2one(
        string=_("Created by"),
        required=False,
        translate=False,
        readonly=False
    )
    gene = fields.Char(
        string=_("Gene"),
        required=False,
        translate=False,
        readonly=False
    )
    write_date = fields.Datetime(
        string=_("Last Updated on"),
        required=False,
        translate=False,
        readonly=False
    )
    protein_involved = fields.Char(
        string=_("Protein involved"),
        required=False,
        translate=False,
        readonly=False
    )
    write_uid = fields.Many2one(
        string=_("Last Updated by"),
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
