from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import matplotlib.pyplot as plt
import time
from sklearn.model_selection import train_test_split
from decision_tree import DecisionTree
from random_forest import RandomForest
from metrix import calculate_metrics, confusion_matrix
from visualize import drawtree



class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(1237, 843)
        Form.setStyleSheet("")
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.DF = pd.read_excel("data.xlsx")
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.ent =False
        self.dt_time=0.000
        self.rf_time=0.000
        self.tt=0.000
        self.labels = ["Attrition", "No Attrition"]

        self.tabWidget.setStyleSheet("QTabWidget::pane {\n"
"  border: 1px solid rgb(43, 93, 147);\n"
"  top:-1px; \n"
"  background: white;\n"
"} \n"
"\n"
"QTabBar::tab {\n"
"  background: rgb(255, 217, 86); \n"
"  decoration:none;\n"
"  border: 5px dashed rgb(255, 217, 86); \n"
"  padding: 15px;\n"
"  color:rgb(43, 93, 147);\n"
"} \n"
"\n"
"QTabBar::tab:selected { \n"
"  background: rgb(255, 217, 86); \n"
"  margin-bottom: -1px; \n"
"}\n"
"QLabel{\n"
"    color:rgb(252, 55, 49);\n"
"font: 87 28pt \"Aileron Heavy\";\n"
"padding:10px;\n"
"}\n"
"QPushButton { background-color: red;\n"
"color: white;\n"
"border-radius:5px;\n"
"padding: 5px 2px;\n"
"font-size:18px;\n"
"}\n"
"\n"
"")
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab)
        self.tabWidget_2.setStyleSheet("pane {\n"
"  border: 1px solid rgb(43, 93, 147);\n"
"  top:-1px; \n"
"  background: white;\n"
"} \n"
"\n"
"tab {\n"
"  background: black; \n"
"  decoration:none;\n"
"  border: 5px dashed black; \n"
"  padding: 15px;\n"
"  color:rgb(43, 93, 147);\n"
"} \n"
"\n"
"tab:selected { \n"
"  background: rgb(170, 170, 255); \n"
"  margin-bottom: -1px; \n"
"}\n"
"")
        self.tabWidget_2.setTabPosition(QtWidgets.QTabWidget.East)
        self.tabWidget_2.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget_2.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget_2.setMovable(True)
        self.tabWidget_2.setTabBarAutoHide(True)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_8)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.tab_8)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.label_3)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.comboBox = QtWidgets.QComboBox(self.tab_8)
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_10.addWidget(self.comboBox)
        self.comboBox_3 = QtWidgets.QComboBox(self.tab_8)
        self.comboBox_3.setCurrentText("")
        self.comboBox_3.setObjectName("comboBox_3")
        self.horizontalLayout_10.addWidget(self.comboBox_3)
        self.lineEdit = QtWidgets.QLineEdit(self.tab_8)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_10.addWidget(self.lineEdit)
        self.verticalLayout_5.addLayout(self.horizontalLayout_10)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_8)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_5.addWidget(self.pushButton_2)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.textEdit_2 = QtWidgets.QTextEdit(self.tab_8)
        self.textEdit_2.setMaximumSize(QtCore.QSize(500, 16777215))
        self.textEdit_2.setObjectName("textEdit_2")
        self.horizontalLayout_11.addWidget(self.textEdit_2)
        self.comboBox_7 = QtWidgets.QComboBox(self.tab_8)
        self.comboBox_7.setCurrentText("")
        self.comboBox_7.setObjectName("comboBox_7")
        self.horizontalLayout_11.addWidget(self.comboBox_7)
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_8)
        self.pushButton_4.setMaximumSize(QtCore.QSize(400, 16777215))
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_11.addWidget(self.pushButton_4)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_8)
        self.pushButton_3.setMaximumSize(QtCore.QSize(400, 16777215))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_11.addWidget(self.pushButton_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_11)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.tabWidget_2.addTab(self.tab_8, "")
        self.horizontalLayout.addWidget(self.tabWidget_2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tabWidget_3 = QtWidgets.QTabWidget(self.tab_2)
        self.tabWidget_3.setTabPosition(QtWidgets.QTabWidget.East)
        self.tabWidget_3.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget_3.setObjectName("tabWidget_3")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.tab_6)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_7 = QtWidgets.QLabel(self.tab_6)
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label_7.setLineWidth(1)
        self.label_7.setMidLineWidth(1)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_9.addWidget(self.label_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_18.addWidget(self.lineEdit_2)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.verticalLayout_18.addWidget(self.lineEdit_6)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.verticalLayout_18.addWidget(self.lineEdit_7)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.verticalLayout_18.addWidget(self.lineEdit_8)
        self.lineEdit_9 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.verticalLayout_18.addWidget(self.lineEdit_9)
        self.lineEdit_10 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.verticalLayout_18.addWidget(self.lineEdit_10)
        self.lineEdit_11 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.verticalLayout_18.addWidget(self.lineEdit_11)
        self.lineEdit_12 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.verticalLayout_18.addWidget(self.lineEdit_12)
        self.lineEdit_13 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.verticalLayout_18.addWidget(self.lineEdit_13)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.verticalLayout_18.addWidget(self.lineEdit_5)
        self.horizontalLayout_6.addLayout(self.verticalLayout_18)
        self.verticalLayout_19 = QtWidgets.QVBoxLayout()
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.verticalLayout_19.addWidget(self.lineEdit_4)
        self.lineEdit_15 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.verticalLayout_19.addWidget(self.lineEdit_15)
        self.lineEdit_16 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.verticalLayout_19.addWidget(self.lineEdit_16)
        self.lineEdit_17 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.verticalLayout_19.addWidget(self.lineEdit_17)
        self.lineEdit_19 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.verticalLayout_19.addWidget(self.lineEdit_19)
        self.lineEdit_20 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.verticalLayout_19.addWidget(self.lineEdit_20)
        self.lineEdit_22 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.verticalLayout_19.addWidget(self.lineEdit_22)
        self.lineEdit_21 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_21.setObjectName("lineEdit_21")
        self.verticalLayout_19.addWidget(self.lineEdit_21)
        self.lineEdit_23 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_23.setObjectName("lineEdit_23")
        self.verticalLayout_19.addWidget(self.lineEdit_23)
        self.lineEdit_18 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.verticalLayout_19.addWidget(self.lineEdit_18)
        self.horizontalLayout_6.addLayout(self.verticalLayout_19)
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_17.addWidget(self.lineEdit_3)
        self.lineEdit_24 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_24.setObjectName("lineEdit_24")
        self.verticalLayout_17.addWidget(self.lineEdit_24)
        self.lineEdit_14 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.verticalLayout_17.addWidget(self.lineEdit_14)
        self.lineEdit_26 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_26.setObjectName("lineEdit_26")
        self.verticalLayout_17.addWidget(self.lineEdit_26)
        self.lineEdit_28 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_28.setText("")
        self.lineEdit_28.setObjectName("lineEdit_28")
        self.verticalLayout_17.addWidget(self.lineEdit_28)
        self.lineEdit_29 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_29.setText("")
        self.lineEdit_29.setObjectName("lineEdit_29")
        self.verticalLayout_17.addWidget(self.lineEdit_29)
        self.lineEdit_27 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_27.setText("")
        self.lineEdit_27.setObjectName("lineEdit_27")
        self.verticalLayout_17.addWidget(self.lineEdit_27)
        self.lineEdit_31 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_31.setText("")
        self.lineEdit_31.setObjectName("lineEdit_31")
        self.verticalLayout_17.addWidget(self.lineEdit_31)
        self.lineEdit_30 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_30.setObjectName("lineEdit_30")
        self.verticalLayout_17.addWidget(self.lineEdit_30)
        self.horizontalLayout_6.addLayout(self.verticalLayout_17)
        self.verticalLayout_9.addLayout(self.horizontalLayout_6)
        self.pushButton = QtWidgets.QPushButton(self.tab_6)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_9.addWidget(self.pushButton)
        self.verticalLayout_10.addLayout(self.verticalLayout_9)
        self.lineEdit_25 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_25.setObjectName("lineEdit_25")
        self.verticalLayout_10.addWidget(self.lineEdit_25)
        self.tabWidget_3.addTab(self.tab_6, "")
        self.horizontalLayout_3.addWidget(self.tabWidget_3)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.prepare_data()
        self.pushButton_2.clicked.connect(lambda : self.entrainer(int(str(self.comboBox_3.currentText())), self.comboBox.currentText(), int(str(self.lineEdit.text()))))
        self.pushButton_3.clicked.connect(lambda: self.performance(self.comboBox_7.currentText(), self.labels))
        self.pushButton_4.clicked.connect(lambda: self.visualize_tree())


        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(0)
        self.comboBox_7.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def performance(self, model,labels):
        fig = plt.figure(figsize=(8, 10))
        if self.ent:
                if model=='DT':
                        cm = confusion_matrix(list(self.y_test), self.y_pred_dt, labels)
                else:
                        cm = confusion_matrix(list(self.y_test), self.y_pred_rf, labels)
                print(cm)
                plt.xlabel("Predicted Values")
                plt.ylabel("Actual Values")
                plt.imshow(cm)
                plt.text(0.25,0.25,cm[1][0],transform=fig.transFigure, bbox=dict(facecolor='white'))
                plt.text(0.25,0.75,cm[0][0],transform=fig.transFigure, bbox=dict(facecolor='white'))
                plt.text(0.75,0.25,cm[1][1],transform=fig.transFigure, bbox=dict(facecolor='white'))
                plt.text(0.75,0.75,cm[0][1],transform=fig.transFigure, bbox=dict(facecolor='white'))
                plt.show()

        
    def visualize_tree(self):
        drawtree(self.dt.tree, self.DF)

    def prepare_data(self):
        dft = self.DF.select_dtypes('object')
        for col in dft:
            dft[col]=dft[col].astype('category')
            dft[col]=dft[col].cat.codes
        self.DF[dft.columns] = dft
        X = self.DF.drop(['Attrition'], axis=1)
        y = self.DF['Attrition']

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, random_state=0, train_size = .8)
        self.lineEdit.setText("5")
        self.load_combos()


    def load_combos(self):
        costs =['gini','entropy']
        self.comboBox.addItems(costs)
        caracs = [str(i+1) for i in range(len(self.X_train.columns))]
        self.comboBox_3.addItems(caracs)
        models = ["DT","RF"]
        self.comboBox_7.addItems(models)

    def predire(self):
        if(self.ent):
                if(self.lineEdit_2.text()==''):
                        if(self.comboBox_7.currentText=='DT'):
                                res = self.dt.predict(self.X_test)
                        else:
                                res = self.rf.predict(self.X_test)
                else:
                        XX = pd.DataFrame([self.lineEdit_2, self.lineEdit_6, self.lineEdit_7, self.lineEdit_8, self.lineEdit_9, self.lineEdit_10, self.lineEdit_11, self.lineEdit_12, self.lineEdit_13, self.lineEdit_5, self.lineEdit_4, self.lineEdit_15, self.lineEdit_16, self.lineEdit_17, self.lineEdit_19, self.lineEdit_20, self.lineEdit_22, self.lineEdit_21, self.lineEdit_23, self.lineEdit_18, self.lineEdit_3, self.lineEdit_24, self.lineEdit_14, self.lineEdit_26, self.lineEdit_28, self.lineEdit_29, self.lineEdit_27, self.lineEdit_31, self.lineEdit_30], columns=self.X_test.columns)
                        if(self.comboBox_7.currentText=='DT'):
                                res = self.dt.predict(XX)
                        else:
                                res = self.rf.predict(XX)
                self.lineEdit_25.setText(str(res))

    def entrainer(self, caracts, cr='gini' ,profondeur = 5):
        c = int(caracts)
        p = int(profondeur)
        start_time = time.time()
        self.dt = DecisionTree(max_depth=p,max_features=c,random_state=42,criterion=cr)
        self.dt.fit(self.X_train, self.y_train)
        self.dt_time = time.time() - start_time
        start_time = time.time()
        self.rf = RandomForest()
        self.rf.fit(self.X_train, self.y_train)
        self.rf_time = time.time() - start_time
        self.y_pred_dt = self.dt.predict(self.X_test)
        self.y_pred_rf = self.rf.predict(self.X_test)
        self.textEdit_2.setText(self.get_metrics('DT', self.labels)+ f"Execution time : {self.tt}\n" )
        self.ent=True

    def switch_model(self,model):
        if(self.ent):
                self.textEdit_2.setText(self.get_metrics(model, self.labels)+ f"Execution time : {self.tt}\n")

    def get_metrics(self, model,labels):
        if model=="DT":
                self.tt = self.dt_time
                return calculate_metrics(list(self.y_test),self.y_pred_dt,labels)
        else:
                self.tt = self.rf_time
                return calculate_metrics(list(self.y_test),self.y_pred_rf,labels)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Data Mining Project Part 1"))
        self.label_3.setText(_translate("Form", "Entrainement des modèles"))
        self.lineEdit.setText(_translate("Form", ""))
        self.lineEdit.setPlaceholderText("Profondeur de l\'arbre")
        self.pushButton_2.setText(_translate("Form", "Entrainer"))
        self.textEdit_2.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Métriques du modèle</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton_4.setText(_translate("Form", "Visualisez arbre"))
        self.pushButton_3.setText(_translate("Form", "Visualisez performance"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_8), _translate("Form", "Description attributs"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Manipulation de dataset"))
        self.label_7.setText(_translate("Form", "Prédiction d\'une nouvelle instance"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Age"))
        self.lineEdit_6.setPlaceholderText(_translate("Form", "BusinessTravel"))
        self.lineEdit_7.setPlaceholderText(_translate("Form", "DailyRate"))
        self.lineEdit_8.setPlaceholderText(_translate("Form", "Department"))
        self.lineEdit_9.setPlaceholderText(_translate("Form", "DistanceFromHome"))
        self.lineEdit_10.setPlaceholderText(_translate("Form", "Education"))
        self.lineEdit_11.setPlaceholderText(_translate("Form", "EducationField"))
        self.lineEdit_12.setPlaceholderText(_translate("Form", "EnvironmentSatisfaction"))
        self.lineEdit_13.setPlaceholderText(_translate("Form", "Gender"))
        self.lineEdit_5.setPlaceholderText(_translate("Form", "HourlyRate"))
        self.lineEdit_4.setPlaceholderText(_translate("Form", "JobInvolvement"))
        self.lineEdit_15.setPlaceholderText(_translate("Form", "JobLevel"))
        self.lineEdit_16.setPlaceholderText(_translate("Form", "JobRole"))
        self.lineEdit_17.setPlaceholderText(_translate("Form", "JobSatisfaction"))
        self.lineEdit_19.setPlaceholderText(_translate("Form", "MaritalStatus"))
        self.lineEdit_20.setPlaceholderText(_translate("Form", "MonthlyIncome"))
        self.lineEdit_22.setPlaceholderText(_translate("Form", "MonthlyRate"))
        self.lineEdit_21.setPlaceholderText(_translate("Form", "NumCompaniesWorked"))
        self.lineEdit_23.setPlaceholderText(_translate("Form", "OverTime"))
        self.lineEdit_18.setPlaceholderText(_translate("Form", "PercentSalaryHike"))
        self.lineEdit_3.setPlaceholderText(_translate("Form", "RelationshipSatisfaction"))
        self.lineEdit_24.setPlaceholderText(_translate("Form", "StockOptionLevel"))
        self.lineEdit_14.setPlaceholderText(_translate("Form", "TotalWorkingYears"))
        self.lineEdit_26.setPlaceholderText(_translate("Form", "TrainingTimesLastYear"))
        self.lineEdit_28.setPlaceholderText(_translate("Form", "WorkLifeBalance"))
        self.lineEdit_29.setPlaceholderText(_translate("Form", "YearsAtCompany"))
        self.lineEdit_27.setPlaceholderText(_translate("Form", "YearsInCurrentRole"))
        self.lineEdit_31.setPlaceholderText(_translate("Form", "YearsSinceLastPromotion"))
        self.lineEdit_30.setPlaceholderText(_translate("Form", "YearsWithCurrManager"))
        self.pushButton.setText(_translate("Form", "Prédire"))
        self.lineEdit_25.setPlaceholderText(_translate("Form", "Attrition prédiction"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_6), _translate("Form", "Saisie des données"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Analyse des caractéristiques"))
        self.comboBox_7.activated.connect(lambda: self.switch_model(self.comboBox_7.currentText()))
        self.pushButton.clicked.connect(lambda: self.predire())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
