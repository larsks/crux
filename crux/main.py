#!/usr/bin/python

import os
import sys
import argparse
import logging

from cliff.app import App
from cliff.commandmanager import CommandManager

import keystoneclient.v2_0.client as ksclient

import crux.commands.user_list
import crux.commands.user_create
import crux.commands.endpoint_list
import crux.commands.endpoint_create

class Crux (App):
    log = logging.getLogger(__name__)

    def __init__(self):
        super(Crux,self).__init__(
            description='Keystone Utility',
            version='2',
            command_manager=CommandManager('com.oddbit.crux'),
        )

        self._client = None

        self.command_manager.add_command('user-list',
                                         crux.commands.user_list.UserList)
        self.command_manager.add_command('user-create',
                                         crux.commands.user_create.UserCreate)
        self.command_manager.add_command('endpoint-list',
                                         crux.commands.endpoint_list.EndpointList)
        self.command_manager.add_command('endpoint-create',
                                         crux.commands.endpoint_create.EndpointCreate)

    def build_option_parser(self, *args, **kwargs):
        parser = super(Crux, self).build_option_parser(*args, **kwargs)

        parser.add_argument('--os-username',
                       default=os.environ.get('OS_USERNAME'))
        parser.add_argument('--os-password',
                       default=os.environ.get('OS_PASSWORD'))
        parser.add_argument('--os-tenant-name',
                       default=os.environ.get('OS_TENANT_NAME'))
        parser.add_argument('--os-tenant-id',
                       default=os.environ.get('OS_TENANT_ID'))
        parser.add_argument('--os-region-name',
                       default=os.environ.get('OS_REGION_NAME'))
        parser.add_argument('--os-auth-url',
                       default=os.environ.get('OS_AUTH_URL'))
        parser.add_argument('--os-service-token',
                       default=os.environ.get('SERVICE_TOKEN')),
        parser.add_argument('--os-service-endpoint',
                       default=os.environ.get('SERVICE_ENDPOINT'))

        return parser

    def get_keystone_client(self):
        return ksclient.Client(username=self.options.os_username, 
                               password=self.options.os_password,
                               token=self.options.os_service_token,
                               tenant_name=self.options.os_tenant_name,
                               tenant_id=self.options.os_tenant_id,
                               auth_url=self.options.os_auth_url,
                               endpoint=self.options.os_service_endpoint)

    @property
    def client(self):
        if self._client:
            return self._client

        self._client = self.get_keystone_client()
        return self._client

app = Crux()

def main():
    reqlog = logging.getLogger('requests')
    reqlog.setLevel(logging.WARNING)
    return app.run(sys.argv[1:])

if __name__ == '__main__':
    main()

