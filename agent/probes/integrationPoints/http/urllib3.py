# Copyright (c) AppDynamics, Inc., and its affiliates
# 2015
# All Rights Reserved

"""Intercept urllib3 to ensure that HTTPS is reported correctly.

"""

from __future__ import unicode_literals

from agent.probes.integrationPoints.http import HTTPConnectionProbe


def probe_urllib3(agent, mod):
    # urllib3 1.8+ provides its own HTTPSConnection class.
    if hasattr(mod, 'connection'):
        HTTPConnectionProbe.https_connection_classes.add(mod.connection.HTTPSConnection)
