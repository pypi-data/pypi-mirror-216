from dataclasses import dataclass
from typing import Optional
from enum import Enum

class CodeType(Enum):
    """
    The type of code to read.
    """
    ACCR_USA = "accr_usa"
    ILU = "ilu"
    ISO = "iso"
    MOCO = "moco"
    BRA = "bra"
    RUS = "rus"
    UIC = "uic"
    AAR = "aar"
    CHASSIS = "chassis"
    USDOT = "usdot"

@dataclass
class TransportAPIOptions:
    """
    Options for configuring the TransportAPI client.
    """
    api_key: str
    type: CodeType
    endpoint: Optional[str] = None
    cloud_service_region: Optional[str] = None
    disable_iso_code: Optional[bool] = False
    disable_checksum_check: Optional[bool] = False
    enable_full_us_accr_code: Optional[bool] = False
    disable_image_resizing: Optional[bool] = False
    enable_wide_range_analysis: Optional[bool] = False
    max_reads: Optional[int] = 1
    retry_count: Optional[int] = 2
