#First working solution 116 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "black"

        if x+y == 4:
            c = "brown"

        if x+y in [3,4,5] and x > 1:
            c = "blue"

        if y-1==x:
            c = "yellow"

        pydle(x, y, "", c)

#Final Solution 111 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "black"

        if x + y == 4:
            c = "brown"

        if 2 < x+y < 6 and x > 1:
            c = "blue"

        if y - 1 == x:
            c = "yellow"

        pydle(x, y, "", c)