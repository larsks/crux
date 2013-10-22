crux: a keystone utility
========================

Crux is a utility for creating objects in the [Keystone][]
authentication database.  It could be used to quickly provision test
environments, or as part of an automated user-provisioning script.

[keystone]: http://docs.openstack.org/developer/keystone/

Options
=======

- `--config`, `-f` *file* -- load definitions from *file*, a file in
  [yaml][] syntax.  See below for an example.

- `--user`, `-u` *user:tenant:role:password* -- create user *user*
  with primary tenant *tenant*.  Assign the user role *role* and set
  the password to *password*.  Either *role* or *password* may be
  empty; if *password* is empty `crux` will generate a random password
  for the user.

  The named role and tenant will be created if they do not exist.

- `--role`, `-r` *role* -- created named role *role*.

- `--tenant`, `-t` *tenant* -- create named tenant *tenant*.

- `--pwlen` *pwlen* -- length of generated passwords.

- `--verbose`, `-v` -- enable verbose logging.

[yaml]: http://en.wikipedia.org/wiki/YAML

Command line examples
=====================

Create user `demo` in the `demo` tenant with password `secret`:

    # crux --user demo:demo::secret
    2013-10-21 crux WARNING creating tenant demo
    2013-10-21 crux WARNING creating user demo with password secret

Add role `admin` (in the `demo` tenant) to the `demo` user:

    # crux --user demo:demo:admin:secret
    2013-10-21 crux WARNING set password for user demo to secret
    2013-10-21 crux WARNING added role admin to user demo

Configuration file examples
===========================

Create a file named (e.g.) `users.yml` with the following content:

    keystone:
      tenants:
      - name: demo
        description: >
          Use this tenant for the demonstration.
      - name: alt_demo
        description: >
          An alternate tenant to demonstrate tenant isolation. This
          tenant also has a very long description to demonstrate that
          it's easy to create multi-line values using YAML syntax.
      users:
      - name: user1
        tenant: demo
        password: secret1
      - name: user2
        tenant: demo
        password: secret2
      - name: demoadmin
        tenant: demo
        password: secretadmin
        role: admin
      - name: user3
        tenant: alt_demo
        password: secret3

Run `crux` like this:

    $ crux -f users.yml
    2013-10-21 crux WARNING creating tenant demo
    2013-10-21 crux WARNING creating tenant alt_demo
    2013-10-21 crux WARNING creating user user1 with password secret1
    2013-10-21 crux WARNING creating user user2 with password secret2
    2013-10-21 crux WARNING creating user demoadmin with password secretadmin
    2013-10-21 crux WARNING added role admin to user demoadmin
    2013-10-21 crux WARNING creating user user3 with password secret3

Bask in the glow of a lovely suite of test accounts:

    $ keystone tenant-list
    +----------------------------------+----------+---------+
    |                id                |   name   | enabled |
    +----------------------------------+----------+---------+
    | f8fb52537f24449d84b374479a45789b |  admin   |   True  |
    | c61e548e5dc14d80b01155781f019de2 | alt_demo |   True  |
    | d81b6b780206467fa0f2ab79c507cb71 |   demo   |   True  |
    | 5030d1e4adae47578eb29d74e20acde4 | services |   True  |
    +----------------------------------+----------+---------+

    $ keystone user-list --tenant-id d81b6b780206467fa0f2ab79c507cb71
    +----------------------------------+-----------+---------+-----------+
    |                id                |    name   | enabled |   email   |
    +----------------------------------+-----------+---------+-----------+
    | 8f0c82336e274b588b42b7e37c8779ff | demoadmin |   True  | demoadmin |
    | 7c6bf08e6a364c6ebc6b673f068e1520 |   user1   |   True  |   user1   |
    | 59798bdfa1504585bee5b12c7706a055 |   user2   |   True  |   user2   |
    +----------------------------------+-----------+---------+-----------+

<!--  (this output table is really too wide to display on most site
      layouts)

    $ keystone user-role-list --tenant demo --user demoadmin
    +----------------------------------+----------+----------------------------------+----------------------------------+
    |                id                |   name   |             user_id              |            tenant_id             |
    +----------------------------------+----------+----------------------------------+----------------------------------+
    | 9fe2ff9ee4384b1894a90878d3e92bab | _member_ | 8f0c82336e274b588b42b7e37c8779ff | d81b6b780206467fa0f2ab79c507cb71 |
    | 09ec0bdbe646425c83f5dbc1a67ec488 |  admin   | 8f0c82336e274b588b42b7e37c8779ff | d81b6b780206467fa0f2ab79c507cb71 |
    +----------------------------------+----------+----------------------------------+----------------------------------+
-->

License
=======

crux -- a utility for creating keystone objects  
Copyright (C) 2013 Lars Kellogg-Stedman <lars@oddbit.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

