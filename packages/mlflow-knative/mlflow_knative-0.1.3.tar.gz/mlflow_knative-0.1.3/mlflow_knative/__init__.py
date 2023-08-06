import logging
import sys
from importlib import metadata

logger = logging.getLogger(__package__)

# If the plugin is running in a TTY, we assume it is used through MLflow CLI
# so we output INFO logs to the console.
# Otherwise we're a well-behaved library and do not set logging configuration.
if sys.stdout.isatty():
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    logger.addHandler(handler)


__version__ = metadata.version(__package__)
