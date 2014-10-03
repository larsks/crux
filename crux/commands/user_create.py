from __future__ import absolute_import

import logging
import random
import string
from cliff.command import Command

from ..exc import *


class UserCreate(Command):

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(UserCreate, self).get_parser(prog_name)

        parser.add_argument('--user-name', '--user', '-n')
        parser.add_argument('--user-email', '-e')
        parser.add_argument('--tenant-name', '--tenant', '-t')
        parser.add_argument('--tenant-description', '-D')
        parser.add_argument('--password', '--pass', '-p')
        parser.add_argument('--role', '-r')
        parser.add_argument('--random-password', '-R',
                            action='store_true')
        parser.add_argument('--password-length', '-L',
                            type=int, default=15)
        parser.add_argument('--enabled',
                            action='store_true',
                            default=True)
        parser.add_argument('--disabled',
                            action='store_false',
                            dest='enabled')
        parser.add_argument('--update',
                            action='store_true')
        return parser

    def take_action(self, args):
        if not args.user_name:
            raise CruxException('you must provide a value for --user-name')
        if not args.tenant_name:
            raise CruxException('you must provide a value for --tenant-name')

        if args.random_password:
            args.password = ''.join(
                random.sample(string.letters + string.digits,
                              args.password_length))
            self.log.info('generated random password: %s',
                          args.password)

        tenant = self.find_or_create_tenant(args)
        user = self.find_or_create_user(args, tenant)

        if args.role:
            self.add_user_role(args, user, tenant)

    def add_user_role(self, args, user, tenant):
        client = self.app.client
        role = self.find_or_create_role(args)
        user_roles = client.roles.roles_for_user(user, tenant=tenant)
        if any((x.id == role.id) for x in user_roles):
            self.log.info('user %s already has role %s in tenant %s',
                          user.name,
                          role.name,
                          tenant.name)
        else:
            for user_role in user_roles:
                self.log.info('removing role %s from user %s in tenant %s',
                          user_role.name,
                          user.name,
                          tenant.name)
                client.roles.remove_user_role(user, user_role, tenant=tenant)

            self.log.info('adding role %s to user %s in tenant %s',
                          role.name,
                          user.name,
                          tenant.name)
            client.roles.add_user_role(user, role, tenant=tenant)

    def find_or_create_tenant(self, args):
        client = self.app.client
        tenants = client.tenants.list()

        res = [x for x in tenants if x.name == args.tenant_name]

        if res:
            tenant = res[0]
            self.log.info('using existing tenant %s (%s)',
                     tenant.name, tenant.id)
        else:
            self.log.info('creating new tenant')
            tenant = client.tenants.create(
                args.tenant_name,
                args.tenant_description)
            self.log.info('created tenant %s (%s)',
                          tenant.name, tenant.id)

        return tenant

    def find_or_create_user(self, args, tenant):
        client = self.app.client
        users = client.users.list()

        res = [x for x in users if x.name == args.user_name]

        if res:
            user = res[0]
            self.log.info('using existing user %s (%s)',
                     user.name, user.id)

            if args.update:
                self.log.info('updating enabled=%s for user %s',
                              args.enabled, user.name)
                client.users.update(user, enabled=args.enabled)
                if args.user_email:
                    self.log.info('updating email for user %s',
                                  user.name)
                    client.users.update(user, email=args.user_email)
                if args.password:
                    self.log.info('updating password for user %s',
                                  user.name)
                    client.users.update_password(user, args.password)
        else:
            if not args.password:
                raise CruxException('cannot create a user with an empty '
                                    'password')

            self.log.info('creating new user %s',
                          args.user_name)
            user = client.users.create(
                args.user_name,
                args.password,
                args.user_email,
                tenant.id,
                args.enabled)
            self.log.info('created user %s (%s)',
                          user.name, user.id)

        return user

    def find_or_create_role(self, args):
        client = self.app.client
        roles = client.roles.list()

        res = [x for x in roles if x.name == args.role]

        if res:
            role = res[0]
            self.log.info('using existing role %s (%s)',
                     role.name, role.id)
        else:
            role = client.roles.create(args.role)
            self.log.info('created role %s (%s)',
                          role.name, role.id)

        return role

