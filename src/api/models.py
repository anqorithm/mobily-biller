from pydantic import BaseModel, Field
from typing import Dict, List


class BillRequest(BaseModel):
    numbers: str = Field(..., description="Comma-separated list of phone numbers")
    national_id: str = Field(..., description="National ID")
    options: str = Field(None, description="Optional features (e.g., send_to_whatsapp)")
    callmebot_phone: str = Field(None, description="CallMeBot phone number")
    callmebot_apikey: str = Field(None, description="CallMeBot API key")


class BillItem(BaseModel):
    number: str
    amount: float
    index: int


class BillResponse(BaseModel):
    id: str
    numbers: List[str]
    bills: List[BillItem]
    total: float
    whatsapp_notification_sent: bool = False


class BillDetails(BaseModel):
    number: str
    amount: float
    id: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    scope: str


class MobilyRequest(BaseModel):
    STATUS: str = "POSTPAID"
    VERSION: str
    TRANSACTION_ID: str = "6105734946382125"
    REQUEST_DATE: str = "04-02-2025 11:09:55.62300"
    USER_NAME: str = ""
    NATIONAL_ID: str
    SESSION_ID: str
    APP_ID: str
    LANG: str = "AR"
    MSISDN: str
    DEVICE_ID: str


class MobilyResponse(BaseModel):
    TRANSACTION_ID: str | None = None
    STATUS_CODE: str | None = None
    ERROR_CODE: str | None = None
    ERROR_DESCRIPTION: str | None = None
    AMOUNT: str | None = None
    LAST_BILL_AMOUNT: str | None = None
    CREDIT_DATE: str | None = None
    UNBILLED_AMOUNT: str | None = None
    UNALLOCATED_AMOUNT: str | None = None
    NCR_BALANCE: str | None = None
    IS_FALLAH_100: bool = False
