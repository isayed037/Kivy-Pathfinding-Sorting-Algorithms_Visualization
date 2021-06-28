
from kivy.uix.gridlayout import GridLayout

from random import randint

#* Modified version of the grid from grid_layout to use in sort algorithm visualization
class Sort_layout(GridLayout):
    #* Initialize the grid
    def __init__(self, Node_widget, grid_rows, grid_cols, **kwargs):
        super(Sort_layout, self).__init__(**kwargs)
        
        #* Kivy sets the rows and cols of the grid based on whats passed in
        self.rows = grid_rows
        self.cols = grid_cols
        
        #* Variables
        self.node_grid = []
        self.array_length = []
        self.random_length = []
        self.random = False
        
        #* Create the grid of nodes
        for _ in range(grid_rows):
            node_row = []
            for _ in range(grid_cols):
                node_row.append(Node_widget())
            self.node_grid.append(node_row)

        #* Add individual nodes to the layout
        for row in self.node_grid:
            for node in row:
                self.add_widget(node)
    
    #* Initializes the grid
    def initialize_grid(self):
        if self.random:
            self.array_length = [randint(2, self.cols-1) for _ in range(self.rows)]
        else:
            self.array_length = [2 for _ in range(self.rows)]
        
        for row_index, row in enumerate(self.node_grid):
            for col_index, node in enumerate(row):
                node.reset_node()
                
                if self.array_length[row_index] > col_index:
                    if col_index == 0:
                        node.update_color(-1)
                    else:
                        node.update_color(0)
                else:
                    node.update_color(6)
    
    #* Redraws the grid       
    def redraw_sort(self):
        for row_index, row in enumerate(self.node_grid):
            for col_index, node in enumerate(row):
                node.reset_node()
                
                if self.array_length[row_index] > col_index:
                    if col_index == 0:
                        node.update_color(-1)
                    else:
                        node.update_color(0)
                else:
                    node.update_color(6)

    #* Get all the nodes and updated array_length for each row
    def get_all_nodes(self):        
        for row_index, row in enumerate(self.node_grid):
            has_empty = False
            for col_index, node in enumerate(row):
                if node.is_barrier:
                    if not has_empty:
                        self.array_length[row_index] = col_index + 1
                if node.is_empty:
                    self.array_length[row_index] = col_index + 1
                    has_empty = True
        
        self.redraw_sort()
        return self.array_length
    
    #* Swaps the position of the two rows and redraws the grid with updated colors for swapped rows
    def swap_arrays(self, row_1, row_2):
        self.array_length[row_1], self.array_length[row_2] = self.array_length[row_2], self.array_length[row_1]
        
        for row_index, row in enumerate(self.node_grid):
                for col_index, node in enumerate(row):
                    node.reset_node()
    
                    if row_index == row_1:
                            if self.array_length[row_index] > col_index:
                                if col_index == 0:
                                    node.update_color(-1)
                                else:
                                    node.update_color(4)
                            else:
                                node.update_color(6)
                    elif row_index == row_2:
                        if self.array_length[row_index] > col_index:
                            if col_index == 0:
                                node.update_color(-1)
                            else:
                                node.update_color(4)
                        else:
                            node.update_color(6)
                    else:
                        if self.array_length[row_index] > col_index:
                            if col_index == 0:
                                node.update_color(-1)
                            else:
                                node.update_color(0)
                        else:
                            node.update_color(6)
    
    #* Draws the the 2 rows that are passed in with different colors                    
    def draw_current_row(self, draw_row_1, draw_row_2):
        for row_index, row in enumerate(self.node_grid):    
                if row_index == draw_row_1 or row_index == draw_row_2:       
                    for col_index, node in enumerate(row):
                        node.reset_node()
                        
                        if row_index == draw_row_1:
                            if self.array_length[row_index] > col_index:
                                if col_index == 0:
                                    node.update_color(-1)
                                else:
                                    node.update_color(1)
                            else:
                                node.update_color(6)
                        if row_index == draw_row_2:
                            if self.array_length[row_index] > col_index:
                                if col_index == 0:
                                    node.update_color(-1)
                                else:
                                    node.update_color(2)
                            else:
                                node.update_color(6)
                        