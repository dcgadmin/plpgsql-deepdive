import streamlit as st
import pandas as pd
from executor import get_test_case_status

results = get_test_case_status()

rows = [
    {"challenges": name, "status": "✅" if data["status"] else "❌"}
    for name, data in results.items()
]
df = pd.DataFrame(rows)

st.markdown("### Task checklist")
st.dataframe(df, use_container_width=True, hide_index=True)

