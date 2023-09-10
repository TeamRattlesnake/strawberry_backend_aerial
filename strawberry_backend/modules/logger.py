"""
Модуль с классом для общения с базой данных
"""

import logging
from datetime import datetime

logging.basicConfig(
    format="%(asctime)sUTC\t%(levelname)s\t%(message)s",
    handlers=[
        logging.FileHandler(
            f"data/logs/log_{str(datetime.now()).replace(' ', '_')}.txt",
            mode="w",
            encoding="UTF-8",
        ),
        logging.StreamHandler(),
    ],
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)
