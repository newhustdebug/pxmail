# -*- coding:utf-8 -*-
import os
import re
import pickle
import time
import poplib
import imaplib
import chardet
from bs4 import UnicodeDammit
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
            smtp_backend = smtplib.SMTP(gl.smtphost, 25)
            # smtp_backend.connect(gl.smtphost, gl.smtpport)    # 25 为 SMTP 端口号
            if gl.smtpssl:
                smtp_backend.starttls()
            smtp_backend.login(gl.username,gl.password)
            smtp_backend.sendmail(gl.username, gl.receivers, gl.message.as_string())
        except Exception as e:
            gl.error=str(e)
            self.triggerFail.emit()
            return

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
            gl.error=str(e)
            print (e)
            self.trigger2.emit()



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
                    # resp, mailBody, octets = pop_backend.retr(len(gl.mails_number)-i) # 获取最新一封邮件, 注意索引号从1开始:
                    # msg_content = b'\r\n'.join(mailBody).decode()          #此处有BUG，收取部分邮件会UTF8解码出错
                    # msg = Parser().parsestr(msg_content)          # 解析邮件:

                    resp, lines, octets = pop_backend.retr(len(gl.mails_number)-i)
                    msg_byte = b'\r\n'.join(lines)
                    msg_content=msg_byte.decode(chardet.detect(msg_byte)['encoding'])

                    msg = Parser().parsestr(msg_content)

                    mails.append((i+1,msg))
                    gl.step=i+1
                    self.triggerNumber.emit()
                except Exception as e:
                    print (str(e)+'receive :'+str(i))
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
                    print(e)+'save'
        gl.March_ID=gl.emails                                   #匹配到的邮件等于所有邮件
        self.cache._commit_state()

        self.triggerFinish.emit()

#草稿文件夹读取线程
class readFileThread(QtCore.QThread):
    triggerFinish = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(readFileThread, self).__init__(parent)

    def run(self):

        gl.emails = []
        files = os.listdir(gl.read_path)                                                       #列出目录下的文件
        files.sort()                                                  #整理文件顺序
        mail_files = [f for f in files if os.path.isfile(os.path.join(gl.read_path, f))]
        for mail_file in mail_files:
            try:
                # with open(os.path.join(self.folder_path, mail_file), 'r',encoding= 'utf-8') as mail_handle:
                with open(os.path.join(gl.read_path, mail_file), 'r') as mail_handle:
                    gl.emails.append(message_from_file(mail_handle))        #带附件的邮件，在此处会有BUG,QQ邮箱
            except Exception as e:
                    print(e)
        gl.March_ID=gl.emails                                   #匹配到的邮件等于所有邮件
        self.triggerFinish.emit()

#搜索线程
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
        gl.draft_path=os.path.join(gl.cache_path, '草稿夹')
        gl.contact_path=os.path.join(gl.cache_path, 'contact.csv')
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


def getCoding(strInput):
  '''
  获取编码格式
  '''
  try:
      str=strInput.decode("utf8")
      return str
  except:
      pass
  try:
      str=strInput.decode("GB2312")
      return str
  except:
      pass


