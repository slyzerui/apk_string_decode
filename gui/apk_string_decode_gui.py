
from core_logic.apk_string_decode_main_core_logic import *

import sys
import socket
import json
import threading

from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QTextEdit, QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, QDialog, QScrollArea
from PyQt5.QtCore import QThread, pyqtSignal, QObject, Qt

# Global QApplication instance
app = None

class GUIWarningHandler(WarningHandlerInterface):
    def __init__(self):
        self.app = QApplication(sys.argv)
        # Ensure a QApplication exists before creating any QWidget
        self.app = QApplication.instance() or QApplication(sys.argv)


    def warn(self, message):
        showWarningMessage(message)
        # Handle the case where QApplication.exec_() might be needed.
        # You can check if the application is already running and only call exec_ if it is not.
        if not QApplication.instance():
            sys.exit(self.app.exec_())


def showWarningMessage(message):
    QMessageBox.warning(None, "Warning", message)

# Inputs Window
class FileDropLabel(QLabel):
    fileDropped = pyqtSignal(str)

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: white;")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.fileDropped.emit(files[0])

class InputCollector(QObject):
    # Signal now carries two strings
    textSubmitted = pyqtSignal(str, str)

class InputsMainWindow(QDialog):
    def __init__(self, collector):
        super().__init__()
        self.collector = collector
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Drag and Drop File + Text Input')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.fileLabel = FileDropLabel('Drag and drop a file here', self)
        self.fileLabel.fileDropped.connect(self.onFileDropped)

        self.javaSignature = QLineEdit(self)
        self.javaSignature.setPlaceholderText('Enter the Java Signature')

        self.startButton = QPushButton('Start', self)
        self.startButton.clicked.connect(self.onStartClicked)

        layout.addWidget(self.fileLabel)
        layout.addWidget(self.javaSignature)
        layout.addWidget(self.startButton)

        self.setLayout(layout)  # For QDialog, set the layout directly

        self.filePath = ''
        self.enteredText = ''

    def onFileDropped(self, path):
        self.filePath = path
        self.fileLabel.setText(f'File: {path}')

    def onStartClicked(self):
        self.javaSignatureText = self.javaSignature.text()
        print(f'File Path: {self.filePath}')
        print(f'Java Signature Text: {self.javaSignatureText}')

        if (not isJavaSignatureValid(self.javaSignatureText)):
            showWarningMessage("Please insert a valid Java signature")
        elif (not self.filePath):
            showWarningMessage("Please insert a valid Apk path")
        else:

            #enteredText = self.javaSignature.text()
            self.collector.textSubmitted.emit(self.javaSignatureText, self.filePath)  # Emit the signal with the entered text
            self.close()

            #setInputParameters(self.javaSignatureText, self.filePath)
            #self.mainmenuWindow = MainMenuWindow()
            #self.mainmenuWindow.show()
            #self.close()


def get_gui_user_input():
    #global app
    #app = QApplication([])  # This should ideally be outside and called once
    collector = InputCollector()
    dialog = InputsMainWindow(collector)
    
    inputTexts = []
    
    def on_text_submitted(text1, text2):
        inputTexts.extend([text1, text2])
        dialog.accept()  # Close the dialog

    collector.textSubmitted.connect(on_text_submitted)
    
    if dialog.exec_() == QDialog.Accepted:
        print("Dialog was accepted")
    else:
        print("Dialog was rejected or closed")

    return inputTexts if inputTexts else (None, None)



# Main Menu Window
class MainMenuCollector(QObject):
    # Signal now carries two strings
    stringSubmitted = pyqtSignal(str)

class MainMenuWindow(QDialog):
    def __init__(self, collector):
        super().__init__()
        self.collector = collector
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Menu')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.textInput = QLineEdit(self)
        self.textInput.setPlaceholderText('Place holder for App information')

        self.startButton1 = QPushButton('1. Decode the Whole App', self)
        self.startButton1.clicked.connect(self.onStartClicked1)

        self.startButton2 = QPushButton('2. Decode 1 String', self)
        self.startButton2.clicked.connect(self.onStartClicked1)

        self.startButton3 = QPushButton('3. Add another Java signature call and Decode the Whole App', self)
        self.startButton3.clicked.connect(self.onStartClicked1)

        self.startButton4 = QPushButton('4. Use already decompile App to trigger Decode', self)
        self.startButton4.clicked.connect(self.onStartClicked1)

        self.startButton5 = QPushButton('5. Exit', self)
        self.startButton5.clicked.connect(self.onStartClicked1)

        layout.addWidget(self.textInput)
        layout.addWidget(self.startButton1)
        layout.addWidget(self.startButton2)
        layout.addWidget(self.startButton3)
        layout.addWidget(self.startButton4)
        layout.addWidget(self.startButton5)

        self.setLayout(layout)


    def onStartClicked1(self):
        print("1. Decode the Whole App")
        self.collector.stringSubmitted.emit("1")
        self.close()
    
    def onStartClicked2(self):
        print("2. Decode 1 String")
        self.collector.stringSubmitted.emit("2")
        self.close()

    def onStartClicked3(self):
        print("3. Add another Java signature call and Decode the Whole App")
        self.collector.stringSubmitted.emit("3")
        self.close()
    
    def onStartClicked4(self):
        print("4. Use already decompile App to trigger Decode")
        self.collector.stringSubmitted.emit("4")
        self.close()

    def onStartClicked5(self):
        print("5. Exit")
        self.close()

def gui_main_menu():
    #if __name__ == '__main__':
    #global app
    #app = QApplication([])
    collector = MainMenuCollector()
    mainmenuWindow = MainMenuWindow(collector)
    inputNumber = []

    def on_number_submitted(string):
        inputNumber.extend(string)
        #mainmenuWindow.accept()

    collector.stringSubmitted.connect(on_number_submitted)
    if mainmenuWindow.exec_() == QDialog.Accepted:
        print("Dialog was accepted")
    else:
        print("Dialog was rejected or closed")

    # Block until the window is closed and text is submitted
    #app.exec_()

    return inputNumber if inputNumber else (None)    


class LoadingScreen(QDialog):
    def __init__(self, parent=None):
        #super(LoadingScreen, self).__init__(parent)
        super().__init__(parent)
        #self.setWindowTitle("Loading")
        self.setWindowTitle("Processing... Please wait.")
        self.setGeometry(100, 100, 500, 500)  # Position and size: x, y, width, height
        self.initUI()
        #self.setModal(True)  # Make the dialog modal

    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Starting...")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.label.setWordWrap(True)

        # Setup scroll area
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollWidget = QWidget()
        scrollLayout = QVBoxLayout(scrollWidget)
        scrollLayout.addWidget(self.label)
        scrollArea.setWidget(scrollWidget)

        layout.addWidget(self.label)
        self.setLayout(layout)



    def updateMessage(self, message):
        current_text = self.label.text()
        new_text = current_text + "\n" + message
        self.label.setText(new_text)
        self.label.scroll(0, 0)
