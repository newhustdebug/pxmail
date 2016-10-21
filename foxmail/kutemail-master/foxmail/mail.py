# -*- coding:utf-8 -*-
import os
import re
import pickle
import time
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email import message_from_file


from pprint import pprint
import string
import email

cache_path='cache'




class MailReceive():
    """
    Retrieve emails through POP3
    """
    pop_backend = None
    
    def __init__(self,port, host, username, password,ssl):
        if ssl:
            self.pop_backend = poplib.POP3_SSL(host,port)           #SSL加密登陆
        else:
            self.pop_backend = poplib.POP3(host,port)
        self.pop_backend.user(username)
        self.pop_backend.pass_(password)

    def guess_charset(self,msg):                             #获得字符编码方法
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset
    def decode_str(self,s):                                      #字符编码转换方法
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value
    def get_info(self,msg, indent = 0):
        subject = ''
        addr = ''
        content = ''
        date=''
        html=''
        if indent == 0:
            for header in ['From', 'Subject','Date']:
                value = msg.get(header, '')
                if value:
                    if header=='Subject':
                        subject = self.decode_str(value)
                    elif header=='Date':
                        date = self.decode_str(value)
                    else:
                        hdr, addr = parseaddr(value)
        if msg.is_multipart():
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                # content_value = self.get_info(part, indent + 1)[2]
                # if content_value != '':
                #     content = content_value
                content_value = self.get_info(part, indent + 1)
                if content_value["content"] != '':
                    content = content_value["content"]
                elif content_value["html"] != '':
                    html = content_value["html"]
        else:
            content_type = msg.get_content_type()
            if content_type=='text/plain':
                content = msg.get_payload(decode=True)
                charset = self.guess_charset(msg)
                if charset:
                    content = content.decode(charset)
            else:
                content = ''
            if content_type=='text/html':
                html = msg.get_payload(decode=True)
                charset = self.guess_charset(msg)
                if charset:
                    html = html.decode(charset)
            else:
                html = ''
        # return (subject, addr, content,html,date)
        return {
            "subject": subject,
            "addr": addr,
            "content": content,
            "html":html,
            "date":date
        }



    def refresh_mail(self):
        pass
        # raw_folders = self.pop_backend.list()
        # print (raw_folders)


    def list_mail(self,folder):
        mails=[]
        resp, mails_number, octets = self.pop_backend.list()
        for i in range(len(mails_number)):
            resp, mailBody, octets = self.pop_backend.retr(len(mails_number)-i) # 获取最新一封邮件, 注意索引号从1开始:
            msg_content = b'\r\n'.join(mailBody).decode('utf-8')
            msg = Parser().parsestr(msg_content)          # 解析邮件:
            mails.append((i+1,msg))
        return mails

    # def list_mail(self, folder):
    #     self.pop_backend.select(folder)
    #     result, data = self.pop_backend.uid("search", None, "ALL")
    #     mailparser = emailparser.Parser()
    #     mails = []
    #     uid_block = data[0].split()
    #     #for uid_block in data:
    #     for uid in uid_block[0:20]:
    #         result, mail_data = self.pop_backend.fetch(uid, "(RFC822)")
    #         if result == "OK":
    #             try:
    #                 parsed_mail = mailparser.parsestr(mail_data[0][1].decode("utf-8"))
    #                 mails.append((uid, parsed_mail))
    #             except UnicodeDecodeError:
    #                 pass
    #     return mails


class MailCache():
    """
    Emails cache. Is totally independent from the back-end
    """
    receive = None
    cache_path = ''
    state_path = ''
    cache_state = {}
    MAX_AGE = 3600
    
    def __init__(self, cache_path, receive):
        self.receive = receive
        self.cache_path = cache_path
        self.state_path = os.path.join(cache_path, 'cache.state')
        
        if not os.path.isdir(self.cache_path):
            os.makedirs(self.cache_path)
        
        self._load_state()

    
    def list_mail(self, folder, force_refresh):
        folder_path = os.path.join(self.cache_path, folder)
        if self._is_stale(folder) or force_refresh == True:
            mails = self.receive.list_mail(folder)
            for mail in mails:
                # with open(os.path.join(folder_path, mail[0].decode('utf-8') + '.ml'), 'w') as mailcache:
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

# class MailLogin():
#     """
#     Abstracts fetching / sending and caching to an email account
#     """
#
#     def __init__(self, info):
#         self.pophost='pop.'+info["username"].split('@')[1]
#
#         receive = MailReceive(self.pophost, info['username'], info['password'])
#         self.cache = MailCache(cache_path, receive)
#
#
#
#     # def list_folders(self, force_refresh=False):
#     #     """Lists the available IMAP folders"""
#     #     return self.cache.list_folders(force_refresh)
#
#     def list_mail(self, folder, force_refresh=False):
#         """Lists emails in a folder, from cache if available"""
#         return self.cache.list_mail(folder, force_refresh)
