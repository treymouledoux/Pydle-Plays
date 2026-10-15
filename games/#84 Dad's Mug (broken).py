# Broken, solution matches but site wont validate (139/250)
t = "I ❤️DAD"
r = range(5)
for x in r:
    for y in r:
        c = "blue"
        l = ""

        if abs((y-2)) == 2 and x > 2 or (x,y) == (3,2):
            c = "white"

        if y in [1,3] and x < 3:
            l = t[(y-1)*2 + x]

        pydle(x, y, l, c)