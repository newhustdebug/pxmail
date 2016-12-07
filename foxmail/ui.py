# -*- coding:utf-8 -*-
import os
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from email import utils
import time
from datetime import datetime
import smtplib
import re
import sys
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mail import *
import parameter as gl
import syntax_pars
from backend import *

APPNAME = 'PxMail v3.0'


class ComposeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ComposeWindow, self).__init__()
        uic.loadUi('ui/composewindow.ui', self)
        self.fileName=''
        self.setupRichText()



        self.send_thread = sendingThread()                               #加载发送线程
        self.send_thread.triggerSuccess.connect(self.onSuccess)
        self.send_thread.triggerFail.connect(self.onFail)
        self.senddialog=SendDialog()

        completer = QtWidgets.QCompleter()                              #文本框自动补全
        self.txtreceiver.setCompleter(completer)
        self.model=QtCore.QStringListModel()
        completer.setModel(self.model)

    def ontextChanged(self):
        getstring=self.txtreceiver.text()
        #从联系人中筛选
        # if not "@" in getstring:
        #     self.model.setStringList([getstring+"@qq.com", getstring+"@sina.com",getstring+"@sina.cn",
        #                 getstring+ "@163.com",getstring+"@126.com", getstring+"@hust.edu.cn"])

    def setupRichText(self):
        pix = QtGui.QPixmap(16, 16)                                     #填充颜色按钮
        pix.fill(Qt.black)
        self.ButtonTextColor.setIcon(QtGui.QIcon(pix))

        db = QtGui.QFontDatabase()                                      #字库里的字体大小
        for size in db.standardSizes():
            self.comboSize.addItem("%s" % (size))
        self.comboSize.setCurrentIndex(                                         #当前字体索引设置为选中文字的大小
                self.comboSize.findText(
                        "%s" % (QtWidgets.QApplication.font().pointSize())))


        self.fontChanged(self.textEdit.font())
        self.colorChanged(self.textEdit.textColor())
        self.alignmentChanged(self.textEdit.alignment())
        # self.textEdit.document().modificationChanged.connect(
        #         self.actionSave.setEnabled)
        # self.textEdit.document().modificationChanged.connect(
        #         self.setWindowModified)
        # self.textEdit.document().undoAvailable.connect(
        #         self.actionUndo.setEnabled)
        # self.textEdit.document().redoAvailable.connect(
        #         self.actionRedo.setEnabled)

    # #当前文字格式改变
    def onCurrentCharFormatChanged(self, format):
        pass
        # self.fontChanged(format.font())
        # self.colorChanged(format.foreground().color())
    #光标位置改变
    def onCursorPositionChanged(self):
        pass
        # self.alignmentChanged(self.textEdit.alignment())
    # def fontChanged(self, font):
    #     self.comboFont.setCurrentIndex(
    #             self.comboFont.findText(QFontInfo(font).family()))
    #     self.comboSize.setCurrentIndex(
    #             self.comboSize.findText("%s" % font.pointSize()))
    #     self.actionTextBold.setChecked(font.bold())
    #     self.actionTextItalic.setChecked(font.italic())
    #     self.actionTextUnderline.setChecked(font.underline())

    def onTextBold(self):
        pass
    def onTextItalic(self):
        pass
    def onTextUnderline(self):
        pass
    def onTextColor(self):
        pass
    def onTextFamily(self):
        pass
    def onTextSize(self):
        pass
    def onTextAlign(self,button):
        if button == self.ButtonAlignLeft:
            self.textEdit.setAlignment(Qt.AlignLeft | Qt.AlignAbsolute)
        elif button == self.ButtonAlignCenter:
            self.textEdit.setAlignment(Qt.AlignHCenter)
        elif button == self.ButtonAlignRight:
            self.textEdit.setAlignment(Qt.AlignRight | Qt.AlignAbsolute)
        elif button == self.ButtonAlignJustify:
            self.textEdit.setAlignment(Qt.AlignJustify)
    def fontChanged(self, font):
        self.comboFont.setCurrentIndex(
                self.comboFont.findText(QtGui.QFontInfo(font).family()))
        self.comboSize.setCurrentIndex(
                self.comboSize.findText("%s" % font.pointSize()))
        self.actionTextBold.setChecked(font.bold())
        self.actionTextItalic.setChecked(font.italic())
        self.actionTextUnderline.setChecked(font.underline())


    #发送邮件
    def onSend(self):
        if not self.txtreceiver.text():
            QtWidgets.QMessageBox.warning(self, APPNAME,"请填写收信人" )
            return
        if not self.txtsubject.text():
            QtWidgets.QMessageBox.warning(self, APPNAME,"请填邮件主题" )
            return
        if not self.textEdit.toPlainText():
            QtWidgets.QMessageBox.warning(self, APPNAME,"请填写邮件正文" )
            return
        if self.fileName:                                                    #如果有附件
            gl.message = MIMEMultipart('related')
            gl.message['Subject'] = self.txtsubject.text()
            gl.message.attach(MIMEText(self.textEdit.toPlainText(), 'plain', 'utf-8'))
            gl.message['from'] = gl.username
            gl.message['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')
            #构造附件
            att = MIMEText(open(self.fileName, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="1.jpg"'
            gl.message.attach(att)
        else:
            gl.message = MIMEText(self.textEdit.toPlainText(), 'plain', 'utf-8')
            gl.message['Subject'] = self.txtsubject.text()
            gl.message['from'] = gl.username
            gl.message['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')
        gl.receivers=self.txtreceiver.text().split(';')
        self.statusBar.showMessage("Sending...")
        self.send_thread.start()
        self.senddialog.exec_()
    #添加附件
    def onAttachment(self):

        self.fileName, filetype = QFileDialog.getOpenFileName(self,
                                    "选取文件",
                                    "C:/",
                                    "All Files (*);;Text Files (*.txt)")   #设置文件扩展名过滤,注意用双分号间隔

        self.statusBar.showMessage(str("附件："+self.fileName))

    def onSuccess(self):
        QtWidgets.QMessageBox.warning(self, APPNAME,"邮件发送成功" )
        self.senddialog.close()
        self.close()

    def onFail(self):
        QtWidgets.QMessageBox.warning(self, APPNAME,gl.error )
        self.senddialog.close()

class AccountDialog(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(AccountDialog, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)  #去边框
        uic.loadUi('ui/accountdialog.ui', self)
        self.popportEdit.setText("110")
        self.smtpportEdit.setText("25")

        self.txtuser.editingFinished.connect(self.txtuserEdited)        #文本编辑完成自动显示服务器

        completer = QtWidgets.QCompleter()                              #文本框自动补全
        self.txtuser.setCompleter(completer)
        self.model=QtCore.QStringListModel()
        completer.setModel(self.model)



        self.in_thread = In()
        self.in_thread.trigger.connect(self.trans)
        self.trans_thread = Trans()                                     #文字淡入淡出
        self.trans_thread.trigger.connect(self.trans)
        self.trans()

        self.closefilter = Filter()                                                 #关闭
        self.labelclose.installEventFilter(self.closefilter)
        self.closefilter.trigger4.connect(self.onCancel)

        self.minfilter = Filter()                                                 #最小化
        self.labelmin.installEventFilter(self.minfilter)
        self.minfilter.trigger4.connect(self.onMinimum)
        desktop = QtWidgets.QApplication.desktop()
        self.dwidth = desktop.width()    # 获取桌面宽度
        self.dheight = desktop.height()    # 获取桌面高度
        self.globalPos = None


        self.hideManualSet()
        self.loading_thread = loadingThread()                               #加载登陆线程
        self.loading_thread.trigger1.connect(self.successed)
        self.loading_thread.trigger2.connect(self.failed)

        #调试方便
        self.txtuser.setText('phantom0506@sina.com')
        self.txtpassword.setText('txyb123456')
    #隐藏手动设置
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
    #展开手动设置
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
    #设置回车快捷键
    def keyPressEvent(self, event):
        if event.key() ==Qt.Key_Enter or event.key() ==Qt.Key_Return:
            self.onLogin()
    #文本编辑完成自动显示服务器文本
    def txtuserEdited(self):
        try:
            if self.txtuser.text().split('@')[1]=="hust.edu.cn":
                pophost='mail.'+self.txtuser.text().split('@')[1]
                smtphost='mail.'+self.txtuser.text().split('@')[1]
            else:
                pophost='pop.'+self.txtuser.text().split('@')[1]
                smtphost='smtp.'+self.txtuser.text().split('@')[1]
        except:
            return
        self.txtpopserver.setText(pophost)
        self.txtsmtpserver.setText(smtphost)



    #登陆成功
    def successed(self):
        self.mainwindow = MainWindow()
        self.mainwindow.show()
        self.close()
    #登陆失败
    def failed(self):
        self.label_prompt.setText(u'<p align=right style="font-family:Microsoft YaHei;font:13px;'
			u'color:#DE5347">服务器连接失败！%s</p>'%gl.error)
        gl.new_trans = True
        time.sleep(0.01)
        self.trans_thread.start()

        self.SetButton.setEnabled(True)                        #按钮可用
        self.ReturnButton.setEnabled(True)
        self.cancelButton.setEnabled(True)
        self.loginButton.setEnabled(True)

    #文本框自动补全
    def ontextChanged(self):
        getstring=self.txtuser.text()
        if not "@" in getstring:
            self.model.setStringList([getstring+"@qq.com", getstring+"@sina.com",getstring+"@sina.cn",
                        getstring+ "@163.com",getstring+"@126.com", getstring+"@hust.edu.cn"])
    #登陆邮箱
    def onLogin(self):
        gl.username=self.txtuser.text().strip()
        gl.password=self.txtpassword.text()
        gl.popport='110'
        gl.smtpport='25'
        gl.popssl=False
        gl.smtpssl=False
        if not (gl.username and gl.password):

            self.label_prompt.setText(u'<p align=right style="font-family:Microsoft YaHei;font:13px;'
                u'color:#4C8BF5">请完整填写用户名密码信息</p>')
            gl.new_trans = True
            time.sleep(0.01)
            self.in_thread.start()

        else:
            try:
                if gl.username.split('@')[1]=="hust.edu.cn":
                    gl.pophost='mail.'+gl.username.split('@')[1]
                    gl.smtphost='mail.'+gl.username.split('@')[1]
                else:
                    gl.pophost='pop.'+gl.username.split('@')[1]
                    gl.smtphost='smtp.'+gl.username.split('@')[1]
            except:
                self.label_prompt.setText(u'<p align=right style="font-family:Microsoft YaHei;font:13px;'
                    u'color:#DE5347">请输入格式正确的用户名！</p>')
                gl.new_trans = True
                time.sleep(0.01)
                self.trans_thread.start()
                return
            if self.txtpopserver.text():
                gl.pophost=self.txtpopserver.text()
            if self.txtsmtpserver.text():
                gl.smtphost=self.txtsmtpserver.text()
            if self.popportEdit.text():
                gl.popport=self.popportEdit.text()
            if self.smtpportEdit.text():
                gl.smtpport=self.smtpportEdit.text()
            if self.checkSSLpop.checkState():
                gl.popssl=True
            if self.checkSSLsmtp.checkState():
                gl.smtpssl=True
            if gl.username.split('@')[1]=="qq.com":
                gl.popport='995'
                gl.smtpport='465'
                gl.popssl=True
                gl.smtpssl=True
            self.label_prompt.setText(u'<p align=right style="font-family:Microsoft YaHei;font:13px;'
			u'color:#4C8BF5">正在连接邮箱服务器...</p>')
            gl.new_trans = True
            time.sleep(0.01)
            self.in_thread.start()
            self.loading_thread.start()                             #登陆线程


            self.SetButton.setEnabled(False)                        #按钮不可用
            self.ReturnButton.setEnabled(False)
            self.cancelButton.setEnabled(False)
            self.loginButton.setEnabled(False)

    #关闭窗口
    def onCancel(self):
        self.close()
    def onMinimum(self):
        self.showMinimized()

    # 鼠标按下事件
    def mousePressEvent(self, event):
        # 鼠标点击事件
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.globalPos = event.globalPos() - self.dragPosition
            self.move(self.globalPos)
            event.accept()

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        if self.y() < 1:    # 上边
            self.move(self.x(), 1 - self.height())
        elif self.x() < 1:    # 左边
            self.move(1 - self.width(), self.y())
        elif self.x() > (self.dwidth - self.width()):    # 右边
            self.move(self.dwidth - 1 , self.y())
        event.accept()



    #SSL按钮事件
    def onSSLpop(self):
        if self.checkSSLpop.isChecked():
            self.popportEdit.setText("995")
        else:
            self.popportEdit.setText("110")
    #SSL按钮事件
    def onSSLsmtp(self):
        if self.checkSSLsmtp.isChecked():
            self.smtpportEdit.setText("465")
        else:
            self.smtpportEdit.setText("25")

    # def showEvent(self, *args, **kwargs):
    #     splash=QtWidgets.QSplashScreen(QtGui.QPixmap("taiyan.jpg"))             #做启动画面
    #     splash.show()
    #     QtCore.QThread.sleep(5)
    #     splash.hide()

    #改变透明度,提示文字淡入淡出，用于更新画面
    def trans(self):
        self.label_opacity.setStyleSheet(u'QLabel{background:rgba(14, 33, 45, ' + str(gl.opacity) + '%)}')
        self.update()



class MainWindow(QtWidgets.QMainWindow):
    folders = []
    emails = []
    row=0
    lastrow=0
    Ascending=True
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/mainwindow.ui', self)
        with open("ui/myUI.qss","r") as fh:                             #加载qss文件
            self.setStyleSheet(fh.read())
        # self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)     #去边框

        self.receive_thread = receiveThread()                               #加载登陆线程
        self.receive_thread.triggerFinish.connect(self.mailDisplay)
        self.receivedialog=ReceiveDialog()
        self.receive_thread.triggerNumber.connect(self.receivedialog.updateProcess)

        self.btnForward.setEnabled(False)                               #转发功能不可用
        self.btnDelete.setEnabled(False)
        self.btnReply.setEnabled(False)


        self.InitSearchEdit()                                           #初始化搜索框
        self.searchEdit.editingFinished.connect(self.txtsearchEdited)        #文本编辑完成自动显示服务器
        self.search_thread = searchThread()
        self.search_thread.trigger.connect(self.mailDisplay)


        self.comboBox.insertSeparator(3)
        self.comboBox.insertItems(4,["√    升序","      降序"])
        self.listEmails.customContextMenuRequested[QtCore.QPoint].connect(self.listmailMenu)
        # self.highlight = syntax_pars.PythonHighlighter(self.emailPreview.document())

        self.attachdisplay.hide()                                           #隐藏附件标签
        self.attachlabel.hide()

        self.createContextMenu()                                                #为按钮创建菜单

    #Combobox显示
    def OnActivated(self, row):
        if row==4 :
            self.comboBox.setItemText(4,"√    升序")
            self.comboBox.setItemText(5,"      降序")
            self.comboBox.setCurrentText(self.comboBox.itemText(self.lastrow))      #设定现在显示值
            self.Ascending=True
        elif row==5 :
            self.comboBox.setItemText(4,"      升序")
            self.comboBox.setItemText(5,"√    降序")
            self.comboBox.setCurrentText(self.comboBox.itemText(self.lastrow))
            self.Ascending=False
        else:
            self.row=row
            self.lastrow=row

        self.mailDisplay()

    #显示邮件
    def mailDisplay(self):
        index=0
        items=[]
        if self.row==0:                                                 #按时间排序
            year,month,day=datetime.now().timetuple()[0:3]
            date=""
            index=0
            Itemslist=[QtWidgets.QTreeWidgetItem() for i in range(7)]                   #创建七个对象

            Itemslist[0].setText(0,"今天")                                        #建立根节点
            Itemslist[1].setText(0,"这周")
            Itemslist[2].setText(0,"一周前")
            Itemslist[3].setText(0,"两周前")
            Itemslist[4].setText(0,"三周前")
            Itemslist[5].setText(0,"上个月")
            Itemslist[6].setText(0,"更早")
            for email in gl.March_ID:
                info=get_info(email)
                if info["date"]:                                                #从邮件提取日期
                    date=info["date"]
                else:
                    date=info["received"][-31:]
                datetuple=utils.parsedate(date)                                 #发送邮件日期
                if datetuple[0]<year or datetuple[1]<month-1 :
                    childItem = QtWidgets.QTreeWidgetItem(Itemslist[6])
                    childItem.setText(0,info["subject"])
                elif  datetuple[1]==month-1  :
                    childItem = QtWidgets.QTreeWidgetItem(Itemslist[5])
                    childItem.setText(0,info["subject"])
                elif  day==datetuple[2]  :
                    childItem = QtWidgets.QTreeWidgetItem(Itemslist[0])
                    childItem.setText(0,info["subject"])
                elif  day-datetuple[2]>=21  :
                    childItem = QtWidgets.QTreeWidgetItem(Itemslist[4])
                    childItem.setText(0,info["subject"])
                elif  day-datetuple[2]>=14  :
                    childItem = QtWidgets.QTreeWidgetItem(Itemslist[3])
                    childItem.setText(0,info["subject"])
                elif  day-datetuple[2]>=7  :
                    childItem = QtWidgets.QTreeWidgetItem(Itemslist[2])
                    childItem.setText(0,info["subject"])
                else:
                    childItem = QtWidgets.QTreeWidgetItem(Itemslist[1])
                    childItem.setText(0,info["subject"])
                childItem.setData(0,1,index)
                index=index+1

            for i in range(7):                                                #将没有邮件的根节点去除
                if Itemslist[i].child(0):
                    items.append(Itemslist[i])
            if not self.Ascending:
                items=reversed(items)
        #按收信人排序
        elif self.row==1:
            for email in gl.March_ID:
                info=get_info(email)
                senders=map(lambda x: x.text(0), items)                          #提取出当前所有邮件的收件人


                if info["addr"] in senders:                                     #如果已存在该联系人，找到其根节点作为父亲
                    for item in items:
                        if info["addr"] == item.text(0):
                            self.parent=item
                    child= QtWidgets.QTreeWidgetItem(self.parent)
                    child.setText(0,info["subject"])
                    child.setData(0,1,index)
                else:                                                       #否则就创建根节点，并加入儿子
                    parent= QtWidgets.QTreeWidgetItem()
                    parent.setText(0,info["addr"])
                    items.append(parent)
                    child= QtWidgets.QTreeWidgetItem(parent)
                    child.setText(0,info["subject"])
                    child.setData(0,1,index)
                index=index+1                                                        #reverse=True  逆序排序
            items=sorted(items, key=lambda item : item.text(0),reverse=self.Ascending)       #按照每个节点的日期作为关键字排序

        #按主题排序
        elif self.row==2:
            for email in gl.March_ID:
                info=get_info(email)
                senders=map(lambda x: x.text(0), items)                          #提取出当前所有邮件的收件人


                if info["subject"] in senders:                        #如果已存在该联系人，找到其根节点作为父亲
                    for item in items:
                        if info["subject"] == item.text(0):
                            self.parent=item
                    child= QtWidgets.QTreeWidgetItem(self.parent)
                    child.setText(0,info["subject"])
                    child.setData(0,1,index)
                else:                                                       #否则就创建根节点，并加入儿子
                    parent= QtWidgets.QTreeWidgetItem()
                    parent.setText(0,info["subject"])
                    items.append(parent)
                    child= QtWidgets.QTreeWidgetItem(parent)
                    child.setText(0,info["subject"])
                    child.setData(0,1,index)
                index=index+1                                                         #reverse=True  逆序排序
            items=sorted(items, key=lambda item : item.text(0),reverse=self.Ascending)       #按照每个节点的主题作为关键字排序

        self.listEmails.clear()                                         #清空
        self.listEmails.insertTopLevelItems(0, items)                   #添加项目
        self.listEmails.expandAll()                                     #全部展开
        self.receivedialog.close()
        self.statusbar.showMessage("")
    #创建附件按钮菜单
    def createContextMenu(self):
        self.attachdisplay.customContextMenuRequested.connect(self.showContextMenu)
        # 创建QMenu
        self.contextMenu = QtWidgets.QMenu(self)
        self.actionA = self.contextMenu.addAction(QtGui.QIcon("images/0.png"),u'|  默认程序打开')
        self.actionB = self.contextMenu.addAction(QtGui.QIcon("images/0.png"),u'|  另存为')
        # #添加二级菜单
        # self.second = self.contextMenu.addMenu(QtGui.QIcon("images/0.png"),u"|  打开方式")
        # self.actionD = self.second.addAction(QtGui.QIcon("images/0.png"),u'|  选择默认程序')

        self.actionA.triggered.connect(self.openFile)
        self.actionB.triggered.connect(self.save_binary_file)

    #显示附件按钮菜单
    def showContextMenu(self):
        self.contextMenu.exec_(QtGui.QCursor.pos()) #在鼠标位置显示
    #保存为二进制文件
    def save_binary_file(self):
        filename, filetype = QFileDialog.getSaveFileName(self,"另存为",
                                        os.path.join("c：/", self.filename),'All Files (*)' )

        if not filename:
            return
        qFile = QtCore.QFile(filename)
        if not qFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.ReadWrite):
            QtWidgets.QMessageBox.warning(self, APPNAME,
                    "无法创建文件: %s\n%s." % (filename, qFile.errorString()))
            return
        with open(filename, 'wb') as file_handle:
            QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)
            file_handle.write(gl.attachment)
            QtWidgets.QApplication.restoreOverrideCursor()
        self.statusBar().showMessage("Saved '%s'" % filename, 2000)



    def onComposeMail(self):
        self.compose = ComposeWindow()
        self.compose.show()
    
    def onRefresh(self):
        gl.force_refresh=True
        refresh_mail()
        self.statusbar.showMessage("Refreshing...")
        self.receive_thread.start()
        self.receivedialog.reset()
        self.receivedialog.exec_()

    def onContactList(self):
        items=[]
        folder_item= QtWidgets.QTreeWidgetItem()
        folder_item.setText(0,'root')
        folder_item.setData(0,1,23)
        items.insert(0,folder_item)

        print(folder_item.child(0))

        child2 = QtWidgets.QTreeWidgetItem(folder_item)
        child2.setText(0,'child')
        print(folder_item.child(0))
        folder2_item = QtWidgets.QTreeWidgetItem()
        folder2_item.setText(0,'hahahaha')

        # items.insert(0,folder2_item)                                #插入

        self.listEmails.clear()                                         #清空
        self.listEmails.insertTopLevelItems(0, items)                   #添加项目
        self.listEmails.expandAll()                                     #全部展开

    #初始化搜索框
    def InitSearchEdit(self):
        self.linefilter = Filter()                                                 #安装行编辑器事件过滤器
        self.searchEdit.installEventFilter(self.linefilter)
        self.linefilter.trigger1.connect(self.FocusIn)
        self.linefilter.trigger2.connect(self.FocusOut)

        self.labelfilter = Filter()                                                 #安装标签事件过滤器
        self.Xlabel.installEventFilter(self.labelfilter)
        self.labelfilter.trigger3.connect(self.cleartxt)

    def FocusIn(self):
        self.Xlabel.setText("x")

    def FocusOut(self):
        if not self.searchEdit.text():

            self.Xlabel.setText("")
    def txtsearchEdited(self):
        if self.searchEdit.text():
            gl.string=self.searchEdit.text()

            # self.search_thread.start()
            QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)          #鼠标设置成忙等待状态
            gl.March_ID=[]                                                  #匹配符合条件的邮件
            for email in gl.emails:
                info=get_info(email)
                if (gl.string in info["subject"]) or (gl.string in info["content"]) or (gl.string in info["addr"]):
                    gl.March_ID.append(email)
                    self.data=info["subject"]+info["content"]+info["addr"]
                    pattern = re.compile(gl.string)
                    dataMatched = re.findall(pattern, self.data)                        #匹配所有关键字，背景高亮
                    # self.highlight.setHighlightData(dataMatched)
                    # self.highlight.rehighlight()
            self.mailDisplay()
            QtWidgets.QApplication.restoreOverrideCursor()

        else:
            gl.March_ID=gl.emails
            self.mailDisplay()
    #清空搜索框
    def cleartxt(self):
        self.searchEdit.clear()
        gl.March_ID=gl.emails
        self.mailDisplay()

    #回复功能
    def onReply(self):
        email = gl.March_ID[self.index]
        document = QtGui.QTextDocument()
        info=get_info(email)
        splitline="----------------------------------------"
        if info["content"] != '':
            document.setPlainText('\n\n\n'+splitline+'\n'+info["content"])                          #显示纯文本
        elif info["html"] != '':
            document.setHtml('\n\n\n'+splitline+'\n'+info["html"])                                  #显示html文本

        self.compose = ComposeWindow()
        self.compose.show()
        self.compose.txtsubject.setText('回复：'+info["subject"])                    #显示主题，发信人，日期
        self.compose.txtreceiver.setText(info["addr"])
        self.compose.textEdit.setDocument(document)
        self.compose.textEdit.setFocus()



    #转发功能
    def onForward(self):
        email = gl.March_ID[self.index]
        document = QtGui.QTextDocument()
        info=get_info(email)
        splitline="----------------------------------------"
        if info["content"] != '':
            document.setPlainText('\n\n\n'+splitline+'\n'+info["content"])                          #显示纯文本
        elif info["html"] != '':
            document.setHtml('\n\n\n'+splitline+'\n'+info["html"])                                  #显示html文本

        self.compose = ComposeWindow()
        self.compose.show()
        self.compose.txtsubject.setText('转发：'+info["subject"])                    #显示主题，发信人，日期
        self.compose.textEdit.setDocument(document)
        self.compose.textEdit.setFocus()

    def onDelete(self):
        QtWidgets.QMessageBox.warning(self, APPNAME,"该功能尚在开发中~~~~~~~" )
        pass

    def onFolderSelected(self, folder):                                                 #folder:选中的目录
        txt = self.treeMailWidget.currentItem().text(0)
        if txt ==u"收件夹":
            gl.folder_path = self._folder_to_path(folder).strip('/')                                      #存放文件的路径
            self.receive_thread.start()
            self.receivedialog.reset()
            self.receivedialog.exec_()
        else:
            QtWidgets.QMessageBox.warning(self, APPNAME,"该功能尚在开发中~~~~~~~" )


    def onMailSelected(self, item):
        if  item.treeWidget().currentItem().parent():                        #假如有父亲节点，则选中相应邮件
            self.btnForward.setEnabled(True)                               #转发功能可用
            self.btnDelete.setEnabled(True)
            self.btnReply.setEnabled(True)
            self.index=item.treeWidget().currentItem().data(0,1)               #将Item中的行号提取出来
            email = gl.March_ID[self.index]

            info=get_info(email)
            try:

                if info["content"] != '':                                    #显示纯文本
                    self.emailPreview.setHtml(info["content"].replace('\n','<br>'))
                elif info["html"] != '':
                    self.emailPreview.setHtml(info["html"])                 #显示html文本


                if info["filename"]:
                    self.filename=info["filename"]
                    self.attachdisplay.setText(self.filename)
                    self.attachdisplay.show()
                    self.attachlabel.show()
                else:
                    self.attachdisplay.hide()
                    self.attachlabel.hide()

                    # self.emailPreview.append(str("<html><head/><body><p><a href=\"https://www.baidu.com/\"><span style=\" text-decoration: underline; color:#0000ff;\">注册账号</span></a></p></body></html>"))
                    # self.emailPreview.append(str("<html><p><a href=\"%1\">进入列表的设置页面</a></p></html>").arg(path.left(path.lastIndexOf('/'))))
                self.subdisplay.setText(info["subject"])                    #显示主题，发信人，日期
                self.fromdisplay.setText(info["addr"])

                date=""
                if info["date"]:                                                #从邮件提取日期
                    date=info["date"]
                else:
                    date=info["received"][-31:]
                datetuple=utils.parsedate(date)
                if(len(str(datetuple[4]))==1):                                  #如果分钟是个位数，前面填充一个0
                    self.datestring=str(datetuple[0])+'-'+str(datetuple[1])+'-'+str(datetuple[2])\
                          +' '+str(datetuple[3])+':0'+str(datetuple[4])
                else:
                    self.datestring=str(datetuple[0])+'-'+str(datetuple[1])+'-'+str(datetuple[2])\
                              +' '+str(datetuple[3])+':'+str(datetuple[4])
                self.datedisplay.setText(self.datestring)

            except Exception as e:
                print(e)

    #跨平台打开文件，支持MAC OS，Linux，Windows
    def openFile(self):
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', gl.file_path))
        elif os.name == 'nt':
            os.startfile(gl.file_path)                          ## only available on windowses
        elif os.name == 'posix':
            subprocess.call(('xdg-open', gl.file_path))

    def onshow(self):
        print (1)
        print (self.listEmails.currentItem().data(0,1) )
        # os.remove("C:/Users/h/Desktop/myproject2/lab1/fuse.log")  #删除文件
    #邮件邮件菜单管理
    def listmailMenu(self,position):

        removeAction = QtWidgets.QAction(u"删除", self, triggered=self.onshow)       # triggered 为右键菜单点击后的激活事件。这里slef.close调用的是系统自带的关闭事件。


        addAction = QtWidgets.QAction(u"添加", self)       # 也可以指定自定义对象事件


        level = 0
        indexes = self.listEmails.selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QtWidgets.QMenu(self.listEmails)
        if level == 1:                                          #选中的是第一个子类
            menu.addAction(removeAction)
            menu.addAction(addAction)

        menu.exec_(self.listEmails.viewport().mapToGlobal(position))




    def _folder_to_path(self, folder):
        text = ''
        if folder.parent() is not None:
            text = self._folder_to_path(folder.parent())
        text += '/' + folder.text(0)
        return text


