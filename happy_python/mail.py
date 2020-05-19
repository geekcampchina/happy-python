#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class EmailAddr:
    name: str
    addr: str

    def to_tuple(self) -> tuple:
        return self.name, self.addr


@dataclass
class HappyEmail:
    """
    发送纯文本邮件类
    
    self.stmp_server: STMP服务器信息，主机地址和端口。比如 (localhost, 465)
    self.stmp_auth: STMP服务器登录信息，用户名和密码。比如 (admin@bar.com, 123456)
    self.recipients: 收件人列表。比如 (EmailAddr('收件人', mail_to@foo.com), )
    self.sender: 发件人。比如 EmailAddr('发件人', mail_from@bar.com)
    self.subject: 邮件标题
    self.body: 邮件正文
    use_tls: 启用 SSL/TLS 连接
    enable_debug: 启用调试模式
    """
    stmp_server: tuple
    stmp_auth: tuple
    recipients: list
    sender: EmailAddr
    subject: str
    body: str
    use_tls: bool = True
    enable_debug: bool = False

    def send_mail(self, enable_mock=False) -> bool:
        from happy_python import HappyLog
        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header
        from email.utils import formataddr

        hlog = HappyLog.get_instance()
        client = None

        # noinspection PyBroadException
        try:
            stmp_host, stmp_port = self.stmp_server
            stmp_user, stmp_pwd = self.stmp_auth

            body = MIMEText(self.body, 'plain', 'utf-8')

            to_str = ''
            recipients = []

            for email_addr_obj in self.recipients:
                to_str += formataddr(email_addr_obj.to_tuple()) + ','
                recipients.append(email_addr_obj.addr)

            to_str = to_str[:-1]

            body['to'] = to_str
            body['from'] = formataddr(self.sender.to_tuple())
            body['subject'] = Header(self.subject, 'utf-8')

            client = smtplib.SMTP_SSL(stmp_host, stmp_port) if self.use_tls else smtplib.SMTP(stmp_host, stmp_port)

            if self.enable_debug:
                client.set_debuglevel(1)

            client.login(stmp_user, stmp_pwd)
            client.sendmail(self.sender.addr, recipients, body.as_string())
            client.quit()

            hlog.info('发送邮件成功')
            return True
        except Exception as e:
            client.close()

            if not enable_mock:
                hlog.error('发送邮件失败')
                hlog.error(e)

            # 如果有测试标记，则返回True
            return True if enable_mock else False
