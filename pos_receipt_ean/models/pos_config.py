# -*- coding: utf-8 -*-

from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    print_ean_ticket = fields.Boolean(string='Print EAN on Ticket')
