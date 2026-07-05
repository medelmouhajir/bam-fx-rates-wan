# Bank Al-Maghrib Exchange Rates & Monetary Stats (ISLI Skill)

This repository contains the `bam-fx-rates-wan` ISLI AI Skill. It is a standalone Dockerized HTTP microservice built on FastAPI that conforms to the **ISLI v2.0 Universal Skill Runtime (USR)**.

The skill provides ISLI AI agents with the ability to query the Bank Al-Maghrib (BAM) public developer API for live Moroccan Dirham (MAD) exchange rates and broad monetary statistics.

## Features
- **Get Exchange Rates**: Fetches the daily reference exchange rates for MAD against major currencies.
- **Get Monetary Stats**: Retrieves specific macro-economic indicators provided by BAM.

## Prerequisites
- Docker (recommended) or Python 3.9+
- A valid BAM API Key

### How to get an API Key
1. Go to the [Bank Al-Maghrib API Portal](https://apihelpdesk.centralbankofmorocco.ma/signup).
2. Create a free developer account and verify your email.
3. Log in, go to the **Products** section, and subscribe to the relevant API products.
4. Copy your `Primary key` from your profile.

## Running Locally (Without Docker)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the FastAPI server (uses the default API key set in `main.py` or your own):
   ```bash
   BAM_API_KEY="your_api_key_here" uvicorn main:app --reload
   ```
   The service will be running at `http://127.0.0.1:8000`.

## Running with Docker (Production/ISLI Core)

ISLI Core automatically pulls the repository and builds the Docker container. To test this manually:

1. Build the image:
   ```bash
   docker build -t isli-skill-bam-fx .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 -e BAM_API_KEY="your_api_key_here" -e JWT_SECRET="your_secret" isli-skill-bam-fx
   ```

## ISLI Integration
This skill requires an `X-Internal-Auth` header with a valid JWT on every tool request. This ensures secure communication between the ISLI Core engine and this skill container. The JWT is signed using the `JWT_SECRET` environment variable.

### Core Endpoints
- `GET /health` : Container health check.
- `GET /.well-known/isli-manifest` : Returns the JSON representation of `isli-skill.yaml`.
- `POST /get-exchange-rates` : Tool endpoint for FX rates.
- `POST /get-monetary-stats` : Tool endpoint for monetary stats.
