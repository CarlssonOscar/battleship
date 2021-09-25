import copy

class Game(object):

    def __init__(self, fleet, width, height):
        self.fleet = fleet
        self.shots = []
        self.width = width
        self.height = height
        
    # If ship was hit, update. Save shot on board needless of hit or miss. 
    def take_shot(self, shot_location):
        is_hit = False
        for s in self.fleet:
            ind = s.hull_index(shot_location)
            if ind is not None:
                is_hit = True
                s.hits[ind] = True
                break

        self.shots.append(Shot(shot_location, is_hit))

    def is_game_over(self):
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

        return Ship(hull)
    
    def __init__(self, hull):
        self.hull = hull
        self.hits = [False] * len(hull)

    def hull_index(self, location):
        try:
            return self.hull.index(location)
        except ValueError:
            return None

    def is_destroyed(self):
        return all(self.hits)

def render(game_board, show_fleet = False):
    header = "+" + "-" * game_board.width + "+"
    print(header)

    board = []
    for _ in range(game_board.width):
        board.append([None for _ in range(game_board.height)])

    if show_fleet:
        # Add fleet to board
        for s in game_board.fleet:
            for x, y in s.hull:
                board[x][y] = "1"

    for sh in game_board.shots:
        x, y = sh.location
        if sh.is_hit:
            add = "X"
        else:
            add = "/"
        board[x][y] = add

    for y in range(game_board.height):
      
        row = []
        for x in range(game_board.width):
            row.append(board[x][y] or " ")
        print("|" + "".join(row) + "|")

    print(header)


if __name__ == "__main__":
    fleet = [
        Ship.build((6,3), 2, "N"),
        Ship.build((5,9), 5, "E"),
        Ship.build((4,1), 3, "W"),
        Ship.build((2,4), 4, "S")
    ]

    game_boards = [
        Game(fleet, 10, 10),
        Game(copy.deepcopy(fleet), 10, 10)
    ]
    player_names = [
        "Username",
        "Dwight Schrute",
    ]

    attacking_ind = 0
    
    while True:
        # Attacking player is the non-defending one.
        defending_ind = (attacking_ind + 1) % 2
        defending_board = game_boards[defending_ind]

        print("%s Your Turn!" % player_names[attacking_ind])

        inp = input("Where Do You Wish To Attack?\n")
         # Split is used to convert the string "x, y" to an array with x and y coordintes.
        xstr, ystr = inp.split(",")
        # Converts the arrays to integers.
        x = int(xstr)
        y = int(ystr)

        defending_board.take_shot((x,y))
        render(defending_board)
        
        if defending_board.is_game_over():
            print("%s WINS!" % player_names[attacking_ind])
            break
        # # Defending fleet becomes the attacking fleet.
        attacking_ind = defending_ind

        

