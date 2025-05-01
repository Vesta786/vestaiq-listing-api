# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
import openai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define schema
class ListingRequest(BaseModel):
    propertyType: str
    location: str
    bedrooms: int
    bathrooms: int
    features: str
    tone: str
    listingType: str
    propertyNumber: str
    postcode: str
    propertySize: str
    tenure: Optional[str] = None
    condition: Optional[str] = None
    recentlyRenovated: Optional[str] = None
    floorLevel: Optional[str] = None
    furnished: Optional[str] = None
    liftAccess: Optional[str] = None
    parking: Optional[str] = None
    outdoorSpace: Optional[str] = None

# Add error handler to log validation issues
@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    print("ERROR occurred during request:", await request.json())
    print("Exception:", str(exc))
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )

@app.post("/generate-listing")
async def generate_listing(data: ListingRequest):
    prompt = (
        f"Write a {data.tone} real estate listing for a {data.bedrooms}-bedroom, "
        f"{data.bathrooms}-bathroom {data.propertyType} in {data.location}. "
        f"Highlight features such as: {data.features}. "
        "Make it engaging and ready to publish."
    )

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful real estate listing assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=400,
    )

    listing = response.choices[0].message.content.strip()
    return {"listing": listing}
