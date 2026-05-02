import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import datetime

# Load the dataset from the URL
url = 'https://raw.githubusercontent.com/datasets/finance-vix/master/data/vix-daily.csv'


# Function to load and inspect the data
def load_data_from_url(url):
    try:
        data = pd.read_csv(url)
        print("Columns in the CSV:", data.columns)  # Print the columns to inspect
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


# Load data from the specified URL
data = load_data_from_url(url)

# If data is loaded successfully, process it
if data is not None:
    # Update the column names to match the CSV file
    data.columns = ['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE']  # Ensure we have the correct column names

    # Remove rows with missing data or invalid entries
    data.dropna(subset=['CLOSE'], inplace=True)  # Drop rows where 'CLOSE' is NaN
    data = data[pd.to_datetime(data['DATE'], errors='coerce').notna()]  # Keep rows with valid date format

    # Ensure the 'DATE' column is in datetime format
    data['DATE'] = pd.to_datetime(data['DATE'], format='%m/%d/%Y')

    # Prepare the data for Polynomial Regression
    data['DATE_Ordinal'] = data['DATE'].apply(lambda x: x.toordinal())  # Convert date to ordinal for regression
    X = data['DATE_Ordinal'].values.reshape(-1, 1)  # Dates as features (independent variable)

    # Define the target variable for prediction (CLOSE)
    y_close = data['CLOSE'].values

    # Adjusted window size for more sensitive predictions
    window_size = 25  # Adjusted to capture more recent trends
    predictions_close = []
    actual_values_close = []

    # Prepare initial dataset for rolling window prediction
    for i in range(window_size, len(data)):
        # Create training data for the CLOSE variable
        X_train = data.iloc[i - window_size:i]['DATE_Ordinal'].values.reshape(-1, 1)

        # Train the models for the CLOSE variable with higher polynomial degree for better smoothness
        poly = PolynomialFeatures(degree=5)  # Increased degree for smoother prediction
        X_train_poly = poly.fit_transform(X_train)

        model_close = LinearRegression()
        model_close.fit(X_train_poly, data.iloc[i - window_size:i]['CLOSE'])

        # Predict the next day (i+1) for the CLOSE variable
        next_day_ordinal = data['DATE_Ordinal'].iloc[i]
        next_day_poly = poly.transform([[next_day_ordinal]])

        next_day_pred_close = model_close.predict(next_day_poly)[0]

        # Add predictions and actual values to the list
        predictions_close.append(next_day_pred_close)
        actual_values_close.append(data['CLOSE'].iloc[i])

    # Create a dataframe for predictions with corresponding dates
    prediction_dates = data['DATE'].iloc[window_size:].values
    predicted_data = pd.DataFrame({
        'DATE': prediction_dates,
        'PREDICTED_CLOSE': predictions_close,
        'ACTUAL_CLOSE': actual_values_close
    })

    # Calculate the percentage error for each prediction
    predicted_data['PERCENTAGE_ERROR'] = abs(
        (predicted_data['PREDICTED_CLOSE'] - predicted_data['ACTUAL_CLOSE']) / predicted_data['ACTUAL_CLOSE']) * 100

    # Filter out predictions with percentage error greater than 20%
    predicted_data = predicted_data[predicted_data['PERCENTAGE_ERROR'] <= 20]

    # Apply Exponential Moving Average (EMA) for smoothing the predictions and actual values
    smoothing_window = 30  # Larger smoothing window for finer smoothness
    predicted_data['ACTUAL_CLOSE_SMOOTHED'] = predicted_data['ACTUAL_CLOSE'].ewm(span=smoothing_window,
                                                                                 adjust=False).mean()
    predicted_data['PREDICTED_CLOSE_SMOOTHED'] = predicted_data['PREDICTED_CLOSE'].ewm(span=smoothing_window,
                                                                                       adjust=False).mean()

    # Smooth the percentage error
    predicted_data['PERCENTAGE_ERROR_SMOOTHED'] = predicted_data['PERCENTAGE_ERROR'].ewm(span=smoothing_window,
                                                                                         adjust=False).mean()

    # 100-Day Future Prediction
    future_predictions = []
    future_dates = []
    last_day_ordinal = data['DATE_Ordinal'].iloc[-1]
    last_day_date = data['DATE'].iloc[-1]

    # Predict the next 100 days
    for i in range(100):
        next_day_ordinal = last_day_ordinal + 1
        next_day_poly = poly.transform([[next_day_ordinal]])

        next_day_pred_close = model_close.predict(next_day_poly)[0]

        future_predictions.append(next_day_pred_close)
        future_dates.append(last_day_date + pd.Timedelta(days=1))

        last_day_ordinal = next_day_ordinal
        last_day_date = last_day_date + pd.Timedelta(days=1)

    # Create a dataframe for future predictions
    future_data = pd.DataFrame(future_predictions, columns=['PREDICTED_CLOSE'])
    future_data['DATE'] = future_dates

    # Plot the results for Actual, Predicted, and Percentage Error, including Future Predictions
    fig = make_subplots(rows=4, cols=1, subplot_titles=(
    "Actual vs Predicted VIX", "Predicted VIX", "Percentage Error", "Future Predictions"))

    # Plot combined actual and predicted VIX
    fig.add_trace(go.Scatter(x=predicted_data['DATE'], y=predicted_data['ACTUAL_CLOSE_SMOOTHED'], mode='lines',
                             name='Actual VIX (Smoothed)', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=predicted_data['DATE'], y=predicted_data['PREDICTED_CLOSE_SMOOTHED'], mode='lines',
                             name='Smoothed Predicted VIX', line=dict(color='red', dash='dash')), row=1, col=1)

    # Plot only predicted VIX
    fig.add_trace(go.Scatter(x=predicted_data['DATE'], y=predicted_data['PREDICTED_CLOSE_SMOOTHED'], mode='lines',
                             name='Smoothed Predicted VIX', line=dict(color='red', dash='dash')), row=2, col=1)

    # Plot smoothed percentage error
    fig.add_trace(go.Scatter(x=predicted_data['DATE'], y=predicted_data['PERCENTAGE_ERROR_SMOOTHED'], mode='lines',
                             name='Smoothed Percentage Error', line=dict(color='green', dash='dot')), row=3, col=1)

    # Plot future predictions for the next 100 days
    fig.add_trace(
        go.Scatter(x=future_data['DATE'], y=future_data['PREDICTED_CLOSE'], mode='lines', name='Future Predicted VIX',
                   line=dict(color='orange', dash='dot')), row=4, col=1)

    # Update layout
    fig.update_layout(
        title='VIX Prediction with Smoothed Values, Percentage Error Below 20%, and Future Predictions',
        xaxis_title='Date',
        yaxis_title='Price',
        showlegend=True,
        height=1200,
        template='plotly_dark',
        hovermode='x unified',
        dragmode='zoom'
    )

    fig.show()
