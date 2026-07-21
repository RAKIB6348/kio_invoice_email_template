# -*- coding: utf-8 -*-
# from odoo import http


# class KioInvoiceEmailTemplate(http.Controller):
#     @http.route('/kio_invoice_email_template/kio_invoice_email_template', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kio_invoice_email_template/kio_invoice_email_template/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kio_invoice_email_template.listing', {
#             'root': '/kio_invoice_email_template/kio_invoice_email_template',
#             'objects': http.request.env['kio_invoice_email_template.kio_invoice_email_template'].search([]),
#         })

#     @http.route('/kio_invoice_email_template/kio_invoice_email_template/objects/<model("kio_invoice_email_template.kio_invoice_email_template"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kio_invoice_email_template.object', {
#             'object': obj
#         })

