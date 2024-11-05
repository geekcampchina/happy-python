from dataclasses import dataclass
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from os.path import basename

from typing import Tuple


@dataclass
class EmailAddr:
    name: str
    addr: str

    def to_tuple(self) -> Tuple[str, str]:
        return self.name, self.addr


@dataclass
class HappyEmail:
    """
    发送纯文本邮件类
    
    stmp_server: STMP服务器信息，主机地址和端口。比如 (localhost, 465)
    stmp_auth: STMP服务器登录信息，用户名和密码。比如 (admin@bar.com, 123456)
    recipients: 收件人列表。比如 (EmailAddr('收件人', mail_to@foo.com), )
    sender: 发件人。比如 EmailAddr('发件人', mail_from@bar.com)
    subject: 邮件标题
    body: 邮件正文
    files: 邮件附件列表
    use_tls: 启用 SSL/TLS 连接
    enable_debug: 启用调试模式
    """
    stmp_server: tuple
    stmp_auth: tuple
    recipients: list
    sender: EmailAddr
    subject: str
    body: str
    files: list
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

            to_str = ''
            recipients = []

            for email_addr_obj in self.recipients:
                to_str += formataddr(email_addr_obj.to_tuple()) + ','
                recipients.append(email_addr_obj.addr)

            to_str = to_str[:-1]

            msg = MIMEMultipart()
            msg['From'] = formataddr(self.sender.to_tuple())
            msg['To'] = to_str
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = Header(self.subject, 'utf-8')

            msg.attach(MIMEText(self.body, 'plain', 'utf-8'))

            for f in self.files:
                with open(f, "rb") as fil:
                    part = MIMEApplication(fil.read(), Name=basename(f))

                part.add_header('Content-Disposition',
                                'attachment',
                                filename=('utf-8', '', basename(f))
                                )
                msg.attach(part)

            client = smtplib.SMTP_SSL(stmp_host, stmp_port) if self.use_tls else smtplib.SMTP(stmp_host, stmp_port)

            if self.enable_debug:
                client.set_debuglevel(1)

            client.login(stmp_user, stmp_pwd)
            client.sendmail(self.sender.addr, recipients, msg.as_string())
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
