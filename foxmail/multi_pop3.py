#  -*- coding: UTF-8 -*-
from HTMLParser import HTMLParser
import poplib
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

class hp(HTMLParser):
    a_text = False
    # def __init__(self,indent):
    #     self.indent = indent
    def handle_starttag(self,tag,attr):
        if tag == 'br':
            self.a_text = True
            #print (dict(attr))

    def handle_endtag(self,tag):
        if tag == 'br':
            self.a_text = False

    def handle_data(self,data):
        if self.a_text:
            print '  '+data


def guess_charset(msg):                             #获得字符编码方法
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):                                      #字符编码转换方法
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):

            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
                if content_type=='text/html':
                    yk = hp()
                    yk.feed(content)
                    yk.close()
                else:
                    print('%sText: %s' % ('  ' * indent, content + '...'))

        # if content_type=='text/plain' or content_type=='text/html':
        #     content = msg.get_payload(decode=True)
        #     charset = guess_charset(msg)
        #     if charset:
        #         content = content.decode(charset)
        #     print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))

pop3_server = "pop.sina.com"                        # pop3服务器地址
username = "phantom0506@sina.com"                    # 用户名
password ="txyb123456"                              #密码


server = poplib.POP3(pop3_server)
print(server.getwelcome())
server.user(username)
server.pass_(password)
print('Messages: %s. Size: %s' % server.stat())
resp, mails_number, octets = server.list()
resp, mailBody, octets = server.retr(len(mails_number)-3) # 获取最新一封邮件, 注意索引号从1开始:
msg = Parser().parsestr('\r\n'.join(mailBody))          # 解析邮件:

print_info(msg)                                            # 打印邮件内容:

# 慎重:将直接从服务器删除邮件:
# server.dele(len(mails))
# 关闭连接:
server.quit()