# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CustomAccountPaymentPo(models.Model):
    _inherit = 'account.move'
    _description = 'account print report'

    #

    def action_print_report(self):
        return self.env.ref('bi_print_journal_entries.journal_entry_report_id').report_action(self)

    def action_print_report_ar(self):
        return self.env.ref('bi_print_journal_entries.journal_entry_report_id_ar').report_action(self)

class CustomAccountPaymentPo(models.Model):
    _inherit = 'account.move.line'
    _description = 'account move line '

    name = fields.Char(string=_('Description'))
    # analytic_line_ids = fields.One2many('account.analytic.line', 'move_id', string='Analytic lines')
    analytic_account_id = fields.Many2one('account.analytic.account', string=_('Activities'), index=True)
    # analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')

