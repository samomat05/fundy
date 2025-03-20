import streamlit as st
import pandas as pd

st.title('⚙️Fundraiser Settings!')

# Ensure we have a initiated necessary variables in session_state.
if "name" not in st.session_state:
    st.session_state["name"] = ""
if "fundraiser_cost" not in st.session_state:
    st.session_state["fundraiser_cost"] = 0
if 'fundraiser_revenue' not in st.session_state:
    st.session_state["fundraiser_revenue"] = -st.session_state["fundraiser_cost"] 
name_input = st.text_input("Name:", value=st.session_state["name"])

# If the user changes the text input, update session_state["name"] accordingly.
if name_input != st.session_state["name"]:
    st.session_state["name"] = name_input
name = st.session_state["name"]

# Fundraiser cost input
fundraiser_cost_input = st.number_input("Fundraiser Cost:", value=st.session_state["fundraiser_cost"])

# Update cost if changed
if fundraiser_cost_input != st.session_state["fundraiser_cost"]:
    st.session_state["fundraiser_cost"] = fundraiser_cost_input
    st.session_state["fundraiser_revenue"] = -fundraiser_cost_input

# Creates the dict that we will use to store all values later.
if name not in st.session_state:
    st.session_state[name] = {}
    st.session_state[name]["items"] = []

# Callbacks/events
def add_item(item_name: str, price: float, quantity: int):
    st.session_state[name]["items"].append({"item_name": item_name, "price": price, "quantity": quantity})

def remove_item(index: int):
    if st.session_state[name]["items"] is not None:
        st.session_state[name]["items"].pop(index)

# Fundraiser Cost Input
if 'fundraiser_cost' not in st.session_state:
    fundraiser_cost = st.number_input("Fundraiser Cost:")
    st.session_state["fundraiser_cost"] = fundraiser_cost
    st.session_state["fundraiser_revenue"] = -st.session_state["fundraiser_cost"]

# Item Form
with st.form("add_item_form", clear_on_submit = True):
    st.write('## Add an item to the fundraiser')
    item_name = st.text_input('Item Name:', key='item_name_field')
    item_price = st.number_input('Price:', key='item_price_field')
    item_quantity = st.number_input('Quantity:', key='item_quantity_field')
    submitted = st.form_submit_button('Add Item')

    if submitted:
        add_item(item_name=item_name, price=float(item_price), quantity=int(item_quantity))

# Table for displaying items
items = st.session_state[name]["items"]
if items:
    st.write("## Items Table")

    # Table header
    header_cols = st.columns([3, 2, 2, 2])
    header_cols[0].write("Item Name")
    header_cols[1].write("Price")
    header_cols[2].write("Qty")
    header_cols[3].write("Action")

    # Item rows
    for i in (range(len(items))):
        item = items[i]
        row_cols = st.columns([3, 2, 2, 2])

        row_cols[0].write(item['item_name'])
        row_cols[1].write(item['price'])
        row_cols[2].write(item['quantity'])

        row_cols[3].button("Remove", key=f"remove_{i}", on_click=remove_item, args=(i,))