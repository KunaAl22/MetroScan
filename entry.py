import pymongo
from datetime import datetime
from fetchdata import fetch
from keys import sendgridKey, mongoKey, mailID

import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

client = pymongo.MongoClient(mongoKey)
db = client['test']
collection = db['userdata']

while 1:
    username = fetch()
    location = "Charbagh Metro INC"
    now = datetime.now()

    if username == "Unknown":
        print("No matches found")

    else:
        print("face detected successfully\n")
        result = collection.update_one(
            {"username": username},
            {"$set": {"entry location": location, "entry time": now}}
        )
        data = collection.find_one({"username": username})

        if result.modified_count > 0:
            print("Record updated successfully.")
        else:
            print("No matching records found.")

        print(f"Username: {data['username']}\nEmail: {data['email id']}\nPhone: {data['phone number']}\n"
              f"in_time:{data['entry time']}\nin_location:{data['entry location']}")

        my_sg = sendgrid.SendGridAPIClient(sendgridKey)

        # Change to your verified sender
        from_email = Email(mailID)

        # Change to your recipient
        emailvar = data['email id']
        to_email = To(emailvar)

        subject = "Boarding Notification"
        content = Content("text/plain", f"You have boarded to LUCKNOW METRO from {data['entry location']} at time: {data['entry time']}")

        mail = Mail(from_email, to_email, subject, content)

        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()

        # Send an HTTP POST request to /mail/send
        response = my_sg.client.mail.send.post(request_body=mail_json)

        print("Boarding Email sent successfully")