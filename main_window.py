# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
import speech_recognition as sr
import pyaudio
import wave
from PyQt5.QtCore import pyqtSlot

class Recorder(object):
    '''A recorder class for recording audio to a WAV file.
    Records in mono by default.
    '''

    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer)

class RecordingFile(object):
    def __init__(self, fname, mode, channels,
                rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        # Use a stream with no callback function in blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer)
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        # Use a stream with a callback in non-blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback


    def close(self):
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile


class Ui_MainWindow(QtWidgets.QWidget):

    # @pyqtSlot()
    def fn_record(self):
        self.recfile.start_recording()

    @pyqtSlot()
    def fn_stop(self):
        self.recfile.stop_recording()
        self.Recognize()


    def setupUi(self, MainWindow):
        self.rec = Recorder(channels=2)
        self.recfile = self.rec.open('say_something.wav', 'wb')
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1005, 809)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_rec = QtWidgets.QPushButton(self.centralwidget)
        self.btn_rec.setGeometry(QtCore.QRect(930, 700, 71, 31))
        self.btn_rec.setObjectName("btn_rec")
        self.btn_stop = QtWidgets.QPushButton(self.centralwidget)
        self.btn_stop.setGeometry(QtCore.QRect(860, 700, 61, 31))
        self.btn_stop.setObjectName("btn_stop")

        self.txt_speech_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_speech_text.setGeometry(QtCore.QRect(10, 10, 981, 361))
        self.txt_speech_text.setObjectName("txt_speech_text")
        self.btn_analyze = QtWidgets.QPushButton(self.centralwidget)
        self.btn_analyze.setGeometry(QtCore.QRect(900, 380, 91, 41))
        self.btn_analyze.setObjectName("btn_analyze")
        self.lst_voca = QtWidgets.QListWidget(self.centralwidget)
        self.lst_voca.setGeometry(QtCore.QRect(10, 380, 241, 351))
        self.lst_voca.setObjectName("lst_voca")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(270, 380, 501, 351))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.lbl_stats = QtWidgets.QLabel(self.centralwidget)
        self.lbl_stats.setGeometry(QtCore.QRect(800, 440, 181, 231))
        self.lbl_stats.setText("")
        self.lbl_stats.setObjectName("lbl_stats")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1005, 36))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuLoad = QtWidgets.QMenu(self.menubar)
        self.menuLoad.setObjectName("menuLoad")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuLoad.menuAction())
        self.retranslateUi(MainWindow)


        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # @pyqtSlot()
    # def btn_rec(self):
    #     self.recfile.start_recording()
    #
    # @pyqtSlot()
    # def btn_stop(self):
    #     self.recfile.stop_recording()
    #     self.Recognize()

    def Recognize(self):
        r = sr.Recognizer()
        with sr.WavFile("say_something.wav") as source:
            audio = r.listen(source)
        try:
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        # self.txt_speech_text.setPlainText(r.recognize_google(audio)+'\r')
        self.txt_speech_text.appendPlainText(r.recognize_google(audio))

    def hello(self):
        print("hello")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_rec.setText(_translate("MainWindow", "Rec"))
        self.btn_stop.setText(_translate("MainWindow", "Stop"))

        self.btn_rec.clicked.connect(self.fn_record)
        self.btn_stop.clicked.connect(self.fn_stop)

        self.btn_analyze.setText(_translate("MainWindow", "Analyze"))
        self.menuFile.setTitle(_translate("MainWindow", "Save"))
        self.menuLoad.setTitle(_translate("MainWindow", "Load"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

