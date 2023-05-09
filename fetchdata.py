import cv2
import time
import pymongo
import numpy as np
import face_recognition
from keys import sendgridKey, mongoKey, mailID


def fetch():
    # Connect to MongoDB server
    client = pymongo.MongoClient(mongoKey)
    db = client['test']
    collection = db['userdata']

    # Load face encodings from database
    known_face_encodings = []
    known_face_names = []
    for data in collection.find():
        username = data["username"]
        image = np.asarray(bytearray(data["image"]), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(username)

    # Open camera window
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera", 960, 720)

    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        # Capture image from camera
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture image from camera.")
            break

        # Find faces in the image
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Initialize flag variable
        match_found = False

        # Loop through each face in the image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare face encoding with known faces in database
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            username = "Unknown"

            # Find best match face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                username = known_face_names[best_match_index]

                # Set flag to True and break out of loop if match is found
                match_found = True
                break

            # Draw face rectangle and name on the image
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, username, (left + 6, bottom - 6), font, 1.0, (0, 255, 0), 1)

        # Show the image
        cv2.imshow("Camera", frame)

        # Return the name if match is found
        if match_found:
            cam.release()
            cv2.destroyAllWindows()
            return username

        # Press 'q' to exit
        if cv2.waitKey(1) == ord("q"):
            break

    # Release camera and close window
    cam.release()
    cv2.destroyAllWindows()
