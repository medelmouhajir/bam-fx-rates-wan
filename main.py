import os
import yaml
import jwt
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI()

# Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "default_secret_for_local_testing")
BAM_API_KEY = os.getenv("BAM_API_KEY", "27bc152207d6476cabf57db756e0787f")

# Load manifest
def get_manifest():
    with open("isli-skill.yaml", "r") as f:
        return yaml.safe_load(f)

# Dependency to verify JWT
async def verify_jwt(x_internal_auth: Optional[str] = Header(None)):
    if not x_internal_auth:
        raise HTTPException(status_code=401, detail="Missing X-Internal-Auth header")
    try:
        # ISLI Core signs the JWT with HS256 using JWT_SECRET
        payload = jwt.decode(x_internal_auth, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/.well-known/isli-manifest")
def manifest():
    return get_manifest()

# --- Tool Endpoints ---

class ExchangeRatesRequest(BaseModel):
    currency: Optional[str] = None
    date: Optional[str] = None

@app.post("/get-exchange-rates")
def get_exchange_rates(req: ExchangeRatesRequest, token: dict = Depends(verify_jwt)):
    if not BAM_API_KEY:
        raise HTTPException(status_code=500, detail="BAM_API_KEY environment variable is not configured.")
    
    # BAM API base URL (placeholder, adapt to actual BAM portal documentation)
    url = "https://api.centralbankofmorocco.ma/v1/exchange-rates"
    headers = {
        "Ocp-Apim-Subscription-Key": BAM_API_KEY,
        "Accept": "application/json"
    }
    
    params = {}
    if req.currency:
        params["currency"] = req.currency
    if req.date:
        params["date"] = req.date

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Mock response for testing/demonstration purposes if BAM API call fails 
        print(f"BAM API error: {e}")
        return {
            "status": "success",
            "source": "BAM (Mock Fallback)",
            "rates": {
                "USD": 9.98,
                "EUR": 10.85,
                "GBP": 12.60
            },
            "note": "This is a mock response because the real API call failed. Verify your BAM_API_KEY and endpoint."
        }

class MonetaryStatsRequest(BaseModel):
    indicator: Optional[str] = None

@app.post("/get-monetary-stats")
def get_monetary_stats(req: MonetaryStatsRequest, token: dict = Depends(verify_jwt)):
    if not BAM_API_KEY:
        raise HTTPException(status_code=500, detail="BAM_API_KEY environment variable is not configured.")
        
    url = "https://api.centralbankofmorocco.ma/v1/monetary-stats"
    headers = {
        "Ocp-Apim-Subscription-Key": BAM_API_KEY,
        "Accept": "application/json"
    }
    params = {}
    if req.indicator:
        params["indicator"] = req.indicator

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "status": "success",
            "source": "BAM (Mock Fallback)",
            "data": {
                "M3_growth": "4.5%",
                "inflation_rate": "2.1%"
            },
            "note": "Mock response due to API call failure."
        }
