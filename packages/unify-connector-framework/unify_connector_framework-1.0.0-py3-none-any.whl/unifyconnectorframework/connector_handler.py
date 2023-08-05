# Copyright 2021 Element Analytics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Abstract class construction to handle the schedule and other triggers
"""


from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from time import sleep
from abc import ABC, abstractmethod
import logging
import json
import random
import string

from enum import Enum

from croniter import croniter
import keyring

class Status(Enum):
    '''
    Enumeration used to check the status of both connector and scheduler
    '''
    IDLE = 0
    RUNNING = 1

class ConnectorHandler(ABC):
    '''
    Abstract class to handle connectors in an on-premise environment with triggers like a schedule
    '''
    def __init__(self, name, config=None):
        """
        Instantiate a new ConnectorHandler class

        :type name: string
        :param name: Name of the Connector Handler, this name will be used to save/load a json file
            with the configuration of the connector, and save logs
        :type config: Union[dict, str, pathlib.Path]
        :param config: Configuration used to setup the connector hanlder, it can be the dict with
            the data or a path to the json file, if is not provided the handler will serch the
            config at the default path and if is not finded, will request you the values via
            terminal input
        """

        self.name = name

        # logs
        path = Path.home().expanduser() / 'Element Unify/Connectors/logs'
        path.mkdir(parents=True, exist_ok=True)
        hdl = logging.FileHandler(path / f'{self.name}.log')
        fmt = logging.Formatter('%(asctime)s - [%(levelname)s] - %(name)s: %(message)s')
        hdl.setFormatter(fmt)
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.addHandler(hdl)
        self.log.setLevel(logging.INFO)
        self.log.info('Saving logs into %s', hdl.baseFilename)

        # Handler variables
        self.config, self.path = self.__get_config(config)
        # self.executions_log = OrderedDict()


        # Trigger variables (schedule only at the moment)
        self.__schedule_status = Status.IDLE
        self.schedule_rule = self.config['schedule']['rule']
        self.scheduler = None # Will store the croniter object with scheduler rule
        self.schedule_executor = ThreadPoolExecutor(1)
        self.schedule_obj = None # Will store the Future object where scheduler is running

        # Execution variables
        self.__connector_status = Status.IDLE
        self.connector = None # This will be instantiated once the execution started
        self.connector_executor = ThreadPoolExecutor(1)
        self.connector_obj = None # Will store the Future object where connector is running

    def start_manual_execution(self):
        """
        Start a thread that will execute the connector behind
        """
        if self.__connector_status == Status.IDLE:
            self.refresh_config()
            self.connector_obj = \
                self.connector_executor.submit(self.__process)
        else:
            self.log.warning(
                'There is already a connector execution in background. SKIPPING execution'
            )

    def __process(self):
        self.__connector_status = Status.RUNNING
        self.log.info(
            'Starting %s running in background, connector status: %s',
            self.connector.__class__.__name__,
            self.__connector_status,
        )
        try:
            self.connector = self.set_connector(self.config)
            self.process(self.config)
            self.log.info('%s excecution finished successfully', self.connector.__class__.__name__)
        except Exception as err:
            self.log.error('An error ocurred during connector execution: %s', err)
            raise
        finally:
            self.__connector_status = Status.IDLE

    def start_trigger(self):
        """
        Start the schedule in a separate thread according with the cron expression provided, this
        will execute the connector once the next datetime provided by the cron expression is met
        """
        if self.__schedule_status == Status.IDLE:
            self.log.info(
                'Startng schedule execution in background, with rule "%s"',
                self.schedule_rule
            )
            self.scheduler = croniter(self.schedule_rule, datetime.now())
            self.log.info('Next execution scheduled at %s', self.scheduler.get_next(datetime))
            self.__schedule_status = Status.RUNNING
            self.schedule_obj = \
                self.schedule_executor.submit(self.__start_schedule)
        else:
            self.log.warning(
                'There is already a schedule execution in background, SKIPPING command'
            )

    def __start_schedule(self):
        while self.__schedule_status == Status.RUNNING:
            scheduled_time = self.scheduler.get_current(datetime)
            if datetime.now() >= scheduled_time:
                self.log.info(
                    'Starting schedule excecition of %s at %s. Next execution scheduled at %s',
                    scheduled_time,
                    datetime.now(),
                    self.scheduler.get_next(datetime)
                )
                self.start_manual_execution()

            sleep(0.25)
        self.log.info('Scheduler was paused, exiting programed scheduled executions')

    def stop(self):
        """
        Stop the scheduler
        """
        self.__schedule_status = Status.IDLE

    def scheduler_is_running(self):
        """
        Returns True if the scheduler is running, False otherwise
        """
        return self.__schedule_status == Status.RUNNING

    def connector_is_running(self):
        """
        Returns True is the connector is executing at the moment, False otherwise like waiting for
        the next execution
        """
        return self.__connector_status == Status.RUNNING

    def status(self):
        """
        Returns a dict with the current status of both scheduler and connector.
        """
        return {
            'Scheduler': self.__schedule_status.name,
            'Connector': self.__connector_status.name,
        }

    @staticmethod
    def set_secret(secret_name, secret_value):
        """
        Method used to safely store the sensible data into the OS keyring service

        :type secret_name: str
        :param secret_name: Name of the secret used later to retrieve the secret value
        :type secret_value: str
        :param secret_value: Value to be stored as a secret
        """
        keyring.set_password('system', f'{secret_name}', secret_value)

    @staticmethod
    def get_secret(secret_name):
        """
        Retrieves the secret value according with the name provided

        :type secret_name: str
        :param secret_name: Name of the secret used to retrieve the secret value
        """
        return keyring.get_password('system', f'{secret_name}')

    @staticmethod
    def rnd_str(length):
        """
        Create a random alphanumeric string of length n

        :type n: int
        :param n: length of the string
        """
        return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(length))

    def __get_config(self, config=None):
        # TODO modify this method when its ready to get the config online

        default_path = f'~/Element Unify/Connectors/config/{self.name}.json'
        Path(default_path).expanduser().parent.mkdir(parents=True, exist_ok=True)

        # If there is not config,
        if config is None:
            # search by name
            if Path(default_path).expanduser().exists():
                return self.get_config(default_path), default_path

            # create it by inputs
            config = self.input_config()

        # once we have the config, store it in the home directory
        if isinstance(config, dict):
            self.__save_config(default_path, config)
            return config, default_path

        # if the config is a path, open it
        return self.get_config(config), config

    def refresh_config(self):
        """
        Reloads the config from the json file
        """
        self.config = self.get_config(self.path)

    def __save_config(self, path, config, encoding='utf8'):
        self.log.info('Saving config in: %s', path)
        data = {
            'type': f'{self.__class__.__name__}',
            'config': config,
        }
        with Path(path).expanduser().open('w',encoding=encoding) as txt:
            json.dump(data, txt, indent=4)

    def get_config(self, path, encoding='utf8'):
        """
        Returns the config dict stored in the json file specified in path parameter

        :type path: Union[str, pathlib.Path]
        :param path: json filename to be loaded
        """
        # TODO think about getting the config from a Yaml with any syntax PyYAML
        self.log.info('Loading config from: %s', path)
        with Path(path).expanduser().open('r', encoding=encoding) as txt:
            config = json.load(txt)
        return config['config']

    @abstractmethod
    def input_config(self):
        """
        Abstract method to implement the config dict for each connector type, this method should
        return a dict with all the data required to instantiate the connector and execute it.
        """

    @abstractmethod
    def set_connector(self, config):
        """
        Abstract method to implement the creation of the connector, should have a parameter called
        config that will be the dict returned by the method input_config. Should return a
        connector instance. This instance will be stored as self.connector variable.

        :type config: dict
        :param config: dict returned by input_config method
        """

    @abstractmethod
    def process(self, config):
        """
        Abstract method to implement the execution of the connector, it should have a parammeter
        called config that will be the dict returned by the method input_config.

        :type config: dict
        :param config: dict returned by input_config method
        """
