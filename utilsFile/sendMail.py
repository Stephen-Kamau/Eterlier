from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_email(subject,email_address,messageToSend):
    msg = MIMEMultipart()
    message = messageToSend
    # user_id = ''
    # msg['From'] = "stiveckamash@gmail.com"
    user_id = ''
    msg['From'] = "stephenkamau714@gmail.com"
    msg['To'] = email_address
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.ehlo()
        server.login(msg['From'], user_id)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print('yes')
    except Exception as e:
        print(e)


# send_email("hi" , 'stiveckamash@gmail.com' , "heloooo")
