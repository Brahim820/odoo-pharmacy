# -*- coding: utf-8 -*-

from odoo import _, api, exceptions, fields, models
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    jrnl_is_cheque = fields.Boolean(string="Cheques?",
    help="On Cash/Misc journals this will be a Cheques wallet. \n\
    On Bank accounts, this will mean that you have Chequebook from this bank." )


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    aml_is_cheque = fields.Boolean(string="Is Cheque", store=True, compute="_is_cheque")
    cheque_bank = fields.Char(string="Cheque Bank",related='payment_id.cheque_bank')
    cheque_date = fields.Date(string="Cheque Date",related='payment_id.date')
    cheque_no = fields.Char(string="Cheque No",related='payment_id.cheque_no')

    @api.depends('payment_id')
    def _is_cheque(self):
        for aml in self:
            aml.aml_is_cheque = aml.payment_id.is_cheque

    # @api.model
    # def create(self, vals):
    #     res = super(AccountMoveLine, self).create(vals)
    #     for aml in res:
    #         if not aml.aml_is_cheque:
    #             aml.aml_is_cheque = aml.journal_id.jrnl_is_cheque
    #     return res

    def _prepare_writeoff_first_line_values(self, values):
        line_values = super(AccountMoveLine, self)._prepare_writeoff_first_line_values(values)
        line_values.update({
        'payment_id': self.payment_id.id,
        'amount_currency': -abs(self.amount_currency) if line_values['credit'] > 0 else abs(self.amount_currency),
        'currency_id': self.currency_id.id and self.currency_id.id,
        })
        return line_values

    def _prepare_writeoff_second_line_values(self, values):
        line_values = super(AccountMoveLine, self)._prepare_writeoff_second_line_values(values)
        line_values.update({
        'payment_id': self.payment_id.id,
        'amount_currency': -abs(self.amount_currency) if line_values['credit'] > 0 else abs(self.amount_currency),
        'currency_id': self.currency_id.id and self.currency_id.id,
        })
        return line_values


class AccountPayment(models.Model):
    _inherit = "account.payment"
    communication = fields.Char(string="Payment Reference", )

    cheque_no = fields.Char(string="Cheque No")
    cheque_bank = fields.Char(string="Cheque Bank")
    date = fields.Date(string="Date" )
    cheque_journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
    )
    is_cheque = fields.Boolean(string="Is Cheque", )

    _sql_constraints = [
        ('chq_no_uniq', 'unique (cheque_no)', 'The cheque number must be unique.!'),
    ]

    @api.depends('cheque_journal_id')
    @api.onchange('cheque_journal_id','currency_id')
    def _change_journal(self):
        for pay in self:
            if pay.cheque_journal_id:
                pay.journal_id = pay.cheque_journal_id
            pay.currency_id = pay.journal_id.currency_id or pay.company_id.currency_id
