#%%
import os
# import base64
from abc import ABC, abstractmethod
import email
import smtplib
import imaplib
import pandas as pd
import json
from email.message import EmailMessage as EMessage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
# from email import encoders
# from io import BytesIO

class EmailMessage:
    def __init__(self, from_address, recipients, subject, body=None, cc=None, bcc=None, content_type="plain"):
        self._from_address = from_address
        self.recipients = self._normalize_recipients(recipients)
        self.cc = self._normalize_recipients(cc) if cc is not None else []
        self.bcc = self._normalize_recipients(bcc) if bcc is not None else []
        self.subject = subject
        if body:
            self._body = str(body)
        else:
            self._body = body
        self._content_type = content_type
        self._attachments = []
        self.emessage = EMessage()
        self._message_id = None
        self._message_status = 'Created'
        self._error_message = None

        self.emessage["From"] = self._from_address
        self.emessage["To"] = self.recipients
        self.emessage["Subject"] = self.subject
        self.set_content(self._body, self._content_type)
        
        if self.cc:
            self.emessage["CC"] = ', '.join(self.cc)
        
        if self.bcc:
            self.emessage["BCC"] = ', '.join(self.bcc)

    @property
    def message_id(self):
        return self._message_id

    @message_id.setter
    def message_id(self, value):
        self._message_id = value

    @property
    def from_address(self):
        return self._from_address

    @from_address.setter
    def from_address(self, value):
        self._from_address = value
        self.emessage["From"] = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = str(value)
        self.set_content(self._body, self.content_type)

    @property
    def content_type(self):
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        self._content_type = value
        self.set_content(self._body, self._content_type)

    @property
    def attachments(self):
        display_attachments = [
            {k: v for k, v in attachment.items() if k != "file_content"}
            for attachment in self._attachments
        ]
        return display_attachments

    @property
    def message_status(self):
        return self._message_status

    @message_status.setter
    def message_status(self, value):
        self._message_status = value

    @property
    def error_message(self):
        return self._error_message

    @error_message.setter
    def error_message(self, value):
        self._error_message = value
    
    def set_content(self, content, content_type="plain"):
        if content_type == "html":
            self.emessage.set_content(content, subtype="html")
        else:
            self.emessage.set_content(content)
    
    def add_attachment(self, filename, file_data):
        """Accepts a filename and either a filepath or byte data and adds the attachment"""
        if isinstance(file_data, str):
            # Read file content from the filepath
            with open(file_data, "rb") as file:
                file_bytes = file.read()
        elif isinstance(file_data, bytes):
            file_bytes = file_data
        else:
            raise ValueError("Invalid file data provided.")
        
        mime_attachment = MIMEApplication(file_bytes, _subtype="octet-stream")
        mime_attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(filename))
        
        if self.emessage.is_multipart():
            self.emessage.attach(mime_attachment)
        else:
            multipart_message = MIMEMultipart()
            for header, value in self.emessage.items():
                multipart_message[header] = value
            multipart_message.attach(MIMEText(self.emessage.get_payload()))
            multipart_message.attach(mime_attachment)
            self.emessage = multipart_message
            
        file_extension = os.path.splitext(filename)[1][1:]
        
        attachment = {
            "filename": filename,
            "file_extension": file_extension,
            "file_content": file_bytes
        }
        self._attachments.append(attachment)
    
    def remove_attachment(self, filename=None):
        """Removes an attachment with the specified filename from the message"""
        for attachment in self._attachments:
            if not filename or attachment["filename"] == filename:
                self._attachments.remove(attachment)
                self._update_emessage_attachments()
                break

        for part in self.emessage.iter_attachments():
            if not filename or part.get_filename() == filename:
                self.emessage.detach(part)
                break
    
    @staticmethod
    def _normalize_recipients(recipients):
        if isinstance(recipients, str):
            return [recipients]
        elif isinstance(recipients, list):
            return recipients
        else:
            raise ValueError("Invalid recipients format. Expected string or list.")

    # @staticmethod
    # def dataframe_to_html(df):
    #     html_table = df.to_html(index=False, border=1, na_rep='<NA>')
    #     # html_table = f'<style>table {{border-collapse: collapse; border: 1px solid black;}}</style>{html_table}'
            
    #     # Add CSS styling to the table
    #     # html_table = f'<style>table {{border-collapse: collapse; border: 1px solid black;}} table td {{padding-left: 2px; padding-right: 4px;}}</style>{html_table}'
        
    #     # html_table = html_table.replace('<td', '<td style="padding-left: 2px; padding-right: 4px;"')

    #     # html_table = f'<table style="border-collapse: collapse; border: 1px solid black;">{html_table}</table>'
    #     # html_table = f'<style>.custom-cell {{padding-left: 2px; padding-right: 4px;}}</style>{html_table}'
    
    #     return html_table

    # @staticmethod
    # def html_body_with_object(body_object, body_object_type='html', body_prefix=None, body_suffix=None):
    #     if isinstance(body_object, str):
    #         if body_object_type.lower() in ['dictionary', 'dict', 'json']:
    #             try:
    #                 body_object_dict = json.loads(body_object)
    #                 body_object_html = f'<pre>{json.dumps(body_object_dict, indent=4)}</pre>'
    #             except json.JSONDecodeError:
    #                 return f'"body_object" must be a valid JSON string'
    #         else:
    #             if '<pre>' not in body_object and body_object_type != 'html':
    #                 body_object_html = f'<pre>{body_object}</pre>'
    #             else:
    #                 body_object_html = body_object
    #     elif isinstance(body_object, pd.DataFrame):
    #         body_object_html = EmailMessage.dataframe_to_html(body_object)
    #     elif isinstance(body_object, dict):
    #         body_object_html = f'<pre>{json.dumps(body_object, indent=4)}</pre>'
    #     # elif isinstance(body_object, str) and body_object_type.lower() in ['dataframe', 'data frame', 'df', 'pandas', 'pd']:
    #     else:
    #         return f'"df_html" must be a dataframe, dictionary or string, it is type {type(body_object)}'
    #     html_template = '''
    #     <!DOCTYPE html>
    #     <html>
    #     <head>
    #     </head>
    #     <body>
    #         {body_content}
    #     </body>
    #     </html>
    #     '''

    #     body_content = ''
    #     if body_prefix:
    #         body_content += f'{body_prefix}\n<br><br>\n'

    #     body_content += body_object_html

    #     if body_suffix:
    #         body_content += f'\n<br><br>\n{body_suffix}'

    #     return html_template.format(body_content=body_content)

    # @staticmethod
    # def body_builder(body_object_to_add, body_object_type='str', existing_body=''):
    #     if isinstance(body_object_to_add, str):
    #         if body_object_type.lower() in ['dictionary', 'dict', 'json']:
    #             try:
    #                 body_object_dict = json.loads(body_object_to_add)
    #                 body_object_html = f'<pre>{json.dumps(body_object_dict, indent=4)}</pre><td><td>'
    #                 existing_body += body_object_html
    #             except json.JSONDecodeError:
    #                 return f'"body_object" must be a valid JSON string'
    #         else:
    #             if '<pre>' not in body_object_to_add and body_object_type != 'html':
    #                 body_object_html = f'<pre>{body_object_to_add}</pre><td><td>'
    #                 existing_body += body_object_html
    #             else:
    #                 body_object_html = f'{body_object_to_add}<td><td>'
    #                 existing_body += body_object_html
    #     elif isinstance(body_object_to_add, pd.DataFrame):
    #         body_object_html = EmailMessage.dataframe_to_html(body_object_to_add) + '<td><td>'
    #         existing_body += body_object_html
    #     elif isinstance(body_object_to_add, dict):
    #         body_object_html = f'<pre>{json.dumps(body_object_to_add, indent=4)}</pre><td><td>'
    #         existing_body += body_object_html
    #     # elif isinstance(body_object, str) and body_object_type.lower() in ['dataframe', 'data frame', 'df', 'pandas', 'pd']:
    #     else:
    #         return f'"df_html" must be a dataframe, dictionary or string, it is type {type(body_object_to_add)}'
        
    #     return existing_body
        
    # @staticmethod
    # def wrap_html_body(body_content):
    #     if body_content.endswith("<td><td>"):
    #         body_content = body_content[:-8]
        
    #     html_template = '''
    #     <!DOCTYPE html>
    #     <html>
    #     <head>
    #     </head>
    #     <body>
    #         {body_content}
    #     </body>
    #     </html>
    #     '''

    #     return html_template.format(body_content=body_content)

