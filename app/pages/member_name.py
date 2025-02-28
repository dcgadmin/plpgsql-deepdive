import streamlit as st
from executor import get_member_name

limit = st.number_input("Enter a limit (Max: 500000)", min_value=1, max_value=500000, value=500000, step=1)
if limit:
    if limit <= 500000:
        if st.button("Member names", type="primary"):
            execution_time = get_member_name(limit)
            if execution_time is not None:
                st.write(f"Time required for execution of get member name is : {execution_time} seconds")