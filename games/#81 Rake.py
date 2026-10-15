#First working solution 106 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "white"

        if x == 2 or y < 1 and x%2:
            c = "brown"

        if y == 3 or y > 3 and 1 - x % 2:
            c = "black"

        pydle(x, y, "", c)