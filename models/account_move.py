from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    grn_reference = fields.Char(
        string="GRN Reference",
        required=True,
        copy=False,
        readonly=True,
        index="trigram",
        default=lambda self: _("New"),
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("grn_reference", _("New")) == _("New"):
                vals["grn_reference"] = self.env["ir.sequence"].next_by_code(
                    "account.move.grn.reference"
                ) or _("New")
        return super().create(vals_list)

    def _get_mail_template(self):
        if self and all(move.move_type == 'out_invoice' for move in self):
            template = self.env.ref(
                'kio_invoice_email_template.mail_template_customer_invoice_samaa',
                raise_if_not_found=False,
            )
            if template:
                return 'kio_invoice_email_template.mail_template_customer_invoice_samaa'
        return super()._get_mail_template()
