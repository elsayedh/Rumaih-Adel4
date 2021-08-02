# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CustomAccountPaymentPo(models.Model):
    _inherit = 'account.payment'
    _description = 'account payment Custom'

    @api.onchange('partner_id')
    def _campus_onchange(self):
        list = []
        for rec in self.partner_id.child_ids:
            list.append(rec.id)
        # self.test5=list
        return {'domain': {'list_contacts': [('id', '=', list)]}}

    choose_po = fields.Many2one(comodel_name="purchase.order", string="Choose Po", required=True,
                                domain=[('state', '=', 'purchase')])
