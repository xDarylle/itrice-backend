def quarterly(data):
    res = []
    for i in range(0, 12):
        total = 0
        if i % 3 == 0 or i == 0:
            for j in range(0, 3):
                total += data[i+j]
            res.append(total)
    return res
