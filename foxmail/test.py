#coding:GBK
# from HTMLParser import HTMLParser
#
# class hp(HTMLParser):
#     a_text = False
#
#     def handle_starttag(self,tag,attr):
#         if tag == 'br':
#             self.a_text = True
#             #print (dict(attr))
#
#     def handle_endtag(self,tag):
#         if tag == 'a':
#             self.a_text = False
#
#     def handle_data(self,data):
#         if self.a_text:
#             print (data)
#
# yk = hp()
# yk.feed('''<br><div id="origbody"><div style="background: #f2f2f2;">----- ԭʼ�ʼ� -----<br>�����ˣ�&lt;phantom0506@sina.com&gt;<br>�ռ��ˣ�"phantom0506" &lt;phantom0506@sina.com&gt;<br>���⣺�������⣩<br>���ڣ�2016��09��27�� 12��57��<br></div><br>��ð������������������쪴�ʦ��<p> </p></div>''')
# yk.close()
#

# import wx
# class MyFrame(wx.Frame):
#     def __init__(self, parent=None, title=u'�ʼ��ͻ���v1.0'):
#         wx.Frame.__init__(self, parent, -1, title=title)
#         self.panel = wx.Panel(self, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN | wx.FULL_REPAINT_ON_RESIZE)
#
#         #����һЩ�ؼ�:�û������벿�֣���ʹ��GridBagSizer��������Щ�ؼ�
#         self.label1=wx.StaticText(self.panel,-1,label=u'�û�����')
#         self.label2=wx.StaticText(self.panel,-1,label=u'  ���룺')
#         self.userText=wx.TextCtrl(self.panel,-1,size=(200,25))
#         self.passText=wx.TextCtrl(self.panel,-1,size=(200,25))
#         self.rempassCheck=wx.CheckBox(self.panel,-1,label=u'��ס����')
#         self.autologCheck=wx.CheckBox(self.panel,-1,label=u'�Զ���¼')
#
#         self.gbsizer1=wx.GridBagSizer(hgap=10, vgap=10)
#         self.gbsizer1.Add(self.label1,pos=(0,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
#         self.gbsizer1.Add(self.userText,pos=(0,1),span=(1,1),flag=wx.EXPAND)
#         self.gbsizer1.Add(self.label2,pos=(1,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
#         self.gbsizer1.Add(self.passText,pos=(1,1),span=(1,1),flag=wx.EXPAND)
#         self.gbsizer1.Add(self.rempassCheck,pos=(2,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
#         self.gbsizer1.Add(self.autologCheck,pos=(2,1),span=(1,1),flag=wx.ALIGN_CENTER|wx.ALIGN_CENTRE_VERTICAL)
#
#         #����һЩ�ؼ�:���������ò��֣���ʹ��GridBagSizer��������Щ�ؼ���
#         #Ȼ����ʹ��StaticBoxSizer����GridBagSizer
#         self.label3=wx.StaticText(self.panel,-1,label=u'��ַ��')
#         self.label4=wx.StaticText(self.panel,-1,label=u'�˿ڣ�')
#         self.ipadText=wx.TextCtrl(self.panel,-1,size=(170,25))
#         self.portText=wx.TextCtrl(self.panel,-1,size=(170,25))
#         self.proxyBtn=wx.Button(self.panel,-1,label=u'����\n����')
#
#         self.gbsizer2=wx.GridBagSizer(hgap=10,vgap=10)
#         self.gbsizer2.Add(self.label3,pos=(0,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
#         self.gbsizer2.Add(self.ipadText,pos=(0,1),span=(1,1),flag=wx.EXPAND)
#         self.gbsizer2.Add(self.proxyBtn,pos=(0,2),span=(2,1),flag=wx.EXPAND)
#         self.gbsizer2.Add(self.label4,pos=(1,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
#         self.gbsizer2.Add(self.portText,pos=(1,1),span=(1,1),flag=wx.EXPAND)
#
#         sbox=wx.StaticBox(self.panel,-1,label=u'������')
#         self.sbsizer=wx.StaticBoxSizer(sbox,wx.VERTICAL)
#         self.sbsizer.Add(self.gbsizer2,proportion=0,flag=wx.EXPAND,border=10)
#
#         #����һЩ�ؼ�:���·��İ�ť����ʹ��ˮƽ�����BoxSizer��������Щ�ؼ�
#         self.setserverBtn=wx.Button(self.panel,-1,label=u'���������á�')
#         self.loginBtn=wx.Button(self.panel,-1,label=u'��¼')
#         self.cancelBtn=wx.Button(self.panel,-1,label=u'ȡ��')
#
#         self.bsizer=wx.BoxSizer(wx.HORIZONTAL)
#         self.bsizer.Add(self.setserverBtn,1,flag=wx.EXPAND)
#         self.bsizer.Add(self.loginBtn)
#         self.bsizer.Add(self.cancelBtn)
#
#         #��"����������"��ť���¼�������
#         self.Bind(wx.EVT_BUTTON, self.OnTouch, self.setserverBtn)
#
#         #����BoxSizer,�����û������벿�ֵ�gbsizer1��
#         #���������ò��ֵ�sbsizer���Լ����·���bsizer
#         self.sizer = wx.BoxSizer(wx.VERTICAL)
#         self.sizer.Add(self.gbsizer1, 0, wx.EXPAND, 20)
#         self.sizer.Add(self.sbsizer, 0, wx.EXPAND, 20)
#         self.sizer.Add(self.bsizer, 0, wx.EXPAND, 20)
#         self.isShown = False    #���������ָʾ��ǰ�Ƿ��ѽ��ؼ�����
#         self.sizer.Hide(self.sbsizer)    #���ؼ�����
#         self.SetClientSize((330,118))    #�������ߴ�
#
#         self.panel.SetSizerAndFit(self.sizer)
#         self.sizer.SetSizeHints(self.panel)
#
#     def OnTouch(self, event):
#         if self.isShown:    #�����ǰ�ؼ�����ʾ
#             self.setserverBtn.SetLabel(u'���������á�')    #���°�ť��ǩ
#             self.sizer.Hide(self.sbsizer)    #���ط��������ò���
#             self.isShown = False    #���������ò��ֵ�ǰ������
#             self.SetClientSize((330,118))    #�������ߴ�
#         else:
#             self.sizer.Show(self.sbsizer)    #�����ǰ�ؼ�������
#             self.setserverBtn.SetLabel(u'���������á�')    #���°�ť��ǩ
#             self.isShown = True    #���������ò��ֵ�ǰ����ʾ
#             self.SetClientSize((330,200))    #�������ߴ�
#         self.sizer.Layout()    #�ؼ����ڣ�ǿ��sizer���¼��㲢����sizer�еĿؼ�
#
#
# if __name__ == "__main__":
#     app = wx.App()
#     frame = MyFrame(None)
#     frame.Show(True)
#     app.MainLoop()
#

