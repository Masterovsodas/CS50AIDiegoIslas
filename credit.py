

def main():
    number = input("Number: ")

    # start, stop (exclusive), end
    # mult by 2 and add individual digits to sum, start at num before last
    multSum = 0
    for i in range(len(number) - 2, -1, -2):
        num = int(number[i]) * 2

        # convert to str and add individual digits
        if (num > 9):
            num = str(num)
            multSum += int(num[0]) + int(num[1])
        else:
            num = str(num)
            multSum += int(num[0])

    # now add un multed nums
    addSum = 0
    for i in range(len(number)-1, -1, -2):
        addSum += int(number[i])

    if((multSum + addSum) % 10 != 0):
        print("INVALID")
        return

    # if number is valid, then check what model it is by inspecting its vals
    match number[0]:
        case "3":
            if (len(number) == 15 and (number[1] == "4" or number[1] == "7")):
                print("AMEX")
                return

        case "4":
            if (len(number) == 13 or len(number) == 16):
                print("VISA")
                return

        case "5":
            if (len(number) == 16 and int(number[1]) <= 5):
                print("MASTERCARD")
                return
    # else is invalid plus return
    print("INVALID")
    return


main()