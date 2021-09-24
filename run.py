class Game(object):

    def __init__(self, fleet, width, height):
        self.fleet = fleet
        self.shots = []
        self.width = width
        self.height = height

    def take_shot(self, shot_location):
        is_hit = False
        for s in self.fleet:
            ind = s.hull_index(shot_location)
            if ind is not None:
                is_hit = True
                s.hits[ind] = True
                break

        self.shots.append(Shot(shot_location, is_hit))


class Shot(object):

    def __init__(self, location, is_hit):
        self.location = location
        self.is_hit = is_hit


class Ship(object):

    @staticmethod
    def build(front, length, lat_long):
        hull = []
        #Latitutue and longitute (North, West etc.) Enables simple positioning of ships.
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

def render(width, height, attack):
    header = "#" + "-" * width + "+"
    print(header)

    attack_set = set(attack)
    for y in range(height):
        row = []
        for x in range(width):
            if (x,y) in attack_set:
                add = "X"
            else:
                add = " "
            row.append(add)
        print("|" + "".join(row) + "|")

    print(header)

def render_fleet(width, height, fleet):
    header = "#" + "-" * width + "#"
    print(header)

    board = []
    for _ in range(width):
        board.append([None for _ in range(height)])

    for s in fleet:
        for x, y in s.hull:
            board[x][y] = "O"

    for y in range(height):
        row = []
        for x in range(width):
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

    for s in fleet:
        print(s.hull)

    render_fleet(10, 10, fleet)

    exit(0)
    
    attack = []

    while True:
        inp = input("Where do you wish to attack?\n")
         # Split is used to convert the string "x, y" to an array with x and y coordintes.
        xstr, ystr = inp.split(",")
        # Converts the arrays to integers.
        x = int(xstr)
        y = int(ystr)

        attack.append((x,y))
        render(10, 10, attack)

