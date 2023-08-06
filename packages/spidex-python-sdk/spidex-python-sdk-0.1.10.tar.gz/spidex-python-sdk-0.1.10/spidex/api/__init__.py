from spidex.request_client import Client
from spidex.constants import API_HOST_URL


class SpidexClient(Client):
    def __init__(self, key=None, secret=None, phrase=None, wallet_secret=None, **kwargs):
        if "host" not in kwargs:
            kwargs["host"] = API_HOST_URL
        super().__init__(key, secret, phrase,  wallet_secret, **kwargs)

    from spidex.api.public import get_depth
    from spidex.api.public import get_kline
    from spidex.api.public import get_latest_trades
    from spidex.api.public import get_market
    from spidex.api.public import get_pool_info
    from spidex.api.public import get_specs
    from spidex.api.public import get_pool_detail
    from spidex.api.public import get_pool_income
    from spidex.api.public import get_pool_trades
    from spidex.api.public import get_pool_deposits
    from spidex.api.public import get_pool_withdraws
    from spidex.api.public import get_pool_shares
    from spidex.api.public import get_pool_user_share

    from spidex.api.private import onboarding
    from spidex.api.private import delete_api_key
    from spidex.api.private import create_api_key
    from spidex.api.private import order
    from spidex.api.private import deposit_to_pool
    from spidex.api.private import deposit_margin
    from spidex.api.private import cancel_order
    from spidex.api.private import get_orders
    from spidex.api.private import get_position
    from spidex.api.private import withdraw_margin
    from spidex.api.private import get_trades
    from spidex.api.private import get_transfers
    from spidex.api.private import get_account

