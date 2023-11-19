import argparse
from datetime import datetime as dt
import logging
import os
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_and_reformat(input_date: str, 
                       source_format: str = "%Y-%m-%dT%H:%M%zZ", 
                       target_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Converts a date string from one format to another.

    This function takes a date string in a specified source format, parses it into a
    datetime object, and then reformats it into the specified target format.

    Parameters:
    input_date (str): The date string that needs to be reformatted.
    source_format (str): The format of the input_date. Default is ISO 8601 format with timezone.
    target_format (str): The desired format for the output date string.

    Returns:
    str: A date string reformatted into the target format.

    Example:
    >>> parse_and_reformat("2021-12-31T23:45+00:00Z")
    '2021-12-31 23:45:00'
    """

    # Parse the original date-time string according to the source format
    datetime_obj = dt.strptime(input_date, source_format)
    
    # Reformat to the new format and return
    return datetime_obj.strftime(target_format)

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a DataFrame.

    Parameters:
    file_path (str): Path to the CSV file to be loaded.

    Returns:
    pd.DataFrame: DataFrame containing the loaded data.
    """
    logging.info(f'Loading data from {file_path}')
    df = pd.read_csv(file_path)
    return df

def clean_data(df: pd.DataFrame, data_type: str) -> pd.DataFrame:
    """
    Clean and preprocess the DataFrame based on the type of data.

    Parameters:
    df (pd.DataFrame): The DataFrame to be cleaned.
    data_type (str): Type of the data ('gen' for generation, 'load' for load data).

    Returns:
    pd.DataFrame: Cleaned DataFrame.
    """
    logging.info(f'Cleaning data for {data_type}...')
    if data_type == 'gen':
        df.drop(['EndTime', 'UnitName', 'AreaID', 'PsrType'], axis=1, inplace=True)
        df.rename(columns={'StartTime': 'start_time', 'quantity': 'energy_generated'}, inplace=True)
    elif data_type == 'load':
        df.drop(['EndTime', 'AreaID', 'UnitName'], axis=1, inplace=True)
        df.rename(columns={'StartTime': 'start_time', 'Load': 'energy_consumption'}, inplace=True)
    df.sort_values(['start_time'], inplace=True)
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the DataFrame by converting date strings to datetime objects and resampling.

    Parameters:
    df (pd.DataFrame): DataFrame to preprocess.

    Returns:
    pd.DataFrame: Preprocessed DataFrame.
    """
    logging.info('Preprocessing data...')
    # Convert start_time to the desired format
    df['start_time'] = df['start_time'].apply(parse_and_reformat)
    # Convert start_time to datetime object
    df['start_time'] = pd.to_datetime(df['start_time'])
    
    df.set_index('start_time', inplace=True)
    df = df.resample('1H').sum()

    # Handle missing data: replace NaN values with zeros
    df.fillna(0, inplace=True)

    df.interpolate(method='linear', limit_direction='both', inplace=True)
    df.reset_index(inplace=True)
    
    return df

def save_data(df: pd.DataFrame, output_file: str):
    """
    Save the DataFrame to a CSV file.

    Parameters:
    df (pd.DataFrame): DataFrame to be saved.
    output_file (str): Path to the output CSV file.
    """
    logging.info(f'Saving processed data to {output_file}')
    df.to_csv(output_file, index=False)

def process_file(input_file: str, output_file: str, data_type: str):
    """
    Process a single file - load, clean, preprocess, and save the data.

    Parameters:
    input_file (str): Path to the input file.
    output_file (str): Path to the output file.
    data_type (str): Type of the data ('gen' or 'load').
    """
    df = load_data(input_file)
    df_clean = clean_data(df, data_type)
    df_processed = preprocess_data(df_clean)
    save_data(df_processed, output_file)

def main(source_directory: str, destination_directory: str):
    """
    Main function to process all files in a directory.

    Parameters:
    source_directory (str): Directory containing the raw data files.
    destination_directory (str): Directory to save the processed data.
    """
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
        logging.info(f'Created directory: {destination_directory}')

    for file in os.listdir(source_directory):
        if file.startswith('gen_') and file.endswith('.csv'):
            data_type = 'gen'
        elif file.startswith('load_') and file.endswith('.csv'):
            data_type = 'load'
        else:
            continue

        input_file = os.path.join(source_directory, file)
        modified_file_name = file.replace('.csv', '_modified.csv')
        output_file = os.path.join(destination_directory, modified_file_name)
        logging.info(f'Processing file: {input_file}')
        process_file(input_file, output_file, data_type)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data processing script for Energy Forecasting')
    parser.add_argument('--input_dir', type=str, default='data/raw', help='Directory containing the raw data files')
    parser.add_argument('--output_dir', type=str, default='data/processed', help='Directory to save the processed data')
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)
