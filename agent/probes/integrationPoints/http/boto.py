# Copyright (c) AppDynamics, Inc., and its affiliates
# 2015
# All Rights Reserved

"""Intercept boto to ensure that HTTPS is reported correctly.

"""

from __future__ import unicode_literals

from . import HTTPConnectionProbe


def probe_boto(agent, mod):
    HTTPConnectionProbe.https_connection_classes.add(mod.CertValidatingHTTPSConnection)
