from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

class NewNetwork(BaseModel):
    name:str
    ssid:str
    password:str

@app.get("/wifi")

def get_all_wifis():
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM wifi_entries ORDER BY created_at DESC;")
    all_networks = cursor.fetchall() 
    cursor.close()
    connection.close()
    return all_networks

@app.post("/wifi")

def add_wifi(network:NewNetwork):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO wifi_entries (name, ssid, password) VALUES (%s, %s, %s)",
        (network.name, network.ssid, network.password)
    )
    connection.commit()
    id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {
        "id":id,
        "name":network.name,
        "ssid":network.ssid,
        "password":network.password,
        "downvotes":0,
        "isNew":True,
    }

@app.post("/wifi/{network_id}/downvote")

def downvote_wifi(network_id : int):
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT downvotes FROM wifi_entries WHERE id = %s", (network_id,))
    downvote_row = cursor.fetchone()
    if not downvote_row:
        raise HTTPException(status_code=404, detail="Network Not Found")
    downvotes = downvote_row["downvotes"] + 1

    if downvotes >= 6:
        cursor.execute("DELETE FROM wifi_entries WHERE id = %s", (network_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return {"deleted":True, "id":network_id}
    else:
        cursor.execute("UPDATE wifi_entries SET downvotes = %s WHERE id = %s", (downvotes, network_id))
        connection.commit()
        cursor.close()
        connection.close()
        return {"deleted":False, "id":network_id}
    