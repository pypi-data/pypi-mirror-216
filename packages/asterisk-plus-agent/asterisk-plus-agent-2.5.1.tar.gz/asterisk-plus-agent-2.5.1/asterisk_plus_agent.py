# TODO: Receive sentry SDK from billing. Re-activate Sentry on sentry_reload method

import asyncio
import base64
import subprocess
import click
import functools
import json
import hashlib
import inspect
import io
import logging
import logging.config
import os
import re
import time
import sys
from urllib.parse import urljoin
import uuid
import yaml
import aioboto3
from aio_odoorpc import AsyncOdooRPC
from aiorun import run
import httpx
from panoramisk import Manager, Message
import wave
import lameenc

__version__ = '2.5.1'


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
        data = base64.b64encode(source_code).decode()
        return data

    async def load_config(self):
        with open('config.yaml') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            if not config:
                logger.error('Bad config.yaml, exit.')
                sys.exit(0)
        try:
            # Next load config from the billing
            r = None
            async with httpx.AsyncClient() as client:                
                r = await client.post(
                    urljoin(config['api_url'], 'app/asterisk_plus/config'),
                    json={
                        'source_code': self.get_source(),
                    },
                    headers={
                        'x-api-key': config['api_key'],
                        'x-instance-uid': config['instance_uid']})
                r.raise_for_status()
                self.config = r.json()
        except Exception as e:
            reason = r and r.text or e
            logger.error('Init config: %s', reason)
            sys.exit(0)
        # Check versions
        major_version = float('.'.join(__version__.split('.')[:2]))
        if float(self.config['asterisk_plus_version']) != major_version:
            logger.error('Asterisk Plus module version is %s, but your Agent version is %s, upgrade the Agent!',
                self.config['asterisk_plus_version'], __version__)
            sys.exit(1)
        # Finally overwrite with local values
        self.config.update(config)
        logger.debug(json.dumps(self.config, indent=2))
        logger.info('Config loaded.')

    async def start(self):        
        # Install signal handlers
        try:
            await self.load_config()
        except Exception as e:
            logger.exception(e)
            sys.exit(1)
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
            args = data.get('args', [])
            if not isinstance(args, list):
                args = [args]
            kwargs = data.get('kwargs', {})
            if args and args != [None]:
                res = await method(*args, **kwargs)
            else:
                res = await method()
            # Deliver result
            if data.get('res_model') and data.get('res_method'):
                if data.get('pass_back'):
                    await self.odoo_execute(data['res_model'], data['res_method'], res, data['pass_back'])
                else:
                    await self.odoo_execute(data['res_model'], data['res_method'], res)
            # Notify with result
            if data.get('res_notify_uid'):
                await self.notify_user(str(res), data['res_notify_uid'],
                    data.get('res_notify_title'))
        except Exception as e:
            logger.exception('RPC Message error: %s', e)


    async def agent_reload_config(self):
        await self.load_config()
        await self.connect_odoo()

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
        if not event.get('Event'):
            return        
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
                await self.send_event(handler, event)
                logger.debug('Handler %s-%s has been published', handler['id'], handler['name'])
            except Exception:
                logger.exception('Handler %s-%s not handle event:', handler['id'], handler['name'])

    async def send_event(self, handler, event):
        if self.subscription_enable != '1':
            logger.error('Ignoring event, subscription is not enabled.')
        try:
            logger.info('Event: %s, exten: %s', event.get('Event'), event.get('Exten'))
            await self.odoo_execute(handler['model'], handler['method'], event)
        except Exception as e:
            if 'Access Denied' in str(e):
                logger.error('Odoo access error, please do not change billing password manually!')
            else:
                logger.error('Send event error: %s', e)

    async def check_event(self, event):
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    urljoin(self.config['api_url'], 'app/asterisk_plus/event'),
                    headers={
                        'x-api-key': self.config['api_key'],
                        'x-instance-uid': self.config['instance_uid']
                    },
                    json={
                        'event': event['Event'],
                        'unique_id': event['Uniqueid']
                    }
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
        if os.environ.get('ODOO_TRACE_RPC'):
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

    async def recording_get_file(self, file_path, file_format='wav', mp3_bitrate=96, mp3_quality=4):
        file_name = os.path.basename(file_path)
        try:
            res = {}
            mp3_conversion_done = False
            # Get Asterisk config
            if file_format == 'mp3':
                loop = asyncio.get_running_loop()
                mp3_data = await loop.run_in_executor(None, functools.partial(self.convert_to_mp3,
                    file_path,
                    mp3_bitrate,
                    mp3_quality))
                if mp3_data:
                    res['file_name'] = file_name.replace('.wav', '.mp3')
                    res['file_data'] = base64.b64encode(mp3_data).decode()
                    mp3_conversion_done = True
            if file_format == 'wav' or not mp3_conversion_done:
                # If we failed to get MP3 send wav anyway
                res['file_name'] = file_name
                res['file_data'] = base64.b64encode(open(file_path, 'rb').read()).decode()
            return res
        except Exception as e:
            logger.exception('Cannot get recording for %s:', file_path)
            return {'error': str(e)}

    def convert_to_mp3(self, file_path, bit_rate, quality):
        try:
            # Reduce priority.
            try:
                nice_level = int(os.environ.get('MP3_ENCODER_NICE', 10))
            except ValueError:
                logger.warning('Wrong MP3_ENCODER_NICE, defaulting to 10.')
                nice_level = 10
            os.nice(nice_level)
            file_data = open(file_path, 'rb')
            #io_data = io.BytesIO(file_data)
            started = time.time()
            wav_data = wave.open(file_data)
            num_channels = wav_data.getnchannels()
            sample_rate = wav_data.getframerate()
            num_frames = wav_data.getnframes()
            pcm_data = wav_data.readframes(num_frames)
            logger.debug(
                'Encoding Wave file. Number of channels: '
                '{}. Sample rate: {}, Number of frames: {}'.format(
                num_channels, sample_rate, num_frames))
            wav_data.close()
            encoder = lameenc.Encoder()
            encoder.set_bit_rate(bit_rate)
            encoder.set_in_sample_rate(sample_rate)
            encoder.set_channels(num_channels)
            encoder.set_quality(quality)  # 2-highest, 7-fastest
            mp3_data = encoder.encode(pcm_data)
            mp3_data += encoder.flush()
            file_name = os.path.basename(file_path)
            logger.info('Encoding of %s took %.2f seconds.', file_name, time.time() - started)
            return mp3_data
        except Exception as e:
            logger.exception('Convert MP3 error:')
            return ''


