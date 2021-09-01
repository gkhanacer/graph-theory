#!/usr/bin/python
# -*- coding: utf-8 -*-
# import itertools

class Cell:

    #newid = itertools.count()
    counter = 0
    def __init__(self, pose, size):
        self.id = Cell.counter #next(Cell.newid)
        Cell.counter += 1
        self.x = pose[0]
        self.y = pose[0]
        self.w = size
        self.h = size
        self.x1 = self.x
        self.y1 = self.y
    
