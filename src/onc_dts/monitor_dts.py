import argparse
from dotenv import load_dotenv, find_dotenv
import os
import logging

import requests

from onc_dts.utils import parse_xt_json
from time import sleep
import json

import itertools
import sys

spinner = itertools.cycle(['-', '/', '|', '\\'])

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

def fetch_onc_realtime_data(device_code, date_from, get_latest=False, row_limit=100):
    """
    Fetches ONC Realtime Data - raw readings for a given device and saves the response as JSON.

    Args:
        device_code (str): The device code to query.
        date_from (str): Start date for data retrieval (YYYY-MM-DD).
        row_limit (int): Maximum number of rows to retrieve.
        size_limit (int): Maximum size of data to retrieve.
        output_format (str): Format of the output data.
        get_latest (str): Whether to get the latest data ("true"/"false").
        onc_api_token (str): ONC API token for authentication.
        data_dir (Path): Directory to save data.
        logging (logging.Logger): Logger for info/error messages.

    Returns:
        dict: The JSON response from the API if successful, None otherwise.
    """
    url = "https://data.oceannetworks.ca/api/rawdata/device"
    #row_limit = 10
    #output_format
    #get_latest #, onc_api_token, data_dir, logging
    params = {
        "deviceCode": device_code,
        "dateFrom": date_from,
        "rowLimit": row_limit,
        #"sizeLimit": size_limit,
        "outputFormat": "Object",
        "getLatest": get_latest,
        "token": ONC_API_TOKEN
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Optionally save the response to disk
        # try:
        #     with open(data_dir / f"{device_code}_rawdata.json", "w") as f:
        #         json.dump(data, f, indent=4)
        #     logging.info(f"Saved raw data to {device_code}_rawdata.json")
        # except Exception as e:
        #     logging.error(f"Failed to save raw data: {e}")
        return data
    else:
        logging.error(f"Error: {response.status_code} - {response.text}")
        return None


class RawDataFetcher:
    def __init__(self, start_date="2025-07-28"):
        self.onc_api_token = ONC_API_TOKEN
        self.next_date = start_date
        self.device_code = "SILIXADTSXT19083"
        self.json_data = []
        
    def _fetch_next(self):
        found_data = False
        
        while self.next_date is None:
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            result = fetch_onc_realtime_data(self.device_code, self.last_date, get_latest=False, row_limit=1)
            try:
                self.next_date = result['next']['parameters']['dateFrom'] # if result['next'] else None
            except (KeyError, TypeError):
                self.next_date = None
                #logging.info('No next date found, waiting to retry...')
                sleep(5) # wait a bit before retrying
            sys.stdout.write('\b')
        
        while not found_data and self.next_date is not None:
            logging.debug(f'Fetching data from {self.next_date}')
            result = fetch_onc_realtime_data(self.device_code, self.next_date)
            logging.debug(f'Fetched {len(result["data"])} items')
            
            for item in result['data']:
                raw_data = item['rawData']
                if len(raw_data) > 80:
                    raw_data =  raw_data[:80] + ' ...'
                #print(f'{item['sampleTime']}{item['lineType']}{raw_data}')
                
                if item['rawData'].startswith('{"Cmd":"getData",'):
                    found_data = True
                    self.json_data.append(json.loads(item['rawData']))
                try:
                    self.next_date = result['next']['parameters']['dateFrom'] # if result['next'] else None
                except (KeyError, TypeError):
                    self.next_date = None
                self.last_date = item['sampleTime']
            #self.json_data.append(result)
        return result
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if len(self.json_data):
            return self.json_data.pop(0)
        else:
            self._fetch_next()
            return self.__next__()
        
def main() -> None:
    logger.info("Monitoring DTS...")
    parser = argparse.ArgumentParser(description="Monitor DTS with start time.")
    parser.add_argument('--start-time', type=str, required=True, help='Start time for monitoring (e.g., "2024-06-01T12:00:00")')
    parser.add_argument('--log-level', type=str, default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set logging level (default: INFO)')
    args = parser.parse_args()
    # Set log level only for this script and selected modules
    logger.setLevel(args.log_level.upper())
    logging.getLogger("onc_dts.utils").setLevel(args.log_level.upper())

    start_time = args.start_time
    logger.info(f"Monitoring DTS from start time: {start_time}")
    # Add monitoring logic here
    
    fetcher = RawDataFetcher(start_date=start_time) # last reading: "2025-07-30T20:35:59.134Z"
    
    for data in fetcher:
        dts_data = parse_xt_json(data['Resp'],trim=True)
        
        temp = dts_data['temp_data'] - 273.15 # convert from Kelvin to Celsius 273.15
        dat_info = data['Resp']['processed data']
        print(f'## Channel {dat_info["forward channel"] + 1} - {dat_info["measurement start time"]}')

        chunk_size = 20
        temp_list = ['%6.3f' % float(t)  for t in temp[0::4*5]]
        chunks = [temp_list[i:i + chunk_size] for i in range(0, len(temp_list), chunk_size)]

        print('    ' + ' '.join([f'{m:5d}m' for m in range(0, 100, 5)]))

        for i, chunk in enumerate(chunks):
            print(f'{chunk_size*5*i:3d}m ' + ' '.join(chunk))
        print('')
    