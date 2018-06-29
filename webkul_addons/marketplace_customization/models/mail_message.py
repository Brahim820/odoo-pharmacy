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


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.multi
    @api.returns('self', lambda value: value.id)
    def message_post(self, body='', subject=None, message_type='notification',
                     subtype=None, parent_id=False, attachments=None,
                     content_subtype='html', **kwargs):
        res = super(MailThread, self).message_post(body=body, subject=subject, message_type=message_type, subtype=subtype, parent_id=parent_id, attachments=attachments, content_subtype=content_subtype, kwargs=kwargs)
        if self.env.user.seller_staff_id:
            res.body = res.body + "\n - (Staff: " + self.env.user.seller_staff_id.name + ")"
        return res
