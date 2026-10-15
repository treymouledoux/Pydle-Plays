#First working solution 153 / 250 chars
u = "yellow"
r = range(5)
for x in r:
    for y in r:
        pydle(x, y, "", "blue")
        if x+y in [2,6] or x+y == 4 and y % 2:
            pydle(x, y, "", "white")
pydle(2, 2, "", "red")
pydle(3, 0, "", u)
pydle(0, 1, "", u)

#Final solution 137/250
u = "yellow"
r = range(5)
for x in r:
    for y in r:
        d = abs(x - 2) + abs(y - 2)
        pydle(x, y, "", "red" if d == 0 else "white" if d == 2 else "blue")
pydle(3, 0, "", u)
pydle(0, 1, "", u)