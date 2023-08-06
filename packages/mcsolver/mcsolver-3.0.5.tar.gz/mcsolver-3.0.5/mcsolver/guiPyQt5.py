import sys
import re
import time
from PyQt5 import QtCore

from pyface.qt import QtGui, QtCore
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor

import numpy as np

from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QToolTip, QToolBox, QPushButton, QGridLayout, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QBoxLayout, QGroupBox, QToolButton
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

try:
    from .guiPyQt5_toolbox import NoteFrm, InfoList, Button
    from . import WannierKit as wan
except:
    from guiPyQt5_toolbox import NoteFrm, InfoList, Button
    import WannierKit as wan

class LatticePannel(QGroupBox):
    def __init__(self, parent=None):
        QGroupBox.__init__(self, parent)
        #self.setTitle("Cell basis and supercell size")
        self.setFixedHeight(300)
        self.a0GUI=NoteFrm(self.textChangeEvent,parent=None,init_notes=['a1:','',''],init_data=[1.000,0.000,0.000],row=True)
        self.a1GUI=NoteFrm(self.textChangeEvent,parent=None,init_notes=['a2:','',''],init_data=[0.000,1.000,0.000],row=True)
        self.a2GUI=NoteFrm(self.textChangeEvent,parent=None,init_notes=['a3:','',''],init_data=[0.000,0.000,1.000],row=True)
        self.supercellGui=NoteFrm(self.textChangeEvent,parent=None,init_notes=['SC:','x','x'],init_data=[16,16,1],row=True)
        formulaLable = QLabel()
        formulaLable.setPixmap(QPixmap("./formula.jpg"))
        
        layoutCrystalFrame=QVBoxLayout()
        layoutCrystalFrame.setContentsMargins(0,0,0,0)
        #layoutCrystalFrame.setAlignment()
        layoutCrystalFrame.addWidget(self.a0GUI)
        layoutCrystalFrame.addWidget(self.a1GUI)
        layoutCrystalFrame.addWidget(self.a2GUI)

        layoutSC=QVBoxLayout()
        layoutSC.addWidget(formulaLable)
        layoutSC.addWidget(self.supercellGui)

        layout = QHBoxLayout(self)
        layout.addLayout(layoutCrystalFrame)
        layout.addLayout(layoutSC)
    
    def textChangeEvent(self):
        print(self.a0GUI.report())

