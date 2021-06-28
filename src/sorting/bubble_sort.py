from kivy.properties import Clock

#* Implements the breadth first search algorithm
class Bubble_sort():
    #* Initialize the algorithm
    def __init__(self):        
        #* Algorithm variable 
        self.node_length = None
        self.len = None
        self.swapped = None
        self.count = None
        
        #* Algorithm clocks variables
        self.algorithm_clock = None
        self.solution_clock = None
        self.running = False
        self.has_solution = True
        self.auto = False
        self.speed = 1
    
    #* Bubble sort algorithm set up
    def algorithm_setup(self, grid):
        self.grid = grid
        
        self.running = True

        self.len = len(self.grid.array_length)
        self.swapped = True
        self.count = -1
            
    #* Loops every frame and stops when swapped is false or a solution was found
    def algorithm(self, dt):
        if self.swapped:
            if self.auto == False:
                self.algorithm_clock.cancel()
            self.swapped = False
            self.count = self.count + 1
            for i in range(1, self.len - self.count):
                if self.grid.array_length[i - 1] > self.grid.array_length[i]:
                    self.grid.swap_arrays(i - 1, i)
                    # self.node_length[i - 1], self.node_length[i] = self.node_length[i], self.node_length[i - 1]
                    self.swapped = True
        else:
            self.running = False
    
    #* Kivy clock that controls when the algorithm is called 
    def algorithm_schedule(self):
        if self.auto == True:
            self.algorithm_clock = Clock.schedule_interval(self.algorithm, 1.0 / self.speed)
        else:
            self.algorithm_clock = Clock.schedule_once(self.algorithm)
    
    #* Controls the speed of the clock       
    def speed_clock(self, value):
        self.speed = value
        self.algorithm_clock.cancel()