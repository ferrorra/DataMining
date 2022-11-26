

from PyQt5 import QtCore, QtGui, QtWidgets
import apriori
import pandas as pd
import util
from PyQt5.QtWidgets import QListWidgetItem

support , confidence=0.2,0.2
rules = []


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(1223, 843)
        Form.setStyleSheet("")
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(Form)
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
        self.tabr = QtWidgets.QWidget()
        self.tabr.setObjectName("tabr")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(100, 50))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(300, 50))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_3.addWidget(self.lineEdit_2)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setMinimumSize(QtCore.QSize(100, 0))
        self.label_3.setMaximumSize(QtCore.QSize(300, 16777215))
        self.label_3.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setMinimumSize(QtCore.QSize(100, 50))
        self.lineEdit.setMaximumSize(QtCore.QSize(300, 50))
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setMinimumSize(QtCore.QSize(100, 0))
        self.label_2.setMaximumSize(QtCore.QSize(300, 16777215))
        self.label_2.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tableView = QtWidgets.QTableView(self.tab)
        self.tableView.setObjectName("tableView")
        self.tableView.setMaximumWidth(800)
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2r = QtWidgets.QHBoxLayout(self.tabr)
        self.horizontalLayout_2r.setObjectName("horizontalLayout_2r")
        self.verticalLayoutr = QtWidgets.QVBoxLayout()
        self.verticalLayoutr.setObjectName("verticalLayoutr")
        self.labelr = QtWidgets.QLabel(self.tabr)
        self.labelr.setObjectName("labelr")
        self.verticalLayoutr.addWidget(self.labelr)
        self.horizontalLayout_3r = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3r.setObjectName("horizontalLayout_3r")
        self.verticalLayout_2r = QtWidgets.QVBoxLayout()
        self.verticalLayout_2r.setObjectName("verticalLayout_2r")
        self.comboBox = QtWidgets.QComboBox(self.tabr)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox.setMaximumSize(QtCore.QSize(300, 40))
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_2r.addWidget(self.comboBox)
        self.label_2r = QtWidgets.QLabel(self.tabr)
        self.label_2r.setMinimumSize(QtCore.QSize(100, 0))
        self.label_2r.setMaximumSize(QtCore.QSize(300, 16777215))
        self.label_2r.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";")
        self.label_2r.setObjectName("label_2r")
        self.verticalLayout_2r.addWidget(self.label_2r)
        self.listView = QtWidgets.QListView(self.tabr)
        self.listView.setObjectName("listView")
        self.comboBox.activated.connect( lambda: self.recommend(self.comboBox.currentText(), self.listView))
        self.verticalLayout_2r.addWidget(self.listView)
        self.horizontalLayout_3r.addLayout(self.verticalLayout_2r)
        self.verticalLayoutr.addLayout(self.horizontalLayout_3r)
        self.horizontalLayout_2r.addLayout(self.verticalLayoutr)
        self.tabWidget.addTab(self.tab, "")
        self.tabWidget.addTab(self.tabr, "Recommendation")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton("Apriori",self.tab)
        self.pushButton.setStyleSheet("color:rgb(252, 55, 49);\n"
"font: 87 15pt \"Aileron Heavy\";\n"
"padding:10px;\n"
"border: 2px solid rgb(252, 55, 49);\n"
"border-radius:20px;")
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(lambda : self.tp(self.tableView, pd.to_numeric(self.lineEdit_2.text()), pd.to_numeric(self.lineEdit.text())))
        self.tableView.setMinimumHeight(500)
        self.tableView.setMinimumWidth(800)
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Data Mining Project part 3"))
        self.label.setText(_translate("Form", "Partie 3 du TP DataMining"))
        self.label_3.setText(_translate("Form", "min_support"))
        self.label_2.setText(_translate("Form", "min_confidence"))
        self.labelr.setText(_translate("Form", "Recommendation"))
        self.label_2r.setText(_translate("Form", "Choisir Une catégorie"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Manipulation de dataset"))

    def load_categories(self, combo):
        combo.clear()
        df = pd.read_excel("Dataset2_ TrendingVideosYoutube_.xlsx")
        categories = df['videoCategoryLabel'].unique()
        combo.addItems(categories)

    def recommend(self, categorie, list):
        global support, confidence, rules
        categorie = "{'"+categorie+"'}"
        recommendations = apriori.get_recommendation(rules, categorie)
        dff=pd.DataFrame(recommendations, columns = ["Recommendations"])
        model = util.pandasModel(dff)
        list.setModel(model)
        list.resize(500, 200)
        list.show()


    def tp(self, view, sup, conf):
        global rules
        df = pd.read_excel("Dataset2_ TrendingVideosYoutube_.xlsx")
        data = apriori.create_data_table(df)        
        rules = apriori.algorithme_apriori(data, sup, conf)

        pd.set_option('display.max_colwidth', None)
        model = util.pandasModel(pd.DataFrame(rules, columns = ["Rule","Confidence","Lift"]))
        view.setModel(model)
        view.resize(500, 200)
        view.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    ui.load_categories(ui.comboBox)
    ui.tp(ui.tableView, support, confidence)
    ui.recommend(ui.comboBox.currentText() , ui.listView)
    Form.show()
    sys.exit(app.exec_())




