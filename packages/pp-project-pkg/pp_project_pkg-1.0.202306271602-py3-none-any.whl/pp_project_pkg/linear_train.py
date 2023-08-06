"""
Module for training linear model
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt


def train_model(data,logger=None):
    """
    Trains a linear model on the data and upload the model to the cloud with parameters
    
    Args:
        data: pd.DataFrame
        logger: logger object
    Returns:
        None
    """
    # Reading data
    data = pd.read_csv('data.csv')

    # Selecting relevant input features
    X = data[['actual_covers', 'food_item_consumed', 'nationalities', 'day_of_the_week']]
    y = data[['predicted_covers', 'food_item_waste']]

    # Encoding categorical features (nationalities, sex, day_of_the_week)
    categorical_features = ['nationalities', 'day_of_the_week']
    one_hot_encoder = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', one_hot_encoder, categorical_features)
        ],
        remainder='passthrough'
    )

    # Creating a Linear Regression model
    model = LinearRegression()

    # Creating a pipeline with the preprocessor and the model
    pipeline_linear = Pipeline(steps=[('preprocessor', preprocessor),
                               ('model', model)])

    # Splitting data into training and test sets (keeping the latest 10% for evaluation)
    train_size = int(0.9 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # Training the model
    pipeline_linear.fit(X_train, y_train)

    # Predicting and evaluating
    y_pred = pipeline_linear.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred) 
    r2 = r2_score(y_test, y_pred)

    if logger:
        logger.info('Mean squared error: {}'.format(mse))
        logger.info('Mean absolute error: {}'.format(mae))
        logger.info('R2 score: {}'.format(r2))   

    # Check feature importances
    importances = model.feature_importances_ 
    feature_df = pd.DataFrame({'Feature': list(X), 'Importance': importances})
    feature_df = feature_df.sort_values('Importance', ascending=False)


def train_randomforest(data,logger=None):
    """
    Train a random forest model on the data and upload the model to the cloud with parameters

    Args:
        data: pd.DataFrame
        logger: logger object
    Returns:
        None
    """
    data = pd.read_csv('data.csv')

    # Selecting relevant input features
    X = data[['actual_covers', 'food_item_consumed', 'nationalities', 'sex', 'day_of_the_week']]
    y = data[['predicted_covers', 'food_item_waste']]

    # Encoding categorical features (nationalities, sex, day_of_the_week)
    categorical_features = ['nationalities', 'sex', 'day_of_the_week']
    one_hot_encoder = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', one_hot_encoder, categorical_features)
        ],
        remainder='passthrough'
    )

    # Splitting data into training and test sets (keeping the latest 10% for evaluation)
    train_size = int(0.9 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    rf_model = RandomForestRegressor(n_estimators=100) 
    pipeline_randomforest = Pipeline(steps=[('preprocessor', preprocessor), 
                               ('model', rf_model)])
    pipeline_randomforest.fit(X_train, y_train) 
    y_pred = pipeline_randomforest.predict(X_test)
 
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred) 
    r2 = r2_score(y_test, y_pred)    

    if logger:
        logger.info('Mean squared error: {}'.format(mse))
        logger.info('Mean absolute error: {}'.format(mae))
        logger.info('R2 score: {}'.format(r2))   
            
    # Check feature importances
    importances = rf_model.feature_importances_ 
    feature_df = pd.DataFrame({'Feature': list(X), 'Importance': importances})
    feature_df = feature_df.sort_values('Importance', ascending=False)



def plot_res(y_test, y_pred):
    """
    Plots the results of the model
    
    Args:
        y_test: pd.DataFrame
        y_pred: pd.DataFrame
    Returns:
        None
    """
    # Explore results
    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(), y_test.max()], [y_pred.min(), y_pred.max()], '--r')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.show()

    
def outliers(data,threshold_val=2.0):
    """
    Detect outliers in the file
    
    Args:
        data: pd.DataFrame
        threshold_val: float
    Returns:
        pd.DataFrame
    """
    
    avg_events = data['events'].mean()
    
    # Calculate the range of events
    range_events = data['events'].max() - data['events'].min()

    # Define a threshold value for outliers
    threshold = threshold_val * range_events

    # Identify the outliers based on the threshold value
    outliers = data[data['events'] > avg_events + threshold]

    return outliers