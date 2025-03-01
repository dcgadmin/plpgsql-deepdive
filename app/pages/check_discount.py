import streamlit as st
from executor import get_discounts,get_members_list


member_mapping, members_list = get_members_list()
if members_list is not None:
    selected_member = st.selectbox("Select Member:", members_list, index=None, placeholder="Select member name...")
    if selected_member is not None:
        data = get_discounts(selected_member)
        bool_cols = data.select_dtypes(include=[bool]).columns
        data[bool_cols] = data[bool_cols].replace({True: "✅", False: "❌"})
        st.write(f"Discount Applicability for Member : {selected_member}")
        st.dataframe(data, use_container_width=True, hide_index=True)
