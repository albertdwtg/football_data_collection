import sys
import os

sys.path.append(os.path.abspath("../src"))
from clients.binance import BinanceApi
from utils.secrets import get_secret
from utils.constants import (PROJECT_ID, 
    SECRET_KEY_SECRET_ID, API_KEY_SECRET_ID,
    QUOTE_ASSET, COINS_TO_TRADE, PROJECT_ENV)

SECRET_KEY = get_secret(
            project_id=PROJECT_ID, 
            secret_id=SECRET_KEY_SECRET_ID
        )
API_KEY = get_secret(
    project_id=PROJECT_ID, 
    secret_id=API_KEY_SECRET_ID
)
BINANCE_CLIENT = BinanceApi(
            api_key=API_KEY,
            secret_key=SECRET_KEY,
            quote_asset=QUOTE_ASSET,
            coins_to_trade=COINS_TO_TRADE[PROJECT_ENV.upper()]
        )

class TestClassBinanceApi:
    def test_init(self):
        assert BINANCE_CLIENT.quote_asset == QUOTE_ASSET.upper()
        assert BINANCE_CLIENT.coins_to_trade == COINS_TO_TRADE[PROJECT_ENV.upper()] or None
        assert isinstance(BINANCE_CLIENT.symbols_to_trade, list)
        for symbol in BINANCE_CLIENT.symbols_to_trade:
            assert isinstance(symbol, str)
            assert symbol.endswith(QUOTE_ASSET.upper())
        assert BINANCE_CLIENT.time_offset > 0
        assert isinstance(BINANCE_CLIENT.trade_fees, dict)
        assert len(BINANCE_CLIENT.trade_fees) == len(BINANCE_CLIENT.symbols_to_trade)

    def test_get_account_orders(self):
        orders = BINANCE_CLIENT.get_account_orders()
        assert isinstance(orders, list)
        for order in orders:
            assert isinstance(order, dict)
            assert "symbol" in order
            assert "orderId" in order
            assert "clientOrderId" in order
            assert "price" in order
            assert "origQty" in order
            assert "executedQty" in order
            assert "cummulativeQuoteQty" in order
            assert "status" in order
            assert "timeInForce" in order
            assert "type" in order
            assert "side" in order
            assert "stopPrice" in order
            assert "icebergQty" in order
            assert "time" in order
    
    def test_get_symbols_trade_fees(self):
        fees = BINANCE_CLIENT._get_symbols_trade_fees()
        assert isinstance(fees, dict)
        assert len(fees) == len(BINANCE_CLIENT.symbols_to_trade)
        for symbol in BINANCE_CLIENT.symbols_to_trade:
            assert symbol in fees
            assert isinstance(fees[symbol], dict)
            assert "maker" in fees[symbol]
            assert "taker" in fees[symbol]
    
    def test_get_account_details(self):
        details = BINANCE_CLIENT.get_account_details()
        assert isinstance(details, dict)
        assert "makerCommission" in details
        assert "takerCommission" in details
        assert "buyerCommission" in details
        assert "sellerCommission" in details
        assert "canTrade" in details
        assert "canWithdraw" in details
        assert "canDeposit" in details
        assert "balances" in details
        assert isinstance(details["balances"], list)
        for balance in details["balances"]:
            assert isinstance(balance, dict)
            assert "asset" in balance
            assert "free" in balance
            assert "locked" in balance
    
    def test_get_account_wallet(self):
        wallet = BINANCE_CLIENT.get_account_wallet(conversion_asset="USDT")
        assert isinstance(wallet, dict)
        assert "total_value" in wallet
        assert isinstance(wallet["total_value"], float)
        assert "conversion_asset" in wallet
        assert isinstance(wallet["conversion_asset"], str)
        assert "conversion_time_utc" in wallet
        assert isinstance(wallet["conversion_time_utc"], str)
        assert "balances" in wallet
        assert isinstance(wallet["balances"], list)
        for balance in wallet["balances"]:
            assert isinstance(balance, dict)
            assert "asset" in balance
            assert isinstance(balance["asset"], str)
            assert "symbol" in balance
            assert isinstance(balance["symbol"], str)
            assert "conversion_rate" in balance
            assert isinstance(balance["conversion_rate"], float)
            assert "quantity_free" in balance
            assert isinstance(balance["quantity_free"], float)
            assert "quantity_locked" in balance
            assert isinstance(balance["quantity_locked"], float)
            assert "total_quantity" in balance
            assert isinstance(balance["total_quantity"], float)
            assert "value" in balance
            assert isinstance(balance["value"], float)