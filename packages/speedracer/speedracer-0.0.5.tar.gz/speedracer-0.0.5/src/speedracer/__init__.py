r'''

.. include:: ../../README.md

'''

import asyncio
import datetime
from enum import Enum
import errno
import hashlib
import logging
import os
from pathlib import Path
import ssl
import time
from typing import Union, Optional, Callable, Tuple, List, Dict, Iterable
from urllib.parse import urlparse, urlunparse

import jwt
import requests
import nats
from nats.errors import TimeoutError as NatsTimeoutError

logging.basicConfig()
logging.getLogger(__name__).setLevel(logging.INFO)

class JWTManager:
    """A class for conveniently working with JSON Web Tokens (JWTs)
    Example:
        ```python
        manager = JWTManager('https://gateway.com/getjwt')

        # get a JWT
        token = manager.get()

        # get HTTP headers dictionary with an Authorization header set
        headers = manager.get_headers()

        # get your Common Name
        name = manager.get_cn()
        ```
    """
    def __init__(self, url:str, cert:Tuple[str, str]=(Path.home().joinpath('.ssh/cert.crt'),
            Path.home().joinpath('.ssh/cert.key')),
            verify:Union[str, bool]=True) -> None:
        '''Create a JWT Manager

        Arguments:
            url: The URL of the API Gateway to fetch JWTs from
            cert: A Tuple containing the paths to the certificate and
                key to use with the API Gateway. By default, looks in the
                user's home directory for the files cert.crt and cert.key
            verify: A bool or a path to a Certificate Authority. Passed to the requests library
        '''

        if not os.path.isfile(cert[0]):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), cert[0])

        if not os.path.isfile(cert[1]):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), cert[1])

        if not isinstance(verify, bool) and not os.path.isfile(verify):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), verify)

        self.token:Optional[Union[str, None]] = None
        '''The most recently fetched JWT. Use the `get` method instead of accessing this directly'''
        self.url:str = url
        '''The URL of the API Gateway to fetch JWTs from'''
        self.cert:Tuple[str, str] = cert
        '''A Tuple containing the paths to the certificate and key to use with the API Gateway'''
        self.verify:Union[str, bool] = verify
        '''A bool or a path to a Certificate Authority. Passed to the requests library'''

    def __is_expired(self) -> None:
        in_five_minutes = time.mktime(
            (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).timetuple())
        claims = jwt.decode(self.token, options={'verify_signature': False})
        if 'exp' in claims:
            return claims['exp'] < in_five_minutes
        return False

    def __get_jwt(self) -> None:
        try:
            resp = requests.get(self.url, cert=self.cert, verify=self.verify, timeout=10)
            resp.raise_for_status()
            self.token = resp.text.strip()
        except requests.exceptions.RequestException:
            logging.getLogger(__name__).exception("fetching JWT")

    def get(self) -> str:
        '''Returns a cached JWT or a new one if the cached JWT is close to expiration

        Example:
            ```python
            token = manager.get()
            ```

        Returns:
            str: JWT
        '''
        if self.token is None or self.__is_expired():
            self.__get_jwt()
        return self.token

    def get_headers(self) -> Dict:
        '''Returns a Dict containing an Authorization HTTP header for use with Autobahn APIs

        Example:

            ```python
            headers = manager.get_headers()
            ```

        Returns:
            Dict: contains Authorization header

                {
                    'Authorization': 'Bearer <jwt-here>'
                }
        '''
        return {
            'Authorization': 'Bearer ' + self.get()
        }

    def get_cn(self) -> str:
        '''Extracts the CN claim from a JSON Web Token

        Example:
            ```python
            name = manager.get_cn()
            ```

        Returns:
            str: common name extracted from the JWT
        '''
        return jwt.decode(self.get(), options={'verify_signature': False})['CN']

class Offset(str, Enum):
    '''The offset to start consuming messages from'''
    BEGIN = 'begin'
    NOW = 'now'

