#First working solution 181 / 250 chars
r = range(5)
for x in r:
    for y in r:
        l = ""
        c = "purple"
        
        if 0<x<4 and 0<y<4:
            c = "white"
            if (x,y) == (2,2):
                c = "purple"
        if y > 3:
            c = "yellow"
            if x > 3:
                c = "purple"
        if (x,y) == (0,3):
            c = "yellow"

        if (x,y) == (4,0):
            l = "⚪"
            
        pydle(x, y, l, c)

#Final Solution 170 / 250 chars
p = "purple"
r = range(5)
for x in r:
    for y in r:
        l = ""
        c = p
        
        if 0<x<4 and 0<y<4:
            c = "white"
            if (x,y) == (2,2):
                c = p
        if y > 3:
            c = "yellow"
            if x > 3:
                c = p
        if (x,y) == (0,3):
            c = "yellow"

        if (x,y) == (4,0):
            l = "⚪"
            
        pydle(x, y, l, c)