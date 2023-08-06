__version__ = "2023.6.8"

import logging

from eodc.settings import settings  # noqa

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)
