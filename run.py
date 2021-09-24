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

