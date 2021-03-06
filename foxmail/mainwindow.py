# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow1.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1094, 826)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background: rgb(68, 69, 73);")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setMinimumSize(QtCore.QSize(40, 30))
        self.widget_2.setStyleSheet("/*background: rgb(68, 69, 73);*/")
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_10.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout_10.setSpacing(5)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.iconlabel = QtWidgets.QLabel(self.widget_2)
        self.iconlabel.setMinimumSize(QtCore.QSize(30, 30))
        self.iconlabel.setMaximumSize(QtCore.QSize(30, 30))
        self.iconlabel.setPixmap(QtGui.QPixmap("ui/logo.png"))
        self.iconlabel.setScaledContents(True)
        self.iconlabel.setObjectName("iconlabel")
        self.horizontalLayout_10.addWidget(self.iconlabel)
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.horizontalLayout_10.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(751, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem)
        self.labelmin = QtWidgets.QLabel(self.widget_2)
        self.labelmin.setMinimumSize(QtCore.QSize(30, 30))
        self.labelmin.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.labelmin.setFont(font)
        self.labelmin.setStyleSheet("QLabel{\n"
"   color:white;\n"
"    border:0px;\n"
"}\n"
"QLabel:hover{\n"
"   background-color:rgb(255,255,255,50%);\n"
"}")
        self.labelmin.setAlignment(QtCore.Qt.AlignCenter)
        self.labelmin.setObjectName("labelmin")
        self.horizontalLayout_10.addWidget(self.labelmin)
        self.labelmax = QtWidgets.QLabel(self.widget_2)
        self.labelmax.setMinimumSize(QtCore.QSize(30, 30))
        self.labelmax.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.labelmax.setFont(font)
        self.labelmax.setStyleSheet("QLabel{\n"
"   color:white;\n"
"    border:0px;\n"
"}\n"
"QLabel:hover{\n"
"   background-color:rgb(255,255,255,50%);\n"
"}")
        self.labelmax.setAlignment(QtCore.Qt.AlignCenter)
        self.labelmax.setObjectName("labelmax")
        self.horizontalLayout_10.addWidget(self.labelmax)
        self.labelclose = QtWidgets.QLabel(self.widget_2)
        self.labelclose.setMinimumSize(QtCore.QSize(30, 30))
        self.labelclose.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.labelclose.setFont(font)
        self.labelclose.setStyleSheet("QLabel{\n"
"   color:white;\n"
"   border:0px;\n"
"}\n"
"QLabel:hover{\n"
"\n"
"   background-color:red;\n"
"\n"
"}")
        self.labelclose.setAlignment(QtCore.Qt.AlignCenter)
        self.labelclose.setObjectName("labelclose")
        self.horizontalLayout_10.addWidget(self.labelclose)
        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 5)
        self.horizontalLayout_10.setStretch(2, 20)
        self.horizontalLayout_10.setStretch(3, 1)
        self.horizontalLayout_10.setStretch(4, 1)
        self.verticalLayout_4.addWidget(self.widget_2)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.composeButton = QtWidgets.QPushButton(self.frame_2)
        self.composeButton.setMinimumSize(QtCore.QSize(91, 51))
        self.composeButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.composeButton.setStyleSheet("/*QPushButton{\n"
"\n"
"border: none;\n"
"\n"
"}\n"
"QPushButton:hover{\n"
"  background-color: qconicalgradient(cx:0.5, cy:0.522909, angle:179.9, stop:0.494318 rgba(181, 225, 250, 255), stop:0.5 rgba(222, 242, 251, 255));\n"
"\n"
"}\n"
"QPushButton:pressed{\n"
"  background-color: qconicalgradient(cx:0.5, cy:0.522909, angle:179.9, stop:0.494318 rgba(134, 198, 233, 255), stop:0.5 rgba(206, 234, 248, 255));\n"
" \n"
"}\n"
"*/")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ui/manwindow/file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.composeButton.setIcon(icon1)
        self.composeButton.setIconSize(QtCore.QSize(30, 30))
        self.composeButton.setObjectName("composeButton")
        self.horizontalLayout.addWidget(self.composeButton)
        self.refreshButton = QtWidgets.QPushButton(self.frame_2)
        self.refreshButton.setMinimumSize(QtCore.QSize(91, 51))
        self.refreshButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.refreshButton.setStyleSheet("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ui/manwindow/刷新.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshButton.setIcon(icon2)
        self.refreshButton.setIconSize(QtCore.QSize(30, 30))
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout.addWidget(self.refreshButton)
        self.contactlistButton = QtWidgets.QPushButton(self.frame_2)
        self.contactlistButton.setMinimumSize(QtCore.QSize(91, 51))
        self.contactlistButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.contactlistButton.setStyleSheet("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ui/manwindow/通讯录.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.contactlistButton.setIcon(icon3)
        self.contactlistButton.setIconSize(QtCore.QSize(30, 30))
        self.contactlistButton.setObjectName("contactlistButton")
        self.horizontalLayout.addWidget(self.contactlistButton)
        self.horizontalLayout_8.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(205, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setLineWidth(1)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_7.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.searchlabel = QtWidgets.QLabel(self.frame_3)
        self.searchlabel.setMinimumSize(QtCore.QSize(25, 25))
        self.searchlabel.setMaximumSize(QtCore.QSize(22, 25))
        self.searchlabel.setStyleSheet("\n"
"border:2px solid gray;\n"
"border-top-left-radius:10px;\n"
"border-bottom-left-radius:10px;\n"
"padding:2px 2px;\n"
"border-right: none; \n"
"border-color:silver;\n"
"\n"
"background-color: #AAA;\n"
"color: #000;")
        self.searchlabel.setText("")
        self.searchlabel.setPixmap(QtGui.QPixmap("search24.png"))
        self.searchlabel.setObjectName("searchlabel")
        self.horizontalLayout_7.addWidget(self.searchlabel)
        self.searchEdit = QtWidgets.QLineEdit(self.frame_3)
        self.searchEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.searchEdit.setSizeIncrement(QtCore.QSize(0, 24))
        self.searchEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.searchEdit.setStyleSheet("border:2px solid gray;\n"
"padding:2px 2px; \n"
"border-left: 0px;\n"
"border-right:0px;\n"
"border-color:silver;\n"
"\n"
"background-color: #AAA;\n"
"    color: #000;\n"
"\n"
"\n"
"")
        self.searchEdit.setText("")
        self.searchEdit.setObjectName("searchEdit")
        self.horizontalLayout_7.addWidget(self.searchEdit)
        self.Xlabel = QtWidgets.QLabel(self.frame_3)
        self.Xlabel.setMinimumSize(QtCore.QSize(25, 25))
        self.Xlabel.setMaximumSize(QtCore.QSize(25, 25))
        self.Xlabel.setStyleSheet("\n"
"border:2px solid gray;\n"
"border-top-right-radius:10px;\n"
"border-bottom-right-radius:10px;\n"
"padding:2px 2px;\n"
"border-color:silver;\n"
"border-left:none;\n"
"\n"
"\n"
"background-color: #AAA;\n"
"color: #000;\n"
"\n"
"")
        self.Xlabel.setText("")
        self.Xlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.Xlabel.setObjectName("Xlabel")
        self.horizontalLayout_7.addWidget(self.Xlabel)
        self.searchlabel.raise_()
        self.Xlabel.raise_()
        self.searchEdit.raise_()
        self.horizontalLayout_8.addWidget(self.frame_3)
        self.horizontalLayout_8.setStretch(0, 2)
        self.horizontalLayout_8.setStretch(1, 1)
        self.horizontalLayout_8.setStretch(2, 2)
        self.verticalLayout_4.addWidget(self.frame_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.treeMailWidget = QtWidgets.QTreeWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Fax")
        font.setPointSize(15)
        self.treeMailWidget.setFont(font)
        self.treeMailWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeMailWidget.setObjectName("treeMailWidget")
        self.treeMailWidget.headerItem().setText(0, "常用文件夹")
        font = QtGui.QFont()
        font.setFamily("Adobe 宋体 Std L")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.treeMailWidget.headerItem().setFont(0, font)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Folder_Open_128px_1072492_easyicon.net.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.treeMailWidget.headerItem().setIcon(0, icon4)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeMailWidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Fax")
        font.setPointSize(15)
        item_0.setFont(0, font)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("ui/manwindow/email.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon5)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeMailWidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Fax")
        font.setPointSize(15)
        item_0.setFont(0, font)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("ui/manwindow/template-default.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon6)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeMailWidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Fax")
        font.setPointSize(15)
        item_0.setFont(0, font)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("ui/manwindow/paper_plane.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon7)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeMailWidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Fax")
        font.setPointSize(15)
        item_0.setFont(0, font)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("ui/manwindow/删除 (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_0.setIcon(0, icon8)
        self.treeMailWidget.header().setVisible(False)
        self.treeMailWidget.header().setHighlightSections(True)
        self.treeMailWidget.header().setMinimumSectionSize(30)
        self.horizontalLayout_3.addWidget(self.treeMailWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        self.listEmails = QtWidgets.QTreeWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.listEmails.setFont(font)
        self.listEmails.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listEmails.setStyleSheet("")
        self.listEmails.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.listEmails.setAlternatingRowColors(False)
        self.listEmails.setAutoExpandDelay(-1)
        self.listEmails.setExpandsOnDoubleClick(True)
        self.listEmails.setColumnCount(1)
        self.listEmails.setObjectName("listEmails")
        self.listEmails.headerItem().setText(0, "1")
        self.listEmails.header().setVisible(False)
        self.verticalLayout.addWidget(self.listEmails)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnReply = QtWidgets.QPushButton(self.centralwidget)
        self.btnReply.setMinimumSize(QtCore.QSize(170, 30))
        self.btnReply.setMaximumSize(QtCore.QSize(16777215, 30))
        self.btnReply.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnReply.setStyleSheet("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("ui/manwindow/回复.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnReply.setIcon(icon9)
        self.btnReply.setObjectName("btnReply")
        self.horizontalLayout_2.addWidget(self.btnReply)
        self.btnForward = QtWidgets.QPushButton(self.centralwidget)
        self.btnForward.setMinimumSize(QtCore.QSize(171, 30))
        self.btnForward.setMaximumSize(QtCore.QSize(16777215, 30))
        self.btnForward.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnForward.setStyleSheet("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("ui/manwindow/转发.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnForward.setIcon(icon10)
        self.btnForward.setObjectName("btnForward")
        self.horizontalLayout_2.addWidget(self.btnForward)
        self.btnDelete = QtWidgets.QPushButton(self.centralwidget)
        self.btnDelete.setMinimumSize(QtCore.QSize(170, 30))
        self.btnDelete.setMaximumSize(QtCore.QSize(16777215, 30))
        self.btnDelete.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnDelete.setStyleSheet("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("ui/manwindow/删除.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDelete.setIcon(icon11)
        self.btnDelete.setObjectName("btnDelete")
        self.horizontalLayout_2.addWidget(self.btnDelete)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(527, 80))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.sublabel = QtWidgets.QLabel(self.frame)
        self.sublabel.setMinimumSize(QtCore.QSize(165, 17))
        self.sublabel.setMaximumSize(QtCore.QSize(165, 17))
        self.sublabel.setObjectName("sublabel")
        self.horizontalLayout_4.addWidget(self.sublabel)
        self.subdisplay = QtWidgets.QLabel(self.frame)
        self.subdisplay.setMinimumSize(QtCore.QSize(329, 17))
        self.subdisplay.setMaximumSize(QtCore.QSize(329, 17))
        self.subdisplay.setText("")
        self.subdisplay.setObjectName("subdisplay")
        self.horizontalLayout_4.addWidget(self.subdisplay)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.fromlabel = QtWidgets.QLabel(self.frame)
        self.fromlabel.setMinimumSize(QtCore.QSize(165, 17))
        self.fromlabel.setMaximumSize(QtCore.QSize(165, 17))
        self.fromlabel.setObjectName("fromlabel")
        self.horizontalLayout_5.addWidget(self.fromlabel)
        self.fromdisplay = QtWidgets.QLabel(self.frame)
        self.fromdisplay.setMinimumSize(QtCore.QSize(329, 17))
        self.fromdisplay.setMaximumSize(QtCore.QSize(329, 17))
        self.fromdisplay.setText("")
        self.fromdisplay.setObjectName("fromdisplay")
        self.horizontalLayout_5.addWidget(self.fromdisplay)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.datelabel = QtWidgets.QLabel(self.frame)
        self.datelabel.setMinimumSize(QtCore.QSize(165, 17))
        self.datelabel.setMaximumSize(QtCore.QSize(165, 17))
        self.datelabel.setObjectName("datelabel")
        self.horizontalLayout_6.addWidget(self.datelabel)
        self.datedisplay = QtWidgets.QLabel(self.frame)
        self.datedisplay.setMinimumSize(QtCore.QSize(329, 17))
        self.datedisplay.setMaximumSize(QtCore.QSize(329, 17))
        self.datedisplay.setText("")
        self.datedisplay.setObjectName("datedisplay")
        self.horizontalLayout_6.addWidget(self.datedisplay)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addWidget(self.frame)
        self.emailPreview = QtWebKitWidgets.QWebView(self.centralwidget)
        self.emailPreview.setMinimumSize(QtCore.QSize(0, 470))
        self.emailPreview.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.emailPreview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.emailPreview.setStyleSheet("")
        self.emailPreview.setUrl(QtCore.QUrl("about:blank"))
        self.emailPreview.setObjectName("emailPreview")
        self.verticalLayout_2.addWidget(self.emailPreview)
        self.widget_attach = QtWidgets.QWidget(self.centralwidget)
        self.widget_attach.setObjectName("widget_attach")
        self.verticalLayout_2.addWidget(self.widget_attach)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 4)
        self.verticalLayout_2.setStretch(2, 20)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3.setStretch(1, 2)
        self.horizontalLayout_3.setStretch(2, 3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionCompose = QtWidgets.QAction(MainWindow)
        self.actionCompose.setCheckable(False)
        self.actionCompose.setChecked(False)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCompose.setIcon(icon12)
        self.actionCompose.setObjectName("actionCompose")
        self.actionRefresh = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("1refresh_128px_1194515_easyicon.net.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon13)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionContactList = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("1point_list_128px_1190662_easyicon.net.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionContactList.setIcon(icon14)
        self.actionContactList.setObjectName("actionContactList")
        self.actionSearch = QtWidgets.QAction(MainWindow)
        self.actionSearch.setCheckable(True)
        self.actionSearch.setChecked(False)
        self.actionSearch.setEnabled(True)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSearch.setIcon(icon15)
        self.actionSearch.setObjectName("actionSearch")

        self.retranslateUi(MainWindow)
        self.actionQuit.triggered.connect(MainWindow.close)
        self.btnDelete.clicked.connect(MainWindow.onDelete)
        self.btnReply.clicked.connect(MainWindow.onReply)
        self.btnForward.clicked.connect(MainWindow.onForward)
        self.treeMailWidget.itemClicked['QTreeWidgetItem*','int'].connect(MainWindow.onFolderSelected)
        self.composeButton.clicked.connect(MainWindow.onComposeMail)
        self.refreshButton.clicked.connect(MainWindow.onRefresh)
        self.contactlistButton.clicked.connect(MainWindow.onContactList)
        self.listEmails.itemClicked['QTreeWidgetItem*','int'].connect(MainWindow.onMailSelected)
        self.comboBox.activated['int'].connect(MainWindow.OnActivated)
        self.searchEdit.textChanged['QString'].connect(MainWindow.ontextChanged)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Foxmail"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">Pxmail</span></p></body></html>"))
        self.labelmin.setText(_translate("MainWindow", "一"))
        self.labelmax.setText(_translate("MainWindow", "口"))
        self.labelclose.setText(_translate("MainWindow", "X"))
        self.composeButton.setText(_translate("MainWindow", "写邮件"))
        self.refreshButton.setText(_translate("MainWindow", "刷新"))
        self.contactlistButton.setText(_translate("MainWindow", "通讯录"))
        self.searchEdit.setPlaceholderText(_translate("MainWindow", "搜索邮件"))
        __sortingEnabled = self.treeMailWidget.isSortingEnabled()
        self.treeMailWidget.setSortingEnabled(False)
        self.treeMailWidget.topLevelItem(0).setText(0, _translate("MainWindow", "收件夹"))
        self.treeMailWidget.topLevelItem(1).setText(0, _translate("MainWindow", "草稿夹"))
        self.treeMailWidget.topLevelItem(2).setText(0, _translate("MainWindow", "已发送"))
        self.treeMailWidget.topLevelItem(3).setText(0, _translate("MainWindow", "已删除"))
        self.treeMailWidget.setSortingEnabled(__sortingEnabled)
        self.comboBox.setItemText(0, _translate("MainWindow", "排序：日期"))
        self.comboBox.setItemText(1, _translate("MainWindow", "排序：发信人"))
        self.comboBox.setItemText(2, _translate("MainWindow", "排序：主题"))
        self.btnReply.setText(_translate("MainWindow", "回复"))
        self.btnForward.setText(_translate("MainWindow", "转发"))
        self.btnDelete.setText(_translate("MainWindow", "删除"))
        self.sublabel.setText(_translate("MainWindow", "主题："))
        self.fromlabel.setText(_translate("MainWindow", "发信人："))
        self.datelabel.setText(_translate("MainWindow", "日期："))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionCompose.setText(_translate("MainWindow", "写邮件"))
        self.actionCompose.setToolTip(_translate("MainWindow", "Write new eMail"))
        self.actionCompose.setShortcut(_translate("MainWindow", "Alt+N"))
        self.actionRefresh.setText(_translate("MainWindow", "刷新"))
        self.actionRefresh.setToolTip(_translate("MainWindow", "Check for new eMails"))
        self.actionRefresh.setShortcut(_translate("MainWindow", "Alt+R"))
        self.actionContactList.setText(_translate("MainWindow", "通讯录"))
        self.actionSearch.setText(_translate("MainWindow", "查找"))

from PyQt5 import QtWebKitWidgets
# import resource_rc
# import style_rc
