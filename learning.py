def Sentence(somelist):
    string = ''
    i = 0
    for word in somelist:
        string += str(word)
        i += 1
        if i < len(somelist) - 1:
            string += ", "
        elif i < len(somelist):
            string += ' i '
    return string


def PicGrid(grid):
    for x in grid:
        for y in x:
            print(y, end='')
        print()
    print()


grid = [['.', '.', '0', '0', '.', '0', '0', '.', '.'],
        ['.', '0', '0', '0', '0', '0', '0', '0', '.'],
        ['.', '0', '0', '0', '0', '0', '0', '0', '.'],
        ['.', '.', '0', '0', '0', '0', '0', '.', '.'],
        ['.', '.', '.', '0', '0', '0', '.', '.', '.'],
        ['.', '.', '.', '.', '0', '.', '.', '.', '.']]

PicGrid(grid)

some_value = False


def change_some_value():
    global some_value
    some_value = True

print(some_value)
change_some_value()
print(some_value)

