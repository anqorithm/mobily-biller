from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    # API Configuration
    api_title: str = Field("Bills Calculator API", description="API Title")
    api_version: str = Field("v1", description="API Version")
    api_description: str = Field(
        "API for calculating bills and sending WhatsApp notifications",
        description="API Description",
    )
    # Mobily API Configuration
    mobily_bearer_token: str = Field(..., description="Mobily API Bearer Token")
    mobily_api_key: str = Field(..., description="Mobily API Key")
    mobily_api_url: str = Field(
        "https://api.mobily.com.sa/apis/mobilybe/rest/payment/balance/info",
        description="Mobily API URL",
    )
    mobily_auth_url: str = Field(
        "https://api.mobily.com.sa/apis/api/oauth-server/oauth/token",
        description="Mobily Auth URL",
    )
    mobily_app_version: str = Field("4.27", description="Mobily App Version")
    mobily_app_id: str = Field("Iconick_IOS", description="Mobily App ID")
    mobily_device_id: str = Field(..., description="Mobily Device ID")
    mobily_transaction_id: str = Field(..., description="Mobily Transaction ID")
    mobily_session_id: str = Field(..., description="Mobily Session ID")
    mobily_request_date: str = Field(..., description="Mobily Request Date")
    mobily_auth_basic: str = Field(..., description="Mobily Basic Auth Token")
    mobily_device_model: str = Field("iPhone 15 Pro Max", description="Device Model")
    mobily_os_type: str = Field("IOS", description="OS Type")
    mobily_os_version: str = Field("18.1.1", description="OS Version")
    mobily_lang: str = Field("AR", description="Language")

    # WhatsApp Configuration
    callmebot_api_url: str = Field(
        "https://api.callmebot.com/whatsapp.php", description="CallMeBot API URL"
    )

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

__all__ = ["settings"]
