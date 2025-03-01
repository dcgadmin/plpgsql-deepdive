import streamlit as st
from executor import get_facilities_list, get_facility_booking_summary



facilities_list = get_facilities_list()
st.write(f"Try different alternatives in database to return same results")
if facilities_list is not None:
    selected_facility = st.selectbox("Select facility:", facilities_list, index=None, placeholder="Select facility name...")
    if selected_facility is not None:
        result  = get_facility_booking_summary(selected_facility)
        if isinstance(result, str):
            st.error(result)
        else:
            booking_summary_df1, booking_summary_df2 = result
            st.write(f"Booking summary for : {selected_facility}")
            st.dataframe(booking_summary_df1, use_container_width=True, hide_index=True)
            st.dataframe(booking_summary_df2, use_container_width=True, hide_index=True)
else:
    st.write("No data for facilities list")

