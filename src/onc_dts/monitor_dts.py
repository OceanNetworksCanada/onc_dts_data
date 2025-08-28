import argparse

def main() -> None:
    print("Monitoring DTS...")
    parser = argparse.ArgumentParser(description="Monitor DTS with start time.")
    parser.add_argument('--start-time', type=str, required=True, help='Start time for monitoring (e.g., "2024-06-01T12:00:00")')
    args = parser.parse_args()

    start_time = args.start_time
    print(f"Monitoring DTS from start time: {start_time}")
    # Add monitoring logic here