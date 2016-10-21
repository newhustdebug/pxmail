#-*-coding:utf-8 -*-

import time
import sys
from utils.mailHelper import mailHelper
from utils.configReader import configReader

reload(sys)
sys.setdefaultencoding('utf-8')

class MCC(object):
    CONFIGPATH = '_config.ini'
    KEY_COMMAND = 'Command'
    KEY_OPEN = 'Open'
    KEY_BOSS = 'Boss'
    KEY_TIMELIMIT = 'timelimit'

    def __init__(self):
        self.mailHelper = mailHelper()
        self.configReader = configReader(self.CONFIGPATH)
        self.timeLimit = int(self.configReader.readConfig(self.KEY_BOSS, self.KEY_TIMELIMIT))
        self.toRun()

    def toRun(self):
        while True:
            self.mailHelper = mailHelper()
            self.run()
            time.sleep(self.timeLimit)

    def run(self):
        mailBody = self.mailHelper.acceptMail()             #接收邮件


if __name__=='__main__':
        mcc = MCC()
