from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ResPartnerIn(models.Model):
    _inherit = 'purchase.order'

    account_expense_categ_id = fields.Many2one('account.account', string="Expense Account",
                                                        domain="[('company_id', '=', current_company_id)]", )
    stock_account_input_categ_id = fields.Many2one(
        'account.account', 'Stock Input Account',
        domain="[('company_id', '=', allowed_company_ids[0]),]", )


    def create_accredition(self):
        if not self.partner_ref:
            param=  self.env['ir.config_parameter'].sudo()
            account_parent_id=param.get_param('eq_invoice_from_picking.credit_account')
            cred_prefix=param.get_param('eq_invoice_from_picking.cred_prefix')
            cred_last_code=param.get_param('eq_invoice_from_picking.cred_last_code')
            parent_account=self.env['account.account'].sudo().search([('id','=',account_parent_id)])
            account_ids = self.env['account.account'].sudo().search([('parent_id','=',account_parent_id)])
            print("acc",parent_account.code)
            print("acc",parent_account.user_type_id)
            print("acc",parent_account.parent_id)
            print("acc",parent_account.group_id)
            print("acc",parent_account.company_id)
            if  cred_last_code:
                acc_code=int(cred_last_code)+1

                num=str(acc_code-int(parent_account.code) )
                num=num.zfill(4)
                self.partner_ref = cred_prefix+"/"+(num)
                vals = {}
                code=acc_code
                vals["code"] = code
                vals["user_type_id"] = parent_account.user_type_id.id
                vals["name"] = parent_account.name + cred_prefix + "/" + (num)
                vals["parent_id"] = parent_account.id
                vals["group_id"] = parent_account.group_id.id or False
                vals["company_id"] = parent_account.company_id.id or False
                print(vals)
                new_account = self.env['account.account'].sudo().search([('code', '=', code)])
                if not new_account:
                     mynewaccount=self.env['account.account'].sudo().create(vals)
                     param.set_param('eq_invoice_from_picking.cred_last_code', acc_code)
                     self.account_expense_categ_id=mynewaccount.id
                     self.stock_account_input_categ_id=mynewaccount.id
            else:
               raise UserError(_("need to config las code"))
        else:
            raise UserError(_("Vendor Reference not Empty"))

    @api.model
    def create(self, vals):
        vals['account_expense_categ_id'] = False
        vals['stock_account_input_categ_id'] = False
        vals['partner_ref'] = ''

        res = super(ResPartnerIn, self).create(vals)
        return res

    @api.onchange('partner_id')
    def on_change_partner_id2(self):
        """Contact number details should be change based on partner."""
        if self.partner_id:
            self.category_id = self.partner_id.category_id
            if self.partner_id.category_id:
                print( self.partner_id.category_id)
                self.onecategory_id = self.partner_id.category_id[0].id

    @api.depends('category_id')
    def _getfirst_category(self):
        if self.category_id:
            print( self.category_id[0])
            self.onecategory_id =  self.category_id[0]



    def _default_category(self):
        return self.env['res.partner.category'].browse(self._context.get('category_id'))

    category_id = fields.Many2many('res.partner.category', column1='partner_id',
                                   column2='category_id', string=_('Tags'), default=_default_category)
    onecategory_id=fields.Many2one ('res.partner.category', string=_('Tags'),copmute="_getfirst_category")

