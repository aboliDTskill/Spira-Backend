import os
import base64
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# import imgkit
import pdfkit 

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']

def create_service():
    creds = None
    if os.path.exists('files/token.json'):
        creds = Credentials.from_authorized_user_file('files/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                print("Failed to refresh token")
                return None
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def send_email(service, to_mail):
    message = MIMEMultipart()
    message['to'] = to_mail
    message['subject'] = 'Subject: Email with Screenshot Attachment'
    msg = MIMEText('This is the body of the email.')
    message.attach(msg)
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    body = {'raw': raw}
    try:
        sent_message = service.users().messages().send(userId="me", body=body).execute()
        print(f'Message Id: {sent_message["id"]}')
        return sent_message["id"]
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def get_sent_email_content(service, message_id):
    try:
        message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        payload = message['payload']
        headers = payload.get('headers', [])
        
        email_details = {}
        for header in headers:
            if header['name'].lower() == 'from':
                email_details['From'] = header['value']
            elif header['name'].lower() == 'to':
                email_details['To'] = header['value']
            elif header['name'].lower() == 'subject':
                email_details['Subject'] = header['value']
            elif header['name'].lower() == 'date':
                email_details['Date'] = header['value']

        parts = payload.get('parts', [])
        email_body = ""
        if parts:
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    email_body = base64.urlsafe_b64decode(data).decode('utf-8')
                elif part['mimeType'] == 'text/html':
                    data = part['body']['data']
                    email_body = base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            if payload['mimeType'] == 'text/plain':
                data = payload['body']['data']
                email_body = base64.urlsafe_b64decode(data).decode('utf-8')
            elif payload['mimeType'] == 'text/html':
                data = payload['body']['data']
                email_body = base64.urlsafe_b64decode(data).decode('utf-8')

        return email_details, email_body
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None, None

def html_to_image(full_html_content, output_image_file):
    with open("email_content.html", "w") as file:
        file.write(full_html_content)
    # imgkit.from_file("email_content.html", output_image_file)
    pdfkit.from_file('email_content.html', 'example.pdf')
    os.remove("email_content.html")

def main(to_email):
    service = create_service()
    if service:
        message_id = send_email(service,to_email)
        if message_id:
            email_details, email_body = get_sent_email_content(service, message_id)
            if email_details and email_body:
                full_html_content = f"""
                <html>
                <body>
                <p><strong>From:</strong> {email_details.get('From', 'N/A')}</p>
                <p><strong>To:</strong> {email_details.get('To', 'N/A')}</p>
                <p><strong>Subject:</strong> {email_details.get('Subject', 'N/A')}</p>
                <p><strong>Date:</strong> {email_details.get('Date', 'N/A')}</p>
                <hr>
                <pre>{email_body}</pre>
                </body>
                </html>
                """
                html_to_image(full_html_content, "email_content.png")
                print("Email content saved as 'email_content.png'")

# if __name__ == '__main__':
#     to_email= 'mohan081995@gmail.com'
#     main(to_email)