async def start():
    agent = AsteriskPlusAgent()
    asyncio.gather(        
        agent.start(),
        agent.rpc_message_loop(),
        agent.ami_start())
    

@click.group()
def main():
    pass

@main.command(help='Call a command.')
@click.argument('odoo_url')
@click.option('--skip-ami-setup', is_flag=True)
@click.option('--asterisk', default='/usr/sbin/asterisk', show_default=True)
def init(odoo_url, skip_ami_setup, asterisk):
    # First create AMI config
    config = {}
    if not skip_ami_setup:
        config.update(create_ami_config(asterisk))
    config.update(load_config_from_odoo(odoo_url))
    # Save config
    curdir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(curdir, 'config.yaml')
    open(config_path, 'w').write(yaml.dump(config))
    logger.info('Initialization complete. You can start the Agent now.')


def load_config_from_odoo(odoo_url):
    logger.info('Connecting to %s...', odoo_url)
    try:
        r = httpx.post(
            urljoin(odoo_url, '/asterisk_plus/agent'),
            json={'init': True})
        r.raise_for_status()
        data = r.json()
        return data
    except Exception:
        logger.error('Initialize error: %s', r.text)
        sys.exit(1)

def create_ami_config(asterisk_executable):
    # Check if for manager.conf contains includes.
    if not os.path.exists('/etc/asterisk/manager.conf'):
        logger.error('/etc/asterisk/manager.conf not found. Do a manual setup and init with --skip-ami-setup option.')
        sys.exit(1)
    # Check for Asterisk executable    
    if not os.path.exists(asterisk_executable):
        logger.error('Asterisk executable %s not found, specify full path with --asterisk option.', asterisk_executable)
        sys.exit(0)
    # Check for include dirs
    if not os.path.isdir('/etc/asterisk/manager.conf.d'):
        logger.error('Directory /etc/asterisk/manager.conf.d not found, Do a manual setup and init with --skip-ami-setup option.')
    # Check AMI port
    re_ami_port = re.compile('^port = ([0-9]+)', re.MULTILINE)
    port_found = re_ami_port.search(open('/etc/asterisk/manager.conf').read())
    if not port_found:
        logger.warning('Cannot get port option from manager.conf, using default 5038!')
        ami_port = 5038
    else:
        ami_port = int(port_found.group(1))
    # Create a configuration and place it there.
    ami_password = str(uuid.uuid4())
    ami_config = """
[asterisk_plus_agent]
secret={}
timestampevents = yes
displayconnects = yes
read=call,dialplan
write=originate
deny=0.0.0.0/0.0.0.0
permit=127.0.0.0/255.0.0.0
allowmultiplelogin=no
""".format(ami_password)
    open('/etc/asterisk/manager.conf.d/asterisk_plus_agent.conf', 'w').write(ami_config)
    # Connect to Asterisk and apply
    try:
        res = subprocess.check_call('{} -rx "manager reload"'.format(asterisk_executable),
            shell=True)
    except Exception:
        logger.error('Cannot apply AMI configuration.')
        sys.exit(1)
    # Check that config is applied.
    try:
        res = subprocess.check_output('{} -rx "manager show user asterisk_plus_agent"'.format(asterisk_executable),
            shell=True, universal_newlines=True)
        if 'username: asterisk_plus_agent' not in str(res):
            logger.error('Asterisk does not see [asterisk_plus_agent] AMI account. Check that /etc/asterisk/manager.conf.d is included from /etc/asterisk/manager.conf!')
            sys.exit(0)
    except Exception:
        logger.error('Cannot apply AMI configuration.')
        sys.exit(1)
    # All is fine!
    logger.info('Asterisk Plus Agent AMI config placed in /etc/asterisk/manager.conf.d/asterisk_plus_agent.conf.')
    logger.info('Asterisk has been reloaded to apply this AMI account.')
    return {
        'ami_user': 'asterisk_plus_agent',
        'ami_password': ami_password,
        'ami_host': 'localhost',
        'ami_port': ami_port,
    }

if __name__ == '__main__':    
    curdir = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(curdir, 'config.yaml')):
        run(start())
    else:
        main()

