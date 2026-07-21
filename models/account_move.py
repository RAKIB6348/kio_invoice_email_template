# -*- coding: utf-8 -*-

from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_mail_template(self):
        if self and all(move.move_type == 'out_invoice' for move in self):
            template = self.env.ref(
                'kio_invoice_email_template.mail_template_customer_invoice_samaa',
                raise_if_not_found=False,
            )
            if template:
                return 'kio_invoice_email_template.mail_template_customer_invoice_samaa'
        return super()._get_mail_template()
