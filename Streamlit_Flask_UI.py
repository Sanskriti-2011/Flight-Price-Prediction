import streamlit as st
import requests

st.title("Flight & Hotel Price Prediction")
st.write("Enter travel details to predict the expected price.")

# User Inputs
days_until_travel = st.number_input("Days Until Travel", min_value=1, max_value=180, value=30)
previous_booking_count = st.number_input("Previous Booking Count", min_value=0, max_value=20, value=2)
journey_month = st.selectbox("Journey Month", list(range(1, 13)), index=5)
season = st.selectbox("Season", ["Winter", "Spring", "Summer", "Autumn"])
flight_class = st.selectbox("Flight Class", ["Economy", "Business", "First Class"])
room_type = st.selectbox("Room Type", ["Standard", "Deluxe", "Suite"])
payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card", "UPI", "PayPal"])
gender = st.selectbox("Gender", ["Male", "Female"])
booking_source = st.selectbox("Booking Source", ["Website", "Travel Agent", "Walk-in"])
avg_ticket_price = st.number_input("Average Ticket Price (Last 30 Days)", min_value=100, max_value=2000, value=500)
avg_hotel_price = st.number_input("Average Hotel Price (Last 30 Days)", min_value=50, max_value=1000, value=200)

# Prepare input data
input_data = {
    'days_until_travel': days_until_travel,
    'previous_booking_count': previous_booking_count,
    'journey_month': journey_month,
    'season': season,
    'flight_class': flight_class,
    'room_type': room_type,
    'payment_method': payment_method,
    'gender': gender,
    'booking_source': booking_source,
    'average_ticket_price_last_30_days': avg_ticket_price,
    'average_hotel_price_last_30_days': avg_hotel_price
}

# Predict button
if st.button("Predict Price"):
    response = requests.post("http://127.0.0.1:5000/predict", json=input_data)
    if response.status_code == 200:
        prediction = response.json().get("predicted_price", "Error")
        st.success(f"Predicted Ticket Price: ${prediction:.2f}")
    else:
        st.error("Failed to get prediction from server")
