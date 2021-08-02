from odoo import api, fields, models, _


class Respartner(models.Model):
    _name = 'res.typepartner'
    _description = 'Partner'

    name = fields.Char(string=_("Partner Type"))



class ResPartnerIn(models.Model):
    _inherit = 'res.partner'

    type_id =  fields.Many2one('res.typepartner', string="type")
    is_customer = fields.Boolean (string= _("Is Customer"))
    is_vendor = fields.Boolean (string= _("Is Vendor"))
    is_employee = fields.Boolean (string= _("Is Employee"))
