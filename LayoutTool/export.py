import os
import uuid
from xml.etree import ElementTree as xml
from xml.dom import Node
from xml.dom.minidom import parseString

from DTL.api import XmlDocument, Utils

WIDTH_UNIT = 4.8
WALL_ADJUST = 2.4
HEIGHT_UNIT = 5.38

#------------------------------------------------------------
#------------------------------------------------------------
#Start Export Utils
#------------------------------------------------------------
#------------------------------------------------------------
def generate_guid():
    return '{' + str(uuid.UUID(bytes=uuid.uuid4().bytes)).upper() + '}'

#------------------------------------------------------------
def add_prefab(xmlnode, new_prefab):
    #Validate Unique else remove existing
    prefabList = xmlnode.get('Prefab',[])
    if not isinstance(prefabList, list):
        prefabList = [prefabList]
    for prefab in prefabList:
        if prefab.get('@Name','') == new_prefab['@Name'] :
            prefabList.remove(prefab)
    
    
    prefabList.append(new_prefab)
    xmlnode['Prefab'] = prefabList
    
#------------------------------------------------------------
def generate_entity_link(entityLinksList, name, targetId=None):
    if targetId is None :
        return
    entityLinksList.append({'@TargetId':str(targetId),
                            '@Name':name,
                            '@RelPos':'0,0,0',
                            '@RelRot':'1,0,0,0'})

#------------------------------------------------------------
def generate_section_entity(pos, location, parentId=None):
    data = {'@Id':generate_guid(),
            '@CastShadow':'0',
            '@Type':'Entity',
            '@HiddenInGame':'1',
            '@Name':location,
            '@Pos':pos,
            '@Rotate':'1,0,0,0',
            '@ViewDistRatio':"255",
            '@EntityClass':'HangerSectionEntity',
            'Properties':{'@bShowFloor':'1',
                          '@bShowCeiling':'1',
                          '@bShowNorthWall':'1',
                          '@bShowSouthWall':'1',
                          '@bShowEastWall':'1',
                          '@bShowWestWall':'1'},
            'EntityLinks':{'Link':[]}
            }
    if parentId :
        data['@Parent'] = str(parentId)
    
    return data

#------------------------------------------------------------
def generate_section_root(objects):
    output = {}
    
    new_section_root = generate_section_entity("0.0,0.0,0.0", "Root")
    objects.append(new_section_root)
    output["Root"] = new_section_root
    
    data = [("0.0,0.0,-3.0","Floor"),
            ("0.0,0.0,2.38", "Ceiling"),
            ("0.0,-2.4,0.0", "North"),
            ("0.0,2.4,0.0", "South"),
            ("-2.4,0.0,0.0", "East"),
            ("2.4,0.0,0.0", "West")]
    
    
    for item in data :
        new_section_entity = generate_section_entity(item[0], item[1], new_section_root['@Id'])
        output[item[1]] = new_section_entity
        generate_entity_link(new_section_root['EntityLinks']['Link'], item[1], new_section_entity.get('@Id',None))
        objects.append(new_section_entity)
    
    return output

#------------------------------------------------------------
def generate_new_object():
    data = {'@Id':generate_guid(),
            '@CastShadow':'1',
            '@Type':'GeomEntity',
            '@EntityClass':'GeomEntity',
            '@Scale':'1,1,1',
            '@ViewDistRatio':"255"}  
    
    return data

#------------------------------------------------------------
def generate_floor(layer, tile, tile_name, tile_pos, prefabObjects, hangerSectionEntityMap):
    floor = (tile.x, tile.y,1)
    floor_name = tile_name + '_floor'
    floor_pos = (tile_pos[0], tile_pos[1], tile_pos[2])
    floor_rotate = '1,0,0,0'    
    #floor
    tile = layer.get_tile(*floor)
    if tile is None:
        new_object = generate_new_object()
        new_object.update({'@Name':floor_name,
                           '@Pos':str(floor_pos[0]) + ',' + str(floor_pos[1]) + ',' + str(floor_pos[2]),
                           '@Rotate':floor_rotate,
                           '@Parent':hangerSectionEntityMap['Root'].get('@Id',None),
                           '@Material':'Materials/dev/512x_grey',
                           '@Geometry':'objects/Modules/Floors/01A.cgf'})
        generate_entity_link(hangerSectionEntityMap['Floor']['EntityLinks']['Link'],
                             new_object.get('@Name','UNDEFINED'),
                             new_object.get('@Id',None))
        prefabObjects.append(new_object)

