from odoo import models, fields, api
import json

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_done(self):
        res = super(StockPicking, self).action_done()
        # self.ensure_one()
        print("WHy2", self.state)
        print("WHy2",self.purchase_id)
        print("WHy2", self.company_id.create_bill_for_is)
        print("WHy2", self.picking_type_code)
        for rec in self.move_ids_without_package:
            print("q",rec.quantity_done)

        if self.state == 'done' and self.purchase_id and self.company_id.create_bill_for_is and self.picking_type_code == 'incoming':
            print(fields.date.today())
            myjournal_id = self.env['account.journal'].search([('type', '=', 'purchase')],limit=1)
            data = {
                'type': 'in_invoice',
                'partner_id': self.purchase_id.partner_id.id or False,
                'purchase_id': self.purchase_id.id or False,
                'invoice_origin': self.purchase_id.name or '',
                # 'ref' : self.purchase_id.name or '',
                'invoice_date': str(fields.date.today()),
                'invoice_date_due': self.purchase_id.date_planned and str(self.purchase_id.date_planned) or  self.purchase_id.date_order and str(self.purchase_id.date_order) or fields.datetime.now(),
                'currency_id': self.purchase_id.currency_id.id or False,
                'company_id': self.purchase_id.company_id.id or False,
                'narration': self.purchase_id.notes or '',
                'journal_id' :myjournal_id.id,
                'invoice_line_ids': [(0, 0, {
                                             'product_id': line.product_id.id or False,
                                             'name': line.name or '',
                                             # 'account_analytic_id': line.account_analytic_id.id or False,
                                             'quantity': self.move_lines.filtered(lambda mv: mv.product_id.id == line.product_id.id) and self.move_lines.filtered(lambda mv: mv.product_id.id == line.product_id.id)[0].product_uom_qty,
                                             'price_unit': line.price_unit,
                                             'product_uom_id': line.product_uom.id or False,
                                             'tax_ids': [(6, 0, line.taxes_id.ids)],
                                             'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                                             'account_id': line.product_id.categ_id.property_account_expense_categ_id.id or self.env['account.account'].search([('name','=','Expenses')],limit=1).id,
                                          }) for line in self.purchase_id.order_line],
            }


            # print("hjh",self.env['account.move'].default_get(['journal_id','reference_type']))
            # data.update(self.env['account.move'].default_get(['journal_id','reference_type']))
            print("shaliby solofan ",data)
            vendor_bill = self.env['account.move'].sudo().create(data)
            for line in self.purchase_id.order_line:
                line.write({'invoice_lines': [(4, inl.id) for inl in vendor_bill.invoice_line_ids]})
            if self.company_id.validate_bill:
                vendor_bill.action_post()

            # action = self.env.ref('account.action_invoice_tree2').read()[0]
            # action['res_id'] = vendor_bill.id
            # action['views'] = [(self.env.ref('account.invoice_supplier_form').id,'form')]
            # return action
        else:
            return res

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        res = super(AccountMove, self).action_post()
        print (self.invoice_outstanding_credits_debits_widget)
        info=json.loads(self.invoice_outstanding_credits_debits_widget)
        # print("hi",info["content"])

        # po=self.invoice_origin
        # mypo=self.env['purchase.order'].search([('name','=',po)],limit=1)
        # mypayment =self.env['purchase.order'].search([('name','=',po)],limit=1)
        for rec in info["content"] :
            print(rec)
            if rec["id"]:
                self.js_assign_outstanding_line(rec["id"])
                if self.invoice_payment_state =='paid':
                    break
        # line_id=1705

        # self.js_assign_outstanding_line( 1705)

        return res
