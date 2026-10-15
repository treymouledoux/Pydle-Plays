#First working solution 99 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "white"
        if 1-x%2:
            c = "yellow"

        if y < 1:
            c = "white"
            if x%2:
                c = "yellow"
        
        pydle(x, y, "", c)

#Final Solution 92 / 250 chars
w = "white"
q = "yellow"
r = range(5)
for x in r:
    for y in r:
        c = w
        if 1-x%2:
            c = q

        if y < 1:
            c = w
            if x%2:
                c = q
        
        pydle(x, y, "", c)