# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ExpensesResBranch(models.Model):
    _name = 'res.branch.expense'
    _description = 'Branch expense'

    account_expense_debit_id = fields.Many2one('account.account', company_dependent=True,
                                               string=_("Account Debit"),
                                               domain="[ ('company_id', '=', current_company_id)]",
                                               )
    journal_id = fields.Many2one('account.journal', string="Journal", required=True,  )



    name =  fields.Char(string =_("Expense Name ")  )

    @api.depends('name')
    def name_get(self):
        # print("hi", self.env.lang)
        res = []
        for record in self:
            name = record.name
            # print("name", record.name)
            res.append((record.id, name))
        return res


class ResBranch(models.Model):
    _name = 'res.branch'
    _description = 'Branch'

    name = fields.Char(required=True)
    company_id = fields.Many2one('res.company', required=True)
    telephone = fields.Char(string='Telephone No')
    address = fields.Text('Address')
    # haytham addition
    account_expense_debit_id = fields.Many2many('res.branch.expense',
                                                       string=_("Account Debit"),

                                                       )
    account_expense_credit_id = fields.Many2one('account.account', company_dependent=True,
                                               string=_("Account Credit"),
                                               domain="[ ('company_id', '=', current_company_id)]",
                                               )


    account_bank_debit_id = fields.Many2one('account.account', company_dependent=True,
                                                       string=_("Bank Account Debit"),
                                                       domain="[ ('company_id', '=', current_company_id)]",
                                                       )
    account_bank_credit_id = fields.Many2one('account.account', company_dependent=True,
                                               string=_("Bank Account Credit"),
                                               domain="[ ('company_id', '=', current_company_id)]",
                                               )