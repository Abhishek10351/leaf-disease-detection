from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings

GEMINI_API_KEY = settings.GEMINI_API_KEY

if GEMINI_API_KEY is None:
    raise Exception("GEMINI_API_KEY not found in environment variables")


# Initialize Gemini Pro Vision model for image analysis
gemini_vision_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.1
)