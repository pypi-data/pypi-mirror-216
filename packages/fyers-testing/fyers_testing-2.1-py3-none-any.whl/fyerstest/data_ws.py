import threading
import time
import websocket
from threading import Thread
import struct
from fyerstest.fyers_api import  FyersModelv3
from fyerstest import defines
import json
from typing import Optional, Callable
from fyerstest.fyers_logger import FyersLogger


class SymbolConversion:
    def __init__(self, access_token: str, data_type: str):
        """
        Initializes a SymbolConversion instance.

        Args:
            access_token (str): The access token used for authentication.
            data_type (str): The data_type associated with the symbol conversion. 
                            Valid values are 'symbolupdate' or 'depthupdate'.

        """
        self.data_type = data_type
        if ":" in access_token:
            access_token = access_token.split(":")[1]
        self.access_token = access_token

    def symbol_to_hsmtoken(self, symbols: list):
        """
        Converts symbols to HSM tokens.

        Args:
            symbols (list): A list of symbols to be converted.

        Returns:
            tuple: A tuple containing dictionary and list.
                - The first dictionary represents the mapping of symbols to HSM tokens.
                - The second list represents any symbols that could not be converted.

        """
        symbols = ",".join(symbols)
        fyers = FyersModelv3(token=self.access_token, is_async=False)
        quote_data = fyers.quotes({"symbols": symbols})
        datadict = {}
        values = {}
        with open("fyerstest/map.json", "r") as file:
            # Load the JSON data into a Python object
            mapper = json.load(file)
        index_dict = mapper["index_dict"]
        exch_seg_dict = mapper["exch_seg_dict"]
        wrong_symbol = []
        if "d" in quote_data:
            for data in quote_data["d"]:
                if data["s"] == "ok":
                    values = {}
                    values["fyToken"] = data["v"]["fyToken"]
                    values["symbol"] = data["v"]["symbol"]
                    key = values["fyToken"][:4]
                    values["segment"] = exch_seg_dict[key]
                    data = values["symbol"].split("-")

                    if len(data) > 1 and data[-1] == "INDEX":
                        if values["symbol"] in index_dict:
                            values["exToken"] = index_dict[values["symbol"]]
                        else:
                            values["exToken"] = (
                                values["symbol"].split(":")[1].split("-")[0]
                            )
                        values["subSymbol"] = (
                            "if" + "|" + values["segment"] + "|" + values["exToken"]
                        )
                    elif self.data_type == "DepthUpdate":
                        values["exToken"] = values["fyToken"][10:]
                        values["subSymbol"] = (
                            "dp" + "|" + values["segment"] + "|" + values["exToken"]
                        )

                    else:
                        values["exToken"] = values["fyToken"][10:]
                        values["subSymbol"] = (
                            "sf" + "|" + values["segment"] + "|" + values["exToken"]
                        )
                    datadict[values["subSymbol"]] = values["symbol"]
                elif data["s"] == "error":
                    wrong_symbol.append(data["n"])

            return (datadict, wrong_symbol)
        return ({}, [])


