#-*-coding:utf8-*-

from email.mime.text import MIMEText
from configReader import configReader
import poplib
import smtplib
import re

class mailHelper(object):
    CONFIGPATH = '_config.ini'

    def __init__(self):
        cfReader = configReader(self.CONFIGPATH)
        self.pophost = cfReader.readConfig('Slave', 'pophost')
        self.smtphost = cfReader.readConfig('Slave', 'smtphost')
        self.port = cfReader.readConfig('Slave', 'port')
        self.username = cfReader.readConfig('Slave', 'username')
        self.password = cfReader.readConfig('Slave', 'password')
        self.bossMail = cfReader.readConfig('Boss', 'mail')
        self.loginMail()
        self.configSlaveMail()

    def loginMail(self):
        try:
            self.pp = poplib.POP3_SSL(self.pophost)             #SSL加密登陆
            self.pp.set_debuglevel(0)                           #是否显示调试信息
            self.pp.user(self.username)
            self.pp.pass_(self.password)
            self.pp.list()
            print u'登录成功！'
        except Exception,e:
            print u'登录失败！'
            exit()

    def acceptMail(self):
        try:
            ret = self.pp.list()                                 #读取邮件列表
            mailBody = self.pp.retr(len(ret[1]))
            return mailBody
        except Exception, e:
            return None

    def configSlaveMail(self):

        try:
            self.handle = smtplib.SMTP(self.smtphost, self.port)
            self.handle.login(self.username, self.password)
        except Exception, e:
            exit()

    def sendMail(self, subject, receiver, body='Success'):
        msg = MIMEText(body,'plain','utf-8') #中文需参数‘utf-8’，单字节字符不需要
        msg['Subject'] = subject
        msg['from'] = self.username
        if receiver == 'Slave':                                            #发给自己
            try:
                self.handle.sendmail(self.username, self.username, msg.as_string())
                return True
            except Exception,e:
                return False

        elif receiver == 'Boss':                                           #发给对方
            try:
                self.handle.sendmail(self.username, self.bossMail, msg.as_string())
            except Exception,e:
                return False

if __name__ == '__main__':
    mail = mailHelper()
    body = mail.acceptMail()
    mail.sendMail('OK','Slave')
