from __future__ import absolute_import

import logging
from cliff.command import Command

from ..exc import *


class EndpointCreate(Command):

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(EndpointCreate, self).get_parser(prog_name)

        parser.add_argument('--service-name', '--service', '-n')
        parser.add_argument('--service-type', '--type', '-t')
        parser.add_argument('--service-description', '--description', '-d')
        parser.add_argument('--region', '-r',
                            default='RegionOne')
        parser.add_argument('--publicurl', '--public', '-P')
        parser.add_argument('--internalurl', '--internal', '-I')
        parser.add_argument('--adminurl', '--admin', '-A')

        return parser

    def take_action(self, args):
        for req in ['service_name', 'service_type', 'internalurl']:
            if not getattr(args, req):
                raise CruxException('you must specify a value for --%s' %
                                    req)

        if not args.publicurl:
            args.publicurl = args.internalurl
        if not args.adminurl:
            args.adminurl = args.internalurl

        service = self.find_or_create_service(args)
        self.find_or_create_endpoint(args, service)

    def find_or_create_service(self, args):
        client = self.app.client
        services = client.services.list()

        res = [x for x in services if x.name == args.service_name]

        if res:
            service = res[0]
            self.log.info('using existing service %s/%s (%s)',
                          service.name, service.type, service.id)
        else:
            service = client.services.create(
                args.service_name,
                args.service_type,
                args.service_description)
            self.log.info('created new service %s/%s (%s)',
                          service.name,
                          service.type,
                          service.id)

        return service

    def find_or_create_endpoint(self, args, service):
        client = self.app.client
        endpoints = client.endpoints.list()

        res = [x for x in endpoints if x.service_id == service.id]

        if res:
            endpoint = res[0]
            self.log.info('using existing endpoint internalurl=%s, '
                          'publicurl=%s, adminurl=%s (%s)',
                          endpoint.internalurl,
                          endpoint.publicurl,
                          endpoint.adminurl,
                          endpoint.id)
            for endpointtype in ['internal', 'public', 'admin']:
                want = getattr(args, '%surl' % endpointtype)
                if want:
                    have = getattr(endpoint, '%surl' % endpointtype)
                    if want != have:
                        self.log.warn('requested %s endpoint %s does not '
                                      'match existing endpoint %s',
                                      endpointtype, want, have)
        else:
            endpoint = client.endpoints.create(
                args.region,
                service.id,
                args.publicurl,
                args.adminurl,
                args.internalurl)
            self.log.info('created new endpoint internalurl=%s, '
                          'publicurl=%s, adminurl=%s (%s)',
                          endpoint.internalurl,
                          endpoint.publicurl,
                          endpoint.adminurl,
                          endpoint.id)

        return endpoint
