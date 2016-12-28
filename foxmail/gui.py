# -*- coding:utf-8 -*-
import os
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import Qt,QTranslator,QUrl,QPoint
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyQt5 import QtWebKitWidgets
from PyQt5.QtWidgets import *
import configparser
from email import utils
import time
from datetime import datetime
import smtplib
import re
import sys
import shutil
import csv
import subprocess
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from mail import *
import parameter as gl
import syntax_pars
from backend import *
from mainwindow import  Ui_MainWindow

APPNAME = 'PxMail v3.0'


class ComposeWindow(QtWidgets.QMainWindow):
    myMenu=[]
    receivestring=''
    def __init__(self):
        super(ComposeWindow, self).__init__()
        uic.loadUi('ui/composewindow.ui', self)
        with open("ui/ui.qss","r") as fh:                             #加载qss文件
            self.setStyleSheet(fh.read())
        # self.setWindowFlags(Qt.FramelessWindowHint)     #去边框
        self.fileName=''
        self.HavePicture=False
        self.filepath=os.path.join(gl.draft_path, 'temp.ini')
        self.InitRichText()

        self.InitToolButton()                       #初始化添加联系人按钮

        self.config=configparser.ConfigParser()
        self.config.add_section('mail')

        self.send_thread = sendingThread()                               #加载发送线程
        self.send_thread.triggerSuccess.connect(self.onSuccess)
        self.send_thread.triggerFail.connect(self.onFail)
        self.senddialog=SendDialog()

        completer = QtWidgets.QCompleter()                              #文本框自动补全
        self.txtreceiver.setCompleter(completer)
        self.model=QtCore.QStringListModel()
        completer.setModel(self.model)


    #初始化工具按钮
    def InitToolButton(self):
        self.myMenu=[]
        contact_table=[]
        with open(gl.contact_path,"r") as csvfile:
                csv_reader = csv.DictReader(csvfile)
                for row in csv_reader:
                    contact_table.append(row)

        for person in contact_table:
            self.myMenu.append(person["姓名"]+'|'+ person["电子邮件地址"])

        self.ToolMenu = QMenu(self)
        self.ToolMenu.hovered.connect(self.hoverAction)
        for person in self.myMenu:
            action = QAction(person,self)
            action.triggered.connect(self.addPerson)
            self.ToolMenu.addAction(action)

        self.addButton.setMenu(self.ToolMenu)

    def hoverAction(self,row):
        self.index=row.text()

    def addPerson(self):
        address=self.index.split('|')[1]
        self.txtreceiver.setText(self.txtreceiver.text()+address+';')


    def ontextChanged(self):
        getstring=self.txtreceiver.text()
        #从联系人中筛选
        if not "@" in getstring:
            self.model.setStringList([getstring+"@qq.com", getstring+"@sina.com",getstring+"@sina.cn",
                        getstring+ "@163.com",getstring+"@126.com", getstring+"@hust.edu.cn"])

    def closeEvent(self, e):

        if self.maybeSave():
            e.accept()
        else:
            e.ignore()

    def maybeSave(self):
        if not self.textEdit.document().isModified():
            return True



        # if ret==QMessageBox.AcceptRole

        ret = QMessageBox.warning(self, "Application",
                "邮件内容已修改，是否需要保存草稿？",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

        if ret == QMessageBox.Save:
            return self.fileSave()

        if ret == QMessageBox.Cancel:
            return False

        return True

    #保存邮件到草稿箱
    def fileSave(self):

        try:

            self.config.set('mail', 'receiver', self.txtreceiver.text())
            self.config.set('mail', 'subject', self.txtsubject.text())
            self.config.set('mail', 'text', self.textEdit.document().toHtml())

            ISOTIMEFORMAT='%Y-%m-%d %X'
            self.config.set('mail', 'time',time.strftime( ISOTIMEFORMAT, time.localtime()))
            self.config.write(open(self.filepath, 'w'))

            self.textEdit.document().setModified(False)
        except Exception as e:
            print(e)
            return False
        return True

    def insertImage(self):

        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Insert image',".","Images (*.png *.xpm *.jpg *.bmp *.gif)")[0]

        if filename:

            image = QtGui.QImage(filename)
            if image.isNull():
                popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                          "Image load error",
                                          "Could not load image file!",
                                          QtWidgets.QMessageBox.Ok,
                                          self)
                popup.show()
            else:
                self.HavePicture=True
                cursor = self.textEdit.textCursor()
                cursor.insertImage(image,filename)

                fp = open(filename, 'rb')
                self.msgImage = MIMEImage(fp.read())
                fp.close()
                self.msgImage.add_header('Content-ID', '<image1>')


    #初始化富文本编辑器
    def InitRichText(self):
        self.textEdit.setTextColor(Qt.white)

        db = QtGui.QFontDatabase()                                      #字库里的字体大小
        for size in db.standardSizes():
            self.comboSize.addItem("%s" % (size))
        self.comboSize.setCurrentIndex(                                         #当前字体索引设置为选中文字的大小
                self.comboSize.findText(
                        "%s" % (QtWidgets.QApplication.font().pointSize())))

        self.textEdit.document().setModified(False)
        self.fontChanged(self.textEdit.font())
        self.colorChanged(self.textEdit.textColor())
        self.alignmentChanged(self.textEdit.alignment())

        self.textEdit.document().modificationChanged.connect(
                self.actionSave.setEnabled)
        # self.textEdit.document().modificationChanged.connect(                   #文件改动-->窗口标题 *
        #         self.setWindowModified)
        self.textEdit.document().undoAvailable.connect(
                self.ButtonUndo.setEnabled)
        self.textEdit.document().redoAvailable.connect(
                self.ButtonRedo.setEnabled)

        self.setWindowModified(self.textEdit.document().isModified())
        self.actionSave.setEnabled(self.textEdit.document().isModified())
        self.ButtonUndo.setEnabled(self.textEdit.document().isUndoAvailable())
        self.ButtonRedo.setEnabled(self.textEdit.document().isRedoAvailable())
        self.textEdit.copyAvailable.connect(self.ButtonCut.setEnabled)
        self.textEdit.copyAvailable.connect(self.ButtonCopy.setEnabled)
        QtWidgets.QApplication.clipboard().dataChanged.connect(self.clipboardDataChanged)

    def onSetCurrentFileName(self,filename):
        self.filepath=os.path.join(gl.draft_path, filename)+'.ini'

        self.setWindowTitle(self.tr("%s[*] - %s" % (filename, "写邮件")))
        self.setWindowModified(False)

    # 当前文字格式改变
    def onCurrentCharFormatChanged(self, format):
        self.fontChanged(format.font())
        self.colorChanged(format.foreground().color())
    #光标位置改变
    def onCursorPositionChanged(self):
        self.alignmentChanged(self.textEdit.alignment())
    #字体改变
    def fontChanged(self, font):
        self.comboFont.setCurrentIndex(
                self.comboFont.findText(QtGui.QFontInfo(font).family()))
        self.comboSize.setCurrentIndex(
                self.comboSize.findText("%s" % font.pointSize()))
        self.BuutonTextBold.setChecked(font.bold())
        self.BuutonTextItalic.setChecked(font.italic())
        self.BuutonTextUnderline.setChecked(font.underline())
    #字体加粗
    def onTextBold(self):
        fmt = QtGui.QTextCharFormat()
        fmt.setFontWeight(self.ButtonTextBold.isChecked() and QtGui.QFont.Bold or QtGui.QFont.Normal)
        self.mergeFormatOnWordOrSelection(fmt)
    #斜体显示
    def onTextItalic(self):
        fmt = QtGui.QTextCharFormat()
        fmt.setFontItalic(self.ButtonTextItalic.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)
    #下划线
    def onTextUnderline(self):
        fmt = QtGui.QTextCharFormat()
        fmt.setFontUnderline(self.ButtonTextUnderline.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)
    #字体颜色
    def onTextColor(self):
        col = QtWidgets.QColorDialog.getColor(self.textEdit.textColor(), self)
        if not col.isValid():
            return
        fmt = QtGui.QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(col)
    #文字字体
    def onTextFamily(self,family):
        fmt = QtGui.QTextCharFormat()
        fmt.setFontFamily(family)
        self.mergeFormatOnWordOrSelection(fmt)
    #文字大小
    def onTextSize(self,pointSize):
        pointSize = float(pointSize)
        if pointSize > 0:
            fmt = QtGui.QTextCharFormat()
            fmt.setFontPointSize(pointSize)
            self.mergeFormatOnWordOrSelection(fmt)
    #文字对齐
    def onTextAlign(self,button):
        if button == self.ButtonAlignLeft:
            self.textEdit.setAlignment(Qt.AlignLeft | Qt.AlignAbsolute)
        elif button == self.ButtonAlignCenter:
            self.textEdit.setAlignment(Qt.AlignHCenter)
        elif button == self.ButtonAlignRight:
            self.textEdit.setAlignment(Qt.AlignRight | Qt.AlignAbsolute)
        elif button == self.ButtonAlignJustify:
            self.textEdit.setAlignment(Qt.AlignJustify)
    #改变字体
    def fontChanged(self, font):
        self.comboFont.setCurrentIndex(
                self.comboFont.findText(QtGui.QFontInfo(font).family()))
        self.comboSize.setCurrentIndex(
                self.comboSize.findText("%s" % font.pointSize()))
        self.ButtonTextBold.setChecked(font.bold())
        self.ButtonTextItalic.setChecked(font.italic())
        self.ButtonTextUnderline.setChecked(font.underline())
    #改变颜色
    def colorChanged(self, color):
        pix = QtGui.QPixmap(16, 16)
        pix.fill(color)
        self.ButtonTextColor.setIcon(QtGui.QIcon(pix))
    #改变对齐
    def alignmentChanged(self, alignment):
        if alignment & Qt.AlignLeft:
            self.ButtonAlignLeft.setChecked(True)
        elif alignment & Qt.AlignHCenter:
            self.ButtonAlignCenter.setChecked(True)
        elif alignment & Qt.AlignRight:
            self.ButtonAlignRight.setChecked(True)
        elif alignment & Qt.AlignJustify:
            self.ButtonAlignJustify.setChecked(True)
    #剪贴板变换
    def clipboardDataChanged(self):
        self.ButtonPaste.setEnabled(len(QtWidgets.QApplication.clipboard().text()) != 0)
    #选中词汇合并格式
    def mergeFormatOnWordOrSelection(self, format):
        cursor = self.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QtGui.QTextCursor.WordUnderCursor)

        cursor.mergeCharFormat(format)
        self.textEdit.mergeCurrentCharFormat(format)

    def onScreenCut(self):
        format = 'png'
        screen = QApplication.primaryScreen()
        if screen is not None:
            self.originalPixmap = screen.grabWindow(0)
        else:
            self.originalPixmap = QtGui.QPixmap()

        self.originalPixmap.save('utitled.png', format)
        filename='utitled.png'
        image = QtGui.QImage(filename)
        cursor = self.textEdit.textCursor()
        cursor.insertImage(image,filename)


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
        if self.fileName or self.HavePicture:                                                    #如果有附件
            gl.message = MIMEMultipart('related')
            gl.message['Subject'] = self.txtsubject.text()
            gl.message['from'] = gl.username
            gl.message['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')
            if self.HavePicture:
                html=self.textEdit.document().toHtml()
                html=re.sub("<img src=(.*?)>",'''<img src=cid:image1>''',html)
                gl.message.attach(self.msgImage)

                gl.message.attach(MIMEText(html, 'html', 'utf-8'))
            else:
                gl.message.attach(MIMEText(self.textEdit.document().toHtml(), 'html', 'utf-8'))
            if self.fileName:
                #构造附件
                att = MIMEText(open(self.fileName, 'rb').read(), 'base64', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                att["Content-Disposition"] = 'attachment; filename='+self.fileName
                gl.message.attach(att)
        else:
            # gl.message = MIMEText(self.textEdit.toPlainText(), 'plain', 'utf-8')
            gl.message = MIMEText(self.textEdit.document().toHtml(), 'html', 'utf-8')
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
        #保存到已发送
        self.config.set('mail', 'receiver', self.txtreceiver.text())
        self.config.set('mail', 'subject', self.txtsubject.text())
        self.config.set('mail', 'text', self.textEdit.document().toHtml())

        ISOTIMEFORMAT='%Y-%m-%d %X'
        self.config.set('mail', 'time',time.strftime( ISOTIMEFORMAT, time.localtime()))

        filepath=os.path.join(gl.send_path, self.txtsubject.text())+'.ini'
        self.config.write(open(filepath, 'w'))



        QtWidgets.QMessageBox.warning(self, APPNAME,"邮件发送成功" )
        self.textEdit.document().setModified(False)
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

        self.config=configparser.ConfigParser()
        self.config.read('config.ini')
        gl.smtpport = self.config.get('mail', 'smtpport')
        gl.popport = self.config.get('mail', 'popport')
        # gl.smtphost = self.config.get('mail', 'smtpserver')
        # gl.pophost = self.config.get('mail', 'popserver')
        # gl.popssl = self.config.get('mail', 'popssl') == "True"
        # gl.smtpssl = self.config.get('mail', 'smtpssl') == "True"
        secret_user = self.config.get('mail', 'user')
        secret_passwd = self.config.get('mail', 'passwd')

        for i in range(0,len(secret_user)):
            gl.username += chr(ord(secret_user[i]) ^ 7)
        for i in range(0,len(secret_passwd)):
            gl.password += chr(ord(secret_passwd[i]) ^ 5)
        self.Initlogin()

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


        self.hideManualSet()
        self.loading_thread = loadingThread()                               #加载登陆线程
        self.loading_thread.trigger1.connect(self.successed)
        self.loading_thread.trigger2.connect(self.failed)

    def Initlogin(self):
        self.txtuser.setText(gl.username)
        self.txtpassword.setText(gl.password)
        self.popportEdit.setText(gl.popport)
        self.smtpportEdit.setText(gl.smtpport)



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
        if gl.username!=self.txtuser.text() :
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

            gl.username=self.txtuser.text()
            secret_user = ''
            for i in range(0,len(gl.username)):
                secret_user += chr(ord(gl.username[i]) ^ 7)
            self.config.set('mail', 'user', secret_user)
            self.save()

    def txtpassEdited(self):
        if gl.password!=self.txtpassword.text():
            gl.password=self.txtpassword.text()
            secret_passwd = ''
            for i in range(0,len(gl.password)):
                secret_passwd += chr(ord(gl.password[i]) ^ 5)
            self.config.set('mail', 'passwd', secret_passwd)
            self.save()


    def popportEdited(self):
        pass
        # if gl.smtpport != str(unicode(self.lineedit1_2_a.text(), 'utf-8', 'ignore')):
        #     smtpport = str(unicode(self.lineedit1_2_a.text(), 'utf-8', 'ignore'))
        #     config.set('mail', 'smtpport', smtpport)
        #     self.save()


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
                gl.smtpport='25'
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

    #保存设置到config.ini
    def save(self):
        self.config.write(open('config.ini', 'w'))
        self.label_prompt.setText(u'<p align=right style="font-family:Microsoft YaHei;font:13px;color:'
            u'#7DFF00">更改已保存<img src="ui/images/saved.png"></p>')
        gl.new_trans = True
        time.sleep(0.01)
        self.trans_thread.start()


    #关闭窗口
    def onCancel(self):
        self.close()
    def onMinimum(self):
        self.showMinimized()

    #鼠标按下事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos()-self.frameGeometry().topLeft()
            event.accept()

    #鼠标移动事件
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self.dragPosition != None:
                self.move(event.globalPos() - self.dragPosition)
                event.accept()

    #鼠标弹起事件
    def mouseReleaseEvent(self, event):
        self.dragPosition = QtCore.QPoint(0, 100)
        event.accept()



    #SSL按钮事件
    def onSSLpop(self):
        if self.checkSSLpop.isChecked():
            self.popportEdit.setText("995")
        else:
            self.popportEdit.setText("110")
        print(self.checkSSLpop.isChecked())

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

class Contact(QWidget):
    def __init__(self, parent=None):
        super(Contact, self).__init__(parent)
        self.contact_table=[]
        self.March_ID=[]
        uic.loadUi('ui/Contact.ui', self)
        with open("ui/ui.qss","r") as fh:                             #加载qss文件
            self.setStyleSheet(fh.read())
        self.setWindowFlags(Qt.FramelessWindowHint)     #去边框
        self.widgetShow.hide()                      #隐藏显示框
        self.widgetEdit.hide()                    #隐藏编辑框
        self.SetupCsv()                             #加载Csv
        self.PersonDisplay()                        #初始化联系人并显示

        self.InitToolButton()                       #初始化工具按钮

        self.closefilter = Filter()                                                 #关闭
        self.labelclose.installEventFilter(self.closefilter)
        self.closefilter.trigger4.connect(self.onCancel)

        self.minfilter = Filter()                                                 #最小化
        self.labelmin.installEventFilter(self.minfilter)
        self.minfilter.trigger4.connect(self.onMinimum)


        # self.InitSearchEdit()                                           #初始化搜索框





    #初始化工具按钮
    def InitToolButton(self):
        self.actionA = QAction(u'导出通讯录 (*.csv)',self)
        self.actionB = QAction(u'导入通讯录 (*.csv)',self)

        self.actionA.triggered.connect(self.exportCsv)
        self.actionB.triggered.connect(self.importCsv)
        self.ToolMenu = QMenu(self)
        self.ToolMenu.addAction(self.actionA)
        self.ToolMenu.addAction(self.actionB)

        self.ToolMenu.hovered.connect(self.hoverAction)
        self.toolButton.setMenu(self.ToolMenu)

    def hoverAction(self,row):
        print(row)
        print(row.text())
    def test(self,row):
        print(self.ToolMenu.menuAction().text())
        print(self.ToolMenu.activeAction())
        print(row)

    #导出通讯录
    def exportCsv(self):
        filename, filetype = QFileDialog.getSaveFileName(self,"导出通讯录",
                                        '.',"CSV (*.csv)" )

        # filename = QtGui.QFileDialog.getSaveFileName(self,
        #         "Saving current message in HTML format...", '.', "HTML (*.html *.htm)")
        # if not filename:
        #     return

        if not filename:
            return
        qFile = QtCore.QFile(filename)
        if not qFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.ReadWrite):
            QtWidgets.QMessageBox.warning(self, APPNAME,
                    "无法创建文件: %s\n%s." % (filename, qFile.errorString()))
            return

        with open(filename,"w",newline="") as datacsv:
            csvwriter = csv.writer(datacsv,dialect = ("excel"))
            #csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
            csvwriter.writerow(["姓名","电子邮件地址","性别","生日","手机","QQ",
            "家庭住址","公司","部门","职位","公司地址"])
            for person in self.contact_table:
                csvwriter.writerow([person["姓名"],person["电子邮件地址"],person["性别"],person["生日"],person["手机"],person["QQ"],
                        person["家庭住址"],person["公司"],person["部门"],person["职位"],person["公司地址"]])

    #导入通讯录
    def importCsv(self):

        filePath,filetype = QFileDialog.getOpenFileName(self,"导入通讯录",
                         '.', "CSV (*.csv)",)

        if filePath:
            with open(filePath, 'r') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                for row in csv_reader:
                    self.contact_table.append(row)

    #读取Csv缓存
    def SetupCsv(self):
        try:
            with open(gl.contact_path,"r") as csvfile:
                csv_reader = csv.DictReader(csvfile)
                for row in csv_reader:
                    self.contact_table.append(row)
        except:
            pass


    #保存并写入Csv
    def WriteCsv(self):
        #存到文件
        with open(gl.contact_path,"w",newline="") as datacsv:
            csvwriter = csv.writer(datacsv,dialect = ("excel"))
            #csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
            csvwriter.writerow(["姓名","电子邮件地址","性别","生日","手机","QQ",
            "家庭住址","公司","部门","职位","公司地址"])
            for person in self.contact_table:
                csvwriter.writerow([person["姓名"],person["电子邮件地址"],person["性别"],person["生日"],person["手机"],person["QQ"],
                        person["家庭住址"],person["公司"],person["部门"],person["职位"],person["公司地址"]])

    #显示联系人列表
    def PersonDisplay(self):
        subjects = []
        for person in self.contact_table:
            subjects.append(person["姓名"])
        self.listpeople.clear()
        self.listpeople.addItems(subjects)

        self.deleteButton.setEnabled(False)
        self.contactlistButton.setEnabled(False)

    #显示联系人内容
    def onPeopleSelected(self, item):
        self.index = item.listWidget().row(item)

        self.contentFlash()

        self.deleteButton.setEnabled(True)
        self.contactlistButton.setEnabled(True)

    #刷新内容
    def contentFlash(self):
        person=self.contact_table[self.index]

        #清空上次显示
        self.labelname.setText('')
        self.labelmailtxt.setText('')
        self.labelsextxt.setText('')
        self.labelbrithtxt.setText('')
        self.labelphonetxt.setText('')
        self.labelqqtxt.setText('')
        self.labelhomeaddtxt.setText('')
        self.labelcomtxt.setText('')
        self.labelparttxt.setText('')
        self.labelworktxt.setText('')
        self.labelcomaddtxt.setText('')
        self.widgetShow.show()

        #显示当前联系人信息
        if "姓名" in person:
            self.labelname.setText(person["姓名"])
        if "电子邮件地址" in person:
            self.labelmailtxt.setText(person["电子邮件地址"])
        if "性别" in person:
            self.labelsextxt.setText(person["性别"])
        if "生日" in person:
            self.labelbrithtxt.setText(person["生日"])
        if "手机" in person:
            self.labelphonetxt.setText(person["手机"])
        if "QQ" in person:
            self.labelqqtxt.setText(person["QQ"])
        if "家庭住址" in person:
            self.labelhomeaddtxt.setText(person["家庭住址"] )
        if "公司" in person:
            self.labelcomtxt.setText(person["公司"])
        if "部门" in person:
            self.labelparttxt.setText(person["部门"])
        if "职位" in person:
            self.labelworktxt.setText(person["职位"])
        if "公司地址" in person:
            self.labelcomaddtxt.setText(person["公司地址"])

    def onEdit(self):
        self.Editname.setText(self.labelname.text())
        self.Editmail.setText(self.labelmailtxt.text())
        self.comboBoxsex.setCurrentText(self.labelsextxt.text())
        self.dateEdit.setDisplayFormat(self.labelbrithtxt.text())
        self.Editphone.setText(self.labelphonetxt.text())
        self.Editqq.setText(self.labelqqtxt.text())
        self.Edithomeadd.setPlainText(self.labelhomeaddtxt.text())
        self.Editcom.setText(self.labelcomtxt.text())
        self.Editpart.setText(self.labelparttxt.text())
        self.Editwork.setText(self.labelworktxt.text())
        self.Editcomadd.setPlainText(self.labelcomaddtxt.text())

    def onCreatperson(self):

        person={"姓名":'未命名',
                "电子邮件地址":'',
                "性别":'',
                "生日":'',
                "手机":'',
                "QQ":'',
                "家庭住址":'',
                "公司":'',
                "部门":'',
                "职位":'',
                "公司地址":''}
        self.contact_table.append(person)
        self.PersonDisplay()
    #删除联系人
    def onDeleteperson(self):
        try:
            self.contact_table.pop(self.index)
            self.PersonDisplay()
            self.widgetShow.hide()
            self.widgetEdit.hide()
            self.WriteCsv()
        except:
            pass
    #保存联系人
    def onPeopleSaved(self):
        self.contact_table[self.index]["姓名"]=self.Editname.text()
        self.contact_table[self.index]["电子邮件地址"]=self.Editmail.text()
        self.contact_table[self.index]["性别"]=self.comboBoxsex.currentText()
        self.contact_table[self.index]["生日"]=self.dateEdit.text()
        self.contact_table[self.index]["手机"]=self.Editphone.text()
        self.contact_table[self.index]["QQ"]=self.Editqq.text()
        self.contact_table[self.index]["家庭住址"]=self.Edithomeadd.toPlainText()
        self.contact_table[self.index]["公司"]=self.Editcom.text()
        self.contact_table[self.index]["部门"]=self.Editpart.text()
        self.contact_table[self.index]["职位"]=self.Editwork.text()
        self.contact_table[self.index]["公司地址"]=self.Editcomadd.toPlainText()

        self.PersonDisplay()
        self.contentFlash()
        self.widgetShow.show()
        self.widgetEdit.hide()
        self.WriteCsv()



    def onComposeMail(self):
        pass

    #初始化搜索框
    def InitSearchEdit(self):
        self.searchEdit.editingFinished.connect(self.txtsearchEdited)        #文本编辑完成自动搜索

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
            self.string=self.searchEdit.text()

            QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)          #鼠标设置成忙等待状态
            self.March_ID=[]                                                  #匹配符合条件的邮件
            for person in self.contact_table:
                if (self.string in person["姓名"]):
                    self.March_ID.append(person)

            self.mailDisplay()
            QtWidgets.QApplication.restoreOverrideCursor()

        else:
            self.March_ID=self.contact_table
            self.mailDisplay()
    #清空搜索框
    def cleartxt(self):
        self.searchEdit.clear()
        gl.March_ID=gl.emails
        gl.string=''
        gl.search=False
        self.mailDisplay()

    #关闭窗口
    def onCancel(self):
        self.close()
    def onMinimum(self):
        self.showMinimized()

    #鼠标按下事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos()-self.frameGeometry().topLeft()
            event.accept()

    #鼠标移动事件
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self.dragPosition != None:
                if self.dragPosition.y() < 30:
                    self.move(event.globalPos() - self.dragPosition)
                    event.accept()

    #鼠标弹起事件
    def mouseReleaseEvent(self, event):
        self.dragPosition = QtCore.QPoint(0, 100)
        event.accept()