class FyersDataSocket:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        access_token: str,
        write_to_file: bool = False,
        log_path: Optional[str] = None,
        litemode: bool = False,
        reconnect: bool = False,
        OnMessage: Optional[Callable] = None,
        OnError: Optional[Callable] = None,
        OnOpen: Optional[Callable] = None,
        OnClose: Optional[Callable] = None,
    ):

        """
        Initialize YourClass instance.

        Args:
            access_token (str): The access token used for authentication.
            write_to_file (bool, optional): Specifies if the class should run in the background.
                Defaults to False.
            log_path (str, optional): The path to the log file. Defaults to None.
            litemode (bool, optional): Specifies if the class should run in litemode.
                Defaults to False.
            reconnect (bool, optional): Specifies if the class should attempt to reconnect on failure.
                Defaults to False.
            OnMessage (callable, optional): Callback function to be executed when a message is received.
                Defaults to None.
            OnError (callable, optional): Callback function to be executed when an error occurs.
                Defaults to None.
            OnOpen (callable, optional): Callback function to be executed when a connection is established.
                Defaults to None.
            OnClose (callable, optional): Callback function to be executed when a connection is closed.
                Defaults to None.
        """

        self.__url = "wss://socket.fydev.tech/hsm/v1-5/dev"
        self.__access_token = access_token
        self.log_path = log_path
        self.reconnect = reconnect
        self.lite = litemode
        self.source = "PythonSDK-1.0.0"
        self.channel_num = 1
        self.channels = []
        self.running_channels = set()
        self.data_type = None
        self.OnMessage = OnMessage
        self.OnError = OnError
        self.OnOpen = OnOpen
        self.OnClose = OnClose
        self.__ws_run = None
        self.write_to_file = write_to_file
        self.background_flag = False
        self.update_count = 0
        self.literesp = {}
        self.channel_symbol = []
        self.symbol_dict = {}
        self.scrips_count = {}
        self.scrips_per_channel = {}
        self.restart_flag = True
        self.websocket_lock = threading.Lock()
        self.unsub_symbol = []
        for i in range(1, 31):
            self.scrips_per_channel[i] = []
        self.active_channel = None
        self.message = []
        self.resp = {}
        self.__ws_object = None
        self.dp_sym = {}
        self.ping_thread = None
        self.message_thread = None
        self.ws_thread = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 5
        self.index_sym = {}
        self.scrips_sym = {}
        self.symbol_token = {}
        self.ack_bool = False

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

        with open("fyerstest/map.json", "r") as file:
            # Imported json file
            mapper = json.load(file)

        self.data_val = mapper["data_val"]
        self.index_val = mapper["index_val"]
        self.lite_val = mapper["lite_val"]
        self.depthvalue = mapper["depthvalue"]

    def __access_token_msg(self) -> bytearray:
        """
        Create a message in bytearray for token.

        Returns:
            bytearray: The token message in bytearray format.
        """
        try:
            buffer_size = 18 + len(self.__access_token) + len(self.source)

            # Create the byte buffer
            byte_buffer = bytearray()

            # Pack data length into the byte buffer
            byte_buffer.extend(struct.pack("!H", buffer_size - 2))

            # Set ReqType
            byte_buffer.extend(bytes([1]))

            # Set FieldCount
            byte_buffer.extend(bytes([4]))

            # Field-1: AuthToken
            field1_id = 1
            field1_size = len(self.__access_token)
            byte_buffer.extend(bytes([field1_id]))
            byte_buffer.extend(struct.pack("!H", field1_size))
            byte_buffer.extend(self.__access_token.encode())

            # Field-2
            field2_id = 2
            field2_size = 1
            byte_buffer.extend(bytes([field2_id]))
            byte_buffer.extend(struct.pack("!H", field2_size))
            byte_buffer.extend(bytes([78]))

            # Field-3
            field3_id = 3
            field3_size = 1
            byte_buffer.extend(bytes([field3_id]))
            byte_buffer.extend(struct.pack("!H", field3_size))
            byte_buffer.extend(bytes([1]))

            # Field-4: self.source
            field4_id = 4
            field4_size = len(self.source)
            byte_buffer.extend(bytes([field4_id]))
            byte_buffer.extend(struct.pack("!H", field4_size))
            byte_buffer.extend(self.source.encode())

            return byte_buffer

        except Exception as e:
            self.logger.error(e)

    def __lite_mode_msg(self) -> bytearray:
        """
        Create a message in bytearray for lite mode connection.

        Returns:
            bytearray: The lite mode message in bytearray format.
        """

        try:
            self.channels = [self.channel_num]
            data = bytearray()

            data.extend(struct.pack(">H", 0))

            data.extend(struct.pack("B", 12))

            data.extend(struct.pack("B", 2))

            channel_bits = 0
            for channel_num in self.channels:
                if channel_num < 64 and channel_num > 0:
                    channel_bits |= 1 << channel_num
            # Field-1
            field_1 = bytearray()
            field_1.extend(struct.pack("B", 1))
            field_1.extend(struct.pack(">H", 8))
            field_1.extend(struct.pack(">Q", channel_bits))
            data.extend(field_1)

            # Field-2
            field_2 = bytearray()
            field_2.extend(struct.pack("B", 2))
            field_2.extend(struct.pack(">H", 1))
            field_2.extend(struct.pack("B", 76))
            data.extend(field_2)

            return data

        except Exception as e:
            self.logger.error(e)

    def __full_mode_msg(self) -> bytearray:

        """
        Create a message in bytearray for full mode connection.

        Returns:
            bytearray: The full mode message in bytearray format.
        """
        try:
            self.channels = [self.channel_num]
            data = bytearray()

            data.extend(struct.pack(">H", 0))

            data.extend(struct.pack("B", 12))

            data.extend(struct.pack("B", 2))

            channel_bits = 0
            for channel_num in self.channels:
                if channel_num < 64 and channel_num > 0:
                    channel_bits |= 1 << channel_num
            # Field-1
            field_1 = bytearray()
            field_1.extend(struct.pack("B", 1))
            field_1.extend(struct.pack(">H", 8))
            field_1.extend(struct.pack(">Q", channel_bits))
            data.extend(field_1)

            # Field-2
            field_2 = bytearray()
            field_2.extend(struct.pack("B", 2))
            field_2.extend(struct.pack(">H", 1))
            field_2.extend(struct.pack("B", 70))
            data.extend(field_2)

            return data

        except Exception as e:
            self.logger.error(e)

    def __subscription_msg(self, symbols: list) -> bytearray:

        """
        Create a message in bytearray for symbol subscription.

        Args:
            symbols (list): A list of symbols to subscribe to.

        Returns:
            bytearray: The subscription message in bytearray format.
        """

        try:
            self.scrips_per_channel[self.channel_num] += symbols
            self.scrips = symbols
            self.scrips_data = bytearray()
            self.scrips_data.append(len(self.scrips) >> 8 & 0xFF)
            self.scrips_data.append(len(self.scrips) & 0xFF)
            for scrip in self.scrips:
                scrip_bytes = str(scrip).encode("ascii")
                self.scrips_data.append(len(scrip_bytes))
                self.scrips_data.extend(scrip_bytes)

            data_len = (
                18 + len(self.scrips_data) + len(self.__access_token) + len(self.source)
            )
            request_type = 4
            field_count = 2
            buffer_msg = bytearray()
            buffer_msg.extend(struct.pack(">H", data_len))
            buffer_msg.append(request_type)
            buffer_msg.append(field_count)

            # Field-1
            buffer_msg.append(1)
            buffer_msg.extend(struct.pack(">H", len(self.scrips_data)))
            buffer_msg.extend(self.scrips_data)

            # Field-2
            buffer_msg.append(2)
            buffer_msg.extend(struct.pack(">H", 1))
            buffer_msg.append(self.channel_num)

            return buffer_msg

        except Exception as e:
            self.logger.error(e)

    def __unsubscription_msg(self, symbols: list) -> bytearray:
        """
        Create a message in bytearray for unsubscription message.

        Args:
            symbols (list): A list of symbols to unsubscribe from.

        Returns:
            bytearray: The unsubscription message in bytearray format.
        """
        try:
            scrips_data = bytearray()
            scrips_data.append(len(symbols) >> 8 & 0xFF)
            scrips_data.append(len(symbols) & 0xFF)
            for scrip in symbols:
                scrip_bytes = str(scrip).encode("ascii")
                scrips_data.append(len(scrip_bytes))
                scrips_data.extend(scrip_bytes)

            data_len = (
                18 + len(scrips_data) + len(self.__access_token) + len(self.source)
            )
            request_type = 5
            field_count = 2
            buffer_msg = bytearray()
            buffer_msg.extend(struct.pack(">H", data_len))
            buffer_msg.append(request_type)
            buffer_msg.append(field_count)

            # Field-1
            buffer_msg.append(1)
            buffer_msg.extend(struct.pack(">H", len(scrips_data)))
            buffer_msg.extend(scrips_data)

            # Field-2
            buffer_msg.append(2)
            buffer_msg.extend(struct.pack(">H", 1))
            buffer_msg.append(self.channel_num)

            return buffer_msg

        except Exception as e:

            self.logger.error(e)

    def __channel_resume_msg(self, channel: int) -> bytearray:

        """
        Create a message in bytearray for channel resume.

        Args:
            channel (int): The channel to resume.

        Returns:
            bytearray: The channel resume message in bytearray format.
        """
        try:

            self.channels = [channel]

            data = bytearray()

            data.extend(struct.pack(">H", 0))

            data.extend(struct.pack("B", 8))

            data.extend(struct.pack("B", 1))

            channel_bits = 0
            for channel_num in self.channels:
                if channel_num < 64 and channel_num > 0:
                    channel_bits |= 1 << channel_num
            # Field-1
            field_1 = bytearray()
            field_1.extend(struct.pack("B", 1))
            field_1.extend(struct.pack(">H", 8))
            field_1.extend(struct.pack(">Q", channel_bits))
            data.extend(field_1)

            return data

        except Exception as e:

            self.logger.error(e)

    def __channel_pause_msg(self, channel: int) -> bytearray:

        """
        Create a message in bytearray for channel pause.

        Args:
            channel (int): The channel to pause.

        Returns:
            bytearray: The channel pause message in bytearray format.
        """

        try:
            self.channels = [channel]

            data = bytearray()

            data.extend(struct.pack(">H", 0))

            data.extend(struct.pack("B", 7))

            data.extend(struct.pack("B", 1))

            channel_bits = 0
            for channel_num in self.channels:
                if channel_num < 64 and channel_num > 0:
                    channel_bits |= 1 << channel_num
            # Field-1
            field_1 = bytearray()
            field_1.extend(struct.pack("B", 1))
            field_1.extend(struct.pack(">H", 8))
            field_1.extend(struct.pack(">Q", channel_bits))
            data.extend(field_1)

            return data

        except Exception as e:
            self.logger.error(e)

    def __ackowledgement_msg(self, message_number: int) -> bytearray:

        """
        Create a message in bytearray for acknowledgement.

        Args:
            message_number (int): The message number to acknowledge.

        Returns:
            bytearray: The acknowledgement message in bytearray format.
        """
        try:
            total_size = 11
            req_type = 3
            field_count = 1
            field_id = 1
            field_size = 4
            field_value = message_number
            buffer_msg = bytearray()
            # Pack the data into the byte array
            buffer_msg.extend(struct.pack(">H", total_size - 2))
            buffer_msg.extend(struct.pack("B", req_type))
            buffer_msg.extend(struct.pack("B", field_count))
            buffer_msg.extend(struct.pack("B", field_id))
            buffer_msg.extend(struct.pack(">H", field_size))
            buffer_msg.extend(struct.pack(">I", field_value))

            return buffer_msg

        except Exception as e:
            self.logger.error(e)

    def __auth_resp(self, data: bytearray) -> dict:
        """
        Unpacks the authentication response from a bytearray.

        Args:
            data (bytearray): The authentication response message.

        Returns:
            dict: The authentication response as a dictionary with keys 'code', 'message', and 's'.
        """

        try:
            offset = 4
            offset += 1
            field_length = struct.unpack("!H", data[offset : offset + 2])[0]
            offset += 2
            string_val = data[offset : offset + field_length].decode("utf-8")
            offset += field_length

            if string_val == "K":

                self.On_message(
                    {
                        "code": defines.SUCCESS_CODE,
                        "message": defines.AUTH_SUCCESS,
                        "s": defines.SUCCESS,
                    }
                )
            else:
                self.On_error(
                    {
                        "code": defines.AUTH_ERROR_CODE,
                        "message": defines.AUTH_FAIL,
                        "s": defines.ERROR,
                    }
                )

            offset += 1
            field_length = struct.unpack("!H", data[offset : offset + 2])[0]
            offset += 2
            self.ack_count = struct.unpack(">I", data[offset : offset + 4])[0]
            offset += 4

        except Exception as e:
            self.logger.error(e)

    def __subscribe_resp(self, data: bytearray) -> dict:
        """
        Unpacks the subscription response from a bytearray.

        Args:
            data (bytearray): The subscription response message.

        Returns:
            dict: The subscription response as a dictionary with keys 'code', 'message', and 's'.
        """

        try:

            offset = 5
            field_length = struct.unpack("H", data[offset : offset + 2])[0]
            offset += 2
            string_val = data[offset : offset + 1].decode("latin-1")
            offset += field_length
            if string_val == "K":

                self.On_message(
                    {
                        "code": defines.SUCCESS_CODE,
                        "message": defines.SUBSCRIBE_SUCCESS,
                        "s": defines.SUCCESS,
                    }
                )
            else:
                self.On_error(
                    {
                        "code": defines.SUBS_ERROR_CODE,
                        "message": defines.SUBSCRIBE_FAIL,
                        "s": defines.ERROR,
                    }
                )

        except Exception as e:
            self.logger.error(e)

    def __unsubscribe_resp(self, data: bytearray) -> dict:

        """
        Unpacks the unsubscription response from a bytearray.

        Args:
            data (bytearray): The unsubscription response message.

        Returns:
            dict: The unsubscription response as a dictionary with keys 'code', 'message', and 's'.
        """

        try:

            offset = 5
            field_length = struct.unpack("H", data[offset : offset + 2])[0]
            offset += 2
            string_val = data[offset : offset + 1].decode("latin-1")
            offset += field_length
            if string_val == "K":

                self.On_message(
                    {
                        "code": defines.SUCCESS_CODE,
                        "message": defines.UNSUBSCRIBE_SUCCESS,
                        "s": defines.SUCCESS,
                    }
                )

            else:
                self.On_error(
                    {
                        "code": defines.UNSUBS_ERROR_CODE,
                        "message": defines.UNSUBSCRIBE_FAIL,
                        "s": defines.ERROR,
                    }
                )

        except Exception as e:
            self.logger.error(e)

    def __lite_full_mode_resp(self, data: bytearray) -> dict:

        """
        Unpacks the lite/full mode response from a bytearray.

        Args:
            data (bytearray): The lite/full mode response message.

        Returns:
            dict: The lite/full mode response as a dictionary with keys 'code', 'message', and 's'.
        """

        try:
            offset = 3

            # Unpack the field count
            field_count = struct.unpack("!B", data[offset : offset + 1])[0]
            offset += 1

            if field_count >= 1:
                # Unpack the field ID
                offset += 1

                # Unpack the field length
                field_length = struct.unpack("!H", data[offset : offset + 2])[0]
                offset += 2

                # Extract the string value and decode it
                string_val = data[offset : offset + field_length].decode("utf-8")
                offset += field_length

                if string_val == "K":
                    if self.lite:
                        self.On_message(
                            {
                                "code": defines.SUCCESS_CODE,
                                "message": defines.LITE_MODE,
                                "s": defines.SUCCESS,
                            }
                        )
                    else:
                        self.On_message(
                            {
                                "code": defines.SUCCESS_CODE,
                                "message": defines.FULL_MODE,
                                "s": defines.SUCCESS,
                            }
                        )
                else:
                    self.On_error(
                        {
                            "code": defines.MODE_ERROR_CODE,
                            "message": defines.MODE_CHANGE_ERROR,
                            "s": defines.ERROR,
                        }
                    )

        except Exception as e:
            self.logger.error(e)

    def __response_output(self, data: str, data_type: str) -> object:

        """
        Processes the response data and returns the output based on the specified data_type.

        Args:
            data (bytearray): The response data.
            data_type (str): The type of data to be processed.

        Returns:
            object: The processed output based on the specified data_type.
        """

        try:
            data_resp = data
            response = {}
            if (
                "bidPrice1" not in data_resp
                and "vol_traded_today" in data_resp
                and self.lite
            ):
                for i, val in enumerate(self.lite_val):
                    if val in data_resp and val == "ltp":
                        response[val] = data_resp[val] / (10 ** data_resp["precision"])
                    else:
                        response[val] = data_resp[val]
            else:
                if data_type == "depth":

                    for i, val in enumerate(self.depthvalue):
                        if val in data_resp and i < 10:
                            response[val] = data_resp[val] / (
                                10 ** data_resp["precision"]
                            )
                        else:
                            response[val] = data_resp[val]
                elif data_type == "scrips":
                    for i, val in enumerate(self.data_val):
                        if val in data_resp and i in [
                            0,
                            6,
                            7,
                            11,
                            13,
                            14,
                            17,
                            18,
                            19,
                            20,
                        ]:
                            response[val] = data_resp[val] / (
                                10 ** data_resp["precision"]
                            )
                        else:
                            response[val] = data_resp[val]

                    if "OI" in response:
                        response.pop("OI")
                    if "Yhigh" in response:
                        response.pop("Yhigh")
                    if "Ylow" in response:
                        response.pop("Ylow")
                else:
                    for i, val in enumerate(self.index_val):
                        if val in data_resp and i in [0, 1, 3, 4, 5]:
                            response[val] = data_resp[val] / (
                                10 ** data_resp["precision"]
                            )
                        else:
                            response[val] = data_resp[val]

            self.On_message(response)

        except Exception as e:
            self.logger.error(e)

    def __datafeed_resp(self, data: bytearray):

        """
        Unpacks and processes the data based on data_type and sends it to the __response_output function.

        Args:
            data (bytearray): The response data.

        Returns:
            None
        """
        try:

            if self.ack_count > 0:
                self.update_count += 1
                message_num = struct.unpack(">I", data[3:7])[0]
                if self.update_count == self.ack_count:
                    self.ack_msg = self.__ackowledgement_msg(message_num)
                    self.message.append(self.ack_msg)
                    self.update_count = 0
            scrip_count = struct.unpack("!H", data[7:9])[0]
            offset = 9

            for _ in range(scrip_count):
                data_type = struct.unpack("B", data[offset : offset + 1])[0]
                if data_type == 83:  # Snapshot datafeed

                    offset += 1
                    topic_id = struct.unpack("H", data[offset : offset + 2])[0]
                    offset += 2
                    topic_name_len = struct.unpack("B", data[offset : offset + 1])[0]
                    offset += 1

                    topic_name = data[offset : offset + topic_name_len].decode("utf-8")
                    offset += topic_name_len

                    # Maintaining dict - topic_id : topic_name
                    if topic_name[:2] == "dp":
                        self.dp_sym[topic_id] = topic_name
                        self.resp[self.dp_sym[topic_id]] = {}

                        field_count = struct.unpack("B", data[offset : offset + 1])[0]
                        offset += 1

                        for index in range(field_count):
                            value = struct.unpack(">I", data[offset : offset + 4])[0]
                            offset += 4
                            self.resp[self.dp_sym[topic_id]][
                                self.depthvalue[index]
                            ] = value

                        offset += 2

                        multiplier = struct.unpack("H", data[offset : offset + 2])[0]
                        self.resp[self.dp_sym[topic_id]]["multiplier"] = multiplier
                        offset += 2

                        precision = struct.unpack("B", data[offset : offset + 1])[0]
                        self.resp[self.dp_sym[topic_id]]["precision"] = precision
                        offset += 1

                        val = ["exchange", "exchange_token", "symbol"]
                        for i in range(3):
                            string_len = struct.unpack("B", data[offset : offset + 1])[
                                0
                            ]
                            offset += 1
                            string_data = data[offset : offset + string_len].decode(
                                "utf-8"
                            )
                            self.resp[self.dp_sym[topic_id]][val[i]] = string_data
                            offset += string_len
                        self.resp[topic_name]["symbol"] = self.symbol_token[topic_name]
                        self.__response_output(
                            self.resp[self.dp_sym[topic_id]], "depth"
                        )

                    elif topic_name[:2] == "if":

                        self.index_sym[topic_id] = topic_name
                        self.resp[self.index_sym[topic_id]] = {}

                        # field_count - 21 in scrips , 25 in depth , 6 in index
                        field_count = struct.unpack("B", data[offset : offset + 1])[0]
                        offset += 1

                        for index in range(field_count):
                            value = struct.unpack(">I", data[offset : offset + 4])[0]
                            offset += 4

                            self.resp[self.index_sym[topic_id]][
                                self.index_val[index]
                            ] = value

                        offset += 2

                        multiplier = struct.unpack("H", data[offset : offset + 2])[0]
                        self.resp[self.index_sym[topic_id]]["multiplier"] = multiplier
                        offset += 2

                        precision = struct.unpack("B", data[offset : offset + 1])[0]
                        self.resp[self.index_sym[topic_id]]["precision"] = precision
                        offset += 1

                        val = ["exchange", "exchange_token", "symbol"]
                        for i in range(3):
                            string_len = struct.unpack("B", data[offset : offset + 1])[
                                0
                            ]
                            offset += 1
                            string_data = data[offset : offset + string_len].decode(
                                "utf-8"
                            )
                            self.resp[self.index_sym[topic_id]][val[i]] = string_data
                            offset += string_len
                        self.resp[topic_name]["symbol"] = self.symbol_token[topic_name]

                        self.__response_output(
                            self.resp[self.index_sym[topic_id]], "index"
                        )

                    elif topic_name[:2] == "sf":
                        self.scrips_sym[topic_id] = topic_name
                        self.resp[self.scrips_sym[topic_id]] = {}

                        # field_count - 21 in scrips , 25 in depth , 6 in index
                        field_count = struct.unpack("B", data[offset : offset + 1])[0]
                        offset += 1

                        for index in range(field_count):
                            value = struct.unpack(">I", data[offset : offset + 4])[0]
                            offset += 4
                            self.resp[self.scrips_sym[topic_id]][
                                self.data_val[index]
                            ] = value

                        offset += 2

                        multiplier = struct.unpack("H", data[offset : offset + 2])[0]
                        self.resp[self.scrips_sym[topic_id]]["multiplier"] = multiplier
                        offset += 2

                        precision = struct.unpack("B", data[offset : offset + 1])[0]
                        self.resp[self.scrips_sym[topic_id]]["precision"] = precision
                        offset += 1
                        val = ["exchange", "exchange_token", "symbol"]
                        for i in range(3):
                            string_len = struct.unpack("B", data[offset : offset + 1])[
                                0
                            ]
                            offset += 1
                            string_data = data[offset : offset + string_len].decode(
                                "utf-8"
                            )
                            self.resp[self.scrips_sym[topic_id]][val[i]] = string_data
                            offset += string_len
                        self.resp[topic_name]["symbol"] = self.symbol_token[topic_name]

                        self.__response_output(
                            self.resp[self.scrips_sym[topic_id]], "scrips"
                        )

                elif data_type == 85:  # Full mode datafeed
                    offset += 1
                    topic_id = struct.unpack("H", data[offset : offset + 2])[0]
                    offset += 2

                    field_count = struct.unpack("B", data[offset : offset + 1])[0]
                    offset += 1
                    sf_flag, idx_flag, dp_flag = False, False, False

                    for index in range(field_count):
                        value = struct.unpack(">I", data[offset : offset + 4])[0]
                        offset += 4
                        if field_count == 21:
                            self.resp[self.scrips_sym[topic_id]][
                                self.data_val[index]
                            ] = value
                            sf_flag = True
                        elif field_count == 6:
                            self.resp[self.index_sym[topic_id]][
                                self.index_val[index]
                            ] = value
                            idx_flag = True
                        else:
                            self.resp[self.dp_sym[topic_id]][
                                self.depthvalue[index]
                            ] = value
                            dp_flag = True

                    if sf_flag:
                        self.__response_output(
                            self.resp[self.scrips_sym[topic_id]], "scrips"
                        )
                    elif idx_flag:

                        self.__response_output(
                            self.resp[self.index_sym[topic_id]], "index"
                        )
                    elif dp_flag:
                        self.__response_output(
                            self.resp[self.dp_sym[topic_id]], "depth"
                        )

                elif data_type == 76:  # lite mode datafeed

                    offset += 1
                    topic_id = struct.unpack("H", data[offset : offset + 2])[0]
                    offset += 2
                    sf_flag, idx_flag = False, False
                    if topic_id in self.scrips_sym:

                        for index in range(3):
                            value = struct.unpack(">I", data[offset : offset + 4])[0]
                            offset += 4
                            self.resp[self.scrips_sym[topic_id]][
                                self.data_val[index]
                            ] = value
                            sf_flag = True

                    if sf_flag:
                        self.__response_output(
                            self.resp[self.scrips_sym[topic_id]], "scrips"
                        )

        except Exception as e:
            self.logger.error(e)

    def __resume_pause_resp(self, data: bytearray, channeltype: int) -> dict:
        """
        Unpacks and processes the resume/pause response data based on the channel type.

        Args:
            data (bytearray): The response data.
            channeltype (int): The channel type. 7 for pause and 8 for resume.

        Returns:
            dict: The resume/pause response as a dictionary with keys 'code', 'message', and 's'.
        """
        try:
            offset = 5

            # Unpack the field length
            field_length = struct.unpack("!H", data[offset : offset + 2])[0]
            offset += 2

            # Extract the string value and decode it
            string_val = data[offset : offset + field_length].decode("utf-8")
            offset += field_length

            if string_val == "K":
                if channeltype == 7:
                    self.On_message(
                        {
                            "code": defines.SUCCESS_CODE,
                            "message": defines.CHANNEL_PAUSED,
                            "s": defines.SUCCESS,
                        }
                    )
                else:
                    self.On_message(
                        {
                            "code": defines.SUCCESS_CODE,
                            "message": defines.CHANNEL_RESUMED,
                            "s": defines.SUCCESS,
                        }
                    )
            else:
                if channeltype == 7:
                    self.On_error(
                        {
                            "code": defines.PAUSE_ERROR_CODE,
                            "message": defines.CHANNEL_CHANGE_FAIL,
                            "s": defines.ERROR,
                        }
                    )
                else:
                    self.On_error(
                        {
                            "code": defines.RESUME_ERROR_CODE,
                            "message": defines.CHANNEL_CHANGE_FAIL,
                            "s": defines.ERROR,
                        }
                    )

        except Exception as e:
            self.logger.error(e)

    def __response_msg(self, data: bytearray):
        """
        Processes the response message based on the response type and calls the corresponding function.

        Args:
            data (bytearray): The response data.

        """
        try:

            _, resp_type = struct.unpack("!HB", data[:3])
            if resp_type == 1:  # Authentication response
                self.__auth_resp(data)

            elif resp_type == 4:  # subsciption response
                self.__subscribe_resp(data)

            elif resp_type == 5:  # Unsubsciption response
                self.__unsubscribe_resp(data)

            elif resp_type == 6:  # Data Feed Response
                self.__datafeed_resp(data)

            elif resp_type == 7 or resp_type == 8:
                self.__resume_pause_resp(data, resp_type)

            elif resp_type == 12:  # Full Mode Data Response
                self.__lite_full_mode_resp(data)

        except Exception as e:

            self.logger.error(e)

    def __symbol_conversion(self, symbolslst: list) -> dict:
        """
        Converts symbols to HSM symbol tokens and returns a dictionary of {hsmtoken: symbol}.

        Args:
            symbolslst (list): A list of symbols to convert.

        Returns:
            dict: A dictionary mapping HSM symbol tokens to symbols.
        """
        try:

            wrong_symbols = []
            flag = False
            symbol_dict = {}
            total_symbols = len(symbolslst)
            if (
                len(self.scrips_per_channel[self.channel_num]) > 200
                or total_symbols > 200
                and len(self.scrips_per_channel[self.channel_num]) + total_symbols > 200
            ):
                self.On_error(
                    {
                        "code": defines.LIMIT_EXCEED_CODE,
                        "message": defines.LIMIT_EXCEED_MSG,
                        "s": defines.ERROR,
                    }
                )
                return None

            symbol_chunks = [
                symbolslst[i : i + 50] for i in range(0, total_symbols, 50)
            ]
            conv = SymbolConversion(self.__access_token, self.data_type)
            for symbols in symbol_chunks:
                symbol_value = conv.symbol_to_hsmtoken(symbols)
                symbol_dict.update(symbol_dict, **symbol_value[0])
                if type(symbol_value[1]) == list and len(symbol_value[1]) > 0:

                    wrong_symbols += symbol_value[1]
                    flag = True
            if flag:
                self.On_error(
                    {
                        "code": defines.INVALID_CODE,
                        "message": defines.INVALID_SYMBOLS,
                        "s": defines.ERROR,
                        "symbols": wrong_symbols,
                    }
                )

            return symbol_dict

        except Exception as e:
            self.logger.error(e)

    def __channel_resume_pause(self):
        """
        Pauses the active channel and resumes the specified channel if necessary.

        If the WebSocket object (__ws_object) is not None and there is an active channel (active_channel)
        that is different from the specified channel (channelNum), the function creates and appends a pause message
        for the active channel to the message list. If the specified channel is already in the running_channels set,
        the function creates and appends a resume message for the specified channel to the message list.

        Finally, it updates the running_channels set and sets the active_channel to the specified channel (channelNum).

        """
        try:
            if (
                self.__ws_object is not None
                and self.active_channel is not None
                and self.active_channel != self.channel_num
            ):
                message = self.__channel_pause_msg(self.active_channel)
                self.message.append(message)

                if self.channel_num in self.running_channels:
                    message = self.__channel_resume_msg(self.channel_num)
                    self.message.append(message)
            self.running_channels.add(self.channel_num)
            self.active_channel = self.channel_num

        except Exception as e:
            self.logger.error(e)

    def channel_resume(self, channel: int) -> None:
        """
        Resumes the specified channel.

        Args:
            channel (int): The channel number to resume.
        """
        try:
            self.channel_num = channel
            self.__channel_resume_pause()

        except Exception as e:
            self.logger.error(e)

    def On_message(self, message: dict) -> None:
        """
        Handles the received message.

        Args:
            message (str): The received message.
        """

        if self.OnMessage is not None:
            self.OnMessage(message)
        else:
            if self.write_to_file:
                self.logger.debug(f"Response:{message}")
            else:
                print(f"Received response: {message}")

    def __send_message(self, message: str) -> None:
        """
        Sends a message through the WebSocket connection.

        Args:
            message (str): The message to send.
        """
        with self.websocket_lock:
            if self.__ws_object is not None:
                self.__ws_object.send(message, websocket.ABNF.OPCODE_BINARY)

    def __process_message_queue(self) -> None:
        """
        Processes the message queue by sending messages sequentially.
        """

        while True:
            if len(self.message) > 0:
                message = self.message.pop(0)
                self.__send_message(message)
                time.sleep(0.6)
            else:
                pass

    def On_error(self, message: dict) -> None:
        """
        Handles the error message.

        Args:
            message (str): The error message.
        """
        if self.OnError is not None:
            self.OnError(message)
        else:
            if self.write_to_file:
                self.logger.debug(f"ERROR Response:{message}")
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

    def __on_open(self, ws) -> None:
        """
        Handles the WebSocket connection open event.

        Args:
            ws (websocket.WebSocketApp): The WebSocket object.
        """
        if self.__ws_object is None:
            self.__ws_object = ws
            self.message_thread = Thread(target=self.__process_message_queue)
            self.ping_thread = Thread(target=self.__ping)
            self.message_thread.start()
            self.ping_thread.start()
            message = self.__access_token_msg()
            self.message.append(message)
            if self.lite:
                message = self.__lite_mode_msg()
                self.message.append(message)
            else:
                message = self.__full_mode_msg()
                self.message.append(message)

    def __on_close(self, ws, close_code, close_reason):
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
                    "s": defines.SUCCESS,
                }
            )

    def __ping(self):
        while (
            self.__ws_object is not None
            and self.__ws_object.sock
            and self.__ws_object.sock.connected
        ):
            self.__ws_object.send("Ping")
            time.sleep(10)

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

                ws = websocket.WebSocketApp(
                    self.__url,
                    on_message=lambda ws, msg: self.__response_msg(msg),
                    on_error=lambda ws, msg: self.On_error(msg),
                    on_close=lambda ws, close_code, close_reason: self.__on_close(
                        ws, close_code, close_reason
                    ),
                    on_open=lambda ws: self.__on_open(ws),
                )
                self.ws_thread = Thread(target=ws.run_forever)
                self.ws_thread.daemon = self.background_flag
                self.ws_thread.start()

        except Exception as e:

            self.logger.error(e)

    def close_connection(self) -> None:
        """
        Closes the WebSocket connection 

        """

        if self.__ws_object:
            self.restart_flag = False
            self.__ws_object.close()
            self.__ws_object = None
            self.ws_thread.join()
            self.message_thread.join()
            self.ping_thread.join()

    def keep_running(self):
        """
        Starts an infinite loop to keep the program running.

        """
        self.__ws_run = True
        t = Thread(target=self.infinite_loop)
        t.start()

    def infinite_loop(self):
        while self.__ws_run:
            pass

    def unsubscribe(
        self, symbols: list, data_type: str = "SymbolUpdate", channel: int = 1
    ):
        """
        Unsubscribes from real-time data updates for the specified symbols.

        Args:
            symbols (list): A list of symbols to unsubscribe from.
            data_type (str, optional): The type of data to unsubscribe from. Defaults to "SymbolUpdate".
            channel (int, optional): The channel to use for unsubscription. Defaults to 1.
        """
        try:
            self.data_type = data_type
            self.symbols = symbols
            self.channel_num = channel
            self.__channel_resume_pause()
            self.channel_symbol = self.__symbol_conversion(symbols)
            self.unsub_symbol = list(self.channel_symbol.keys())
            for symb in self.unsub_symbol:
                if symb not in self.scrips_count[self.channel_num]:
                    self.unsub_symbol.remove(symb)

            if len(self.unsub_symbol) != 0:
                total_symbols = len(self.unsub_symbol)
                symbol_chunks = [
                    self.unsub_symbol[i : i + 100] for i in range(0, total_symbols, 100)
                ]
                for symbols in symbol_chunks:
                    message = self.__unsubscription_msg(symbols)
                    self.message.append(message)
            else:
                self.On_error(
                    {
                        "code": defines.INVALID_CODE,
                        "message": defines.WRONG_CHANNEL_MSG,
                        "s": defines.ERROR,
                    }
                )

        except Exception as e:
            self.logger.error(e)

    def subscribe(
        self, symbols: list, data_type: str = "SymbolUpdate", channel: int = 1
    ):
        """
        Subscribes to real-time data updates for the specified symbols.

        Args:
            symbols (list): A list of symbols to subscribe to.
            data_type (str, optional): The type of data to subscribe to. Defaults to "SymbolUpdate".
            channel (int, optional): The channel to use for subscription. Defaults to 1.
        """
        try:
            self.init_connection()
            time.sleep(2)

            self.data_type = data_type
            self.symbols = symbols
            self.channel_num = channel
            self.__channel_resume_pause()
            self.channel_symbol = self.__symbol_conversion(symbols)
            if self.channel_symbol is None:
                return
            self.symbol_token.update(self.symbol_token, **self.channel_symbol)
            self.scrips_count[self.channel_num] = list(self.channel_symbol.keys())
            total_symbols = len(self.scrips_count[self.channel_num])
            symbol_chunks = [
                self.scrips_count[self.channel_num][i : i + 100]
                for i in range(0, total_symbols, 100)
            ]
            for symbols in symbol_chunks:
                message = self.__subscription_msg(symbols)
                self.message.append(message)

        except Exception as e:
            self.logger.error(e)
