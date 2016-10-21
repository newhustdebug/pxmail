#-*-coding:utf-8-*-

import wx
import win32api
import threading
import smtplib
from email.mime.text import MIMEText

mail_host="smtp.sina.com"                       #设置服务器
mail_user="phantom0506@sina.com"                 #用户名
mail_pass="txyb123456"                           #口令


'''基于Sizer的控件相对布局'''
class Slave(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title=u'邮件管理客户端v1.0', size=(600, 600))
        self.panel = wx.Panel(self, -1)
        self.lock = threading.Lock()
        self.Centre()



        receiveStatic = wx.StaticText(self.panel, -1, u'           收件人:')                      #静态文字
        subjectStatic = wx.StaticText(self.panel, -1, u'             主题:')

        self.receiversText = wx.TextCtrl(self.panel, -1, u'',size=(200, 25))            #动态文本框
        self.subjectText = wx.TextCtrl(self.panel, -1, u'',size=(200, 25))
        self.writeText = wx.TextCtrl(self.panel, -1, u'',
                                  style=wx.TE_MULTILINE, size=(400, 200))

        self.send = wx.Button(self.panel, label=u'发送')
        self.attachment = wx.Button(self.panel, label=u'附件')

        self.Bind(wx.EVT_BUTTON, self.onSend, self.send)


        #基于GirdBagSizer布局
        self.gridBagSizerAll = wx.GridBagSizer(hgap=14, vgap=14)
        self.gridBagSizerAll.Add(self.send, pos=(0, 0),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(2, 1), border=5)
        self.gridBagSizerAll.Add(self.attachment, pos=(0, 1),
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            span=(2, 1), border=5)

        self.gridBagSizerAll.Add(receiveStatic, pos=(2, 0),
                            flag=wx.ALL | wx.EXPAND,
                            span=(1,1),border=5)
        self.gridBagSizerAll.Add(self.receiversText, pos=(2, 1),
                            flag=wx.ALL | wx.EXPAND,
                            span=(1, 13), border=5)

        self.gridBagSizerAll.Add(subjectStatic, pos=(3, 0),
                            flag=wx.ALL | wx.EXPAND,
                            span=(1,1),border=5)

        self.gridBagSizerAll.Add(self.subjectText, pos=(3, 1),
                            flag=wx.ALL | wx.EXPAND,
                            span=(1, 13), border=5)


        self.gridBagSizerAll.Add(self.writeText, pos=(4, 0),
                            flag=wx.ALL | wx.EXPAND,
                            span=(10, 14), border=5)

        self.panel.SetSizer(self.gridBagSizerAll)


        self.SetSizeHints(800, 500, 1600, 1000)          #设定窗口的最大最小值    (列，行，列，行)
        self.gridBagSizerAll.AddGrowableCol(3, 1)                #列可伸缩
        self.gridBagSizerAll.AddGrowableCol(4, 1)
        self.gridBagSizerAll.AddGrowableCol(5, 1)
        self.gridBagSizerAll.AddGrowableCol(6, 1)
        self.gridBagSizerAll.AddGrowableCol(7, 1)
        self.gridBagSizerAll.AddGrowableCol(8, 1)

        self.gridBagSizerAll.AddGrowableRow(4, 1)                #行可伸缩
        self.gridBagSizerAll.AddGrowableRow(5, 1)
        self.gridBagSizerAll.AddGrowableRow(6, 1)
        self.gridBagSizerAll.Fit(self)

    def onSend(self, event):
        receiversText = self.receiversText.GetValue()
        subjectText = self.subjectText.GetValue()
        writeText = self.writeText.GetValue()
        if not receiversText:
            win32api.MessageBox(0, u'请输入收件人', 'warning')
            return
        if not subjectText:
            win32api.MessageBox(0, u'请输入主题', 'warning')
            return
        if not writeText:
            win32api.MessageBox(0, u'请输入文本内容', 'warning')
            return
        message = MIMEText(writeText, 'plain', 'utf-8')
        message['Subject'] = subjectText
        message['from'] = 'phantom0506@sina.com'
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
            smtpObj.login(mail_user,mail_pass)
            smtpObj.sendmail(mail_user, receiversText, message.as_string())
            win32api.MessageBox(0, u'发送成功', 'warning')
        except smtplib.SMTPException:
            print "Error: 无法发送邮件"



if __name__ == "__main__":
    app = wx.App()
    frame = Slave()
    frame.Show()
    app.MainLoop()
