import streamlit as st
from executor import get_individual_bookings

name = st.text_input("Member Name(firstname or surname) Column", placeholder="Enter firstname or surname column name").strip()
surname = st.text_input("Input Name ", placeholder="Enter name to search").strip()

if st.button("Search Bookings"):
    details = get_individual_bookings(name, surname)
    if isinstance(details, str):
        st.error(details)
    else:
        st.dataframe(details, use_container_width=True, hide_index=True)
            
