# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CustomAccountPaymentPo(models.Model):
    _inherit = 'account.payment'
    _description = 'account payment Custom'

    #

    choose_po = fields.Many2one("purchase.order", string="Choose Po", tracking=True,
                                domain=[('state', '=', 'purchase')] )


class CustomAccountPaymentPopurchase(models.Model):
    _inherit = 'purchase.order'
    _description = 'account purhase Custom'

    child_ids = fields.One2many('account.payment', 'choose_po', 'Child Accounts')