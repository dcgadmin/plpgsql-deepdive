
import streamlit as st
import pandas as pd
from tests import run_all_tests


results = run_all_tests()

rows = [
    {"challenges": name, "status": "✅" if data["status"] else "❌"}
    for name, data in results.items()
]
df = pd.DataFrame(rows)

st.markdown("### Task checklist")
st.dataframe(df, use_container_width=True, hide_index=True)

