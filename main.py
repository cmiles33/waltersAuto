import sys
import os
import threadedSearch
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog,QComboBox,QTextBrowser, QProgressBar,QLabel,QSlider)

from PySide2.QtGui import QPixmap, QColor

from PySide2.QtCore import QBasicTimer

from PySide2.QtCore import Qt

stepper = 0


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Automation.... WITH KITTENS!!!! AHHH I LOVE KITTENS")
        # Create Widgets
        self.fileLoader = QPushButton("Load Files")
        self.stopButton = QPushButton("Stop")
        self.fileBox = QComboBox()  # Holds name of files
        self.filePreview = QTextBrowser()  # Preview Files
        self.loadingBar = QProgressBar(self)
        self.preview = QTextBrowser()
        self.ConfirmButton = QPushButton("Start")
        # Variable Creation Area
        self.pictureDic = {}  # Holds the tings
        self.timerBool = bool
        # Create layout and add widgets
        layout = QVBoxLayout()
        # Design Area
        self.label2 = QLabel()
        self.label2.setText("Automating Kittens!")
        self.label2.setStyleSheet("QLabel { background-color : black; color : white; font-size: 20px; text-align : "
                                  "center; }")
        self.label = QLabel()
        pixmap = QPixmap('pictures/helloKitten.png')
        w = 440
        h = 200
        pixmap = pixmap.scaled(w, h, aspectMode=Qt.IgnoreAspectRatio, mode=Qt.FastTransformation)
        self.timer = QBasicTimer()
        self.step = 0
        self.label.setPixmap(pixmap)

        # Adding widgets to the layout
        layout.addWidget(self.label2)
        layout.addWidget(self.label)
        layout.addWidget(self.fileLoader)
        layout.addWidget(self.fileBox)
        layout.addWidget(self.filePreview)
        layout.addWidget(self.ConfirmButton)
        layout.addWidget(self.stopButton)
        self.loadingBar.setStyleSheet("QProgressBar::chunk {background-color: red}")
        layout.addWidget(self.loadingBar)
        # Enable Minimize and maximize
        self.setWindowFlag(Qt.WindowMinimizeButtonHint,True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        # Set layout
        self.setLayout(layout)
        p = self.palette()
        p.setColor(self.foregroundRole(),QColor(10,10,10,127))
        p.setColor(self.backgroundRole(),QColor(0,0,127,127))
        self.setPalette(p)
        self.setFixedWidth(450)
        self.setFixedHeight(700)
        # Connecting functions to buttons
        self.fileLoader.clicked.connect(self.loadFiles)
        self.ConfirmButton.clicked.connect(self.newStart)
        self.stopButton.clicked.connect(self.stop)
        self.fileBox.activated.connect(self.updatePreview)

    def start(self):
        print("Ready to Go")
        self.loadingBar.setStyleSheet("QProgressBar::chunk {background-color: gold } QProgressBar {text-align: center}")
        if bool(self.pictureDic) is False:
            self.filePreview.append("**** Empty Files **** \n")
            self.filePreview.append("**** Please load Files **** \n")
            self.timer.stop()
        else:
            self.filePreview.append("**** Starting Picture Search **** \n")
            self.searchThread = threadedSearch.thread_with_exception("Searching", self.pictureDic)
            self.searchThread.start()
        pixmap = QPixmap('pictures/pawwingKitten.jpg')
        w = 440
        h = 200
        pixmap = pixmap.scaled(w, h, aspectMode=Qt.IgnoreAspectRatio, mode=Qt.FastTransformation)
        self.label.setPixmap(pixmap)

    def loadFiles(self):
        print("We gone load them files doh")
        self.filePreview.append("**** Files Loaded **** \n")
        self.fileBox.clear()
        self.pictureDic.clear()
        with os.scandir('testpictures/') as files:
            for file in files:
                print(file.path)
                print(file.name)
                self.pictureDic.update({file.name: file.path})
                self.fileBox.addItem(file.name)
                self.filePreview.append("{} \n".format(file.name))
        self.filePreview.append("**** Files done loading **** \n")

    def newStart(self):
        pixmap = QPixmap('pictures/roaringKitten.jpg')
        w = 440
        h = 200
        pixmap = pixmap.scaled(w, h, aspectMode=Qt.IgnoreAspectRatio, mode=Qt.FastTransformation)
        self.label.setPixmap(pixmap)
        self.timerBool = True
        global stepper
        stepper = 0
        self.loadingBar.setValue(0)
        self.loadingBar.setStyleSheet("QProgressBar::chunk {background-color: red;} QProgressBar {text-align: center}")
        self.startTracking()

    def updatePreview(self):
        self.label.clear()
        location = self.pictureDic[self.fileBox.currentText()]
        pixmap = QPixmap('{}'.format(location))
        w = 440
        h = 200
        pixmap = pixmap.scaled(w, h, aspectMode=Qt.IgnoreAspectRatio, mode=Qt.FastTransformation)
        self.timer = QBasicTimer()
        self.step = 0
        self.label.setPixmap(pixmap)

    def startTracking(self):
        self.timer.start(80,self)

    def stop(self):
        self.timer.stop()
        try:
            self.searchThread.raise_exception()
            self.searchThread.join()
            self.filePreview.append("**** Sucessfully Killed thread **** \n")
        except:
            self.filePreview.append("**** No thread to kill! **** \n")
        pixmap = QPixmap('pictures/sadkitten.jpg')
        w = 440
        h = 200
        pixmap = pixmap.scaled(w, h, aspectMode=Qt.IgnoreAspectRatio, mode=Qt.FastTransformation)
        self.label.setPixmap(pixmap)
        self.loadingBar.setValue(0)

    def timerEvent(self, event):
        if self.timerBool is True:
            global stepper
            stepper +=1
            self.loadingBar.setValue(stepper)
            if self.loadingBar.value() == 100:
                self.start()
                self.timerBool = False
                self.loadingBar.setStyleSheet(
                    "QProgressBar::chunk {background-color: green;} QProgressBar {text-align: center}")
        else:
            try:
                printingMess = self.searchThread.getMessage()
                if printingMess !="":
                    self.filePreview.append("{} \n".format(printingMess))
            except:
                self.filePreview.append(" *** No information from Thread *** \n")


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())