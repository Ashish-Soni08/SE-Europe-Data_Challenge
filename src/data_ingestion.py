import argparse
import datetime
import pandas as pd
import logging
from utils import perform_get_request, xml_to_load_dataframe, xml_to_gen_data

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_load_data_from_entsoe(regions, periodStart='202201010000', periodEnd='202212312300', output_path='./data'):
    url = 'https://web-api.tp.entsoe.eu/api'
    params = {
        'securityToken': '1d9cd4bd-f8aa-476c-8cc1-3442dc91506d',
        'documentType': 'A65',
        'processType': 'A16',
        'outBiddingZone_Domain': 'FILL_IN',
        'periodStart': periodStart,
        'periodEnd': periodEnd,
    }

    for region, area_code in regions.items():
        logging.info(f'Fetching load data for {region}...')
        params['outBiddingZone_Domain'] = area_code

        response_content = perform_get_request(url, params)
        df = xml_to_load_dataframe(response_content)

        df.to_csv(f'{output_path}/load_{region}.csv', index=False)
        logging.info(f"Finished Fetching Load Data for {region}")
    logging.info("Load Data fetched successfully")

def get_gen_data_from_entsoe(regions, periodStart='202201010000', periodEnd='202212312300', output_path='./data'):
    url = 'https://web-api.tp.entsoe.eu/api'
    params = {
        'securityToken': '1d9cd4bd-f8aa-476c-8cc1-3442dc91506d',
        'documentType': 'A75',
        'processType': 'A16',
        'outBiddingZone_Domain': 'FILL_IN',
        'in_Domain': 'FILL_IN',
        'periodStart': periodStart,
        'periodEnd': periodEnd,
    }
    green_energy_codes = ['B01', 'B09', 'B10', 'B11', 'B12', 'B13', 'B15', 'B16', 'B17', 'B18', 'B19']

    for region, area_code in regions.items():
        logging.info(f'Fetching generation data for {region}...')
        params['outBiddingZone_Domain'] = area_code
        params['in_Domain'] = area_code

        response_content = perform_get_request(url, params)
        
        dfs = xml_to_gen_data(response_content)
        
        for psr_type, df in dfs.items():
            if psr_type in green_energy_codes:
                df.to_csv(f'{output_path}/gen_{region}_{psr_type}.csv', index=False)
                logging.info(f"Finished Fetching Data for {region} and {psr_type}")
    logging.info("Generation Data fetched successfully")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Data ingestion script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--start_time', 
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), 
        default=datetime.datetime(2023, 1, 1), 
        help='Start time for the data to download, format: YYYY-MM-DD'
    )
    parser.add_argument(
        '--end_time', 
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), 
        default=datetime.datetime(2023, 1, 2), 
        help='End time for the data to download, format: YYYY-MM-DD'
    )
    parser.add_argument(
        '--output_path', 
        type=str, 
        default='./data',
        help='Name of the output file'
    )
    return parser.parse_args()

def main(start_time, end_time, output_path):
    
    regions = {
        'HU': '10YHU-MAVIR----U',
        'IT': '10YIT-GRTN-----B',
        'PO': '10YPL-AREA-----S',
        'SP': '10YES-REE------0',
        'UK': '10Y1001A1001A92E',
        'DE': '10Y1001A1001A83F',
        'DK': '10Y1001A1001A65H',
        'SE': '10YSE-1--------K',
        'NE': '10YNL----------L',
    }

    start_time = start_time.strftime('%Y%m%d%H%M')
    end_time = end_time.strftime('%Y%m%d%H%M')

    get_load_data_from_entsoe(regions, start_time, end_time, output_path)