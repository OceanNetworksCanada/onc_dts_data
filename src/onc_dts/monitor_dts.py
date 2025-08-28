import argparse
from dotenv import load_dotenv
import os

load_dotenv()

ONC_API_TOKEN = os.getenv("ONC_API_TOKEN")

if not ONC_API_TOKEN:
    raise EnvironmentError("ONC_API_TOKEN not found in environment variables.")

working_dir = os.getcwd()
print(f"Working directory: {working_dir}")

def main() -> None:
    print("Monitoring DTS...")
    parser = argparse.ArgumentParser(description="Monitor DTS with start time.")
    parser.add_argument('--start-time', type=str, required=True, help='Start time for monitoring (e.g., "2024-06-01T12:00:00")')
    args = parser.parse_args()

    start_time = args.start_time
    print(f"Monitoring DTS from start time: {start_time}")
    # Add monitoring logic here