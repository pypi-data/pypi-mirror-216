from email.utils import parseaddr
from xia_fields import StringField, TimestampField, CompressedStringField, IntField, ByteField, BooleanField
from xia_engine import Document, EmbeddedDocument, ListField, EmbeddedDocumentField


class MailField(StringField):
    """Standard Mail Field

    Example:
        "john.smith@x-i-a.com"
        "John Smith <john.smith@x-i-a.com>"
    """
    def validate(self, value):
        super().validate(value)
        parsed_adr = parseaddr(value)
        if parsed_adr[1] == '':
            raise ValueError(f"No Mail Address found in {value}")


class MailAttachment(EmbeddedDocument):
    """Mail attachments"""
    file_name: str = StringField(required=True)  #: File name of attachment
    data_store: str = StringField(required=True, default="body")  #: Content store location
    size: int = IntField()  #: Mail Size
    content_type: str = StringField()  #: Attachment file type
    content: bytes = ByteField()  #: Attachment content if data_store = 'body'


class Mail(Document):
    """General Mail Objects"""
    _privilege_keys = {"receipt": ["mail_recipients"]}

    subject: str = StringField(required=True)  #: Mail subject
    is_html: bool = BooleanField()  #: If the mail content is in HTML format
    content: str = StringField()  #: Mail Content
    mail_from: str = MailField(required=True)  #: Sender of Mail
    mail_to: list = ListField(MailField())  #: Mail receivers
    mail_cc: list = ListField(MailField())  #: Mail Forwarded receivers
    mail_bcc: list = ListField(MailField())   #: Mail Hidden receiver
    mail_recipients: list = ListField(MailField())   #: Full Mail recipient List
    mail_date: float = TimestampField()  #: Mail Send Datetime
    attachments: list = ListField(EmbeddedDocumentField(document_type=MailAttachment))  #: Attachment List
    raw_content: str = CompressedStringField()  #: Raw content of mail without attachments

    @classmethod
    def get_sender_dict(cls, mail_adr: str):
        """Get sender information from mail address

        Args:
            mail_adr (str): Full Email address. Like "John Smith" <john.smith@x-i-a.com>

        Returns:
            dict: name and email
        """
        mail_dict = dict()
        parsed_adr = parseaddr(mail_adr)
        mail_dict["email"] = parsed_adr[1]
        if parsed_adr[0]:
            mail_dict["name"] = parsed_adr[0]
        else:
            mail_dict["name"] = parsed_adr[1].split("@")[0].replace(".", " ").replace("_", " ").title()
        return mail_dict

    def remove_adr(self, mail_adr: str):
        self.update(mail_recipients__remove__=mail_adr)
        if not self.mail_recipients:
            self.delete()
