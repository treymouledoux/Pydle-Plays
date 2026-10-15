#First working solution 138 / 250 chars
g = "green"
r = range(5)
for y in r:
    for x in r:
        pydle(x, y, "", "black")
        if y in [1,2] and x in [1,2,3]:
            pydle(x, y, "🍒", g)
    if y > 2:
        pydle(2, y, "", "brown")
pydle(2, 0, "", g)

#Final solution 116 / 250 chars
g = "green"
r = range(5)
for y in r:
    for x in r:
        c, e = "black", ""
        if 0 < x < 4 and 0 < y < 3:
            c, e = g, "🍒"
        elif x == 2: 
            c = "brown" if y > 2 else g
        pydle(x, y, e, c)