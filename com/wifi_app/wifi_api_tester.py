import streamlit as st
import requests
import time

operation = st.segmented_control("", ["new wifi", "search", "get wifis", "downvote"])
if operation:
    if operation == "new wifi":
        name = st.text_input("name")
        password = st.text_input("password")
        if name and password:
            new_wifi_entry_url = f"http://127.0.0.1:5000/new-entry?name={name}&password={password}"
            response = requests.post(new_wifi_entry_url)
            time.sleep(1.5)
            if response.status_code == 200 or response.status_code == 201:
                st.write(f"✅ wifi successfully created")
            else:
                st.write(f"❌ error in creating wifi")
    
    if operation == "search":
        name = st.text_input("name")

        if name:
            
            search_url = f"http://127.0.0.1:5000/search?name={name}"
            response = requests.get(search_url)

            if response.status_code == 200:
                st.write(response.json()[0]["password"])
        

