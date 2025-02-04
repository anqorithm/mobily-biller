import httpx
from fastapi import HTTPException
from ..config import settings
from ..models import MobilyRequest, MobilyResponse
from ..utils.logger import setup_logger
from .auth import get_access_token

logger = setup_logger("mobily_service")


async def fetch_bill_info(number: str, national_id: str) -> float:
    """Fetch bill information for a single number"""
    async with httpx.AsyncClient(verify=False) as client:
        try:
            session_id = await get_access_token()
            logger.info(f"Using session ID: {session_id}")

            request_data = MobilyRequest(
                VERSION=settings.mobily_app_version,
                NATIONAL_ID=national_id,
                APP_ID=settings.mobily_app_id,
                MSISDN=number,
                DEVICE_ID=settings.mobily_device_id,
                SESSION_ID=session_id,
            )

            headers = {
                "ADRUM": "isAjax:true",
                "ADRUM_1": "isMobile:true",
                "Accept": "application/json",
                "Accept-Encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
                "Accept-Language": "en-SA;q=1, ar-SA;q=0.9",
                "App-Version": f"{settings.mobily_app_version}, 1562",
                "Authorization": f"Bearer {session_id}",
                "Connection": "keep-alive",
                "Host": "api.mobily.com.sa",
                "User-Agent": "userAgent",
                "apikey": settings.mobily_api_key,
                "app_id": settings.mobily_app_id,
                "app_version": settings.mobily_app_version,
                "cem-key": settings.mobily_api_key,
                "content-type": "application/json",
            }

            logger.info(
                f"Making request to Mobily API - Number: {number}, National ID: {national_id}"
            )
            logger.debug(f"Request data: {request_data.model_dump()}")

            response = await client.post(
                settings.mobily_api_url,
                headers=headers,
                json=request_data.model_dump(),
                timeout=30.0,
            )

            response.raise_for_status()
            response_data = response.json()
            logger.info(f"Received response from Mobily API: {response_data}")

            mobily_response = MobilyResponse(**response_data)

            if mobily_response.STATUS_CODE == "1":
                error_msg = (
                    mobily_response.ERROR_DESCRIPTION or "Unknown error from Mobily API"
                )
                logger.error(f"Mobily API error: {error_msg}")
                raise HTTPException(status_code=400, detail=error_msg)

            if not mobily_response.AMOUNT:
                error_msg = f"No amount returned for number {number}"
                logger.error(f"{error_msg}. Response: {response_data}")
                raise HTTPException(status_code=400, detail=error_msg)

            try:
                amount = float(mobily_response.AMOUNT)
                logger.info(
                    f"Successfully fetched bill amount: {amount} for number: {number}"
                )
                return amount
            except (ValueError, TypeError):
                error_msg = (
                    f"Invalid amount format in response: {mobily_response.AMOUNT}"
                )
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)

        except httpx.TimeoutException:
            error_msg = "Request timed out while contacting Mobily API"
            logger.error(error_msg)
            raise HTTPException(status_code=504, detail=error_msg)

        except httpx.ConnectError:
            error_msg = "Could not connect to Mobily API"
            logger.error(error_msg)
            raise HTTPException(status_code=503, detail=error_msg)

        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error occurred: {e.response.text}"
            logger.error(error_msg)
            raise HTTPException(status_code=e.response.status_code, detail=error_msg)

        except HTTPException:
            raise

        except Exception as e:
            error_msg = f"Unexpected error fetching bill for {number}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise HTTPException(status_code=500, detail=error_msg)
