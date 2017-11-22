#!/usr/bin/env python3
# Copyright (C) 2017  Ghent University
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from charmhelpers.core.hookenv import status_set, log
from charms.reactive import when, set_state


@when_not('auth.installed')
def install_k8s_auth():
    status_set('maintenance', 'Waiting for kubernetes cluster')
    if os.path.exists('/home/ubuntu/config'):
        status_set('active', 'ready')
        set_state('auth.installed')


@when('kube-auth.available', 'auth.installed')
def send_config(auth):
    status_set('active', 'Sending authentication')
    try:
        with open('/home/ubuntu/config') as f:
            config = yaml.load(f)
            auth.send_config(config)
            status_set('active', 'ready')
    except OSError as e:
        log(e)
        status_set('blocked', 'Could not find authentication file')
    except yaml.YAMLError as e:
        log(e)
        status_set('blocked', 'Error parsing authentication file')