class EmailParser(object):

    cleaning_is_enabled = False

    @staticmethod
    def parse_email_body(email_message):

        if not email_message:
            return None, None

        attachments = []

        body_plain = u''
        body_html = u''
        body_image = u''
        body_attacments_info = u''
        mainbodydata = u''

        already_have_html = False

        if email_message.is_multipart():
            for part in email_message.walk():
                # print part.get_content_type(), part.is_multipart(), len(part.get_payload())

                charset = part.get_content_charset()

                if charset and charset.lower() in VALID_ENCODINGS:
                    charset = None

                content_type = part.get_content_type()

                if 'text/html' in content_type:
                    body_html = EmailParser.decode_part(part, charset, content_type)
                    already_have_html = True

                elif ('text/plain' in content_type and not already_have_html) \
                        or 'text/calendar' in content_type:
                    body_plain = '<pre style="white-space:pre-wrap; word-wrap:break-word;">' \
                                 + EmailParser.decode_part(part, charset) + "</pre>"

                elif 'image/png' in content_type \
                        or 'image/jpeg' in content_type \
                        or 'image/jpg' in content_type \
                        or 'image/gif' in content_type:
                    body_image += EmailParser.decode_image_part(part, content_type)

                else:
                    filename = part.get_filename()
                    # content_disposition = part['Content-Disposition']

                    if filename:
                        body_attacments_info += "<b>Attachment</b>: {0}<br/>\n".format(filename)
                        attachment = Attachment(filename, part.get_payload(decode=True))
                        attachments.append(attachment)

                    else:
                        dec_payload = EmailParser.decode_part(part, charset)
                        if dec_payload:
                            body_attacments_info += '''<br/><p><small>Content-Type: %s</small></p>%s''' % (
                                content_type, dec_payload)

        else:
            content_type = email_message.get_content_type()
            msg_charset = email_message.get_content_charset()

            if content_type and 'text/plain' in content_type.lower():
                mainbodydata = u'<pre  style="white-space:pre-wrap; word-wrap:break-word;">' \
                               + EmailParser.decode_part(email_message, msg_charset) + u"</pre>"
            else:
                if msg_charset and msg_charset.lower() in VALID_ENCODINGS:
                    mainbodydata = EmailParser.decode_part(email_message, msg_charset)
                else:
                    mainbodydata = EmailParser.decode_part(email_message)

        assembled_body = body_html or body_plain + body_image + body_attacments_info + mainbodydata

        return assembled_body, attachments
        # email_bodies.append((htmlhead + mainbodydata, attachments, email_message))

    @staticmethod
    def parse_email_headers(email_message, allowed_headers=None):

        """
        TODO: only parse headers, stash Message object into storage and only parse it when
              the item is selected
        https://gist.github.com/miohtama/5389146

        insert image into QTextEdit

        return dictionary of key values for headers
        :param allowed_headers:
        """
        if not allowed_headers:
            allowed_headers = ['subject',
                               'from',
                               'to',
                               'date',
                               'reply-to',
                               'x-mailer']

        headers = {}

        for key in email_message.keys():
            if key.lower() in (allowed_headers):

                current_header = email_message[key]

                if key.lower() in ['from', 'to', 'reply-to']:
                    current_header = EmailParser.clean_header(current_header, chars="""'\"""")

                # print repr(current_header)
                decoded_chunks = decode_header(current_header)

                header_chunks = []
                try:
                    for val, enc in decoded_chunks:
                        if enc and enc.lower() in VALID_ENCODINGS:
                            header_chunks.append(unicode(val, encoding=enc))
                        else:
                            if chardet:
                                guessed_enc = chardet.detect(current_header)['encoding']

                                if guessed_enc == 'ascii':
                                    guessed_enc = 'latin1'

                                if guessed_enc:
                                    header_chunks.append(unicode(val, encoding=guessed_enc))
                                else:
                                    header_chunks.append(unicode(val, encoding='latin1', errors='ignore'))
                            else:
                                header_chunks.append(val.decode('latin1'))

                    current_header = (''.join(header_chunks))

                except (LookupError, UnicodeDecodeError) as e:
                    LOG.error('Error decoding header: %s', pprint.pformat(current_header), exc_info=e)

                    if chardet:
                        guessed_encoding = chardet.detect(current_header)['encoding']

                        if guessed_encoding:
                            LOG.debug('\t\tguessed encoding %s', guessed_encoding)
                            current_header = unicode(current_header, encoding=guessed_encoding, errors='ignore')
                        else:
                            LOG.debug('\t\tsupressing errors in header: %s', pprint.pformat(current_header))
                            current_header = unicode(current_header, encoding='utf8', errors='ignore')
                    else:
                        LOG.debug('\t\tsupressing errors in header: %s', pprint.pformat(current_header))
                        current_header = unicode(current_header, encoding='utf8', errors='ignore')

                if key.lower() in ['from', 'to', 'reply-to']:
                    current_header = EmailParser.clean_header(current_header, '\r\n\t')

                if key.lower() == 'date':
                    parsed_date = parsedate_tz(current_header)

                    if parsed_date:
                        timestamp = mktime_tz(parsed_date)
                        headers['timestamp'] = timestamp

                        if timestamp:
                            formatted_time = datetime.datetime.fromtimestamp(
                                    timestamp).strftime('%d-%b-%Y %H:%M')
                            current_header = formatted_time

                headers[key] = current_header

        return headers

    @staticmethod
    def clean_header(header, chars=None):

        # if '" <' in header:
        #     parts = header.split('" <')
        #
        #     if len(parts) == 2:
        #         left = parts[0].replace('"', '').strip()
        #         right = parts[1]
        #         cln_right = right.replace('<', '').replace('>', '').strip()
        #
        #         if left.lower() == cln_right.lower():
        #             header = cln_right
        #         else:
        #             header = left + ' ' + right
        # if '"' in hedr:
        #     hedr = hedr.translate({ord('\\'): None, ord("'"): None, ord('"'): None})
        # if '\n' in hedr or '\r' in hedr:
        #     hedr = hedr.translate({ord('\r'): None, ord('\n'): None})
        # if isinstance(header, unicode):
        #     return header.translate({
        #                             ord('\\'): None,
        #                             ord("'"): None,
        #                             ord('"'): None,
        #                             ord('\r'): None,
        #                             ord('\n'): None,
        #                             ord('\t'): None
        #                             })
        clean = header
        for char in chars:
            clean = clean.replace(char, '')
        # else:
        return clean


    @staticmethod
    def decode_image_part(part, content_type):
        image_bytes = part.get_payload(decode=True)
        image_base64 = base64.b64encode(image_bytes)
        return '<img src="data:{0};base64,{1}">'.format(content_type,image_base64)

    @staticmethod
    def decode_part(part, charset=None, content_type=None):

        payload = None
        is_success = False

        try:
            payload = part.get_payload(decode=True)

            if isinstance(payload, str) and len(payload):

                if charset and charset in VALID_ENCODINGS:
                    try:
                        payload = unicode(payload, encoding=charset, errors="ignore") #.encode('utf8', 'replace')
                        is_success = True
                    except Exception as e:
                        LOG.debug('\t\terror decoding payload with charset: %s\n%s', charset, pprint.pformat(payload), exc_info=e)
                if not is_success and chardet:
                        guessed_charset = chardet.detect(payload)['encoding']

                        if guessed_charset and guessed_charset in VALID_ENCODINGS:
                            payload = unicode(payload, encoding=guessed_charset, errors='ignore')
                        else:
                            payload = unicode(payload, encoding='utf-8', errors='ignore')
            elif isinstance(payload, list) and len(payload):
                payload = "".join([unicode(pl, encoding='latin1', errors='ignore') for pl in payload])

        except Exception as e:
            LOG.error("error decoding payload for part: {}\n{}".format(pprint.pformat(part), str(e)))

            # payload = part.get_payload()
            #
            # if payload:
            #     if isinstance(payload, list) and len(payload):
            #         return "".join([str(pl) for pl in payload])

        if not payload:
            return u""

        if content_type and content_type == 'text/html' and EmailParser.cleaning_is_enabled and len(payload.strip()):

            try:
                if Cleaner and payload:

                    cleaner = Cleaner(page_structure=False, links=False, style=True, scripts=True, frames=True)
                    if isinstance(payload, unicode):
                        payload = payload.encode("utf-8")
                    payload = cleaner.clean_html(payload)
            except (lxml.etree.ParserError, UnicodeDecodeError, ValueError) as e:
                LOG.error("Html cleaning error:", exc_info=e)

        if isinstance(payload, str) and len(payload):
            payload = unicode(payload, encoding='utf-8', errors='ignore')

        return payload