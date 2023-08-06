# TODO: Receive sentry SDK from billing. Re-activate Sentry on sentry_reload method

import asyncio
import base64
import yaml
import json
import hashlib
import inspect
import logging
import logging.config
import os
import time
import sys
from urllib.parse import urljoin
import yaml
import aioboto3
from aio_odoorpc import AsyncOdooRPC
from aiorun import run
import httpx
from panoramisk import Manager, Message

__version__ = '1.0'
__asterisk_plus_minimal_version__ = 2.5

if os.environ.get('SENTRY_DSN'):
    import sentry_sdk
    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        traces_sample_rate=1.0)    

LOG_CONFIG = """version: 1
formatters:
    default:
        format: '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'

handlers:
    console:
        class: logging.StreamHandler
        formatter: default
root:
    level: {}
    handlers: [console]
""".format(os.environ.get('LOG_LEVEL', 'INFO').upper())

config = yaml.safe_load(LOG_CONFIG)
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)



class AsteriskPlusAgent:
    manager = None
    odoo = None
    odoo_connected_event = asyncio.Event()
    ami_connected_event = asyncio.Event()
    # Dictionary to store channels for accounting
    current_channels = {}
    config = {}


############### SYSTEM #################################

    def get_source(self):
        script_path = inspect.getfile(inspect.currentframe())
        source_code = open(script_path, 'rb').read()
        encoded = base64.b64encode(source_code)
        return encoded

    async def load_config(self):        
        try:
            # First load config from file
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f)
            # Next load config from the billing
            source_code = self.get_source()
            async with httpx.AsyncClient() as client:
                print(1)
                r = await client.post(
                    urljoin(config['api_url'], 'app/asterisk_plus/config'),
                    json={
                        'source_code': ''#source_code,
                    },
                    headers={
                        'x-api-key': config['api_key'],
                        'x-instance-uid': config['instance_uid']})
                print(2)
                r.raise_for_status()
                self.config = r.json()
        except Exception as e:
            logger.error('Cannot load config: %s', r.text)
            sys.exit(0)
        # Check versions
        if float(self.config['asterisk_plus_version']) < __asterisk_plus_minimal_version__:
            logger.error('You have Asterisk Plus version %s installed. Minimal required version is %s',
                self.config['asterisk_plus_version'], __asterisk_plus_minimal_version__)
            sys.exit(1)
        # Finally overwrite with local values
        self.config.update(config)
        logger.debug(json.dumps(self.config, indent=2))
        logger.info('Config loaded.')

    async def start(self):        
        # Install signal handlers
        await self.load_config()
        # Connect to Odoo.
        retry = 0
        while True:
            if await self.connect_odoo():
                # Start failed queries worker.
                # asyncio.ensure_future(self.failed_request_worker())
                break
            else:
                retry += 1
                if retry > 30:
                    retry = 1
                logger.info('Retry in %s seconds...', retry * 2)
                await asyncio.sleep(retry * 2)
        
    async def rpc_message_loop(self):
        try:
            await self.odoo_connected_event.wait()
            session = aioboto3.Session()
            async with session.client('sqs', region_name='eu-central-1') as sqs_client:
                # TODO: Purge queue on startup. 
                while True:
                    logger.debug('Checking RPC queue...')
                    response = await sqs_client.receive_message(
                        QueueUrl=self.config['event_queue_url'],
                        MaxNumberOfMessages=1,
                        WaitTimeSeconds=20
                    )
                    messages = response.get('Messages', [])
                    if messages:
                        message = messages[0]
                        receipt_handle = message['ReceiptHandle']
                        await sqs_client.delete_message(
                            QueueUrl=self.config['event_queue_url'],
                            ReceiptHandle=receipt_handle
                        )
                        asyncio.ensure_future(self.rpc_message(message))
        except Exception as e:
            logger.exception('RPC Message error:')

    async def rpc_message(self, message):
        data = {}
        try:
            data = json.loads(message['Body'])
            # Replace . with _ and find the method
            method = getattr(self, data['fun'].replace('.', '_'), False)
            if not method:                
                raise Exception('Method %s not found' % data['fun'])
            args = data['args']
            if not isinstance(args, list):
                args = [args]
            kwargs = data['kwargs']
            if args and args != [None]:
                res = await method(*args, **kwargs)
            else:
                res = await method()
            # Deliver result
            if data['res_model'] and data['res_method']:
                if data['pass_back']:
                    await self.odoo_execute(data['res_model'], data['res_method'], res, data['pass_back'])
                else:
                    await self.odoo_execute(data['res_model'], data['res_method'], res)
            # Notify with result
            if data['res_notify_uid']:
                await self.notify_user(str(res), data['res_notify_uid'], data['res_notify_title'])
        except Exception as e:
            logger.exception('RPC Message error: %s', e)


