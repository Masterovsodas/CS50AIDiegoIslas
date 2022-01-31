
height = 0

while(True):
    try:
        height = int(input("Height: "))
    except:
        continue

    if (height > 0 and height <= 8):
        break


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