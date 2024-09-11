import smtplib
from email.mime.text import MIMEText
import os


class SendEmail:
    def __init__(self):
        self.sender_email = "livedb.free@gmail.com"
        self.key_file_path = "./key.key"

    def send_email(self, receiver_email, user_code):
        # Read the app code from the key file
        try:
            with open(self.key_file_path, "r") as f:
                app_code = f.read().strip()
        except FileNotFoundError:
            print(f"Key file not found.")
            return False
        except Exception as e:
            print(f"Error reading app code from file: {e}")
            return False

        # Construct the email content with the app code
        subject = "Livedb: Your Unique User Code"
        body = f"The unique user code is: {user_code}. \nThe data stored will only be valid for 72 Hours"

        # Create the email message
        message = MIMEText(body)
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Send the email
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, app_code)
                server.sendmail(self.sender_email, receiver_email, message.as_string())
                return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False


if __name__ == "__main__":
    receiver_email = "mpjunaid96@gmail.com"
    user_code = "123456"
    email_sender = SendEmail()
    if email_sender.send_email(receiver_email, user_code):
        print("Email sent successfully!")
    else:
        print("Error sending email.")
