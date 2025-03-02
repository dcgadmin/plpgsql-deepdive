import streamlit as st
from datetime import datetime, date, time
from executor import get_facilities_list, get_members_list, get_create_booking


facilities_list = get_facilities_list()
if facilities_list:
    selected_facility = st.selectbox("Select facility:", facilities_list, index=None, placeholder="Select facility name...")

member_mapping, members_list = get_members_list()
if members_list:
    selected_member = st.selectbox("Select Member:", members_list, index=None, placeholder="Select member name...")


selected_date = st.date_input("Select Date", date.today())
selected_time = st.time_input("Select Time", time(), step=1800)
start_datetime = datetime.combine(selected_date, selected_time)
formatted_start_time = start_datetime.strftime("%Y-%m-%d %H:%M:%S")

st.write("Your Booking time will be:", formatted_start_time)

slots = st.number_input("Enter slots (Max: 5)", min_value=1, max_value=5, value=2, step=1)

if selected_facility is not None  and selected_member is not None:
    if st.button("Create", type="primary"):
        result = get_create_booking(selected_facility, selected_member, formatted_start_time, slots)
        if isinstance(result, str):
            st.error(result)
        else:
            st.dataframe(result, use_container_width=True, hide_index=True)
