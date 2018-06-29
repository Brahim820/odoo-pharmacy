# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# © 2017 Mohamed M. Hagag (DVIT.ME) <mohamedhagag1981@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).



from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class HrContract(models.Model):
    _inherit = 'hr.contract'
    commission = fields.Float(string='Commission',
                              compute='_comp_commission', store=True)
    comm_rate = fields.Float(string='Commissions Rate',
                             digits=dp.get_precision('Payroll Rate'), store=True)
    comm_type = fields.Selection(string='Commission Type',
        selection=[('all','All Sales'),('team','Team Sales'),('own','Own sales')],
        default='own',
        help='Sales = His sales only; Team = His team sales only; All = On all sales')

    # @api.multi
    # @api.depends('employee_id','employee_id.payslip_count')
    @api.onchange('comm_type','employee_id')
    def _comp_commission(self):
        for contract in self:
            invoice_ids = []
            comm_type = contract.comm_type
            contract.commission = 0
            invoice_obj = self.env['account.invoice']

            if comm_type == 'own':
                own_invoices = invoice_obj.search([
                    ('state', 'in', ('open', 'paid')),
                    ('user_id', '=', contract.employee_id.user_id.id),
                    ('type', '=', 'out_invoice'),
                ])
                for inv in own_invoices:
                    if inv.payment_ids and not inv.slip_ids:
                            invoice_ids.append(inv)
                    else:
                        uids = []
                        for payment in inv.payment_ids:
                            for aml in payment.move_line_ids:
                                uids.append([s.employee_id.user_id.id for s in aml.slip_ids])
                        if contract.employee_id.user_id.id not in uids:
                            invoice_ids.append(inv)

            elif comm_type == 'team':
                team_obj = self.env['crm.team']
                team_ids = team_obj.search(['|',
                    ('user_id','=',contract.employee_id.user_id.id),
                    ('member_ids','child_of', contract.employee_id.user_id.id)])
                # print "------ team_ids= "+ str(team_ids) + " --------"
                team_invoices = invoice_obj.search([
                    ('state', 'in', ('open', 'paid')),
                    ('type', '=', 'out_invoice'),
                    ('team_id', 'in', [t.id for t in team_ids]),
                    ('date_invoice', '>=', contract.date_start),
                    ])

                for inv in team_invoices:
                    # if inv.team_id in team_ids:
                    if inv.payment_ids and not inv.slip_ids:
                            invoice_ids.append(inv)
                    else:
                        uids = []
                        for payment in inv.payment_ids:
                            for aml in payment.move_line_ids:
                                uids.append([s.employee_id.user_id.id for s in aml.slip_ids])
                        if contract.employee_id.user_id.id not in uids:
                            invoice_ids.append(inv)

            else: #comm_type = all
                all_invoices = invoice_obj.search([
                    ('state', 'in', ('open', 'paid')),
                    ('type', '=', 'out_invoice'),
                    ('date_invoice', '>=', contract.date_start),
                    ])
                for inv in all_invoices:
                    if inv.payment_ids and not inv.slip_ids:
                            invoice_ids.append(inv)
                    else:
                        uids = []
                        for payment in inv.payment_ids:
                            for aml in payment.move_line_ids:
                                uids.append([s.employee_id.user_id.id for s in aml.slip_ids])
                        if contract.employee_id.user_id.id not in uids:
                            invoice_ids.append(inv)

            commission = 0
            for inv in invoice_ids:
                for payment in inv.payment_ids:
                    for aml in payment.move_line_ids:
                        if not aml.slip_ids:
                            # commission += payment.amount
                            commission += aml.credit
                        else:
                            uids = []
                            for pslip in aml.slip_ids:
                                uids.append(pslip.employee_id.user_id.id)
                            if contract.employee_id.user_id.id not in uids:
                                commission += aml.credit

            contract.commission = commission
            return invoice_ids
