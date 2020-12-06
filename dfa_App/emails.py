from django.core.mail import EmailMessage
import datetime
from django.template.loader import get_template
from io import StringIO
from django.conf import settings
import csv
import imaplib
import email
import io
from dfa_App import views
import re

def send_error_report(_from, _to, _subject, _uploaddatetime, _uploadtype, _error):
    if _uploadtype == 'vehicle':
        ut = 'Fahrzeugdaten'
    if _uploadtype == 'his':
        ut = 'Reparaturarbeiten'
    if _uploadtype == 'workshop':
        ut = 'Werkstattdaten'
    ctx = {
        'title': _subject,
        'uploaddate': _uploaddatetime.strftime('%d.%m.%Y'),
        'uploadtime': _uploaddatetime.strftime('%H:%M:%S'),
        'uploadtype': ut,
    }
    htmly= get_template('email-templates/error_report.html')
    html_content = htmly.render(ctx)
    email = EmailMessage(_subject,html_content,_from,_to)
    if _error:
        a = create_attachment(_error)
        email.attach('Importfehler.csv', a.getvalue(), 'text/csv')
    email.content_subtype = 'html'
    email.send()
    return None

def create_attachment(_error):
    csvfile = StringIO()
    fieldnames = list(_error[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(_error)
    return csvfile

def start_tech_mail_listener(*args, **kwargs):
    #Funktioniert nicht, re.split() --> Leerzeichen werden zu tabs, Enter wird zu zwei mal enter, file not readable
    username = settings.TECH_EMAIL_HOST_USER
    password = settings.TECH_EMAIL_HOST_PASSWORD
    imap = imaplib.IMAP4_SSL(settings.TECH_EMAIL_HOST)
    imap.login(username,password)
    imap.select(settings.TECH_EMAIL_INBOX, readonly=True) 
    result, messages = imap.search(None, '(UNSEEN)')
    if result == "OK":
        for num in messages[0].split():
            typ, data = imap.fetch(num,'(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            subject = msg['Subject']
            attach = msg.get_payload()[1]
            file_name = attach.get_filename()
            content = attach.get_payload(decode=True).decode('utf-8').splitlines()
            with open("tmp.csv", "w") as csv_file:
                writer = csv.writer(csv_file, delimiter = '\t')
                for line in content:
                    writer.writerow(re.split('\s+',line))
                views.import_csv(csv_file,'vehicle', False)
    imap.close()
    imap.logout()
