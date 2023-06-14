import cv2
import time
import pymongo
import numpy as np
import face_recognition
from keys import sendgridKey, mongoKey, mailID

from datetime import datetime


client = pymongo.MongoClient(mongoKey)
db = client['test']
collection = db['userdata']

username = input("Enter your username: ")
email = input("Enter your email: ")
phone = input("Enter your phone number: ")
balance = 0
entry_location = "NA"
exit_location = "NA"
entry_time = "NA"
exit_time = "NA"



if collection.find_one({"username": username}):
    print("Error: username already exists in database.")
else:
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera", 960, 720)
    timer = 4
    font = cv2.FONT_HERSHEY_SIMPLEX
    while timer >= 0:
        ret, frame = cam.read()
        if ret:
            cv2.putText(frame, f"Capturing in {timer} seconds...", (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Camera", frame)
            cv2.waitKey(1000)
            timer -= 1
    ret, frame = cam.read()
    cam.release()
    cv2.destroyAllWindows()

    img_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
    data = {"username": username, "email id": email, "phone number": phone, "image": img_bytes,
            "balance": balance, "entry location": entry_location, "entry time": entry_time,
            "exit location": exit_location, "exit time": exit_time, }
    collection.insert_one(data)

    img_array = np.asarray(bytearray(img_bytes), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(img_rgb)
    if len(face_locations) > 0:
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.imshow("Face Detection", img)
        print("success!!  face detected in image.")

        cv2.waitKey(3000)
        cv2.destroyAllWindows()
    else:
        print("No faces detected in image.")