class Connection:
    '''Connect to Autobahn'''
    def __init__(self, url:str, cert:Tuple[str, str]=(Path.home().joinpath('.ssh/cert.crt'),
                Path.home().joinpath('.ssh/cert.key')),
            ca_bundle:Optional[str]=None) -> None:
        '''
        Example:
            ```python
            conn = Connection('https://mdb-account-server/')
            ```

        Arguments:
          url: URL of the Autobahn MDB account server
          cert: Paths to a PEM formated X.509 certificate and key file
            Defaults to ('$HOME/.ssh/cert.crt', '$HOME/.ssh/cert.key')
          ca_bundle: A path to a PEM encoded certificate authority file
        '''

        if not os.path.isfile(cert[0]):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), cert[0])

        if not os.path.isfile(cert[1]):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), cert[1])

        if ca_bundle and not os.path.isfile(ca_bundle):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ca_bundle)

        def get_urls():
            config_url = urlparse(url)
            config_url = urlunparse(config_url._replace(path='/api/v1/config'))
            try:
                resp = requests.get(config_url, verify=self.verify, timeout=10)
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.SSLError as ssl_error:
                logging.getLogger(__name__).exception('''SSLError getting
service urls. Commonly caused by not providing client certificates or by
not specifying a ca_bundle''')
                raise ssl_error
            except requests.exceptions.RequestException as err:
                logging.getLogger(__name__).exception('getting service urls')
                raise err

        self.cert: Tuple[str, str] = cert
        '''Client certificate. Invalid certificates result in `SSLError`'''
        self.ca_bundle: Optional[str] = ca_bundle
        '''Certificate Authority used to verify server SSL certificates'''
        self.verify: Union[str, bool] = ca_bundle if ca_bundle else True
        '''Verify server SSL certificates. Set to false if a valid ca_bundle is not available.'''
        self.urls: Dict = get_urls()
        '''URLs to Autobahn services (read-only)'''
        self.jwt_manager: JWTManager = JWTManager(self.urls['api_gateway_url'],
                cert=cert, verify=self.verify)
        '''A `JWTManager` for authenticating to Autobahn'''
        self.subscriptions: List = []
        '''An array of all Subscriptions associated with this Connection'''

    async def subscribe(self, dataset:str, offset:Offset=Offset.NOW, batch:int=10,
            callback:Optional[Callable]=None) -> Iterable:
        '''Subscribe to a dataset.

        Example:
            ```python
            sub = await conn.subscribe('mydataset')
            async for msg in sub:
                print(msg.data.decode())
            ```

        Arguments:
            dataset: The slug of the dataset
            offset: The offset to start consuming messages from
            batch: The number of messages retrieved at a time
        '''
        sub = self.Subscription(self.urls, self.jwt_manager, self.ca_bundle,
                dataset, offset, batch, callback)
        await sub.start()
        self.subscriptions.append(sub)
        logging.getLogger(__name__).info("Subscribed to dataset: %s", dataset)
        return sub

    async def close(self):
        '''Close all subscriptions associated with this Connection'''

        # pylint: disable=broad-exception-caught
        # Try closing each subscription

        for sub in self.subscriptions:
            try:
                await sub.close()
            except Exception as ex:
                print('exception closing subscription:', ex)
            self.subscriptions = []


    class Subscription:
        '''A subscription to a dataset. Iterable'''

        # pylint: disable=too-many-instance-attributes

        # pylint: disable=too-many-arguments
        # Only called internally so it is fine

        def __init__(self, urls:Dict, jwt_manager:JWTManager, ca_bundle:Optional[str],
                dataset:str, offset:Offset, batch:int, callback:Optional[Callable]) -> None:
            '''Create a subscription. Use a Connection's `subscribe` method instead

            Arguments:
                urls: A Dict containing URLs to services
                jwt_manager: A `JWTManager` for authenticating to Autobahn
                ca_bundle: Path to a Certificate Authority
                dataset: The slug of the dataset to subscribe to
                offset: The offset to start consuming messages from
                batch: The number of messages the client will pull at a time
                callback: A Callable that takes a NATS message as an
                    argument. Called for each messages received
            '''
            self.verify:Union[str, bool] = ca_bundle if ca_bundle else True
            '''Verify server SSL certificates. Set to false if a valid 
            ca_bundle is not available.'''
            self.urls:Dict = urls
            '''URLs to Autobahn services (read-only)'''
            self.jwt_manager:JWTManager = jwt_manager
            '''A JWTManager for authenticating to Autobahn'''
            self.dataset:str = dataset
            '''The dataset slug for this subscription'''
            self.offset:Offset = offset
            '''The offset to start consuming messages from'''
            self.batch:int = batch
            '''Number of messages the subscription will pull at a time'''
            self.callback:Optional[Callable] = callback
            '''Optional callback that takes a NATS message as an argument'''
            self.__ssl_context:ssl.SSLContext = ssl.create_default_context()
            '''SSL context used by aiohttp'''
            if ca_bundle:
                self.__ssl_context.load_verify_locations(ca_bundle)
            self.__nats_conn = None
            '''NATS Connection'''
            self.__js_ctx = None
            '''NATS JetStream Context'''
            self.__psub = None
            '''NATS Pull Subscription'''
            self.__consumer_name:str = None
            '''NATS Consumer name'''
            self.__cb_task = None
            '''Asyncio Task for message callback'''

            def get_subject() -> str:
                headers = jwt_manager.get_headers()
                headers['Accept'] = 'application/vnd.pgrst.object+json'
                resp = requests.get(
                        f"{urls['registry_url']}/api/v1/datasets?slug=eq.{self.dataset}",
                        headers=headers, verify=self.verify, timeout=10)
                resp.raise_for_status()
                dataset_entry = resp.json()
                subject = f"EVENTS.{self.dataset}"
                if dataset_entry.get('data_object_backend'):
                    if dataset_entry['data_object_backend'] == 'MDB':
                        subject = f"OBJECTS.{self.dataset}"
                elif dataset_entry.get('mdb_object_publish'):
                    subject = f"OBJECTS.{self.dataset}"
                return subject

            self.subject: str = get_subject()
            '''NATS Subject'''

        async def __aiter__(self):
            while True:
                try:
                    msgs = await self.__psub.fetch(self.batch, timeout=10)
                    for msg in msgs:
                        await msg.ack()
                    for msg in msgs:
                        yield msg
                except NatsTimeoutError: # no messages to return yet
                    pass
                except KeyboardInterrupt:
                    break

        async def __call_callback(self):
            async for msg in self:
                self.callback(msg)

        async def start(self):
            '''Start receiving data from the dataset. This is called automatically
            when using `Connection.subscribe()`'''
            def signature(_):
                return bytes('', 'UTF-8')

            def get_mas_jwt() -> bytearray:
                resp = requests.get(f"{self.urls['mas_url']}/api/v1/user/jwt/{self.dataset}",
                        headers=self.jwt_manager.get_headers(), verify=self.verify, timeout=10)
                resp.raise_for_status()
                encoded_token = resp.text.encode()
                return bytearray(encoded_token)

            def get_consumer_name() -> str:
                cn_hash = hashlib.md5(self.jwt_manager.get_cn().encode())
                return cn_hash.hexdigest()[:-1] + '0'


            async def create_conn() -> None:
                self.__nats_conn = await nats.connect(
                        self.urls['nats_websocket_url'],
                        name=f"{self.jwt_manager.get_cn()} ({self.dataset})",
                        signature_cb=signature,
                        user_jwt_cb=get_mas_jwt,
                        tls=self.__ssl_context)
                self.__js_ctx = self.__nats_conn.jetstream()
                self.__consumer_name = get_consumer_name()

            await create_conn()
            await self.__create_sub()

        async def __create_sub(self, start_sequence:Union[int, None]=None,
                start_datetime:Union[datetime.datetime, None]=None) -> None:

            cfg=nats.js.api.ConsumerConfig(inactive_threshold=60.0*60.0*24.0*7.0) # seconds

            if start_sequence is not None:
                cfg.deliver_policy = (
                    nats.js.api.DeliverPolicy.BY_START_SEQUENCE)
                cfg.opt_start_seq = start_sequence
            elif start_datetime is not None:
                cfg.deliver_policy = (
                    nats.js.api.DeliverPolicy.BY_START_TIME)
                cfg.opt_start_time =  start_datetime.replace(
                        tzinfo=datetime.timezone.utc).isoformat()
            elif self.offset == 'new':
                cfg.deliver_policy = nats.js.api.DeliverPolicy.NEW
            else:
                cfg.deliver_policy = nats.js.api.DeliverPolicy.ALL

            self.__psub = await self.__js_ctx.pull_subscribe(
                    subject=self.subject,
                    durable=self.__consumer_name,
                    config=cfg)

            if self.callback and not self.__cb_task:
                self.__cb_task = asyncio.create_task(self.__call_callback())

        async def seek(self, seq_or_datetime: Union[int, datetime.datetime]) -> None:
            '''Move cursor to specified sequence number or datetime

            Example:
                ```python
                await sub.seek(1)
                await sub.seek(datetime.datetime.utcnow() -
                    datetime.timedelta(minutes=5))
                ```

            Arguments:
                seq_or_datetime: Sequence number or datetime to seek to
            '''
            start_sequence = None
            start_datetime = None
            if isinstance(seq_or_datetime, int):
                start_sequence = seq_or_datetime
            elif isinstance(seq_or_datetime, datetime.datetime):
                start_datetime = seq_or_datetime
            else:
                raise TypeError("seek to argument must be int or datetime")
            logging.getLogger(__name__).info('Seeking')
            await self.__psub.unsubscribe()
            await self.__delete_consumer()
            await self.__create_sub(start_sequence, start_datetime)
            logging.getLogger(__name__).info('Finished seeking')

        async def __delete_consumer(self) -> bool:
            stream_name = self.subject.replace('.', '_')
            return await self.__js_ctx.delete_consumer(stream_name, self.__consumer_name)

        async def wait(self, messages:Union[int, None]=None,
                timeout:Union[int, datetime.datetime, datetime.timedelta, None]=None) -> None:
            '''Block until specified number of messages are consumed or specified
            amount of time has elapsed

            Example:
                ```python
                await sub.wait(messages=15)
                await sub.wait(timeout=5)
                ```

            Arguments:
                messages: The number of messages to wait for
                timeout: The number of seconds to wait for, the
                    datetime to wait until, or the timedelta to
                    wait for
            '''
            if messages:
                msgs_target = self.__psub.delivered + messages
                while self.__psub.delivered < msgs_target:
                    await asyncio.sleep(1)
            if timeout:
                if isinstance(timeout, datetime.datetime):
                    await asyncio.sleep((timeout - datetime.datetime.utcnow()).total_seconds())
                elif isinstance(timeout, datetime.timedelta):
                    await asyncio.sleep(timeout.total_seconds())
                else:
                    await asyncio.sleep(timeout)

        async def close(self) -> None:
            '''Close this Subscription'''
            if self.__cb_task:
                self.__cb_task.cancel()
                await asyncio.sleep(0.1)
            await self.__nats_conn.close()
