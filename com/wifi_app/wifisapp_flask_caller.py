import requests

operation_input = input('(n)ew wifi or (d)ownvote (type "help" for ssid, "quit" to quit)? ').lower()

if operation_input == "quit" or operation_input == "q":
    quit()

elif operation_input == "n" or operation_input == "new":
    wifi_name = input("wifi name: ")
    wifi_ssid = input("SSID: ")
    wifi_password = input("Password: ")

    new_wifi_request = requests.post(f"http://127.0.0.1:5000/new-wifi-entry?name={wifi_name}&ssid={wifi_ssid}&password={wifi_password}")
    print(new_wifi_request.status_code)

elif operation_input == "help" or operation_input == "h":
    wifi_name = input("Name of wifi: ")
    get_ssid_request = requests.get(f"http://127.0.0.1:5000/get-ssid?name={wifi_name}").json()
    print(get_ssid_request["status"])
    

elif operation_input == "d"or operation_input == "downvote":
    wifi_name = input("Name of wifi: ")
    wifi_ssid = input("SSID: ")
    remove_downvotes = requests.post(f"http://127.0.0.1:5000/downvote?name={wifi_name}&ssid={wifi_ssid}")
    print(remove_downvotes.status_code)