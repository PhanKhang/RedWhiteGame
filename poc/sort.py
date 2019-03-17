candidates = ["a", "b", "c", "d", "e", "f", "g"]

def distance2(letter1):
    rnum = ord("d")
    lnum1 = ord(letter1)
    return abs(rnum -lnum1)


candidates.sort(key=distance2, reverse=False)


print(candidates)

sample = "1 2 3 4 5 6 7"
print(sample[-3:-2])