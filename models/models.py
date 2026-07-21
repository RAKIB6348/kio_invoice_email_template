# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class kio_invoice_email_template(models.Model):
#     _name = 'kio_invoice_email_template.kio_invoice_email_template'
#     _description = 'kio_invoice_email_template.kio_invoice_email_template'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

