import requests

while True:

    operation = input("(N)ew Wifi, (G)et wifis, (D)ownvote or (S)earch? ").lower()

    if operation == "n" or operation == "new wifi":
        name = input("Name: ")
        password = input("Password: ")
        new_wifi_entry_url = f"http://127.0.0.1:5000/new-entry?name={name}&password={password}"
        response = requests.post(new_wifi_entry_url)
        print(response)
    elif operation == "g":
        get_all_wifis_url = " http://127.0.0.1:5000/get-wifis"
        response = requests.get(get_all_wifis_url)
        print(response)
    elif operation == "d":
        id = input("id: ")

        downvote_url = f"http://127.0.0.1:5000/downvote?id={id}"
        response = requests.post(downvote_url)
        print(response)
    elif operation == "s":
        name = input("name: ")
        search_url = f"http://127.0.0.1:5000/search?name={name}"
        response = requests.get(search_url)
        print(response)

   





