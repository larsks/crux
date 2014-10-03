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
