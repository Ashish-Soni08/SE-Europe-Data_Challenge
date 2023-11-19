import pandas as pd
import logging
import os
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def merge_country_data(intermediate_directory: str, country_codes: list) -> pd.DataFrame:
    """
    Merge data from multiple country files into a single DataFrame.

    Parameters:
    intermediate_directory (str): Directory containing intermediate data files.
    country_codes (list): List of country codes to process data for.

    Returns:
    pd.DataFrame: Merged DataFrame of all countries' data.
    """
    merged_data = None

    for country_code in country_codes:
        file_path = os.path.join(intermediate_directory, f'{country_code}_intermediate.csv')
        if not os.path.exists(file_path):
            logging.warning(f"File not found: {file_path}")
            continue

        country_data = pd.read_csv(file_path)
        
        if merged_data is None:
            merged_data = country_data
        else:
            merged_data = pd.merge(merged_data, country_data, on='start_time', how='outer')

    return merged_data

def main(intermediate_directory: str, output_file: str):
    """
    Main function to create the train.csv file from intermediate data files.

    Parameters:
    intermediate_directory (str): Directory containing intermediate data files.
    output_file (str): Path to save the final train.csv file.
    """
    country_codes = ['DE', 'HU', 'IT', 'PO', 'SP', 'UK', 'DK', 'SE', 'NE'] 
    merged_data = merge_country_data(intermediate_directory, country_codes)

    if merged_data is not None:
        merged_data.fillna(0, inplace=True)  # Replace NaNs with zeros
        merged_data.to_csv(output_file, index=False)
        logging.info(f'Train data saved to {output_file}')
    else:
        logging.error('No data to merge. Exiting.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create train.csv from intermediate data files')
    parser.add_argument('--intermediate_dir', type=str, default='data/processed/intermediate', help='Directory containing intermediate data files')
    parser.add_argument('--output_file', type=str, default='data/processed.csv', help='File path for the output train.csv file')
    args = parser.parse_args()
    main(args.intermediate_dir, args.output_file)