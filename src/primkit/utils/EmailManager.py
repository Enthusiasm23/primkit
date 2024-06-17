import os
import re
import logging
import smtplib
import yagmail
from smtplib import SMTPException
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.header import Header
from email.header import decode_header
from imapclient import IMAPClient

logger = logging.getLogger(__name__)


class EmailManager:
    def __init__(self, config, use_ssl=True, use_yagmail=False):
        """
        Initialize the EmailManager with configuration settings.

        :param config: A dictionary containing SMTP server configurations.
                       Required keys are:
                       - 'host': The SMTP server host.
                       - 'port': The SMTP server port.
                       - 'user': The SMTP account username.
                       - 'password': The SMTP account password.
                       Optional keys are:
                       - 'from': The email address to use in the 'from' header (defaults to 'user').
                       - 'from_alias': An alias name for the 'from' email address.
        :param use_ssl: A boolean indicating whether to use SSL for the connection. Defaults to True.
        :param use_yagmail: Use yagmail for sending emails. Defaults to False.
        :raises ValueError: If any required configuration items are missing or invalid.
        """
        # Ensure necessary configuration keys are present
        required_keys = ['host', 'port', 'user', 'password']
        optional_keys = ['from', 'from_alias']  # Define optional configuration keys

        # Check for missing required keys
        missing_required_keys = [key for key in required_keys if key not in config]
        if missing_required_keys:
            raise ValueError(f"Missing required configuration items: {', '.join(missing_required_keys)}. "
                             f"Optional items that can be included are: {', '.join(optional_keys)}.")

        # Validate email host and port
        self.host = config['host']
        if not (0 <= config['port'] <= 65535):
            raise ValueError("Port number must be between 0 and 65535")
        self.port = config['port']

        # Validate email address format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", config['user']):
            raise ValueError("Invalid email format for user")
        self.user = config['user']
        self.password = config['password']

        # Optional parameters with defaults
        self.use_ssl = use_ssl
        self.use_yagmail = use_yagmail
        if self.use_yagmail and not use_ssl:
            logger.warning("SSL setting is ignored when using yagmail.")
        self.from_addr = config.get('from', self.user)
        self.sender_alias = config.get('from_alias', '')

    def _login(self):
        """
        Initialize and login to the SMTP server using either smtplib or yagmail.
        """
        if self.use_yagmail:
            try:
                # Initialize yagmail SMTP connection
                self.smtp = yagmail.SMTP(user={self.user: self.sender_alias}, password=self.password, host=self.host, port=self.port)
            except Exception as e:
                logger.error(f"Yagmail SMTP initialization failed: {e}")
                raise
        else:
            try:
                # Initialize smtplib SMTP connection
                if self.use_ssl:
                    self.smtp = smtplib.SMTP_SSL(self.host, self.port)
                else:
                    self.smtp = smtplib.SMTP(self.host, self.port)
                    self.smtp.starttls()  # Upgrade to secure connection if not using SSL
                self.smtp.login(self.user, self.password)
            except SMTPException as e:
                logger.error(f"smtplib SMTP login failed: {e}")
                raise

    def test_conn(self):
        """
        Test the SMTP connection by logging in and then closing the connection.
        """
        try:
            self._login()
            self._close_conn()
            logger.info("SMTP connection successful.")
        except Exception as e:  # Catching all exceptions to cover both smtplib and yagmail
            logger.error(f"Connection test failed: {e}")
            raise

    def _close_conn(self):
        """
        Close the SMTP connection. For smtplib, it explicitly closes the connection.
        For yagmail, it does nothing as yagmail handles it internally.
        """
        if not self.use_yagmail:
            try:
                self.smtp.quit()
            except Exception as e:
                logger.error(f"Error closing connection: {e}")

    def send_email(self, to_addrs, subject, message, cc_addrs=None, bcc_addrs=None, attachments=None):
        """
        Send an email.

        :param to_addrs: List of recipient email addresses.
        :param subject: Subject of the email.
        :param message: Body of the email.
        :param cc_addrs: List of CC email addresses. Optional.
        :param bcc_addrs: List of BCC email addresses. Optional.
        :param attachments: List of Path to the file to be attached. Optional.
        """
        try:
            self._login()  # Initialize and login for either smtplib or yagmail

            if self.use_yagmail:
                # Use yagmail to send the email
                self.smtp.send(to=to_addrs, subject=subject, contents=[message], cc=cc_addrs, bcc=bcc_addrs,
                               attachments=attachments)
            else:
                msg = MIMEMultipart()
                msg['From'] = formataddr((self.sender_alias, self.from_addr))
                msg['To'] = ', '.join(to_addrs)
                msg['Subject'] = subject

                if cc_addrs:
                    msg['Cc'] = ', '.join(cc_addrs)
                if bcc_addrs:
                    msg['Bcc'] = ', '.join(bcc_addrs)

                msg.attach(MIMEText(message, 'plain'))

                if attachments:
                    for attachment in attachments:
                        with open(attachment, 'rb') as annex:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(annex.read())
                        encoders.encode_base64(part)
                        # 使用 Header 对象来创建一个适当的 Content-Disposition 头
                        filename_header = Header(os.path.basename(attachment), 'utf-8')
                        part.add_header('Content-Disposition', 'attachment', filename=str(filename_header))
                        msg.attach(part)

                # 使用 sendmail 而不是 send_message
                self.smtp.sendmail(self.from_addr,
                                   to_addrs + (cc_addrs if cc_addrs else []) + (bcc_addrs if bcc_addrs else []),
                                   msg.as_string())
                self.smtp.quit()

            logger.info('Email sent.')
        except Exception as e:
            logger.error(f'Failed to send email: {e}')
            raise

    def _imap_login(self) -> object:
        """
        Log in to the IMAP server and return the client.
        """
        try:
            server = IMAPClient(self.host)
            server.login(self.user, self.password)
            return server
        except Exception as e:
            logger.error(f"IMAP login failed: {e}")
            raise

    def check_sent(self, subject):
        """
        Check if an email with the specified subject has been sent.

        This function searches the 'Sent' folder of the email account for an email
        with the given subject. It uses IMAP to access the email server.

        :param subject: The subject of the email to search for.
        :return: True if an email with the specified subject is found, False otherwise.
        """
        try:
            server = self._imap_login()
            server.select_folder('Sent Messages')
            messages = server.search()
            if messages:
                logger.warning("Large number of sent emails can cause slow performance. Use this function cautiously.")
                sent_message = []
                for uid in reversed(messages):
                    response = server.fetch(uid, ['ENVELOPE', 'FLAGS', 'RFC822.SIZE'])
                    envelope = response[uid][b'ENVELOPE']
                    email_subject, decode = decode_header(envelope.subject.decode())[0]
                    sent_message.append(email_subject.decode(decode))
                    if subject == email_subject.decode(decode):
                        server.logout()
                        return True
                server.logout()
            else:
                server.logout()
                return False
        except Exception as e:
            logger.error(f"Error checking sent emails: {e}")
            raise
