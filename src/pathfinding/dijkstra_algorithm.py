from kivy.properties import Clock

from queue import PriorityQueue

#* Implements the dijkstra algorithm
class Dijkstra_algo():
    #* Initialize the algorithm
    def __init__(self):        
        #* Algorithm variable 
        self.count = None
        self.open_set = None
        self.came_from = None
        self.open_set_hash = None
        self.current = None
        self.cost = None
        self.cost_so_far = None
        
        #* Algorithm clocks variables
        self.algorithm_clock = None
        self.solution_clock = None
        self.running = False
        self.has_solution = True
        self.auto = False
        self.speed = 1
    
    #* Dijkstra algorithm set up
    def algorithm_setup(self, grid, all_nodes, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        
        self.running = True
        
        self.grid.get_neighbors(all_nodes)
        
        self.count = 0
        self.open_set = PriorityQueue()
        self.open_set.put((0, self.count, self.start))
        
        self.came_from = {}
        self.came_from[start] = None
        
        self.cost = {node: 1 for node in all_nodes}
        self.cost_so_far = {node: float('inf') for node in all_nodes}
        self.cost_so_far[start] = 0
        
        self.open_set_hash = {self.start}
    
    #* Loops thorugh the open_set each frame and stop with open_set is empty or a solution was found
    def algorithm(self, dt):
        self.current = self.open_set.get()[2]
        #self.open_set_hash.remove(self.current)
        
        if self.current == self.end:
            #* You can change the solution draw speed by changeing x in (self.solution, 1.0 / x)
            self.solution_clock = Clock.schedule_interval(self.solution, 1.0 / 30)
            self.running = False
            self.has_solution = True
            self.algorithm_clock.cancel()
            
        for neighbor in self.current.node_neighbors:
            new_cost = self.cost_so_far[self.current] + self.cost[neighbor]
            
            if neighbor not in self.open_set_hash or new_cost < self.cost_so_far[neighbor]:
                self.cost_so_far[neighbor] = new_cost
                self.count += 1
                self.open_set.put((new_cost, self.count, neighbor))
                self.came_from[neighbor] = self.current
                self.open_set_hash.add(neighbor)
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