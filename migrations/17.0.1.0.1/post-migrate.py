from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    action = env.ref(
        'kio_invoice_email_template.action_resequence_grn_references',
        raise_if_not_found=False,
    )
    if action:
        action.unlink()
    env['account.move']._backfill_and_sync_grn_references()
