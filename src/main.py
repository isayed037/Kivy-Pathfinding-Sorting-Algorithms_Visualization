from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty

#* Imports
from pathfindingAlgo_layout import Pathfinding_layout
from sortAlgo_layout import SortAlgo_layout
from setting import Alert
from node import node_widget

#* Kivy Screen setup
class MenuScreen(Screen):
    pass

#* Lets the user change the colors
class SettingsScreen(Screen):
    #* Sets up kivy property to update automically when value changes
    empty_color = ListProperty()
    barrier_color = ListProperty()
    edge_color = ListProperty()
    start_color = ListProperty()
    end_color = ListProperty()
    neighbor_open = ListProperty()
    neighbor_closed = ListProperty()
    solution_path = ListProperty()
    
    #* Initialize the setting screen
    def __init__(self, **kw):     
        super(SettingsScreen, self).__init__(**kw)
        self.color = None
        
        self.empty_color = node_widget.empty_color
        self.barrier_color = node_widget.barrier_color
        self.edge_color = node_widget.edge_color
        self.start_color = node_widget.start_color
        self.end_color = node_widget.end_color
        self.neighbor_open = node_widget.neighbor_open
        self.neighbor_closed = node_widget.neighbor_closed
        self.solution_path = node_widget.solution_path

    #* Update the color based on user input
    def update_color(self):
        if self.ids.empty_input.text != '':
            self.color = []
            input = self.ids.empty_input.text
            if self.check_input(input):
                node_widget.empty_color = self.color
                self.empty_color = self.color
        if self.ids.barrier_input.text != '':
            self.color = []
            input = self.ids.barrier_input.text
            if self.check_input(input):
                node_widget.barrier_color = self.color
                self.barrier_color = self.color
        if self.ids.edge_input.text != '':
            self.color = []
            input = self.ids.edge_input.text
            if self.check_input(input):
                node_widget.edge_color = self.color
                self.edge_color = self.color
        if self.ids.start_input.text != '':
            self.color = []
            input = self.ids.start_input.text
            if self.check_input(input):
                node_widget.start_color = self.color
                self.start_color = self.color
        if self.ids.end_input.text != '':
            self.color = []
            input = self.ids.end_input.text
            if self.check_input(input):
                node_widget.end_color = self.color
                self.end_color = self.color
        if self.ids.neighbor_open_input.text != '':
            self.color = []
            input = self.ids.neighbor_open_input.text
            if self.check_input(input):
                node_widget.neighbor_open = self.color
                self.neighbor_open = self.color
        if self.ids.neighbor_closed_input.text != '':
            self.color = []
            input = self.ids.neighbor_closed_input.text
            if self.check_input(input):
                node_widget.neighbor_closed = self.color
                self.neighbor_closed = self.color
        if self.ids.solution_path_input.text != '':
            self.color = []
            input = self.ids.solution_path_input.text
            if self.check_input(input):
                node_widget.solution_path = self.color
                self.solution_path = self.color
    
    #* Resets the colors
    def reset_color(self):
        self.empty_color = [0.5, 0.5, 0.5, 0.5]
        node_widget.empty_color = self.empty_color
        self.ids.empty_input.text = ''
        
        self.barrier_color = [1, 0, 0, 0.5]
        node_widget.barrier_color = self.barrier_color
        self.ids.barrier_input.text = ''
        
        self.edge_color = [.5, 0, 0, 0.5]
        node_widget.edge_color = self.edge_color
        self.ids.edge_input.text = ''
        
        self.start_color = [0, 1, 0, 1]
        node_widget.start_color = self.start_color
        self.ids.start_input.text = ''
        
        self.end_color = [0, 0, 1, 1]
        node_widget.end_color = self.end_color
        self.ids.end_input.text = ''
        
        self.neighbor_open = [0.1, 0.4, 0.0, 0.7]
        node_widget.neighbor_open = self.neighbor_open
        self.ids.neighbor_open_input.text = ''
        
        self.neighbor_closed = [.0, .1, .5, 0.7]
        node_widget.neighbor_closed = self.neighbor_closed
        self.ids.neighbor_closed_input.text = ''
        
        self.solution_path = [1, 1, 1, 0.5]
        node_widget.solution_path = self.solution_path
        self.ids.solution_path_input.text = ''
    
    #* Check if the input are floats between 0 and 1
    def check_input(self, input):
        try:
            valid = True
            self.color = input.split(',')
            if len(self.color) == 4:
                for num in self.color:
                    num = float(num)
                                        
                    if not 0 <= num <= 1:
                        valid = False
                        self.color = []
            else:
                valid = False
                Alert(title='Invalid Input', text=input + ' is a invalid input')
                self.color = []
                
            return valid
        except:
            Alert(title='Invalid Input', text=input + ' is a invalid input')
            self.color = []
            return False

#* Pathfinding layout
class Pathfinding_layout_root(Pathfinding_layout, Screen):
    pass

#* Soarting layout
class Sorting_layout_root(SortAlgo_layout, Screen):
    pass

#* Kivy main app
class AlgoVizKivyApp(App):
    def build(self):
        #* Kivy screen manger setup
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(Pathfinding_layout_root(name='path'))
        sm.add_widget(Sorting_layout_root(name='sort'))
        
        return sm

if __name__ == '__main__':
    AlgoVizKivyApp().run()