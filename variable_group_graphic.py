from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.Qt import *

colors = [Qt.red, Qt.green, Qt.blue, Qt.cyan, Qt.magenta, Qt.yellow, Qt.gray,
          Qt.darkRed, Qt.darkGreen, Qt.darkBlue, Qt.darkCyan, Qt.darkMagenta, Qt.darkYellow, Qt.darkGray, Qt.white, Qt.black]

class VariableGroupGraphic(QtGui.QWidget):
    # column_coordinates is a list of x-coordinates of middles of columns belonging to a particular variable group
    # so it is a list of lists
    def __init__(self, column_coordinates=[], penwidth=4, spacing=3, height = 5, parent=None):
        super(VariableGroupGraphic, self).__init__(parent)
    
        self.penwidth = penwidth
        self.column_coordinates = column_coordinates
        self.spacing=spacing
        self.height = height
        
    def set_column_coordinates(self, new_column_coordinates):
        self.column_coordinates = self.redistribute_coords(new_column_coordinates)
        self.adjustSize()
        self.update()
    
    def paintEvent(self, event=None):
        painter = QPainter(self)

        start = 0
        x_coords_index = 0
        for i, x_coords in enumerate(self.column_coordinates):
            pen = QPen(colors[i%len(colors)])
            pen.setWidth(self.penwidth)
            painter.setPen(pen)
            offset = start + self.height
            for xcor in x_coords:
                painter.drawLine(xcor,0, xcor, offset) # vertical lines
            painter.drawLine(min(x_coords), offset, max(x_coords), offset)
             
            start += self.spacing
    
    def redistribute_coords(self, column_coordinates):
        coordinates_together = []
        for coord_set in column_coordinates:
            coordinates_together.extend(coord_set)
            
        # count overlapping coordinates
        count_each = {}
        for x in coordinates_together:
            try:
                count_each[x]+=1
            except KeyError:
                count_each[x]=1
        
        available_coords = {}
        for x, count in count_each.items():
            if count == 1:
                continue
            available_coords[x]=self.distributed_coords(x, count)
    
        new_column_coordinates = []
        for cord_set in column_coordinates:
            new_cord_set = []
            for x in cord_set:
                if count_each[x]==1:
                    new_cord_set.append(x)
                else:
                    new_x = available_coords[x][0]
                    new_cord_set.append(new_x)
                    available_coords[x] = available_coords[x][1:]
            new_column_coordinates.append(new_cord_set)
        return new_column_coordinates
                
    
    def distributed_coords(self, x, n):
        # x is the x-coordinate, n is number of overlaps
        # returns new list of xcoordinates close to x but not overlapping
        n_even = n%2 == 0
        if not n_even:
            new_range = range(x-n/2, x+n/2+1)
        else:
            new_range = range(x+1-n/2, x+1+n/2+1)
            new_range.remove(x)
        
        shift = self.penwidth*(len(new_range)-1)/2+2
        def adjust(num):
            if num == x:
                return x
            if num > x:
                return num+(num-x)*shift
            else:
                return num-(x-num)*shift
        new_range = [adjust(num) for num in new_range]
        
        return new_range
        
    
    def sizeHint(self):
        n = len(self.column_coordinates)
        height_hint = self.height*n + self.spacing*(n-1) if n>0 else 1
        return QtCore.QSize(4000, height_hint)
    
    def minimumSizeHint(self):    
        size = self.sizeHint()
        size.setWidth(200)
        return size

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    render_area = VariableGroupGraphic([[10,40,60],[13,50,65,70]])
    #render_area = VariableGroupGraphic()
    render_area.show()
    sys.exit(app.exec_())
