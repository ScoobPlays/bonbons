from random import randint

AIR = 0
PLAYER = 1 
CAVE = 2
WALL = 3

class Maze:
    def __init__(self, boxes: int = 3) -> None: 
        self.tree = [[0 for _ in range(boxes)] for _ in range(boxes)]

        self._CAVE_POSITION = (randint(0, boxes-1), randint(0, boxes-1))
        self._PLAYER_POSITION = (randint(0, boxes-1), randint(0, boxes-1))

        if self.tree[self._CAVE_POSITION[0]][self._CAVE_POSITION[1]] == AIR: # generates the cave position
            self.tree[self._CAVE_POSITION[0]][self._CAVE_POSITION[1]] = CAVE

            self.cave = self._CAVE_POSITION

        if self.tree[self._PLAYER_POSITION[0]][self._PLAYER_POSITION[1]] == AIR: # generates the players position
            self.tree[self._PLAYER_POSITION[0]][self._PLAYER_POSITION[1]] = PLAYER

        for index, item in enumerate(self.tree): # generates the walls
            wall_position = randint(0, boxes-1)

            if item[index] in (1, 2, 3):
                continue
            
            item[wall_position] = WALL


    def check_for_win(self) -> bool:
        positions = self.get()

        if positions == self.cave:
            return True
        
        return False

    def get(self) -> tuple[int]:
        for index, list_object in enumerate(self.tree):
            for value in list_object:
                if value == PLAYER:
                    return index, list_object.index(value)


    def move_up(self) -> str | list:
        positions = self.get()
        list_pos = positions[0]
        item_pos = positions[1]

        if list_pos == 0:
            return 'You cannot move up'

        if self.tree[list_pos-1][item_pos] == WALL:
            return 'You hit a wall'
  
        self.tree[list_pos][item_pos] = AIR
        self.tree[list_pos-1][item_pos] = PLAYER

        return self.tree

    def move_down(self) -> str | list:
        positions = self.get()
        list_pos = positions[0]
        item_pos = positions[1]
    
        if list_pos == len(self.tree)-1:
            return 'You cannot move down'
  
        if self.tree[list_pos+1][item_pos] == WALL:
            return 'You hit a wall'

        self.tree[list_pos][item_pos] = AIR
        self.tree[list_pos+1][item_pos] = PLAYER

        return self.tree

    def move_left(self) -> str | list:
        positions = self.get()
        list_pos = positions[0]
        item_pos = positions[1]
    
        if item_pos == 0:
            return 'You cannot move left'
  
        if self.tree[list_pos][item_pos-1] == WALL:
            return 'You hit a wall'

        self.tree[list_pos][item_pos] = AIR
        self.tree[list_pos][item_pos-1] = PLAYER

        return self.tree

    def move_right(self) -> str | list:
        positions = self.get()
        list_pos = positions[0]
        item_pos = positions[1]
    
        if item_pos == len(self.tree[0])-1:
            return 'You cannot move right'

        if self.tree[list_pos][item_pos+1] == WALL:
            return 'You hit a wall'
  
        self.tree[list_pos][item_pos] = AIR
        self.tree[list_pos][item_pos+1] = PLAYER

        return self.tree