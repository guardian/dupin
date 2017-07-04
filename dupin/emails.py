import smtplib
from email.mime.text import MIMEText

from utils import printerr


def send_email_properly(contents, to_addr, from_addr, host, username, password):
    msg = MIMEText(contents, "plain")
    msg['Subject'] = "Dupin notification"
    msg['From'] = from_addr
    msg['To'] = to_addr

    s = smtplib.SMTP(host)
    s.starttls()
    if username is not None and password is not None:
        s.login(username, password)
    s.sendmail(from_addr, [to_addr], msg.as_string())
    s.quit()
    return

def send_email_quick(contents, to_addr):
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail("dupin@example.com", [to_addr], contents)
    except smtplib.SMTPException as err:
        printerr("Error: unable to send email, try configuring an SMTP server")
        raise err
