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

if __name__ == "__main__":
    attack = []

    while True:
        inp = input("Where do you wish to attack?\n")
        xstr, ystr = inp.split(",")
        x = int(xstr)
        y = int(ystr)

        attack.append((x,y))
        render(10, 10, attack)

