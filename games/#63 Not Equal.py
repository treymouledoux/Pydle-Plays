#First working solution 123 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "white"
        if y % 2:
            c = "black"
        if x+y == 4 and 4>x>0:
            c = "red"
        if x == 1 and y == 4 or x == 3 and y == 0:
            c = "red"
        pydle(x, y, "", c)

#Final Solution 111 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "white"

        if y % 2:
            c = "black"

        if x+y == 4 and 4>x>0 or (x, y) in [(1, 4), (3, 0)]:
            c = "red"

        pydle(x, y, "", c)