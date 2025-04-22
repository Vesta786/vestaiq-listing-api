from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS so Wix can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your OpenAI key here
openai.api_key = os.getenv("OPENAI_API_KEY")  # Use env variable in production

class ListingRequest(BaseModel):
    property_type: str
    location: str
    bedrooms: int
    bathrooms: int
    features: str
    tone: str = "professional"

@app.post("/generate-listing")
async def generate_listing(data: ListingRequest):
    prompt = f"""
    Write a {data.tone} real estate listing for a {data.bedrooms}-bedroom, {data.bathrooms}-bathroom {data.property_type} in {data.location}.
    Highlight features such as: {data.features}.
    Make it engaging and ready to publish.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful real estate listing assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=400
    )

    listing = response.choices[0].message.content.strip()
    return {"listing": listing}
