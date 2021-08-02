# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class PoSPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    receivable_account_id = fields.Many2one('account.account',
                                            string='Intermediary Account',
                                            required=True,
                                            # domain=[('reconcile', '=', True), ('user_type_id.type', '=', 'receivable')],
                                            default=lambda
                                                self: self.env.company.account_default_pos_receivable_account_id,
                                            ondelete='restrict',
                                            help='Account used as counterpart of the income account in the accounting entry representing the pos sales.')

# class payment__m(models.Model):
#     _name = 'payment__m.payment__m'
#     _description = 'payment__m.payment__m'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
