#First working solution 140 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "blue"
        l = ""

        if x+y == 3:
            c = "red"

        if y == 3:
            c = "black"
        if x in [1,2,3] and y in [2,4]:
            c = "white"
        if y == 4:
            if x in [0,4]:
                l = "🧊"

        pydle(x, y, l, c)

#Final Solution 123 / 250 chars
r = range(5)
for x in r:
    for y in r:
        l = "🧊" if y > 3 else ""
        c = "blue"

        if x + y == 3:
            c = "red"

        if y > 1 and 4 > x > 0:
            c = "white"
            l = ""

        if y == 3:
            c = "black"

        pydle(x, y, l, c)