#------------------------------------------------------------
def generate_ceiling(layer, tile, tile_name, tile_pos, prefabObjects, hangerSectionEntityMap):
    ceiling = (tile.x, tile.y,-1)
    ceiling_name = tile_name + '_ceiling'
    ceiling_pos = (tile_pos[0], tile_pos[1], tile_pos[2] + HEIGHT_UNIT)
    ceiling_rotate = '1,0,0,0'    
    #Ceiling
    tile = layer.get_tile(*ceiling)
    if tile is None:    
        new_object = generate_new_object()
        new_object.update({'@Name':ceiling_name,
                           '@Pos':str(ceiling_pos[0]) + ',' + str(ceiling_pos[1]) + ',' + str(ceiling_pos[2]),
                           '@Rotate':ceiling_rotate,
                           '@Parent':hangerSectionEntityMap['Root'].get('@Id',None),
                           '@Material':'Materials/dev/512x_grey',
                           '@Geometry':'objects/Modules/Ceiling/01A.cgf'})
        generate_entity_link(hangerSectionEntityMap['Ceiling']['EntityLinks']['Link'],
                             new_object.get('@Name','UNDEFINED'),
                             new_object.get('@Id',None))
        prefabObjects.append(new_object) 

#------------------------------------------------------------
def generate_walls(layer, tile, tile_name, tile_pos, prefabObjects, hangerSectionEntityMap):
    north = (tile.x, tile.y - 1)
    north_name = tile_name + '_north'
    north_pos = (tile_pos[0], tile_pos[1] - WALL_ADJUST, tile_pos[2])
    north_rotate = '0,0,0,1'
    south = (tile.x, tile.y + 1)
    south_name = tile_name + '_south'
    south_pos = (tile_pos[0], tile_pos[1] + WALL_ADJUST, tile_pos[2])
    south_rotate = '1,0,0,0'
    
    east = (tile.x + 1, tile.y)
    east_name = tile_name + '_east'
    east_pos = (tile_pos[0] - WALL_ADJUST, tile_pos[1], tile_pos[2])
    east_rotate = '0.707106,0,0,0.707106'    
    west = (tile.x - 1, tile.y)
    west_name = tile_name + '_west'
    west_pos = (tile_pos[0] + WALL_ADJUST, tile_pos[1], tile_pos[2])
    west_rotate = '0.707106,0,0,-0.707106'    
    
    #North
    tile = layer.get_tile(*north)
    if tile is None :
        new_wall = generate_new_object()
        new_wall.update({'@Material':'Materials/dev/512x_grey',
                         '@Geometry':'objects/Modules/Walls/01A.cgf',
                         '@Name':north_name,
                         '@Pos':str(north_pos[0]) + ',' + str(north_pos[1]) + ',' + str(north_pos[2]),
                         '@Rotate':north_rotate,
                         '@Parent':hangerSectionEntityMap['Root'].get('@Id',None)})
        generate_entity_link(hangerSectionEntityMap['North']['EntityLinks']['Link'],
                             new_wall.get('@Name','UNDEFINED'),
                             new_wall.get('@Id',None))
        prefabObjects.append(new_wall)        
        
        
    #South
    tile = layer.get_tile(*south)
    if tile is None:
        new_wall = generate_new_object()
        new_wall.update({'@Material':'Materials/dev/512x_grey',
                         '@Geometry':'objects/Modules/Walls/01A.cgf',
                         '@Name':south_name,
                         '@Pos':str(south_pos[0]) + ',' + str(south_pos[1]) + ',' + str(south_pos[2]),
                         '@Rotate':south_rotate,
                         '@Parent':hangerSectionEntityMap['Root'].get('@Id',None)})
        generate_entity_link(hangerSectionEntityMap['South']['EntityLinks']['Link'],
                             new_wall.get('@Name','UNDEFINED'),
                             new_wall.get('@Id',None))
        prefabObjects.append(new_wall)   
        
        
    #East
    tile = layer.get_tile(*east)
    if tile is None:
        new_wall = generate_new_object()
        new_wall.update({'@Material':'Materials/dev/512x_grey',
                         '@Geometry':'objects/Modules/Walls/01A.cgf',
                         '@Name':east_name,
                         '@Pos':str(east_pos[0]) + ',' + str(east_pos[1]) + ',' + str(east_pos[2]),
                         '@Rotate':east_rotate,
                         '@Parent':hangerSectionEntityMap['Root'].get('@Id',None)})
        generate_entity_link(hangerSectionEntityMap['East']['EntityLinks']['Link'],
                             new_wall.get('@Name','UNDEFINED'),
                             new_wall.get('@Id',None))
        prefabObjects.append(new_wall)
        
        
    #West
    tile = layer.get_tile(*west)
    if tile is None:
        new_wall = generate_new_object()
        new_wall.update({'@Material':'Materials/dev/512x_grey',
                         '@Geometry':'objects/Modules/Walls/01A.cgf',
                         '@Name':west_name,
                         '@Pos':str(west_pos[0]) + ',' + str(west_pos[1]) + ',' + str(west_pos[2]),
                         '@Rotate':west_rotate,
                         '@Parent':hangerSectionEntityMap['Root'].get('@Id',None)})
        generate_entity_link(hangerSectionEntityMap['West']['EntityLinks']['Link'],
                             new_wall.get('@Name','UNDEFINED'),
                             new_wall.get('@Id',None))
        prefabObjects.append(new_wall)
        

