import streamlit as st
from executor import get_member_name

limit = st.number_input("Enter a limit (Max: 1000000)", min_value=1, max_value=1000000, value=500000, step=1)
if limit:
    if limit <= 1000000:
        if st.button("Member names", type="primary"):
            execution_time = get_member_name(limit)
            if execution_time is not None:
                st.write(f"Time required for execution of get member name is : {execution_time} seconds")
