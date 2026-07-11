import streamlit as st
import requests
import time

operation = st.segmented_control("", ["new wifi", "search", "get wifis", "downvote"])
if operation:
    if operation == "new wifi":
        name = st.text_input("Name")
        password = st.text_input("Password")
        if name and password:
            new_wifi_entry_url = f"http://127.0.0.1:5000/new-entry?name={name}&password={password}"
            response = requests.post(new_wifi_entry_url)
            time.sleep(1.5)
            if response.status_code == 200 or response.status_code == 201:
                st.write(f"✅ wifi successfully created")
            else:
                st.write(f"❌ error in creating wifi")
        

