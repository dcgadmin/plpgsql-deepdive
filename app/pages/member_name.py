import streamlit as st
from executor import get_member_name



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
        ✅ 💡 HINT: use SQL to optimize where applicable.
      </div>
    </div>
""", unsafe_allow_html=True)


st.info("""## 🏆 Challenges- 
- Consider these challenges as performance tuning exercises and provide a review suggesting possible

""")

st.write("SQL Running in Database - with alias1 as NOT MATERIALIZED (select get_member_name(mod(generate_series,50)) from generate_series(1,%s)) select count(1) from alias1;")
limit = st.number_input("Enter a limit (Max: 1000000)", min_value=1, max_value=1000000, value=500000, step=1)
if limit:
    if limit <= 1000000:
        if st.button("Member names", type="primary"):
            execution_time = get_member_name(limit)
            if execution_time is not None:
                st.write(f"Time required for execution of get member name is : {execution_time} seconds")
