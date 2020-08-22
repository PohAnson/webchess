class MoveHistory:
    '''MoveHistory works like a CircularStack'''
    def __init__(self, size):
        # Remember to validate input
        self.size = size
        self.__data = [None] * size
        self.head = None
    
    def push(self, move):
        if self.head is None:
            self.head = 0
        else:
            self.head = (self.head + 1) % self.size
        self.__data[self.head] = move
            
    def pop(self):
        # Remember to check if MoveHistory is empty
        if self.head != None:
            move = self.__data[self.head]
            self.__data[self.head] = None
            if self.head == 0:       #????????????
                self.head = self.size - 1 
            else:
                self.head -= 1
            return move
        else:
            return 'no more undo move'