#!/bin/bash

# Usage:
# ./run_pipeline.sh <start_date> <end_date> <raw_data_dir> <intermediate_data_dir> <final_data_dir> <model_file> <test_data_file> <predictions_file>
# Example:
# ./run_pipeline.sh 2020-01-01 2020-01-31 data/raw data/processed/intermediate data/processed/final models/model.pkl data/test_data.csv predictions/predictions.json

# Get command line arguments
start_date="$1"
end_date="$2"
raw_data_dir="$3"
intermediate_data_dir="$4"
final_data_dir="$5"
model_file="$6"
test_data_file="$7"
predictions_file="$8"

# Run data_ingestion.py
echo "Starting data ingestion..."
python src/data_ingestion.py --start_date="$start_date" --end_date="$end_date" --output_dir="$raw_data_dir"

# Run data_processing_1.py
echo "Starting data processing (Stage 1)..."
python src/data_processing_1.py --input_dir="$raw_data_dir" --output_dir="$intermediate_data_dir"

# Run data_processing_2.py
echo "Starting data processing (Stage 2)..."
python src/data_processing_2.py --input_dir="$intermediate_data_dir" --output_dir="$final_data_dir"

# Run final_data_processing.py
echo "Starting final data processing..."
python src/final_data_processing.py --intermediate_dir="$final_data_dir" --output_file="data/processed.csv"

# Run model_training.py
echo "Starting model training..."
python src/model_training.py --input_file="data/train.csv" --model_file="$model_file"

# Run model_prediction.py
echo "Starting prediction..."
python src/model_prediction.py --input_file="$test_data_file" --model_file="$model_file" --output_file="$predictions_file"

echo "Pipeline completed."