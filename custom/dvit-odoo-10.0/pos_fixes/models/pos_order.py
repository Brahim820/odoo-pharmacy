from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = "pos.order"

    '''This code will complete the anglo-saxon STJ entries
        in COGS / Stock accounts per order'''

    @api.multi
    def pos_fixes(self, ids):
        move_line_obj = self.env['account.move.line']
        for order in self.browse(ids):
            if order.state == 'invoiced' or order.invoice_id:
                continue

            company_id = order.company_id.id
            session = order.session_id
            move = self._create_account_move(session.start_at,
                                                 order.name,
                                                 int(session.config_id.journal_id.id),
                                                 company_id,
                                                 )
            amount_total = order.amount_total

            for line in order.lines:
                # Process normal products
                if line.product_id.type != 'service' and \
                        line.product_id.categ_id.property_valuation == 'real_time':

                    amount = 0
                    stkacc = line.product_id.categ_id.property_stock_account_output_categ_id and \
                        line.product_id.categ_id.property_stock_account_output_categ_id
                    cogacc = line.product_id.property_account_expense_id and \
                        line.product_id.property_account_expense_id
                    if not cogacc:
                        cogacc = line.product_id.categ_id.property_account_expense_categ_id and \
                            line.product_id.categ_id.property_account_expense_categ_id
                    amount = line.qty * line.product_id.standard_price

                    line_vals = {
                        'name': line.product_id.name,
                        'move_id': move.id,
                        'journal_id': move.journal_id.id,
                        'date': move.date,
                        'product_id': line.product_id.id,
                        'partner_id': order.partner_id and order.partner_id.id or False,
                        'quantity': line.qty,
                        'ref': line.name
                    }
                    # create move.lines to credit stock and debit cogs
                    caml = {
                        'account_id': stkacc.id,
                        'credit': amount_total > 0 and amount or 0.0,
                        'debit': amount_total < 0 and -amount or 0.0,
                    }
                    caml.update(line_vals)
                    daml = {
                        'account_id': cogacc.id,
                        'debit': amount_total > 0 and amount or 0.0,
                        'credit': amount_total < 0 and -amount or 0.0,
                    }
                    daml.update(line_vals)

                    move_line_obj.with_context(check_move_validity=False).create(caml)
                    move_line_obj.with_context(check_move_validity=False).create(daml)

                # Process product_pack separately
                if hasattr(line.product_id, 'pack') and line.product_id.pack:
                    for pack_line in line.product_id.pack_line_ids.filtered(lambda l: \
                        l.product_id.categ_id.property_valuation == 'real_time' and \
                            l.product_id.type != 'service'):
                        amount = 0
                        stkacc = pack_line.product_id.categ_id.property_stock_account_output_categ_id and \
                            pack_line.product_id.categ_id.property_stock_account_output_categ_id
                        # cost of goods account cogacc
                        cogacc = pack_line.product_id.property_account_expense_id and \
                            pack_line.product_id.property_account_expense_id or \
                            pack_line.product_id.categ_id.property_account_expense_categ_id

                        if cogacc and stkacc:
                            amount = line.qty * pack_line.quantity * pack_line.product_id.standard_price
                            name = str(line.qty) + 'x' + line.product_id.name + ' > ' + \
                                str(pack_line.quantity * line.qty) + 'x' + pack_line.product_id.name
                            line_vals = {
                                'name': name,
                                'move_id': move.id,
                                'journal_id': move.journal_id.id,
                                'date': move.date,
                                'product_id': pack_line.product_id.id,
                                'partner_id': order.partner_id and order.partner_id.id or False,
                                'quantity': pack_line.quantity * line.qty,
                                'ref': line.name,
                            }

                            # create move.lines to credit stock and debit cogs
                            caml = {
                                'account_id': stkacc.id,
                                'credit': amount_total > 0 and amount or 0.0,
                                'debit': amount_total < 0 and -amount or 0.0,
                            }
                            caml.update(line_vals)
                            daml = {
                                'account_id': cogacc.id,
                                'debit': amount_total > 0 and amount or 0.0,
                                'credit': amount_total < 0 and -amount or 0.0,
                            }
                            daml.update(line_vals)

                            # #TODO if the pack itself is a service POS will not
                            # # create stock entries at all for its components so we
                            # # need to process it
                            # valacc = pack_line.product_id.categ_id.property_stock_valuation_account_id
                            # val_journal = self.env['account.journal'].search([('type','=','misc')])
                            #
                            # valuation_lines={
                            # 'name': name,
                            # 'move_id': move.id,
                            # 'journal_id': move.journal_id.id,
                            # 'date': move.date,
                            # 'product_id': pack_line.product_id.id,
                            # 'partner_id': order.partner_id and order.partner_id.id or False,
                            # 'quantity': pack_line.quantity * line.qty,
                            # 'ref': line.name,
                            # }
                            #
                            # # create stock valuation entries cr. inventory dr. goods shipped not invoiced
                            # vcaml = {
                            #     'account_id': valacc.id,
                            #     'credit': amount_total > 0 and amount or 0.0,
                            #     'debit': amount_total < 0 and -amount or 0.0,
                            # }
                            # vcaml.update(line_vals)
                            #
                            # vdaml = {
                            #     'account_id': stkacc.id,
                            #     'debit': amount_total > 0 and amount or 0.0,
                            #     'credit': amount_total < 0 and -amount or 0.0,
                            # }
                            # vdaml.update(line_vals)
                            # # FIXME: Below should go in the stock journal
                            # move_line_obj.with_context(check_move_validity=False).create(vcaml)
                            # move_line_obj.with_context(check_move_validity=False).create(vdaml)

                            move_line_obj.with_context(check_move_validity=False).create(caml)
                            move_line_obj.with_context(check_move_validity=False).create(daml)

                move.sudo().post()

        return True

    @api.model
    def create_from_ui(self, orders):
        o_ids = super(PosOrder, self).create_from_ui(orders)
        self.pos_fixes(o_ids)
        return o_ids

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
