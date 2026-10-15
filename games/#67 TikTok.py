#First working solution 163 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "black"
        if x == 3 and y < 4 or (1 - y) % 2 and y>1:
            c = "white"
        if x>3 or (x,y) == (3,4):
            c = "black"
            if y == 1:
                c = "white"
        if x<1:
            c = "black"
            if y == 3:
                c = "white"
        pydle(x, y, "", c)