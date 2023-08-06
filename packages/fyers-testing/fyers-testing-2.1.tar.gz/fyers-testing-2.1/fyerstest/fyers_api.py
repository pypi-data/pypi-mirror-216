moduleName = "fyersApi"

import logging
import urllib.parse
import hashlib
import json
import asyncio
import subprocess
import sys
import requests
import json
import urllib
import aiohttp
import asyncio
import json
from fyerstest.fyers_logger import FyersLogger


class Config:
    # API = 'https://api-t1.fyers.in/trade/v3'
    # API = 'https://api-t1.fydev.tech/trade/dev'
    API = "https://api.fyers.in/api/v2"
    HISTORY_URL = "https://api.fyers.in/data-rest/v2"
    DATA_API = "https://api-t1.fyers.in/data"
    AUTH_URL = "https://api.fyers.in/api/v2"

    # Endpoint
    get_profile = "/profile"
    tradebook = "/tradebook"
    positions = "/positions"
    holdings = "/holdings"
    convert_position = "/positions"
    funds = "/funds"
    orders = "/orders"
    minquantity = "/minquantity"
    market_status = "/market_status"
    auth = "/generate-authcode"
    generate_access_token = "/validate-authcode"
    generate_data_token = "/data-token"
    data_vendor_td = "truedata-ws"
    # multi_orders = 'orders-multi'
    sync_multi_order = "/multi-order/sync"
    multi_orders = "/multi-order"
    history = "/history"
    quotes = "/quotes"
    market_depth = "/depth"


class FyersServiceSync:
    def __init__(self, logger):
        """
        Initializes an instance of FyersServiceSync.

        Args:
            logger: The logger object used for logging errors.
        """
        self.logger = logger
        self.content = "application/json"

    def post_call(self, api: str, header: str, data=None) -> dict:
        """
        Makes a POST request to the specified API.

        Args:
            api: The API endpoint to make the request to.
            header: The authorization header for the request.
            data: The data to send in the request payload.

        Returns:
            The response JSON as a dictionary, or the response object if an error occurs.
        """
        try:
            response = requests.post(
                Config.API + api,
                data=json.dumps(data),
                headers={"Authorization": header, "Content-Type": self.content},
            )
            return response.json()
        except Exception as e:
            self.logger.error(e)

    def get_call(self, api: str, header: str, data=None, data_flag=False) -> dict:
        """
        Makes a GET request to the specified API.

        Args:
            api: The API endpoint to make the request to.
            header: The authorization header for the request.
            data: The data to send in the request query parameters.
            data_flag: A flag indicating whether to use custom data URLs.

        Returns:
            The response JSON as a dictionary, or the response object if an error occurs.
        """
        try:
            if data_flag:
                if api == Config.history:
                    URL = Config.HISTORY_URL + api
                else:
                    URL = Config.DATA_API + api
            else:
                URL = Config.API + api

            if data is not None:
                url_params = urllib.parse.urlencode(data)
                URL = URL + "?" + url_params

            response = requests.get(
                url=URL,
                headers={
                    "Authorization": header,
                    "Content-Type": self.content,
                    "version": "2.1",
                },
            )
            return response.json()
        except Exception as e:
            self.logger.error(e)

    def delete_call(self, api: str, header: str, data) -> dict:
        """
        Makes a DELETE request to the specified API.

        Args:
            api: The API endpoint to make the request to.
            header: The authorization header for the request.
            data: The data to send in the request payload.

        Returns:
            The response JSON as a dictionary, or the response object if an error occurs.
        """
        try:
            response = requests.delete(
                url=Config.API + api,
                data=json.dumps(data),
                headers={"Authorization": header, "Content-Type": self.content},
            )
            return response.json()
        except Exception as e:
            self.logger.error(e)

    def patch_call(self, api: str, header: str, data) -> dict:
        """
        Makes a PATCH request to the specified API.

        Args:
            api: The API endpoint to make the request to.
            header: The authorization header for the request.
            data: The data to send in the request payload.

        Returns:
            The response JSON as a dictionary, or the response object if an error occurs.
        """
        try:
            response = requests.patch(
                url=Config.API + api,
                data=json.dumps(data),
                headers={"Authorization": header, "Content-Type": self.content},
            )
            return response.json()
        except Exception as e:
            self.logger.error(e)