class EmailBody:
    def __init__(self, body_text=''):
        if body_text and '<pre>' not in body_text:
            self.body_text = f'<pre>{body_text}</pre>'
            self.final_body_text = self.body_text
        else:
            self.body_text = body_text
            self.final_body_text = self.body_text

    def __str__(self):
        return self.final_body_text

    def __repr__(self):
        return self.__str__()

    # def add_to_body(self, body_object_to_add, body_object_type='str'):
    #     if isinstance(body_object_to_add, str):
    #         if body_object_type.lower() in ['dictionary', 'dict', 'json']:
    #             try:
    #                 body_object_dict = json.loads(body_object_to_add)
    #                 body_object_html = f'<pre>{json.dumps(body_object_dict, indent=4)}</pre><td><td>'
    #                 self.body_text += body_object_html
    #             except json.JSONDecodeError:
    #                 # return f'"body_object" must be a valid JSON string'
    #                 print(f'"body_object" must be a valid JSON string')
    #         else:
    #             if '<pre>' not in body_object_to_add and body_object_type != 'html':
    #                 body_object_html = f'<pre>{body_object_to_add}</pre><td><td>'
    #                 self.body_text += body_object_html
    #             else:
    #                 body_object_html = f'{body_object_to_add}<td><td>'
    #                 self.body_text += body_object_html
    #     elif isinstance(body_object_to_add, pd.DataFrame):
    #         body_object_html = EmailMessage.dataframe_to_html(body_object_to_add) + '<td><td>'
    #         self.body_text += body_object_html
    #     elif isinstance(body_object_to_add, dict):
    #         body_object_html = f'<pre>{json.dumps(body_object_to_add, indent=4)}</pre><td><td>'
    #         self.body_text += body_object_html
    #     # elif isinstance(body_object, str) and body_object_type.lower() in ['dataframe', 'data frame', 'df', 'pandas', 'pd']:
    #     else:
    #         # return f'"df_html" must be a dataframe, dictionary or string, it is type {type(body_object_to_add)}'
    #         print(f'"df_html" must be a dataframe, dictionary or string, it is type {type(body_object_to_add)}')

    def add_to_body(self, body_object_to_add, body_object_type='str'):
        body_object_html = None
        if isinstance(body_object_to_add, str):
            if body_object_type.lower() in ['html']:
                body_object_html = body_object_to_add
            elif body_object_type.lower() in ['dictionary', 'dict', 'json']:
                try:
                    body_object_dict = json.loads(body_object_to_add)
                    body_object_html = f'<pre>{json.dumps(body_object_dict, indent=4)}</pre>'
                except json.JSONDecodeError:
                    print('"body_object_to_add" must be a valid JSON string')
                    return
            else:
                if '<pre>' not in body_object_to_add:# and body_object_type != 'str':
                    body_object_html = f'<pre>{body_object_to_add}</pre>'
                else:
                    body_object_html = body_object_to_add
        elif isinstance(body_object_to_add, pd.DataFrame):
            body_object_html = self.dataframe_to_html(body_object_to_add)
        elif isinstance(body_object_to_add, dict):
            body_object_html = f'<pre>{json.dumps(body_object_to_add, indent=4)}</pre>'
        else:
            print(f'"body_object_to_add" must be a dataframe, dictionary, or string. It is of type {type(body_object_to_add)}')
            return

        if body_object_html is None:
            print('Could not add object to body')
            return
        
        self.body_text += f'{body_object_html}<td><td>'
        self.final_body_text = self.body_text
    
    def wrap_html_body(self):
        if self.body_text.endswith("<td><td>"):
            self.body_text = self.body_text[:-8]
        
        html_template = '''
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
            {body_content}
        </body>
        </html>
        '''

        self.final_body_text = html_template.format(body_content=self.body_text)

        # return html_template.format(body_content=self.body_text)

    @staticmethod
    def dataframe_to_html(df):
        html_table = df.to_html(index=False, border=1, na_rep='<NA>')

        return html_table

