#First working solution 156 / 250 chars
r = range(5)
for x in r:
    for y in r:
        c = "white"
        if x + y in [3,4,5]:
            if x==1 and y==2 or x==2 and y==3:
                c = "orange"
            elif x > 3 and y < 1:
                c = "blue"
            elif x < 2:
                c = "yellow"
        else:
            c = "black"
        pydle(x, y, "", c)