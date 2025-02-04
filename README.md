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


