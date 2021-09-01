#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from subgrid import Grid, Cell

class Plot:
    def __init__(self, grid: Grid) -> None:
        self.grid = grid

        self.pose = self.grid.pose
        # self.path = list()
        # self.path.append(self.pose[:])
        print("pose: " + str(self.pose))

        self.fig, self.axes = plt.subplots()
        self.fig.canvas.mpl_connect('button_press_event', self.onClick)

        indeces = list(range(self.grid.grid_size))
        self.data = self.grid.get_weights() #np.zeros((self.grid.grid_size, self.grid.grid_size))
        self.data[self.pose[0]][self.pose[1]] = 1
        self.axes.imshow(self.data)
        # plt.imshow(self.data)

        self.axes.set_xticklabels(indeces)
        self.axes.set_yticklabels(indeces)

        self.axes.set_xticks(np.arange(len(self.data)) + 0.5, minor=False)
        self.axes.set_yticks(np.arange(len(self.data)) + 0.5, minor=False)
        
        self.axes.tick_params(which="major", bottom=True, left=True)
        self.axes.grid(which="major", color="k", linestyle='-', linewidth=3)

        # Loop over self.data dimensions and create text annotations.
        self.text_obj_list = np.empty((self.grid.grid_size, self.grid.grid_size), dtype=object)
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                self.text_obj_list[i][j] = self.axes.text(j, i, round(self.data[i][j], 2), ha="center", va="center", color="w")
        
        plt.show()  

    def draw_path(self, path):
        if len(path) > 1:
            x_val = [path[-2][0], path[-1][0]]
            y_val = [path[-2][1], path[-1][1]]
            plt.plot(y_val, x_val, marker = 'o')   

    def fill_data(self):
        self.data[self.pose[0]][self.pose[1]] = 1
        self.axes.imshow(self.data)

        # Loop over self.data dimensions and create text annotations.
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                self.text_obj_list[i][j].set_text(str(round(self.data[i][j], 2)))

    def onClick(self, event):
        pose = self.grid.get_next_pose()
        if pose is None:
            print("Grid is covered!")
            print("Path: {}".format(self.grid.path))
            return
        self.pose = pose
        self.grid.pose = pose
        print("pose: " + str(self.pose))

        # self.path.append(self.pose[:])
        self.draw_path(self.grid.path)
        self.grid.update_neighbor_weights()
        self.data = self.grid.get_weights()
        self.fill_data()

        # self.fig.canvas.draw()
        # self.fig.canvas.flush_events()
        plt.draw()

def main():
    # 1. Create a grid
    grid = Grid(cell_size=500, map_no=0)
    plot = Plot(grid=grid)

if __name__ == "__main__":
    main()

