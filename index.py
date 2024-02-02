

import io
import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import  *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget
import cv2

import google.generativeai as genai
# from google.cloud import vision
from google.auth import credentials
import google.auth

from PyQt5 import uic


from PIL import Image

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/maria/Downloads/identifytext-387022-636ef47771a2.json" # My file of Service Account at Project with GenerativeAI enable

# link of Linkedin video https://www.linkedin.com/events/7158924618618089475/theater
# link of Youtube video https://youtube.com/live/Hsdz3F-JjVU
# link of Github code https://github.com/marianoaloi/GeminiDemo

# Create your virtual environment python -m venv venv
# Activate your virtual environment venv/Scripts/activate.bat (Windows like the live) or venv/bin/activate (Linux)
# install libraries pip install -r requirements.txt

# You neeed create a GCP project , enable the generativelibrary in your project , create a user account , dowload the user account key, setup the user account key file to link the environment variable "GOOGLE_APPLICATION_CREDENTIALS"
# At lest go to https://makersuite.google.com/app/prompts/new_freeform and create your API key access that you will put in the environment variable KEY_GEMENI

class Util:
    def convertMillis(millis:int):
        seconds=(millis/1000)%60
        minutes=(millis/(1000*60))%60
        hours=(millis/(1000*60*60))%24
        return '{0:02d}:{1:02d}:{2:02d}'.format(int(hours),int(minutes), int(seconds))

class GeminiDemo(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.cred = google.auth
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)),"interface.ui"), self)

        self.playbutton.setEnabled(False)
        self.playbutton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.playbutton.clicked.connect(self.play_video)

        self.mediaPlayer = QMediaPlayer(parent=self.centralwidget,flags=QMediaPlayer.VideoSurface)

        self.volume = 50
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        self.video = QVideoWidget()
        # self.video.setStyleSheet('background-color:lightgreen')
        self.video.setObjectName("mediaPlayer")
        self.mediaPlayer.setVideoOutput(self.video)

        self.actionOpen.triggered.connect(self.openFile)

        vbox = QVBoxLayout()
        vbox.addWidget(self.video)
        self.videoWidget.setLayout(vbox)

        #create slider
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)

        self.sendQuestion.clicked.connect(self.actSendQuestion)
        self.btgetframe.clicked.connect(self.actGetFrame)

        
        genai.configure(api_key=os.getenv("KEY_GEMENI"))
        self.model = genai.GenerativeModel('gemini-pro-vision')

        self.actualImageQuestion = None


    def actSendQuestion(self):
        if(self.actualImageQuestion):
            try:
                question=self.MakeQuestion.toPlainText()
                response = self.model.generate_content([question,self.actualImageQuestion])
                # self.writeResponse(f"\n\n\n {self.getText(frame)}")
                self.writeResponse(f"\n====================\n {response.text}")
            except Exception as e:
                print(str(e))

    def actGetFrame(self):
        position=self.get_position()
        video = cv2.VideoCapture(self.filePathVideo.text())        
        video.set(cv2.CAP_PROP_POS_MSEC,position)
        if(position != round(video.get(cv2.CAP_PROP_POS_MSEC))):
            video.set(cv2.CAP_PROP_POS_FRAMES,round((position/1000)*video.get(cv2.CAP_PROP_FPS)))
        ret,frame = video.read()
        if(ret):
            self.actualImageQuestion = Image.fromarray(frame,"RGB")
            self.actualImageQuestion.save(self.filePathVideo.text()+".jpg")

        try:
            question="How is the correct answer? How is the Question number? How is the total of questions? Return the text you can read. If you can , please, explain why the answer is correct."
            response = self.model.generate_content([question,self.actualImageQuestion])
            # self.writeResponse(f"\n\n\n {self.getText(frame)}")
            self.writeResponse(f"\n====================\n {response.text}")
        except Exception as e:
            print(str(e))

    def writeResponse(self,text):
        self.GeminiResponse.setPlainText(f"{self.GeminiResponse.toPlainText()}{text}")
        
    def mediastate_changed(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playbutton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.playbutton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

            

    def position_changed(self,position):
        if(not position ):
            position=self.get_position() 
        self.slider.setValue(position)
        self.durationtime.setText(Util.convertMillis(position))

    def duration_changed(self,duration):
        
        self.slider.setRange(0, duration)
        self.maxDuration=duration        


    def set_position(self,position):
        self.mediaPlayer.setPosition(int(position))

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def get_position(self):
        return self.mediaPlayer.position()
    
    
    def openFile(self):
        
        fileName = QFileDialog.getOpenFileName(self,
            "Open Video", filter= "Video Files (*.mp4 *.avi *.m4v *.3gp *.wmv *.mkv *.mpv)")
        if(fileName[0] ):
           self.openVideoFile(fileName[0])
    
    def openVideoFile(self,filePath):


        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filePath)))
        self.mediaPlayer.setVolume(50);
        self.mediaPlayer.setPosition(0) # to start at the beginning of the video every time
        self.mediaPlayer.play();


        self.playbutton.setEnabled(True)
        self.filePathVideo.setText(filePath)




if __name__ == "__main__"   :
    app = QApplication(sys.argv)
    window = GeminiDemo()
    window.show()

    sys.exit(app.exec())