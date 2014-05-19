#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: svg.py

from main import helper
from math import pi, sin, cos

def svg(*args, **kw):
    """
    Use in this way:
    
    ´from tagtor import helper as h, svg´
    
    """
    class svg(type(helper.svg())):
        # cartesian grid on/off
        grid = False
        # azes on/off
        axes = False
        # show origin
        origin = False
        # grid aspects
        grid_aspects = (8, 4)
        # size of the svg canvas, width and height
        size = (400, 400)
        # origin x preset, svg 0 is on left up corner
        x = 200
        # origin y preset, svg 0 is on left up corner
        y = 200
        # elements
        elements = []
        
        def __init__(self, *args, **kw):
            super(self.__class__, self).__init__(*args, **kw)
            self.grid_id = "gid%s" % id(self)
            self.grid_item_id = "gitem%s" % id(self)
            width = kw['width'] if kw.has_key('width') else self.x*2
            height = kw['height'] if kw.has_key('height') else self.y*2
            self.set_size(width, height)
        
        def set_grid(self, grid = True):
            self.grid = grid
            return self
        
        def set_axes(self, axes = True):
            self.axes = axes
            return self
        
        def set_origin(self, origin = True):
            self.origin = origin
            return self
        
        def set_size(self, width, height):
            self.x = width/2
            self.y = height/2
            self.size = (width, height)
            self.setAttribute('width', width)
            self.setAttribute('height', height)
            self.setAttribute('viewbox', "0 0 %s %s" % (width+1, height+1))
            return self
        
        def set_text(self, *args, **kw):
            kw['x'] = self.x+kw['x'] if kw.has_key('x') else self.x 
            kw['y'] = self.y-kw['y'] if kw.has_key('y') else self.y
            self.elements.append(helper.text(*args, **kw))
            return self
        
        def set_rectangle(self, *args, **kw):
            kw['x'] = self.x+kw['x'] if kw.has_key('x') else self.x
            kw['y'] = self.y-kw['y'] if kw.has_key('y') else self.y
            self.elements.append(helper.rect(*args, **kw))
            return self
        
        def set_group(self, *args, **kw):
            self.elements.append(helper.g(*args, **kw))
            return self
        
        def set_defs(self, *args, **kw):
            self.elements.append(helper.defs(*args, **kw))
            return self
        
        def set_line(self, *args, **kw):
            kw['x1'] = self.x+kw['x1'] if kw.has_key('x1') else self.x
            kw['y1'] = self.y-kw['y1'] if kw.has_key('y1') else self.y
            kw['x2'] = self.x+kw['x2'] if kw.has_key('x2') else self.x + 10
            kw['y2'] = self.y-kw['y2'] if kw.has_key('y2') else self.y + 10
            self.elements.append(helper.line(*args, **kw))
            return self
        
        def set_circle(self, *args, **kw):
            kw['cx'] = self.x+kw['cx'] if kw.has_key('cx') else self.x
            kw['cy'] = self.y-kw['cy'] if kw.has_key('cy') else self.y
            self.elements.append(helper.circle(*args, **kw))
            return self
        
        def set_triangle(self, *args, **kw):
            kw['sides'] = 3
            return self.set_polygon(*args, **kw)
        
        def set_square(self, *args, **kw):
            kw['sides'] = 4
            return self.set_polygon(*args, **kw)
        
        def set_pentagon(self, *args, **kw):
            kw['sides'] = 5
            return self.set_polygon(*args, **kw)
        
        def set_hexagon(self, *args, **kw):
            kw['sides'] = 6
            return self.set_polygon(*args, **kw)
        
        def set_polygon(self, *args, **kw):
            # set default properties for vertex
            kw['cx'] = kw['cx']+self.x if kw.has_key('cx') else self.x
            kw['cy'] = kw['cy']-self.y if kw.has_key('cy') else self.y
            kw['radius'] = kw['radius'] if kw.has_key('radius') else 1
            kw['sides'] = kw['sides'] if kw.has_key('sides') else 4
            kw['degrees'] = kw['degrees'] if kw.has_key('degrees') else 0
            # set generate polygon points
            points = self.polygon_points(self.vertex(cx=kw['cx'],
                                                     cy=kw['cy'],
                                                     radius=kw['radius'],
                                                     sides=kw['sides'],
                                                     degrees=kw['degrees']))
            # delete default properties
            del kw['cx']
            del kw['cy']
            del kw['radius']
            del kw['sides']
            del kw['degrees']
            # create polygon with given points and keywords
            self.elements.append(helper.polygon(points=points, *args, **kw))
            return self
        
        def polygon_points(self, vertex):
            return ' '.join(['%s,%s' % (point[0], point[1]) for point in vertex])
        
        def vertex(self, cx = 0, cy = 0, sides = 4, radius = 1, degrees = 0):
            centerAng = 2*pi/sides
            startAng = pi*degrees/180
            points = []
            for i in range(0, sides):
                ang = startAng + (i*centerAng);
                x = round(cx + radius*cos(ang), 2)
                y = round(cy - radius*sin(ang), 2)
                points.append([x,y])
            return points
        
        def _set_grid(self):
            """ Set up background grid for drawing canvas """
            grid_sizex = self.size[0]/self.grid_aspects[0]
            grid_sizey = self.size[1]/self.grid_aspects[0]
            
            sizex = grid_sizex*(1.0/self.grid_aspects[1])
            sizey = grid_sizey*(1.0/self.grid_aspects[1])
            
            defs = helper.defs()
            defs << helper.pattern(helper.path(**{'d': 'M %s 0 L 0 0 0 %s' % (sizex, sizey), 'fill': 'none', 'stroke': 'gray', 'stroke-width': 0.5}),
                                   **{'id': self.grid_item_id, 'width': sizex, 'height': sizey, 'patternUnits': 'userSpaceOnUse'})
            defs << helper.pattern(helper.path(**{'d': 'M %s 0 L 0 0 0 %s' % (grid_sizex, grid_sizey), 'fill': 'none', 'stroke': 'gray', 'stroke-width': 1}),
                                   helper.rect(width=grid_sizex, height=grid_sizey, fill="url(#%s)" % self.grid_item_id),
                                   **{'id': self.grid_id, 'width': grid_sizex, 'height': grid_sizey, 'patternUnits': 'userSpaceOnUse'})
            self << defs
            self << helper.rect(fill="white", height=self.x*grid_sizex, width=self.y*grid_sizey)
            self << helper.rect(fill="url(#%s)" % self.grid_id, height=self.x*grid_sizex, width=self.y*grid_sizey)
        
        def _set_axes(self):
            """ Set up x and y axis for drawing canvas """
            self << helper.line(stroke="black", x1=self.x, x2=self.x, y1=0, y2=self.y*2)
            self << helper.line(stroke="black", x1=0, x2=self.x*2, y1=self.y, y2=self.y)
        
        def _set_origin(self):
            """ Set up origin dot and x/y coordinates for drawing canvas """
            self << helper.circle(cx=self.x, cy=self.y, r=2, fill="black", stroke="black", style="fill-opacity: 50%")
            self << helper.text("(0,0)", x=self.x+5, y=self.y-5, style="fill-opacity: 50%")
        
        def __str__(self):
            if self.grid:
                self._set_grid()
            if self.axes:
                self._set_axes()
            if self.origin:
                self._set_origin()
            if self.elements:
                for element in self.elements:
                    self << element
            return super(self.__class__, self).__str__()
    
    return svg(*args, **kw)