# Broken, solution matches but site wont validate (166/250)
s = "HAPPYB'DAY❤❤❤❤❤"
r = range(5)
for y in r:
    for x in r:
        l = ""
        c = "black"

        if y > 1:
            c = "purple"
            l = s[(y-2)*5 + x]

        if y > 2:
            c = "brown"

        if (x,y) == (2,0):
            c = "orange"

        if (x,y) == (2,1):
            c = "white"
        
        pydle(x, y, l, c)