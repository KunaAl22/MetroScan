import pymongo
from datetime import datetime
from fetchdata import fetch
from keys import sendgridKey, mongoKey
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

client = pymongo.MongoClient(mongoKey)
db = client['test']
collection = db['userdata']

while 1:

    username = fetch()
    location = "Hazratganj Metro INC"
    now = datetime.now()

    if username == "Unknown":
        print("No matches found")

    else:
        new_balance = 0
        print("face detected successfully\n")
        data = collection.find_one({"username": username})
        if data['entry location'] == "Charbagh Metro INC" and location == "Hazratganj Metro INC":
            new_balance = data['balance']+20

        result = collection.update_one(
            {"username": username},
            {"$set": {"exit location": location, "exit time": now, "balance": new_balance}}
        )

        if result.modified_count > 0:
            print("Record updated successfully.")
        else:
            print("No matching records found.")

        print(f"Username: {data['username']}\nEmail: {data['email id']}\nPhone: {data['phone number']}\n"
              f"out_time:{data['exit time']}\nout_location:{data['exit location']}\nbalance: {new_balance}")

        my_sg = sendgrid.SendGridAPIClient(sendgridKey)

        # Change to your verified sender
        from_email = Email("pritish.kr3@gmail.com")

        # Change to your recipient
        emailvar = data['email id']
        to_email = To(emailvar)

        subject = "De-Boarding Notification"
        content = Content("text/plain",
                          f"You have De-boarded the LUCKNOW METRO Corp. from {data['exit location']} at time: {data['exit time']}"
                          f"\n"
                          f"Your balance due is: {new_balance}")

        mail = Mail(from_email, to_email, subject, content)

        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()

        # Send an HTTP POST request to /mail/send
        response = my_sg.client.mail.send.post(request_body=mail_json)

        print("De-Boarding Email sent successfully")