import streamlit as st
from executor import get_discounts,get_members_list

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
        ✅  HINT: EXECUTE alone does not set FOUND. You need another way — maybe capturing ROW_COUNT with GET DIAGNOSTICS  💡You can build the interval dynamically (like '6 month'::interval) using string concatenation inside EXECUTE.
      </div>
    </div>
""", unsafe_allow_html=True)


st.info("""## 🏆 Challenges- Dynamic Function Debug & Reuse
- Fix the function so it really detects whether the query returned rows.
- Rewrite the function so the interval is passed as a parameter, and the user can call it with 6, 12, or 24 months.
""")


member_mapping, members_list = get_members_list()
if members_list is not None:
    selected_member = st.selectbox("Select Member:", members_list, index=None, placeholder="Select member name...")
    if selected_member is not None:
        data = get_discounts(selected_member)
        bool_cols = data.select_dtypes(include=[bool]).columns
        data[bool_cols] = data[bool_cols].replace({True: "✅", False: "❌"})
        st.write(f"Discount Applicability for Member : {selected_member}")
        st.dataframe(data, use_container_width=True, hide_index=True)
