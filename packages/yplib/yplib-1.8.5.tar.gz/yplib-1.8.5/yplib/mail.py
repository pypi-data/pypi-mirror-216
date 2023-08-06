from yplib.index import *
import smtplib
from email.mime.text import MIMEText


def send_mail(title,
              content,
              user='',
              password='',
              send='',
              send_port=0,
              receivers=None):
    message = MIMEText(content, 'html', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(user)
    message['To'] = ",".join(receivers)
    message['Subject'] = title
    smtpObj = smtplib.SMTP_SSL(send, send_port)  # 启用SSL发信, 端口一般是465
    # try:
    smtpObj.login(user, password)
    smtpObj.sendmail(user, receivers, message.as_string())
    # return True
    # except smtplib.SMTPException as e:
    #     print(e)
    #     return False
    # finally:
    smtpObj.close()



# print('end')
