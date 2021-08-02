# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date

from odoo import _, api, fields, models , _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    cred_account_id = fields.Many2one('account.account', string="Accreditation Account Parent",        )
    cred_prefix = fields.Char( string="Prefix",        )
    cred_last_code = fields.Char( string="Last Code",        )
    property_account_income_categ_id = fields.Many2one('account.account', company_dependent=True,
                                                       string="Income Account",
                                                       domain="[ ('company_id', '=', current_company_id)]",
                                                       )

    property_valuation = fields.Selection([
        ('manual_periodic', 'Manual'),
        ('real_time', 'Automated')], string='Inventory Valuation',
        company_dependent=True, copy=True,
       )
    property_cost_method = fields.Selection([
        ('standard', 'Standard Price'),
        ('fifo', 'First In First Out (FIFO)'),
        ('average', 'Average Cost (AVCO)')], string="Costing Method",
        company_dependent=True, copy=True,
        )
    property_stock_journal = fields.Many2one(
        'account.journal', 'Stock Journal', company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0])]", check_company=True,
      )

    property_stock_account_output_categ_id = fields.Many2one(
        'account.account', 'Stock Output Account', company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0]), ]", check_company=True,
        )
    property_stock_valuation_account_id = fields.Many2one(
        'account.account', 'Stock Valuation Account', company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0]),  ]", check_company=True,
         )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        app_credit_account = self.cred_account_id and self.cred_account_id.id or False
        app_cred_prefix = self.cred_prefix or  False
        app_cred_last_code = self.cred_last_code or  False
        app_property_account_income_categ_id = self.property_account_income_categ_id and self.property_account_income_categ_id.id or False
        app_property_valuation = self.property_valuation or False
        app_property_cost_method= self.property_cost_method   or False
        app_property_stock_journal = self.property_stock_journal and self.property_stock_journal.id or False
        app_property_stock_account_output_categ_id = self.property_stock_account_output_categ_id and self.property_stock_account_output_categ_id.id or False
        app_property_stock_valuation_account_id = self.property_stock_valuation_account_id and self.property_stock_valuation_account_id.id or False

        # if  app_credit_account:
        ir_config.set_param("eq_invoice_from_picking.credit_account", app_credit_account)
        ir_config.set_param("eq_invoice_from_picking.cred_prefix", app_cred_prefix)
        ir_config.set_param("eq_invoice_from_picking.cred_last_code", app_cred_last_code)
        ir_config.set_param("eq_invoice_from_picking.property_account_income_categ_id", app_property_account_income_categ_id)
        ir_config.set_param("eq_invoice_from_picking.property_valuation", app_property_valuation)
        ir_config.set_param("eq_invoice_from_picking.property_cost_method", app_property_cost_method)
        ir_config.set_param("eq_invoice_from_picking.property_stock_journal", app_property_stock_journal)
        ir_config.set_param("eq_invoice_from_picking.property_stock_account_output_categ_id", app_property_stock_account_output_categ_id)
        ir_config.set_param("eq_invoice_from_picking.property_stock_valuation_account_id", app_property_stock_valuation_account_id)


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        app_credit_account =   ir_config.get_param('eq_invoice_from_picking.credit_account', )
        app_cred_prefix =   ir_config.get_param('eq_invoice_from_picking.cred_prefix', )
        app_cred_last_code =   ir_config.get_param('eq_invoice_from_picking.cred_last_code', )
        app_property_account_income_categ_id =   ir_config.get_param('eq_invoice_from_picking.property_account_income_categ_id', )
        app_property_valuation =   ir_config.get_param('eq_invoice_from_picking.property_valuation', )
        app_property_cost_method =   ir_config.get_param('eq_invoice_from_picking.property_cost_method', )
        app_property_stock_journal =   ir_config.get_param('eq_invoice_from_picking.property_stock_journal', )
        app_property_stock_account_output_categ_id =   ir_config.get_param('eq_invoice_from_picking.property_stock_account_output_categ_id', )
        app_property_stock_valuation_account_id =   ir_config.get_param('eq_invoice_from_picking.property_stock_valuation_account_id', )

        # print("get",app_cred_account_id)

        res.update(
            cred_account_id=int(app_credit_account),
            cred_prefix=(app_cred_prefix),
            cred_last_code=(app_cred_last_code),
            property_account_income_categ_id=int(app_property_account_income_categ_id),
            property_valuation= (app_property_valuation),
            property_cost_method= (app_property_cost_method),
            property_stock_journal=int(app_property_stock_journal),
            property_stock_account_output_categ_id=int(app_property_stock_account_output_categ_id),
            property_stock_valuation_account_id=int(app_property_stock_valuation_account_id),

        )
        return res
