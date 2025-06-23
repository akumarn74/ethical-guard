import os
import uvicorn
import logging
from google.adk.cli.fast_api import get_fast_api_app

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory where your agents live (relative to main.py)
AGENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))


# Example session DB URL (can be SQLite for demo)
SESSION_DB_URL = "sqlite:///./sessions.db"

# Allowed CORS origins
ALLOWED_ORIGINS = ["http://localhost", "http://localhost:8080", "*"]

# Set to True to serve the ADK dev UI
SERVE_WEB_INTERFACE = True

# Create the FastAPI app with your agent directory
app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_DB_URL,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)

# Optionally, add custom FastAPI routes here

@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    # Use the PORT environment variable for Cloud Run compatibility
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