# encoding: utf-8

import wx
import telnetlib
from time import sleep
import thread

class LoginFrame(wx.Frame):
    """
    ��¼����
    """

    def __init__(self, parent, id, title, size):
        '��ʼ������ӿؼ������¼�'
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        self.serverAddressLabel = wx.StaticText(self, label = "Server Address", pos = (10, 50), size = (120, 25))
        self.userNameLabel = wx.StaticText(self, label = "UserName", pos = (40, 100), size = (120, 25))
        self.serverAddress = wx.TextCtrl(self, pos = (120, 47), size = (150, 25))
        self.userName = wx.TextCtrl(self, pos = (120, 97), size = (150, 25))
        self.loginButton = wx.Button(self, label = 'Login', pos = (80, 145), size = (130, 30))
        self.loginButton.Bind(wx.EVT_BUTTON, self.login)
        self.Show()

    def login(self, event):
        '��¼����'
        try:
            serverAddress = self.serverAddress.GetLineText(0).split(':')
            con.open(serverAddress[0], port = int(serverAddress[1]), timeout = 10)
            response = con.read_some()
            if response != 'Connect Success':
                self.showDialog('Error', 'Connect Fail!', (95, 20))
                return
            con.write('login ' + str(self.userName.GetLineText(0)) + '\n')
            response = con.read_some()
            if response == 'UserName Empty':
                self.showDialog('Error', 'UserName Empty!', (135, 120))
            elif response == 'UserName Exist':
                self.showDialog('Error', 'UserName Exist!', (135, 120))
            else:
                self.Close()
                ChatFrame(None, -2, title = 'ShiYanLou Chat Client', size = (500, 350))
        except Exception:
            self.showDialog('Error', 'Connect Fail!', (95, 20))

    def showDialog(self, title, content, size):
        '��ʾ������Ϣ�Ի���'
        dialog = wx.Dialog(self, title = title, size = size)
        dialog.Center()
        wx.StaticText(dialog, label = content)
        dialog.ShowModal()

class ChatFrame(wx.Frame):
    """
    ���촰��
    """

    def __init__(self, parent, id, title, size):
        '��ʼ������ӿؼ������¼�'
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        self.chatFrame = wx.TextCtrl(self, pos = (5, 5), size = (490, 310), style = wx.TE_MULTILINE | wx.TE_READONLY)
        self.message = wx.TextCtrl(self, pos = (5, 320), size = (300, 25))
        self.sendButton = wx.Button(self, label = "Send", pos = (310, 320), size = (58, 25))
        self.usersButton = wx.Button(self, label = "Users", pos = (373, 320), size = (58, 25))
        self.closeButton = wx.Button(self, label = "Close", pos = (436, 320), size = (58, 25))
        self.sendButton.Bind(wx.EVT_BUTTON, self.send)
        self.usersButton.Bind(wx.EVT_BUTTON, self.lookUsers)
        self.closeButton.Bind(wx.EVT_BUTTON, self.close)
        thread.start_new_thread(self.receive, ())
        self.Show()

    def send(self, event):
        '������Ϣ'
        message = str(self.message.GetLineText(0)).strip()
        if message != '':
            con.write('say ' + message + '\n')
            self.message.Clear()

    def lookUsers(self, event):
        '�鿴��ǰ�����û�'
        con.write('look\n')

    def close(self, event):
        '�رմ���'
    	con.write('logout\n')
    	con.close()
    	self.Close()

    def receive(self):
        '���ܷ���������Ϣ'
        while True:
        	sleep(0.6)
        	result = con.read_very_eager()
        	if result != '':
        		self.chatFrame.AppendText(result)

'��������'
if __name__ == '__main__':
    app = wx.App()
    con = telnetlib.Telnet()
    LoginFrame(None, -1, title = "Login", size = (280, 200))
    app.MainLoop()