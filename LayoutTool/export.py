import uuid
from xml.etree import ElementTree as xml
from xml.dom.minidom import parseString

WIDTH_UNIT = 4.8
WALL_ADJUST = 2.4
HEIGHT_UNIT = 5.38

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = xml.tostring(elem, 'utf-8')
    reparsed = parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def generate_guid():
    return '{' + str(uuid.UUID(bytes=uuid.uuid4().bytes)).upper() + '}'

def save_doc(doc, filepath):
    print prettify(doc)
    with open(filepath, 'w') as file_spec :
        file_spec.write(prettify(doc))

def read_doc():
    doc = xml.Element('PrefabsLibrary')
    doc.set('Name','Hanger')
    return doc

def create_prefab(doc, prefab_name):
    prefab = xml.SubElement(doc, 'Prefab')
    print "prefab_name", prefab_name
    prefab.set('Name', prefab_name)
    prefab.set('Id',generate_guid())
    prefab.set('Library', doc.get('Name'))
    xml.SubElement(prefab,'Objects')
    return prefab

def convert_map(model):
    #Request Doc
    #Read Doc or create new one
    doc = read_doc()
    new_prefab = create_prefab(doc, model.Name)
    for layer in model.Layers :
        convert_layer(new_prefab, layer)
        
    return doc
    
def convert_layer(prefab, layer):
    objects = prefab.find('Objects')
    for tile in layer.Tiles :
        if tile.active :
            new_object = generate_new_object(objects)
            #Custom
            tile_name = str(tile.x) + '_' + str(tile.y)
            new_object.set('Name', tile_name)
            tile_pos = (tile.x * -WIDTH_UNIT,
                        tile.x * WIDTH_UNIT,
                        layer.Index * -HEIGHT_UNIT)
            new_object.set('Pos',str(tile_pos[0]) + ',' + str(tile_pos[1]) + ',' + str(tile_pos[2]))
            new_object.set('Rotate','1,0,0,0')
            new_object.set('Material','Materials/dev/512x_grey')
            new_object.set('Geometry','objects/Modules/Floors/01A.cgf')
            
            generate_ceiling(layer, tile, tile_name, tile_pos, objects)
            generate_walls(layer, tile, tile_name, tile_pos, objects)
            
def generate_new_object(objects):
    new_object = xml.SubElement(objects,'Object')
    
    #Generic
    new_object.set('Id',generate_guid())
    new_object.set('CastShadow','1')
    new_object.set('Type','GeomEntity')
    new_object.set('EntityClass','GeomEntity')  
    
    return new_object
            
def generate_ceiling(layer, tile, tile_name, tile_pos, objects):
    new_object = generate_new_object(objects)
    #Custom
    new_object.set('Name', tile_name + '_ceiling')
    new_object.set('Pos',str(tile_pos[0]) + ',' + str(tile_pos[1]) + ',' + str(tile_pos[2] + HEIGHT_UNIT))
    new_object.set('Rotate','1,0,0,0')
    new_object.set('Material','Materials/dev/512x_grey')
    new_object.set('Geometry','objects/Modules/Ceiling/01A.cgf')
      
    
            
def make_wall(objects):
    new_object = generate_new_object(objects)
    #Custom
    new_object.set('Material','Materials/dev/512x_grey')
    new_object.set('Geometry','objects/Modules/Walls/02A.cgf')
    
    return new_object
            
def generate_walls(layer, tile, tile_name, tile_pos, objects):
    north = (tile.x, tile.y - 1)
    north_name = tile_name + '_north'
    north_pos = (tile_pos[0], tile_pos[1] - WALL_ADJUST, tile_pos[2])
    north_rotate = '0,0,0,1'
    south = (tile.x, tile.y + 1)
    south_name = tile_name + '_south'
    south_pos = (tile_pos[0], tile_pos[1] + WALL_ADJUST, tile_pos[2])
    south_rotate = '1,0,0,0'
    
    #East and West Position data is reveresed
    east = (tile.x - 1, tile.y)
    east_name = tile_name + '_east'
    east_pos = (tile_pos[0] + WALL_ADJUST, tile_pos[1], tile_pos[2])
    east_rotate = '0.707106,0,0,-0.707106'    
    west = (tile.x + 1, tile.y)
    west_name = tile_name + '_west'
    west_pos = (tile_pos[0] - WALL_ADJUST, tile_pos[1], tile_pos[2])
    west_rotate = '0.707106,0,0,0.707106'    
    
    #North
    tile = layer.get_tile(*north)
    if tile :
        if not tile.active :
            new_wall = make_wall(objects)
            new_wall.set('Name',north_name)
            new_wall.set('Pos',str(north_pos[0]) + ',' + str(north_pos[1]) + ',' + str(north_pos[2]))
            new_wall.set('Rotate',north_rotate)            
    else:
        new_wall = make_wall(objects)
        new_wall.set('Name',north_name)
        new_wall.set('Pos',str(north_pos[0]) + ',' + str(north_pos[1]) + ',' + str(north_pos[2]))
        new_wall.set('Rotate',north_rotate)
        
        
    #South
    tile = layer.get_tile(*south)
    if tile :
        if not tile.active:
            new_wall = make_wall(objects)
            new_wall.set('Name',south_name)
            new_wall.set('Pos',str(south_pos[0]) + ',' + str(south_pos[1]) + ',' + str(south_pos[2]))
            new_wall.set('Rotate',south_rotate)        
    else:
        new_wall = make_wall(objects)
        new_wall.set('Name',south_name)
        new_wall.set('Pos',str(south_pos[0]) + ',' + str(south_pos[1]) + ',' + str(south_pos[2]))
        new_wall.set('Rotate',south_rotate)
        
        
    #East
    tile = layer.get_tile(*east)
    if tile :
        if not tile.active:
            new_wall = make_wall(objects)
            new_wall.set('Name',east_name)
            new_wall.set('Pos',str(east_pos[0]) + ',' + str(east_pos[1]) + ',' + str(east_pos[2]))
            new_wall.set('Rotate',east_rotate)        
    else:
        new_wall = make_wall(objects)
        new_wall.set('Name',east_name)
        new_wall.set('Pos',str(east_pos[0]) + ',' + str(east_pos[1]) + ',' + str(east_pos[2]))
        new_wall.set('Rotate',east_rotate)
        
        
    #West
    tile = layer.get_tile(*west)
    if tile :
        if not tile.active:
            new_wall = make_wall(objects)
            new_wall.set('Name',west_name)
            new_wall.set('Pos',str(west_pos[0]) + ',' + str(west_pos[1]) + ',' + str(west_pos[2]))
            new_wall.set('Rotate',west_rotate)        
    else:
        new_wall = make_wall(objects)
        new_wall.set('Name',west_name)
        new_wall.set('Pos',str(west_pos[0]) + ',' + str(west_pos[1]) + ',' + str(west_pos[2]))
        new_wall.set('Rotate',west_rotate)
        
        

            




