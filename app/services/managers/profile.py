from dataclasses import dataclass
from datetime import datetime

from app.services.base import TransfermarktBase
from app.utils.utils import (
    clean_response,
    extract_from_url,
)
from app.utils.xpath import Coaches
