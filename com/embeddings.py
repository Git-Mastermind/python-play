import cv2
import os
import numpy as np
from imgbeddings import imgbeddings
from PIL import Image
import psycopg2



conn = psycopg2.connect("postgres://avnadmin:AVNS_BYdgCCV7eMhTLlgXBZv@pg-169561b0-eshanjha1234-facerecognitionschool.a.aivencloud.com:13734/defaultdb?sslmode=require")

for filename in os.listdir("stored-faces"):
    img = Image.open("stored-faces/" + filename)
    ibed = imgbeddings()
    embedding = ibed.to_embeddings(img)
    cur = conn.cursor()
    cur.execute("INSERT INTO pictures, values (%s, %s)", (filename, embedding[0].tolist()))
    print(filename)
conn.commit()