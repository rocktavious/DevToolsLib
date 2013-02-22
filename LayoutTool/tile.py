from PyQt4.QtCore import Qt, QRectF, QPoint
from PyQt4.QtGui import QGraphicsItemGroup, QGraphicsItem, QColor, QBrush, QPolygon

from DTL.db.base import BaseData
from DTL.db.properties import IntegerProperty, BooleanProperty


class Tile(BaseData):
    active = BooleanProperty(default=False)
    x = IntegerProperty(default=0)
    y = IntegerProperty(default=0)
    z = IntegerProperty(default=0)
    
    def __init__(self, x=0, y=0, z=0, active=False, **kw):
        super(Tile, self).__init__(**kw)
        self.x = x
        self.y = y
        self.z = z
        self.active = active
        
class Shapes(object):
    Square = [QPoint(0,0),
              QPoint(0,30),
              QPoint(30,30),
              QPoint(30,0)]
    Square_North_Wall = [0,0,
                         0,2,
                         30,2,
                         30,0,
                         0,0]
    Square_South_Wall = [0,28,
                         0,30,
                         30,30,
                         30,28,
                         0,28]
    Square_East_Wall = [28,0,
                        28,30,
                        30,30,
                        30,0,
                        28,0]
    Square_West_Wall = [0,0,
                        0,30,
                        2,30,
                        2,0,
                        0,0]

        
class ClickableGraphic(QGraphicsItem):
    inactive_color = QColor(100,100,100)
    active_color = QColor(190,210,250)
    selected_color = QColor(100,250,100)
    def __init__(self, points, active):
        super(ClickableGraphic, self).__init__()
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsFocusable)
        
        self.rect = QRectF(0,0,10,10)
        self.points = QPolygon(points)
        self.brush = QBrush()
        self.brush.setColor(self.inactive_color)
        self.brush.setStyle(Qt.SolidPattern)
        self.setVisible(True)        
        self.setZValue(1)
        self.active = active
    
    def boundingRect(self):
        return self.rect
    
    def paint(self, painter, option, widget):
        if self.active :
            self.brush.setColor(self.active_color)
        else:
            self.brush.setColor(self.inactive_color)
        if self.isSelected() or self.hasFocus():
            self.setOpacity(1)
            self.brush.setColor(self.selected_color)        
        painter.setBrush(self.brush)
        painter.drawPolygon(self.points)
        
    def setActive(self, new_value):
        self.active = new_value
        self.update()



class WallGraphic(ClickableGraphic):
    def __init__(self, *a):
        super(WallGraphic, self).__init__(*a)
    
    def paint(self, painter, option, widget):
        if self.active :
            self.setOpacity(0.01)
        else:
            self.setOpacity(1)
            
        super(WallGraphic, self).paint(painter, option, widget)

    
class SquareTile(QGraphicsItemGroup):
    tile_size = 30
    def __init__(self, x, y, active):
        super(SquareTile, self).__init__()
        x = (x * self.tile_size)
        y = (y * self.tile_size)
        
        
        self.tile = ClickableGraphic(Shapes.Square, active)
        setattr(self.tile, 'isTile', True)
        self.tile.setPos(x , y )
        self.addToGroup(self.tile)
        
        
        #Walls
        self.north_wall = WallGraphic(Shapes.Square_North_Wall, active)
        self.north_wall.setPos(x, y)
        #self.addToGroup(self.north_wall)
        
        self.south_wall = WallGraphic(Shapes.Square_South_Wall, active)
        self.south_wall.setPos(x, y + 28)
        #self.addToGroup(self.south_wall)
        
        self.east_wall = WallGraphic(Shapes.Square_East_Wall, active)
        self.east_wall.setPos(x + 28, y)
        #self.addToGroup(self.east_wall)
        
        self.west_wall = WallGraphic(Shapes.Square_West_Wall, active)
        self.west_wall.setPos(x, y)
        #self.addToGroup(self.west_wall)
        
    def show_walls(self, value):
        if value :
            self.north_wall.setVisible(True)
            self.south_wall.setVisible(True)
            self.east_wall.setVisible(True)
            self.west_wall.setVisible(True)
        else:
            self.north_wall.setVisible(False)
            self.south_wall.setVisible(False)
            self.east_wall.setVisible(False)
            self.west_wall.setVisible(False)
        

    
        


