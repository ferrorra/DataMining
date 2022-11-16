from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QTreeWidgetItem
import sys, res
import pandas as pd
pd.options.mode.chained_assignment = None
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
import math
from pandas.api.types import is_numeric_dtype
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from matplotlib.colors import ListedColormap




from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    app = QApplication([])
    DF =pd.read_excel("Dataset1_ HR-EmployeeAttrition.xlsx")
    DFORIGINAL = pd.read_excel("Dataset1_ HR-EmployeeAttrition.xlsx")

    binning, moustaches,scat,histo = QWidget(),QWidget(),QWidget(),QWidget()

    def normalizer(self, combo):
        numeric = self.DF.select_dtypes(include=['number'])
        if combo.currentText()=="MinMax":
            min_max_df = numeric
            self.dataset_minmax(min_max_df)
            self.DF=min_max_df
        else:
            z_score_df = numeric
            self.zscores_dataset(z_score_df)
            self.DF = z_score_df
        self.visualiser_dataset(self.listView_3)   
            
    def dataset_minmax(self,dataset):
        for d in dataset.columns:
            cols = dataset[d].to_numpy()
            mini = min(cols)
            maxi = max(cols)
            dataset[d] = ((dataset[d] - mini) / (maxi - mini))*(1-0)+0
            
  
    def outlierss(self,df):
        mesures_de_dispersion = {}
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
        return pd.DataFrame.from_dict(mesures_de_dispersion, orient='index')
    
    #forward fill
    def ffill(self,df, d): 
        df[d].replace(np.nan, df.loc[df[d].first_valid_index()][d], inplace=True)
    
    #backward fill
    def bfill(self, df, d): 
        df[d].replace(np.nan, df.loc[df[d].last_valid_index()][d], inplace=True)    
        
    def treat_outlier(self,tendance, df5): 
        dfff =self.outlierss(self.DF)
        dicto = dict(dfff['Donnees aberanttes'][dfff['Donnees aberanttes'] != 'Aucune'])
        outliers = pd.DataFrame.from_dict(dicto, orient='index')
        print(outliers.head())
        for d in outliers.index:
            keys = outliers.loc[d].values
            t = tendance(self.DF,d)
            for k in keys:
                df5[d][df5[d]==k] = t
                
    def features(self, combo):
        df = pd.read_excel("Dataset1_ HR-EmployeeAttrition.xlsx")

        feats, featss =[],[]
        numeric = df.select_dtypes(include=['number'])
        categorical = df.select_dtypes(include=['object'])
        newdf= pd.DataFrame(df['Attrition'])
        if combo.currentText()=="Horrizontale":
            df.drop_duplicates(keep='first', inplace=True)
            newdf=df
        else:
            #on commence par les attributs qui ont une seule valeur
            for d in df.columns:
                if len(df[d].unique())==1:
                    df.drop(d, inplace=True, axis = 1)
            
            feats =self.chi2_feature_selection_scratch(categorical,detail=False)

            
            X = pd.get_dummies(data=df['Attrition'], drop_first=True) #1==yes
            X = X.rename({'Yes':'Attrition'}, axis=1)
            numeric['Attrition'] = X.squeeze()
            featss=self.pbc_scratch(numeric)
            
            for k,v in feats:
                if v>50:
                    newdf[k] =df[k]   

            for kk,vv in featss:
                if abs(vv)>0.1:
                    newdf[kk] =df[kk] 
                
        self.DF=newdf
        self.visualiser_dataset(self.listView_2)

    def pbc_scratch(self,data):
        featss =[]

        for d in data.columns[:-2]:
            bd_unique = data['Attrition'].unique()

            g0 = data[data['Attrition'] == bd_unique[0]][d]
            g1 = data[data['Attrition'] == bd_unique[1]][d]

            s_y = np.std(data[d])
            n = len(data['Attrition'])
            n0 = len(g0)
            n1 = len(g1)
            m0 = g0.mean()
            m1 = g1.mean()

            featss.append((d,(m0-m1)*math.sqrt((n0*n1)/n**2)/s_y))
        return featss

                
    def chi2_feature_selection_scratch(self,df, detail):    
        feat = []
        for d in df.columns[2:]:
            #---create the contingency table---
            df_cont = pd.crosstab(index = df['Attrition'], columns = df[d])

            if detail:
                print('---Contingency table (T)---')
                display(df_cont)


            #---calculate degree of freedom---(dof)
            degree_f = (df_cont.shape[0]-1) * (df_cont.shape[1]-1)

            #---sum up the totals for row and columns---
            df_cont.loc[:,'Total']= df_cont.sum(axis=1)
            df_cont.loc['Total']= df_cont.sum()

            if detail:   
                print('---Observed (O)---') 
                display(df_cont)



            #---create the expected value dataframe---
            df_exp = df_cont.copy()    
            df_exp.iloc[:,:] = np.multiply.outer(df_cont.sum(1).values,df_cont.sum().values) / df_cont.sum().sum()            

            if detail:   
                print('---Expected (E)---') 
                display(df_exp)


            # calculate chi-square values
            df_chi2 = ((df_cont - df_exp)**2) / df_exp    
            df_chi2.loc[:,'Total']= df_chi2.sum(axis=1)
            df_chi2.loc['Total']= df_chi2.sum()

            if detail:   
                print('---Chi-Square---') 
                display(df_chi2)

            df_chi2_yates = ((np.abs(df_cont - df_exp)-0.5)**2) / df_exp    
            df_chi2_yates.loc[:,'Total']= df_chi2_yates.sum(axis=1)
            df_chi2_yates.loc['Total']= df_chi2_yates.sum()

            if detail:   
                print('---Chi-Square---') 
                display(df_chi2_yates)


            #---get chi-square score---   
            chi_square_score = df_chi2.iloc[:-1,:-1].sum().sum()


            feat.append((d,chi_square_score))
        return feat
        
        
    def traiter_val(self,combo1,combo2):
        df = self.DF

        if combo1.currentText() =='Valeurs manquantes':
            if combo2.currentText() =='Moyenne':
                for d in df.columns:
                    if is_numeric_dtype(df[d]):
                        df[d].replace(np.nan, self.moyenne(self.DF,d), inplace=True) 
            elif combo2.currentText() =='Mediane':
                for d in df.columns:
                    if is_numeric_dtype(df[d]):
                        df[d].replace(np.nan, self.median(self.DF,d), inplace=True)
            elif combo2.currentText() =='Mode':
                for d in df.columns:
                    if is_numeric_dtype(df[d]):
                        if(isinstance(self.mode(self.DF,d),list)):
                            df[d].replace(np.nan, self.mode(self.DF,d)[0], inplace=True)
                        else:
                            df[d].replace(np.nan, self.mode(self.DF,d), inplace=True)

            elif combo2.currentText() =='Substitution':
                for d in df.columns:
                    self.bfill(df, d)
                    self.ffill(df, d)
                    
            elif combo2.currentText() =='Regression lineaire':
                for d in df.columns:
                    if is_numeric_dtype(df[d]) and not df[d][df[d].isnull()].empty:
                        df[d][df[d].isnull()] = self.regression_lineaire(df,d)
            else:
                pass
        elif combo1.currentText() =='Valeurs aberrantes':    
            if combo2.currentText() =='Moyenne':
                self.treat_outlier(self.moyenne,df)
            elif combo2.currentText() =='Mediane':
                self.treat_outlier(self.median,df)
            elif combo2.currentText() =='Mode':
                self.treat_outlier(self.mode,df)
            else:
                pass
        else:
            pass
        df.to_excel('Dataset1_ HR-EmployeeAttrition.xlsx', index =False)
        self.DF =pd.read_excel("Dataset1_ HR-EmployeeAttrition.xlsx")
        self.visualiser_dataset(self.listView)
            
    def regression_lineaire(self,df3,d):
        corr = df3.corr()
        cor_tar = abs(corr[d])
        relevant_features = cor_tar[cor_tar>0.5]
        df3 = df3[relevant_features.index]
        testdf = df3[df3[d].isnull()==True] #the missing values we should be predicting
        traindf = df3[df3[d].isnull()==False]
        y = traindf[d]
        traindf.drop(d,axis=1,inplace=True) #take off the values to be predicted
        testdf.drop(d,axis=1,inplace=True) #take off the values to be predicted
        lr = LinearRegression()
        lr.fit(traindf, y)
        lrpred = lr.predict(testdf)
        return lrpred




    def load_methodes(self,combo, propositions, ats):
        methodes=[]
        if combo.currentText() =='Valeurs manquantes':
            methodes = ['','Moyenne','Mediane','Mode', 'Substitution', 'Regression lineaire']
            propositions.clear()
            propositions.addItems(methodes)
            ats.clear()
            ats.addItem('')
            ats.addItems(self.DF.columns)
        else:
            methodes = ['','Moyenne','Mediane','Mode']
            propositions.clear()
            propositions.addItems(methodes)  
            ats.clear()
            ats.addItem('')
            dfff =self.outlierss(self.DF)
            dicto = dict(dfff['Donnees aberanttes'][dfff['Donnees aberanttes'] != 'Aucune'])
            outliers = pd.DataFrame.from_dict(dicto, orient='index')
            for d in outliers.index:
                if is_numeric_dtype(self.DF[d]):
                    ats.addItem(d)

    def load_dsc(self,combo,ats):
                atss = ['Age', 'DailyRate', 'DistanceFromHome', 'EmployeeNumber', 'HourlyRate',
           'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked',
           'PercentSalaryHike', 'TotalWorkingYears', 'TrainingTimesLastYear',
           'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole',
           'YearsSinceLastPromotion', 'YearsWithCurrManager']
                ats.clear()
                ats.addItem('')
                ats.addItems(atss)                


    def plottingMoustaches(self,tab,verticalLayout,plot="",combo1="",combo2=""):
        verticalLayout.removeWidget(self.moustaches)
        # creating a window object
        self.moustaches = Window(tab)
        self.moustaches.setMinimumSize(QtCore.QSize(400, 250))
        self.moustaches.setObjectName("Plot")

        self.moustaches.button.clicked.connect(lambda: self.moustaches.Moustaches(combo1))

        verticalLayout.addWidget(self.moustaches)
        # showing the window
        self.moustaches.show()
        
    def plotting_bins(self,tab,verticalLayout,combo1="",combo2=""):
        #verticalLayout.removeWidget(self.binning)
        # creating a window object
        self.bining = Window()
        #self.bining.setMaximumSize(QtCore.QSize(800, 500))
        self.bining.setMinimumSize(QtCore.QSize(600, 450))
        self.bining.setObjectName("Plot")

        self.bining.button.clicked.connect(lambda: self.bining.Bin(combo1,combo2))

        #verticalLayout.addWidget(self.bining)
        # showing the window
        self.bining.show()
        
    def compare_outliers(self,combo1=""):
            # creating a window object
            self.moustaches = Window()

            self.moustaches.setObjectName("Plot")
            if self.comboBox_11.currentText()=="Valeurs aberrantes":
                self.moustaches.button.clicked.connect(lambda: self.moustaches.draw_outliers(combo1,self.DFORIGINAL,self.DF))
            else:
                self.moustaches.button.clicked.connect(lambda: self.moustaches.draw_valmanquantes(combo1,self.DFORIGINAL,self.DF))


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
        
    def zscores_dataset(self,dataset):
        for d in dataset.columns:
            mean = sum(dataset[d]) / len(dataset[d])
            differences = [(value - mean)**2 for value in dataset[d]]
            sum_of_differences = sum(differences)
            standard_deviation = (sum_of_differences / (len(dataset[d]) - 1)) ** 0.5
            zscores = [(value - mean) / standard_deviation for value in dataset[d]]
            dataset[d] =zscores
        
        
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
        Form.setWindowIcon(QtGui.QIcon('resources/puzzle.png'))

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
        self.pushButton = QtWidgets.QPushButton(self.tab_9)
        self.pushButton.setStyleSheet("color:rgb(252, 55, 49);\n"
"font: 87 15pt \"Aileron Heavy\";\n"
"padding:10px;\n"
"border: 2px solid rgb(252, 55, 49);\n"
"border-radius:20px;")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_7.addWidget(self.pushButton)
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

        self.horizontalLayout_6.addWidget(self.comboBox_3)
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
        self.comboBox_4.activated.connect(lambda : self.highlight(self.comboBox_4, self.tableView_6))

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
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget_4 = QtWidgets.QTabWidget(self.tab_3)
        self.tabWidget_4.setGeometry(QtCore.QRect(-40, 0, 1241, 731))
        self.tabWidget_4.setStyleSheet("pane {\n"
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
        self.tabWidget_4.setTabPosition(QtWidgets.QTabWidget.East)
        self.tabWidget_4.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget_4.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget_4.setMovable(True)
        self.tabWidget_4.setTabBarAutoHide(True)
        self.tabWidget_4.setObjectName("tabWidget_4")
        self.tab_14 = QtWidgets.QWidget()
        self.tab_14.setObjectName("tab_14")
        self.comboBox_12 = QtWidgets.QComboBox(self.tab_14)
        self.comboBox_12.setGeometry(QtCore.QRect(110, 280, 321, 22))
        self.comboBox_12.setObjectName("comboBox_12")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        
        self.comboBox_122 = QtWidgets.QComboBox(self.tab_14)
        self.comboBox_122.setGeometry(QtCore.QRect(110, 350, 321, 22))
        self.comboBox_122.setObjectName("comboBox_122")
        self.comboBox_122.addItem("")
        self.comboBox_122.addItem("")
        self.comboBox_122.addItem("")
        self.comboBox_122.addItem("")
        self.comboBox_122.addItem("")
        self.comboBox_122.addItem("")


        self.comboBox_122.activated.connect(lambda: self.compare_outliers(self.comboBox_122.currentText()))

        self.listView = QtWidgets.QTableView(self.tab_14)
        self.listView.setGeometry(QtCore.QRect(640, 130, 301, 361))
        self.listView.setObjectName("listView")
        self.listView.setMaximumSize(QtCore.QSize(400, 600))
        self.label_23 = QtWidgets.QLabel(self.tab_14)
        self.label_23.setGeometry(QtCore.QRect(170, 17, 853, 62))
        self.label_23.setObjectName("label_23")
        self.comboBox_11 = QtWidgets.QComboBox(self.tab_14)
        self.comboBox_11.setGeometry(QtCore.QRect(110, 140, 331, 22))
        self.comboBox_11.setObjectName("comboBox_11")
        self.comboBox_11.addItem("")
        self.comboBox_11.addItem("")
        self.comboBox_11.addItem("")

        self.tabWidget_4.addTab(self.tab_14, "")
        self.tab_15 = QtWidgets.QWidget()
        self.tab_15.setObjectName("tab_15")
        self.label_24 = QtWidgets.QLabel(self.tab_15)
        self.label_24.setGeometry(QtCore.QRect(340, 10, 491, 81))
        self.label_24.setObjectName("label_24")

        self.label_31 = QtWidgets.QLabel(self.tab_15)
        self.label_31.setGeometry(QtCore.QRect(640, 100, 271, 81))
        self.label_31.setObjectName("label_31")
        self.label_32 = QtWidgets.QLabel(self.tab_15)
        self.label_32.setGeometry(QtCore.QRect(180, 100, 271, 81))
        self.label_32.setObjectName("label_32")
        self.comboBox_14 = QtWidgets.QComboBox(self.tab_15)
        self.comboBox_14.setGeometry(QtCore.QRect(120, 180, 391, 22))
        self.comboBox_14.setObjectName("comboBox_14")
        self.comboBox_14.addItem("")
        self.comboBox_14.addItem("")
        self.comboBox_14.addItem("")
        


        self.tabWidget_4.addTab(self.tab_15, "")
        self.tab_16 = QtWidgets.QWidget()
        self.tab_16.setObjectName("tab_16")
        self.label_25 = QtWidgets.QLabel(self.tab_16)
        self.label_25.setGeometry(QtCore.QRect(180, 30, 801, 61))
        self.label_25.setObjectName("label_25")
        self.label_33 = QtWidgets.QLabel(self.tab_16)
        self.label_33.setGeometry(QtCore.QRect(380, 100, 301, 81))
        self.label_33.setObjectName("label_33")
        self.comboBox_15 = QtWidgets.QComboBox(self.tab_16)
        self.comboBox_15.setGeometry(QtCore.QRect(340, 180, 391, 22))
        self.comboBox_15.setObjectName("comboBox_15")
        self.comboBox_15.addItem("")
        self.comboBox_15.addItem("")
        self.listView_2 = QtWidgets.QTableView(self.tab_16)
        self.listView_2.setGeometry(QtCore.QRect(410, 230, 256, 192))
        self.listView_2.setObjectName("listView_2")
        self.listView_2.setMinimumSize(QtCore.QSize(600, 400))
        self.listView_2.setMaximumSize(QtCore.QSize(600, 400))
        self.tabWidget_4.addTab(self.tab_16, "")
        self.tab_17 = QtWidgets.QWidget()
        self.tab_17.setObjectName("tab_17")
        self.label_34 = QtWidgets.QLabel(self.tab_17)
        self.label_34.setGeometry(QtCore.QRect(420, 100, 311, 81))
        self.label_34.setObjectName("label_34")
        self.comboBox_16 = QtWidgets.QComboBox(self.tab_17)
        self.comboBox_16.setGeometry(QtCore.QRect(380, 180, 391, 22))
        self.comboBox_16.setObjectName("comboBox_16")
        self.comboBox_16.addItem("")
        self.comboBox_16.addItem("")
        self.comboBox_16.addItem("")
        self.label_27 = QtWidgets.QLabel(self.tab_17)
        self.label_27.setGeometry(QtCore.QRect(390, 300, 381, 61))
        self.label_27.setText("")
        self.label_27.setObjectName("label_27")
        self.label_26 = QtWidgets.QLabel(self.tab_17)
        self.label_26.setGeometry(QtCore.QRect(430, 20, 261, 62))
        self.label_26.setObjectName("label_26")
        self.tabWidget_4.addTab(self.tab_17, "")
        self.tabWidget.addTab(self.tab_3, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.comboBox_13 = QtWidgets.QComboBox(self.tab_15)
        self.comboBox_13.setGeometry(QtCore.QRect(580, 180, 391, 22))
        self.comboBox_13.setObjectName("comboBox_13")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.textEdit.textChanged.connect(lambda: self.lookup(self.comboBox_2, self.textEdit.toPlainText(), self.tableView_4))   
        self.comboBox_11.activated.connect(lambda : self.load_methodes(self.comboBox_11,self.comboBox_12,self.comboBox_122))
        self.comboBox_11.activated.connect(lambda : self.traiter_val(self.comboBox_11,self.comboBox_12))
        self.comboBox_12.activated.connect(lambda : self.traiter_val(self.comboBox_11,self.comboBox_12))
        self.comboBox_14.activated.connect(lambda : self.load_dsc(self.comboBox_14,self.comboBox_13))
        self.comboBox_16.activated.connect(lambda : self.normalizer(self.comboBox_16))

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_2.setCurrentIndex(2)
        self.tabWidget_3.setCurrentIndex(3)
        self.tabWidget_4.setCurrentIndex(3)
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
        self.label_23.setText(_translate("Form", "Traitrement des valeurs manquantes et aberrantes"))
        self.comboBox_11.setItemText(0, _translate("Form", " "))
        self.comboBox_11.setItemText(1, _translate("Form", "Valeurs manquantes"))
        self.comboBox_11.setItemText(2, _translate("Form", "Valeurs aberrantes"))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_14), _translate("Form", "Traitement des valeurs"))
        self.label_24.setText(_translate("Form", "Discrétisation"))
        self.label_31.setText(_translate("Form", "Choisir attribut"))
        self.label_32.setText(_translate("Form", "Choisir classe"))
        self.comboBox_14.setItemText(0, _translate("Form", ""))
        self.comboBox_14.setItemText(1, _translate("Form", "Effectifs égaux"))
        self.comboBox_14.setItemText(2, _translate("Form", "Amplitudes égales"))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_15), _translate("Form", "Réduction des données"))
        self.label_25.setText(_translate("Form", "Réduction des données verticale et horrizontale"))
        self.label_33.setText(_translate("Form", "Choisir méthode"))
        self.comboBox_15.setItemText(0, _translate("Form", "Horrizontale"))
        self.comboBox_15.setItemText(1, _translate("Form", "Verticale"))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_16), _translate("Form", "Réduction de données"))
        self.label_34.setText(_translate("Form", "Choisir méthode"))
        self.comboBox_16.setItemText(0, _translate("Form", ""))
        self.comboBox_16.setItemText(1, _translate("Form", "MinMax"))
        self.comboBox_16.setItemText(2, _translate("Form", "Zscore"))
        self.label_26.setText(_translate("Form", "Normalisation"))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_17), _translate("Form", "Normalisation des données"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "Prétraitement des données"))
        self.tabWidget.currentChanged.connect(lambda: self.visualiser_dataset(self.tableView)) 
        self.tabWidget.currentChanged.connect(lambda: self.attributs(self.tableView_3))
        self.tabWidget_2.currentChanged.connect(lambda: self.attributs(self.tableView_3))
        self.listView_3 = QtWidgets.QTableView(self.tab_17)
        self.listView_3.setGeometry(QtCore.QRect(410, 230, 256, 192))
        self.listView_3.setObjectName("listView_3")
        self.listView_3.setMinimumSize(QtCore.QSize(600, 400))
        self.listView_3.setMaximumSize(QtCore.QSize(600, 400))
        

        
        self.tabWidget.currentChanged.connect(lambda: self.tendances(self.tableView_5)) 
        self.tabWidget.currentChanged.connect(lambda: self.mesures(self.tableView_6))

        self.comboBox_7.activated.connect(lambda: self.plottingScatter(self.tab_13,self.verticalLayout_17,"Scatter", self.comboBox_7.currentText(),self.comboBox_8.currentText()))
        self.comboBox_8.activated.connect(lambda: self.plottingScatter(self.tab_13,self.verticalLayout_17,"Scatter", self.comboBox_7.currentText(),self.comboBox_8.currentText())) 
        self.comboBox_6.activated.connect(lambda: self.plottingHist(self.tab_10,self.verticalLayout_16,"Hist", self.comboBox_6.currentText()))
        self.comboBox_5.activated.connect(lambda: self.plottingMoustaches(self.tab_12,self.verticalLayout_13,"Moustaches", self.comboBox_5.currentText()))
        self.comboBox_13.activated.connect(lambda: self.plotting_bins(self.tab_15,self.verticalLayout_13, self.comboBox_14.currentText(), self.comboBox_13.currentText()))
        self.comboBox_15.activated.connect(lambda : self.features(self.comboBox_15))


        


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
            self._data.iloc[index.row(), index.column()] = float(value)        
            dffff = pd.read_excel("Dataset1_ HR-EmployeeAttrition.xlsx")
            dffff.iloc[int(index.row()), int(index.column())] =float(value)    
            dffff.update(self._data)
            dffff.to_excel('Dataset1_ HR-EmployeeAttrition.xlsx', index =False)
            return True
        return False




