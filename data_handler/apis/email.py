import smtplib
import os
import logging

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    logger = logging.getLogger(__name__)

    def __init__(self, host: str=None, port: int=0, sender: str=None, sender_pwd: str=None) -> None:
        self.host = host or os.getenv('TG_EMAIL_HOST', '') or "mail.migu.cn"
        self.port = port or int(os.getenv('TG_EMAIL_PORT', 0)) or 25
        self.sender = sender or os.getenv('TG_EMAIL_ACCOUNT', '')
        self.sender_pwd = sender_pwd or os.getenv('TG_EMAIL_PASSWD', '')

    def add_html_attachment(self, message: MIMEMultipart, org_file, attachment_file_name):
        if not os.path.exists(org_file):
            self.logger.warning(f"Email {org_file} attachment not exists.")
            return
        with open(org_file, 'r', encoding='utf-8') as fp:
            html_attch = MIMEText(fp.read(), 'html', 'utf-8')
            html_attch.add_header('Content-Disposition', 'attachment', filename=attachment_file_name)
            message.attach(html_attch)

    def send(
        self,
        to_list: list[str],
        subject: str,
        content: str = "",
        cc_list: list[str] = [],
        attachment: dict = {}
    ):
        """群发邮件功能
        :param to_list: 收件人列表.
        :type to_list: list[str]

        :param subject: 邮件主题.
        :type subject: str

        :param content: 邮件内容, html格式.
        :type content: str

        :param cc_list: 抄送人列表.
        :type cc_list: list[str]
        """
        self.logger.debug(f'{subject=}, {to_list=}, {cc_list=}')
        message = MIMEMultipart('related')
        message["Subject"] = subject
        message["From"] = self.sender
        message["To"] = ';'.join(to_list)
        if cc_list:
            message["Cc"] = ';'.join(cc_list)
        if content:
            message.attach(MIMEText(content, 'html', 'utf-8'))
        for attach, newname in attachment.items():
            self.add_html_attachment(message, attach, newname)
        with smtplib.SMTP(self.host, self.port) as smtp:
            smtp.login(self.sender, self.sender_pwd)
            smtp.send_message(message)