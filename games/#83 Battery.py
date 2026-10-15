#First working solution 144 / 250 chars
b = ["red", "orange", "yellow", "green"]
r = range(5)
for x in r:
    for y in r:
        c = "white"
        l = ""

        if y == 2:
            c = "black"

        if 0 < y < 4 and x < 4:
            c = b[x]

        if (x,y) == (3,2):
            l = "⚡"
        
        pydle(x, y, l, c)