class FyersServiceAsync:
    def __init__(self, logger):
        """
        Initializes an instance of FyersServiceAsync.

        Args:
            logger: The logger object used for logging errors.
        """
        self.logger = logger
        self.content = "application/json"

    async def post_async_call(self, api: str, header: str, data=None) -> dict:
        """
        Makes an asynchronous POST request to the specified API.

        Args:
            api: The API endpoint to make the request to.
            header: The authorization header for the request.
            data: The data to send in the request payload.

        Returns:
            The response JSON as a dictionary, or the response object if an error occurs.
        """
        try:
            async with aiohttp.ClientSession(
                headers={"Authorization": header, "Content-Type": self.content}
            ) as session:
                url = Config.API + api
                async with session.post(url, data=json.dumps(data)) as response:
                    response = await response.json()
                    return response
        except Exception as e:
            self.logger.error(e)
            return response

    async def get_async_call(
        self, api: str, header: str, params=None, data_flag=False
    ) -> dict:
        """
        Makes an asynchronous GET request to the specified API.

        Args:
            api: The API endpoint to make the request to.
            header: The authorization header for the request.
            params: The query parameters to send with the request.
            data_flag: A flag indicating whether to use custom data URLs.

        Returns:
            The response JSON as a dictionary, or the response object if an error occurs.
        """
        try:
            if data_flag:
                if api == "/history":
                    URL = Config.HISTORY_URL + api
                else:
                    URL = Config.DATA_API + api
            else:
                URL = Config.API + api
            async with aiohttp.ClientSession(
                headers={
                    "Authorization": header,
                    "Content-Type": self.content,
                    "version": "2.1",
                }
            ) as session:
                async with session.get(URL, params=params) as response:
                    response = await response.json()
                    return response

        except Exception as e:
            self.logger.error(e)
            return response

    async def delete_async_call(self, api: str, header: str, data) -> dict:
        """
        Makes an asynchronous DELETE request to the specified API.

        Args:
            api: The API endpoint to make the request to.
            header: The authorization header for the request.
            data: The data to send in the request payload.

        Returns:
            The response JSON as a dictionary, or the response object if an error occurs.
        """
        try:
            async with aiohttp.ClientSession(
                headers={"Authorization": header, "Content-Type": self.content}
            ) as session:
                url = Config.API + api
                async with session.delete(url, data=json.dumps(data)) as response:
                    return await response.json()
        except Exception as e:
            self.logger.error(e)
            return response

    async def patch_async_call(self, api: str, header: str, data) -> dict:
        """
        Makes an asynchronous PATCH request to the specified API.

        Args:
            api: The API endpoint to make the request to.
            header: The authorization header for the request.
            data: The data to send in the request payload.

        Returns:
            The response JSON as a dictionary, or the response object if an error occurs.
        """
        try:
            async with aiohttp.ClientSession(
                headers={"Authorization": header, "Content-Type": self.content}
            ) as session:
                url = Config.API + api
                json_data = json.dumps(data).encode("utf-8")

                async with session.patch(url, data=json_data) as response:
                    return await response.json()
        except Exception as e:
            self.logger.error(e)
            return response


