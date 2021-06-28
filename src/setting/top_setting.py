from kivy.uix.gridlayout import GridLayout

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.uix.spinner import Spinner

#* Setting that is displayed on the top of the window
class Top_setting(GridLayout):
    def __init__(self, **kwargs):
        super(Top_setting, self).__init__(**kwargs)
        self.cols = 5
        
        #* Button to return to the menu
        self.menu_button = Button(text = "Menu", background_color = (1,0,1,1))
        self.menu_button.size_hint = (.15, 1)
        
        #* Lets user update the row or column
        self.row_col_layout = GridLayout(rows = 2)
        self.row_col_layout.size_hint = (.4, 1)
        self.row = Button(text = 'Row:', background_color = (.1,.1,.9,.8))
        self.col = Button(text = 'Column:', background_color = (.1,.1,.9,.8))
        self.row_input = TextInput()
        self.col_input = TextInput()
        self.row_col_layout.add_widget(self.row)
        self.row_col_layout.add_widget(self.row_input)
        self.row_col_layout.add_widget(self.col)
        self.row_col_layout.add_widget(self.col_input)
        
        #* Lets user control the speed of the algorithm
        self.auto_step_layout = GridLayout(rows = 2, cols = 2) 
     
        self.auto_step_layout.size_hint = (.4, 1)
        self.auto_label = Label(text = 'Auto')
        self.auto_switch = Switch(active = False)
        self.speed_label = Label(text = 'Speed')
        self.auto_speed = Slider(min = 1, max = 60, value = 1)
        self.auto_step_layout.add_widget(self.auto_label)
        self.auto_step_layout.add_widget(self.auto_switch)
        self.auto_step_layout.add_widget(self.speed_label)
        self.auto_step_layout.add_widget(self.auto_speed)
        
        #* Lets user chose the algorithm
        self.chose_algo_layout = GridLayout(cols = 1)
        self.path_spinner = Spinner(text='Pick algorithm', values=('A star','Dijkstra', 'BFS', 'Maze'))
        self.sort_spinner = Spinner(text='Pick algorithm', values=('Bubble','Selection', 'Insertion', 'Random'))
        self.chose_algo_layout.size_hint = (.4, 1)
        
        #* Lets user reset or run the algorithm
        self.reset_run_layout = GridLayout(cols = 2)
        self.reset_run_layout.size_hint = (.5, 1)
        self.reset = Button(text='Reset', background_color = (1,.1,.1,1))
        self.run = Button(text='Run', background_color = (0, 1, 0, .9))
        self.reset_run_layout.add_widget(self.reset)
        self.reset_run_layout.add_widget(self.run)
        
        #* Add all the layouts to the main top_setting layout
        self.add_widget(self.menu_button)
        self.add_widget(self.row_col_layout)
        self.add_widget(self.auto_step_layout)
        self.add_widget(self.chose_algo_layout)
        self.add_widget(self.reset_run_layout)
