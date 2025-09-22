import streamlit as st
from executor import get_all_facilities


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
        ✅ HINT: The FOR loop automatically handles OPEN, FETCH, and CLOSE. 💡 Use the last value stored in the loop, then add it once after the loop finishes.
      </div>
    </div>
""", unsafe_allow_html=True)


st.info("""## 🏆 Challenges- Cursor Simplification & Final Value
- Rewrite the function to remove manual cursor operations and use the cleaner FOR ... IN CURSOR style.
- Make sure the function always appends “Last Facility – <name>” at the very end of the result set.

""")


limit = st.number_input("Enter Rows (Max: 10)", min_value=1, max_value=10, value=5, step=1)
if limit:
    if st.button("Search", type="primary"):
        data = get_all_facilities(limit)
        st.dataframe(data, use_container_width=True, hide_index=True)

