from dotenv import load_dotenv,find_dotenv
import os

load_dotenv(find_dotenv())

google_api_url = os.environ.get("GOOGLE_SHEET_API_KEY")