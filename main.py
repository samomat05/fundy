import streamlit as st

settings = st.Page("pages\\settings.py", title="Settings", icon="⚙️")
table_view = st.Page("pages\\statistics.py", title="Statistics", icon="📊")
add_order = st.Page("pages\\add_order.py", title="Add Order", icon="💲")

pg = st.navigation([settings, table_view, add_order])
pg.run()