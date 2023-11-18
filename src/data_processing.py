import os
import pandas as pd
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    logging.info(f'Loading data from {file_path}')
    df = pd.read_csv(file_path)
    return df

def clean_data(df):
    logging.info('Cleaning data...')
    df.drop(['EndTime', 'UnitName', 'AreaID', 'PsrType'], axis=1, inplace=True)
    df.sort_values(['StartTime'], inplace=True)
    df.rename(columns = {'StartTime': 'start_time', 'quantity' : 'energy_generated'}, inplace=True)
    return df

def preprocess_data(df):
    logging.info('Preprocessing data...')
    
    df['start_time'] = df['start_time'].str[:-1]  # Remove 'Z'
    df['start_time'] = pd.to_datetime(df['start_time'])
    
    df.set_index('start_time', inplace=True)
    df = df.resample('1H').sum()
    
    df['energy_generated'] = df['energy_generated'].interpolate(method='linear')
    
    df.reset_index(inplace=True)
    
    return df

def save_data(df, output_file):
    logging.info(f'Saving processed data to {output_file}')
    df.to_csv(output_file, index=False)

def process_file(file_path, output_file):
    df = load_data(file_path)
    df_clean = clean_data(df)
    df_processed = preprocess_data(df_clean)
    save_data(df_processed, output_file)

def main(source_directory, destination_directory):
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
        logging.info(f'Created directory: {destination_directory}')

    for file in os.listdir(source_directory):
        if file.startswith('gen_') and file.endswith('.csv'):
            file_path = os.path.join(source_directory, file)
            modified_file_name = file.replace('.csv', '_modified.csv')
            output_file = os.path.join(destination_directory, modified_file_name)
            logging.info(f'Processing file: {file_path}')
            process_file(file_path, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data processing script for Energy Forecasting Hackathon')
    parser.add_argument('--input_dir', type=str, default='data/raw/2022_to_2023', help='Directory containing the raw data files')
    parser.add_argument('--output_dir', type=str, default='data/processed/2022_to_2023', help='Directory to save the processed data')
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)
