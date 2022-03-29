from random import randint

# 0 = air
# 1 = the player
# 2 = the exit

class Maze:
    def __init__(self, boxes: int = 3) -> None: 
        self.tree = [
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
            ]
        self._x = randint(0, 2)
        self._y = randint(0, 2)
        
        if self.tree[self._x][self._y] != 1:
            self.tree[self._x][self._y] = 2

        self.cave = (self._x, self._y)


    def check_for_win(self) -> bool:
        positions = self.get()

        if positions == self.cave:
            return True
        
        return False

    def get(self) -> tuple[int]:
        for index, list_object in enumerate(self.tree):
            for value in list_object:
                if value == 1:
                    return index, list_object.index(value)

    def move_up(self) -> str | list:
        positions = self.get()
        list_pos = positions[0]
        item_pos = positions[1]

        if list_pos == 0:
            return 'You cannot move up'
  
        self.tree[list_pos][item_pos] = 0
        self.tree[list_pos-1][item_pos] = 1

        return self.tree

    def move_down(self):
        positions = self.get()
        list_pos = positions[0]
        item_pos = positions[1]
    
        if list_pos == 2:
            return 'You cannot move down'
  
        self.tree[list_pos][item_pos] = 0
        self.tree[list_pos+1][item_pos] = 1

        return self.tree

    def move_left(self):
        positions = self.get()
        list_pos = positions[0]
        item_pos = positions[1]
    
        if item_pos == 0:
            return 'You cannot move left'
  
        self.tree[list_pos][item_pos] = 0
        self.tree[list_pos][item_pos-1] = 1

        return self.tree

    def move_right(self):
        positions = self.get()
        list_pos = positions[0]
        item_pos = positions[1]
    
        if item_pos == 2:
            return 'You cannot move right'
  
        self.tree[list_pos][item_pos] = 0
        self.tree[list_pos][item_pos+1] = 1

        return self.tree