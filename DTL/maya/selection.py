import maya.cmds as cmds

from DTL.api import Enum, apiUtils, BaseStruct

SelectionTypes = Enum("Vertex","Edge","Face","UV","VertexFace","Polygon","Object")

#--------------------------------------------------------
#--------------------------------------------------------
class ObjSelData(BaseStruct, dict):
    _compPrefixes = {SelectionTypes.Vertex:'vtx',
                     SelectionTypes.Edge:'e',
                     SelectionTypes.Face:'f',
                     SelectionTypes.UV:'map',
                     SelectionTypes.VertexFace:'vtxFace'}
    
    _filterExpandMap = {SelectionTypes.Vertex:31,
                        SelectionTypes.Edge:32,
                        SelectionTypes.Face:34,
                        SelectionTypes.UV:35,
                        SelectionTypes.VertexFace:70,
                        SelectionTypes.Polygon:12}
    
    #--------------------------------------------------------
    def __init__(self, obj, hilite=False, compData={}, vtxFaceColorData={}):
        super(ObjSelData, self).__init__()
        apiUtils.synthesize(self, 'object', obj)
        apiUtils.synthesize(self, 'hilite', hilite)
        apiUtils.synthesize(self, 'vtxFaceColorData', vtxFaceColorData)
        
        #For each type of component add list var for it
        for compPrefix in ObjSelData._compPrefixes.values():
            self.__setitem__(compPrefix, [])
        
        if compData:
            self._set_data(data_dict=compData)
            
    #------------------------------------------------------------
    def _set_data(self, data_dict):
        for key, value in data_dict.items():
            self.__setitem__(key, value)
    
    #------------------------------------------------------------
    def __get(self):
        return (self.object(),
                self.hilite(),
                super(dict, self).__repr__(),
                self.vtxFaceColorData())
    
    #--------------------------------------------------------
    def populateSubSelection(self):
        '''Populates the class with the objects component selection'''
        self._getSelectedComp(SelectionTypes.Vertex)
        self._getSelectedComp(SelectionTypes.Edge)
        self._getSelectedComp(SelectionTypes.Face)
        self._getSelectedComp(SelectionTypes.UV)
        self._getSelectedComp(SelectionTypes.VertexFace)
    
    #--------------------------------------------------------
    def _populateVertColorData(self):
        '''Populates a dictionary of color/alpha key -> vtxFace list'''
        rgbaDict = dict()
        if cmds.listRelatives(self.object(),s=1) :
            for vtxFace in self.getVtxFaceList() :
                try:
                    colorList = cmds.polyColorPerVertex(vtxFace,q=1,rgb=1)
                except:
                    cmds.polyColorPerVertex(self.object(),rgb=[0,0,0],a=1)
                    colorList = cmds.polyColorPerVertex(vtxFace,q=1,rgb=1)
                alpha = cmds.polyColorPerVertex(vtxFace,q=1,a=1)
                rgba = (colorList[0],colorList[1],colorList[2],alpha[0])
                if rgba not in rgbaDict :
                    rgbaDict[rgba] = []
                rgbaDict[rgba].append(vtxFace)
        self.setVtxFaceColorData(rgbaDict)

    #--------------------------------------------------------
    def _getSelectedComp(self, selType):
        '''Populates a dictionary of selected components of the given type'''
        compType = ObjSelData._filterExpandMap[selType]
        compPrefix = ObjSelData._compPrefixes[selType]
        selectedComp = cmds.filterExpand(ex=1,fp=1,sm=compType)
        if selectedComp is None:
            return
        for comp in selectedComp :
            compNum = comp.split('[')[-1].split(']')[0]
            self.__getitem__(compPrefix).append(compNum)
            

    #--------------------------------------------------------
    def getDescendents(self, obj=None):
        '''Return a list of all of the objects descendents(without shape nodes)'''
        allChilden = set(cmds.listRelatives(self.object(), ad=1, f=1) or [])
        allShapes = set()
        for item in allChilden:
            allShapes.update(cmds.listRelatives(item, s=1, f=1) or [])
        
        return list(allChilden - allShapes)
            
    #--------------------------------------------------------
    def getVtxFaceList(self):
        '''Returns the objects vtxFace list'''
        return list(cmds.ls(cmds.polyListComponentConversion(self.object(),tvf=1),l=1,fl=1))
            

#------------------------------------------------------------
#------------------------------------------------------------
class Selection(dict):
    '''Custom Class to handle selection data as well as helper commands to use/parse the selection data'''
    #--------------------------------------------------------
    def __init__(self):
        super(Selection, self).__init__()

    #--------------------------------------------------------
    def getSelection(self):
        self = Selection()
        #Handle Object Selection
        for item in cmds.ls(sl=1,tr=1,l=1):
            self.__setitem__(item,ObjSelData(item))
        
        #Handle Component Selection
        for item in cmds.ls(hl=1,l=1):
            self.__setitem__(item,ObjSelData(item, hilite=True))
            
    def __repr__(self):
            return 'Selection({0})'.format(super(Selection, self).__repr__())

    #--------------------------------------------------------
    def select(self,obj,compType,clearSel=1,addVal=0):
        '''Allow easy reselection of specific selection data'''
        cmds.select(cl=clearSel)
        if self[obj][compType] != None :
            cmds.hilite(obj)
            cmds.select(self[obj][compType],add=addVal)

    #--------------------------------------------------------
    def restoreSelection(self):
        '''Restores the selection back to how it was when the class populated its selection data'''
        cmds.select(cl=1)
        for obj in self.keys():
            cmds.select(obj,add=1)
            self.select(obj, 0, 0, addVal=1)
            self.select(obj, 1, 0, addVal=1)
            self.select(obj, 2, 0, addVal=1)
            self.select(obj, 3, 0, addVal=1)

    #--------------------------------------------------------
    def getFirstMesh(self):
        '''Returns the first mesh it finds in the selection list'''
        for item in self.keys() :
            if cmds.listRelatives(item,s=1) :
                return item

    #--------------------------------------------------------
    def getCompList(self,obj,compIndex=0):
        compList = []
        if self[obj][compIndex] == None : #Return all
            return cmds.ls(obj + "." + self.compPrefixes[compIndex] + '[*]',l=1,fl=1)
        else:
            return self[obj][compIndex]

    #--------------------------------------------------------
    def getCompIndex(self,obj,compIndex=0):
        indexList = []
        if self[obj][compIndex] :
            for comp in self[obj][compIndex] :
                compNum = comp.split('[')[-1].split(']')[0]
                indexList.append(compNum)
        return indexList

    #--------------------------------------------------------
    def getInverseCompIndex(self,obj,compIndex=0):
        indexList = []
        fullCompList = []
        if self[obj][compIndex] :
            fullCompList = cmds.ls(obj + "." + self.compPrefixes[compIndex] + '[*]',l=1,fl=1)
            selCompList = cmds.ls(self[obj][compIndex],l=1,fl=1)
            for comp in [comp for comp in fullCompList if comp not in selCompList ] :
                compNum = comp.split('[')[-1].split(']')[0]
                indexList.append(compNum)

        return indexList