class EmailProtocol(ABC):
    def __init__(self):
        self.delivery_engine = None
        self.from_address = None

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def disconnect(self):
        pass

class DeliveryEmailProtocol(EmailProtocol, ABC):
    @abstractmethod
    def deliver_email(self, message: EmailMessage):
        pass

    @abstractmethod
    def deliver_all_emails(self):
        pass

class ReceiveEmailProtocol(EmailProtocol, ABC):
    @abstractmethod
    def fetch_unread_emails(self):
        pass

    @abstractmethod
    def fetch_attachment(self, message_uid, attachment_name):
        pass

class SMTPProtocol(DeliveryEmailProtocol):
    def connect(self, *args, **kwargs):
        self.server, self.port = args
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        
        # Create a connection to the SMTP server
        self.engine = smtplib.SMTP(self.server, self.port)
        self.engine.starttls()
        self.engine.login(self.username, self.password)
        self.from_address = self.engine.user

    def deliver_email(self, message: EmailMessage):
        try:
            self.engine.send_message(message.emessage)
            message.message_status = 'Sent'
        except Exception as e:
            message.message_status = 'Send Failure'
            message.error_message = str(e)

    def deliver_all_emails(self, email_messages = []):
        for message in email_messages:
            self.deliver_email(self, message)
    
    def disconnect(self):
        self.engine.quit()

