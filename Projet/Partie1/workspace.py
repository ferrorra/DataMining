from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QTreeWidgetItem
import sys, res
import pandas as pd
import numpy as np
from PyQt5.QtCore import Qt, QItemSelectionModel, QSortFilterProxyModel
from pandas.api.types import is_numeric_dtype
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel, QModelIndex
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QAbstractItemView
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import seaborn as sns
from openpyxl import load_workbook


class Ui_Form(object):
    app = QApplication([])
    DF =pd.read_excel("Dataset1_ HR-EmployeeAttrition.xlsx")
    moustaches,scat,histo = QWidget(),QWidget(),QWidget()

    '''def search(self,textEdit, table):
        data = pd.read_excel("Dataset1_ HR-EmployeeAttrition.xlsx")
        #sech = combo.currentIndex() 
        model = pandasModel(data)
        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setFilterKeyColumn(-1)
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        table.setModel(filter_proxy_model)'''

    def plottingMoustaches(self,tab,verticalLayout,plot="",combo1="",combo2=""):
        verticalLayout.removeWidget(self.moustaches)
        # creating a window object
        self.moustaches = Window(tab)
        self.moustaches.setMinimumSize(QtCore.QSize(800, 500))
        self.moustaches.setMaximumSize(QtCore.QSize(800, 500))
        self.moustaches.setObjectName("Plot")

        self.moustaches.button.clicked.connect(lambda: self.moustaches.Moustaches(combo1))

        verticalLayout.addWidget(self.moustaches)
        # showing the window
        self.moustaches.show()

    def plottingHist(self,tab,verticalLayout,plot="",combo1="",combo2=""):
        verticalLayout.removeWidget(self.histo)
        # creating a window object
        self.histo = Window(tab)
        self.histo.setMinimumSize(QtCore.QSize(800, 500))
        self.histo.setMaximumSize(QtCore.QSize(800, 500))
        self.histo.setObjectName("Plot")

        self.histo.button.clicked.connect(lambda: self.histo.hist(combo1))

        
        verticalLayout.addWidget(self.histo)
        # showing the window
        self.histo.show()

    def plottingScatter(self,tab,verticalLayout,plot="",combo1="",combo2=""):
        verticalLayout.removeWidget(self.scat)
        # creating a window object
        self.scat = Window(tab)
        self.scat.setMinimumSize(QtCore.QSize(800, 500))
        self.scat.setMaximumSize(QtCore.QSize(800, 500))
        self.scat.setObjectName("Plot")

        self.scat.button.clicked.connect(lambda: self.scat.dispersion(combo1,combo2))
        verticalLayout.addWidget(self.scat)
        # showing the window
        self.scat.show()
        
    def tendances(self, view):
        df = self.DF
        tendance_centrale = {}
        for d in df:
            tc = {}
            if is_numeric_dtype(df[d]):
                tc["Moyenne"] = self.moyenne(df, d)
                tc["Mediane"] = self.median(df, d)
                tc["Mode"] = self.mode(df, d)
                tc["symetrie"] = self.coeff_asy(tc)
                tendance_centrale[d] = tc
        self.fill_widget(view, tendance_centrale)
        view.show()

    def lookup(self, combo, text, table):
        column=0
        column = combo.currentIndex()
        model = table.model()
        start = model.index(0, column)
        matches = model.match(
            start, QtCore.Qt.DisplayRole,
            text, 1, QtCore.Qt.MatchContains)
        if matches:
            index = matches[0]
            table.selectionModel().select(
                index, QItemSelectionModel.Select)
            table.scrollTo(index)

    def scroll_tree(self,treeWidget,text):
        newItem = []
        newItem = treeWidget.findItems(text.currentText(),Qt.MatchRegularExpression, 0)
        treeWidget.scrollToItem(newItem[0])        
        print(newItem[0])
        treeWidget.setCurrentItem(newItem[0])    

    def find(self, text, table, column=0 ):
        model = table.model()
        start = model.index(0, column)
        matches = model.match(
            start, QtCore.Qt.DisplayRole,
            text, 1, QtCore.Qt.MatchContains)
        if matches:
            index = matches[0]
            table.selectionModel().select(
                index, QItemSelectionModel.Select)
            table.scrollTo(index)

    def ecart_moyen(self,df, d):
        em = []
        m = self.moyenne(df, d)
        for d in df[d]:
            em.append(float("{:.2f}".format(np.abs(d-m))))
        return em
    
    def variance(self,df, d):
        em_sum = []
        m = self.moyenne(df, d)
        n = len(df[d])
        for d in df[d]:
            em_sum.append(np.power((d - m), 2))
        return float("{:.2f}".format(sum(em_sum) / n))
    
    def ecart_type(self,var):
        return float("{:.2f}".format(np.sqrt(var)))
    
    def quartilles(self,df, d):
        colonne_sorted = list(df[d].sort_values())
        n = len(df[d])
        return [min(colonne_sorted), colonne_sorted[n // 4], colonne_sorted[(n * 3) // 4], max(colonne_sorted)]
    
    def iqr(self,quart):
        return quart[2] - quart[1] 

    def highlight(self, combo, table):
       high = combo.currentText() 
       self.find(high, table)

    def attributs(self,view):
        colonnes_description = []
        df = self.DF
        for d in df:
                colonnes_description.append([d, df[d].count(), str(df.dtypes[d])])
        dff=pd.DataFrame(colonnes_description, columns = ["Nom","Valeurs non null","Type"])
        model = pandasModel(dff)
        view.setModel(model)
        view.resize(500, 200)
        view.show()

    def load_combo(self, combo):
        df = self.DF
        items = df.columns
        combo.clear()
        combo.addItems(items)

    def infos(self,widget):
        dataset_description = {}
        df = self.DF
        dataset_description["Nombre de lignes"] = df.shape[0]
        dataset_description["Nombre de colonnes"] = df.shape[1]
        dataset_description["Usage en memoire"] = str(df.memory_usage(index=False).sum() / 1024) + " ko"
        dataset_description["Type de donnees"] = list(map(str, df.dtypes.unique().tolist()))
        self.fill_widget(widget, dataset_description)
        widget.show()

    def fill_item(self,item, value):
        item.setExpanded(True)
        if type(value) is dict:
                for key, val in sorted(value.items()):
                        child = QTreeWidgetItem()
                        child.setText(0, str(key))
                        item.addChild(child)
                        self.fill_item(child, val)
        elif type(value) is list:
                for val in value:
                        child = QTreeWidgetItem()
                        item.addChild(child)
                        if type(val) is dict:      
                                child.setText(0, '[dict]')
                                self.fill_item(child, val)
                        elif type(val) is list:
                                child.setText(0, '[list]')
                                self.fill_item(child, val)
                        else:
                                child.setText(0, str(val))              
                        child.setExpanded(True)
        else:   
                child = QTreeWidgetItem()
                child.setText(0, str(value))
                item.addChild(child)

    def fill_widget(self,widget, value):
        widget.clear()
        self.fill_item(widget.invisibleRootItem(), value)

    def visualiser_dataset(self,view):
        df = self.DF
        model = pandasModel(df)
        view.setModel(None)
        view.setModel(model)
        view.resize(1000, 700)
        view.show()

    def mesures(self, view):
        mesures_de_dispersion = {}
        df = self.DF
        for d in df:
            mdd = {}
            if is_numeric_dtype(df[d]):
                em = self.ecart_moyen(df, d)
                mdd["Ecart moyen"] = [min(em), max(em)]
                mdd["Variance"] = self.median(df, d)
                mdd["Ecart type"] = self.ecart_type(mdd["Variance"])
                quart = self.quartilles(df, d)
                quart_name = ["Minimum", "Q1", "Q3", "Maximum"]
                for q, qm in zip(quart, quart_name):
                    mdd[qm] = q
                mdd["IQR"] = self.iqr(quart)
                Outliers = [x for x in df[d] if (x > (mdd["Q3"] + 1.5 * mdd["IQR"])) or (x < (mdd["Q1"] - 1.5 * mdd["IQR"]))]
                mdd["Donnees aberanttes"] = "Aucune" if len(Outliers) == 0 else set(Outliers)
                mesures_de_dispersion[d] = mdd
        data= pd.DataFrame.from_dict(mesures_de_dispersion, orient='index')
        data = data.reset_index(level=0)
        model = pandasModel(data)
        view.setModel(model)
        view.resize(600, 500)
        view.show()


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(1000, 800)
        Form.setStyleSheet("")
        Form.setWindowIcon(QtGui.QIcon('resources/puzzle.png'))
        QtWidgets.QApplication.setStyle(ProxyStyle())
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
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab)
        self.tabWidget_2.setTabBar(TabBar1(self.tabWidget_2))
        self.tabWidget_2.setStyleSheet("QTabWidget::pane {\n"
"  border: 1px solid rgb(43, 93, 147);\n"
"  top:-1px; \n"
"  background: white;\n"
"} \n"
"\n"
"QTabBar::tab {\n"
"  background:  rgb(255, 217, 86); \n"
"  decoration:none;\n"
"  border: 5px dashed rgb(252, 55, 49); \n"
"  padding: 15px;\n"
"  color:#2b5d93;\n"
"} \n"
"\n"
"QTabBar::tab:selected { \n"
"  background: rgb(255, 217, 86); \n"
"  margin-bottom: -1px; \n"
"}\n"
)

        self.tabWidget_2.setTabPosition(QtWidgets.QTabWidget.East)
        self.tabWidget_2.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_2.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget_2.setMovable(True)
        self.tabWidget_2.setTabBarAutoHide(True)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.tab_5)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.tab_5)
        self.tableView.setObjectName("tableView")
        self.tableView.resizeColumnToContents(0)
        self.verticalLayout.addWidget(self.tableView)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget_2.addTab(self.tab_5, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_7)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.tab_7)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.tableView_2 = QtWidgets.QTreeWidget(self.tab_7)
        self.tableView_2.setObjectName("tableView_2")
        self.verticalLayout_3.addWidget(self.tableView_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.tabWidget_2.addTab(self.tab_7, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_8)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.tab_8)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_5.addWidget(self.label_3)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setObjectName("formLayout")
        self.tableView_3 = QtWidgets.QTableView(self.tab_8)
        self.tableView_3.setMinimumSize(QtCore.QSize(500, 200))
        self.tableView_3.setObjectName("tableView_3")
        self.tableView_3.setMidLineWidth(100)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.tableView_3)
        self.comboBox = QtWidgets.QComboBox(self.tab_8)
        self.comboBox.setMaximumSize(QtCore.QSize(300, 16777215))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.activated.connect(lambda : self.highlight(self.comboBox, self.tableView_3))
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.label_5 = QtWidgets.QLabel(self.tab_8)
        self.label_5.setMaximumSize(QtCore.QSize(350, 200))
        self.label_5.setStyleSheet("border-image: url(:/images/resources/growth-chart (1).png);")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_5)
        self.label_21 = QtWidgets.QLabel(self.tab_8)
        self.label_21.setMinimumSize(QtCore.QSize(150, 0))
        self.label_21.setStyleSheet("border-image: url(:/images/resources/growth-graph.png);")
        self.label_21.setText("")
        self.label_21.setObjectName("label_21")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_21)
        self.label_22 = QtWidgets.QLabel(self.tab_8)
        self.label_22.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_22.setStyleSheet("border-image: url(:/images/resources/money-growth.png);")
        self.label_22.setText("")
        self.label_22.setObjectName("label_22")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_22)
        self.verticalLayout_5.addLayout(self.formLayout)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.tabWidget_2.addTab(self.tab_8, "")
        self.tab_9 = QtWidgets.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_9)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.tab_9)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_7.addWidget(self.label_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.tab_9)
        self.label_6.setMaximumSize(QtCore.QSize(300, 50))
        self.label_6.setStyleSheet("color:rgb(252, 55, 49);\n"
"font: 87 15pt \"Aileron Heavy\";\n"
"padding:10px;")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.textEdit = QtWidgets.QTextEdit(self.tab_9)
        self.textEdit.setMaximumSize(QtCore.QSize(500, 50))
        self.textEdit.setStyleSheet("color:rgb(43, 93, 147);\n"
"font: 20pt \"Roboto\";\n"
"")
        self.textEdit.setObjectName("textEdit")

        self.horizontalLayout_5.addWidget(self.textEdit)
        self.comboBox_2 = QtWidgets.QComboBox(self.tab_9)
        self.comboBox_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.comboBox_2.setObjectName("comboBox_2")
        self.horizontalLayout_5.addWidget(self.comboBox_2)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.tableView_4 = QtWidgets.QTableView(self.tab_9)
        self.tableView_4.setMinimumSize(QtCore.QSize(0, 500))
        self.tableView_4.setStyleSheet("")
        self.tableView_4.setObjectName("tableView_4")
        self.verticalLayout_7.addWidget(self.tableView_4)
        self.verticalLayout_8.addLayout(self.verticalLayout_7)
        self.tabWidget_2.addTab(self.tab_9, "")
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
        self.tabWidget_3.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_3.setObjectName("tabWidget_3")
        #self.tabWidget_3.setTabBar(TabBar2(self.tabWidget_3))
        self.tabWidget_3.setStyleSheet("QTabWidget::pane {\n"
"  border: 1px solid rgb(43, 93, 147);\n"
"  top:-1px; \n"
"  background: white;\n"
"} \n"
"\n"
"QTabBar::tab {\n"
"  background:  rgb(255, 217, 86); \n"
"  decoration:none;\n"
"  border: 5px dashed rgb(252, 55, 49); \n"
"  padding: 15px;\n"
"  color:#2b5d93;\n"
"} \n"
"\n"
"QTabBar::tab:selected { \n"
"  background: rgb(255, 217, 86); \n"
"  margin-bottom: -1px; \n"
"}\n"
)
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.tab_6)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_7 = QtWidgets.QLabel(self.tab_6)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_9.addWidget(self.label_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_8 = QtWidgets.QLabel(self.tab_6)
        self.label_8.setMaximumSize(QtCore.QSize(300, 50))
        self.label_8.setStyleSheet("color:rgb(252, 55, 49);\n"
"font: 87 15pt \"Aileron Heavy\";\n"
"padding:10px;")
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_6.addWidget(self.label_8)
        self.comboBox_3 = QtWidgets.QComboBox(self.tab_6)
        self.comboBox_3.setMaximumSize(QtCore.QSize(300, 30))
        self.comboBox_3.setObjectName("comboBox_3")
        self.horizontalLayout_6.addWidget(self.comboBox_3)
        self.comboBox_3.activated.connect(lambda: self.scroll_tree(self.tableView_5,self.comboBox_3))
        self.label_9 = QtWidgets.QLabel(self.tab_6)
        self.label_9.setMaximumSize(QtCore.QSize(90, 50))
        self.label_9.setStyleSheet("border-image: url(:/images/resources/circle-chart.png);")
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        self.verticalLayout_9.addLayout(self.horizontalLayout_6)
        self.verticalLayout_10.addLayout(self.verticalLayout_9)
        self.tableView_5 = QtWidgets.QTreeWidget(self.tab_6)
        self.tableView_5.setMinimumSize(QtCore.QSize(0, 500))
        self.tableView_5.setObjectName("tableView_5")
        self.verticalLayout_10.addWidget(self.tableView_5)
        self.tabWidget_3.addTab(self.tab_6, "")
        self.tab_11 = QtWidgets.QWidget()
        self.tab_11.setObjectName("tab_11")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.tab_11)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_10 = QtWidgets.QLabel(self.tab_11)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_11.addWidget(self.label_10)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_11 = QtWidgets.QLabel(self.tab_11)
        self.label_11.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_11.setStyleSheet("color:rgb(252, 55, 49);\n"
"font: 87 15pt \"Aileron Heavy\";\n"
"padding:10px;")
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_7.addWidget(self.label_11)
        self.comboBox_4 = QtWidgets.QComboBox(self.tab_11)
        self.comboBox_4.setMaximumSize(QtCore.QSize(300, 30))
        self.comboBox_4.setObjectName("comboBox_4")
        self.horizontalLayout_7.addWidget(self.comboBox_4)
        self.label_12 = QtWidgets.QLabel(self.tab_11)
        self.label_12.setMaximumSize(QtCore.QSize(150, 50))
        self.label_12.setStyleSheet("border-image: url(:/images/resources/network-chart.png);")
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_7.addWidget(self.label_12)
        self.verticalLayout_11.addLayout(self.horizontalLayout_7)
        self.verticalLayout_12.addLayout(self.verticalLayout_11)
        self.tableView_6 = QtWidgets.QTableView(self.tab_11)
        self.tableView_6.setObjectName("tableView_6")
        self.comboBox_4.activated.connect(lambda : self.highlight(self.comboBox_4, self.tableView_6))
        self.verticalLayout_12.addWidget(self.tableView_6)
        self.tabWidget_3.addTab(self.tab_11, "")
        self.tab_12 = QtWidgets.QWidget()
        self.tab_12.setObjectName("tab_12")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.tab_12)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_13 = QtWidgets.QLabel(self.tab_12)
        self.label_13.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label_13.setObjectName("label_13")
        self.verticalLayout_13.addWidget(self.label_13)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_14 = QtWidgets.QLabel(self.tab_12)
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_14.setStyleSheet("color:rgb(252, 55, 49);\n"
"font: 87 15pt \"Aileron Heavy\";\n"
"padding:10px;")
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_8.addWidget(self.label_14)
        self.comboBox_5 = QtWidgets.QComboBox(self.tab_12)
        self.comboBox_5.setMinimumSize(QtCore.QSize(200, 30))
        self.comboBox_5.setMaximumSize(QtCore.QSize(500, 30))
        self.comboBox_5.setObjectName("comboBox_5")
        self.horizontalLayout_8.addWidget(self.comboBox_5)
        self.verticalLayout_13.addLayout(self.horizontalLayout_8)
        self.verticalLayout_14.addLayout(self.verticalLayout_13)
        self.tabWidget_3.addTab(self.tab_12, "")
        self.tab_10 = QtWidgets.QWidget()
        self.tab_10.setObjectName("tab_10")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.tab_10)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_15 = QtWidgets.QLabel(self.tab_10)
        self.label_15.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label_15.setObjectName("label_15")
        self.verticalLayout_15.addWidget(self.label_15)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_16 = QtWidgets.QLabel(self.tab_10)
        self.label_16.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_16.setStyleSheet("color:rgb(252, 55, 49);\n"
"font: 87 15pt \"Aileron Heavy\";\n"
"padding:10px;")
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_9.addWidget(self.label_16)
        self.comboBox_6 = QtWidgets.QComboBox(self.tab_10)
        self.comboBox_6.setMinimumSize(QtCore.QSize(200, 30))
        self.comboBox_6.setMaximumSize(QtCore.QSize(500, 16777215))
        self.comboBox_6.setObjectName("comboBox_6")
        self.horizontalLayout_9.addWidget(self.comboBox_6)
        self.verticalLayout_15.addLayout(self.horizontalLayout_9)
        self.verticalLayout_16.addLayout(self.verticalLayout_15)
        self.tabWidget_3.addTab(self.tab_10, "")
        self.horizontalLayout_3.addWidget(self.tabWidget_3)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_13 = QtWidgets.QWidget()
        self.tab_13.setObjectName("tab_13")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.tab_13)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.label_17 = QtWidgets.QLabel(self.tab_13)
        self.label_17.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label_17.setObjectName("label_17")
        self.verticalLayout_17.addWidget(self.label_17)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_18 = QtWidgets.QLabel(self.tab_13)
        self.label_18.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_18.setStyleSheet("color:rgb(252, 55, 49);\n"
"font: 87 15pt \"Aileron Heavy\";\n"
"padding:10px;")
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_10.addWidget(self.label_18)
        self.verticalLayout_19 = QtWidgets.QVBoxLayout()
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.label_19 = QtWidgets.QLabel(self.tab_13)
        self.label_19.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_19.setStyleSheet("color:rgb(252, 55, 49);\n"
"font: 87 15pt \"Aileron Heavy\";\n"
"padding:10px;")
        self.label_19.setObjectName("label_19")
        self.verticalLayout_19.addWidget(self.label_19)
        self.comboBox_7 = QtWidgets.QComboBox(self.tab_13)
        self.comboBox_7.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_7.setMaximumSize(QtCore.QSize(300, 16777215))
        self.comboBox_7.setObjectName("comboBox_7")
        self.verticalLayout_19.addWidget(self.comboBox_7)
        self.horizontalLayout_10.addLayout(self.verticalLayout_19)
        self.verticalLayout_20 = QtWidgets.QVBoxLayout()
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout()
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.label_20 = QtWidgets.QLabel(self.tab_13)
        self.label_20.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_20.setStyleSheet("color:rgb(252, 55, 49);\n"
"font: 87 15pt \"Aileron Heavy\";\n"
"padding:10px;")
        self.label_20.setObjectName("label_20")
        self.verticalLayout_21.addWidget(self.label_20)
        self.comboBox_8 = QtWidgets.QComboBox(self.tab_13)
        self.comboBox_8.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_8.setMaximumSize(QtCore.QSize(300, 16777215))
        self.comboBox_8.setObjectName("comboBox_8")
        self.verticalLayout_21.addWidget(self.comboBox_8)
        self.verticalLayout_20.addLayout(self.verticalLayout_21)
        self.horizontalLayout_10.addLayout(self.verticalLayout_20)
        self.verticalLayout_17.addLayout(self.horizontalLayout_10)
        self.verticalLayout_18.addLayout(self.verticalLayout_17)
        self.tabWidget.addTab(self.tab_13, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.textEdit.textChanged.connect(lambda: self.lookup(self.comboBox_2, self.textEdit.toPlainText(), self.tableView_4))   

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(3)
        self.tabWidget_3.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Data Mining Project Part 1"))
        self.label.setText(_translate("Form", "Visualisation du contenu de notre dataset"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("Form", "Dataset"))
        self.label_2.setText(_translate("Form", "Description globale de notre dataset"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_7), _translate("Form", "Infos"))
        self.label_3.setText(_translate("Form", "Description des attributs"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_8), _translate("Form", "Attributs"))
        self.label_4.setText(_translate("Form", "Mise à jour des attributs"))
        self.label_6.setText(_translate("Form", "Scroller"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_9), _translate("Form", "MAJ"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Manipulation de dataset"))
        self.label_7.setText(_translate("Form", "Mesures de tendances centrales et asymétrie"))
        self.label_8.setText(_translate("Form", "Chercher attribut"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_6), _translate("Form", "Tendances centrales et symétries"))
        self.label_10.setText(_translate("Form", "Mesures de dispersion et données abberantes"))
        self.label_11.setText(_translate("Form", "Chercher attribut"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_11), _translate("Form", "Dispersion et Outliers"))
        self.label_13.setText(_translate("Form", "Boite à moustaches et données abberantes"))
        self.label_14.setText(_translate("Form", "Choisir attribut"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_12), _translate("Form", "Boite à Moustaches"))
        self.label_15.setText(_translate("Form", "Histogramme et distribution de données"))
        self.label_16.setText(_translate("Form", "Choisir attribut"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_10), _translate("Form", "Histogramme"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Analyse des caractéristiques"))
        self.label_17.setText(_translate("Form", "Diagrammes de dispersion des données et corrélations entre les attributs"))
        self.label_18.setText(_translate("Form", "Choisir les attributs"))
        self.label_19.setText(_translate("Form", "Axes X"))
        self.label_20.setText(_translate("Form", "Axes Y"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_13), _translate("Form", "Visualisation"))

                
        


        self.tabWidget.currentChanged.connect(lambda: self.visualiser_dataset(self.tableView)) 
        self.tabWidget.currentChanged.connect(lambda: self.attributs(self.tableView_3))
        self.tabWidget_1.currentChanged.connect(lambda: self.attributs(self.tableView_3))

        self.tabWidget.currentChanged.connect(lambda: self.tendances(self.tableView_5)) 
        self.tabWidget.currentChanged.connect(lambda: self.mesures(self.tableView_6))

        self.comboBox_7.activated.connect(lambda: self.plottingScatter(self.tab_13,self.verticalLayout_17,"Scatter", self.comboBox_7.currentText(),self.comboBox_8.currentText()))
        self.comboBox_8.activated.connect(lambda: self.plottingScatter(self.tab_13,self.verticalLayout_17,"Scatter", self.comboBox_7.currentText(),self.comboBox_8.currentText())) 
        self.comboBox_6.activated.connect(lambda: self.plottingHist(self.tab_10,self.verticalLayout_16,"Hist", self.comboBox_6.currentText()))
        self.comboBox_5.activated.connect(lambda: self.plottingMoustaches(self.tab_12,self.verticalLayout_13,"Moustaches", self.comboBox_5.currentText()))

        


    def moyenne(self,df, d):
        return float("{:.2f}".format(df[d].sum() / df[d].count()))
    
    def median(self,df, d): 
        colonne_sorted = list(df[d].sort_values())
        n = len(df[d])
        return ((colonne_sorted[n//2] + colonne_sorted[n//2 + 1]) / 2) if n % 2 == 0 else colonne_sorted[(n+1)/2]
    
    def mode(self,df, d):
        l = []
        l.append(df[d].value_counts().index)
        l.append(list(df[d].value_counts()))
        mod = [l[0][0]]
        for i in range(1, len(l[0])):
            if l[1][i] == l[1][0]:
                mod.append(l[0][i])
            else:
                break
        return mod if len(mod) > 1 else [] if len(mod) == len(df[d]) else mod[0]
    
    def coeff_asy(self,tc):
        mode = max(tc["Mode"]) if type(tc["Mode"]) == list else tc["Mode"]
    
        if round(tc["Moyenne"]) == round(tc["Mediane"]) == round(mode):
            return "Distribution symetrique"
        elif tc["Moyenne"] < tc["Mediane"] < mode:
            return "Distribution d'asymetrie negative"
        elif tc["Moyenne"] > tc["Mediane"] > mode:
            return "Distribution d'asymetrie positive"
        else:
            return "Distribution non identifie"
    
    
        


class TabBar1(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(270)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt);
            painter.restore()



class ProxyStyle(QtWidgets.QProxyStyle):
    def drawControl(self, element, opt, painter, widget):
        if element == QtWidgets.QStyle.CE_TabBarTabLabel:
            ic = self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            r = QtCore.QRect(opt.rect)
            w =  0 if opt.icon.isNull() else opt.rect.width() + self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            r.setHeight(opt.fontMetrics.width(opt.text) + w)
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QtWidgets.QProxyStyle.drawControl(self, element, opt, painter, widget)


class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
    def flags(self, index):
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable

    def setData(self, index, value, role):
        if value=="":
                value = np.nan
        if role == Qt.EditRole:
            # Set the value into the frame.
            self._data.iloc[index.row(), index.column()] = value            
            dffff = pd.read_excel("Dataset1_ HR-EmployeeAttrition.xlsx")
            dffff.iloc[int(index.row()), int(index.column())] =value    
            dffff.update(self._data)
            dffff.to_excel('Dataset1_ HR-EmployeeAttrition.xlsx', index =False)
            return True
        return False




class Window(QWidget):
    DF =pd.read_excel("Dataset1_ HR-EmployeeAttrition.xlsx")

    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
  
        # a figure instance to plot on
        self.figure = plt.figure()
  
        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
  
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
  
        # Just some button connected to 'plot' method
        self.button = QPushButton('Plot')
          
        # creating a Vertical Box layout
        layout = QVBoxLayout()
          
        # adding tool bar to the layout
        layout.addWidget(self.toolbar)
          
        # adding canvas to the layout
        layout.addWidget(self.canvas)
          
        # adding push button to the layout
        layout.addWidget(self.button)
          
        # setting layout to the main window
        self.setLayout(layout)
  
    # action called by the push button
    def Moustaches(self, combo):

        # clearing old figure
        self.figure.clear()
        df = self.DF
        axe = self.figure.add_subplot(111)
        if is_numeric_dtype(df[combo]):
            axe.boxplot(df[combo])
            axe.set_title(combo)
        # refresh canvas
        self.canvas.draw()

    def hist(self, combo):

        # clearing old figure
        self.figure.clear()
        df = self.DF
        axe = self.figure.add_subplot(111)
        if is_numeric_dtype(df[combo]):
                sns.histplot(data = df[combo], kde=True, ax=axe).set(title=combo)
        # refresh canvas
        self.canvas.draw()


    def dispersion(self, combo1, combo2):
            # clearing old figure
            self.figure.clear()
            df = self.DF
            axe = self.figure.add_subplot(111)
            if is_numeric_dtype(df[combo1]) and is_numeric_dtype(df[combo2]):
                    axe.scatter(df[combo1],df[combo2])
                    axe.set_title(combo1 + " & "+ combo2)
            # refresh canvas
            self.canvas.draw()





