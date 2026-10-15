#First working solution 125 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "green"
        if y == 3 or x == 2:
            c = "white"

        if 0 < x < 4 and 0 < y < 4:
            c = "green"

        if y == 1 and x in [1,3]:
            c = "yellow"
        pydle(x, y, "", c)

#Final Solution 111 / 250 chars
