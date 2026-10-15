#First working solution 178 / 250 chars
r = range(5)
for x in r:
    for y in r:
        pydle(1 - (y % 2), y, "", "white")
        if y < 4:
            pydle(x, y, "", "black")
        else:
            pydle(x, y, "", "yellow")
            if x == 0:
                pydle(x, y, "", "red")
            if x == 2:
                pydle(x, y, "", "white")
pydle(4, 0, "😷", "")

#Final Solution 144 / 250 chars
w = "white"
r = range(5)
for y in r:
    for x in r:
        pydle(x, y, "", "yellow" if y == 4 else "black")
    pydle(1 - y % 2, y, "", w)
pydle(0, 4, "", "red")
pydle(2, 4, "", w)
pydle(4, 0, "😷", "")