import streamlit as st
import requests

operation = st.segmented_control("", ["new wifi", "search", "get wifis", "downvote"])
if operation:
    if operation == "new wifi":
        name = st.text_input("name")
        password = st.text_input("password")
        if name and password:
            new_wifi_entry_url = f"http://127.0.0.1:5000/new-entry?name={name}&password={password}"
            response = requests.post(new_wifi_entry_url)
            if response.status_code == 200 or response.status_code == 201:
                st.write(f"✅ wifi successfully created")
            else:
                st.write(f"❌ error in creating wifi ----- status code = {response.status_code}")
    
    if operation == "search":
        name = st.text_input("name")

        if name:
            is_in_url = f"http://127.0.0.1:5000/is-in?name={name}"
            is_in_response = requests.get(is_in_url)
            if is_in_response.status_code == 400:
                st.write("❌ invalid name - no wifi found")
            elif is_in_response.status_code == 200:

                search_url = f"http://127.0.0.1:5000/search?name={name}"
                response = requests.get(search_url)

                if response.status_code == 200:
                    st.write("password ----> " + response.json()[0]["password"])
                    st.write("id ----> " + str(response.json()[0]["id"]))
                    st.write("downvotes ----> " + str(response.json()[0]["downvotes"]))
    
    if operation == "get wifis":
        get_all_wifis_url = " http://127.0.0.1:5000/get-wifis"
        response = requests.get(get_all_wifis_url)
        st.write(response.json())
    if operation == "downvote":
        id = st.text_input("id")
        if id:
            downvote_url = f"http://127.0.0.1:5000/downvote?id={id}"
            response = requests.post(downvote_url)
        
            if response.status_code == 400:
                st.write("❌ invalid id")

            elif response.status_code == 204:
                st.write("✅ wifi deleted due to high number of downvotes")
            elif response.status_code == 200:
                st.write("✅ wifi downvoted")
            
        

