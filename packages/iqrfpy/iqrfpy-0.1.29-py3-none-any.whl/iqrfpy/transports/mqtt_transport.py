import json
import random
import string
import threading

from typing import Callable, List, Optional, overload
from paho.mqtt.client import Client
from iqrfpy.enums.message_types import MessageType
from iqrfpy.exceptions import TransportNotConnectedError, MessageNotReceivedError, DpaRequestTimeoutError, \
    JsonRequestTimeoutError
from iqrfpy.confirmation import Confirmation
from iqrfpy.response_factory import ResponseFactory
from iqrfpy.transports.itransport import ITransport
from iqrfpy.messages import *

__all__ = [
    'MqttTransportParams',
    'MqttTransport',
]


class MqttTransportParams:

    __slots__ = '_host', '_port', '_client_id', '_user', '_password', '_request_topic', '_response_topic', '_qos', \
        '_keepalive'

    def __init__(self, host: str = 'localhost', port: int = 1883, client_id: Optional[str] = None,
                 user: Optional[str] = None, password: Optional[str] = None, request_topic: Optional[str] = None,
                 response_topic: Optional[str] = None, qos: int = 1, keepalive: int = 60):
        self._validate(port=port, qos=qos)
        self._host = host
        self._port = port
        self._client_id = client_id if client_id is not None else \
            ''.join(random.choice(string.ascii_letters + string.digits) for i in range(16))
        self._user = user
        self._password = password
        self._request_topic = request_topic
        self._response_topic = response_topic
        self._qos = qos
        self._keepalive = keepalive

    def _validate(self, port: int, qos: int):
        self._validate_port(port)
        self._validate_qos(qos)

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value

    @staticmethod
    def _validate_port(port: int):
        if not (1024 <= port <= 65535):
            raise MqttParamsError('Port value should be between 1024 and 65535.')

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value: int):
        self._validate_port(value)
        self._port = value

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value: str):
        self._client_id = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value: Optional[str]):
        self._user = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: Optional[str]):
        self._password = value

    @property
    def request_topic(self):
        return self._request_topic

    @request_topic.setter
    def request_topic(self, value: str):
        self._request_topic = value

    @property
    def response_topic(self):
        return self._response_topic

    @response_topic.setter
    def response_topic(self, value: str):
        self._response_topic = value

    @staticmethod
    def _validate_qos(qos: int):
        if not (0 <= qos <= 2):
            raise MqttParamsError('QoS value should be between 0 and 2.')

    @property
    def qos(self):
        return self._qos

    @qos.setter
    def qos(self, value: int):
        self._validate_qos(value)
        self._qos = value

    @property
    def keepalive(self):
        return self._keepalive

    @keepalive.setter
    def keepalive(self, value: int):
        self._keepalive = value


