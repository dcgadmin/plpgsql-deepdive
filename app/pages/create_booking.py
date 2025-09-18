import streamlit as st
from datetime import datetime, date, time
from executor import get_facilities_list, get_members_list, get_create_booking



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
        ✅  HINT:Remove COMMIT and ROLLBACK from the procedure. PostgreSQL will manage transactions automatically — just use EXCEPTION blocks for error handling.
          💡 Instead of converting starttime with to_char, insert it directly as a timestamp.
      </div>
    </div>
""", unsafe_allow_html=True)


st.info("""## 🏆 Challenges
- This query failed because COMMIT and ROLLBACK are placed inside the procedure. In PL/pgSQL, explicit transaction control (commit/rollback) is not allowed inside functions/procedures triggered by SQL.
- to_char(starttime,'DD-MON-YYYY HH24:MI')::timestamp is converting a timestamp into text
""")


facilities_list = get_facilities_list()
if facilities_list:
    selected_facility = st.selectbox("Select facility:", facilities_list, index=None, placeholder="Select facility name...")

member_mapping, members_list = get_members_list()
if members_list:
    selected_member = st.selectbox("Select Member:", members_list, index=None, placeholder="Select member name...")


selected_date = st.date_input("Select Date", date.today())
selected_time = st.time_input("Select Time", time(), step=1800)
start_datetime = datetime.combine(selected_date, selected_time)
formatted_start_time = start_datetime.strftime("%Y-%m-%d %H:%M:%S")

st.write("Your Booking time will be:", formatted_start_time)

slots = st.number_input("Enter slots (Max: 5)", min_value=1, max_value=5, value=2, step=1)

if selected_facility is not None  and selected_member is not None:
    if st.button("Create", type="primary"):
        result = get_create_booking(selected_facility, selected_member, formatted_start_time, slots)
        if isinstance(result, str):
            st.error(result)
        else:
            st.write("Booking is Confirm, :sunglasses:")
