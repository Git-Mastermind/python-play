import streamlit as st
import requests
import time

operation = st.radio("Choose an operation", ["new wifi", "get all wifis", "downvote a wifi", "search for a wifi"])

if operation == "new wifi":
    name = st.text_input("Name: ")
    password = st.text_input("Password: ")
    if name and password:
        new_wifi_entry_url = f"http://127.0.0.1:5000/new-entry?name={name}&password={password}"
        response = requests.post(new_wifi_entry_url)
        st.write("☝️ Fulfilling request...")
        time.sleep(0.7)
        st.write("Almost there...")
        time.sleep(0.5)
        st.write("✅ Success! Your wifi was added!")

if operation == "get all wifis":
    get_all_wifis_url = " http://127.0.0.1:5000/get-wifis"
    response = requests.get(get_all_wifis_url)
    data = response.json()
    parsed = [
        {   
            "id" : item["id"],
            "name" : item["name"],
            "password" : item["password"],
            "downvotes" : item["downvotes"]
        }
        for item in data
    ]
    for wifi in parsed:
        st.write(f"""
        NAME : {wifi['name']}
        PASSWORD : {wifi['password']}
        DOWNVOTES : {wifi['downvotes']} 
        ID : {wifi['id']}

""")

if operation == "downvote a wifi":
    id = st.text_input("id: ")

    if id:
    
        downvote_url = f"http://127.0.0.1:5000/downvote?id={id}"
        response = requests.post(downvote_url)

        st.write("Downvoting...")
        time.sleep(0.8)
        st.write("✅ Success!")

if operation == "search for a wifi":
    name = st.text_input("name: ")
    if name:
        search_url = f"http://127.0.0.1:5000/search?name={name}"
        response = requests.get(search_url)
        st.write(response)
    