class ReceiveDialog(QtWidgets.QDialog):
    def __init__(self):
        super(ReceiveDialog, self).__init__()
        uic.loadUi('ui/receivingDialog.ui', self)
        self.movie = QtGui.QMovie("ui/mailgif.gif")            #显示收邮件gif
        self.gifLabel.setMovie(self.movie)
        self.movie.start()
        self.userLabel.setText(gl.username)
    def reset(self):
        self.progressBar.setValue(0)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(len(gl.mails_number))
    def updateProcess(self):
        self.progressBar.setValue(gl.step)

class SendDialog(QtWidgets.QDialog):
    def __init__(self):
        super(SendDialog, self).__init__()
        uic.loadUi('ui/sendDialog.ui', self)
        self.movie = QtGui.QMovie("ui/mailgif.gif")            #显示收邮件gif
        self.gifLabel.setMovie(self.movie)
        self.movie.start()
        self.userLabel.setText(gl.username)
        self.movie = QtGui.QMovie("ui/process1.gif")            #显示进度条
        self.processlabel.setMovie(self.movie)
        self.movie.start()
        self.processlabel.show()



class Filter(QtCore.QObject):
    trigger1= QtCore.pyqtSignal()
    trigger2= QtCore.pyqtSignal()
    trigger3= QtCore.pyqtSignal()
    trigger4= QtCore.pyqtSignal()
    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.FocusIn:
            self.trigger1.emit()
            return False
        elif event.type() == QtCore.QEvent.FocusOut:
            self.trigger2.emit()
            return False
        elif event.type() == QtCore.QEvent.MouseButtonPress:
            self.trigger3.emit()
            return False
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            self.trigger4.emit()
            return False
        else:
            return False





