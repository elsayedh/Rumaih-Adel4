# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PurchaseConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    create_bill_for_is = fields.Boolean(string="Auto Create Bill From Shipment?", default=lambda self: self.env.user.company_id.create_bill_for_is)
    validate_bill = fields.Boolean(string='Auto Validate Supplier Bills?', default=lambda self: self.env.user.company_id.validate_bill)

    
    def get_values(self):
        res = super(PurchaseConfigSettings, self).get_values()
        res.update(
            create_bill_for_is = self.env.user.company_id.create_bill_for_is,
            validate_bill = self.env.user.company_id.validate_bill,
        )
        return res

    def set_values(self):
        super(PurchaseConfigSettings, self).set_values()
        company_id=self.env.user.company_id
        company_id.create_bill_for_is = self.create_bill_for_is
        company_id.validate_bill = self.validate_bill