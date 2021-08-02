from odoo import api, fields, models
class ResCompany(models.Model):
    _inherit = "res.company"


    create_bill_for_is=fields.Boolean(string='Auto Create Bill From Shipment?')
    validate_bill = fields.Boolean(string='Auto Validate Supplier Bills?')