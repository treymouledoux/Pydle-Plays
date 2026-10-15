#First working solution 156 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "white"
        l = ""
        
        if x>3 and y>1 or y > 2 or x+y==0:
            c = "black"

        if y == 2 and (x in [1,3]):
            l = "⚡"

        pydle(x, y, l, c)
        pydle(x, 1-(x % 2)+3, "", "blue" if x < 4 else "black")

#Final Solution 147 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "white"
        
        if y > 2 or x+y in [0,6]:
            c = "black"

        pydle(x, y, "⚡" if y == 2 and (x in [1,3]) else "", c)
        pydle(x, 1-(x % 2)+3, "", "blue" if x < 4 else "black")
