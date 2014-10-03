from __future__ import absolute_import

import logging
from cliff.lister import Lister

class UserList(Lister):

    log = logging.getLogger(__name__)

    def take_action(self, args):
        client = self.app.client
        users = client.users.list()

        return (('id', 'name', 'tenant_id', 'enabled'),
                ((u.id, u.name, getattr(u, 'tenantId', '-'), u.enabled) for u in users))
