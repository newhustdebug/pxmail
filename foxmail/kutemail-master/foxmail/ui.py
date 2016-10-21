# -*- coding:utf-8 -*-
import os
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import QThread
import win32api
import smtplib
from email.mime.text import MIMEText
from .mail import MailCache
from .mail import MailReceive
import multiprocessing
# from threading import Thread


cache_path='cache'
# global username,password

def ui_path(filename):
    basepath = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(basepath, 'ui', filename)

class ComposeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ComposeWindow, self).__init__()
        uic.loadUi(ui_path('composewindow.ui'), self)
    
    def onSend(self):
        message = MIMEText(self.textEdit.toPlainText(), 'plain', 'utf-8')
        message['Subject'] = self.txtsubject.text()
        receivers=self.txtreceiver.text()
        message['from'] = username
        try:
            smtp_backend = smtplib.SMTP()
            smtp_backend.connect(smtphost, smtpport)    # 25 为 SMTP 端口号
            if smtpssl:
                smtp_backend.starttls()
            smtp_backend.login(username,password)
        except:
            win32api.MessageBox(0, u'smtp登陆失败', 'warning')
            return
        try:
            smtp_backend.sendmail(username, receivers, message.as_string())
        except:
            win32api.MessageBox(0, u'邮件发送失败', 'warning')
            return
        win32api.MessageBox(0, u'邮件发送成功', 'warning')
        self.close()
    def onAttachment(self):
        self.close()



