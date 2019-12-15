"""
V. O'Donnell

Clone of 2048 game.

online version : http://www.codeskulptor.org/#user44_KDPawR9SehQzCIx_18.py
"""

import poc_2048_gui, random

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    slid_line = []
    add_line = []
    
    print "line start", line #for testing
    
    def slide (line1):
        for i in range(0, len(line1)):
            if line1[i] > 0:
                slid_line.append(line1[i])    
    slide(line)

    def add_up(line1):
        if line1[0] == line1[1]:
            add_line.append(line1[0] + line1[1])
            line1.pop(0)
            line1.pop(0)
        #if unequal pop 1st and append it to add_list
        else:
            add_line.append(line1[0])
            line1.pop(0)
    while len(slid_line) >= 2:        
        add_up(slid_line)
    if len(slid_line) > 0:
        add_line.append(slid_line[0])
    #add in zeros
    for i in range(0, len(line) - len(add_line)):
        add_line.append(0)

    return add_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.cells = []
        self.reset()
        #use this to generate the indices in a dictionary to use later        
        up_list = []
        for i in range(self.grid_width):
            up_list.append((0,i))
            
        left_list = []
        for i in range(self.grid_height):
            left_list.append((i, 0))
            
        right_list = []
        width_list = range(0, self.grid_width)
        for i in range(self.grid_height):
            right_list.append((i, width_list[-1]))
            
        down_list = []
        height_list = range(0, self.grid_height)
        for i in range(self.grid_width):
            down_list.append((height_list[-1], i ))
            
        self.indices = {UP:up_list, DOWN:down_list, LEFT:left_list, RIGHT:right_list}
               
    def reset(self):
        self.cells = [ [0 for col in range(self.grid_width)] for row in range(self.grid_height)] 
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        for i in range(self.grid_height):
            print str(self.cells[i])
        return ""

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        
        """
        #bool value used to determine whether to add a new tile
        add_new = True
        #to compare board changes
        comp_value_list = []
        comp_merge_list = []
        
        #opening
        for i in self.indices[direction]:
            temp_list = [i]
            
            #get proper length of either row or grid to iterate over:
            if direction == UP or direction == DOWN:
                length = len(self.indices[LEFT])
            else: 
                length = len(self.indices[UP])
            
            #step 1 of 3
            for j in range(length - 1):
                a = temp_list[-1][0] + OFFSETS[direction][0]
                b = temp_list[-1][1] + OFFSETS[direction][1]
                temp_list.append((a,b))
            
            #before merge, need to change the coordinates to tile value
            value_list = []
            for n in temp_list:
                value_list.append(self.cells[n[0]][n[1]])
            
            #step 2 merge()
            merge_list = merge(value_list)
           
            #step 3 iterate and store merged values back in grid
            for x in zip(merge_list, temp_list):
                self.cells[x[1][0]][x[1][1]] = x[0]
                print "TEST VALUE", x   

            #these lists are to compare board changes
            comp_merge_list.append(merge_list)
            comp_value_list.append(value_list)
            
        print "comp_merge_list", comp_merge_list #for testing
        print "comp_value_list", comp_value_list #for testing
        for x in zip(comp_merge_list, comp_value_list):
            if x[0] == x[1]:
                add_new = False
                print "x[0], x[1]", x[0], x[1] #for testing
                print "add_new False", add_new #for testing
            else:
                add_new = True
                print "x[0], x[1]", x[0], x[1] #for testing
                print "add_new True", add_new #for testing 
                break

        print "add_new FINAL VALUE", add_new # for testing
        if add_new == True:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile is 2 90% of the time and
        4 10% of the time.
        
        """
        num_list = [2,2,2,2,2,2,2,2,2,4]
        num = num_list[random.randint(0,9)]
        for n in range(1):
            count = 0
            while count < 1:
                x = random.randint(0, self.grid_height-1)
                y = random.randint(0, self.grid_width-1)
                if self.cells[x][y] == 0:
                    self.cells[x][y] = num
                    count += 1
        
    def set_tile(self, row, col, value):
        self.cells[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        
        """
        return self.cells[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
