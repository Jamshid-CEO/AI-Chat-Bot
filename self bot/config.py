import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TUIT_USERNAME = os.getenv("TUIT_USERNAME")
TUIT_PASSWORD = os.getenv("TUIT_PASSWORD")
