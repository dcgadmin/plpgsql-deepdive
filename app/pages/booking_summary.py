import streamlit as st
from executor import get_facilities_list, get_facility_booking_summary

st.markdown("""
    <style>
    .tooltip {
      position: relative;
      display: inline-block;
      cursor: pointer;
      font-size: 18px;
      background: linear-gradient(135deg, #20c997, #6f42c1);
      color: white;
      border-radius: 50%;
      width: 32px;
      height: 32px;
      text-align: center;
      line-height: 32px;
      font-weight: bold;
      margin-bottom: 10px;
      margin-left: 680px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.2);
      transition: all 0.3s ease;
    }

    .tooltip:hover {
      transform: scale(1.1);
      box-shadow: 0 6px 16px rgba(0,0,0,0.3);
    }

    /* Hidden tooltip text */
    .tooltip .tooltiptext {
      visibility: hidden;
      max-height: 0;
            margin-left: 203px;
      overflow: hidden;
      width: 380px;
      background: #212529;
      color: #f8f9fa;
      text-align: left;
      padding: 0 12px;
      border-radius: 8px;
      position: absolute;
      z-index: 1;
      left: 50%;
      transform: translateX(-50%);
      opacity: 0;
      transition: max-height 0.4s ease, opacity 0.4s ease, padding 0.3s ease;
      font-size: 14px;
      line-height: 1.4;
      box-shadow: 0 4px 12px rgba(0,0,0,0.4);
      margin-top: 8px;
    }

    /* Show on hover with expand effect */
    .tooltip:hover .tooltiptext {
      visibility: visible;
      opacity: 1;
      max-height: 300px;
      padding: 12px;
    }
    </style>

    <div class="tooltip">
      i
      <div class="tooltiptext">
        ✅ 💡 HINT: PostgreSQL is case-sensitive. Check if the column is created as surname or "Surname", and use the same everywhere.  
            - 💡 Using concat_ws() glues values together. Add a space in concat_ws and keep only one RETURN QUERY in the function.
      </div>
    </div>
""", unsafe_allow_html=True)


st.info("""## 🏆 Challenges  
- This query failed because PostgreSQL could not find the column due to case-sensitivity and because string concatenation glued names and dates together, causing syntax issues

""")

facilities_list = get_facilities_list()
st.write(f"Try different alternatives in database to return multiple results - dbcode (get_facility_booking_summary)")
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

