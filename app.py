import requests
import streamlit as st
import random
import time
from datetime import datetime, timedelta
from params import TAXI_FARE_API_URL

# Streamlit UI
st.markdown(
    '''
    # 🚖 JP's Annoying New York Taxifare Predictor
    ## Super user-friendly interface.
    '''
)

## Define min/max datetime
start_time = datetime(2024, 4, 7)
end_time = datetime(2026, 1, 1)

# Persistent state for datetime
if "selected_datetime" not in st.session_state:
    st.session_state.selected_datetime = start_time

# 🎛 Layout: Datetime left, increase/decrease buttons stacked right
col1, col2 = st.columns([2, 1])
with col1:
    st.write(f"📅 **Selected Datetime:** {st.session_state.selected_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
with col2:
    if st.button("🔼 Increase Datetime"):
        st.session_state.selected_datetime += timedelta(hours=6,minutes=30)
        if st.session_state.selected_datetime > end_time:
            st.session_state.selected_datetime = end_time
        st.rerun()
    if st.button("🔽 Decrease Datetime"):
        st.session_state.selected_datetime -= timedelta(hours=6,minutes=30)
        if st.session_state.selected_datetime < start_time:
            st.session_state.selected_datetime = start_time
        st.rerun()

# 🎲 Pickup & Dropoff Coordinates as Sliders
st.write("### 🌍 Location Selection")
col1, col2 = st.columns(2)

# 🚕 Pickup Location (Slider)
with col1:
    st.write("🚕 **Pickup Location**")
    st.session_state.pickup_latitude = st.slider("📍 Latitude", 40.4774, 40.9176, 40.783282, step=0.0001)
    st.session_state.pickup_longitude = st.slider("📍 Longitude", -74.2591, -73.7004, -73.950655, step=0.0001)

# 🏁 Dropoff Location (Slider)
with col2:
    st.write("🏁 **Dropoff Location**")
    st.session_state.dropoff_latitude = st.slider("📍 Latitude", 40.4774, 40.9176, 40.769802, step=0.0001)
    st.session_state.dropoff_longitude = st.slider("📍 Longitude", -74.2591, -73.7004, -73.984365, step=0.0001)

# 👥 Centered Passenger Count Section
st.markdown("<h3 style='text-align: center;'>🎲 Passenger Count</h3>", unsafe_allow_html=True)

if "passenger_count" not in st.session_state:
    st.session_state.passenger_count = random.randint(1, 16)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.write(f"👥 **Passenger Count:** {st.session_state.passenger_count}")

# Centered Generate Passenger Count Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🎲 Generate Random Passenger Count"):
        st.session_state.passenger_count = random.randint(1, 7)
        st.rerun()

# 🔮 Perfectly Centered "Click here" Deceptive Text
st.markdown(
    "<h4 style='text-align: center;'> Click on the green button to restart your prediction.</h4>",
    unsafe_allow_html=True
)

# 🟢 Restart and 💰 Get Prediction Buttons Perfectly Centered Side by Side
col1, col2, col3 = st.columns([1, 2, 1])

# 🟢 FULL PAGE RELOAD ON RESTART
with col1:
    restart_button = st.button("🟢 Click Here")
    if restart_button:
        st.session_state.clear()
        st.rerun()  # 🚀 Forces a real app reload
with col3:
    if st.button("🔴 Enter"):
        payload = {
            "pickup_datetime": st.session_state.selected_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            "pickup_longitude": st.session_state.pickup_longitude,
            "pickup_latitude": st.session_state.pickup_latitude,
            "dropoff_longitude": st.session_state.dropoff_longitude,
            "dropoff_latitude": st.session_state.dropoff_latitude,
            "passenger_count": st.session_state.passenger_count
        }

        try:
            response = requests.post(TAXI_FARE_API_URL, json=payload)

            # Fake suspense effect
            st.write("🔮 *Consulting the Taxi Oracle...*")
            time.sleep(random.uniform(1, 3))

            if response.status_code == 200:
                fare = response.json().get("fare", "??")
                st.markdown(
                    f"<h2 style='text-align: center; color: lightgreen;'>💵 Predicted Fare: ${fare:.2f}</h2>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<h3 style='text-align: center; color: red;'>😵 Error: Something *mysterious* happened ({response.status_code}). Try again.</h3>",
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.markdown(
                f"<h3 style='text-align: center; color: red;'>⚠️ The universe has rejected your request. ({str(e)})</h3>",
                unsafe_allow_html=True
            )
