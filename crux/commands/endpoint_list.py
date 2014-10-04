# BEGIN LICENSE
# Copyright 2014 Lars Kellogg-Stedman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# END LICENSE


from __future__ import absolute_import

import logging
from cliff.lister import Lister

from ..exc import *


class EndpointList(Lister):

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(EndpointList, self).get_parser(prog_name)
        parser.add_argument('--endpoint-type', '-t',
                            action='append',
                            default=[])
        return parser

    def take_action(self, args):
        if not args.endpoint_type:
            args.endpoint_type = ['public', 'internal', 'admin']
        if any((x not in ['public', 'internal', 'admin'])
               for x in args.endpoint_type):
            raise CruxException('--endpoint-type must be one of: '
                                'internal, public, admin')

        client = self.app.client
        services = client.services.list()
        services = dict((x.id, {'name': x.name, 'type': x.type})
                        for x in services)
        endpoints = client.endpoints.list()

        data = []
        for endpoint in endpoints:
            data.append(
                (endpoint.id,
                 services[endpoint.service_id]['name'],
                 services[endpoint.service_id]['type'],
                 ) + tuple(
                 getattr(endpoint, '%surl' % which, '-') for which in
                     args.endpoint_type
                 ))

        return (('id', 'name', 'type') + tuple(args.endpoint_type),
                data)
