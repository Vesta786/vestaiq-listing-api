from fastapi import FastAPI
from pydantic import BaseModel
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

class ListingRequest(BaseModel):
    propertytype: str
    location: str
    bedrooms: int
    bathrooms: int
    features: str
    tone: str
    listingType: str
    propertyNumber: str
    postcode: str
    propertySize: str
    tenure: str
    condition: str
    recentlyRenovated: str
    floorLevel: str
    furnished: str
    liftAccess: str
    parking: str
    outdoorSpace: str

@app.post("/generate-listing")
async def generate_listing(data: ListingRequest):
    prompt = (
        f"Write a {data.tone} real estate listing for a {data.bedrooms}-bedroom, "
        f"{data.bathrooms}-bathroom {data.property_type} in {data.location}. "
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
