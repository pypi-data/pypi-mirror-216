from email.message import EmailMessage
import os
import smtplib

from utilspkg import utils_init
utils_init.load_env_variables_from_yaml('/Users/croft/VScode/ptagit/channels_from_slack/env_vars.yaml')

GMAIL_USER = os.environ['GMAIL_USER']
GMAIL_FROM = os.environ['GMAIL_FROM']
GMAIL_PASSWORD = os.environ['GMAIL_PASSWORD']
TESTING_EMAIL = os.environ['TESTING_EMAIL']

class EmailConnect:
    """
    A utility class to send emails using Gmail's SMTP service.
    """

    def __init__(self, user_name=GMAIL_USER, pw=GMAIL_PASSWORD, from_name=GMAIL_FROM, testing_flag=False):
        """
        Constructs an instance of the EmailSender class.
        
        Args:
            user_name (str, optional): Gmail username to send emails. Defaults to GMAIL_USER environment variable.
            pw (str, optional): Gmail password. Defaults to GMAIL_PASSWORD environment variable.
            from_name (str, optional): Sender's display name in email. Defaults to GMAIL_FROM environment variable.
            testing_flag (bool, optional): Indicates whether to use a testing email address. Defaults to False.
        """
        self.user_name = user_name
        self.pw = pw
        self.from_name = from_name
        self.testing_flag = testing_flag
        self.testing_email = TESTING_EMAIL

    def send_email(self, to, subject, body, testing_flag=None):
        """
        Sends an email with the specified details using the Gmail SMTP service.

        Args:
            to (str): The recipient's email address.
            subject (str): The email subject.
            body (str): The email body.
            testing_flag (bool, optional): If set, overrides the `testing_flag` attribute of the class. Defaults to None.
        """
        if testing_flag is None:
            testing_flag = self.testing_flag
        to = to if not testing_flag else self.testing_email
        message = EmailMessage()
        message.set_content(body)
        message["From"] = self.from_name
        message["To"] = to
        message["Subject"] = subject

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.user_name, self.pw)
            server.send_message(message)
