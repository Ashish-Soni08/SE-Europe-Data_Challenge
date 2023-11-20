import argparse
import json
import pandas as pd
import pickle


def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['start_time'], index_col='start_time')
    return df

def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

def make_predictions(df, model):
    X_test = df.drop('label', axis=1)
    predictions = model.predict(X_test)
    return predictions

def save_predictions(predictions, predictions_file):
    predictions = {'target': {str(index): int(prediction) for index, prediction in enumerate(predictions)}}
    predictions_json = json.dumps(predictions)
    with open(predictions_file, 'w') as file:
        file.write(predictions_json)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Prediction script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file', 
        type=str, 
        default='data/test_data.csv', 
        help='Path to the test data file to make predictions'
    )
    parser.add_argument(
        '--model_file', 
        type=str, 
        default='models/random_forest_model.pkl',
        help='Path to the trained model file'
    )
    parser.add_argument(
        '--output_file', 
        type=str, 
        default='predictions/predictions.json', 
        help='Path to save the predictions'
    )
    return parser.parse_args()

def main(input_file, model_file, output_file):
    df = load_data(input_file)
    model = load_model(model_file)
    predictions = make_predictions(df, model)
    save_predictions(predictions, output_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.model_file, args.output_file)
