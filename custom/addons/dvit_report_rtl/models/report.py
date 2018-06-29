# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Mohammed M. Hagag.
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

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.http import request
import time


class Report(models.Model):
    _inherit = 'report'

    @api.multi
    def render(self, template, values=None):

        if values is None:
            values = {}

        context = dict(self.env.context, inherit_branding=True)  # Tell QWeb to brand the generated html

        view_obj = self.env['ir.ui.view']

        def translate_doc(doc_id, model, lang_field, template):
            return self.translate_doc(doc_id, model, lang_field, template, values)

        model=values['doc_model']
        doc_id=values['doc_ids'][0]
        doc = self.env[model].browse(doc_id)

        try:
             lang = str(doc.partner_id.lang)
        except AttributeError:
             lang = context.get('lang')

        lang_obj = self.env['res.lang'].search([('code', '=', lang),('active','=',True)])
        lang_dir = str(lang_obj.direction)
        values['lang_dir'] = str(lang_dir)
        print "-------- doc_partner= "+str(doc.partner_id)+" ---------------"
        print "-------- lang= "+str(lang)+" ---------------"
        print "-------- lang_dir= "+str(lang_dir)+" ---------------"
        print "-------- values_lang_dir= "+str(values['lang_dir'])+" ---------------"

        user = self.env['res.users'].browse(self.env.uid)
        website = None
        if request and hasattr(request, 'website'):
            if request.website is not None:
                website = request.website
                context = dict(context, translatable=context.get('lang') != request.website.default_lang_code)

        values.update(
            time=time,
            context_timestamp=lambda t: fields.datetime.context_timestamp( t, context),
            translate_doc=translate_doc,
            editable=True,
            user=user,
            res_company=user.company_id,
            website=website,
        )
        return view_obj.render_template(template, values)