#------------------------------------------------------------
#------------------------------------------------------------
#Begin Real Work
#------------------------------------------------------------
#------------------------------------------------------------
def exportMap(model, filepath):
    xmldoc = XmlDocument(filepath)
    if not xmldoc.get('PrefabsLibrary', None):
        text, success = Utils.getUserInput('Enter new prefab library name:')
        if success:
            xmldoc['PrefabsLibrary'] = {'@Name',text}
        else:
            xmldoc['PrefabsLibrary'] = {'@Name','Default'}
            
    #Get the Root Node
    prefabLibNode = xmldoc['PrefabsLibrary']
    
    #Add a new prefab
    prefab_name = prefabLibNode.get('@Name','') + '.' + model.name
    new_prefab = {'@Name':prefab_name,
                  '@Id':generate_guid(),
                  '@Library':prefabLibNode.get('@Name',''),
                  'Objects':{'Object':[]}}
    add_prefab(prefabLibNode, new_prefab)
    
    prefabObjects = new_prefab['Objects']['Object']
    
    #Generate the Section Entity
    hangerSectionEntityMap = generate_section_root(prefabObjects)
    
    #Handle the models layers
    for layer in model.children() :    
        for tile in layer.children() :
            tile_name = str(tile.x) + '_' + str(tile.y)
            tile_pos = (tile.x * -WIDTH_UNIT,
                        tile.y * WIDTH_UNIT,
                        layer.index * -HEIGHT_UNIT)
            generate_floor(layer, tile, tile_name, tile_pos, prefabObjects, hangerSectionEntityMap)
            generate_ceiling(layer, tile, tile_name, tile_pos, prefabObjects, hangerSectionEntityMap)
            generate_walls(layer, tile, tile_name, tile_pos, prefabObjects, hangerSectionEntityMap)
    
    #Finally...Save the XML file
    xmldoc.save()
