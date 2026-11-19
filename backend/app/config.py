import os
from pathlib import Path
from dotenv import load_dotenv

# Get the backend directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Get Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")