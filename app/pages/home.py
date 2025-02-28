import streamlit as st
import time
from executor import get_default_data, booking_details_chart

st.title("PostgreSQL Excercise")
simulation = st.toggle("Simulation")

booking_chart_placeholder = st.empty()  
booking_placeholder = st.empty()
facility_placeholder = st.empty()

def display_simulation_data():
    data = get_default_data()
    if data is not None:
        booking_details_df, facility_details_df = data

        with booking_chart_placeholder:
            st.write("Booking Details")
            booking_details_chart(booking_details_df)  

        with booking_placeholder:
            st.dataframe(booking_details_df, use_container_width=True, hide_index=True)

        with facility_placeholder:
            st.write("Facility Details")
            st.dataframe(facility_details_df, use_container_width=True, hide_index=True)


if simulation:
    while True:
        display_simulation_data()
        time.sleep(5) 
else:
    display_simulation_data()
