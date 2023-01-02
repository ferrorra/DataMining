
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import warnings
from collections import Counter
warnings.filterwarnings("ignore")
from dbscan import dbscan
from agnes import agglomerative_clustering
from utils import *
from sklearn.metrics import silhouette_score
from PyQt5.QtGui import QMovie
from visualisation import pca_scatterplot, radar_plot, box_plots, bar_plot, plot_3dd




class Ui_Form(object):
    def setupUi(self, Form):
        df = pd.read_excel("data.xlsx")
        df.drop(columns = df.columns[0], axis = 1, inplace= True)
        df.drop(columns = df.columns[1], axis = 1, inplace= True)   
        self.data = df.select_dtypes(include='number') #on ne garde que les variables numériques
        self.distances = self.manhattan_distance(self.data.to_numpy())
        self.new_data = self.data.copy()
        self.new_data['Cluster_dbscan'] = 0
        self.dbscan_silouette = 0.00
        self.agnes_silouette = 0.00


        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(1768, 843)
        Form.setMaximumSize(QtCore.QSize(1768, 16777215))
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
"}")
        self.tabWidget_2.setTabPosition(QtWidgets.QTabWidget.East)
        self.tabWidget_2.setTabShape(QtWidgets.QTabWidget.Triangular)
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
        self.verticalLayout.addWidget(self.tableView)
        self.label_4 = QtWidgets.QLabel(self.tab_5)
        self.label_4.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_5)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
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
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.tab_7)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_5.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.textEdit = QtWidgets.QTextEdit(self.tab_7)
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setPlaceholderText("3")
        self.horizontalLayout_5.addWidget(self.textEdit)
        self.label_3 = QtWidgets.QLabel(self.tab_7)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_3.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.textEdit_2 = QtWidgets.QTextEdit(self.tab_7)
        self.textEdit_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setPlaceholderText("5")
        self.horizontalLayout_5.addWidget(self.textEdit_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.label_6 = QtWidgets.QLabel(self.tab_7)
        self.label_6.setMinimumSize(QtCore.QSize(0, 500))
        self.label_6.setObjectName("label_6")
        self.verticalLayout_4.addWidget(self.label_6)
        self.pushButton = QtWidgets.QPushButton(self.tab_7)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton.setStyleSheet("background-color:rgb(252, 55, 49);\n"
"color:white;\n"
"border-radius:20px;\n"
"font-size : 20px;")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda : self.plots(self.data, self.new_data,'Cluster_dbscan'))
        self.verticalLayout_4.addWidget(self.pushButton)
        self.tabWidget_2.addTab(self.tab_7, "")
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
        self.label_7.setObjectName("label_7")
        self.verticalLayout_9.addWidget(self.label_7)
        self.verticalLayout_10.addLayout(self.verticalLayout_9)
        self.tableView_5 = QtWidgets.QTableView(self.tab_6)
        self.tableView_5.setMinimumSize(QtCore.QSize(0, 500))
        self.tableView_5.setObjectName("tableView_5")
        self.verticalLayout_10.addWidget(self.tableView_5)
        self.label_15 = QtWidgets.QLabel(self.tab_6)
        self.label_15.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_15.setObjectName("label_15")
        self.verticalLayout_10.addWidget(self.label_15)
        self.lineEdit = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_10.addWidget(self.lineEdit)
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
        self.label_11.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_7.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.tab_11)
        self.label_12.setMaximumSize(QtCore.QSize(150, 50))
        self.label_12.setStyleSheet("border-image: url(:/images/resources/network-chart.png);")
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_7.addWidget(self.label_12)
        self.textEdit_3 = QtWidgets.QTextEdit(self.tab_11)
        self.textEdit_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_3.setPlaceholderText("2")
        self.horizontalLayout_7.addWidget(self.textEdit_3)
        self.label_14 = QtWidgets.QLabel(self.tab_11)
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_14.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_7.addWidget(self.label_14)
        self.comboBox = QtWidgets.QComboBox(self.tab_11)
        self.comboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(['complete', 'single', 'average', 'centroid'])
        self.horizontalLayout_7.addWidget(self.comboBox)
        self.verticalLayout_11.addLayout(self.horizontalLayout_7)
        self.verticalLayout_12.addLayout(self.verticalLayout_11)
        self.label_13 = QtWidgets.QLabel(self.tab_11)
        self.label_13.setMinimumSize(QtCore.QSize(0, 500))
        self.label_13.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_13.setObjectName("label_13")
        self.verticalLayout_12.addWidget(self.label_13)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_11)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_2.setStyleSheet("background-color:rgb(252, 55, 49);\n"
"color:white;\n"
"border-radius:20px;\n"
"font-size : 20px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda : self.plots(self.data, self.new_data,'Cluster_agnes'))

        self.verticalLayout_12.addWidget(self.pushButton_2)
        self.tabWidget_3.addTab(self.tab_11, "")
        self.horizontalLayout_3.addWidget(self.tabWidget_3)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    # Calculer la distance de manhattan entre tout les points du dataset
    # Pour économiser du temps d'execution, on ne calcule que la matrice superieure de la matrice de distance
    def manhattan_distance(self, df):
        distances = np.zeros((len(df), len(df)))
        for i in range(len(df)):
            for j in range(i+1, len(df)):
                dist = np.sum(np.abs(df[i] - df[j]))
                
                distances[i][j] = dist
                distances[j][i] = dist
    
        return distances

    def init_dbscan(self):
        # On teste l'algorithme DBSCAN avec différentes valeurs de eps et min_pts
        min_pts = [2, 5, 7, 10, 15, 20, 25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 750, 1000]
        results = []
        for i in range(1, 16):
            for j in range(len(min_pts)):
                len_clusters = []
                clusters, noise = dbscan(self.distances, i, min_pts[j])
                for k in range(len(clusters)):
                    len_clusters.append(len(clusters[k]))
                results.append([i, min_pts[j], len(clusters), len_clusters, len(noise)])
        results = pd.DataFrame(results, columns = ['eps', 'min_pts', 'clusters', 'len_clusters', 'noise'])
        return results

    def try_dbscan(self, textfield, eps=3, minpts=5):
        y_pred = dbscan(self.distances,eps,minpts) #on fait nos prédictions
        #on créé un nouveau dataset avec les predictions
        cluster_index = 1
        for c in y_pred[0]: 
            for row in c:
                self.new_data.loc[row,'Cluster_dbscan'] = cluster_index
            cluster_index+=1
        for noise in y_pred[1]:
                self.new_data.loc[noise,'Cluster_dbscan'] = -1
        textfield.setText(str(silhouette_score(self.data, self.new_data.Cluster_dbscan, metric='manhattan')))
        #visualization thingy thing
        self.movie = QMovie("dbscan_new.gif")
        self.label_6.setMovie(self.movie)
        #self.label.setScaledContents(True)
        self.movie.start()

    def try_agnes(self, textfield, nb_clusters=2, linkage_method='complete'):
        y_pred = agglomerative_clustering(self.data, nb_clusters, linkage_method)
        #on créé un nouveau dataset avec les predictions
        cluster_index = 1
        for c in y_pred: 
           for row in c:
               self.new_data.loc[row,'Cluster_agnes'] = cluster_index
           cluster_index+=1
        textfield.setText(str(silhouette_score(self.data, self.new_data.Cluster_agnes, metric='manhattan')))
        #visualization thingy thing
        self.movie = QMovie("agnes_new.gif")
        self.label_13.setMovie(self.movie)
        #self.label.setScaledContents(True)
        self.movie.start()

    def show_dbscan_grid(self, view):
        #dff= self.init_dbscan()
        dff = pd.read_csv('dbscan.csv')
        dff = dff.drop(['Unnamed: 0'], axis = 1)
        model = pandasModel(dff)
        view.setModel(model)
        view.resize(500, 200)
        view.show()
        self.try_dbscan(self.lineEdit_2)

    def plots(self, data, new_data,cluster_type):
        if(len(self.textEdit.toPlainText()) !=0 & len(self.textEdit_2.toPlainText())  != 0):
            self.try_dbscan(self.lineEdit_2, int(self.textEdit.toPlainText()), int(self.textEdit_2.toPlainText()))
        if(len(self.textEdit_3.toPlainText())  != 0):
            self.try_agnes(self.lineEdit, int(self.textEdit_3.toPlainText()), self.comboBox.currentText())
        pca_scatterplot(data, new_data,cluster_type)
        radar_plot(data, new_data,cluster_type)
        box_plots(data, new_data,cluster_type)
        bar_plot(data, new_data,cluster_type)

    def init_agnes(self):
        linkage_methods = ['complete', 'single', 'average', 'centroid']
        number_of_clusters = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        agnes_results = []
        for i in range(len(number_of_clusters)):
            for j in range(len(linkage_methods)):
                clusters = agglomerative_clustering(self.data, number_of_clusters[i], linkage_methods[j])
                clusters_length = []
                for c in clusters:
                    clusters_length.append(len(c))
                agnes_results.append([number_of_clusters[i], linkage_methods[j], clusters_length])
        agnes_results = pd.DataFrame(agnes_results, columns = ['Number of clusters', 'Linkage method', 'Clusters length'])
        return agnes_results

    def show_agnes_grid(self, view):
        #dff= self.init_agnes()
        dff = pd.read_csv('agnes.csv')
        dff = dff.drop(['Unnamed: 0'], axis = 1)
        model = pandasModel(dff)
        view.setModel(model)
        view.resize(500, 200)
        view.show()
        self.try_agnes(self.lineEdit)


    def first_setup(self):
        self.show_dbscan_grid(self.tableView)
        self.show_agnes_grid(self.tableView_5)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Data Mining Project Part 5"))
        self.label.setText(_translate("Form", "Application d\'algorithmes de clustering basé densité : Résultats"))
        self.label_4.setText(_translate("Form", "Silouette Score"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("Form", "Résultats"))
        self.label_2.setText(_translate("Form", "Application d\'algorithmes de clustering basé densité : Visualisation"))
        self.label_5.setText(_translate("Form", "Eps"))
        self.label_3.setText(_translate("Form", "MinPts"))
        self.label_6.setText(_translate("Form", "3D model Gif"))
        self.pushButton.setText(_translate("Form", "Plus de visualisations"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_7), _translate("Form", "Visualisation"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "DBSCAN"))
        self.label_7.setText(_translate("Form", "Application d\'algorithmes de clustering basé hiérarchie: resultats"))
        self.label_15.setText(_translate("Form", "Silouette Score"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_6), _translate("Form", "Résultats"))
        self.label_10.setText(_translate("Form", "Application d\'algorithmes de clustering basé hiérarchie : visualisation"))
        self.label_11.setText(_translate("Form", "Nombre de clusters"))
        self.label_14.setText(_translate("Form", "Chainage"))
        self.label_13.setText(_translate("Form", "3D giffff"))
        self.pushButton_2.setText(_translate("Form", "Plus de visualisations"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_11), _translate("Form", "Visualisation"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "AGNES"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    ui.first_setup()
    Form.show()
    sys.exit(app.exec_())
