from flask import Flask, request, jsonify
from flask_cors import CORS
import catboost as cb
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS to allow Streamlit to access Flask API

# Load the trained CatBoost model
MODEL_PATH = "C:\\Users\\Sanskriti\\optimized_catboost_model.cbm"
model = cb.CatBoostRegressor()
model.load_model(MODEL_PATH)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Convert input data into the correct format
        input_data = np.array([
            data['days_until_travel'],
            data['previous_booking_count'],
            data['journey_month'],
            1 if data['season'] == "Winter" else 2 if data['season'] == "Spring" else 3 if data['season'] == "Summer" else 4,
            1 if data['flight_class'] == "Economy" else 2 if data['flight_class'] == "Business" else 3,
            1 if data['room_type'] == "Standard" else 2 if data['room_type'] == "Deluxe" else 3,
            1 if data['payment_method'] == "Credit Card" else 2 if data['payment_method'] == "Debit Card" else 3 if data['payment_method'] == "UPI" else 4,
            1 if data['gender'] == "Male" else 2,
            1 if data['booking_source'] == "Website" else 2 if data['booking_source'] == "Travel Agent" else 3,
            data['average_ticket_price_last_30_days'],
            data['average_hotel_price_last_30_days']
        ]).reshape(1, -1)

        # Make prediction
        predicted_price = model.predict(input_data)[0]

        return jsonify({'predicted_price': float(predicted_price)})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
