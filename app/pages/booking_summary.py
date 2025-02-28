import streamlit as st
from executor import get_facilities_list, get_facility_booking_summary



facilities_list = get_facilities_list()
if facilities_list is not None:
    selected_facility = st.selectbox("Select facility:", facilities_list, index=None, placeholder="Select facility name...")
    if selected_facility is not None:
        booking_summary_df = get_facility_booking_summary(selected_facility)
        if booking_summary_df is not None:
            if isinstance(booking_summary_df, str):
                st.error(booking_summary_df)
            else:
                st.write(f"Booking summary for : {selected_facility}")
                st.dataframe(booking_summary_df, use_container_width=True, hide_index=True)
            
else:
    st.write("No data for facilities list")

