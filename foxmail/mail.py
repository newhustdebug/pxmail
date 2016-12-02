# -*- coding:utf-8 -*-
import os
import re
import pickle
import time
import poplib
import imaplib
from PyQt5 import QtCore,QtWidgets
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email import message_from_file
from threading import Thread
import smtplib
from pprint import pprint
import string
import email
import parameter as gl

APPNAME = 'PxMail v3.0'

class sendingThread(QtCore.QThread):

    triggerSuccess = QtCore.pyqtSignal()
    triggerFail = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(sendingThread, self).__init__(parent)

    def run(self):
        try:
            smtp_backend = smtplib.SMTP()
            smtp_backend.connect(gl.smtphost, gl.smtpport)    # 25 为 SMTP 端口号
            if gl.smtpssl:
                smtp_backend.starttls()
            smtp_backend.login(gl.username,gl.password)
        except:
            QtWidgets.QMessageBox.warning(self, APPNAME,"smtp登陆失败" )
            self.triggerFail.emit()
            return
        try:
            smtp_backend.sendmail(gl.username, gl.receivers, gl.message.as_string())
        except:
            QtWidgets.QMessageBox.warning(self, APPNAME,"邮件发送失败" )
            self.triggerFail.emit()
            return
        QtWidgets.QMessageBox.warning(self, APPNAME,"邮件发送成功" )
        self.triggerSuccess.emit()


class loadingThread(QtCore.QThread):
    trigger1 = QtCore.pyqtSignal()
    trigger2 = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(loadingThread, self).__init__(parent)

    def run(self):
        global pop_backend
        try:
            if gl.popssl:
                pop_backend = poplib.POP3_SSL(gl.pophost,gl.popport)           #SSL加密登陆
            else:
                pop_backend = poplib.POP3(gl.pophost,gl.popport)
            pop_backend.user(gl.username)
            pop_backend.pass_(gl.password)
            resp, gl.mails_number, octets = pop_backend.list()
            self.trigger1.emit()
        except Exception as e:
            self.trigger2.emit()
            QtWidgets.QMessageBox.warning(self, APPNAME,str(e) )


class receiveThread(QtCore.QThread):
    triggerNumber = QtCore.pyqtSignal()
    triggerFinish = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(receiveThread, self).__init__(parent)
        self.cache=MailCache()
    def run(self):
        gl.cathe_folder_path = os.path.join(gl.cache_path, gl.folder_path)
        if self.cache._is_stale(gl.folder_path) or gl.force_refresh == True :
            gl.force_refresh == False
            mails=[]
            for i in range(len(gl.mails_number)):
                try:
                    resp, mailBody, octets = pop_backend.retr(len(gl.mails_number)-i) # 获取最新一封邮件, 注意索引号从1开始:
                    msg_content = b'\r\n'.join(mailBody).decode()          #此处有BUG，收取部分邮件会UTF8解码出错
                    msg = Parser().parsestr(msg_content)          # 解析邮件:
                    # msg = email.message_from_bytes(b'\n'.join(mailBody))
                    mails.append((i+1,msg))
                    gl.step=i+1
                    self.triggerNumber.emit()
                except Exception as e:
                    print(e)
            for mail in mails:
                with open(os.path.join(gl.cathe_folder_path, str(mail[0]) + '.ml'), 'w') as mailcache:
                    mailcache.write(mail[1].as_string())

            self.cache._renew_state(gl.folder_path)
        gl.emails = []
        files = os.listdir(gl.cathe_folder_path)                                                       #列出目录下的文件
        files.sort(key=lambda x:int(x[:-3]))                                                  #整理文件顺序
        mail_files = [f for f in files if os.path.isfile(os.path.join(gl.cathe_folder_path, f))]
        for mail_file in mail_files:
            try:
                # with open(os.path.join(self.folder_path, mail_file), 'r',encoding= 'utf-8') as mail_handle:
                with open(os.path.join(gl.cathe_folder_path, mail_file), 'r') as mail_handle:
                    gl.emails.append(message_from_file(mail_handle))        #带附件的邮件，在此处会有BUG,QQ邮箱
            except Exception as e:
                    print(e)
        gl.March_ID=gl.emails                                   #匹配到的邮件等于所有邮件
        self.cache._commit_state()

        self.triggerFinish.emit()


class searchThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(searchThread, self).__init__(parent)

    def run(self):
        gl.March_ID=[]                                                  #匹配符合条件的邮件
        for email in gl.emails:
            info=get_info(email)
            if (gl.string in info["subject"]) or (gl.string in info["content"]) or (gl.string in info["addr"]):
                gl.March_ID.append(email)
                data=info["subject"]+info["content"]+info["addr"]
                pattern = re.compile(gl.string)
                dataMatched = re.findall(pattern, data)                        #匹配所有关键字，背景高亮
                gl.highlight.setHighlightData(dataMatched)
                gl.highlight.rehighlight()

        self.trigger.emit()




class refreshThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(refreshThread, self).__init__(parent)
        self.cache=MailCache()
    def run(self):
        gl.emails = self.cache.list_mail(gl.folder_path,False)
        self.trigger.emit()



class MailCache():
    """
    Emails cache. Is totally independent from the back-end
    """
    receive = None
    state_path = ''
    cache_state = {}
    MAX_AGE = 3600

    def __init__(self,):
        gl.cache_path = os.path.join('cache', gl.username)
        gl.temp_path=os.path.join(gl.cache_path, 'temp')
        self.state_path = os.path.join(gl.cache_path, 'cache.state')

        if not os.path.isdir(gl.cache_path):                            #创建每个用户的目录
            os.makedirs(gl.cache_path)
        if not os.path.isdir(os.path.join(gl.cache_path, '草稿夹')):
            os.makedirs(os.path.join(gl.cache_path, '草稿夹'))
        if not os.path.isdir(os.path.join(gl.cache_path, '垃圾邮件')):
            os.makedirs(os.path.join(gl.cache_path, '垃圾邮件'))
        if not os.path.isdir(os.path.join(gl.cache_path, '收件夹')):
            os.makedirs(os.path.join(gl.cache_path, '收件夹'))
        if not os.path.isdir(os.path.join(gl.cache_path, '已发送')):
            os.makedirs(os.path.join(gl.cache_path, '已发送'))
        if not os.path.isdir(os.path.join(gl.cache_path, 'temp')):
            os.makedirs(os.path.join(gl.cache_path, 'temp'))
        self._load_state()


    def list_mail(self, folder, force_refresh):
        folder_path = os.path.join(gl.cache_path, folder)
        if self._is_stale(folder) or force_refresh == True:
            mails = self.receive.list_mail()
            for mail in mails:
                with open(os.path.join(folder_path, str(mail[0]) + '.ml'), 'w') as mailcache:
                    mailcache.write(mail[1].as_string())
            self._renew_state(folder)
        mails = []
        files = os.listdir(folder_path)                                                       #列出目录下的文件
        files.sort(key=lambda x:int(x[:-3]))                                                  #整理文件顺序
        mail_files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
        for mail_file in mail_files:
            with open(os.path.join(folder_path, mail_file), 'r',encoding= 'utf-8') as mail_handle:
                mails.append(message_from_file(mail_handle))
        self._commit_state()
        return mails


    def _is_stale(self, folder):                                                #不干净，被更改过
        if folder in self.cache_state:
            return time.time() - self.cache_state[folder] > self.MAX_AGE
        else:
            return True


    def _renew_state(self, folder):
        self.cache_state[folder] = time.time()

    def _load_state(self):
        if os.path.isfile(self.state_path):
            with open(self.state_path, 'rb') as cache:
                self.cache_state = pickle.load(cache)

    def _commit_state(self):
        with open(self.state_path, 'wb') as cache:
            pickle.dump(self.cache_state, cache)


def refresh_mail():
    resp, gl.mails_number, octets = pop_backend.list()


def guess_charset(msg):                             #获得字符编码方法
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
            charset=charset.split(';')[0]
    return charset
def decode_str(s):                                      #字符编码转换方法
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
def get_info(msg, indent = 0):
    subject = ''
    addr = ''
    content = ''
    date=''
    html=''
    filename=''
    received=''
    if indent == 0:
        for header in ['From', 'Subject','Date','Received']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    subject = decode_str(value)
                elif header=='Date':
                    date = decode_str(value)
                elif header=='Received':
                    received = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
    for part in msg.walk():
        filename = part.get_filename()
        content_type = part.get_content_type()
        charset = guess_charset(part)
        if filename:
            filename = decode_str(filename)
            gl.attachment = part.get_payload(decode = True)
            gl.file_path=os.path.join(gl.temp_path, filename)
            fEx = open(gl.file_path, 'wb')
            fEx.write(gl.attachment)
            fEx.close()


        elif content_type == 'text/plain':
            if charset:
                # content = part.get_payload(decode=True).decode('unicode_escape')      #处理新浪邮箱附件邮件的中文字符
                content = part.get_payload(decode=True).decode(charset)
        elif content_type == 'text/html':
            if charset:
                html = part.get_payload(decode=True).decode(charset)

    return {
        "subject": subject,
        "addr": addr,
        "content": content,
        "html":html,
        "date":date,
        "received":received,
        "filename":filename
        }