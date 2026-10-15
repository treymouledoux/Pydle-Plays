#First working solution 162 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "white"
        l =""
        
        if x+y in [3,4,5]:
            c = "red"

        if (x,y) in [(0,3), (3,0), (4,1)]:
            c = "white"

        if (x,y) == (4,0):
            c = "green"

        if x+y == 4 and x in [1,3]:
            l = "🔥"

        pydle(x, y, l, c)

#Final Solution 159 / 250 chars
w = "white"
r = range(5)
for x in r:
    for y in r:
        c = w
        l =""
        
        if x+y in [3,4,5]:
            c = "red"

        if (x,y) in [(0,3), (3,0), (4,1)]:
            c = w

        if (x,y) == (4,0):
            c = "green"

        if x+y == 4 and x in [1,3]:
            l = "🔥"

        pydle(x, y, l, c)