#Final Solution 115 / 250 chars
s = "MoTuWeThFr"
i = 24
while i > -1:
    if i < 5:
        c = "green"
        l = s[0+2*i:2+2*i]
    else:
        c = "blue"
        l = 3 + ( 7 * (i // 5)) - 7 + i % 5

    pydle(i % 5, i // 5, l, c)

    i -= 1