class OrbitalPannel(QGroupBox):
    def __init__(self, parent=None):
        QGroupBox.__init__(self, parent)

        #self.setTitle("Orbital information")
        self.OrbListGUI=InfoList(self.selectEvent,parent=None,dataFormat=self.orbitalDataFormat, initialInfo=[[0,0,1,(0.,0.,0.),(0.,0.,0.)],])
        
        self.OrbModGUI1=NoteFrm(self.textChangeEvent,parent=None, init_notes=['ID:','Type:','Init spin:'],init_data=[0,0,1],row=True)
        self.OrbModGUI1.entry_list[0].setDisabled(True)
        self.OrbModGUI2=NoteFrm(self.textChangeEvent,parent=None, init_notes=['pos: fx','fy','fz'],init_data=[0.,0.,0.],row=True)
        self.OrbModGUI3=NoteFrm(self.textChangeEvent,parent=None, init_notes=['Ani: Dx','Dy','Dz'],init_data=[0,0,0],row=True)
        
        self.addBtn=Button(self.addOrb,None,'add')
        self.resetBtn=Button(self.resetOrb,None,'reset')
        self.deletBtn=Button(self.deleteOrb,None,'delete')

        layoutOrbModGUI = QVBoxLayout()
        layoutOrbModGUI.setContentsMargins(0,0,0,0)
        layoutOrbModGUI.setSpacing(0)
        layoutOrbModGUI.addWidget(self.OrbModGUI1)
        layoutOrbModGUI.addWidget(self.OrbModGUI2)
        layoutOrbModGUI.addWidget(self.OrbModGUI3)

        layoutBtnGUI = QHBoxLayout()
        layoutBtnGUI.setAlignment
        layoutBtnGUI.addWidget(self.addBtn)
        layoutBtnGUI.addWidget(self.resetBtn)
        layoutBtnGUI.addWidget(self.deletBtn)

        layoutOrbModGUI.addLayout(layoutBtnGUI)

        layout = QVBoxLayout(self)
        
        layout.addWidget(self.OrbListGUI)
        layout.addLayout(layoutOrbModGUI)
    
    def setStructureVisualizer(self,visualizer):
        self.struVisual=visualizer

    def selectEvent(self,item):
        print("Selected",item.text())
        _orbID, spin, fx, fy, fz, Dx, Dy, Dz= re.findall('[0-9.-]+',item.text())
        orbID=int(_orbID)

        self.OrbModGUI1.setValue([orbID,0,spin])
        self.OrbModGUI2.setValue([fx,fy,fz])
        self.OrbModGUI3.setValue([Dx,Dy,Dz])

        self.struVisual.update(lightOrb=orbID)
    
    def orbitalDataFormat(self,info):
        return 'Orb%d Spin: %.1f FracX: %.3f %.3f %.3f Ani: %.2f %.2f %.2f'%(info[0],info[2],info[3][0],info[3][1],info[3][2],info[4][0],info[4][1],info[4][2])

    def textChangeEvent(self):
        pass

    def getDataFromOrbModGUI(self):
        _orbID, _orbType, spin = self.OrbModGUI1.report()
        orbID, orbType = int(_orbID), int(_orbType)
        fx,fy,fz = self.OrbModGUI2.report()
        Dx,Dy,Dz = self.OrbModGUI3.report()
        return [orbID,orbType,spin,(fx,fy,fz),(Dx,Dy,Dz)]

    def addOrb(self):
        self.OrbListGUI.addInfo(info=self.getDataFromOrbModGUI())
        self.struVisual.update()
    
    def resetOrb(self):
        info=self.getDataFromOrbModGUI()
        self.OrbListGUI.updateInfo(info[0],info=info)
        self.struVisual.update()

    def deleteOrb(self):
        info=self.getDataFromOrbModGUI()
        self.OrbListGUI.removeInfo(info[0])
        self.struVisual.update()

