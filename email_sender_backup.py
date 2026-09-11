# # libraries import
# import smtplib
#
# # send mail put
# lists =['parikhdhruv05@gmail.com','parikhdhruv025@gmail.com']
#
# # connection in port no:-all Email same number in 587
# connection = smtplib.SMTP('smtp.gmail.com',587)
# connection.ehlo()
# connection.starttls()
#
# # connection in first your email id and send email password
# connection.login('parikhdhruv05@gmail.com','pniqhkgxgoqylvhi')
# # parikhdhruv05@gmail.com:= your Email put
# # pniqhkgxgoqylvhi := This password is Email password not.
# # step-1: open google account
# # step-2: Security selected
# # step-3: 2-Step Verification selected and completed step
# # step-4: search 'app password'
# # step-5: Select the app and device for which you want to generate the app password.
# # step-6: select app ('other') input('python')
# # step-7: Enter  Generate
#
# for i in lists:
#     connection.sendmail('parikhdhruv05@gmail.com', i ,'Subject:python \n\n Hello my name is Dhruv Parikh')
#
#     print(f"mail send Done {i}")
# connection.quit()
####################################################################################################################
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Email and password setup
email_sender = 'parikhdhruv05@gmail.com'
email_password = 'lkao mlwv hgle qvfr'  # App-specific password
email_recipients = ["hr@mindlyticai.com","himanshu@moverrotechno.in"]

# Path to the PDF file to be attached
pdf_path = r'C:\Users\Admin\Downloads\Sending-Emails-With-Python-main\Sending-Emails-With-Python-main\Dhruv_Resume.pdf'  # Replace with your PDF file path

# SMTP connection setup
connection = smtplib.SMTP('smtp.gmail.com', 587)
connection.ehlo()
connection.starttls()
connection.login(email_sender, email_password)

# Loop through each recipient
for recipient in email_recipients:
    # Create a MIME message
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = recipient
    msg['Subject'] = 'Application for Python Django Developer Position'

    # Email body
    body = '''Dear Hiring Manager,

I hope you are doing well. My name is Dhruv Parikh, and I am writing to let you know about my interest in the Python Django Developer position.I have attached my resume to this email for your review.

I have 3 years of experience in developing web applications using Python and Django, along with expertise in creating RESTful APIs, managing PostgreSQL databases, and integrating front-end technologies like HTML, CSS, and JavaScript. I am passionate about building efficient and scalable solutions and would be excited to contribute to your team.

Please let me know if you need any additional information or documents. I look forward to the opportunity to discuss how my skills and experience align with your requirements.

Thank you for your time and consideration.

Best regards,
Dhruv Parikh
+91 7600524348'''

    # Attach the body to the message
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF file
    try:
        with open(pdf_path, 'rb') as attachment:
            pdf_attachment = MIMEBase('application', 'octet-stream')
            pdf_attachment.set_payload(attachment.read())
        # Encode the payload
        encoders.encode_base64(pdf_attachment)
        # Add header with the filename
        pdf_attachment.add_header(
            'Content-Disposition',
            f'attachment; filename=Dhruv_Resume.pdf'
        )
        # Attach the PDF to the email
        msg.attach(pdf_attachment)

    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
        continue

    # Send the email
    connection.sendmail(email_sender, recipient, msg.as_string())
    print(f"Mail sent to {recipient}")

# Close the connection
connection.quit()
