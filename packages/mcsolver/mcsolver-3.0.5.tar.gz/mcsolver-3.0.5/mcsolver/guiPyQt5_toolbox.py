#from pyface.qt import QtGui
from PyQt5.QtWidgets import QWidget, QTextEdit, QLineEdit, QLabel, QGridLayout, QListWidget, QListWidgetItem, QToolButton
from PyQt5.QtGui import QFontMetrics

class NoteFrm(QWidget):
    
    def __init__(self,textChangeEvent,parent=None,init_notes=[],init_data=[0,0],
                 row=False,height=40,
                 ):
        QWidget.__init__(self, parent)

        self.textChangeEvent=textChangeEvent
        self.totn=len(init_data)
        self.row=row
        self.h=height

        self.label_list=[]
        self.entry_list=[]
        self.data_list=[]

        self.grid = QGridLayout(self)
        #self.grid.setContentsMargins(0,0,0,0)
        #self.grid.setSpacing(0)
        self.loadlabel(init_notes)
        self.loadentries(init_data)

    def loadlabel(self,init_notes):
        self.label_list=[]
        for i in range(self.totn):
            label=QLabel(self)
            label.setText("%s"%init_notes[i])
            #label.setFixedHeight(self.h)
            label.resize(label.sizeHint())
            self.label_list.append(label)
        
        if self.row:
            for i in range(self.totn):
                self.grid.addWidget(self.label_list[i], 0, 2*i)
        else:
            for i in range(self.totn):
                self.grid.addWidget(self.label_list[i], i, 0)
    
    def loadentries(self,init_data):
        self.entry_list=[]
        for i in range(self.totn):
            entry=QLineEdit(self)
            entry.setText("%s"%init_data[i])
            #entry.setDisabled

            entry.textChanged.connect(self.textChangeEvent)
            self.entry_list.append(entry)
        
        if self.row:
            for i in range(self.totn):
                self.grid.addWidget(self.entry_list[i], 0, 2*i+1)
        else:
            for i in range(self.totn):
                self.grid.addWidget(self.entry_list[i], i, 1)
    
    def setValue(self,data=[1,600]):
        for i in range(self.totn):
            self.entry_list[i].setText("%s"%data[i])
    
    def report(self,strrep=False):
        self.data_list=[]
        if strrep:
            for ele in self.entry_list:
                value=ele.text()
                self.data_list.append(value)
        else:
            for ele in self.entry_list:
                value=ele.text()
                self.data_list.append(float(value))
        return self.data_list
    
class InfoList(QListWidget):

    def __init__(self, selectEvent, parent, dataFormat, initialInfo=[]):
        QListWidget.__init__(self,parent=parent)
        self.infoData=initialInfo
        self.dataFormat=dataFormat

        self.initInfo(self.infoData)
        self.itemClicked.connect(selectEvent)
    
    def initInfo(self,infoDataList=[]):
        for info in infoDataList:
            item=QListWidgetItem(self.dataFormat(info))
            self.addItem(item)
    
    def updateInfo(self,iitem=-1,info=[]):
        self.item(iitem).setText(self.dataFormat(info))
        self.infoData[iitem]=info
    
    def addInfo(self,info=[]):
        info[0]=self.count()
        item=QListWidgetItem(self.dataFormat(info))
        self.addItem(item)
        self.infoData.append(info)
    
    def removeInfo(self,iitem=-1):
        newInfoData=[]
        cnt=0
        for iinfo, infoData in enumerate(self.infoData):
            if iinfo==iitem:continue
            newInfoData.append([cnt]+infoData[1:])
        self.infoData=newInfoData
        self.clear()
        self.initInfo(self.infoData)
        
    '''
    def report(self):
        idxs = self.infoList.curselection()
        if len(idxs)==1:
            return self.infoData[idxs[0]]
        return []
    '''

class Button(QToolButton):

    def __init__(self, clickEvent, parent = None, text='Button') -> None:
        super().__init__(parent)

        self.clicked.connect(clickEvent)
        self.setText(text)