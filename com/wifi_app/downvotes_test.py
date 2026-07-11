import mysql.connector

connection = mysql.connector.connect(
        host="localhost",
        user="eshanjha",
        password="ILovebooks!@#123",
        database="wifi_db",
        port=3306
    )

cursor = connection.cursor(dictionary=True)
name = input("name: ")
ssid = input("ssid: ")

cursor.execute("SELECT downvotes FROM wifi_entries WHERE name = %s AND ssid = %s;", (name, ssid))
downvotes_row = cursor.fetchone()
print(downvotes_row)