#First working solution 106 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "white"

        if x > 3 or y < 2 and x < 3 or x == 1:
            c = "black"

        if (x,y) == (1,0):
            c = "white"
            
        pydle(x, y, "", c)

#Final Solution 103 / 250 chars
w = "white"
r = range(5)
for x in r:
    for y in r:
        c = w

        if x > 3 or y < 2 and x < 3 or x == 1:
            c = "black"

        if (x,y) == (1,0):
            c = w
            
        pydle(x, y, "", c)