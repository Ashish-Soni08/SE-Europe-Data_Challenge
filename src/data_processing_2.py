import pandas as pd
import logging
import os
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def aggregate_gen_data(processed_directory: str, country_code: str) -> pd.DataFrame:
    """
    Aggregate generation data from multiple files into a single DataFrame.

    Parameters:
    processed_directory (str): Directory containing processed data files.
    country_code (str): Country code for which to aggregate data.

    Returns:
    pd.DataFrame: Aggregated DataFrame of generation data.
    """
    gen_files = [os.path.join(processed_directory, f) for f in os.listdir(processed_directory) 
                 if f.startswith(f'gen_{country_code}_') and f.endswith('_modified.csv')]
    gen_data = pd.concat([pd.read_csv(file) for file in gen_files], ignore_index=True)
    gen_data = gen_data.groupby('start_time').sum().reset_index()
    gen_data.rename(columns={'energy_generated': f'green_energy_{country_code}'}, inplace=True)
    return gen_data

def process_country_data(processed_directory: str, country_code: str, output_directory: str):
    """
    Process and merge generation and load data for a specific country.

    Parameters:
    processed_directory (str): Directory containing the processed data files.
    country_code (str): Country code to process data for.
    output_directory (str): Directory to save the merged data.
    """
    # Aggregate generation data
    aggregated_gen = aggregate_gen_data(processed_directory, country_code)

    # Load the load data
    load_file = os.path.join(processed_directory, f'load_{country_code}_modified.csv')
    load_data = pd.read_csv(load_file)
    load_data.rename(columns={'energy_consumption': f'{country_code}_Load'}, inplace=True)

    # Merge generation and load data
    merged_data = pd.merge(aggregated_gen, load_data, on='start_time', how='outer')

    # Save the merged data
    output_file = os.path.join(output_directory, f'{country_code}_intermediate.csv')
    merged_data.to_csv(output_file, index=False)
    logging.info(f"Data for {country_code} processed and saved to {output_file}")

def main(processed_directory: str, output_directory: str):
    """
    Main function to process all country data files.

    Parameters:
    processed_directory (str): Directory containing the processed data files.
    output_directory (str): Directory to save the final merged data.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        logging.info(f'Created directory: {output_directory}')

    country_codes = ['DE', 'HU', 'IT', 'PO', 'SP', 'UK', 'DK', 'SE', 'NE'] 
    for country_code in country_codes:
        logging.info(f'Processing data for {country_code}')
        process_country_data(processed_directory, country_code, output_directory)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Final Data Processing Script for Energy Forecasting')
    parser.add_argument('--processed_dir', type=str, default='data/processed/2022_to_2023', help='Directory containing the processed data files')
    parser.add_argument('--output_dir', type=str, default='data/processed/intermediate', help='Directory to save the final merged data')
    args = parser.parse_args()
    main(args.processed_dir, args.output_dir)