class BondPannel(QGroupBox):
    def __init__(self, parent=None):
        QGroupBox.__init__(self, parent)

        #self.setTitle("Bond information")
        self.BondListGUI=InfoList(self.selectEvent,parent=None,dataFormat=self.bondDataFormat, 
                                  initialInfo=[[0,[-1,-1,-1,0,0,0,0,0,0],[0,0,(1,0,0)]],[1,[-1,-1,-1,0,0,0,0,0,0],[0,0,(0,1,0)]]])

        self.bondBasicGUI=NoteFrm(self.textChangeEvent,parent=None, init_notes=['ID:','source id','target id'],init_data=[0,0,0],row=True)
        self.bondBasicGUI.entry_list[0].setDisabled(True)
        self.bondOverLatGUI=NoteFrm(self.textChangeEvent,parent=None, init_notes=['over Lat.','',''],init_data=[1,0,0],row=True)
        noteLabel=QLabel("Note all energy units are in Kelvin (1meV=11.604609K)",None)

        self.JxGUI=NoteFrm(self.textChangeEvent,parent=None,init_notes=['xx','xy','xz'],init_data=[-1.000,0.000,0.000],row=True)
        self.JyGUI=NoteFrm(self.textChangeEvent,parent=None,init_notes=['yx','yy','yz'],init_data=[0.000,-1.000,0.000],row=True)
        self.JzGUI=NoteFrm(self.textChangeEvent,parent=None,init_notes=['zx','zy','zz'],init_data=[0.000,0.000,-1.000],row=True)

        self.addBtn=Button(self.addBond,None,'add')
        self.resetBtn=Button(self.resetBond,None,'reset')
        self.deletBtn=Button(self.deleteBond,None,'delete')

        layoutButton = QHBoxLayout()
        layoutButton.addWidget(self.addBtn)
        layoutButton.addWidget(self.resetBtn)
        layoutButton.addWidget(self.deletBtn)

        boxJ = QGroupBox("J (in Kelvin)",None)
        layoutJ = QVBoxLayout(boxJ)
        layoutJ.setSpacing(0)
        layoutJ.addWidget(self.JxGUI)
        layoutJ.addWidget(self.JyGUI)
        layoutJ.addWidget(self.JzGUI)

        boxConnect=QGroupBox("Bond connection",None)
        layoutV1 = QVBoxLayout(boxConnect)
        layoutV1.setSpacing(0)
        layoutV1.addWidget(self.bondBasicGUI)
        layoutV1.addWidget(self.bondOverLatGUI)
        layoutV1.addLayout(layoutButton)
        layoutV1.addWidget(noteLabel)

        #boxJEditor= QGroupBox("Edit bond",self)
        layoutH1 = QHBoxLayout()#boxJEditor)
        layoutH1.addWidget(boxConnect)
        layoutH1.addWidget(boxJ)

        layout = QVBoxLayout(self)
        layout.addWidget(self.BondListGUI)
        layout.addLayout(layoutH1)

    def setStructureVisualizer(self,visualizer):
        self.struVisual=visualizer
    
    def selectEvent(self,item):
        print("Selected",item.text())
        _bondID,_sourceID,_targetID,_oL1,_oL2,_oL3,Jxx,Jyy,Jzz,Jxy,Jxz,Jyz,Jyx,Jzx,Jzy=[float(x) for x in re.findall('[0-9.-]+',item.text())]
        bondID,sourceID,targetID,oL1,oL2,oL3 = int(_bondID),int(_sourceID),int(_targetID),int(_oL1),int(_oL2),int(_oL3)
        
        self.bondBasicGUI.setValue([bondID,sourceID,targetID])
        self.bondOverLatGUI.setValue([oL1,oL2,oL3])
        self.JxGUI.setValue([Jxx,Jxy,Jxz])
        self.JyGUI.setValue([Jyx,Jyy,Jyz])
        self.JzGUI.setValue([Jzx,Jzy,Jzz])

        self.struVisual.update(lightID=bondID)
    
    def bondDataFormat(self,info):
        return 'Bond%d orb%d~orb%d [%d %d %d] J: xx %.3f yy %.3f zz %.3f xy %.3f xz %.3f yz %.3f yx %.3f zx %.3f zy %.3f'%(info[0],info[2][0],info[2][1],info[2][2][0],info[2][2][1],info[2][2][2],info[1][0],info[1][1],info[1][2],info[1][3],info[1][4],info[1][5],info[1][6],info[1][7],info[1][8])

    def textChangeEvent(self):
        pass

    def addBond(self):
        print("add bond")
    
    def resetBond(self):
        print("add bond")
    
    def deleteBond(self):
        print("delete bond")

class SystemDefine(QToolBox):
    def __init__(self, parent=None) -> None:
        QToolBox.__init__(self,parent)

        self.latticeGUI = LatticePannel(self)
        self.orbitalGUI = OrbitalPannel(self)
        self.bondGUI = BondPannel(self)

        self.addItem(self.latticeGUI, 'Unit cell basis and supercell size')
        self.addItem(self.orbitalGUI, 'Orbital properties')
        self.addItem(self.bondGUI, 'Bond properties')

