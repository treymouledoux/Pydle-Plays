#First working solution 79 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "yellow"

        if x % 2:
            c = "white"

        if y > 0:
            c = "red"

        pydle(x, y, "", c)