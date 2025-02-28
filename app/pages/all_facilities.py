import streamlit as st
from executor import get_all_facilities


limit = st.number_input("Enter Rows (Max: 50)", min_value=1, max_value=50, value=50, step=1)
if limit:
    if st.button("Search", type="primary"):
        data = get_all_facilities(limit)
        st.dataframe(data, use_container_width=True, hide_index=True)

