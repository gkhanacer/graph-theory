#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math
import random
import numpy as np
from numpy.core.defchararray import translate
from typing import List
from maps import MapsWeights

class Cell:
    def __init__(self, center=list(), borders=dict(), is_visited=False, weight=0.0):
        self.center = center
        self.borders = borders
        self.is_visited = is_visited
        self.weight = weight
        
        self.ind_x, self.ind_y = (0, 0)

class Grid:
    MAP_SIZE = 3500 # 25 meters = 2500 cm
    MIN_DISTANCE = MAP_SIZE * MAP_SIZE
    MIN_WEIGHT = -1
    def __init__(self, cell_size=500, map_no=0) -> None:
        self.cell_size = cell_size # cm
        self.grid_size = math.ceil(Grid.MAP_SIZE / self.cell_size)
        self.origin_ind = math.floor(self.grid_size / 2)

        self.map_no = map_no

        # Set start position as center of grid
        self.pose = [self.origin_ind, self.origin_ind]

        # Robot path list
        self.path = list()
        self.path.append(self.pose)

        self.grid = self.create_grid()
        self.fill_weights()
        self.current_cell = self.grid[self.origin_ind][self.origin_ind]
        self.current_cell.is_visited = True

        print("pose: " + str(self.pose))

    def get_current_cell(self):
        self.current_cell = self.grid[self.pose[0]][self.pose[1]]
        return self.current_cell

    def create_grid(self):
        """
        Creates and returns a grid according to Grid and Map size
        """
        grid = list()

        # Fill cells
        for row_ind in range(self.grid_size):
            col = list()
            for column_ind in range(self.grid_size):
                row_dist = self.origin_ind - row_ind
                column_dist = self.origin_ind - column_ind
                center_pose = [row_dist * self.cell_size, column_dist * self.cell_size]

                border_gap = self.cell_size / 2
                borders = { "x1": center_pose[0] + border_gap,
                            "y1": center_pose[1] + border_gap,
                            "x2": center_pose[0] + border_gap,
                            "y2": center_pose[1] - border_gap,
                            "x3": center_pose[0] - border_gap,
                            "y3": center_pose[1] - border_gap,
                            "x4": center_pose[0] - border_gap,
                            "y4": center_pose[1] + border_gap,
                            }
                weight = random.random()

                cell = Cell(center=center_pose, borders=borders, is_visited=False, weight=weight)
                cell.ind_x = row_ind
                cell.ind_y =column_ind
                col.append(cell)
            grid.append(col)
        return grid        

    def fill_weights(self):
        if self.map_no == 1:
            map = MapsWeights.map1_weights
        else:
            pass

        if self.map_no != 0:
            for row_ind in range(self.grid_size):
                for column_ind in range(self.grid_size):
                    self.grid[row_ind][column_ind].weight = map[row_ind][column_ind]
            
    def get_weights(self):
        weights = [[self.grid[row_ind][column_ind].weight for column_ind in range(self.grid_size)] for row_ind in range(self.grid_size)]
        return weights
    
    def get_current_unvisited_neighbors(self):
        neighbors = list()
        border = np.arange(0, self.grid_size)
        neigbors_ind = np.arange(-1,2) # [-1, 0, 1]
        for i in neigbors_ind:
            for j in neigbors_ind:
                if (i == 0) and (j == 0): continue
                row = self.pose[0] + i
                column = self.pose[1] + j
                if (row not in border) or (column not in border): continue
                
                # Select unvisited neighbors
                cell = self.grid[row][column]
                if not cell.is_visited:
                    print("{}, {}".format(row, column))
                    neighbors.append(cell)
        return neighbors

    def get_distance(self, row_ind, column_ind):
        x_distance = self.pose[0] - row_ind
        y_distance = self.pose[1] - column_ind
        return math.sqrt(x_distance*x_distance + y_distance*y_distance)

    def get_unvisited_nearest_cell(self):
        nearest_cell = None
        min_distance = Grid.MIN_DISTANCE
    
        for row_ind in range(self.grid_size):
            for column_ind in range(self.grid_size):
                #Check unvisited cell
                if self.grid[row_ind][column_ind].is_visited == False:  
                    if self.grid[row_ind][column_ind].weight >  Grid.MIN_WEIGHT:   
                        distance = self.get_distance(row_ind, column_ind)
                        if distance < min_distance:
                            min_distance = distance
                            nearest_cell = Cell()
                            nearest_cell.ind_x = row_ind
                            nearest_cell.ind_y = column_ind
        return nearest_cell

    def get_unvisited_nearest_pose(self):
        nearest_cell = self.get_unvisited_nearest_cell()
        if nearest_cell is None:
            return None
        
        next_cell = self.grid[nearest_cell.ind_x][nearest_cell.ind_y]
        next_cell.is_visited = True
        next_cell.weight = 1.0
        next_pose = [next_cell.ind_x, next_cell.ind_y]
        return next_pose

    def update_neighbor_weights(self):
        neighbors = self.get_current_unvisited_neighbors()
        for n in neighbors:
            if (self.grid[n.ind_x][n.ind_y].weight > Grid.MIN_WEIGHT):
                self.grid[n.ind_x][n.ind_y].weight += np.random.uniform(0, 0.1)

    def get_next_pose(self):
        next_cell = None

        neighbors = self.get_current_unvisited_neighbors()
        
        # If there is no unvisited neighbor, the grid is scanned.
        if len(neighbors) == 0:
            next_pose = self.get_unvisited_nearest_pose()
            self.path.append(next_pose)
            return next_pose

        # There are unvisited neighbors. Selection of next one which has max weight.
        max_weight = -1.0
        for cell in neighbors:
            print("[{}, {}]: {}".format(cell.ind_x, cell.ind_y, cell.weight))
            # Filter unreachable areas
            if cell.weight > max_weight:
                max_weight = cell.weight
                next_cell = cell

        # If Neighbros are unreachable. Go unvisited nearest pose
        if next_cell is None:
            next_pose = self.get_unvisited_nearest_pose()
            self.path.append(next_pose)
            return next_pose
        
        next_cell.is_visited = True
        next_cell.weight = 1.0
        next_pose = [next_cell.ind_x, next_cell.ind_y]
        self.path.append(next_pose)
        return next_pose



def main():
    grid = Grid(cell_size=500)

if __name__ == '__main__':
    main()
    