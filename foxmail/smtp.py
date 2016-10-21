# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText

# 第三方 SMTP 服务
mail_host="smtp.sina.com"                       #设置服务器
mail_user="phantom0506@sina.com"                 #用户名
mail_pass="txyb123456"                           #口令
receivers = ['245297262@qq.com']                        # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
subject = 'Python SMTP 邮件测试'
message['Subject'] = subject
message['from'] = 'phantom0506@sina.com'

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(mail_user, receivers, message.as_string())
    print "邮件发送成功"
except smtplib.SMTPException,e:
    print e

