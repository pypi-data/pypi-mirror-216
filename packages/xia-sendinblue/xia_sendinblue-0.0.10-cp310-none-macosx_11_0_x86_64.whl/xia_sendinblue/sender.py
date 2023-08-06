import os
import requests
import logging
from xia_mail_sender import MailSender


class SendInBlue(MailSender):
    API_URL = "https://api.sendinblue.com/v3/smtp/email"
    API_KEY = ""

    @classmethod
    def send_mail_plain(cls, sender: str, to: list, subject: str, content: str):
        headers = {
            "accept": "application/json",
            "api-key": "xkeysib-" + cls.API_KEY,
            "content-type": "application/json",
        }
        mail_json = {
            "sender": cls.get_sender_dict(sender),
            "to": [cls.get_sender_dict(mail) for mail in to],
            "subject": subject,
            "htmlContent": content
        }
        resp = requests.post(cls.API_URL, headers=headers, json=mail_json)
        if resp.status_code < 300:
            return True
        else:
            code, message = resp.json()["code"], resp.json()["message"]
            logging.error(f"Sendinblue Error: {code}({resp.status_code}): {message}")
            return False
