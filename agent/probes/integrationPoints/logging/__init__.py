
"""Probing the Python logging module.

"""

from __future__ import unicode_literals
import logging
import sys

from agent.probes.instrumentation import BaseProbe
from appdynamics.agent.models.errors import ErrorInfo
from appdynamics.agent.core import conditions


class LoggingProbe(BaseProbe):
    LOGGING_ERROR_DISPLAY_NAME = '{logger_name} [{level_name}]'

    def _callHandlers(self, callHandlers, logger, record):
        with self.log_exceptions():
            if not record.name.startswith('appdynamics') and self.bt:
                self.add_logged_error(record)
        callHandlers(logger, record)

    def add_logged_error(self, record):
        """Add an error to the BT if the log record should trigger an error.

        If the level is greater or equal than the threshold and the message is
        not ignored, create an ErrorInfo object and add it to the BT.

        """
        error_config = self.agent.error_config_registry

        if not error_config.should_detect_logged_errors:
            return

        levelno = record.levelno
        if levelno < error_config.error_threshold:
            return

        msg = record.getMessage()
        if any(conditions.match(msg, match_cond) for match_cond in error_config.ignored_messages):
            return

        if record.exc_info:
            msg += '\n' + logging.Formatter().formatException(record.exc_info)

        display_name = self.LOGGING_ERROR_DISPLAY_NAME.format(logger_name=record.name, level_name=record.levelname)
        self.bt.add_logged_error(ErrorInfo(msg, display_name, levelno))


def probe_logging(agent, mod):
    LoggingProbe(agent, mod.Logger).attach('callHandlers')


