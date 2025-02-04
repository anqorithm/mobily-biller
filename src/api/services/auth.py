import httpx
from fastapi import HTTPException
from ..config import settings
from ..models import TokenResponse
from ..utils.logger import setup_logger

logger = setup_logger("auth_service")


async def get_access_token() -> str:
    async with httpx.AsyncClient(verify=False) as client:
        try:
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
                "Accept-Language": "ar;q=1.0",
                "ADRUM": "isAjax:true",
                "ADRUM_1": "isMobile:true",
                "apikey": settings.mobily_api_key,
                "app_id": settings.mobily_app_id,
                "app_version": settings.mobily_app_version,
                "Authorization": settings.mobily_auth_basic,
                "Cache-Control": "no-cache",
                "cem-key": settings.mobily_api_key,
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "api.mobily.com.sa",
                "isTesting": "false",
                "User-Agent": f"Mobily/{settings.mobily_app_version} (com.mobily.mobilyapp; build:1562; iOS {settings.mobily_os_version}) Alamofire/5.9.1",
            }

            data = {
                "app_id": settings.mobily_app_id,
                "app_version": settings.mobily_app_version,
                "device_id": settings.mobily_device_id,
                "device_model": settings.mobily_device_model,
                "grant_type": "client_credentials",
                "lang": settings.mobily_lang,
                "os_type": settings.mobily_os_type,
                "os_version": settings.mobily_os_version,
                "transactionId": settings.mobily_transaction_id,
            }

            logger.info("Making auth request")
            logger.debug(f"Headers: {headers}")
            logger.debug(f"Data: {data}")

            response = await client.post(
                settings.mobily_auth_url,
                headers=headers,
                data=data,
                timeout=30.0,
            )

            response.raise_for_status()
            response_data = response.json()
            logger.info(f"Token response: {response_data}")
            token_response = TokenResponse(**response_data)
            logger.info(f"Access token: {token_response.access_token}")
            return token_response.access_token

        except Exception as e:
            error_msg = f"Failed to obtain access token: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise HTTPException(status_code=500, detail=error_msg)