class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
# class MainWindow(QtWidgets.QMainWindow):
    folders = []
    emails = []
    currentPath=''
    ReadFiles=[]
    row=0
    lastrow=0
    Ascending=True
    background=True
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # uic.loadUi('mainwindow1.ui', self)
        with open("ui/ui.qss","r") as fh:                             #加载qss文件
            self.setStyleSheet(fh.read())



        self.isMaxShow = 0
        self.setWindowFlags(Qt.FramelessWindowHint)     #去边框

        self.receive_thread = receiveThread()                               #加载登陆线程
        self.receive_thread.triggerFinish.connect(self.mailDisplay)
        self.receivedialog=ReceiveDialog()
        self.receivedialog.triggerclose.connect(self.stopReceive)
        self.receive_thread.triggerNumber.connect(self.receivedialog.updateProcess)


        self.btnForward.setEnabled(False)                               #转发功能不可用
        self.btnDelete.setEnabled(False)
        self.btnReply.setEnabled(False)

        self.config=configparser.ConfigParser()
        self.config.add_section('mail')

        self.InitSearchEdit()                                           #初始化搜索框
        self.searchEdit.editingFinished.connect(self.txtsearchEdited)        #文本编辑完成自动显示服务器
        self.search_thread = searchThread()
        self.search_thread.trigger.connect(self.mailDisplay)


        self.comboBox.insertSeparator(3)
        self.comboBox.insertItems(4,["√    升序","      降序"])
        self.listEmails.customContextMenuRequested[QtCore.QPoint].connect(self.listmailMenu)
        self.treeMailWidget.customContextMenuRequested[QtCore.QPoint].connect(self.folderMenu)
        self.emailPreview.customContextMenuRequested[QtCore.QPoint].connect(self.webviewMenu)
        # self.highlight = syntax_pars.PythonHighlighter(self.emailPreview.document())

        self.attachdisplay.hide()                                           #隐藏附件标签
        self.attachlabel.hide()

        self.createContextMenu()                                                #为按钮创建菜单


        self.closefilter = Filter()                                                 #关闭
        self.labelclose.installEventFilter(self.closefilter)
        self.closefilter.trigger4.connect(self.onCancel)

        self.minfilter = Filter()                                                 #最小化
        self.labelmin.installEventFilter(self.minfilter)
        self.minfilter.trigger4.connect(self.onMinimum)

        self.maxfilter=Filter()
        self.labelmax.installEventFilter(self.maxfilter)
        self.maxfilter.trigger4.connect(self.onMaxmum)

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
                try:
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
                except:
                    pass

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


    #发送邮件
    def onComposeMail(self):
        self.compose = ComposeWindow()
        self.compose.show()

    #联系人列表
    def onContactList(self):
        self.contact = Contact()
        self.contact.show()

    #初始化搜索框
    def InitSearchEdit(self):
        self.linefilter = Filter()                                                 #安装行编辑器事件过滤器
        self.searchEdit.installEventFilter(self.linefilter)
        self.linefilter.trigger1.connect(self.FocusIn)
        self.linefilter.trigger2.connect(self.FocusOut)

        self.labelfilter = Filter()                                                 #安装标签事件过滤器
        self.Xlabel.installEventFilter(self.labelfilter)
        self.labelfilter.trigger3.connect(self.cleartxt)

        completer = QtWidgets.QCompleter()                              #文本框自动补全
        self.searchEdit.setCompleter(completer)
        self.model=QtCore.QStringListModel()
        completer.setModel(self.model)


    def FocusIn(self):
        self.Xlabel.setText("x")

    def FocusOut(self):
        if not self.searchEdit.text():

            self.Xlabel.setText("")

    def ontextChanged(self):

        getstring=self.searchEdit.text()
        print(getstring)

        self.model.setStringList([getstring+" |发件人", getstring+" |主题",getstring+" |内容",getstring+" |全文"])

    def txtsearchEdited(self):
        if self.searchEdit.text():
            gl.string=self.searchEdit.text().split('|')[0]
            QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)          #鼠标设置成忙等待状态
            gl.March_ID=[]                                                  #匹配符合条件的邮件

            if len(self.searchEdit.text().split('|')) ==1:                  #默认条件
                for email in gl.emails:
                    info=get_info(email)
                    if (gl.string in info["subject"]) or (gl.string in info["content"]) or (gl.string in info["addr"]):
                        gl.March_ID.append(email)
                        self.data=info["subject"]+info["content"]+info["addr"]
                        pattern = re.compile(gl.string)
                        dataMatched = re.findall(pattern, self.data)                        #匹配所有关键字，背景高亮
                        gl.search=True

                    # self.highlight.setHighlightData(dataMatched)
                    # self.highlight.rehighlight()
            elif self.searchEdit.text().split('|')[1] =="全文" :
                for email in gl.emails:
                    info=get_info(email)
                    if (gl.string in info["subject"]) or (gl.string in info["content"]) or (gl.string in info["addr"]):
                        gl.March_ID.append(email)
                        self.data=info["subject"]+info["content"]+info["addr"]
                        gl.search=True
            elif self.searchEdit.text().split('|')[1] =="发件人" :
                for email in gl.emails:
                    info=get_info(email)
                    if (gl.string in  info["addr"]):
                        gl.March_ID.append(email)
                        self.data=info["subject"]+info["content"]+info["addr"]
                        gl.search=True
            elif self.searchEdit.text().split('|')[1] =="主题" :
                for email in gl.emails:
                    info=get_info(email)
                    if (gl.string in  info["subject"]):
                        gl.March_ID.append(email)
                        self.data=info["subject"]+info["content"]+info["addr"]
                        gl.search=True
            elif self.searchEdit.text().split('|')[1] =="内容" :
                for email in gl.emails:
                    info=get_info(email)
                    if (gl.string in  info["content"]):
                        gl.March_ID.append(email)
                        self.data=info["subject"]+info["content"]+info["addr"]
                        gl.search=True


            self.mailDisplay()
            QtWidgets.QApplication.restoreOverrideCursor()

        else:
            gl.March_ID=gl.emails
            self.mailDisplay()
    #清空搜索框
    def cleartxt(self):
        self.searchEdit.clear()
        gl.March_ID=gl.emails
        gl.string=''
        gl.search=False
        self.mailDisplay()





    def changeBackground(self):
        if self.background:
            self.emailPreview.setStyleSheet(u'background-color: rgb(255, 255, 255);')
            self.background=False
        else :
            self.emailPreview.setStyleSheet('')
            self.background=True


    #webview的右键菜单
    def webviewMenu(self,position):
        changeAction = QtWidgets.QAction(u"更换背景", self,triggered=self.changeBackground)


        menu = QtWidgets.QMenu(self.emailPreview)
        menu.addAction(changeAction)

        menu.exec_(self.pos())



    #回复功能
    def onReply(self):
        splitline="----------------------------------------"
        self.compose = ComposeWindow()
        self.compose.show()
        self.compose.txtsubject.setText('回复：'+self.subdisplay.text())        #显示主题，发信人，日期
        self.compose.txtreceiver.setText(self.fromdisplay.text())

        document = QtGui.QTextDocument()
        document.setHtml('\r\n\r\n\r\n'+splitline+'\n'+str(self.emailPreview.page().mainFrame().toHtml()))
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

    def makeFolder(self):
        item= QtWidgets.QTreeWidgetItem()
        item.setText(0,'新建文件夹')
        icon=QtGui.QIcon("ui/manwindow/新建文件夹.png")
        item.setIcon(0,icon)

        item.setFlags(item.flags()| Qt.ItemIsEditable)
        self.treeMailWidget.addTopLevelItem(item)

    #文件夹的菜单
    def folderMenu(self,position):
        removeAction = QtWidgets.QAction(u"删除文件夹", self)
        addAction = QtWidgets.QAction(u"新建文件夹", self,triggered=self.makeFolder)       # 也可以指定自定义对象事件


        indexes = self.treeMailWidget.selectedIndexes()

        menu = QtWidgets.QMenu(self.treeMailWidget)
        menu.addAction(addAction)

        if len(indexes) > 0 :                           #有选中文件夹
            if indexes[0].row()>2:                      #选中的是第三行以上
                menu.addAction(removeAction)


        menu.exec_(self.treeMailWidget.viewport().mapToGlobal(position))


    #选择文件夹
    def onFolderSelected(self, folder):                                                 #folder:选中的目录
        txt = self.treeMailWidget.currentItem().text(0)
        if txt ==u"收件夹":
            self.listEmails.clear()
            self.comboBox.show()
            self.btnReply.setText("回复")
            self.btnForward.show()
            self.fromlabel.setText("发信人：")
            gl.folder_path = self._folder_to_path(folder).strip('/')                                      #存放文件的路径
            self.receive_thread.start()
            self.receivedialog.reset()
            self.receivedialog.exec_()
        elif txt ==u"草稿夹":
            self.listEmails.clear()
            self.btnReply.setText("编辑")
            self.btnForward.hide()
            self.fromlabel.setText("收信人：")
            self.comboBox.hide()
            self.currentPath=gl.draft_path
            self.readFiles(gl.draft_path)
        elif txt ==u"已发送":
            self.listEmails.clear()
            self.btnReply.setText("编辑")
            self.btnForward.hide()
            self.fromlabel.setText("收信人：")
            self.comboBox.hide()
            self.readFiles(gl.send_path)
        elif txt ==u"已删除":
            self.listEmails.clear()
            self.btnReply.setText("编辑")
            self.btnForward.hide()
            self.fromlabel.setText("收信人：")
            self.comboBox.hide()
            self.readFiles(gl.delete_path)

    #读取其他文件夹的邮件到列表
    def readFiles(self,path):

        files = os.listdir(path)                                                       #列出目录下的文件
        files.sort()                                                                     #整理文件顺序
        mail_files = [f for f in files if os.path.isfile(os.path.join(path, f))]

        items=[]
        self.ReadFiles=[]
        for mail_file in mail_files:
            self.config.read(os.path.join(path, mail_file))

            subject = self.config.get('mail', 'subject')
            draft={
                'subject':subject,
                'receiver':self.config.get('mail', 'receiver'),
                'text':self.config.get('mail', 'text'),
                'time':self.config.get('mail', 'time')
            }

            self.ReadFiles.append(draft)
            item= QtWidgets.QTreeWidgetItem()
            item.setText(0,subject)
            items.append(item)
        self.listEmails.clear()
        self.listEmails.insertTopLevelItems(0, items)

   #刷新邮件
    def onRefresh(self):
        try:
            self.receive_thread.wait()                          #等待线程退出，再执行下面代码，否则list和retr同时执行会崩溃
            gl.force_refresh=True
            refresh_mail()
            self.statusbar.showMessage("Refreshing...")
            self.receive_thread.running=True
            self.receive_thread.start()
            self.receivedialog.reset()
            self.receivedialog.exec_()
        except:
            pass
    #停止接收邮件
    def stopReceive(self):
        self.receive_thread.stop()


    #显示邮件正文
    def onMailSelected(self, item):
        self.btnForward.setEnabled(True)                               #转发功能可用
        self.btnDelete.setEnabled(True)
        self.btnReply.setEnabled(True)
        if  item.treeWidget().currentItem().parent():                        #假如有父亲节点，则选中相应邮件

            self.index=item.treeWidget().currentItem().data(0,1)               #将Item中的行号提取出来
            email = gl.March_ID[self.index]

            info=get_info(email)
            try:

                if info["html"] != '':
                    if gl.search:
                        info["html"]=info["html"].replace(gl.string,"<strong><font color='#e87400'>"+gl.string+"</font></strong>")


                    self.emailPreview.setHtml(info["html"])                 #显示html文本
                    # print(info["html"])
                elif info["content"] != '':                                    #显示纯文本
                    info["content"]="<strong><font color='#ffffff'>"+info["content"]+"</font></strong>"
                    if gl.search:

                        info["content"]=info["content"].replace(gl.string,"<strong><font color='#e87400'>"+gl.string+"</font></strong>")

                    self.emailPreview.setHtml(info["content"].replace('\n','<br>'))

                if info["filename"]:
                    self.filename=info["filename"]
                    self.attachdisplay.setText(self.filename)
                    self.attachdisplay.show()
                    self.attachlabel.show()
                else:
                    self.attachdisplay.hide()
                    self.attachlabel.hide()

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

        elif self.treeMailWidget.currentItem().text(0) != u"收件夹" :

            for each in self.ReadFiles:
                if each["subject"] == item.treeWidget().currentItem().text(0):
                    self.subdisplay.setText(each["subject"])                    #显示主题，发信人，日期
                    self.fromdisplay.setText(each["receiver"])
                    self.emailPreview.setHtml(each["text"])
                    self.datedisplay.setText(each["time"])



    #跨平台打开文件，支持MAC OS，Linux，Windows
    def openFile(self):
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', gl.file_path))
        elif os.name == 'nt':
            os.startfile(gl.file_path)                          ## only available on windowses
        elif os.name == 'posix':
            subprocess.call(('xdg-open', gl.file_path))

    #收的邮件的内容
    def ReceivemailContent(self,index):
        content=''
        subject=''
        addr=''
        datestring=''
        try:
            email = gl.March_ID[index]
            info=get_info(email)
            if info["html"] != '':
                content=info["html"]           #显示html文本

            elif info["content"] != '':                                    #显示纯文本
                content=info["content"].replace('\n','<br>')
            subject=info["subject"]                    #显示主题，发信人，日期
            addr=info["addr"]
            date=""

            if info["date"]:                                                #从邮件提取日期
                date=info["date"]
            else:
                date=info["received"][-31:]
            datetuple=utils.parsedate(date)
            if(len(str(datetuple[4]))==1):                                  #如果分钟是个位数，前面填充一个0
                datestring=str(datetuple[0])+'-'+str(datetuple[1])+'-'+str(datetuple[2])\
                      +' '+str(datetuple[3])+':0'+str(datetuple[4])
            else:
                datestring=str(datetuple[0])+'-'+str(datetuple[1])+'-'+str(datetuple[2])\
                          +' '+str(datetuple[3])+':'+str(datetuple[4])
            return content,subject,addr,datestring
        except:
            pass

    #删除邮件
    def onDelete(self):
        if self.treeMailWidget.currentItem().text(0) ==u"收件夹":
            index = self.listEmails.currentItem().data(0,1)

            path=os.path.join(gl.cathe_folder_path,str(index)) +'.ml'


            ret = QMessageBox.warning(self, "warning",
                    "确定删除邮件？",
                    QMessageBox.Yes | QMessageBox.No)

            if ret == QMessageBox.No:
                return False
            elif ret == QMessageBox.Yes:
                os.remove(path)                     #删邮件
                delete_mail(index)

                content,subject,addr,datestring=self.ReceivemailContent(index)      #并保存到已删除
                self.config.set('mail', 'receiver', addr)
                self.config.set('mail', 'subject', subject)
                self.config.set('mail', 'text', content)
                self.config.set('mail', 'time',datestring)
                self.config.write(open(gl.delete_path, 'w'))

                #删除完成以后重新加载一遍列表邮件
                gl.emails = []
                files = os.listdir(gl.cathe_folder_path)
                files.sort(key=lambda x:int(x[:-3]))
                mail_files = [f for f in files if os.path.isfile(os.path.join(gl.cathe_folder_path, f))]
                for mail_file in mail_files:
                    try:
                        with open(os.path.join(gl.cathe_folder_path, mail_file), 'r') as mail_handle:
                            gl.emails.append(message_from_file(mail_handle))
                    except Exception as e:
                            print(e)+'save'
                gl.March_ID=gl.emails                                   #匹配到的邮件等于所有邮件
                self.mailDisplay()
        else :
            text = self.listEmails.currentItem().text(0)
            path = os.path.join(gl.cache_path,self.treeMailWidget.currentItem().text(0),text)+'.ini'
            print(path)
            ret = QMessageBox.warning(self, "warning",
                    "确定删除邮件？",
                    QMessageBox.Yes | QMessageBox.No)

            if ret == QMessageBox.No:
                return False
            elif ret == QMessageBox.Yes:
                try:
                    shutil.move(path,os.path.join(gl.delete_path,text)+'.ini')          #先移动
                except:
                    os.remove(path)                                                     #失败了则强行删除
                self.readFiles(self.currentPath)





    #邮件邮件菜单管理
    def listmailMenu(self,position):

        removeAction = QtWidgets.QAction(u"删除", self, triggered=self.onDelete)       # triggered 为右键菜单点击后的激活事件。这里slef.close调用的是系统自带的关闭事件。

        addAction = QtWidgets.QAction(u"添加", self)       # 也可以指定自定义对象事件


        isChild=False
        indexes = self.listEmails.selectedIndexes()

        if len(indexes) > 0:
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                isChild=True

        menu = QtWidgets.QMenu(self.listEmails)
        if isChild or (self.treeMailWidget.currentItem().text(0) != u"收件夹" and len(indexes) > 0):   #选中的是第一个子类
            menu.addAction(removeAction)
            menu.addAction(addAction)

        menu.exec_(self.listEmails.viewport().mapToGlobal(position))


    #鼠标按下事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos()-self.frameGeometry().topLeft()
            event.accept()

    #鼠标移动事件
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self.dragPosition != None:
                if self.dragPosition.y() < 30:
                    self.move(event.globalPos() - self.dragPosition)
                    event.accept()

    #鼠标弹起事件
    def mouseReleaseEvent(self, event):
        self.dragPosition = QtCore.QPoint(0, 100)
        event.accept()

        #关闭窗口
    def onCancel(self):
        self.close()
    #最小化
    def onMinimum(self):
        self.showMinimized()
    #最大化
    def onMaxmum(self):
        if self.isMaxShow:
            self.showNormal()
            self.isMaxShow = 0
        else:
            self.showMaximized()
            self.isMaxShow = 1



    def _folder_to_path(self, folder):
        text = ''
        if folder.parent() is not None:
            text = self._folder_to_path(folder.parent())
        text += '/' + folder.text(0)
        return text