class Window(QWidget):
    DFORIGINAL =pd.read_excel("Dataset1_ HR-EmployeeAttrition.xlsx")
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
        
    def EqualWidth(self, df7):
        ats = ['Age', 'DailyRate', 'DistanceFromHome', 'EmployeeNumber', 'HourlyRate',
           'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked',
           'PercentSalaryHike', 'TotalWorkingYears', 'TrainingTimesLastYear',
           'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole',
           'YearsSinceLastPromotion', 'YearsWithCurrManager']
        for d in ats:
            maximum = df7[d].max()
            minimum = df7[d].min()
            rangrang= maximum - minimum 
            k= 1+3*math.log10(len(df7[d]))
            width = int(rangrang/k) 
            min_value = int(np.floor(minimum))
            max_value = int(np.ceil( maximum))
            if(width==0):
                width = 1
            intervals = [i for i in range(min_value, max_value + width,width)]
            df7[f'{d}_Bins'] = pd.cut(x=df7[d], bins=intervals,include_lowest=True)
            t1 = df7[f'{d}_Bins'].value_counts() / len(df7)
            
    def EqualFreq(self, df,q):   
        ats = ['Age', 'DailyRate', 'DistanceFromHome', 'EmployeeNumber', 'HourlyRate',
           'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked',
           'PercentSalaryHike', 'TotalWorkingYears', 'TrainingTimesLastYear',
           'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole',
           'YearsSinceLastPromotion', 'YearsWithCurrManager'] 
        dffffffffff = pd.read_excel("org.xlsx")
        all = []
        for d in ats:
            a = len(df[d])
            n = int(a / q)
            for i in range(0, q):
                arr = []
                for j in range(i * n, (i + 1) * n):
                    if j >= a:
                        break
                    arr = arr + [df[d][j]]
                all.extend(arr)
            dffffffffff[d]= pd.Series(all)

        return dffffffffff
        
    # action called by the push button
    def Bin(self, combo1,combo2):

        # clearing old figure
        self.figure.clear()
        df = self.DF
        
        
        if combo1=="Effectifs égaux":
            dff = self.EqualFreq(df,3)
            axe = self.figure.add_subplot(121)
            sns.countplot(x=self.DFORIGINAL[combo2], ax= axe)
            axe.set_title("Before")
            axe = self.figure.add_subplot(122)
            sns.countplot(x=dff[combo2], ax= axe)
            axe.set_title("After")  
            
            
        elif combo1=="Amplitudes égales":
            print('waaaaaaaa')
            self.EqualWidth(df)
            axe = self.figure.add_subplot(121)
            sns.countplot(x=self.DFORIGINAL[combo2], ax= axe)
            axe.set_title("Before")
            axe = self.figure.add_subplot(122)
            sns.countplot(x=df[f'{combo2}_Bins'], ax= axe)
            axe.set_title("After")  
        

        
      
            
        # refresh canvas
        self.canvas.draw()

    def draw_outliers(self, combo,dfbefore, dfafter):

        # clearing old figure
        self.figure.clear()
        axe = self.figure.add_subplot(121)
        axe.boxplot(dfbefore[combo])
        axe.set_title("Before")
        axe = self.figure.add_subplot(122)
        axe.boxplot(dfafter[combo])
        axe.set_title("After")
        # refresh canvas
        self.canvas.draw()
        
    def draw_valmanquantes(self, combo,dfbefore, dfafter):

        # clearing old figure
        self.figure.clear()
        axe = self.figure.add_subplot(121)
        sns.heatmap(np.asarray(dfbefore[combo].isnull()).reshape(-1,1),yticklabels=False,cbar=False,ax=axe,cmap=ListedColormap([ 'yellow', 'red']))
        #axe.boxplot(dfbefore[combo])
        axe.set_title("Before")
        axe = self.figure.add_subplot(122)
        sns.heatmap(np.asarray(dfafter[combo].isnull()).reshape(-1,1),yticklabels=False,cbar=False,ax=axe,cmap=ListedColormap(['yellow', 'red']))
        #axe.boxplot(dfafter[combo])
        axe.set_title("After")
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



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())