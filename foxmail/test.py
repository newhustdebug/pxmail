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
# yk.feed('''<br><div id="origbody"><div style="background: #f2f2f2;">----- 原始邮件 -----<br>发件人：&lt;phantom0506@sina.com&gt;<br>收件人："phantom0506" &lt;phantom0506@sina.com&gt;<br>主题：（无主题）<br>日期：2016年09月27日 12点57分<br></div><br>你好啊啊啊啊啊啊啊啊啊飒飒大师的<p> </p></div>''')
# yk.close()
#

# import wx
# class MyFrame(wx.Frame):
#     def __init__(self, parent=None, title=u'邮件客户端v1.0'):
#         wx.Frame.__init__(self, parent, -1, title=title)
#         self.panel = wx.Panel(self, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN | wx.FULL_REPAINT_ON_RESIZE)
#
#         #增加一些控件:用户名密码部分，并使用GridBagSizer来管理这些控件
#         self.label1=wx.StaticText(self.panel,-1,label=u'用户名：')
#         self.label2=wx.StaticText(self.panel,-1,label=u'  密码：')
#         self.userText=wx.TextCtrl(self.panel,-1,size=(200,25))
#         self.passText=wx.TextCtrl(self.panel,-1,size=(200,25))
#         self.rempassCheck=wx.CheckBox(self.panel,-1,label=u'记住密码')
#         self.autologCheck=wx.CheckBox(self.panel,-1,label=u'自动登录')
#
#         self.gbsizer1=wx.GridBagSizer(hgap=10, vgap=10)
#         self.gbsizer1.Add(self.label1,pos=(0,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
#         self.gbsizer1.Add(self.userText,pos=(0,1),span=(1,1),flag=wx.EXPAND)
#         self.gbsizer1.Add(self.label2,pos=(1,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
#         self.gbsizer1.Add(self.passText,pos=(1,1),span=(1,1),flag=wx.EXPAND)
#         self.gbsizer1.Add(self.rempassCheck,pos=(2,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
#         self.gbsizer1.Add(self.autologCheck,pos=(2,1),span=(1,1),flag=wx.ALIGN_CENTER|wx.ALIGN_CENTRE_VERTICAL)
#
#         #增加一些控件:服务器设置部分，并使用GridBagSizer来管理这些控件，
#         #然后再使用StaticBoxSizer管理GridBagSizer
#         self.label3=wx.StaticText(self.panel,-1,label=u'地址：')
#         self.label4=wx.StaticText(self.panel,-1,label=u'端口：')
#         self.ipadText=wx.TextCtrl(self.panel,-1,size=(170,25))
#         self.portText=wx.TextCtrl(self.panel,-1,size=(170,25))
#         self.proxyBtn=wx.Button(self.panel,-1,label=u'代理\n设置')
#
#         self.gbsizer2=wx.GridBagSizer(hgap=10,vgap=10)
#         self.gbsizer2.Add(self.label3,pos=(0,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
#         self.gbsizer2.Add(self.ipadText,pos=(0,1),span=(1,1),flag=wx.EXPAND)
#         self.gbsizer2.Add(self.proxyBtn,pos=(0,2),span=(2,1),flag=wx.EXPAND)
#         self.gbsizer2.Add(self.label4,pos=(1,0),span=(1,1),flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
#         self.gbsizer2.Add(self.portText,pos=(1,1),span=(1,1),flag=wx.EXPAND)
#
#         sbox=wx.StaticBox(self.panel,-1,label=u'服务器')
#         self.sbsizer=wx.StaticBoxSizer(sbox,wx.VERTICAL)
#         self.sbsizer.Add(self.gbsizer2,proportion=0,flag=wx.EXPAND,border=10)
#
#         #增加一些控件:最下方的按钮，并使用水平方向的BoxSizer来管理这些控件
#         self.setserverBtn=wx.Button(self.panel,-1,label=u'服务器设置↓')
#         self.loginBtn=wx.Button(self.panel,-1,label=u'登录')
#         self.cancelBtn=wx.Button(self.panel,-1,label=u'取消')
#
#         self.bsizer=wx.BoxSizer(wx.HORIZONTAL)
#         self.bsizer.Add(self.setserverBtn,1,flag=wx.EXPAND)
#         self.bsizer.Add(self.loginBtn)
#         self.bsizer.Add(self.cancelBtn)
#
#         #给"服务器设置"按钮绑定事件处理器
#         self.Bind(wx.EVT_BUTTON, self.OnTouch, self.setserverBtn)
#
#         #增加BoxSizer,管理用户名密码部分的gbsizer1，
#         #服务器设置部分的sbsizer，以及最下方的bsizer
#         self.sizer = wx.BoxSizer(wx.VERTICAL)
#         self.sizer.Add(self.gbsizer1, 0, wx.EXPAND, 20)
#         self.sizer.Add(self.sbsizer, 0, wx.EXPAND, 20)
#         self.sizer.Add(self.bsizer, 0, wx.EXPAND, 20)
#         self.isShown = False    #用这个变量指示当前是否已将控件隐藏
#         self.sizer.Hide(self.sbsizer)    #将控件隐藏
#         self.SetClientSize((330,118))    #更改面板尺寸
#
#         self.panel.SetSizerAndFit(self.sizer)
#         self.sizer.SetSizeHints(self.panel)
#
#     def OnTouch(self, event):
#         if self.isShown:    #如果当前控件已显示
#             self.setserverBtn.SetLabel(u'服务器设置↓')    #更新按钮标签
#             self.sizer.Hide(self.sbsizer)    #隐藏服务器设置部分
#             self.isShown = False    #服务器设置部分当前已隐藏
#             self.SetClientSize((330,118))    #更新面板尺寸
#         else:
#             self.sizer.Show(self.sbsizer)    #如果当前控件已隐藏
#             self.setserverBtn.SetLabel(u'服务器设置↑')    #更新按钮标签
#             self.isShown = True    #服务器设置部分当前已显示
#             self.SetClientSize((330,200))    #更新面板尺寸
#         self.sizer.Layout()    #关键所在，强制sizer重新计算并布局sizer中的控件
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
    登录窗口
    """

    def __init__(self, parent, id, title, size):
        '初始化，添加控件并绑定事件'
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
        '登录处理'
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
        '显示错误信息对话框'
        dialog = wx.Dialog(self, title = title, size = size)
        dialog.Center()
        wx.StaticText(dialog, label = content)
        dialog.ShowModal()

class ChatFrame(wx.Frame):
    """
    聊天窗口
    """

    def __init__(self, parent, id, title, size):
        '初始化，添加控件并绑定事件'
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
        '发送消息'
        message = str(self.message.GetLineText(0)).strip()
        if message != '':
            con.write('say ' + message + '\n')
            self.message.Clear()

    def lookUsers(self, event):
        '查看当前在线用户'
        con.write('look\n')

    def close(self, event):
        '关闭窗口'
    	con.write('logout\n')
    	con.close()
    	self.Close()

    def receive(self):
        '接受服务器的消息'
        while True:
        	sleep(0.6)
        	result = con.read_very_eager()
        	if result != '':
        		self.chatFrame.AppendText(result)

'程序运行'
if __name__ == '__main__':
    app = wx.App()
    con = telnetlib.Telnet()
    LoginFrame(None, -1, title = "Login", size = (280, 200))
    app.MainLoop()