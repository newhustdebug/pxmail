from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

import poplib


# pop3_server = "pop.sina.com"                        # pop3服务器地址
# email = "phantom0506@sina.com"                    # 用户名
# password ="txyb123456"                              #密码

# pop3_server = "pop.163.com"                        # pop3服务器地址
# email = "tongxing1401@163.com"                    # 用户名
# password ="txyb123456"                              #密码
pop3_server = "mail.hust.edu.cn"                        # pop3服务器地址
email = "U201413426@hust.edu.cn"                    # 用户名
password ="HUSTMYGIRL.COM"                              #密码
popport="110"

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
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
        print (type(msg))
        print ("sssssssssssssssss")
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
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))

# 连接到POP3服务器:
server = poplib.POP3(pop3_server,popport)
# 可以打开或关闭调试信息:
server.set_debuglevel(1)
# 可选:打印POP3服务器的欢迎文字:
print(server.getwelcome().decode('utf-8'))
# 身份认证:
server.user(email)
server.pass_(password)
# stat()返回邮件数量和占用空间:
print('Messages: %s. Size: %s' % server.stat())
# list()返回所有邮件的编号:
resp, mails, octets = server.list()
# 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
print(mails)
# 获取最新一封邮件, 注意索引号从1开始:
index = len(mails)
resp, lines, octets = server.retr(index)
# lines存储了邮件的原始文本的每一行,
# 可以获得整个邮件的原始文本:
msg_content = b'\r\n'.join(lines).decode('utf-8')
# 稍后解析出邮件:
msg = Parser().parsestr(msg_content)
print_info(msg)
# 可以根据邮件索引号直接从服务器删除邮件:
# server.dele(index)
# 关闭连接:
server.quit()


# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# import time
# '''
# 信号传参类型
# pyqtSignal()                                #无参数信号
# pyqtSignal(int)                             # 一个参数(整数)的信号
# pyqtSignal([int],[str]                     # 一个参数(整数或者字符串)重载版本的信号
# pyqtSignal(int,str)                         #二个参数(整数,字符串)的信号
# pyqtSignal([int,int],[int,str])           #二个参数([整数,整数]或者[整数,字符串])重载版本
# '''
# class Mythread(QThread):
#     #定义信号,定义参数为str类型
#     _signal=pyqtSignal(str)
#     def __init__(self):
#         super(Mythread,self).__init__()
#     def run(self):
#         for i in range(2000000):
#             #发出信号
#             self._signal.emit('当前循环值为:%s'%i)
#             #让程序休眠
#             time.sleep(0.5)
#
# if __name__ == '__main__':
#     app = QApplication([])
#     dlg = QDialog()
#     dlg.resize(400, 300)
#     dlg.setWindowTitle("自定义按钮测试")
#     dlgLayout = QVBoxLayout()
#     dlgLayout.setContentsMargins(40, 40, 40, 40)
#     btn=QPushButton('测试按钮')
#     dlgLayout.addWidget(btn)
#     dlgLayout.addStretch(40)
#     dlg.setLayout(dlgLayout)
#     dlg.show()
#
#
#     def chuli(s):
#         dlg.setWindowTitle(s)
#         btn.setText(s)
#     #创建线程
#     thread=Mythread()
#     #注册信号处理函数
#     thread._signal.connect(chuli)
#     #启动线程
#     thread.start()
#     dlg.exec_()
#     app.exit()