
#-------------------------------------------------------------------------------
# Name:        Snake_MMO
# Purpose:     To win the Hackathon May 2-3
#
# Author:      Shrayus
#
# Created:     02/05/2014
# Copyright:   (c) Shrayus 2014
# Licence:     <1-800-bananas>
#-------------------------------------------------------------------------------

import random
import image

class Block:
    def __init__(self, position, lifetime):
        self.position = position
        self.lifetime = lifetime
        self.danger_zone = False

class Player:
    DEFAULT_LENGTH = 4

    VECTORS = {"L" : (-1,0), "R" : (1,0), "U" : (0,-1), "D" : (0,1)}

    def __init__(self,  position, ID, direction = (-1,0), length = DEFAULT_LENGTH):
        self.position = position
        self.ID = ID
        self.direction = direction
        self.length = length
        self.alive = True

class Game:
    DEFAULT_BOARD_SIZE = 30
    STARTING_WALL = 0

    EMPTY_BLOCK = 0
    SNAKE_ASS = 1
    PLAYER = 2
    FOOD = 3
    WALL = 4

    def __init__(self, walls = STARTING_WALL, food_list = [], player_list = [], move_queue = [], block_list = [], wall_list = []):
        self.curr_walls = walls
        self.food_list = food_list
        self.player_list = player_list
        self.next_id = 0
        self.move_queue = move_queue
        self.block_list = block_list

        board = []   #create the board with walls
        for x in range(Game.DEFAULT_BOARD_SIZE):
            row = []
            for y in range(Game.DEFAULT_BOARD_SIZE):
                row.append(Game.EMPTY_BLOCK)
            board.append(row)
        for x in range(Game.DEFAULT_BOARD_SIZE):
            board[x][0] = Game.WALL
            board[0][x] = Game.WALL
            
        self.board = board
        self.expand_walls(self.curr_walls)

    def __str__(self):
        return str(self.board)

    def print(self):
        string = ""
        for row in self.board:
           string = string + str(row) + '\n'
        return print(string)
    
    def add_tuples(x,y):
        return tuple(map(lambda x, y: x + y, tuple1, tuple2))

    def expand_walls(self, x):
        self.curr_walls = x
        if x == 0:
            return
        for y_coord in range(1,x):
            self.board[y_coord][x - 1] = Game.WALL
        for x_coord in range(1,x):
            self.board[x - 1][x_coord] = Game.WALL
        return

    def clean_board(self, x):
        self.remove_walls()
        self.expand_walls(x)
        for y_coord in range(x , Game.DEFAULT_BOARD_SIZE):
            for x_coord in range(x , Game.DEFAULT_BOARD_SIZE):
                block = self.board[y_coord][x_coord]

                if block == Game.FOOD:
                    for food in self.FOOD_LIST:
                        if food.position[0] == x_coord and food.position[1] == y_coord:
                            self.FOOD_LIST.remove(food)
                            break

                if block == Game.PLAYER:
                    for player in self.player_list:
                        if player.position[0] == x_coord and player.position[1] == y_coord:
                            self.player_list.remove(player)
                            player.alive = False
                            break

                self.board[y_coord][x_coord] = Game.EMPTY_BLOCK
        return

    def remove_walls(self):
        for y_coord in range(1,self.curr_walls):
            self.board[y_coord][self.curr_walls - 1] = Game.EMPTY_BLOCK
        for x_coord in range(1,self.curr_walls):
            self.board[self.curr_walls - 1][x_coord] = Game.EMPTY_BLOCK
        self.curr_walls = Game.DEFAULT_BOARD_SIZE
        return

    def add_player(self):
        new_walls = self.curr_walls

        if self.curr_walls >= Game.DEFAULT_BOARD_SIZE - 2 and self.board[self.curr_walls - 2][self.curr_walls - 2] != Game.EMPTY_BLOCK:
            return
        
        self.remove_walls();
        self.expand_walls(new_walls + 3)

        player = Player((self.curr_walls - 2, self.curr_walls - 2), self.next_id)
        self.player_list.append(player)
        self.board[self.curr_walls - 2][self.curr_walls - 2] = Game.PLAYER
        self.next_id += 1
        return

    def renew_player(self, player):    
        while (True):
            rando_x = random.randint(0, self.curr_walls - 2)
            rando_y = random.randint(0, self.curr_walls - 2)
            if self.board[rando_y][rando_x] == Game.EMPTY_BLOCK:
                self.player_list.append(player)
                player.position = (rando_x , rando_y)
                self.board[rando_y][rando_x] = Game.PLAYER
                break
        return
        
    def remove_player(self, player):
        self.player_list.remove(player)
        self.board[player.position[1]][player.position[0]] = Game.EMPTY_BLOCK
        return

    def add_food(self):
        num_foods = int(pow(len(self.player_list), .65))
        while len(self.food_list) < num_foods:
            while (True):
                rando_x = random.randint(0, self.curr_walls - 2)
                rando_y = random.randint(0, self.curr_walls - 2)
                if self.board[rando_y][rando_x] == Game.EMPTY_BLOCK:
                    self.food_list.append((rando_x , rando_y))
                    self.board[rando_y][rando_x] = Game.FOOD
                    break
        return

    def make_move(self):
        for player in self.player_list:
            old_position = player.position
            if (not player.alive):
                continue
            for move in self.move_queue:
                if move[0] == player.ID:
                    player.direction = Player.VECTORS[move[1]]
                    break
            player.position = self.add_tuples(player.direction, player.position)
            for player2 in self.player_list:
                if player.position == player2.position and player is not player2:
                    player.alive = False
                    player2.alive = False
            block = self.board[player.position[1]][player.position[0]]
            if block == Game.WALL or block == Game.SNAKE_ASS:
                player.alive = False
            if block == Game.FOOD:
                player.length += 1
            obj = Block(old_position, player.length)
            self.block_list.append(obj)
        self.move_queue = []
        self.update()
        return

    def update(self):
        for block in self.block_list:
            block.lifetime -= 1
            if block.lifetime == 0:
                self.board[block.position[1]][block.position[0]] = Game.EMPTY_BLOCK
        self.block_list = filter(lambda x: x.lifetime != 0, self.block_list)
        return
                
    def new_board_test(self):  #uses DEFAULT_BOARD_SIZE and STARTING_WALL to create a simple board
        for x in range(self.curr_walls):
            assert self.board[self.curr_walls - 1][x] == Game.WALL
        for y in range(Game.STARTING_WALL):
            assert self.board[y][self.curr_walls - 1] == Game.WALL
        self.remove_walls()
        for x in range(Game.DEFAULT_BOARD_SIZE):
            for y in range(Game.DEFAULT_BOARD_SIZE):
                assert self.board[y][x] == Game.EMPTY_BLOCK
        self.expand_walls(Game.STARTING_WALL)
        print("passed board_test1")
        return

    def add_player_test(self):
        self.add_player()
        player = self.player_list[-1]
        self.remove_player(player)
        assert player not in self.player_list
        assert self.board[self.curr_walls - 2][ self.curr_walls - 2] == Game.EMPTY_BLOCK
        self.renew_player(player)
        self.print()
        print("passed player_test1")
        return

    def clean_board_test(self):
        for y in range(1,self.DEFAULT_BOARD_SIZE):
            for x in range(1,self.DEFAULT_BOARD_SIZE):
                self.board[y][x] = 1
        self.clean_board(3)
        self.print()
        return
