#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import ui

app = QtWidgets.QApplication(sys.argv)



my_mainWindow = ui.AccountDialog()

my_mainWindow.show()

sys.exit(app.exec_())
