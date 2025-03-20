import streamlit as st
import pandas as pd
import math

# Ensure we have a valid fundraiser name in session_state.
# If not, redirect the user to the settings page.
if "name" not in st.session_state or not st.session_state["name"]:
    st.warning("No fundraiser name set. Please configure it in the settings page.")
    st.switch_page("pages/settings.py")

# Retrieve the fundraiser name and items.
name = st.session_state["name"]
items = st.session_state[name]["items"]  # This should be a list of dicts: [ { "item_name": ..., "price": ..., "quantity": ... }, ...]
total_cost = st.session_state["fundraiser_cost"]
revenue = st.session_state["fundraiser_revenue"]

st.title(f"📊{name}")

# Use the items to create a list of item names.
item_cols = [item["item_name"] for item in items]

base_cols = ["Date", "Customer #"]
extra_cols = ["Price Adjustments", "Payment Method", "Total", "Notes"]
all_cols = base_cols + item_cols + extra_cols

# Use a DataFrame in session_state to store your spreadsheet data.
# If "orders_data" doesn't exist OR its columns don't match (in case items have changed),
# we create a fresh DataFrame with the current column set.
if ("orders_data" not in st.session_state or list(st.session_state["orders_data"].columns) != all_cols):
    st.session_state["orders_data"] = pd.DataFrame(columns=all_cols)

st.subheader("Orders Spreadsheet")

# Use st.data_editor (Streamlit ≥1.22) to provide an editable spreadsheet-like UI.
# Note: If you're on older Streamlit, you may need st.experimental_data_editor instead.
edited_df = st.data_editor(
    st.session_state["orders_data"],
    num_rows="dynamic",  # Allows adding new rows
)

if st.button("Save Changes"):
    st.session_state["orders_data"] = edited_df
    st.success("Orders updated successfully!")

# Inventory Tracker

st.subheader("Inventory")
num_cols = 2
num_rows = math.ceil(len(items) / num_cols)

for i in range(num_rows):
    row_items = items[i*num_cols : i*num_cols + num_cols]
    cols = st.columns(len(row_items))
    for col, item in zip(cols, row_items):
        col.metric(
            label=item["item_name"],
            value=item["quantity"],
            border=True
        )

# Financials
st.subheader("Financials ($)")
total_cost_col, revenue_col = st.columns(2)
total_cost_col.metric(label="Total Cost", value=total_cost)
delta = (revenue/total_cost)* 100
revenue_col.metric(label="Revenue", value=revenue, delta=f"{delta}%")