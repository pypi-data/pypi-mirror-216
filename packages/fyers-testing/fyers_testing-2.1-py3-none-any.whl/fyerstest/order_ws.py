from typing import Any, Callable, Dict, Optional
import websocket
from threading import Thread
import logging
import threading
import time
import json
import fyerstest.defines as defines
from fyerstest.fyers_logger import FyersLogger


class FyersOrderSocket:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        access_token: str,
        write_to_file: Optional[bool] = False,
        log_path: Optional[str] = None,
        OnMessage: Optional[Callable] = None,
        OnError: Optional[Callable] = None,
        OnOpen: Optional[Callable] = None,
        OnClose: Optional[Callable] = None,
    ) -> None:
        """
        Initializes the class instance.

        Args:
            access_token (str): The access token to authenticate with.
            write_to_file (bool): Flag indicating whether to save data to file.
            log_path (str, optional): The path to the log file. Defaults to None.
            OnMessage (callable, optional): Callback function for message events. Defaults to None.
            OnError (callable, optional): Callback function for error events. Defaults to None.
            OnOpen (callable, optional): Callback function for open events. Defaults to None.
            OnClose (callable, optional): Callback function for close events. Defaults to None.
        """
        self.__access_token = access_token
        self.__url = "wss://socket.fydev.tech/trade/v3"
        self.log_path = log_path
        self.__ws_object = None
        self.__ws_run = False
        self.ping_thread = None
        self.write_to_file = write_to_file
        self.background_flag = False
        self.OnMessage = OnMessage
        self.OnError = OnError
        self.OnOpen = OnOpen
        self.OnClose = OnClose
        self.__ws_object = None
        self.__url = "wss://socket.fyers.in/trade/v3"

        if log_path:
            self.logger = FyersLogger(
                "FyersDataSocket",
                "DEBUG",
                stack_level=2,
                logger_handler=logging.FileHandler(log_path + "/fyersSocket.log"),
            )
        else:
            self.logger = FyersLogger(
                "FyersDataSocket",
                "DEBUG",
                stack_level=2,
                logger_handler=logging.FileHandler("fyersSocket.log"),
            )
        self.websocket_task = None

        self.write_to_file = write_to_file
        self.background_flag = False
        self.socket_type = {
            "OnOrders": "orders",
            "OnTrades": "trades",
            "OnPositions": "positions",
            "General": ["edis", "pricealerts"],
        }

    def __parse_position_data(self, msg: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses position data from a message and returns it in a specific format.

        Args:
            msg (str): The message containing position data.

        Returns:
            Dict[str, Any] : The parsed position data in a specific format.

        """
        try:
            position_data_keys = [
                "buy_avg",
                "buy_qty",
                "buy_val",
                "cf_buy_qty",
                "cf_sell_qty",
                "day_buy_qty",
                "day_sell_qty",
                "fy_token",
                "id",
                "net_avg",
                "net_qty",
                "pl_realized",
                "product_type",
                "segment",
                "sell_avg",
                "sell_qty",
                "sell_val",
                "symbol",
                "tran_side",
            ]
            position_data = {key: msg["positions"][key] for key in position_data_keys}
            position_data.update(
                {
                    "qty_multi": msg["positions"]["qty_multiplier"],
                    "rbi_ref_rate": msg["positions"]["rbirefrate"],
                    "sym_desc": msg["positions"]["symbol_desc"],
                }
            )

            return {"ws_type": 1, "s": msg["s"], "d": position_data}

        except Exception as e:
            self.logger.error(e)

    def __parse_trade_data(self, msg: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses trade data from a message and returns it in a specific format.

        Args:
            msg (str): The message containing trade data.

        Returns:
            Dict[str, Any] : The parsed trade data in a specific format.

        """
        try:
            trade_data_keys = [
                "id_fill",
                "id",
                "qty_traded",
                "price_traded",
                "traded_val",
                "product_type",
                "client_id",
                "id_exchange",
                "ord_type",
                "tran_side",
                "symbol",
                "time_epoch",
                "fy_token",
            ]
            trade_data = dict((key, msg["trades"][key]) for key in trade_data_keys)
            trade_data["tradeNumber"] = msg["trades"]["id"]

            return {"ws_type": 1, "s": msg["s"], "d": trade_data}

        except Exception as e:
            self.logger.error(e)

    def __parse_order_data(self, msg: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses order update data from a dictionary and returns it in a specific format.

        Args:
            msg (Dict[str, Any]): The dictionary containing order update data.

        Returns:
            Dict[str, Any]: The parsed order update data in a specific format.
        """
        try:
            key_map = {
                "update_time_epoch_oms": "orderDateTime",
                "id": "exchOrdId",
                "product_type": "productType",
                "instrument": "instrument",
                "side": "side",
                "ord_status": "status",
                "qty": "qty",
                "qty_filled": "filledQty",
                "qty_remaining": "remainingQuantity",
                "ord_type": "type",
                "validity": "orderValidity",
                "offline_flag": "offlineOrder",
                "status_msg": "message",
                "symbol": "symbol",
                "fy_token": "fyToken",
                "segment": "segment",
                "dqQtyRem": "dqQtyRem",
                "price_limit": "limitPrice",
                "price_stop": "stopPrice",
                "qty_disc": "discloseQty",
                "price_traded": "tradedPrice",
            }
            order = msg["orders"]
            order_data = {key_map[key]: order.get(key, 0) for key in key_map}

            order_data["orderNumStatus"] = (
                order["id"] + ":" + str(order["org_ord_status"])
            )
            order_data["id"] = order["id"]
            # order_data["slNo"] = int(time.time())

            return {"ws_type": 1, "s": msg["s"], "d": order_data}

        except Exception as e:
            self.logger.error(e)

    def __on_message(self, message: Dict[str, Any]):
        """
        Parses the response data based on its content.

        Args:
            message (str): The response message to be parsed.

        Returns:
            Any: The parsed response data.
        """
        try:
            response = json.loads(message)

            if "orders" in response:
                response = self.__parse_order_data(response)
            elif "positions" in response:
                response = self.__parse_position_data(response)
            elif "trades" in response:
                response = self.__parse_trade_data(response)

            if self.write_to_file:
                self.logger.debug(f"Response:{response}")
            else:
                self.logger.debug(f"Response:{response}")
                self.On_message(response)

        except Exception as e:
            self.logger.error(e)

    def On_message(self, message: Any) -> None:
        """
        Callback function for handling message events.

        Args:
            message (Any): The message received.

        """
        if self.OnMessage is not None:
            self.OnMessage(message)
        else:
            print(f"Response : {message}")

    def On_error(self, message: str) -> None:
        """
        Callback function for handling error events.

        Args:
            message (str): The error message.

        """
        self.logger.error(message)
        if self.OnError is not None:
            self.OnError(message)
        else:
            if self.write_to_file:
                self.logger.debug(f"Response:{message}")
            else:
                print(f"Error Response : {message}")

    def __on_open(self, ws):
        try:
            if self.__ws_object is None:
                self.__ws_object = ws
                self.ping_thread = threading.Thread(target=self.__ping)
                self.ping_thread.start()

        except Exception as e:
            self.logger.error(e)

    def __on_close(self, ws, close_code=None, close_reason=None):
        """
        Handle the WebSocket connection close event.

        Args:
            ws (WebSocket): The WebSocket object.
            close_code (int): The code indicating the reason for closure.
            close_reason (str): The reason for closure.

        Returns:
            dict: A dictionary containing the response code, message, and s.
        """
        if self.restart_flag:
            if self.reconnect_attempts < self.max_reconnect_attempts:
                self.reconnect_attempts += 1

                if self.write_to_file:
                    self.logger.debug(
                        f"Response:{f'Attempting reconnect {self.reconnect_attempts} of {self.max_reconnect_attempts}...'}"
                    )
                else:
                    print(
                        f"Attempting reconnect {self.reconnect_attempts} of {self.max_reconnect_attempts}..."
                    )
                time.sleep(self.reconnect_delay)
                self.on_open()
            else:
                if self.write_to_file:
                    self.logger.debug(
                        f"Response:{'Max reconnect attempts reached. Connection abandoned.'}"
                    )
                else:
                    print("Max reconnect attempts reached. Connection abandoned.")
        else:

            self.on_close(
                {
                    "code": defines.SUCCESS_CODE,
                    "message": defines.CONNECTION_CLOSED,
                    "s": defines.success,
                }
            )

    def __ping(self) -> None:
        """
        Sends periodic ping messages to the server to maintain the WebSocket connection.

        The method continuously sends "__ping" messages to the server at a regular interval
        as long as the WebSocket connection is active.

        """

        while (
            self.__ws_object is not None
            and self.__ws_object.sock
            and self.__ws_object.sock.connected
        ):
            self.__ws_object.send("__ping")
            time.sleep(10)

    def on_close(self, message: dict) -> None:
        """
        Handles the close event.

        Args:
            message (dict): The close message .
        """

        if self.OnClose:
            self.OnClose(message)
        else:
            print(f"Response: {message}")

    def on_open(self) -> None:
        """
        Performs initialization and waits before executing further actions.
        """
        self.init_connection()
        time.sleep(2)

        if self.OnOpen:
            self.OnOpen()

    def init_connection(self):
        """
        Initializes the WebSocket connection and starts the WebSocketApp.

        The method creates a WebSocketApp object with the specified URL and sets the appropriate event handlers.
        It then starts the WebSocketApp in a separate thread.
        """
        try:
            if self.__ws_object is None:
                if self.write_to_file:
                    self.background_flag = True
                header = {"authorization": self.__access_token}
                ws = websocket.WebSocketApp(
                    self.__url,
                    header=header,
                    on_message=lambda ws, msg: self.__on_message(msg),
                    on_error=lambda ws, msg: self.On_error(msg),
                    on_close=lambda ws, close_code, close_reason: self.__on_close(
                        ws, close_code, close_reason
                    ),
                    on_open=lambda ws: self.__on_open(ws),
                )
                self.t = Thread(target=ws.run_forever)
                self.t.daemon = self.background_flag
                self.t.start()

        except Exception as e:
            self.logger.error(e)

    def keep_running(self):
        """
        Starts an infinite loop to keep the program running.

        """
        self.__ws_run = True
        t = Thread(target=self.infinite_loop)
        t.start()

    def stop_running(self):
        self.__ws_run = False

    def infinite_loop(self):
        while self.__ws_run:
            pass

    def close_connection(self):
        """
        Closes the WebSocket connection 

        """
        if self.__ws_object is not None:
            self.__ws_object.close(reason=json.dumps({}))
            self.__ws_object = None
            self.__on_close(None)
            self.ping_thread.join()

    def subscribe(self, data_type: str) -> None:
        """
        Subscribes to real-time updates of a specific data type.

        Args:
            data_type (str): The type of data to subscribe to, such as orders, position, or holdings.


        """

        try:
            self.init_connection()
            time.sleep(1)
            if self.__ws_object is not None:
                self.data_type = [
                    self.socket_type[(type)] for type in data_type.split(",")
                ]
                message = json.dumps(
                    {"T": "SUB_ORD", "SLIST": self.data_type, "SUB_T": 1}
                )
                self.__ws_object.send(message)

        except Exception as e:
            self.logger.error(e)

    def unsubscribe(self, data_type: str) -> None:
        """
        Unsubscribes from real-time updates of a specific data type.

        Args:
            data_type (str): The type of data to unsubscribe from, such as orders, position, holdings or general.

        """

        try:
            if self.__ws_object is not None:
                self.data_type = [
                    self.socket_type[(type)] for type in data_type.split(",")
                ]
                message = json.dumps(
                    {"T": "SUB_ORD", "SLIST": self.data_type, "SUB_T": -1}
                )
                self.__ws_object.send(message)

        except Exception as e:
            self.logger.error(e)
