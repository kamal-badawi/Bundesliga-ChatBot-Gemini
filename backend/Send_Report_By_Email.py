# Diese Methode wurde schon im Masterprojekt verwendet und an diesem Fall angepasst
# Diese Methode wurde mit ChatGPT erstellt aber auch zu einem großen Teil angepasst
def run_send_report_by_mail(to_email, attachment, created_datetime_file_name, created_datetime_sending_time):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    from email.utils import formataddr
    from decouple import config

 
    from_email = config("FROM_EMAIL")
    smtp_password = config("FROM_EMAIL_PASSWORD")
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    body = f'''
       Liebe Kundin, lieber Kunde,<br><br><br>
       anbei übersenden wir Ihnen die Unterhaltung.<br><br>
       Vielen Dank für die Nutzung des Bundesliga-ChatBots.<br><br>
       
       Mit freundlichen Grüßen<br><br><br>

       Ihr Bundesliga-ChatBot Team<br><br><br>

       Erstellt am {created_datetime_file_name}
       '''

    msg = MIMEMultipart()
    msg['From'] = formataddr(("Bundesliga-ChatBot", from_email))
    msg['To'] = to_email
    msg['Subject'] = f'Bundesliga-ChatBot Report vom {created_datetime_file_name}'

    msg.attach(MIMEText(body, 'html'))

    
    attachment.seek(0)

    part = MIMEBase('application', 'pdf')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename="Bundesliga-ChatBot-Report-{created_datetime_sending_time}.pdf"'
    )
    msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())


