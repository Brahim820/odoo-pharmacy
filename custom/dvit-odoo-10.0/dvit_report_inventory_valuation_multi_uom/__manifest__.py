# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Inventory valuation by location Report",
    "version": "10.0.1.2",
    "author": "DVIT.ME, Ananthu Krishna",
    "license": "AGPL-3",
    "website": "dvit.me",
    "summary": "Inventory valuation pdf report",
    "description": "Print pdf report for inventory valuation by location in all product units",
    "category": "Inventory",
    "depends": [
        'stock',
    ],
    "data": [
        "report/stock_inventory_report.xml",
        "report/stock_inventory_location_report.xml",
        "wizard/stock_quant_report.xml",
        "views/product_view.xml",
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
    "external_dependencies": {
        'python': [],
    },
}
