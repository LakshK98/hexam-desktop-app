import sys
from PyQt5.QtCore import QTimer

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from QuestionMCQWidget import QuestionMCQWidget
from QuestionBriefWidget import QuestionBriefWidget

from ui import *


class SubmitWindow(QMainWindow):
    def __init__(self,eye_track,switch_duration,app_switching_percent,face_sus,eye_sus,total_frames):

        super(SubmitWindow,self).__init__()
        loadUi('ui/submitwindow.ui',self)
        print("switch_duration",switch_duration)
        self.label_3.setText(str(int(switch_duration/60)))
        self.label_5.setText(str(switch_duration%60))

        self.label_8.setText(str(app_switching_percent)+"%")

        self.label_10.setText(str(face_sus)+"/"+str(total_frames))

        self.label_14.setText(str(eye_sus)+"/"+str(total_frames-face_sus))
        self.label_13.setHidden(not eye_track)
        self.label_14.setHidden(not eye_track)