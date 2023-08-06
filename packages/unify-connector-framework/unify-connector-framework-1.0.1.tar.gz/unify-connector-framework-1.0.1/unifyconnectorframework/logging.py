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
'''
A logger method used to log in console, file and Unify at the same time
'''

import logging
from unify.connectors import LogType

class UnifyHandler(logging.Handler):
    '''
    A handler class which writes formatted logging records to Unify Connector Service.
    '''

    def __init__(self, connector):
        '''
        Set the connector to be used to send logs
        '''
        logging.Handler.__init__(self)
        self.connector = connector

    def emit(self, record):
        '''
        Send the record log to Unify
        '''
        try:
            msg = self.format(record)
            if record.levelno <= logging.INFO:
                log_type = LogType.INFO
            elif record.levelno <= logging.WARNING:
                log_type = LogType.WARNING
            else:
                log_type = LogType.ERROR
            self.connector.write_log(msg, log_type=log_type)
        except Exception:
            self.handleError(record)

    def __repr__(self):
        level = logging.getLevelName(self.level)
        return f"<UnifyHandler <{self.connector.id}> ({level})>"