class MqttTransport(ITransport):

    __slots__ = '_client', '_params', '_callback', '_global_request_timeout', '_cv', '_msg_ids', '_m_type', \
        '_response', '_dpa_timeout', '_received_timeout'

    def __init__(self, params: MqttTransportParams, callback: Optional[Callable] = None,
                 auto_init: bool = False, global_request_timeout: Optional[float] = 5):
        self._client: Optional[Client] = None
        self._params: MqttTransportParams = params
        self._callback: Optional[Callable] = callback
        self._global_request_timeout: float = global_request_timeout
        self._cv: threading.Condition = threading.Condition()
        self._sub_cv: threading.Condition = threading.Condition()
        self._msg_ids: List[str] = []
        self._m_type: Optional[MessageType] = None
        self._response: Optional[IResponse] = None
        self._dpa_timeout: Optional[float] = None
        self._received_timeout: bool = False
        if auto_init:
            self.initialize()

    def initialize(self) -> None:
        self._client = Client(self._params.client_id)
        self._client.on_connect = self._connect_callback
        self._client.on_message = self._message_callback
        self._client.on_subscribe = self._subscribe_callback
        if self._params.user is not None and self._params.password is not None:
            self._client.username_pw_set(self._params.user, self._params.password)
        self._client.connect(self._params.host, self._params.port)
        self._client.loop_start()
        with self._sub_cv:
            self._sub_cv.wait()

    def terminate(self, force: bool = False) -> None:
        self._client.disconnect()
        self._client.loop_stop(force=force)

    def _connect_callback(self, client, userdata, flags, rc):
        # pylint: disable=W0613
        if rc == 0:
            self._client.subscribe(self._params.response_topic, self._params.qos)

    def _subscribe_callback(self, client, userdata, mid, granted_qos):
        # pylint: disable=W0613
        with self._sub_cv:
            self._sub_cv.notify()

    def _message_callback(self, client, userdata, message):
        # pylint: disable=W0613
        payload = json.loads(message.payload.decode('utf-8'))
        try:
            response = ResponseFactory.get_response_from_json(payload)
        except MessageNotReceivedError as err:
            if err.msgid == self._msg_ids[0]:
                self._received_timeout = True
                with self._cv:
                    self._cv.notify()
            return
        if len(self._msg_ids) > 0 and response.msgid == self._msg_ids[0] and response.mtype == self._m_type:
            self._msg_ids.pop(0)
            self._response = response
            with self._cv:
                self._cv.notify()
        if self._callback is not None:
            self._callback(response)

    def is_connected(self) -> bool:
        return self._client.is_connected()

    def print_msg_ids(self):
        print(self._msg_ids)

    def send(self, request: IRequest) -> None:
        self._response = None
        self._m_type = None
        self._dpa_timeout = None
        self._received_timeout = False
        if not self._client.is_connected():
            raise TransportNotConnectedError(f'MQTT client {self._params.client_id} not connected to broker.')
        self._client.publish(
            topic=self._params.request_topic,
            payload=json.dumps(request.to_json()),
            qos=self._params.qos
        )
        if request.nadr == 255:
            return
        self._dpa_timeout = request.dpa_rsp_time
        self._msg_ids.append(request.msgid)
        self._m_type = request.mtype

    def receive(self, timeout: Optional[float] = None) -> Optional[IResponse]:
        if len(self._msg_ids) == 0:
            return None
        timeout_to_use = timeout if timeout is not None else self._global_request_timeout
        with self._cv:
            self._cv.wait(timeout=timeout_to_use)
        if self._response is None:
            msg_id = self._msg_ids.pop(0)
            if self._received_timeout and self._dpa_timeout is not None:
                self._received_timeout = False
                raise DpaRequestTimeoutError(f'DPA request timed out (timeout {self._dpa_timeout} seconds).')
            else:
                if self._received_timeout:
                    self._received_timeout = False
                    raise JsonRequestTimeoutError(
                        f'Response message to request with ID {msg_id} received, but DPA request timed out.'
                    )
                else:
                    raise JsonRequestTimeoutError(
                        f'Response message to request with ID {msg_id} not received within the specified time of '
                        f'{timeout_to_use} seconds.')
        return self._response

    def confirmation(self) -> Confirmation:
        raise NotImplementedError('Method not implemented.')

    def set_receive_callback(self, callback: Callable[[IResponse], None]) -> None:
        self._callback = callback

    @overload
    def send_and_receive(self, request: CoordinatorAddrInfoReq,
                         timeout: Optional[float] = None) -> CoordinatorAddrInfoRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorAuthorizeBondReq,
                         timeout: Optional[float] = None) -> CoordinatorAuthorizeBondRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorBackupReq,
                         timeout: Optional[float] = None) -> CoordinatorBackupRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorBondNodeReq,
                         timeout: Optional[float] = None) -> CoordinatorBondNodeRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorBondedDevicesReq,
                         timeout: Optional[float] = None) -> CoordinatorBondedDevicesRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorClearAllBondsReq,
                         timeout: Optional[float] = None) -> CoordinatorClearAllBondsRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorDiscoveredDevicesReq,
                         timeout: Optional[float] = None) -> CoordinatorDiscoveredDevicesRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorDiscoveryReq,
                         timeout: Optional[float] = None) -> CoordinatorDiscoveryRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorRemoveBondReq,
                         timeout: Optional[float] = None) -> CoordinatorRemoveBondRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorRestoreReq,
                         timeout: Optional[float] = None) -> CoordinatorRestoreRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorSetDpaParamsReq,
                         timeout: Optional[float] = None) -> CoordinatorSetDpaParamsRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorSetHopsReq,
                         timeout: Optional[float] = None) -> CoordinatorSetHopsRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorSetMidReq,
                         timeout: Optional[float] = None) -> CoordinatorSetMidRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorSmartConnectReq,
                         timeout: Optional[float] = None) -> CoordinatorSmartConnectRsp:
        ...

    @overload
    def send_and_receive(self, request: OsReadReq, timeout: Optional[float] = None) -> OsReadRsp:
        ...

    @overload
    def send_and_receive(self, request: EepromReadReq, timeout: Optional[float] = None) -> EepromReadRsp:
        ...

    @overload
    def send_and_receive(self, request: EepromWriteReq, timeout: Optional[float] = None) -> EepromWriteRsp:
        ...

    @overload
    def send_and_receive(self, request: LedgSetOnRsp, timeout: Optional[float] = None) -> LedgSetOnRsp:
        ...

    @overload
    def send_and_receive(self, request: LedgSetOffReq, timeout: Optional[float] = None) -> LedrSetOffRsp:
        ...

    @overload
    def send_and_receive(self, request: LedgPulseReq, timeout: Optional[float] = None) -> LedgPulseRsp:
        ...

    @overload
    def send_and_receive(self, request: LedgFlashingReq, timeout: Optional[float] = None) -> LedgFlashingRsp:
        ...

    @overload
    def send_and_receive(self, request: LedrSetOnReq, timeout: Optional[float] = None) -> LedrSetOnRsp:
        ...

    @overload
    def send_and_receive(self, request: LedrSetOffReq, timeout: Optional[float] = None) -> LedrSetOffRsp:
        ...

    @overload
    def send_and_receive(self, request: LedrPulseReq, timeout: Optional[float] = None) -> LedrPulseRsp:
        ...

    @overload
    def send_and_receive(self, request: LedrFlashingReq, timeout: Optional[float] = None) -> LedrFlashingRsp:
        ...

    def send_and_receive(self, request: IRequest, timeout: Optional[float] = None) -> Optional[IResponse]:
        self.send(request)
        if request.nadr == 255:
            return None
        return self.receive(timeout)


class MqttParamsError(Exception):
    pass
