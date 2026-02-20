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
alg = r"C:\Workspaces\python-play\com\haarcascade_frontalface_default.xml"
haar_cascade = cv2.CascadeClassifier(alg)


file_name = r"C:\Workspaces\python-play\com\harry potter cast.webp"


img = cv2.imread(file_name)


if img is None:
    print(f"Error: Could not load image at {file_name}. Check the path/extension!")
else:
   
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    faces = haar_cascade.detectMultiScale(gray_img, scaleFactor=1.2, minNeighbors=8, minSize=(100,100))

    if not os.path.exists("stored-faces"):
        os.makedirs("stored-faces")

    for i, (x, y, w, h) in enumerate(faces):
        cropped_image = img[y:y + h, x:x + w]
        target_file_name = f"stored-faces/{i}.jpg"
        cv2.imwrite(target_file_name, cropped_image)
        print(f"Saved face {i} to {target_file_name}")