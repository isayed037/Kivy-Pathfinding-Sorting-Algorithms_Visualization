from kivy.properties import Clock

from queue import Queue

#* Implements the breadth first search algorithm
class BFS_algo():
    #* Initialize the algorithm
    def __init__(self):        
        #* Algorithm variable 
        self.open_set = None
        self.came_from = None
        self.current = None
        
        #* Algorithm clocks variables
        self.algorithm_clock = None
        self.solution_clock = None
        self.running = False
        self.has_solution = True
        self.auto = False
        self.speed = 1
    
    #* BFS algorithm set up
    def algorithm_setup(self, grid, all_nodes, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        
        self.running = True
        
        self.grid.get_neighbors(all_nodes)
        
        self.open_set = Queue()
        self.open_set.put(self.start)
        
        self.came_from = {}
        self.came_from[start] = None
            
    #* Loops thorugh the open_set each frame and stop with open_set is empty or a solution was found
    def algorithm(self, dt):
        self.current = self.open_set.get()
        
        if self.current == self.end:
            #* You can change the solution draw speed by changeing x in (self.solution, 1.0 / x)
            self.solution_clock = Clock.schedule_interval(self.solution, 1.0 / 30)
            self.running = False
            self.has_solution = True
            self.algorithm_clock.cancel()
            
        for neighbor in self.current.node_neighbors:            
            if neighbor not in self.came_from:
                self.open_set.put(neighbor)
                self.came_from[neighbor] = self.current
                #* Algo: 4 = Neighbor open, 5 = Neighbor closed, 6 = Solution path
                neighbor.update_color(4)    
        
        if self.current != self.start:
            self.current.update_color(5)
            
        if self.open_set.empty() and self.current != self.end:
            self.running = False
            self.has_solution = False
            self.algorithm_clock.cancel()
        
        if self.auto == False:
            self.algorithm_clock.cancel()
    
    #* Draws the solution
    def solution(self, dt):
        if self.current in self.came_from and self.current != self.start:
            self.current.update_color(6)
            self.current = self.came_from[self.current]
        else:
            self.running = False
            self.solution_clock.cancel()
            self.algorithm_clock.cancel()
    
    #* Kivy clock that controls when the algorithm is called 
    def algorithm_schedule(self):
        if self.auto == True:
            self.algorithm_clock = Clock.schedule_interval(self.algorithm, 1.0 / self.speed)
        else:
            self.algorithm_clock = Clock.schedule_once(self.algorithm)
    
    #* Controls the speed of the clock(Only affect algorithm_clock and not solution_clock)      
    def speed_clock(self, value):
        self.speed = value
        self.algorithm_clock.cancel()