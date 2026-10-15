#First working solution 147 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "yellow"
        l = ""

        if y < 1 and 0 < x < 4:
            c = "blue"

        if (x,y) == (2,1):
            c = "blue"
            l = "🫒"

        if y > 1 and x in [0,4] or y == 3 and x in [1,3]:
            c = "white"

        pydle(x, y, l, c)