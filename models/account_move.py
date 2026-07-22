import re

from odoo import api, fields, models, _


GRN_SEQUENCE_CODE = "account.move.grn.reference"
GRN_REFERENCE_PATTERN = r"^\s*GRN\s*0*([0-9]+)\s*$"
GRN_MOVE_TYPES = ("out_invoice",)


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
        needs_grn_reference = any(
            self._vals_needs_grn_sequence(vals)
            for vals in vals_list
        )
        if needs_grn_reference:
            self._sync_grn_sequence_with_existing_references(allow_rewind=False)

        for vals in vals_list:
            if self._vals_needs_grn_sequence(vals):
                vals["grn_reference"] = (
                    self.env["ir.sequence"].next_by_code(GRN_SEQUENCE_CODE) or _("New")
                )
        return super().create(vals_list)

    @api.model
    def _vals_needs_grn_sequence(self, vals):
        move_type = (
            vals.get("move_type")
            or self.env.context.get("default_move_type")
            or "entry"
        )
        return (
            move_type in GRN_MOVE_TYPES
            and self._is_missing_grn_reference(vals.get("grn_reference", _("New")))
        )

    @api.model
    def _is_missing_grn_reference(self, grn_reference):
        return not grn_reference or grn_reference.strip() == _("New")

    @api.model
    def _parse_grn_reference_number(self, grn_reference):
        match = re.match(GRN_REFERENCE_PATTERN, grn_reference or "")
        return int(match.group(1)) if match else False

    @api.model
    def _get_grn_sequence(self):
        return self.env["ir.sequence"].sudo().search(
            [
                ("code", "=", GRN_SEQUENCE_CODE),
                ("company_id", "in", [self.env.company.id, False]),
            ],
            order="company_id",
            limit=1,
        )

    @api.model
    def _get_grn_invoice_domain(self):
        return [("move_type", "in", GRN_MOVE_TYPES)]

    @api.model
    def _get_next_available_grn_number(self, used_numbers, start=1):
        number = start
        while number in used_numbers:
            number += 1
        return number

    @api.model
    def _backfill_missing_grn_references(self):
        sequence = self._get_grn_sequence()
        if not sequence:
            return False

        invoices = self.sudo().search(
            self._get_grn_invoice_domain(),
            order="invoice_date, name, id",
        )
        grn_numbers_by_id = {}
        grn_number_counts = {}
        for invoice in invoices:
            number = self._parse_grn_reference_number(invoice.grn_reference)
            if number:
                grn_numbers_by_id[invoice.id] = number
                grn_number_counts[number] = grn_number_counts.get(number, 0) + 1

        has_duplicates = any(count > 1 for count in grn_number_counts.values())
        if has_duplicates:
            next_number = 1
            for invoice in invoices:
                invoice.write({"grn_reference": sequence.get_next_char(next_number)})
                next_number += 1
            return True

        used_numbers = set(grn_numbers_by_id.values())
        next_number = 1
        for invoice in invoices:
            if grn_numbers_by_id.get(invoice.id):
                continue
            if not self._is_missing_grn_reference(invoice.grn_reference):
                continue
            next_number = self._get_next_available_grn_number(used_numbers, next_number)
            invoice.write({"grn_reference": sequence.get_next_char(next_number)})
            used_numbers.add(next_number)
        return True

    @api.model
    def _get_highest_grn_reference_number(self):
        self.flush_model(["grn_reference", "move_type"])
        self.env.cr.execute(
            """
            WITH matched AS (
                SELECT regexp_match(grn_reference, %s) AS match
                  FROM account_move
                 WHERE grn_reference IS NOT NULL
                   AND move_type IN %s
            )
            SELECT COALESCE(MAX((match)[1]::integer), 0)
              FROM matched
             WHERE match IS NOT NULL
            """,
            [GRN_REFERENCE_PATTERN, GRN_MOVE_TYPES],
        )
        return self.env.cr.fetchone()[0]

    @api.model
    def _sync_grn_sequence_with_existing_references(self, allow_rewind=False):
        sequence = self._get_grn_sequence()
        if not sequence:
            return False

        next_number = (
            self._get_highest_grn_reference_number()
            + (sequence.number_increment or 1)
        )
        current_sequence = sequence._get_current_sequence()
        current_next = current_sequence.number_next_actual

        if current_next < next_number or (allow_rewind and current_next != next_number):
            current_sequence.sudo().write({"number_next": next_number})
        return True

    @api.model
    def _backfill_and_sync_grn_references(self):
        self._backfill_missing_grn_references()
        return self._sync_grn_sequence_with_existing_references(allow_rewind=True)

    def _get_mail_template(self):
        if self and all(move.move_type == 'out_invoice' for move in self):
            template = self.env.ref(
                'kio_invoice_email_template.mail_template_customer_invoice_samaa',
                raise_if_not_found=False,
            )
            if template:
                return 'kio_invoice_email_template.mail_template_customer_invoice_samaa'
        return super()._get_mail_template()
