import streamlit as st
import pandas as pd
import datetime

# Ensure we have a valid fundraiser name in session_state.
if "name" not in st.session_state or not st.session_state["name"]:
    st.warning("No fundraiser name set. Please configure it in the settings page.")
    st.switch_page("pages\\settings.py")

if "order_count" not in st.session_state:
    st.session_state["order_count"] = 0

name = st.session_state["name"]
items = st.session_state[name]["items"]

st.title(f"💲{name}")

# Define the columns for the spreadsheet
base_cols = ["Date", "Customer #"]
item_cols = [it["item_name"] for it in items]
extra_cols = ["Price Adjustments", "Payment Method", "Total", "Notes"]
all_cols = base_cols + item_cols + extra_cols

if (
    "orders_data" not in st.session_state
    or not isinstance(st.session_state["orders_data"], pd.DataFrame)
    or list(st.session_state["orders_data"].columns) != all_cols
):
    st.session_state["orders_data"] = pd.DataFrame(columns=all_cols)

# This callback re-calculates the total on changes outside the form
def update_total_due():
    total = 0
    for it in items:
        q = st.session_state.get(f"quantity_{it['item_name']}", 0)
        price = it["price"]
        total += q * price
    st.session_state["dynamic_total_due"] = total
    return total

st.write("## Add a new order ")
for it in items:
    q_key = f"quantity_{it['item_name']}"
    if q_key not in st.session_state:
        st.session_state[q_key] = 0
    st.number_input(
        f"Quantity for {it['item_name']}",
        key=q_key,
        min_value=0,
        step=1,
        on_change=update_total_due,
        max_value= it["quantity"],
    )

# The form collects the rest of the inputs
with st.form("add_order_form", clear_on_submit=True):
    price_adjust = st.number_input("Price Adjustments:", key="price_adjust_field")
    payment_method = st.radio("Payment Method:", ["Venmo", "Cash", "Zelle"], key="payment_method_field")
    notes = st.text_input("Notes:", key="notes_field")
    submitted = st.form_submit_button("Add Order")

    if submitted:
        st.session_state["order_count"] += 1
        order_num = st.session_state["order_count"]
        new_order = {
            "Date": datetime.date.today().strftime("%m/%d/%y"),
            "Customer #": order_num,
            "Price Adjustments": price_adjust,
            "Payment Method": payment_method,
            "Total": update_total_due(),
            "Notes": notes,
        }
        
        for it in items:
            item_name = it["item_name"]
            q_val = st.session_state.get(f"quantity_{item_name}", 0)
            new_order[item_name] = q_val
            it["quantity"] -= q_val

        df_orders = st.session_state["orders_data"]
        new_row_df = pd.DataFrame([new_order], columns=all_cols)
        st.session_state["orders_data"] = pd.concat([df_orders, new_row_df], ignore_index=True)
        st.session_state["fundraiser_revenue"] = st.session_state["fundraiser_revenue"] + new_order["Total"]
        st.success("Order has been added and stored!")

total_due = st.session_state.get("dynamic_total_due", 0)
st.write(f"Total Due: ${total_due:.2f}")
