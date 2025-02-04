from urllib.parse import quote
import httpx
from fastapi import HTTPException
from ..config import settings
from ..utils.logger import setup_logger

logger = setup_logger("whatsapp_service")


async def send_whatsapp_message(phone: str, apikey: str, message: str) -> bool:
    encoded_message = quote(message)
    url = f"{settings.callmebot_api_url}?phone={phone}&text={encoded_message}&apikey={apikey}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            return response.status_code == 200
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error sending WhatsApp message: {str(e)}"
            )
