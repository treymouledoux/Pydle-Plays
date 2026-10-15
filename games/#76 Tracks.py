#First working solution 94 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "black"

        if y in [0,4]:
            c = "brown"

        if y == 2 and 1 - x % 2:
            c = "white"

        pydle(x, y, "", c)