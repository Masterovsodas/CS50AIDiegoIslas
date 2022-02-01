import csv
import sys


def main():

    # TODO: Check for command-line usage
    if(len(sys.argv) != 3):
        print("Incorrect comamnd-line args")
        return

    # TODO: Read database file into a variable
    suspects = []

    file = open(sys.argv[1], "r")
    fileReader = csv.DictReader(file)

    for line in fileReader:
        suspects.append(line)

    # TODO: Read DNA sequence file into a variable
    sequenceFile = open(sys.argv[2], "r")
    sequenceReader = csv.reader(sequenceFile)
    sequence = next(sequenceReader)

    # TODO: Find longest match of each STR in DNA sequence
    sampleLongest = {}

    # grab keys from any suspects var in order to pass them each as subsequences
    for key in suspects[0]:
        if (key != "name"):
            # find longest match for specified subsequence / key
            thisRun = longest_match(str(sequence), str(key))

            # create new key + value for sample, containing consecutive lengths to aim for
            sampleLongest[key] = thisRun

    # TODO: Check database for matching profiles
    for i in suspects:
        # get next suspect
        suspect = i
        # load var to store STR matches
        matches = 0

        # get STR matches
        for seq in suspect:
            if (seq == "name"):
                continue
            if (int(suspect[seq]) == int(sampleLongest[seq])):
                matches += 1

        if(matches == len(sampleLongest)):
            print(suspect["name"])
            return

    print("no match")


return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()