class Visualization(HasTraits):

    #def __init__(self,systemObj:SystemDefine=None):
    #    self.systemObj=systemObj
    systemObj:SystemDefine=None
    scene = Instance(MlabSceneModel, ())

    @on_trait_change('scene.activated')
    def initial_plot(self):
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.

        # We can do normal mlab calls on the embedded scene.
        #'''
        tb=wan.TBmodel()
        a1=self.systemObj.latticeGUI.a0GUI.report()
        a2=self.systemObj.latticeGUI.a1GUI.report()
        a3=self.systemObj.latticeGUI.a2GUI.report()
        tb.lattice=np.array([a1,a2,a3])
                         # pos            size  color  spin
        tb.orbital_coor=[[np.array(ele[3]),0.5,(1,0,0),(0,0,ele[2])] for ele in self.systemObj.orbitalGUI.OrbListGUI.infoData]
        tb.norbital=len(tb.orbital_coor)

        tb.hopping=[[bond_data[2][0],bond_data[2][1],np.array(bond_data[2][2]),bond_data[1][0],(0,1,0), 0.025] for bond_data in self.systemObj.bondGUI.BondListGUI.infoData]
        tb.nhoppings=len(tb.hopping)
        Lx, Ly, Lz=[min([x,4]) for x in self.systemObj.latticeGUI.supercellGui.report()]
        tb.make_supercell([Lx,0,0],[0,Ly,0],[0,0,Lz])

        #self.scene.mlab.options.backend = 'envisage'
        #self.scene.mlab.options.offscreen = True
        tb.viewStructure_maya(self.scene.mlab)
        #'''
        #self.test_quiver3d()

    # the layout of the dialog screated
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=500, width=600, show_label=False),
                resizable=True # We need this to resize with the parent widget
                )
    
    def update(self,lightOrb=-1,lightID=-1):
        time0=time.time()
        tb=wan.TBmodel()
        a1=self.systemObj.latticeGUI.a0GUI.report()
        a2=self.systemObj.latticeGUI.a1GUI.report()
        a3=self.systemObj.latticeGUI.a2GUI.report()
        tb.lattice=np.array([a1,a2,a3])
        tb.orbital_coor=[[np.array(ele[3]),0.7 if ele[0]==lightOrb else 0.5, (1,1,0) if ele[0]==lightOrb else (1,0,0), (0,0,ele[2])] for ele in self.systemObj.orbitalGUI.OrbListGUI.infoData]
        tb.norbital=len(tb.orbital_coor)
        tb.hopping=[[bond_data[2][0],bond_data[2][1],np.array(bond_data[2][2]),bond_data[1][0],(1,1,0) if bond_data[0]==lightID else (0,1,0), 0.05 if bond_data[0]==lightID else 0.025] for bond_data in self.systemObj.bondGUI.BondListGUI.infoData]
        tb.nhoppings=len(tb.hopping)
        Lx, Ly, Lz=[4 if x>1 else 1 for x in self.systemObj.latticeGUI.supercellGui.report()]
        tb.make_supercell([Lx,0,0],[0,Ly,0],[0,0,Lz])
        print("Prepare to display 3D model: %.3fs"%(time.time()-time0))
        time0=time.time()
        view=self.scene.mlab.view()
        roll=self.scene.mlab.roll()
        self.scene.mlab.clf()
        tb.viewStructure_maya(self.scene.mlab)
        self.scene.mlab.view(*view)
        self.scene.mlab.roll(roll)
        print("Draw 3D model: %.3fs"%(time.time()-time0))
    
class MayaviQWidget(QtGui.QWidget):
    def __init__(self, parent=None, systemObj:SystemDefine=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.visualization = Visualization()#systemObj)
        self.visualization.systemObj=systemObj

        # The edit_traits call will generate the widget to embed.
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)

class MainFrame(QWidget):

    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 2000, 1200)
        self.setWindowTitle('mcsolver v3.0')
        self.setWindowIcon(QIcon('./test_tube.ico'))

        self.system=SystemDefine(self)
        self.structureGUI = MayaviQWidget(self, self.system)

        self.system.orbitalGUI.setStructureVisualizer(self.structureGUI.visualization)
        self.system.bondGUI.setStructureVisualizer(self.structureGUI.visualization)

        grid = QGridLayout(self)
        grid.addWidget(self.system, 0, 0)
        grid.addWidget(self.structureGUI, 0, 1, 3, 1)

def loadEveryThing(submitFunc):
    app = QApplication(sys.argv)
    mainPannel=MainFrame()
    mainPannel.show()
    sys.exit(app.exec_())