class AccountDialog(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(AccountDialog, self).__init__()
        uic.loadUi(ui_path('accountdialog.ui'), self)
        self.hideManualSet()
    def hideManualSet(self):
        self.ReturnButton.hide()
        self.checkSSLpop.hide()
        self.poplabel.hide()
        self.popportEdit.hide()
        self.popportlabel.hide()
        self.txtpopserver.hide()
        self.checkSSLsmtp.hide()
        self.smtplabel.hide()
        self.smtpportEdit.hide()
        self.smtpportlabel.hide()
        self.txtsmtpserver.hide()
        self.SetButton.show()

    def showManualSet(self):
        self.ReturnButton.show()
        self.checkSSLpop.show()
        self.poplabel.show()
        self.popportEdit.show()
        self.popportlabel.show()
        self.txtpopserver.show()
        self.checkSSLsmtp.show()
        self.smtplabel.show()
        self.smtpportEdit.show()
        self.smtpportlabel.show()
        self.txtsmtpserver.show()
        self.SetButton.hide()
        self.popportEdit.setText("110")
        self.smtpportEdit.setText("25")

    def onLogin(self):
        global username,password,pophost,smtphost,popport,smtpport,popssl,smtpssl
        username=self.txtuser.text()
        password=self.txtpassword.text()
        popport='110'
        smtpport='25'
        popssl=False
        smtpssl=False
        if not (username and password):
            win32api.MessageBox(0, u'请输入用户名密码', 'warning')
        else:
            try:
                pophost='pop.'+username.split('@')[1]
                smtphost='smtp.'+username.split('@')[1]
            except:
                win32api.MessageBox(0, u'请输入格式正确的用户名', 'warning')
                return
            if self.txtpopserver.text():
                pophost=self.txtpopserver.text()
            if self.txtsmtpserver.text():
                smtphost=self.txtsmtpserver.text()
            if self.popportEdit.text():
                popport=self.popportEdit.text()
            if self.smtpportEdit.text():
                smtpport=self.smtpportEdit.text()
            if self.checkSSLpop.checkState():
                popssl=True
            if self.checkSSLsmtp.checkState():
                smtpssl=True
            try:
                self.mailreceive = MailReceive(popport,pophost, username, password,popssl)
            except:
                win32api.MessageBox(0, u'登陆失败', 'warning')
                return
            self.mainwindow = MainWindow(self.mailreceive)
            self.mainwindow.show()
            self.close()

    def onCancel(self):
        self.close()


class MainWindow(QtWidgets.QMainWindow):
    mail_account = None
    config = None
    folders = []
    emails = []
    
    def __init__(self,mailreceive):
        super(MainWindow, self).__init__()
        uic.loadUi(ui_path('mainwindow.ui'), self)
        self.mailreceive=mailreceive
        self.cache = MailCache(cache_path, self.mailreceive)
        

    def advanceSlider(self):
        self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)
    
    def onComposeMail(self):
        self.compose = ComposeWindow()
        self.compose.show()
    
    def onRefresh(self):
        win32api.MessageBox(0, u'该功能尚在开发中~~~~~~~', 'warning')
        # self.statusbar.showMessage("Refreshing...")
        # self.folders = self.mail_account.list_folders()
        # self.statusbar.showMessage("")
        # self.refreshTreeView()

    def onContactList(self):
        win32api.MessageBox(0, u'该功能尚在开发中~~~~~~~', 'warning')
        pass

    def onSearch(self):
        win32api.MessageBox(0, u'该功能尚在开发中~~~~~~~', 'warning')
        pass

    def onReply(self):
        win32api.MessageBox(0, u'该功能尚在开发中~~~~~~~', 'warning')
        pass

    def onForward(self):
        win32api.MessageBox(0, u'该功能尚在开发中~~~~~~~', 'warning')
        pass

    def onDelete(self):
        win32api.MessageBox(0, u'该功能尚在开发中~~~~~~~', 'warning')
        pass

    def onFolderSelected(self, folder):
        txt = self.treeMailWidget.currentItem().text(0)
        if txt ==u"收件夹":
            folder_path = self._folder_to_path(folder).strip('/')                                      #存放文件的路径
            self.emails = self.cache.list_mail(folder_path,False)
            subjects=[]
            for email in self.emails:
                subject = self.mailreceive.decode_str(email.get('subject'))
                subjects.append(subject)
            self.listEmails.clear()
            self.listEmails.addItems(subjects)
        else:
            win32api.MessageBox(0, u'该功能尚在开发中~~~~~~~', 'warning')
    
    def onMailSelected(self, item):
        index = item.listWidget().row(item)                                   #选中邮件的第几行
        email = self.emails[index]
        document = QtGui.QTextDocument()

        info=self.mailreceive.get_info(email)
        if info["content"] != '':
            document.setPlainText(info["content"])                          #显示纯文本
        elif info["html"] != '':
            document.setHtml(info["html"])                                  #显示html文本
        
        self.emailPreview.setDocument(document)                             #显示在文本框中
    
    # def refreshTreeView(self):
    #     items = self._makeFolderTree(self.folders)
    #     self.treeMailWidget.insertTopLevelItems(0, items)
        
    # def _makeFolderTree(self, folders, parent=None):
    #     items = [];
    #     for folder in folders:
    #         if parent != None:
    #             folder_item = QtWidgets.QTreeWidgetItem(parent, [folder[0]], 0)
    #         else:
    #             folder_item = QtWidgets.QTreeWidgetItem([folder[0]], 0)
    #
    #         icon = QtGui.QIcon.fromTheme('folder-mail')
    #         if folder[0].lower() == 'inbox':
    #             icon = QtGui.QIcon.fromTheme('mail-folder-inbox')
    #         elif folder[0].lower() == 'junk' or folder[0].lower() == 'spam':
    #             icon = QtGui.QIcon.fromTheme('mail-mark-junk')
    #         elif folder[0].lower() == 'trash':
    #             icon = QtGui.QIcon.fromTheme('user-trash')
    #         folder_item.setIcon(0, icon)
    #         if len(folder[1]) > 0:
    #             folder_item.addChildren(self._makeFolderTree(folder[1], parent=folder_item))
    #         items.append(folder_item)
    #     return items
    #
    def _folder_to_path(self, folder):
        text = ''
        if folder.parent() is not None:
            text = self._folder_to_path(folder.parent())
        text += '/' + folder.text(0)
        return text
    
    # def showEvent(self, event):
    #     info = AccountDialog.getAccountDetails()
    #     if not info["accepted"]:
    #         exit()
    #     if not (info["username"] and info["password"]):
    #         win32api.MessageBox(0, u'请输入用户名密码', 'warning')
    #         self.showEvent(event)
    #     else:
    #         print (info)
    #         self.pophost='pop.'+info["username"].split('@')[1]
    #
    #         self.mailreceive = MailReceive(self.pophost, info['username'], info['password'])
    #         self.cache = MailCache(cache_path, self.mailreceive)
    #         # self.onRefresh()
        
        
