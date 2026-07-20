import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import pandas as pd

OUTLOOK_EMAIL = "you@yourcompany.com"   # your Outlook address
OUTLOOK_PASSWORD = "your_password_here" # use an App Password if MFA is on

df = pd.read_csv("investors.csv")

with smtplib.SMTP("smtp.office365.com", 587) as server:
    server.starttls()
    server.login(OUTLOOK_EMAIL, OUTLOOK_PASSWORD)

    for _, row in df.iterrows():
        msg = MIMEMultipart()
        msg["From"] = OUTLOOK_EMAIL
        msg["To"] = row["email"]
        msg["Subject"] = f"Deal memo - {row['name']}"

        body = f"Dear {row['name']},\n\nPlease find attached the deal memo prepared for you.\n\nBest regards"
        msg.attach(MIMEText(body, "plain"))

        with open(row["pdf_path"], "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={row['name']}_memo.pdf")
            msg.attach(part)

        server.sendmail(OUTLOOK_EMAIL, row["email"], msg.as_string())
        print(f"Sent to {row['name']} ({row['email']})")

print("Done.")

# To run it:
# pip install pandas
# python3 ~/send_emails.py
