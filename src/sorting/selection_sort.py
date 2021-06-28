from kivy.properties import Clock


#* Implements the breadth first search algorithm
class Selection_sort():
    #* Initialize the algorithm
    def __init__(self):        
        #* Algorithm variable 
        self.current = None
        self.swap_value = None
        self.total = None
        self.draw = None
        
        #* Algorithm clocks variables
        self.algorithm_clock = None
        self.solution_clock = None
        self.running = False
        self.has_solution = True
        self.auto = False
        self.speed = 1
    
    #* Selection sort algorithm set up
    def algorithm_setup(self, grid):
        self.grid = grid
        
        self.running = True
                
        arr = self.grid.array_length.copy()
        self.swap_value = []
        self.current = 0
        self.total = len(arr) * 2
        self.draw = []
        
        for i in range(len(arr)):
            minimum = i
            
            for j in range(i + 1, len(arr)):
                self.draw.append(['check', i, j])
                if arr[j] < arr[minimum]:
                    minimum = j
              
            arr[minimum], arr[i] = arr[i], arr[minimum]
            self.draw.append(['swap', minimum, i])
                        
    #* Loops every frame and stop with self.draw is empty or a solution was found
    def algorithm(self, dt):
        if len(self.draw) > 0:
            if self.auto == False:
                self.algorithm_clock.cancel()
            draw_type, draw_row_1, draw_row_2 = self.draw.pop(0)
            if draw_type == 'swap':
                self.grid.swap_arrays(draw_row_1, draw_row_2)
            if draw_type == 'check':
                self.grid.draw_current_row(draw_row_1, draw_row_2)
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