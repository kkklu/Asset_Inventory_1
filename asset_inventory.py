# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication,QMessageBox,QDialog,QFileDialog
from PySide2.QtCore import QFile, QIODevice,Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
import form_ui
import pandas as pd
from pandas import DataFrame
import numpy as np
import numpy as np2
from PySide2.QtCore import qDebug
import time,datetime
from openpyxl import load_workbook
import pyttsx3
import threading

from form_ui import Ui_Widget
from PySide2.QtWidgets import *

class Asset_Inventory(QWidget,form_ui.Ui_Widget): #有没有机会改为QWidget类
    def __init__(self):
        #self.__init__(self)
        #QDialog.__init__(self)

        #1 load ui 方法1：
        QWidget.__init__(self)
        self.initUI()
        #self.init_tts()

        self.openpushButton.clicked.connect(self.openfile)
        self.openpushButton.clicked.connect(self.creat_table_show)
        self.lineEdit.editingFinished.connect(self.readline_scancode)
        
        
        
        pass  # call __init__(self) of the custom base class here
    
    def initUI(self):
        #1 load ui 方法1： 
        self.setupUi(self)
        

        #2 load ui 方法2：不好用，主要是没有控件的提示
        """
        loader=QUiLoader()
        ui_file=QFile("form.ui")
        if not ui_file.open(QIODevice.ReadOnly):
            #loadui_messagebox = QMessageBox()
            #loadui_messagebox.warning(self, "错误", "无法打开UI文件")
            sys.exit(-1)
        self.window= loader.load(ui_file)
        ui_file.close()
        """


    #https://www.jianshu.com/p/88f48e667c17
    #读取表格并显示
    def openfile(self):
        ###===========读取表格，转换表格，========
        openfile_name=QFileDialog.getOpenFileName(self,'选择文件','','Excel files(*.xlsx , *.xls)')
        global path_openfile_name
        path_openfile_name=openfile_name[0]
        if len(path_openfile_name)>0:
            global all_DataFrame 
            all_DataFrame = pd.read_excel(path_openfile_name,engine='openpyxl',header=0) #input_table is dataframe?
        else:
            pass #后期写异常提示
    
    def creat_table_show(self):
        if all_DataFrame is not None:#len(path_openfile_name)>0:
            input_table=all_DataFrame#['盘点情况'].#.isin(['未盘点'])
            #input_table=pd.read_excel(path_openfile_name) #input_table is dataframe?
            input_rows=input_table.shape[0]
            input_colunms=input_table.shape[1]
            input_table_header=input_table.columns.values.tolist()

            #self.lcdNumber.value=input_rows
            #self.lcdNumber.display(input_rows)
        
        ###===========读取表格，转换表格，============================================
        ###======================给tablewidget设置行列表头=====
        self.tableWidget.setColumnCount(input_colunms)
        self.tableWidget.setRowCount(input_rows) 
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)

        self.tableWidget_2.setColumnCount(input_colunms)
        self.tableWidget_2.setRowCount(input_rows) 
        self.tableWidget_2.setHorizontalHeaderLabels(input_table_header)
        ###======================给tablewidget设置行列表头============================

        ###================遍历表格每个元素，同时添加到tablewidget中=============
        p=0
        #i=1
        for i in range(input_rows):
            if input_table.iat[i,12] != '已盘点':
                input_table_rows_values = input_table.iloc[[i]]
            #print(input_table_rows_values)
            #if input_table_rows_values['盘点情况'].isin(['未盘点']):
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
        #print(input_table_rows_values_list)
                for j in range(input_colunms):
                    input_table_items_list = input_table_rows_values_list[j]
                    #print(input_table_items_list)
                    # print(type(input_table_items_list))
        ##==============将遍历的元素添加到tablewidget中并显示=======================

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items) 
                    newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                    self.tableWidget.setItem((i-p), j, newItem) 
                    self.lcdNumber.display((i-p))
        ###================遍历表格每个元素，同时添加到tablewidget中========================
            else:
                p=p+1
                #self.tableWidget_2.setRowCount(p) 
                input_table_rows_values_2 = input_table.iloc[[i]]
            #print(input_table_rows_values)
            #if input_table_rows_values['盘点情况'].isin(['未盘点']):
                input_table_rows_values_array_2 = np2.array(input_table_rows_values_2)
                input_table_rows_values_list_2 = input_table_rows_values_array_2.tolist()[0]
        #print(input_table_rows_values_list)
                for q in range(input_colunms):
                    input_table_items_list_2 = input_table_rows_values_list_2[q]
                    #print(input_table_items_list)
                    # print(type(input_table_items_list))
        ##==============将遍历的元素添加到tablewidget中并显示=======================

                    input_table_items_2 = str(input_table_items_list_2)
                    newItem_2 = QTableWidgetItem(input_table_items_2) 
                    newItem_2.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                    self.tableWidget_2.setItem(p-1, q, newItem_2) 
                    self.lcdNumber_2.display(p)
        else:
            pass#self.centralWidget.show()
    
            # 函数名：AI语音播报


    def Artificial_voice_playback_1(self,messages):
        
        # 创建语音引擎
        engine = pyttsx3.init()

        # 设置语音速度
        engine.setProperty('rate', 180)

        volume = engine.getProperty('volume')
        qDebug(f'语音音量：{volume}')

        # 设置语音音量
        engine.setProperty('volume', 1)

        # 定义要转换为语音的消息
        # messages = ["现在是北京时间", "现在是纽约时间"]
        
        # 循环播放消息
        #    while True:
        # for message in messages:
        # 将消息转换为语音并播放
        engine.say(messages)
        engine.runAndWait()
        # 等待语音播放完毕
        #time.sleep(1)
        # 等待60秒后再次循环播放消息
        # time.sleep(60)
    
    def readline_scancode(self):
        qDebug("二维码为： "+self.lineEdit.text())
        #1 查找
        if (all_DataFrame is not None) and (self.lineEdit.text() is not None):
            #pass
            for i in range(all_DataFrame.shape[0]):
                if all_DataFrame.iat[i,1] ==self.lineEdit.text():
                    qDebug("找到该二维码")
                    if all_DataFrame.iat[i,12]!="已盘点":  #https://blog.csdn.net/rouge_eradiction/article/details/108586925

                        #2 写入excel
                        all_DataFrame.iloc[i,12]="已盘点"
                        
                        #with pd.ExcelWriter(path_openfile_name) as writer:
                        #writer=pd.ExcelWriter('new.xlsx',engine='openpyxl')#,mode='w',if_sheet_exists='replace')                   
                        #book=load_workbook(path_openfile_name)
                        #writer.book=book
                        #writer.sheets=dict((ws.title,ws) for ws in book.worksheets())
                        
                        #https://blog.csdn.net/HJ_xing/article/details/112390297
                        #https://blog.csdn.net/qq_45176548/article/details/115290941
                        #https://zhuanlan.zhihu.com/p/363810440


                        all_DataFrame.to_excel(path_openfile_name,sheet_name='Sheet',index=False,header=True)#,startrow=i,startcol=12)
                        
                        #3显示
                        self.creat_table_show()
                        #4 语音提示
                        #messsage='已录入'
                        qDebug('已录入')
                        self.Artificial_voice_playback_1('已录入')

                        break
                    else: # elif all_DataFrame.iat[i,12]=="已盘点":
                        #pass #提示“重复盘点“
                        qDebug("重复盘点")
                        #messsage='重复盘点'
                        self.Artificial_voice_playback_1('重复盘点')
                        break
                else: 
                    if i == (len(range(all_DataFrame.shape[0]))-1):
                        qDebug("无此项")
                        #messsage='表中找不到此项资产'
                        self.Artificial_voice_playback_1('无此项')
                        #pass
                    #qDebug("表中无此项资产")

        #time.sleep(1)
        self.lineEdit.clear()
        pass
            




if __name__ == "__main__":
    app = QApplication([])
    window = Asset_Inventory()
    #window.window.show()
    window.show()
    sys.exit(app.exec_())