class IMAPProtocol(ReceiveEmailProtocol):
    def connect(self, *args, **kwargs):
        self.server, self.port = args
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.engine = imaplib.IMAP4_SSL(self.server, self.port)
        self.engine.login(self.username, self.password)
        self.unread_emails = []
        # self.from_address = self.username

    def fetch_unread_emails(self):
        # Connect to the IMAP server
        # imap_server = imaplib.IMAP4_SSL(self.server, self.port)
        
        # Login to the email account
        # imap_server.login(self.username, self.password)
        
        # Select the mailbox (e.g., 'INBOX')
        self.engine.select("INBOX")
        
        # Search for unread emails
        # _, message_numbers = engine.search(None, "(UNSEEN)")
        _, message_uids = self.engine.uid('search', None, "(UNSEEN)")
        
        self.unread_emails = []
        
        # Loop through the message numbers
        for message_uid in message_uids[0].split():
            # Fetch the email details for each message number
            # _, msg_data = engine.fetch(message_uid, "(RFC822)")
            # _, msg_data = engine.uid('FETCH', message_uid, "(RFC822)")
            _, msg_data = self.engine.uid('fetch', message_uid, "(RFC822)")
            
            # Process the email message
            # Here, you can extract the desired details (e.g., subject, sender, date)
            # and store them in a dictionary or any other data structure
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)
            # Re-mark email as unread
            # engine.store(message_uid, '-FLAGS', '\\Seen')
            self.engine.uid('store', message_uid, '-FLAGS', '\\Seen')
            
            subject = email_message.get("Subject")
            sender = email_message.get("From")
            date = email_message.get("Date")

            # extract the email body
            if email_message.is_multipart():
                for part in email_message.get_payload():
                    content_type = part.get_content_type()
                    if content_type == "multipart/alternative":
                        for subpart in part.get_payload():
                            subpart_content_type = subpart.get_content_type()
                            if subpart_content_type == "text/plain":
                                email_body = subpart.get_payload(decode=True).decode().lower()
                                break
                            elif subpart_content_type == "text/html":
                                email_body = subpart.get_payload(decode=True).decode().lower()
                                break
                        if email_body:
                            break
                    elif "text" in content_type:
                        email_body = part.get_payload(decode=True).decode().lower()
                        break
            else:
                email_body = email_message.get_payload(decode=True).decode().lower()

            # check for attachments
            attachments = []
            # print(message_number.decode())
            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                    continue
                filename = part.get_filename()
                if filename:
                    attachment_details = {}
                    # attachments.append(filename.lower())
                    attachment_details['filename'] = filename
                    file_content = part.get_payload(decode=True)
                    file_size = len(file_content)
                    if file_size < 5 * 1024 * 1024:
                        attachment_details['file_content_extracted'] = 'True'
                        attachment_details['file_content'] = file_content
                    else:
                        attachment_details['file_content_extracted'] = 'False'
                        file_size_kb = '{:,}'.format(file_size // 1024)
                        file_content_str = f'File too large, size: {file_size_kb} KB'
                        attachment_details['file_content'] = file_content_str.encode('utf-8')
                    attachments.append(attachment_details)
                    # print(attachment_details)
                    # print(filename.lower())
                    # print(part.get_payload(decode=True))
            
            num_attachments = len(attachments)
            
            # Add the email details to the list
            self.unread_emails.append({
                "message_uid": message_uid.decode(),
                "sender": sender,
                "subject": subject,
                "date": date,
                "body": email_body,
                "num_attachments": num_attachments,
                "attachments": attachments,
                "message_data": raw_email
            })
        
        # Logout and close the connection
        # self.engine.logout()
        
        return self.unread_emails
    
    def fetch_attachment(self, message_uid, attachment_filename):
        for email_data in self.unread_emails:
            if email_data['message_uid'] == message_uid:
                for attachment in email_data['attachments']:
                    if attachment['filename'] == attachment_filename:
                        if attachment['file_content_extracted'] == 'True':
                            file_content = attachment['file_content']
                            return file_content
        
        if self.engine.state != 'SELECTED':
            self.engine.select("INBOX")
        _, msg_data = self.engine.uid('fetch', message_uid, "(RFC822)")
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        self.engine.uid('store', message_uid, '-FLAGS', '\\Seen')
        for part in email_message.walk():
            if part.get_filename() == attachment_filename:
                attachment_content = part.get_payload(decode=True)
                break
        if attachment_content:
            return attachment_content
        else:
            # return 'Attachment not found'.encode('utf-8')
            return None
            
    def disconnect(self):
        self.engine.quit()

class OAuth2Protocol(EmailProtocol):
    def connect(self, *args, **kwargs):
        server, port = args
        tenant_id = kwargs.get('tenant_id')
        client_id = kwargs.get('client_id')
        client_secret = kwargs.get('client_secret')
        # Implement OAuth2 connection here
        pass

    def deliver_email(self, message: EmailMessage):
        # Implement send method for SMTP here
        pass

class DeliveryEmailProvider(ABC):
    def __init__(self, name, server=None, port=None):
        self.name = name
        self.server = server
        self.port = port

class ReceivalEmailProvider(ABC):
    def __init__(self, name, server=None, port=None):
        self.name = name
        self.server = server
        self.port = port

class EmailProvider(ABC):
    def __init__(self, name, delivery_provider: DeliveryEmailProvider = None, receival_provider: ReceivalEmailProvider = None):
        self.name = name
        self.delivery_provider = delivery_provider
        self.receival_provider = receival_provider

    def __str__(self):
        return f"{self.name} Provider"

class CustomProvider(EmailProvider):
    def __init__(self, provider_name, delivery_server=None, delivery_port=None, receival_server=None, receival_port=None):
        delivery_provider = DeliveryEmailProvider(f'{provider_name} Delivery', delivery_server, delivery_port)
        receival_provider = ReceivalEmailProvider(f'{provider_name} Receival', receival_server, receival_port)
        super().__init__(provider_name, delivery_provider, receival_provider)

class GmailProvider(EmailProvider):
    def __init__(self):
        super().__init__("Gmail", 
                         DeliveryEmailProvider("Gmail Delivery", "smtp.gmail.com", 587),
                         ReceivalEmailProvider("Gmail Receival", "imap.gmail.com", 993))

class EmailClient:
    def __init__(self, provider: EmailProvider, delivery_protocol: DeliveryEmailProtocol, delivery_args: tuple, delivery_kwargs: dict, 
                 receive_protocol: ReceiveEmailProtocol, receive_args: tuple, receive_kwargs: dict):
        self.provider = provider
        self.delivery_protocol = delivery_protocol
        self.delivery_args = delivery_args
        self.delivery_kwargs = delivery_kwargs
        self.receive_protocol = receive_protocol
        self.receive_args = receive_args
        self.receive_kwargs = receive_kwargs
        # self.from_address = self.delivery_protocol.from_address or 'Unknown'
        self.from_address = None
        # self.unread_emails = unread_emails or []
        self.unread_emails = None
        self.email_messages = []
        self.max_message_id = 0

    def connect(self):
        if self.delivery_protocol:
            self.delivery_protocol.connect(*self.delivery_args, **self.delivery_kwargs)
            self.from_address = self.delivery_protocol.from_address
        if self.receive_protocol:
            self.receive_protocol.connect(*self.receive_args, **self.receive_kwargs)

    def provider_name(self):
        return str(self.provider)

    def from_address(self):
        return str(self.from_address)

    # def add_message(self, recipient, subject, body, attachments=None):
    #     message = EmailMessage(recipient, subject, body, attachments)
    #     self.messages.append(message)

    def add_message(self, message):
        # message = EmailMessage(recipient, subject, body, attachments)
        self.max_message_id += 1
        message.message_id = self.max_message_id
        # message.message_status = 'Created'
        self.messages.append(message)

    def deliver_email(self, message: EmailMessage):
        if self.delivery_protocol:
            self.delivery_protocol.deliver_email(message)
            # message.message_status = 'Sent'
        else:
            print('No delivery protocol provided')

    def deliver_all_emails(self):
        if self.email_messages:
            self.delivery_protocol.deliver_all_emails(self.email_messages)
        else:
            print('No emails to delivery')

    def fetch_unread_emails(self):
        if self.receive_protocol:
            self.unread_emails = self.receive_protocol.fetch_unread_emails()
        else:
            print('No receival protocol provided')

    def fetch_attachment(self, message_uid, attachment_filename):
        if self.receive_protocol:
            return self.receive_protocol.fetch_attachment(message_uid, attachment_filename)
        else:
            print('No receival protocol provided')
            return None
    
    def disconnect(self):
        if self.delivery_protocol:
            self.delivery_protocol.disconnect()
        if self.receive_protocol:
            self.receive_protocol.disconnect()

DELIVERY_PROTOCOLS = {
    "smtp": SMTPProtocol,
    # Add other protocol mappings
}

RECEIVAL_PROTOCOLS = {
    "imap": IMAPProtocol,
    # Add other protocol mappings
}

PROVIDERS = {
    "gmail": GmailProvider,
    # Add other provider mappings
}

def create_email_client(provider_name=None, delivery_protocol_name=None, receival_protocol_name=None, **kwargs) -> EmailClient:
    if os.getenv('NEXUS_EMAIL_USERNAME'):
        kwargs['username'] = os.getenv('NEXUS_EMAIL_USERNAME')
    
    if os.getenv('NEXUS_EMAIL_PASSWORD'):
        kwargs['password'] = os.getenv('NEXUS_EMAIL_PASSWORD')
    
    DeliveryProtocolClass = None
    if delivery_protocol_name:
        try:
            DeliveryProtocolClass = DELIVERY_PROTOCOLS[delivery_protocol_name.lower()]
        except KeyError:
            raise ValueError(f"Invalid delivery protocol descriptor specified: {delivery_protocol_name}")
    
    ReceivalProtocolClass = None
    if receival_protocol_name:
        try:
            ReceivalProtocolClass = RECEIVAL_PROTOCOLS[receival_protocol_name.lower()]
        except KeyError:
            raise ValueError(f"Invalid receival protocol descriptor specified: {receival_protocol_name}")

    try:
        if provider_name.lower() in PROVIDERS:
            ProviderClass = PROVIDERS[provider_name.lower()]
            provider = ProviderClass()
        else:
            ProviderClass = CustomProvider
            provider = CustomProvider(provider_name)
    except KeyError:
        raise ValueError("Invalid provider descriptor specified.")
    
    delivery_protocol = None
    delivery_args = None
    delivery_kwargs = None
    if DeliveryProtocolClass:
        delivery_protocol = DeliveryProtocolClass()
        delivery_server = kwargs.get('delivery_server', provider.delivery_provider.server)
        delivery_port = kwargs.get('delivery_port', provider.delivery_provider.port)
        delivery_args = (delivery_server, delivery_port)
        delivery_kwargs = kwargs

    receival_protocol = None
    receive_args = None
    receive_kwargs = None
    if ReceivalProtocolClass:
        receival_protocol = ReceivalProtocolClass()
        receival_server = kwargs.get('receival_server', provider.receival_provider.server)
        receival_port = kwargs.get('receival_port', provider.receival_provider.port)
        receive_args = (receival_server, receival_port)
        receive_kwargs = kwargs

    client = EmailClient(provider, delivery_protocol, delivery_args, delivery_kwargs, receival_protocol, receive_args, receive_kwargs)
    client.connect()
    
    return client

#%%
