import smtplib
import time
import random
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email( sender_email, receiver_emails, subject, body, attachment_paths,
                                smtp_server, smtp_port, smtp_username, smtp_password):
    # Ensure receiver_emails is a list
    if isinstance(receiver_emails, str):
        receiver_emails = receiver_emails.split(", ")

    # Create the email header
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, 'plain'))

    # Attach multiple files
    for path in attachment_paths:
        if os.path.exists(path):
            with open(path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(path)}'
                )
                msg.attach(part)
        else:
            print(f"Attachment path '{path}' does not exist.")
            return

    # Send the email
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_emails, msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")



def process_applications(data):
    item = 1

    for d in data:
        print(item)
        if item == 80:
            time.sleep(180)
            item =0
        sender_email = "abdellahgram01@gmail.com"
        receiver_email = "abdolahwidadi00@gmail.com" #[d['Email']]
        subject = d['Subject']
       
        # Load the email template from file
        email_template = d['Email_template']
        with open(email_template, "r", encoding="utf-8") as f:
            template = f.read()
        # Format template with your dictionary values
        body = template.format(JOB_TITLE=d['Job_title'] ,LOCATION=d['Location'] , COMPANY_NAME=d['job_poster'] )
        
        
        # Load the resume (CV)
        resume_path = d['Resume_path']
        # Load the resume (CV)
        cover_letter_path = d['Cover_letter']
        attachment_paths = [resume_path , cover_letter_path]
        smtp_server = "smtp.gmail.com"
        smtp_port = 465  # or 587 for STARTTLS
        smtp_username = "abdellahgram01@gmail.com"
        smtp_password = "qwtm umzh waai whoo"
        send_email(sender_email, receiver_email, subject, body, attachment_paths, smtp_server, smtp_port, smtp_username, smtp_password)
        item =item+1
        # Random number of minutes between 3 and 18
        minutes = random.randint(3, 10)
        seconds = minutes * 60
        
        print(f"Sleeping for {minutes} minutes...")
        time.sleep(seconds)
    



def test_outlook_email(sender_email, receiver_email, app_password):
    """
    Send a test email via Outlook SMTP using an App Password.
    """
    smtp_server = "smtp.office365.com"
    smtp_port = 587  # TLS port

    try:
        # Create the email
        msg = MIMEText("This is a test email sent via Outlook SMTP using Python.")
        msg['Subject'] = "Outlook SMTP Test"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # Connect to Outlook SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade to secure connection
        server.login(sender_email, app_password)  # Use App Password
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("✅ Test email sent successfully!")

    except Exception as e:
        print("❌ Failed to send test email:", str(e))
