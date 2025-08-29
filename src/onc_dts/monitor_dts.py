import argparse
from dotenv import load_dotenv, find_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env_file = find_dotenv(usecwd=True)
logger.info(f"Loading .env file from: {env_file}")
out = load_dotenv(env_file, verbose=True)
logger.info(f".env loaded: {out}")

ONC_API_TOKEN = os.getenv("ONC_API_TOKEN")

working_dir = os.getcwd()
logger.info(f"Working directory: {working_dir}")

if not ONC_API_TOKEN:
    logger.warning(f"ONC_API_TOKEN not found in environment variables. {ONC_API_TOKEN}")

def main() -> None:
    logger.info("Monitoring DTS...")
    parser = argparse.ArgumentParser(description="Monitor DTS with start time.")
    parser.add_argument('--start-time', type=str, required=True, help='Start time for monitoring (e.g., "2024-06-01T12:00:00")')
    args = parser.parse_args()

    start_time = args.start_time
    logger.info(f"Monitoring DTS from start time: {start_time}")
    # Add monitoring logic here