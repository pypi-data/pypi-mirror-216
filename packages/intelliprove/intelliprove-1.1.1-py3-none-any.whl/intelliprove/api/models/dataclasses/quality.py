from typing import Optional
from dataclasses import dataclass
from intelliprove.api.models.enums import QualityErrorType


@dataclass
class Quality:
    score: int
    error_type: QualityErrorType
    message: str
    signature: Optional[str] = None
