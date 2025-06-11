from dataclasses import dataclass
from typing import Tuple

@dataclass
class Config:
    supported_formats: Tuple[str, ...] = ('.jpg', '.jpeg')
