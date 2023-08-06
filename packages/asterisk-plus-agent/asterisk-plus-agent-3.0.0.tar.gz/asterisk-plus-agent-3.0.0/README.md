[![Build status](https://github.com/odoopbx/pbx/actions/workflows/docker.yml/badge.svg)](https://github.com/odoopbx/pbx/actions)

# [OdooPBX]
Deployment instructions are available on the [Docker Hub].

This repository contains the PBX part for the [Asterisk Plus] module:

* `asterisk`: [Asterisk] PBX SIP server.
* `services`: The OdooPBX Agent middleware based on the [Nameko] microservices platform.
* `docker`: Docker based deployment scripts.

## Services
The following services are defined:

* `services/asterisk_broker`: Asterisk Broker (AMI, File access, IP security).
* `services/odoo_broker`: Odoo Broker (JSON-RPC, AMI actions & events).
* `services/console`: Odoo Asterisk Web CLI backend server.

## Deployment & Development
Different kind of deployments can be found in the `docker/examples` folder.

[Asterisk Plus]: https://github.com/odoopbx/addons
[Asterisk]: https://www.asterisk.org/
[odoo]: https://www.odoo.com/
[OdooPBX]: https://odoopbx.com
[Nameko]: https://www.nameko.io/
[docker hub]: https://hub.docker.com/u/odoopbx