class SessionModel:
    def __init__(
        self,
        client_id=None,
        redirect_uri=None,
        response_type=None,
        scope=None,
        state=None,
        nonce=None,
        secret_key=None,
        grant_type=None,
    ):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.scope = scope
        self.state = state
        self.nonce = nonce
        self.secret_key = secret_key
        self.grant_type = grant_type

    def generate_authcode(self):
        data = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": self.response_type,
            "state": self.state,
        }
        if self.scope is not None:
            data["scope"] = self.scope
        if self.nonce is not None:
            data["nonce"] = self.nonce

        url_params = urllib.parse.urlencode(data)
        return f"{Config.AUTH_URL}{Config.auth}?{url_params}"

    def get_hash(self):
        hash_val = hashlib.sha256(f"{self.client_id}:{self.secret_key}".encode())
        return hash_val

    def set_token(self, token):
        self.auth_token = token

    def generate_token(self):
        data = {
            "grant_type": self.grant_type,
            "appIdHash": self.get_hash().hexdigest(),
            "code": self.auth_token,
        }
        response = requests.post(
            Config.AUTH_URL + Config.generate_access_token, headers="", json=data
        )
        return response.json()


class FyersModelv3:
    """
    A class that provides methods for making API calls synchronously or asynchronously.

    Attributes:
        is_async (bool): A boolean indicating whether API calls should be made asynchronously.
        service (object): An object that provides methods for making API calls.
        header (str): A string containing the header information for making API calls.
        logger (Logger): The logger object used for logging.
        client_id (str): The client ID for API authentication.
        token (str): The token for API authentication.
    """

    def __init__(
        self,
        is_async: bool = False,
        log_path=None,
        client_id: str = "",
        token: str = "",
    ):
        """
        Initializes an instance of FyersModelv3.

        Args:
            is_async: A boolean indicating whether API calls should be made asynchronously.
            client_id: The client ID for API authentication.
            token: The token for API authentication.
        """
        self.client_id = client_id
        self.token = token
        self.is_async = is_async
        self.log_path = log_path
        self.header = "{}:{}".format(self.client_id, self.token)
        if log_path:
            self.logger = FyersLogger(
                "FyersDataSocket",
                "DEBUG",
                stack_level=2,
                logger_handler=logging.FileHandler(log_path + "/fyersApi.log"),
            )
        else:
            self.logger = FyersLogger(
                "FyersDataSocket",
                "DEBUG",
                stack_level=2,
                logger_handler=logging.FileHandler("fyersApi.log"),
            )
        if is_async:
            self.service = FyersServiceAsync(self.logger)
        else:
            self.service = FyersServiceSync(self.logger)

    def get_profile(self) -> dict:
        """
        Retrieves the user profile information.

        """
        if self.is_async:
            response = asyncio.run(
                self.service.get_async_call(Config.get_profile, self.header)
            )
        else:
            response = self.service.get_call(Config.get_profile, self.header)
        return response

    def tradebook(self, data=None) -> dict:
        """
        Retrieves daily trade details of the day.

        """
        if self.is_async:
            response = asyncio.run(
                self.service.get_async_call(Config.tradebook, self.header, params=data)
            )
        else:
            response = self.service.get_call(Config.tradebook, self.header, data=data)
        return response

    def funds(self, data=None) -> dict:
        """
        Retrieves funds details.

        Args:
            data: Optional data to send in the request.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.get_async_call(Config.funds, self.header)
            )
        else:
            response = self.service.get_call(Config.funds, self.header, data=data)
        return response

    def positions(self) -> dict:
        """
        Retrieves information about current open positions.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.get_async_call(Config.positions, self.header)
            )
        else:
            response = self.service.get_call(Config.positions, self.header)
        return response

    def holdings(self, data=None) -> dict:
        """
        Retrieves information about current holdings.

        Args:
            data: Optional data to send in the request.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.get_async_call(Config.holdings, self.header, params=data)
            )
        else:
            response = self.service.get_call(Config.holdings, self.header, data=data)
        return response

    def get_orders(self, data) -> dict:
        """
        Retrieves order details by ID.

        Args:
            data: The data containing the order ID.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.get_async_call(
                    Config.multi_orders, self.header, params=data
                )
            )
        else:
            response = self.service.get_call(
                Config.multi_orders, self.header, data=data
            )
        return response

    def orderbook(self, data=None) -> dict:
        """
        Retrieves the order information.

        Args:
            data: Optional data to send in the request.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.get_async_call(Config.orders, self.header, params=data)
            )
        else:
            response = self.service.get_call(Config.orders, self.header, data)
        return response

    def market_status(self) -> dict:
        """
        Retrieves market status.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.get_async_call(
                    Config.market_status, self.header, data_flag=True
                )
            )
        else:
            response = self.service.get_call(
                Config.market_status, self.header, data_flag=True
            )
        return response

    def convert_position(self, data) -> dict:
        """
        Convert position.

        Args:
            data: The data containing the position conversion details.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.patch_async_call(
                    Config.convert_position, self.header, data
                )
            )
        else:
            response = self.service.patch_call(
                Config.convert_position, self.header, data
            )
        return response

    def cancel_order(self, data) -> dict:
        """
        Cancel order.

        Args:
            data: The data containing the order cancellation details.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.delete_async_call(Config.orders, self.header, data)
            )
        else:
            response = self.service.delete_call(Config.orders, self.header, data)
        return response

    def place_order(self, data) -> dict:
        """
        Order placement.

        Args:
            data: The data containing the order placement details.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.post_async_call(Config.orders, self.header, data)
            )
        else:
            response = self.service.post_call(Config.orders, self.header, data)
        return response

    def modify_order(self, data) -> dict:
        """
        Modify order.

        Args:
            data: The data containing the order modification details.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.patch_async_call(Config.orders, self.header, data)
            )
        else:
            response = self.service.patch_call(Config.orders, self.header, data)
        return response

    def exit_positions(self, data=None) -> dict:
        """
        Exit positions.

        Args:
            data: Optional data to send in the request.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.delete_async_call(Config.positions, self.header, data)
            )
        else:
            response = self.service.delete_call(Config.positions, self.header, data)
        return response

    def generate_data_token(self, data):
        allPackages = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
        installed_packages = [r.decode().split("==")[0] for r in allPackages.split()]
        if Config.dataVendorTD not in installed_packages:
            print("Please install truedata package | pip install truedata-ws")
        response = self.service.post_call(Config.generateDataToken, self.header, data)
        return response

    def cancel_basket_orders(self, data):
        """
        Cancel basket order.

        Args:
            data: The data containing the basket order cancellation details.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.delete_async_call(
                    Config.sync_multi_order, self.header, data
                )
            )
        else:
            response = self.service.delete_call(
                Config.sync_multi_order, self.header, data
            )
        return response

    def place_basket_orders(self, data):
        """
        Place basket order.

        Args:
            data: The data containing the basket order placement details.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.post_async_call(Config.multi_orders, self.header, data)
            )
        else:
            response = self.service.post_call(
                Config.sync_multi_order, self.header, data
            )
        return response

    def modify_basket_orders(self, data):
        """
        Modify basket orders.

        Args:
            data: The data containing the basket order modification details.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.patch_async_call(
                    Config.sync_multi_order, self.header, data
                )
            )
        else:
            response = self.service.patch_call(
                Config.sync_multi_order, self.header, data
            )
        return response

    def history(self, data=None):
        """
        Retrieves history data.

        Args:
            data: Optional data to send in the request.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.get_async_call(
                    Config.history, self.header, data, data_flag=True
                )
            )
        else:
            response = self.service.get_call(
                Config.history, self.header, data, data_flag=True
            )
        return response

    def quotes(self, data=None):
        """
        Retrieves quotes data.

        Args:
            data: Optional data to send in the request.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.get_async_call(
                    Config.quotes, self.header, data, data_flag=True
                )
            )
        else:
            response = self.service.get_call(
                Config.quotes, self.header, data, data_flag=True
            )
        return response

    def depth(self, data=None):
        """
        Retrieves market depth.

        Args:
            data: Optional data to send in the request.

        Returns:
            The response JSON as a dictionary.
        """
        if self.is_async:
            response = asyncio.run(
                self.service.get_async_call(
                    Config.market_depth, self.header, data, data_flag=True
                )
            )
        else:
            response = self.service.get_call(
                Config.market_depth, self.header, data, data_flag=True
            )
        return response
