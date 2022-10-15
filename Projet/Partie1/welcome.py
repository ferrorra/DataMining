from ast import For
from cProfile import label
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QMainWindow
from PyQt5.QtGui import QMovie
import sys, res
import workspace
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QRect
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMainWindow, QLabel, QDesktopWidget
import pandas as pd

class Ui_Form(QMainWindow):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(796, 704)
        Form.setWindowFlags(Qt.FramelessWindowHint)
        Form.setAttribute(Qt.WA_TranslucentBackground)
        Form.setMinimumSize(QtCore.QSize(600, 700))
        self.setWindowIcon(QtGui.QIcon('resources/puzzle.png'))
        Form.setWindowTitle("Data Mining Project")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 20, 771, 671))
        self.widget.setStyleSheet("QPushButton#pushButton{\n"
"border-radius: 50%;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(80, 192, 255), stop:1 rgb(98, 205, 255));\n"
"}\n"
"QPushButton#pushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(98, 205, 255), stop:1 rgb(80, 192, 255));\n"
"border: 5px double #ffd956;\n"
"\n"
"}\n"
"")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(30, 10, 471, 631))
        self.label.setStyleSheet("border-top-left-radius:70px;\n"
"background-color:white;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(500, 10, 251, 631))
        self.label_2.setStyleSheet("background-color:white;\n"
"border-bottom-right-radius:70px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(-20, 580, 111, 101))
        self.label_3.setStyleSheet("border-image: url();\n"
"")

        self.movie = QMovie("resources/circle-chart.gif")
        self.label_3.setMovie(self.movie)
        #self.label.setScaledContents(True)
        self.movie.start()
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(400, 80, 281, 201))
        self.label_4.setStyleSheet("font: 87 10pt \"Roboto Black\";\n"
"font-size:50px;\n"
"color:rgb(43, 93, 147);\n"
"")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(400, 300, 281, 31))
        self.label_5.setStyleSheet("font: 87 10pt \"Roboto Bold\";\n"
"font-size:25px;\n"
"color:rgb(80, 192, 255);")
        self.label_5.setObjectName("label_5")
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setGeometry(QtCore.QRect(400, 350, 281, 271))
        self.label_8.setStyleSheet("font: 87 10pt \"Roboto Light\";\n"
"font-size:16px;\n"
"color:;\n"
"color: ;\n"
"color: rgb(43, 93, 147);\n"
"direction: rtl;\n"
"")
        self.label_8.setObjectName("label_8")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setGeometry(QtCore.QRect(0, 150, 350, 291))
        self.label_6.setStyleSheet("border-image:url();")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.movie = QMovie("resources/label-chart.gif")
        self.label_6.setMovie(self.movie)
        #self.label.setScaledContents(True)
        self.movie.start()
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setGeometry(QtCore.QRect(670,-20, 150, 112))
        self.label_7.setStyleSheet("border-image: url();\n"
"")
        self.movie = QMovie("resources/finance-analysis.gif")
        self.label_7.setMovie(self.movie)
        #self.label.setScaledContents(True)
        self.movie.start()


        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setGeometry(QtCore.QRect(590, 230, 81, 71))
        self.label_9.setStyleSheet("border-image: url(:/images/resources/customization.png);\n" #custumization.gif
"")
        self.movie = QMovie("resources/custumization.gif")
        self.label_9.setMovie(self.movie)
        self.label.setScaledContents(True)
        self.movie.start()



        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.widget)
        self.label_10.setGeometry(QtCore.QRect(10, 20, 141, 131))
        self.label_10.setStyleSheet("border-image: url();\n"
"")
        self.movie = QMovie("resources/creative-bulb.gif")
        self.label_10.setMovie(self.movie)
        #self.label.setScaledContents(True)
        self.movie.start()
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.widget)
        self.label_11.setGeometry(QtCore.QRect(90, 390, 261, 31))
        self.label_11.setStyleSheet("font: 87 10pt \"Roboto Bold\";\n"
"font-size:16px;\n"
"color:rgb(252, 55, 49);\n"
"direction: rtl;\n"
"")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.widget)
        self.label_12.setGeometry(QtCore.QRect(110, 600, 91, 31))
        self.label_12.setStyleSheet("font: 87 10pt \"Roboto Bold\";\n"
"font-size:16px;\n"
"color:rgb(16, 59, 95);\n"
"direction: rtl;\n"
"")
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.widget)
        self.label_13.setGeometry(QtCore.QRect(320, 480, 161, 151))
        self.label_13.setStyleSheet("border-image: url();")
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.movie = QMovie("resources/bar-chart.gif")
        self.label_13.setMovie(self.movie)
        #self.label.setScaledContents(True)
        self.movie.start()
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(120, 430, 90, 90))
        self.pushButton.setStyleSheet("border-radius:45%;\n"
"border: 5px double rgb(88, 248, 106);\n"
"color:rgb(255, 217, 86);\n"
"font-size:100px;\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.starting)
        self.pushButton.clicked.connect(Form.close)
        self.label.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius =25, xOffset=0, yOffset =0))
        self.label_2.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius =25, xOffset=0, yOffset =0))
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Data Mining Project"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p> Projet de </p><p>Data Mining </p><p>Partie 1</p></body></html>"))
        self.label_5.setText(_translate("Form", "Exploratory Data Analysis"))
        self.label_8.setText(_translate("Form", "<html><head/><body><p align=\"right\">Dans cette partie, nous nous </p><p align=\"right\"><span style=\" font-weight:600; font-style:italic;\">familiarisons</span></p><p align=\"right\">avec les données de notre </p><p align=\"right\"><span style=\" font-weight:600; font-style:italic;\">dataset</span></p><p align=\"right\">tout en extrayant des informations </p><p align=\"right\"><span style=\" font-weight:600; font-style:italic;\">utiles</span></p><p align=\"right\">et des connaissances </p><p align=\"right\"><span style=\" font-weight:600; font-style:italic;\">visualisables.</span></p><p align=\"right\"><br/></p></body></html>"))
        self.label_11.setText(_translate("Form", "<html><head/><body><p align=\"right\">Bourouina Rania, Chibane Ilies.</p></body></html>"))
        self.label_12.setText(_translate("Form", "<html><head/><body><p align=\"right\">Copyright ©</p></body></html>"))
        self.pushButton.setText(_translate("Form", "►"))

    def starting(self):
        self.window = QtWidgets.QWidget()
        self.ui = workspace.Ui_Form()
        self.ui.setupUi(self.window)
        self.window.show()
        self.ui.visualiser_dataset(self.ui.tableView)
        self.ui.infos(self.ui.tableView_2)
        self.ui.load_combo(self.ui.comboBox)
        self.ui.attributs(self.ui.tableView_3)
        self.ui.highlight(self.ui.comboBox, self.ui.tableView_3)
        self.ui.visualiser_dataset(self.ui.tableView_4)
        self.ui.load_combo(self.ui.comboBox_2)
        self.ui.load_combo(self.ui.comboBox_3)
        self.ui.load_combo(self.ui.comboBox_4)
        self.ui.load_combo(self.ui.comboBox_5)
        self.ui.load_combo(self.ui.comboBox_6)
        self.ui.load_combo(self.ui.comboBox_7)
        self.ui.load_combo(self.ui.comboBox_8)
        self.ui.tendances(self.ui.tableView_5)
        self.ui.mesures(self.ui.tableView_6)
        self.ui.plottingScatter(self.ui.tab_13,self.ui.verticalLayout_17,"Scatter", self.ui.comboBox_7.currentText(),self.ui.comboBox_8.currentText())
        self.ui.plottingHist(self.ui.tab_10,self.ui.verticalLayout_16,"Hist", self.ui.comboBox_6.currentText())
        self.ui.plottingMoustaches(self.ui.tab_12,self.ui.verticalLayout_13,"Moustaches", self.ui.comboBox_5.currentText())
        self.ui.highlight(self.ui.comboBox_4, self.ui.tableView_6)





if __name__=="__main__":
        app = QtWidgets.QApplication(sys.argv)
        Form = QtWidgets.QWidget()
        ui = Ui_Form()
        ui.setupUi(Form)
        Form.show()
        sys.exit(app.exec_())