import argparse
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier


def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['start_time'], index_col='start_time')
    return df

def split_data(df):
    
    X_train = df.drop('label', axis=1)
    y_train = df['label']
    
    return X_train, y_train

def train_model(X_train, y_train):
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def save_model(model, model_path):
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Model training script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file', 
        type=str, 
        default='data/train.csv', 
        help='Path to the processed data file to train the model'
    )
    parser.add_argument(
        '--model_file', 
        type=str, 
        default='models/random_forest_model.pkl', 
        help='Path to save the trained model'
    )
    return parser.parse_args()

def main(input_file, model_file):
    df = load_data(input_file)
    X_train, y_train = split_data(df)
    model = train_model(X_train, y_train)
    save_model(model, model_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.model_file)