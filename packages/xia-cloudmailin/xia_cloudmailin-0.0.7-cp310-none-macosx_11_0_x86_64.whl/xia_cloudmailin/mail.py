import json
from email.utils import parsedate_to_datetime
from xia_mail import Mail, MailAttachment, MailField


class CloudMail(Mail):
    """Mail sent by cloud mail
    """
    @classmethod
    def parse_attachment(cls, attachment: dict):
        parsed = MailAttachment.from_display(**attachment)
        return parsed

    @classmethod
    def parse_payload(cls, payload: dict):
        header = payload["headers"]
        attachments = payload.pop("attachments", [])
        content = {
            "subject": header.get("subject", ""),
            "is_html": "html" in payload,
            "content": payload.get("html", payload.get("plain")),
            "mail_from": header.get("from", ""),
            'mail_to': [adr.strip() for adr in header.get("to", "").split(",") if adr],
            'mail_cc': [adr.strip() for adr in header.get("cc", "").split(",") if adr],
            'mail_bcc': [adr.strip() for adr in header.get("bcc", "").split(",") if adr],
            "mail_date": parsedate_to_datetime(header["date"]).timestamp(),
            "attachments": [cls.parse_attachment(attach) for attach in attachments],
            "raw_content": json.dumps(payload, ensure_ascii=False)
        }
        if content.get("mail_bcc", []):
            total_recipients = content['mail_bcc']
        else:
            total_recipients = content['mail_to'] + content['mail_cc']
        content["mail_recipients"] = [cls.get_sender_dict(recipient)["email"] for recipient in total_recipients]
        parsed_mail = cls(**content)
        parsed_mail.validate()
        return parsed_mail
