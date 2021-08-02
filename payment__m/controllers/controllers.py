# -*- coding: utf-8 -*-
# from odoo import http


# class PaymentM(http.Controller):
#     @http.route('/payment__m/payment__m/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payment__m/payment__m/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payment__m.listing', {
#             'root': '/payment__m/payment__m',
#             'objects': http.request.env['payment__m.payment__m'].search([]),
#         })

#     @http.route('/payment__m/payment__m/objects/<model("payment__m.payment__m"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payment__m.object', {
#             'object': obj
#         })
