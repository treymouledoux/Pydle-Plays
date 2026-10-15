#First working solution 233 / 250 chars
u = "yellow"
p = "purple"
r = range(5)
for x in r:
    for y in r:
        pydle(x, y, "", "white")
        if x > 1 and y < 3:
            if x % 2:
                pydle(x, y, "|", u)
            if y % 2:
                pydle(x, y, "─", u)
        if x + y == 4 and x < 4:
            pydle(x, y, "", p)
pydle(4, 0, "╱", u)
pydle(2, 2, "╱", p)
pydle(2, 0, "╲", u)
pydle(4, 2, "╲", u)
pydle(3, 1, "O", p)

#Final Solution 223 / 250 chars
u = "yellow"
p = "purple"
r = range(5)
for x in r:
    for y in r:
        if x > 1 and y < 3:                   
            dx, dy = x - 3, y - 1
            c = "O" if dx == dy == 0 else "|" if not dx else "─" if not dy else "╱" if dx*dy < 0 else "╲"
            pydle(x, y, c, p if x + y == 4 and x < 4 else u)
        elif x + y == 4:                      
            pydle(x, y, "", p)
        else:
            pydle(x, y, "", "white")