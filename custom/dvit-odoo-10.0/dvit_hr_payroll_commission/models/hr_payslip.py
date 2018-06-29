# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# © 2017 Mohamed M. Hagag (DVIT.ME) <mohamedhagag1981@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    invoice_ids = fields.Many2many('account.invoice', string='Invoices')
    payment_ids = fields.Many2many('account.move.line', string='Payments')

    @api.multi
    def _detach_invoices(self):
        for slip in self:
            InvoiceObj = self.env['account.invoice']
            invoices = InvoiceObj.search([('slip_ids', 'in', self.ids)])
            for inv in invoices:
                inv.slip_ids -= slip

    @api.multi
    def _detach_AMLs(self):
        for slip in self:
            aml_obj = self.env['account.move.line']
            amls = aml_obj.search([('slip_ids', 'in', self.ids)])

            for aml in amls:
                aml.slip_ids -= slip

    @api.multi
    def _attach_invoices(self):
        # this module is computing payments not invoices, so search
        # for all user's invoices and do not attach invoices
        for slip in self:
            invoice_ids = slip.contract_id._comp_commission()
        return invoice_ids

    @api.multi
    def _attach_AMLs(self, invoices):
        # for each payment that dont have slip id of current employee;
        # add self.id to payment.slip_ids
        for slip in self:
            for inv in invoices:
                for payment in inv.payment_ids:
                    for aml in payment.move_line_ids:
                        if not aml.slip_ids:
                            aml.slip_ids += slip
                        else:
                            uids = []
                            for pslip in aml.slip_ids:
                                uids.append(pslip.employee_id.user_id.id)
                            if slip.employee_id.user_id.id in uids:
                                continue
                            else:
                                aml.slip_ids += slip

    @api.multi
    def compute_sheet(self):
        for payslip in self:
            payslip._detach_invoices()
            payslip._detach_AMLs()
            # No contract? forget about it
            if not payslip.contract_id:
                continue

            invoice_ids = payslip.contract_id._comp_commission()
            payslip._attach_AMLs(invoice_ids)

        res = super(HrPayslip, self).compute_sheet()
        return res


    @api.multi
    def action_payslip_done(self):
        for slip in self:
            res = super(HrPayslip, self).action_payslip_done()
            slip.contract_id._comp_commission()
        return res

    @api.multi
    def action_payslip_draft(self):
        for slip in self:
            slip.compute_sheet()
        return super(HrPayslip, self).action_payslip_draft()

    @api.multi
    def action_payslip_cancel(self):
        for slip in self:
            slip._detach_invoices()
            slip._detach_AMLs()
            slip.contract_id._comp_commission()
        return super(HrPayslip, self).action_payslip_cancel()


    @api.multi
    def unlink(self):
        for slip in self:
            slip._detach_invoices()
            slip._detach_AMLs()
            slip.contract_id._comp_commission()
        return super(HrPayslip, self).unlink()
