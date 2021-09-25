import copy
import random
import time

username = input("Enter Admiral Name\n")

class Game(object):
    def __init__(self, fleet, width, height):
        self.fleet = fleet
        self.shots = []
        self.width = width
        self.height = height
        
    # If ship was hit, update. Save shot on board needless of hit or miss. 
    def take_shot(self, shot_location):
        hit_ship = None
        is_hit = False
        for s in self.fleet:
            ind = s.hull_index(shot_location)
            if ind is not None:
                is_hit = True
                s.hits[ind] = True
                hit_ship = s
                break

        self.shots.append(Shot(shot_location, is_hit))
        return hit_ship
    
    # When one squad entire fleet has been destroyed the game is over. 
    def is_game_over(self):
         # ALL only returns true if the list of all the ships initial positions have been hit.
        return all([s.is_destroyed() for s in self.fleet])

class Shot(object):
    def __init__(self, location, is_hit):
        self.location = location
        self.is_hit = is_hit

class Ship(object):
    @staticmethod
    def build(front, length, lat_long):
        hull = []
        #Latitude and longitute (North, West etc.) Enables simple positioning of ships.
        for i in range(length):
            if lat_long == "N":
                elem = (front[0], front[1] - i)
            elif lat_long == "E":
                elem = (front[0] + i, front[1]) 
            elif lat_long == "W":
                elem = (front[0] - i, front[1])       
            elif lat_long == "S":
                elem = (front[0], front[1] + i)

            hull.append(elem)

        return Ship(hull, lat_long)
    
    def __init__(self, hull, lat_long):
        self.hull = hull
        self.lat_long = lat_long
        self.hits = [False] * len(hull)

    def hull_index(self, location):
        try:
            return self.hull.index(location)
        except ValueError:
            return None

    def is_destroyed(self):
        return all(self.hits)

class admiral (object):
    def __init__(self, name, shot_f):
        self.name = name
        self.shot_f = shot_f

# Construct empty board horisontally, fleet is set to True when adjusting placement of the fleets ships.
def render_basic(game_board, show_fleet = False):
    header = "#" + "-" * game_board.width + "#"
    print(header)

    board = []
    for _ in range(game_board.width):
        board.append([None for _ in range(game_board.height)])

    if show_fleet:
        # Enables construction of fleet, positioning is added later.
        for s in game_board.fleet:
            for i, (x, y) in enumerate(s.hull):
                # Hull shape
                if s.lat_long == "N":
                    shape = ("v", "|", "^")
                elif s.lat_long == "S":
                    shape = ("^", "|", "v")
                elif s.lat_long == "W":
                    shape = (">", "=", "<")
                elif s.lat_long == "E":
                    shape = ("<", "=", ">")
                else:
                    raise "Unknown lat/long"

                if i == 0:
                    add = shape[0]
                elif i == len(s.hull) - 1:
                    add = shape[2]
                else:
                    add = shape[1]
                board[x][y] = add

    # Add the shots to the board
    for sh in game_board.shots:
        x, y = sh.location
        if sh.is_hit:
            add = "X"
        else:
            add = "/"
        board[x][y] = add
    
    # Construct empty board vertically
    for y in range(game_board.height):
      
        row = []
        for x in range(game_board.width):
            row.append(board[x][y] or " ")
        print("|" + "".join(row) + "|")

    print(header)

def announce_en(event_type, metadata = {}):
    # Enable a player to choose their squad name.
    if event_type == "game_over":
        print("%s You Are Victorius" % metadata['admiral'])
    elif event_type == "new_turn":
        print("%s Your Turn!" % metadata['admiral'])
    elif event_type == "miss":
        print("%s Your Attack Was Unsucessfull" % metadata['admiral'])
    elif event_type == "Ship_destroyed":
        print("%s You Destroyed a Ship!" % metadata['admiral'])
    elif event_type == "Ship_hit":
        print("%s Your Attack Was Sucessfull!" % metadata['admiral'])
    else:
        # Game crashes if an admiral does add 10 (x or y) or above. Either wright in rules in instructions file or fix.
        print("Borde Missed: %s" % event_type)

def announce_none(event_type, metadata={}):
    pass

def get_human_shot(game_board):
    inp = input("Where Do You Want To Attack?\n")
    # Split is used to convert the string "x, y" to an array with x and y coordintes.
    xstr, ystr = inp.split(",")
    # Converts the arrays to integers.
    x = int(xstr)
    y = int(ystr)

    return (x, y)

# Provides random shot on the board, width / height -1 since coordinates goes from 0-9, negative numbers or 10 or above will crash the program.
def get_random_ai_shot(game_board):
    x = random.randint(0, game_board.width - 1)
    y = random.randint(0, game_board.height - 1)
    return (x, y)

def random_slow_ai(sleep_time):
    return slow_ai(get_random_ai_shot, sleep_time)

def slow_ai(ai_f, sleep_time):
    def f(game_board):
        time.sleep(sleep_time)
        return ai_f(game_board)
    return f

# Fleet, have to position fleet manually.
def run(announce_f, render_f):
    fleet = [
        Ship.build((6,3), 2, "N"),
        Ship.build((5,9), 5, "E"),
        Ship.build((4,1), 3, "W"),
        Ship.build((2,4), 4, "S")
    ]

    game_boards = [
        Game(fleet, 10, 10),
        # Copy to give each admiral their own board, not optimal since each board is identical, will work as long as the admiral dont have access to the code, wont make a difference to the ai.
        Game(copy.deepcopy(fleet), 10, 10)
    ]

    #Player + Ai. Only able to change name or let two human players or two AIs manually.
    Squad = [
        admiral(username, get_human_shot),
        # Ai 3.0 second delay before making a move.
        admiral("Dwight Schrute", random_slow_ai(3.0)),
    ]
    
    attacking_ind = 0
    
    while True:
        # While loop enables two player game, where players switch after each attack.
        # Defending admiral is the admiral which is not attacking.
        defending_ind = (attacking_ind + 1) % 2

        defending_board = game_boards[defending_ind]
        attacking_admiral = Squad[attacking_ind]

        announce_f("new_turn", {"admiral": attacking_admiral.name})
        shot_location = attacking_admiral.shot_f(defending_board)

        hit_ship = defending_board.take_shot(shot_location)
        if hit_ship is None:
            announce_f("miss", {"admiral": attacking_admiral.name})
        else:
            if hit_ship.is_destroyed():
                announce_f("Ship_destroyed", {"admiral": attacking_admiral.name})
            else:
                announce_f("Ship_hit", {"admiral": attacking_admiral.name})

        render_f(defending_board)
        
        if defending_board.is_game_over():
            announce_f("game_over", {"admiral": attacking_admiral.name})
            break
            
        # Defending fleet becomes the attacking fleet.
        attacking_ind = defending_ind

if __name__ == "__main__":
    run(announce_en, render_basic)
        

