import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import  QUrl
from windows import Ui_MainWindow

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.emailPreview.load(QUrl('http://www.cnblogs.com/misoag/archive/2013/01/09/2853515.html'))

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

        self.senddialog=SendDialog()
        # self.senddialog.exec_()

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
                    gl.search=True

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
        gl.string=''
        gl.search=False
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

        # self.compose.textEdit.setDocument(document)
        self.compose.textEdit.append(str(document.toHtml()))

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
        elif txt ==u"草稿夹":
            gl.read_path=gl.draft_path
            self.read_thread.start()

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
                    if gl.search:

                        info["content"]=info["content"].replace(gl.string,"<strong><font color='#e87400'>"+gl.string+"</font></strong>")


                    # self.emailPreview.insertHtml('''<img src="http://www.cyberhome.cn/images/girl/PLMM_A.jpg">''')
                    self.emailPreview.setHtml(info["content"].replace('\n','<br>'))
                elif info["html"] != '':
                    if gl.search:
                        info["html"]=info["html"].replace(gl.string,"<strong><font color='#e87400'>"+gl.string+"</font></strong>")
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

if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    window=Main()
    window.show()

    sys.exit(app.exec_())