def post_init_hook(env):
    env['account.move']._backfill_and_sync_grn_references()