################### AMI ################################

    async def ami_start(self):
        try:
            await self.odoo_connected_event.wait()
            manager = Manager(
                host=self.config['ami_host'],
                port=self.config['ami_port'],
                username=self.config['ami_user'],
                secret=self.config['ami_password'],
                ping_delay=10,  # Delay after start
                ping_interval=10,  # Periodically ping AMI (dead or alive)
                reconnect_timeout=2,  # Timeout reconnect if connection lost
            )
            manager.on_login = self.on_login
            manager.on_connect = self.on_connect
            manager.on_disconnect = self.on_disconnect
            self.manager = manager
            logger.info('Connecting to AMI at %s@%s:%s',
                self.config['ami_host'],
                self.config['ami_user'],
                self.config['ami_port']
            )
            return manager.connect(run_forever=False, on_shutdown=self.on_shutdown)
        except Exception:
            logger.exception('AMI start error: ')

    def on_login(self, mngr):
        logger.info('AMI connected.')

    def on_disconnect(self, mngr, exc):
        logger.info(
            'AMI disconnect, error: %s', exc)

    def on_connect(self, mngr):
        evmap = set([k['name'] for k in self.config['events_map']])
        for event in evmap:
            logger.info('Register AMI event: %s', event)
            self.manager.register_event(event, self.send_ami_event)

    async def on_shutdown(self, mngr):
        logger.info(
            'Shutdown AMI connection on %s:%s' % (mngr.config['host'], mngr.config['port'])
        )

    async def asterisk_manager_action(self, action, as_list=None):        
        logger.info('Received AMI action: %s', action['Action'])
        if not self.manager or not self.manager._connected:
            logger.error('AMI not connected. Dropping action.')
            return {}
        res = await self.manager.send_action(action, as_list=as_list)
        logger.debug('AMI reply: %s', res)
        if isinstance(res, list):
            return dict(res[0].items())
        else:
            return dict(res.items())

    async def send_ami_event(self, manager, event):
        event = dict(event)
        logger.debug('Event: %s', event)
        handlers = [k for k in self.config['events_map'] if k['name'] == event.get('Event')]
        logger.debug('Handlers: %s', handlers)
        # Call handlers.
        for handler in handlers:
            try:                
                if handler.get('condition'):
                    # Handler has a condition so evaluate it first.
                    try:
                        # TODO: Create a more secure eval context?
                        res = eval(handler['condition'],
                                None, {'event': event})
                        if not res:
                            # The confition evaluated to False so do not send.                        
                            logger.debug('Handler %s evaluated to False', handler['id'])
                            continue
                    except Exception:
                        logger.exception(
                            'Error evaluating condition: %s, event: %s',
                            handler['condition'], event)
                        # The confition evaluated to error so do not send.
                        continue                
                # Sometimes it's required to send event to Odoo with a delay.
                if handler.get('delay'):
                    logger.debug('Handler %s sleep %s before send...', handler['id'], handler['delay'])
                    await asyncio.sleep(float(handler['delay']))
                else:
                    logger.debug('Delay for handler %s not set', handler['id'])
                if await self.check_event(event):
                    await self.send_event(handler, event)
                logger.debug('Handler %s-%s has been published', handler['id'], handler['name'])
            except Exception:
                logger.exception('Handler %s-%s not handle event:', handler['id'], handler['name'])

    async def send_event(self, handler, event):
        try:
            await self.odoo_execute(handler['model'], handler['method'], event)
        except Exception as e:
            logger.error('Send event error: %s', e)

    async def check_event(self, event):
        if event.get('Event') not in ['Newchannel', 'Hangup']:
            return True
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    urljoin(self.config['api_url'], 'app/asterisk_plus/event'),
                    headers={
                        'x-api-key': self.config['api_key'],
                        'x-instance-uid': self.config['instance_uid']
                    },
                    json={'event': event['Event']}
                )
                r.raise_for_status()
                return True
        except Exception as e:
            logger.error(r.text)

    ###########################  ODOO CONNECTION ##############################
        
    async def connect_odoo(self):
        try:
            odoo_user = str(self.config['odoo_user'])
            password = str(self.config['odoo_password'])
            url = self.config['odoo_url']
            logger.info('Connecting to Odoo at %s', url)
            session = httpx.AsyncClient(base_url=url + '/jsonrpc', follow_redirects=True)
            self.odoo = AsyncOdooRPC(database=self.config['odoo_db'], username_or_uid=odoo_user ,
                                password=password, http_client=session)
            logged = await self.odoo.login()
            if not logged:
                logger.error('Cannot login. Check user and password.')
                return False
            logger.info('Connected to Odoo.')
            self.odoo_connected_event.set()
            return True
        except Exception as e:
            if 'Somehow the response id differs from the request id' in str(e):
                logger.error('HTTPS redirection issue, use 308 Permanent Redirect.')
            elif 'FATAL:  database' in str(e):
                logger.error('Database %s does not exist.', db)
            else:
                logger.error('Odoo connect error: %s', e)

    async def odoo_execute(self, model, method, args, kwargs={}):
        logger.debug('Odoo Execute %s.%s(%s, %s)', model, method, args, kwargs)
        start = time.time()
        res = await self.odoo.execute_kw(
            model_name=model,
            method=method,
            args=args,
            kwargs=kwargs
        )
        req_time = time.time() - start
        logger.info('Execute %s.%s took %.2f seconds.', model, method, req_time)
        return res
        
    async def failed_request_worker(self):
        REQUESTS_INTERVAL = 0.2 # Pause between sending failed requests.
        SLEEP_INTERVAL = 3 # Pause when Odoo is still down.
        MAX_FAILED_REQUESTS = 500 # Maximum requests in the deque.
        FAILED_REQUEST_EXPIRE = 300 # 5 minutes.
        self.failed_requests = deque(maxlen=MAX_FAILED_REQUESTS) # 100 requests maximum.
        while True:
            if len(self.failed_requests) == 0:
                await asyncio.sleep(1)
                continue
            # Take the oldest job.
            logger.info('%s requests in queue, processing...', len(self.failed_requests))
            data = self.failed_requests.popleft()
            failed_time = data.pop('failed_time')
            if time.time() - failed_time > FAILED_REQUEST_EXPIRE:
                # Remove outdated jobs and continue
                logger.info('Discarding expired request %s.%s', data['model'], data['method'])
                await asyncio.sleep(REQUESTS_INTERVAL)
                continue
            try:
                res = await self._odoo_execute(data)
                # Sleep a bit before the next request
                await asyncio.sleep(REQUESTS_INTERVAL)
            except Exception:
                # Move task back in the deck head.
                data['failed_time'] = failed_time
                self.failed_requests.insert(0, data)
                logger.info('Retry request %s.%s error, sleeping...', data['model'], data['method'])
                await asyncio.sleep(SLEEP_INTERVAL)

    async def notify_user(self, message, uid, title='PBX'):
        await self.odoo_execute(
            method='odoopbx_notify',
            model='asterisk_plus.settings',
            args=[message],
            kwargs={
                'title': title,
                'notify_uid': uid
            })

    async def test_ping(self):
        logger.info('Test ping received.')
        return True


async def start():
    agent = AsteriskPlusAgent()
    asyncio.gather(        
        agent.start(),
        agent.rpc_message_loop(),
        agent.ami_start())


def main():
    run(start())    

if __name__ == '__main__':    
    main()


