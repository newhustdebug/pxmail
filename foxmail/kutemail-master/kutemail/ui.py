import os
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
import quopri
import win32api
from .mail import MailLogin
from .mail import MailCache
from .mail import MailReceive

from pprint import pprint
cache_path='cache'

def ui_path(filename):
    basepath = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(basepath, 'ui', filename)

class ComposeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ComposeWindow, self).__init__()
        uic.loadUi(ui_path('composewindow.ui'), self)
    
    def onSend(self):
        self.close()

    def onAttachment(self):
        self.close()

class AccountDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(AccountDialog, self).__init__(parent)
        uic.loadUi(ui_path('accountdialog.ui'), self)
    
    @staticmethod
    def getAccountDetails(username='', password='', parent=None):
        dialog = AccountDialog(parent)
        dialog.txtUserName.setText(username)
        result = dialog.exec_()
        return {
            "accepted": result == QtWidgets.QDialog.Accepted,
            "username": dialog.txtUserName.text(),
            "password": dialog.txtPassword.text()
        }

class MainWindow(QtWidgets.QMainWindow):
    mail_account = None
    config = None
    folders = []
    emails = []
    
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(ui_path('mainwindow.ui'), self)
        self.statusbar.showMessage("Refreshing...",100000000)
        

    def advanceSlider(self):
        self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)
    
    def onComposeMail(self):
        self.compose = ComposeWindow()
        self.compose.show()
    
    def onRefresh(self):
        self.statusbar.showMessage("Refreshing...")
        self.folders = self.mail_account.list_folders()
        self.statusbar.showMessage("")
        self.refreshTreeView()

    def onContactList(self):
        pass

    def onSearch(self):
        pass

    def onReply(self):
        pass

    def onForward(self):
        pass

    def onDelete(self):
        pass





    def onFolderSelected(self, folder):

        folder_path = self._folder_to_path(folder).strip('/')                                      #存放文件的路径
        self.emails = self.cache.list_mail(folder_path,False)
        subjects=[]
        for email in self.emails:
            subject = self.mailreceive.decode_str(email.get('subject'))
            subjects.append(subject)

        # print (folder_path)
        # for i in range(10):
        #     subjects.append(str(folder))
        self.listEmails.clear()
        self.listEmails.addItems(subjects)
    
    def onMailSelected(self, item):
        index = item.listWidget().row(item)                 #选中邮件的第几行

        email = self.emails[index]
        document = QtGui.QTextDocument()
        if email.is_multipart():
            html = None
            plain = None
            for payload in email.walk():
                if payload.get_content_type() == 'text/html' and html == None:
                    html = payload.get_payload(decode=True).decode("utf-8")
                if payload.get_content_type() == 'text/plain' and plain == None:
                    plain = payload.get_payload(decode=True).decode("utf-8")
                if plain != None and html != None:
                    break;
            
            if html != None:
                document.setHtml(html)
            if "DOCTYPE" in plain or "doctype" in plain:
                document.setHtml(plain)
            else:
                document.setPlainText(plain)
        else:
            plain = email.get_payload(decode=True).decode("utf-8")
            if "DOCTYPE" in plain or "doctype" in plain:
                document.setHtml(plain)
            else:
                document.setPlainText(plain)
        
        self.emailPreview.setDocument(document)
    
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
    
    def showEvent(self, event):
        info = AccountDialog.getAccountDetails()
        if not info["accepted"]:
            exit()
        if not (info["username"] and info["password"]):
            win32api.MessageBox(0, u'请输入用户名密码', 'warning')
            self.showEvent(event)
        else:
            print (info)
            self.mail_account = MailLogin(info)
            self.pophost='pop.'+info["username"].split('@')[1]

            self.mailreceive = MailReceive(self.pophost, info['username'], info['password'])
            self.cache = MailCache(cache_path, self.mailreceive)
            # self.onRefresh()
        
        
