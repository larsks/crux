import logging

import keystoneclient.v2_0.client as ksclient
from .exc import *


class Keystone (object):

    log = logging.getLogger(__name__)

    def __init__(self, username=None, password=None,
                 token=None, tenant_name=None,
                 tenant_id=None, auth_url=None,
                 endpoint=None):

        self.username = username
        self.password = password
        self.token = token
        self.tenant_name = tenant_name
        self.tenant_id = tenant_id
        self.auth_url = auth_url
        self.endpoint = endpoint

        self.get_keystone_client()

    def get_keystone_client(self):
        self.client = ksclient.Client(username=self.username,
                                      password=self.password,
                                      token=self.token,
                                      tenant_name=self.tenant_name,
                                      tenant_id=self.tenant_id,
                                      auth_url=self.auth_url,
                                      endpoint=self.endpoint)


    def find_tenant(self, tenant_name):
        tenants = self.client.tenants.list()

        res = [x for x in tenants if x.name == tenant_name]

        if len(res) == 1:
            return res[0]
        elif len(res) > 1:
            raise ValueError('found multiple matches for tenant %s' %
                             tenant_name)
        else:
            raise KeyError(tenant_name)

    def create_tenant(self, tenant_name,
                      tenant_description=None):
        tenant = self.client.tenants.create(
            tenant_name,
            tenant_description)

        return tenant

    def find_or_create_tenant(self, tenant_name,
                              tenant_description=None):
        try:
            tenant = self.find_tenant(tenant_name)
            self.log.info('using existing tenant %s (%s)',
                          tenant.name,
                          tenant.id)
        except KeyError:
            tenant = self.create_tenant(tenant_name,
                                        tenant_description=tenant_description)
            self.log.info('created new tenant %s (%s)',
                          tenant.name,
                          tenant.id)

        return tenant

    def find_user(self, user_name):
        users = self.client.users.list()
        res = [x for x in users if x.name == user_name]

        if len(res) == 1:
            return res[0]
        elif len(res) > 1:
            raise ValueError('found multiple matches for user %s' %
                             user_name)
        else:
            raise KeyError(user_name)

    def create_user(self, user_name, user_password, tenant,
                    user_email=None, user_enabled=True):
        if not user_password:
            raise CruxException('cannot create a user with an empty '
                                'password')

        user = self.client.users.create(
            user_name,
            user_password,
            user_email,
            tenant.id,
            user_enabled)

        return user

    def find_or_create_user(self, user_name,
                            user_password=None,
                            tenant=None,
                            user_email=None, user_enabled=True):
        try:
            user = self.find_user(user_name)
            self.log.info('using existing user %s (%s)',
                          user.name,
                          user.id)
        except KeyError:
            if tenant is None:
                raise ValueError('cannot create user with '
                                 'undefined tenant')

            user = self.create_user(user_name, user_password, tenant,
                                    user_email=user_email,
                                    user_enabled=user_enabled)
            self.log.info('created new user %s (%s)',
                          user.name,
                          user.id)

        return user

    def update_user(self, user,
                    user_email=None,
                    user_password=None,
                    user_enabled=None):

        if user_enabled is not None:
            self.log.info('updating enabled for user %s',
                          user.name)
            self.client.users.update(user, enabled=user_enabled)

        if user_email is not None:
            self.log.info('updating email for user %s',
                          user.name)
            self.client.users.update(user, email=user_email)

        if user_password is not None:
            self.log.info('updating password for user %s',
                          user.name)
            self.client.users.update_password(user, user_password)

    def find_user(self, user_name):
        users = self.client.users.list()
        res = [x for x in users if x.name == user_name]

        if len(res) == 1:
            return res[0]
        elif len(res) > 1:
            raise ValueError('found multiple matches for user %s' %
                             user_name)
        else:
            raise KeyError(user_name)

    def find_role(self, role_name):
        roles = self.client.roles.list()
        res = [x for x in roles if x.name == role_name]

        if len(res) == 1:
            return res[0]
        elif len(res) > 1:
            raise ValueError('found multiple matches for role %s' %
                             role_name)
        else:
            raise KeyError(role_name)

    def create_role(self, role_name):
        role = self.client.roles.create(role_name)
        return role

    def find_or_create_role(self, role_name):
        try:
            role = self.find_role(role_name)
            self.log.info('using existing role %s (%s)',
                          role.name,
                          role.id)
        except KeyError:
            role = self.create_role(role_name)
            self.log.info('created new role %s (%s)',
                          role.name,
                          role.id)

        return role
