from fastapi import FastAPI, HTTPException, Query
import asyncio
from api.services.mobily import fetch_bill_info
from api.services.whatsapp import send_whatsapp_message
from api.models import BillRequest, BillResponse, BillItem
from api.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Mobily Biller API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/v1/bills/calculate", response_model=BillResponse)
async def calculate_bills(
    numbers: str = Query(..., description="Comma-separated list of phone numbers"),
    national_id: str = Query(..., description="National ID"),
    options: str = Query(
        None, description="Optional features (e.g., send_to_whatsapp)"
    ),
    callmebot_phone: str = Query(None, description="CallMeBot phone number"),
    callmebot_apikey: str = Query(None, description="CallMeBot API key"),
):
    number_list = [num.strip() for num in numbers.split(",")]
    tasks = [fetch_bill_info(number, national_id) for number in number_list]
    bills = await asyncio.gather(*tasks)
    total = sum(bills)

    bills_list = [
        BillItem(number=number, amount=bill, index=i + 1)
        for i, (number, bill) in enumerate(zip(number_list, bills))
    ]

    result = BillResponse(
        id=national_id,
        numbers=number_list,
        bills=bills_list,
        total=total,
    )

    if options == "send_to_whatsapp" and callmebot_phone and callmebot_apikey:
        message = f"*Bills Summary*\nID: {national_id}\nTotal Amount: {total}\n"
        for bill in bills_list:
            message += f"\n{bill.number} (#{bill.index}): {bill.amount}"

        whatsapp_sent = await send_whatsapp_message(
            callmebot_phone, callmebot_apikey, message
        )
        result.whatsapp_notification_sent = whatsapp_sent

    return result
