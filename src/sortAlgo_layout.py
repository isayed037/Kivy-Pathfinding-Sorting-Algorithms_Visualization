from kivy.uix.gridlayout import GridLayout
from kivy.properties import Clock

from node import Node_widget, node_widget
from grid import Sort_layout
from sorting import Bubble_sort, Selection_sort, Insertion_sort
from setting import Alert, Top_setting

#* Create the pathfinding layout
class SortAlgo_layout(GridLayout):
    def __init__(self, **kwargs):
        #* Initializes the top settings section and the grid. 
        #* Sets default algorithm to the selection sort algorithm
        super(SortAlgo_layout, self).__init__(**kwargs)
        self.rows = 2
        self.top_setting = Top_setting()
        self.top_setting.size_hint = (1, .1)
        self.add_widget(self.top_setting)
        
        self.grid = Sort_layout(Node_widget, 50, 20)
        self.grid.initialize_grid()
        self.add_widget(self.grid)
        
        self.algorithm = Selection_sort()
        self.init_binds()
        self.pathfinding_clock = Clock.schedule_interval(self.update, 1 / 10)

        # node_widget.has_end_global = True
        # node_widget.has_start_global = True
    
    #* Gets called continuously
    def update(self, dt):     
        self.top_setting.row_input.hint_text = str(self.grid.rows)
        self.top_setting.col_input.hint_text = str(self.grid.cols)
    
        if self.algorithm.running:
            self.grid.disabled = True
            self.top_setting.row_col_layout.disabled = True
            self.top_setting.chose_algo_layout.disabled = True
            self.top_setting.auto_step_layout.disabled = False
        else:
            self.grid.disabled = False
            self.top_setting.auto_step_layout.disabled = True
            self.top_setting.row_col_layout.disabled = False
            self.top_setting.run.disabled = False
            self.top_setting.run.text = "Run"
            self.top_setting.run.unbind(on_release = self.next_algo)
            self.top_setting.run.bind(on_release = self.run_algo)
            self.top_setting.chose_algo_layout.disabled = False
            
            if self.top_setting.sort_spinner.text == 'Pick algorithm':
                self.top_setting.run.disabled = True
    
    #* Initialize the kivy binds
    def init_binds(self):
        self.top_setting.menu_button.bind(on_release = self.go_to_menu)
        
        self.top_setting.run.bind(on_release = self.run_algo)
        self.top_setting.reset.bind(on_release = self.reset_grid)
        
        self.top_setting.row.bind(on_release = self.update_row_col)
        self.top_setting.col.bind(on_release = self.update_row_col)
        
        self.top_setting.auto_switch.bind(active=self.switch_callback)
        self.top_setting.auto_speed.bind(value = self.update_auto_speed)
        
        self.top_setting.chose_algo_layout.add_widget(self.top_setting.sort_spinner)
        self.top_setting.sort_spinner.bind(text = self.get_current_algo)
    
    #* Reset the grid and algo
    def reset_grid(self, _):
        self.algorithm.auto = False
        if self.algorithm.algorithm_clock is not None:
            self.algorithm.algorithm_clock.cancel()
        if self.algorithm.solution_clock is not None:
            self.algorithm.solution_clock.cancel()
            
        self.algorithm = self.get_current_algo(_, _)
        self.grid.initialize_grid()
        self.algorithm.running = False
     
    #* Get the current algo from the user   
    def get_current_algo(self, _, text):
        if text == 'Bubble':
            self.algorithm = Bubble_sort()
        if text == 'Selection':
            self.algorithm = Selection_sort()
        if text == 'Insertion':
            self.algorithm = Insertion_sort()
        if text == 'Random':
            self.grid.random = True
    
        return self.algorithm
    
    #* Get all the nodes, start, and end. Sets up the algorithm and calls switch_callback function
    def run_algo(self, _):
        self.grid.get_all_nodes()
        self.algorithm.algorithm_setup(self.grid)
        self.algorithm.auto = False
        self.top_setting.auto_switch.active = False
        self.switch_callback(self.top_setting.auto_switch, False)
    
    #* Updates and draws algorithm when user click next
    def next_algo(self, _):
        self.algorithm.algorithm_schedule()
    
    #* Update if the algorithm should run on auto or not
    def switch_callback(self, _, value):
        #* Auto is true
        if self.algorithm.running:
            if value == True:
                self.algorithm.auto = True
                self.top_setting.auto_speed.disabled = False
                self.algorithm.speed = self.top_setting.auto_speed.value
                self.algorithm.algorithm_schedule()
                self.top_setting.run.disabled = True
                self.top_setting.run.text = "Run"
                self.top_setting.run.unbind(on_release = self.next_algo)
                self.top_setting.run.bind(on_release = self.run_algo)
            #* Auto is false
            else:
                self.algorithm.auto = False
                self.top_setting.auto_speed.disabled = True
                self.top_setting.run.disabled = False
                self.top_setting.run.text = "Next"
                self.top_setting.run.unbind(on_release = self.run_algo)
                self.top_setting.run.bind(on_release = self.next_algo)
    
    #* Updates the speed of the algorithm    
    def update_auto_speed(self, _, speed):
        if self.algorithm.running:
            self.algorithm.speed_clock(speed)
            self.algorithm.algorithm_schedule()   
    
    #* Updates the row or column based on what the user enters
    #* The rows and cols can be any positive interger, but is limited to 400
    def update_row_col(self, _):
        rows = self.grid.rows
        cols = self.grid.cols
        try:
            x = int(self.top_setting.row_input.text)
            if 3 < x < 401:
                rows = x + 2
            else:
                Alert(title='Row out of bounds', text='Number out of bounds. \nEnter a number between 4 and 400')
        except:
            rows = self.grid.rows
            Alert(title='Row out of bounds', text='Rows can only be a number. \nEnter a number between 4 and 400')
        try:
            y = int(self.top_setting.col_input.text)
            if 3 < y < 401:
                cols = y + 2
            else:
                Alert(title='Column out of bounds', text='Number out of bounds. \nEnter a number between 4 and 400')
        except:
            cols = self.grid.cols
            Alert(title='Column out of bounds', text='Column can only be a number. \nEnter a number between 4 and 400')
        
        self.remove_widget(self.grid)
        
        self.grid = Sort_layout(Node_widget, rows, cols)
        self.grid.initialize_grid()
        self.add_widget(self.grid)
        
    #* Take the user back to the menu
    def go_to_menu(self, event):
        self.parent.transition.direction = 'right'
        self.parent.current = 'menu'
    
    #* Displays a alert with user runs algorithm with no start or end node
    #* 0 = no start node and 1 = no end node
    def no_start_end_Alert(self, missing):
        if missing == 0:
            Alert(title='Missing Start Node', text='Click any node in the grid\n to make it a start node')
        else:
            Alert(title='Missing End Node', text='Click any node in the grid\n  to make it a end node') 
        