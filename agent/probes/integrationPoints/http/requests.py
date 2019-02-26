

"""Probe requests to ensure that HTTPS is reported correctly.

"""

from __future__ import unicode_literals

from . urllib3 import probe_urllib3


def probe_requests(agent, mod):
    # requests ships with its own version of urllib3, so we need to manually probe it.
    probe_urllib3(agent, mod.packages.urllib3)
