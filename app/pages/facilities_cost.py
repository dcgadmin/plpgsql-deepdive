import streamlit as st
from executor import get_facilities_list, get_facilities_cost

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
        ✅ 💡 HINT: Use table aliases like f.membercost and f.facid to clearly show PostgreSQL that you mean the column, not the variable.
      </div>
    </div>
""", unsafe_allow_html=True)


st.info("""## 🏆 Challenges - Ambiguity
- This query failed because PostgreSQL found membercost ambiguous  it exists both as a column and as a PL/pgSQL variable.
- The condition where facid = facid always looks the same to PostgreSQL (variable vs column).

""")


facilities_list = get_facilities_list()
if facilities_list is not None:
    selected_facility = st.selectbox("Select facility:", facilities_list, index=None, placeholder="Select facility name...")
    if selected_facility is not None:
        booking_summary_df = get_facilities_cost(selected_facility)
        if booking_summary_df is not None:
            if isinstance(booking_summary_df, str):
                st.error(booking_summary_df)
            else:
                st.write(f"Booking summary for : {selected_facility}")
                st.dataframe(booking_summary_df, use_container_width=True, hide_index=True)
            
else:
    st.write("No data for facilities list")