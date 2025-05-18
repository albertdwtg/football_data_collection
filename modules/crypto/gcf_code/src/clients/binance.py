"""Module defining BinanceApi, interface to make interactions with binance API"""

from binance import Client
from binance.enums import HistoricalKlinesType
import polars as pl
import logging
import time
from datetime import datetime, timezone
from typing import Optional

class BinanceApi:
    """Class defining BinanceApi, interface to make interactions with binance API
    Doc: https://python-binance.readthedocs.io/en/latest/binance.html
    """

    def __init__(self, api_key: str, secret_key: str, quote_asset: str,
    coins_to_trade: Optional[list[str]] = None):
        """Init of the BinanceApi class

        Args:
            api_key (str): Api key of the Binance API
            secret_key (str): Secret key of the Binance API
            quote_asset (str): Name of the asset used for trades (ex: USDT)
            coins_to_trade (list[str], optional): List of coins that we want to trade.
                                                Defaults to None (all available coins).
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.client = Client(self.api_key, self.secret_key)
        self.quote_asset = quote_asset.upper()
        self.coins_to_trade = coins_to_trade
        self.symbols_to_trade = self._get_symbols_to_trade()
        self.time_offset = self._get_time_offset()
        self.trade_fees = self._get_symbols_trade_fees()
    
    def _get_symbols_to_trade(self, limit: Optional[int] = None) -> list[str]:
        """Function that returns a list of symbols to trade

        Args:
            limit (int, optional): If provided, it's the number of symbols
                                    that will be returned.
                                    Defaults to None.

        Returns:
            list[str]: List of symbols to trade. It contais the quote asset.
        """
        # Collect from Binance
        exchange_info = self.client.get_exchange_info()

        # We want to limit symbols to crypto only
        fiat_currencies = [
            "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "HKD", "NZD",
            "SGD", "KRW", "INR", "RUB", "BRL", "ZAR", "TRY", "MXN", "SEK", "NOK",
            "DKK", "PLN", "THB", "MYR", "IDR", "PHP", "TWD", "ILS", "SAR", "AED"
        ]

        # Filter symbols to only keep ones with corret assets and with status TRADING
        symbols = [symbol["symbol"].upper() for symbol in exchange_info["symbols"]
                if symbol["status"] == "TRADING"
                and symbol["quoteAsset"] == self.quote_asset
                and symbol["baseAsset"] not in fiat_currencies]
            
        # If coins_to_trade is provided, we filter symbols to only keep coins_to_trade
        if self.coins_to_trade:
            coins_with_quote_asset = [
                f"{coin}{self.quote_asset}".upper() for coin in self.coins_to_trade
            ]
            #Made intersection to be sure all symbols really exist
            symbols = list(set(symbols) & set(coins_with_quote_asset))
        
        # If limit is provided, we limit the number of symbols to return
        if limit:
            symbols = symbols[:limit]
        
        # We move BTC to the front of the list of symbols
        symbols = self._move_btc_to_front(symbols)
        logging.info("Symbols to trade : %s", symbols)
        logging.info("Number of symbols : %s", len(symbols))
        return symbols
    
    def get_historical_data(self, start_time: str|int,
        end_time: Optional[str|int] = None) -> tuple[list[int], dict]:
        """Function that collects historical data for all symbols
        Data will be formatted as a dict of dataframes, where keys are open, close, etc.
        For each dataframe, the index is the timestamp and the columns are the symbols.

        Args:
            start_time (str | int): Start time of the data to get
            end_time (str | int, optional): End time of the data to get.
                            If None > everything up to now. Defaults to None.

        Returns:
            tuple[list[int], dict]: The list of int is the indexes of the dataframes,
                    repsresenting the timestamps of the data point.
                    The dict is a dict of dataframes, where keys are open, close, etc.
        """
        # Template of the returned dict of dataframes
        klines_dict = {
            "open": pl.DataFrame(),
            "high": pl.DataFrame(),
            "low": pl.DataFrame(),
            "close": pl.DataFrame(),
            "volume": pl.DataFrame()
        }
        nb_lines = 0
        for index, symbol in enumerate(self.symbols_to_trade):
            logging.debug("Collecting data symbol number %s : %s", index, symbol)
            # Collect historical klines, daily, for each symbol
            klines = self.client.get_historical_klines(
                symbol = symbol,
                interval = Client.KLINE_INTERVAL_1DAY,
                start_str = start_time,
                end_str = end_time,
                klines_type = HistoricalKlinesType.SPOT)
                            
            # Transform data into polars dataframe
            klines_df = pl.DataFrame(klines, schema=[
                "timestamp", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "number_of_trades",
                "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
            ])

            # With the first symbol, we define the number of lines
            if index == 0:
                nb_lines = klines_df.shape[0]
                logging.info("Number of historical_records : %s", nb_lines)
                time_indexes = klines_df.to_series(0).to_list() # Timestamp is index 0
            
            # We collect and format only data for symbol having the same number of lines
            if klines_df.shape[0] == nb_lines:
                # Create dict of dataframes, where keys are open, close, etc.
                for key in klines_dict:
                    if key in klines_df.columns:
                        symbol_series = pl.Series(symbol, klines_df.get_column(key))\
                                        .cast(pl.Float64)
                        klines_dict[key].insert_column(0, symbol_series)
            else:
                logging.warning("Symbol %s has less than nb_lines columns", symbol)
        return time_indexes, klines_dict
    
    def _move_btc_to_front(self, symbols: list[str]) -> list[str]:
        """Function that moves 'BTC' to the front of the list of symbols

        Args:
            symbols (list[str]): List of symbols

        Returns:
            list[str]: List of symbols with 'BTC' in the first position.
        """
        # Apply sort only if BTC is in the list of symbols
        if f"BTC{self.quote_asset}" in symbols:
            symbols.remove(f"BTC{self.quote_asset}")
            symbols.insert(0, f"BTC{self.quote_asset}")
        return symbols
    
    def _get_time_offset(self) -> int:
        """Function that returns the time offset between binance and local time

        Returns:
            int: Offset observed
        """
        res = self.client.get_server_time()
        return res["serverTime"] - int(time.time() * 1000)

    def get_account_orders(self) -> list[dict]:
        """Function returning all orders made by the account

        Returns:
            list[dict]: List of detailed orders
        """
        orders = []
        # We only get symbols we are interested in
        for index, symbol in enumerate(self.symbols_to_trade):
            logging.debug("Collecting orders symbol number %s : %s", index, symbol)
            #Apply offset to avoid errors
            orders += self.client.get_all_orders(
                symbol=symbol,
                recvWindow=self.time_offset
            )
        return orders
    
    def _get_symbols_trade_fees(self) -> dict:
        """Function that returns symbols and trade fees

        Returns:
            dict: Dict of fees, where keys are symbols and values are fees
        """
        fees = {}
        for index, symbol in enumerate(self.symbols_to_trade):
            logging.debug("Collecting fees symbol number %s : %s", index, symbol)
            fees[symbol] = {}

            # As we request one symbol at a time,
            # returned list will have only one element
            fee_details = self.client.get_trade_fee(
                symbol=symbol,
                recvWindow=self.time_offset)[0]

            # Get fees
            fees[symbol]["maker"] = fee_details["makerCommission"]
            fees[symbol]["taker"] = fee_details["takerCommission"]
        return fees
    
    def get_account_details(self) -> dict:
        """Function that returns account details

        Returns:
            dict: Account details
        """
        return self.client.get_account()

    def get_account_wallet(self, conversion_asset: str) -> dict:
        """Collect account wallet with details

        Args:
            conversion_asset (str): Currency to convert to ex: USDT, USD etc.

        Returns:
            dict: Detailed wallet
        """
        # Collect conversion rates from Binance
        tickers = self.client.get_all_tickers()

        # Create wallet dict that be returned
        wallet = {}
        wallet["balances"] = []
        wallet["conversion_asset"] = conversion_asset
        wallet["conversion_time_utc"] = datetime\
                        .now(timezone.utc)\
                        .strftime("%Y-%m-%d %H:%M:%S")
        
        for asset in self.client.get_account()["balances"]:
            # Get asset only if we have it in our wallet
            if float(asset["free"]) + float(asset["locked"]) > 0:
                try:
                    # Collect ticker corresponding to <ASSET><CONVERSION_ASSET>
                    asset_ticker = [ticker for ticker in tickers
                        if ticker["symbol"] == f"{asset["asset"]}{conversion_asset}"
                    ][-1]
                    details = {
                        "asset": asset["asset"],
                        "symbol": asset_ticker["symbol"],
                        "conversion_rate": float(asset_ticker["price"]),
                        "quantity_free": float(asset["free"]),
                        "quantity_locked": float(asset["locked"]),
                        "total_quantity": float(asset["free"]) + float(asset["locked"]),
                        "value": (
                            float(asset["free"]) + float(asset["locked"])
                            ) * float(asset_ticker["price"])
                    }
                    wallet["balances"].append(details)
                except IndexError:
                    # Case where asset["asset"] is like USDT...
                    pass
        # Calculate total value of wallet
        wallet["total_value"] = sum(
            [balance["value"] for balance in wallet["balances"]]
        )
        return wallet
