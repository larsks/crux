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


class UserList(Lister):

    log = logging.getLogger(__name__)

    def take_action(self, args):
        client = self.app.client
        users = client.users.list()

        return (('id', 'name', 'tenant_id', 'enabled'),
                ((u.id, u.name, getattr(u, 'tenantId', '-'), u.enabled)
                 for u in users))
