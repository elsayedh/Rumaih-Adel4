# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models , _ , api
from odoo.exceptions import AccessError, UserError, ValidationError
# from odoo.tools import float_is_zero

class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    pos_image = fields.Image("PoS Image", attachment=True)
    
    receivable_account_id = fields.Many2one('account.account',
                                            string='Intermediary Account',
                                            required=True,ondelete='restrict',
                                            help='Account used as counterpart of the income account in the accounting entry representing the pos sales.')
    
    name = fields.Char(string="Payment Method1", required=True)

class ProductTemplatepos (models.Model):
    _inherit = "product.template"


    account_income_pos_categ_id = fields.Many2one('account.account', company_dependent=True,
        string="Income Account",
        domain="['&', ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
        help="Keep this field empty to use the default value from the product category.")

class ProductCategorypos(models.Model):
    _inherit = "product.category"

    account_income_pos_categ_id = fields.Many2one('account.account', company_dependent=True,
        string="Income Account POS",
        domain="['&', ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
        help="This account will be used when validating a customer invoice.")
        
        
class PossessionMethod(models.Model):
    _inherit = "pos.session"
    
    #
    # def _prepare_line(self, order_line):
    #     """ Derive from order_line the order date, income account, amount and taxes information.
    #     product.with_context(force_company=order_line.company_id.id).property_account_income_id or
    #     These information will be used in accumulating the amounts for sales and tax lines.
    #     """
    #     def get_income_account(order_line):
    #         product = order_line.product_id
    #         # income_account =  product.categ_id.with_context(force_company=order_line.company_id.id).account_income_pos_categ_id
    #         income_account = product.with_context(force_company=order_line.company_id.id).account_income_pos_categ_id or product.categ_id.with_context(force_company=order_line.company_id.id).account_income_pos_categ_id
    #
    #         if not income_account:
    #             raise UserError(_('Please define income account for this product: "%s" (id:%d).')
    #                             % (product.name, product.id))
    #         print(income_account.name, income_account.id)
    #         return order_line.order_id.fiscal_position_id.map_account(income_account)
    #
    #     tax_ids = order_line.tax_ids_after_fiscal_position\
    #                 .filtered(lambda t: t.company_id.id == order_line.order_id.company_id.id)
    #     price = order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0)
    #     taxes = tax_ids.compute_all(price_unit=price, quantity=order_line.qty, currency=self.currency_id, is_refund=order_line.qty<0).get('taxes', [])
    #     date_order = order_line.order_id.date_order
    #     taxes = [{'date_order': date_order, **tax} for tax in taxes]
    #     return {
    #         'date_order': order_line.order_id.date_order,
    #         'income_account_id': get_income_account(order_line).id,
    #         'amount': order_line.price_subtotal,
    #         'taxes': taxes,
    #     }
    #
    def _prepare_line(self, order_line):
        """ Derive from order_line the order date, income account, amount and taxes information.

        These information will be used in accumulating the amounts for sales and tax lines.
        """
        def get_income_account(order_line):
            product = order_line.product_id
            income_account = product.with_context(force_company=order_line.company_id.id).account_income_pos_categ_id or product.categ_id.with_context(force_company=order_line.company_id.id).account_income_pos_categ_id
            if not income_account:
                raise UserError(_('Please define income account for this product: "%s" (id:%d).')
                                % (product.name, product.id))
            return order_line.order_id.fiscal_position_id.map_account(income_account)

        tax_ids = order_line.tax_ids_after_fiscal_position\
                    .filtered(lambda t: t.company_id.id == order_line.order_id.company_id.id)
        sign = -1 if order_line.qty >= 0 else 1
        price = sign * order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0)
        # The 'is_refund' parameter is used to compute the tax tags. Ultimately, the tags are part
        # of the key used for summing taxes. Since the POS UI doesn't support the tags, inconsistencies
        # may arise in 'Round Globally'.
        check_refund = lambda x: x.qty * x.price_unit < 0
        if self.company_id.tax_calculation_rounding_method == 'round_globally':
            is_refund = all(check_refund(line) for line in order_line.order_id.lines)
        else:
            is_refund = check_refund(order_line)
        tax_data = tax_ids.compute_all(price_unit=price, quantity=abs(order_line.qty), currency=self.currency_id, is_refund=is_refund)
        taxes = tax_data['taxes']
        # For Cash based taxes, use the account from the repartition line immediately as it has been paid already
        for tax in taxes:
            tax_rep = self.env['account.tax.repartition.line'].browse(tax['tax_repartition_line_id'])
            tax['account_id'] = tax_rep.account_id.id
        date_order = order_line.order_id.date_order
        taxes = [{'date_order': date_order, **tax} for tax in taxes]
        return {
            'date_order': order_line.order_id.date_order,
            'income_account_id': get_income_account(order_line).id,
            'amount': order_line.price_subtotal,
            'taxes': taxes,
            'base_tags': tuple(tax_data['base_tags']),
        }
