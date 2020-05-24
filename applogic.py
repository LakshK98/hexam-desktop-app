import sys
from PyQt5.QtCore import pyqtSlot,QTimer
import json
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.uic import loadUi
from ui import *
from TestDetailsWindow import TestDetailsWindow
from TestWindow import TestWindow
from SubmitWindow import SubmitWindow
from MonitoringThread import MonitoringThread
dummy_data='{ ' \
           '  "test_id": 123,' \
           '  "test_title":"Advanced Internet Technology",' \
           '  "test_description":"Second Unit Test",' \
           '  "test_duration":1,' \
           '  "test_deadline":"19/05/20 19:55:00",' \
           '  "student_img":"base64string",' \
           '  "eye_track":false,' \
           ' "questions":[' \
           '    {' \
           '      "question_id":1,' \
           '      "question_type":0,' \
           '      "question":"What is all this?",' \
           '      "options":["this","that","all this","all that"]' \
           '    },' \
           '    {' \
           '      "question_id":2,' \
           '      "question_type":1,' \
           '      "question":"What is all this answer briefly?"' \
           '    }' \
           '    ]' \
           '}'

class MainPage(QMainWindow):
    def __init__(self):
        super(MainPage,self).__init__()

        loadUi('ui/firstpage.ui',self)

        self.pushButton.clicked.connect(self.moveToTestDetails)



    def moveToTestDetails(self):
        self.test_details_dict=json.loads(dummy_data)

        self.hide()
        self.testDetails = TestDetailsWindow(self.test_details_dict)
        self.testDetails.startTestSignal.connect(self.moveToTestWindow)

        self.testDetails.show()


    def moveToTestWindow(self):

        self.testDetails.hide()
        self.testWindow = TestWindow(self.test_details_dict)

        self.monitorThread= MonitoringThread(self.test_details_dict['eye_track'])
        self.monitorThread.report_signal.connect(self.monitor_report_slot)
        self.total_frames=-1
        self.monitorThread.start()
        self.testWindow.show()
        self.testWindow.pushButton_3.clicked.connect(self.submit_test)
        self.testWindow.setFocus()
        app.focusChanged.connect(self.onFocusChange)

        self.timer_start()

    def monitor_report_slot(self,verifiedFramesCount,eyeTrackSuspicionCount,total_frames):

        self.testWindow.hide()
        test_duration_seconds = self.test_details_dict['test_duration'] * 60
        app_switch_percent = int(
            (self.offscreen_time / test_duration_seconds * 100))
        self.testWindow.qtimer.stop()



        # face_sus = int((verifiedFramesCount / total_frames) * 100)
        # if(verifiedFramesCount==total_frames):
        #     eye_sus=0
        # else:
        #     eye_sus = int((eyeTrackSuspicionCount / verifiedFramesCount) * 100)

        print("Eye track",self.test_details_dict['eye_track'])
        self.submitWindow = SubmitWindow(self.test_details_dict['eye_track'],self.offscreen_time, app_switch_percent, verifiedFramesCount, eyeTrackSuspicionCount,total_frames)

        self.submitWindow.show()

    def onFocusChange(self):
        print("is active:",self.testWindow.isActiveWindow())

        try:

            self.submitWindow.isActiveWindow()
            print("here")
        except:
            if not self.testWindow.isActiveWindow():
                self.offscreen_interval = self.min_left * 60 + self.sec_left
            else:

                self.offscreen_time += self.offscreen_interval - (self.min_left * 60 + self.sec_left)
                self.offscreen_interval = self.min_left * 60 + self.sec_left


    def timer_start(self):
        self.min_left = self.test_details_dict['test_duration']
        self.sec_left = 0
        self.offscreen_time=0
        self.testWindow.qtimer.timeout.connect(self.timer_timeout)
        self.testWindow.qtimer.start(1000)

        self.update_timer()

    def timer_timeout(self):
        if self.min_left==0 and self.sec_left==0:
            self.testWindow.qtimer.stop()
            self.submit_test()

        elif(self.sec_left==0):
            self.min_left-=1
            self.sec_left=59

        else:
            self.sec_left-=1


        self.update_timer()

    def update_timer(self):
        self.testWindow.label_3.setText(str(self.min_left))
        self.testWindow.label_5.setText(str(self.sec_left))


    def submit_test(self):
        self.testWindow.label_7.setVisible(True)

        self.monitorThread.stop=True



def focus():
    print("fuckus")
app =QApplication(sys.argv)
widget=MainPage()
widget.show()

# app.focusWindowChanged(focus)
sys.exit(app.exec_())
