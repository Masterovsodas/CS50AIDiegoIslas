
def main():
    text = input("Text: ")
    # formula vars
    # starts at one by def
    words = 1
    sentences = 0
    letters = 0

    for i in range(len(text)):
        if (text[i] == " "):
            words += 1
        elif (text[i] == "." or text[i] == "!" or text[i] == "?"):
            sentences += 1
        elif(ord(text[i].upper()) >= 65 and ord(text[i].upper()) <= 90):
            letters += 1

    # apply formula
    # make fraction over 100
    avgLettersPerWords = (letters/words) * 100
    avgSentencesPerWords = (sentences/words) * 100

    grade =  0.0588 *  avgLettersPerWords  - 0.296 * avgSentencesPerWords - 15.8
    print("Grade: " + str(round(grade)))


main()