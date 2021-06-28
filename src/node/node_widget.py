
#* Kivy Imports
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

#* Global colors that can be changed from the setting page
empty_color = [0.5, 0.5, 0.5, 0.5]
barrier_color = [1, 0, 0, 0.5]
edge_color = [.5, 0, 0, 0.5]
start_color = [0, 1, 0, 1]
end_color = [0, 0, 1, 1]
neighbor_open = [0.1, 0.4, 0.0, 0.7]
neighbor_closed = [.0, .1, .5, 0.7]
solution_path = [1, 1, 1, 0.5]

#* Global variables to check if there is a start or end nodes
has_start_global = False
has_end_global = False

#* Node_widget class
#* Represents single node in the grid
class Node_widget(Widget):
    #* Initialize the node
    def __init__(self, **kwargs):
        super(Node_widget, self).__init__(**kwargs)
        
        #* Node variables
        self.is_empty = True
        self.is_barrier = False
        self.is_start = False
        self.is_end = False
        self.is_edge = False
        self.is_open_neighbor = False
        self.is_closed_neighbor = False
        self.is_solution_Path = False
        
        #* Node's neighbors in grid
        self.node_pos = ()
        self.node_neighbors = []
        
        #* Kivy binds. Calls the function when the event occurs
        self.bind( pos = self.update_node_canvas )
        self.bind( size = self.update_node_canvas )
        self.bind( on_touch_down = self.onPressed)
        self.bind( on_touch_move = self.onPressedMoved)
        
        #* Canvas variables
        self.color = []
        self.rect = Rectangle()
        
    #* Gets called automically when the widget pos/size changes
    #* Called to update the node's canvas
    def update_node_canvas(self, *args):
        if self.is_empty and not self.is_edge:
            rect_pos_x = self.pos[0] - 0.5
            rect_pos_y = self.pos[1] - 0.5
            rect_size_x = self.size[0] - 0.5
            rect_size_y = self.size[1] - 0.5
            
            self.color = empty_color
        else:
            rect_pos_x = self.pos[0]
            rect_pos_y = self.pos[1]
            rect_size_x = self.size[0]
            rect_size_y = self.size[1]

            if self.is_barrier:
                self.color = barrier_color
            elif self.is_start:
                self.color = start_color
            elif self.is_end:
                self.color = end_color
            elif self.is_open_neighbor:
                self.color = neighbor_open
            elif self.is_closed_neighbor:
                self.color = neighbor_closed
            elif self.is_solution_Path:
                self.color = solution_path
            elif self.is_edge:
                self.color = edge_color
            else:
                raise Exception("Node_Widget: Unknown variable")
        
        #* Draw the node
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            self.rect = Rectangle( pos = (rect_pos_x, rect_pos_y), size = (rect_size_x, rect_size_y))
        
    #* Reset the node  
    def reset_node(self):
        self.is_empty = True
        self.is_barrier = False
        self.is_start = False
        self.is_end = False
        self.is_edge = False
        self.is_open_neighbor = False
        self.is_closed_neighbor = False
        self.is_solution_Path = False
        
        self.node_pos = ()
        self.node_neighbors = []
        
        self.color = []
        self.rect = Rectangle()
        
    #* Updates the node that is pressed
    def onPressed(self, instance, touch):
        if not self.collide_point(*touch.pos):
            return
        
        global has_start_global
        global has_end_global
        
        if not self.is_edge:
            if self.is_empty:
                if not has_start_global:
                    self.color = start_color
                    has_start_global = True
                    self.is_empty = False
                    self.is_barrier = False
                    self.is_start = True
                    self.is_end = False
                    self.is_open_neighbor = False
                    self.is_closed_neighbor = False
                    self.is_solution_Path = False
                elif not has_end_global:
                    has_end_global = True
                    self.color = end_color
                    self.is_empty = False
                    self.is_barrier = False
                    self.is_start = False
                    self.is_end = True
                    self.is_open_neighbor = False
                    self.is_closed_neighbor = False
                    self.is_solution_Path = False
                else:
                    self.color = barrier_color
                    self.is_empty = False
                    self.is_barrier = True
                    self.is_start = False
                    self.is_end = False
                    self.is_open_neighbor = False
                    self.is_closed_neighbor = False
                    self.is_solution_Path = False
            else:
                if self.is_start:
                    has_start_global = False
                if self.is_end:
                    has_end_global = False
                self.color = empty_color
                self.is_empty = True
                self.is_barrier = False
                self.is_start = False
                self.is_end = False
                self.is_open_neighbor = False
                self.is_closed_neighbor = False
                self.is_solution_Path = False
                
            self.update_node_canvas()
        return
    
    def onPressedMoved(self, instance, touch):
        if not self.collide_point(*touch.pos):
            return
        
        global has_start_global
        global has_end_global
        
        if not self.is_edge:
            if self.is_start:
                has_start_global = False
            if self.is_end:
                has_end_global = False
            self.color = barrier_color
            self.is_empty = False
            self.is_barrier = True
            self.is_start = False
            self.is_end = False
            self.is_open_neighbor = False
            self.is_closed_neighbor = False
            self.is_solution_Path = False

        self.update_node_canvas()
        return
    
    #* Updates nodes variables and redraws the node
    def update_color(self, color):
        #* color: -1 = Edge, 0 = barrier_color, 1 = start_color, 2 = end_color, 3 = empty_color
        #* Algo: 4 = Neighbor open, 5 = Neighbor closed, 6 = Solution path
        
        global has_start_global
        global has_end_global
        
        if color == -1:
            self.color = edge_color
            self.is_edge = True
            self.is_empty = False
            self.is_barrier = False
            self.is_start = False
            self.is_end = False
            self.is_open_neighbor = False
            self.is_closed_neighbor = False
            self.is_solution_Path = False
            if self.is_start:
                has_start_global = False
            if self.is_end:
                has_end_global = False
        elif color == 0:
            self.color = barrier_color
            self.is_empty = False
            self.is_barrier = True
            self.is_start = False
            self.is_end = False
            self.is_open_neighbor = False
            self.is_closed_neighbor = False
            self.is_solution_Path = False
            if self.is_start:
                has_start_global = False
            if self.is_end:
                has_end_global = False
        elif color == 1:
            self.color = start_color
            has_start_global = True
            self.is_empty = False
            self.is_barrier = False
            self.is_start = True
            self.is_end = False
            self.is_open_neighbor = False
            self.is_closed_neighbor = False
            self.is_solution_Path = False
            if self.is_end:
                has_end_global = False
        elif color == 2:
            self.color = end_color
            has_end_global = True
            self.is_empty = False
            self.is_barrier = False
            self.is_start = False
            self.is_end = True
            self.is_open_neighbor = False
            self.is_closed_neighbor = False
            self.is_solution_Path = False
            if self.is_start:
                has_start_global = False
        elif color == 3:
            self.color = empty_color
            self.is_empty = True
            self.is_barrier = False
            self.is_start = False
            self.is_end = False
            self.is_open_neighbor = False
            self.is_closed_neighbor = False
            self.is_solution_Path = False
            if self.is_start:
                has_start_global = False
            if self.is_end:
                has_end_global = False
        elif color == 4:
            self.color = neighbor_open
            self.is_empty = False
            self.is_barrier = False
            self.is_start = False
            self.is_end = False
            self.is_open_neighbor = True
            self.is_closed_neighbor = False
            self.is_solution_Path = False
            if self.is_start:
                has_start_global = False
            if self.is_end:
                has_end_global = False
        elif color == 5:
            self.color = neighbor_closed
            self.is_empty = False
            self.is_barrier = False
            self.is_start = False
            self.is_end = False
            self.is_open_neighbor = False
            self.is_closed_neighbor = True
            self.is_solution_Path = False
            if self.is_start:
                has_start_global = False
            if self.is_end:
                has_end_global = False
        elif color == 6:
            self.color = solution_path
            self.is_empty = False
            self.is_barrier = False
            self.is_start = False
            self.is_end = False
            self.is_open_neighbor = False
            self.is_closed_neighbor = False
            self.is_solution_Path = True
            if self.is_start:
                has_start_global = False
            if self.is_end:
                has_end_global = False
        
        self.update_node_canvas()
        return
            