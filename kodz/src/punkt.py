# -*- coding: utf-8 -*-


class Punkt(object):

    def __init__(self, numer, x='0.0', y='0.0'):
        self.numer = numer
        self.x = str(x)
        self.y = str(y)

    def __str__(self):
        """
        Wydruk współrzędnych punktów w postaci tesktowej x y
        """
        return '%s %s' % (self.x, self.y)
        
    def set_x(self, x):
        self.x = str(x)
        
    def set_y(self, y):
        self.y = str(y)

    def set_coords(self, x, y):
        self.x = str(x)
        self.y = str(y)