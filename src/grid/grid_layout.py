from kivy.uix.gridlayout import GridLayout

#* Creates a grid with node_widgets
class Grid_Layout(GridLayout):
    #* Initialize the grid
    def __init__(self, Node_widget, grid_rows, grid_cols, **kwargs):
        super(Grid_Layout, self).__init__(**kwargs)
        #* Kivy sets the rows and cols of the grid based on whats passed in
        self.rows = grid_rows
        self.cols = grid_cols
        
        #* Variables
        self.node_grid = []
        self.all_nodes = []
        self.start = None
        self.end = None
        
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
    
    #* Initialize the grid        
    def initialize_grid(self):
        self.all_nodes = []
        self.start = None
        self.end = None
        
        for row_index, row in enumerate(self.node_grid):
            for col_index, node in enumerate(row):
                node.reset_node()
                
                if row_index == 0 or row_index == self.rows - 1 or col_index == 0 or col_index == self.cols - 1:
                    node.update_color(-1)
                else:
                    node.update_node_canvas()
                
                node.node_pos = (row_index, col_index)
    
    #* Gets all valid nodes. Returns all empty, start, and end nodes
    def get_all_nodes(self):
        self.all_nodes = []
        self.start = None
        self.end = None
        
        for row in self.node_grid:
            for node in row:
                #* Need to set node_neighbors to empty here
                node.node_neighbors = []
                
                if not node.is_barrier and not node.is_edge:
                    self.all_nodes.append(node)
                    
                    if node.is_start:
                        self.start = node
                    if node.is_end:
                        self.end = node
                    
        return self.all_nodes
    
    #* Sets the neighbors of all the nodes in list
    def get_neighbors(self, all_nodes):
        if len(all_nodes) != 0:
            for node in all_nodes:
                node_row_index = node.node_pos[0]
                node_col_index = node.node_pos[1]
                
                neighbors = [(node_row_index+1, node_col_index), (node_row_index,node_col_index-1), (node_row_index-1, node_col_index), (node_row_index,node_col_index+1)]
                
                for neighbor in neighbors:
                    neighbor_node = self.node_grid[neighbor[0]][neighbor[1]]
                    
                    if neighbor_node in all_nodes:
                        node.node_neighbors.append(neighbor_node)
        else:
            print("Passed in a empty list of nodes")
    
    #* Heuristic function that uses Manhattan distance
    def heuristic(self, current_widget):
        start_row = current_widget.node_pos[0]
        start_col = current_widget.node_pos[1]
        end_row = self.end.node_pos[0]
        end_col = self.end.node_pos[1]
        
        return abs(start_row - end_row) + abs(start_col - end_col)
    
    #* Returns the start and end nodes.
    def get_start_and_end(self):
        if self.start != None and self.end != None:            
            return self.start, self.end
        elif self.start == None and self.end == None:
            return None, None
        elif self.start == None:
            return None, self.end
        elif self.end == None:
            return self.start, None