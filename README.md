# Mobily Biller API

## TL;DR

## Description

This is a simple API that calculates the bills for a list of phone numbers and sends a WhatsApp notification to the user.


# Running the API

## Build and Run with Docker
```bash
docker compose up --build
```

## Hit the API
```bash
curl -X GET "http://localhost:{PORT}/v1/bills/calculate?numbers=966500000000,966500000001&national_id=1234567890"
```


## Example


### Request


```bash
curl -X 'GET' \
  'http://localhost:8000/v1/bills/calculate?numbers=966561896009%2C966561896009%2C966561896009%2C966561896009%2C966561896009&national_id=230507' \
  -H 'accept: application/json'
```


### Response


```json
{
  "id": "230507",
  "numbers": [
    "966561896009",
    "966561896009",
    "966561896009",
    "966561896009",
    "966561896009"
  ],
  "bills": [
    {
      "number": "966561896009",
      "amount": 471.5,
      "index": 1
    },
    {
      "number": "966561896009",
      "amount": 471.5,
      "index": 2
    },
    {
      "number": "966561896009",
      "amount": 471.5,
      "index": 3
    },
    {
      "number": "966561896009",
      "amount": 471.5,
      "index": 4
    },
    {
      "number": "966561896009",
      "amount": 471.5,
      "index": 5
    }
  ],
  "total": 2357.5,
  "whatsapp_notification_sent": false
}

```