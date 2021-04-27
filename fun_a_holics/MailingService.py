import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# environment variables
username = 'cse546asuproject2@gmail.com'
password = 'cse546project2'

def send_mail(text='Email Body', subject='Hello World', from_email='Fun-A-Holics <cse546asuproject2@gmail.com>', to_emails=['teja.tejaswip@gmail.com'], html=None):
    assert isinstance(to_emails, list)

    msg=MIMEMultipart('alternative')
    msg['From']=from_email
    msg['To']=",".join(to_emails)
    msg['Subject']=subject
    
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)

    #html_part = MIMEText("<h1>This is working</h1>", 'html')
    #msg.attach(html_part)

    msg_str=msg.as_string()

    server=smtplib.SMTP(host='smtp.gmail.com',port=587)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(from_email,to_emails,msg_str)
    server.quit()


