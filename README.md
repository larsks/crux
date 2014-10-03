# crux: a keystone utility

Crux is a utility for creating [Keystone][] tenants, roles, users,
services, and endpoints.

Crux is designed to be *idempotent* -- you can safely run it multiple
times with the same inputs without bad things happening.

[keystone]: http://docs.openstack.org/developer/keystone/

## Authentication

Crux gets authentication information from the standard OpenStack
environment variables.  Like the `keystone` client, you can use a
username/password pair via `OS_USERNAME`, `OS_PASSWORD`, etc, or you
can use the admin token via `SERVICE_TOKEN` and `SERVICE_ENDPOINT`.

## Command line examples

Create user `testuser` in the `testproject` tenant with a random
password:

    $ crux user-create -n testuser -t testproject -R
    generated random password: lrw0zFe5uJ8IND1
    creating new tenant
    created tenant testproject (2c6577e7c3cd4721bbd0b3f4c2fbedc2)
    using existing user testuser (5d483f53c38a44eebb04d04c14bf35e0)

Create user `testuser2` in the same tenant with an explicit password:

    $ crux user-create -n testuser2 -t testproject -p secret
    using existing tenant testproject (2c6577e7c3cd4721bbd0b3f4c2fbedc2)
    creating new user testuser2
    created user testuser2 (689c732208db4ccca1844f72cd1844b3)

Create an endpoint for service `myservice`, a `messagequeue` service:

    $ crux endpoint-create -n myservice -t messagequeue -I http://localhost:5254/
    created new service myservice/messagequeue (00214ed4885d4417ae97c23e093a9845)
    created new endpoint internalurl=http://localhost:5254/, publicurl=http://localhost:5254/, adminurl=http://localhost:5254/ (c700a2c4df9f41e1979d1e330c73dccb)

Create an additional endpoint for the `myservice` service.  This won't
work by default (crux will just use the existing one) so so that you
do not accidentally create a new endpoint:

    $ crux endpoint-create -n myservice -t messagequeue -I http://otherhost:5254/
    using existing service myservice/messagequeue (00214ed4885d4417ae97c23e093a9845)
    using existing endpoint internalurl=http://localhost:5254/, publicurl=http://localhost:5254/, adminurl=http://localhost:5254/ (c700a2c4df9f41e1979d1e330c73dccb)

But you can explicitly add additional endpoints with `--append`:

    $ crux endpoint-create -n myservice -t messagequeue -I http://otherhost:5254/ --append
    using existing service myservice/messagequeue (00214ed4885d4417ae97c23e093a9845)
    created new endpoint internalurl=http://otherhost:5254/, publicurl=http://otherhost:5254/, adminurl=http://otherhost:5254/ (e2615d049ea34c9289323a0d6e045a2f)

    $ crux endpoint-list -t internal | grep messagequeue
    | c700a2c4df9f41e1979d1e330c73dccb | myservice  | messagequeue  | http://localhost:5254/                 |
    | e2615d049ea34c9289323a0d6e045a2f | myservice  | messagequeue  | http://otherhost:5254/                 |

## Packages

Crux packages for RHEL, CentOS, and Fedora are available from:

- http://copr.fedoraproject.org/coprs/larsks/crux/

