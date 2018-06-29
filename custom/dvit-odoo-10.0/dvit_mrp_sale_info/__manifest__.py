# -*- coding: utf-8 -*-
# © 2016 Antiun Ingenieria S.L. - Javier Iniesta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MRP Sale Info",
    "summary": "Adds sale information to Manufacturing models",
    "version": "10.0.1.2",
    "category": "Manufacturing",
    "website": "http://www.dvit.me",
    "author": ["DVIT.ME",
                "Antiun Ingenieria S.L.",
              "OdooMRP team",
              "AvanzOSC",
              "Serv. Tecnol. Avanzados - Pedro M. Baeza",
              "Odoo Community Association (OCA), ",],
    "license": "AGPL-3",
    "application": False,
    'installable': True,
    "depends": [
        "sale_mrp",
        "stock"
    ],
    "data": [
        "views/mrp_production.xml",
        "views/mrp_workorder.xml"
    ]
}
