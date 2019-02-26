

from __future__ import unicode_literals
import sys

from agent.probes.instrumentation import ExitCallProbe
from appdynamics.lang import str
from appdynamics.agent.models.exitcalls import EXIT_CUSTOM, EXIT_SUBTYPE_MONGODB


def probe_pymongo(agent, mod):
    class ExitCallListener(mod.monitoring.CommandListener):
        backend_name_format_string = '{HOST}:{PORT} - {DATABASE}'

        def __init__(self):
            self.probe = ExitCallProbe(agent, None)
            self.exit_call_map = {}

        def get_backend(self, connection_id, database_name):
            host, port = connection_id
            backend_properties = {
                'HOST': host,
                'PORT': str(port),
                'DATABASE': database_name,
            }
            backend = self.probe.agent.backend_registry.get_backend(EXIT_CUSTOM, EXIT_SUBTYPE_MONGODB,
                                                                          backend_properties,
                                                                          self.backend_name_format_string)
            return backend

        def started(self, event):
            with self.probe.log_exceptions():
                bt = self.probe.bt
                if bt:
                    backend = self.get_backend(event.connection_id, event.database_name)
                    if backend:
                        exit_call = self.probe.start_exit_call(bt, backend, str(event.command))
                        self.exit_call_map[event.operation_id] = exit_call

        def succeeded(self, event):
            self.probe.end_exit_call(self.exit_call_map.pop(event.operation_id, None))

        def failed(self, event):
            self.probe.end_exit_call(self.exit_call_map.pop(event.operation_id, None), exc_info=sys.exc_info())

    mod.monitoring.register(ExitCallListener())