class ReceiveDialog(QtWidgets.QDialog):
    triggerclose = QtCore.pyqtSignal()
    def __init__(self):
        super(ReceiveDialog, self).__init__()
        uic.loadUi('ui/receivingDialog.ui', self)
        self.movie = QtGui.QMovie("ui/mailgif.gif")            #显示收邮件gif
        self.gifLabel.setMovie(self.movie)
        self.movie.start()
        self.userLabel.setText('''<p align=left style="font-family:Microsoft YaHei;font:14px;
                color:#437cd8">%s</p>'''%gl.username)

        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)  #去边框
        self.closefilter = Filter()                                                 #关闭
        self.labelclose.installEventFilter(self.closefilter)
        self.closefilter.trigger4.connect(self.onCancel)

        self.minfilter = Filter()                                                 #最小化
        self.labelmin.installEventFilter(self.minfilter)
        self.minfilter.trigger4.connect(self.onMinimum)

    def closeEvent(self, QCloseEvent):
        self.triggerclose.emit()

    def reset(self):
        self.progressBar.setValue(0)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(len(gl.mails_number))
    def updateProcess(self):
        self.progressBar.setValue(gl.step)


    #关闭窗口
    def onCancel(self):
        self.close()
    def onMinimum(self):
        self.showMinimized()

    #鼠标按下事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos()-self.frameGeometry().topLeft()
            event.accept()

    #鼠标移动事件
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self.dragPosition != None:
                self.move(event.globalPos() - self.dragPosition)
                event.accept()

    #鼠标弹起事件
    def mouseReleaseEvent(self, event):
        self.dragPosition = QtCore.QPoint(0, 100)
        event.accept()


class SendDialog(QtWidgets.QDialog):
    def __init__(self):
        super(SendDialog, self).__init__()
        uic.loadUi('ui/sendDialog.ui', self)
        self.movie = QtGui.QMovie("ui/mailgif.gif")            #显示收邮件gif
        self.gifLabel.setMovie(self.movie)
        self.movie.start()
        self.userLabel.setText(gl.username)

        # self.movie = QtGui.QMovie("ui/process1.gif")            #显示进度条
        # self.processlabel.setMovie(self.movie)
        # self.movie.start()
        # self.processlabel.show()



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





