import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import email.mime.text
import base64

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    print "canot import flags??"
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = '/home/pi/Monitor/client_secret.json'
APPLICATION_NAME = 'pyscript'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            #credentials = tools.run_flow(flow, store, flags)
            credentials = tools.run_flow(flow, store, "noauth_local_webserver")
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print(('Storing credentials to ' + credential_path))
    return credentials

def CreateMessage(sender, to, subject, message_text, files):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """

    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from os.path import basename
    #message = email.mime.text.MIMEText(message_text,  )
    message= MIMEMultipart()

    message['from'] = sender
    message['to'] = to
    message['subject'] = subject
    message.preamble = 'Multipart massage.\n'

    msgpart = MIMEText(message_text)
    message.attach(msgpart)

    for f in files or []:
        with open(f, "rb") as fil:
            message.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % basename(f),
                Name=basename(f)
            ))

    #return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode() }  #py3
    return {'raw': base64.urlsafe_b64encode(message.as_string()).decode() }  #py2


def SendMessage(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.
    Returns:
      Sent Message.
    """

    message = (service.users().messages().send(userId=user_id, body=message).execute())
    print(('Message Id: %s' % message['id']))
    return message

def sendEmail(frm, to, subjectline="empty subject", msgbody="empty body", files=None):
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    message = CreateMessage(frm, to, subjectline, msgbody, files)
    SendMessage(service, frm, message)

if __name__ == '__main__':
    sendEmail()
