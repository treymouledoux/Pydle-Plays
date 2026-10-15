#First working solution 147 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "white"
        l = ""

        if x == 2:
            c = "black"

        if y > 3:
            c = "green"

        if x > 2 and y < 2:
            c = "red"
            if (x,y) == (4,0):
                c = "white"

        if (x,y) == (1,3):
            l = "🟡"

        
        pydle(x, y, l, c)

#Final Solution 117 / 250 chars
i = 24
while i > -1:
    c = "white"
    l = ""

    if i % 5 == 2:
        c = "black"

    if i > 19:
        c = "green"

    if i in [3,8,9]:
        c = "red"

    if i == 16:
        l = "🟡"

    pydle(i % 5, i // 5, l, c)

    i -= 1
