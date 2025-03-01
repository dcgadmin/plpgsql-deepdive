import streamlit as st
from executor import get_individual_bookings

name = st.text_input("Column Name", placeholder="Enter column name").strip()
surname = st.text_input("Name", placeholder="Enter name").strip()

if st.button("Search Bookings"):
    details = get_individual_bookings(name, surname)
    if isinstance(details, str):
        st.error(details)
    else:
        st.dataframe(details, use_container_width=True, hide_index=True)
            
