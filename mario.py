def getInt():
    try:
        intv = int(input("Height: "))
    except:
        getInt()
        return

    if(intv <= 0 or intv > 8):
        getInt()
        return

    return intv

height = getInt()

def main():
    build(height)


def build(h):

    if(h <= 0):
        return
    else:
        build(h - 1)
        blanks = height - h

        for i in range(height):
            if (i < blanks):
                print(" ", end="")
            else:
                print("#", end="")

        # add extra space
        print("  ", end="")

        for i in range(height - blanks):
            print("#", end="")
        print()

main()