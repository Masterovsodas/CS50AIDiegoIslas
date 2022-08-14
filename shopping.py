import csv
import sys
from tokenize import _all_string_prefixes
from zlib import compressobj

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    file = open(filename, "r")
    dataReader = csv.reader(file)
    evidence = []
    labels = []

    # special arrays
    monthArray = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for row in dataReader:
        # skip first
        if row[0] == 'Administrative':
            continue

        # make array
        rowEvidence = []

        # index tracker
        counter = -1
        for data in row:
            counter += 1
            # all data are initially strings
            # if column header wants a float
            if counter in [1, 3, 5, 6, 7, 8, 9]:
                rowEvidence.append(float(data))
                continue

            # else make it an int, and ask if they are the special ones or label
            if counter in [10, 15, 16]:
                # month
                if counter == 10:
                    rowEvidence.append(monthArray.index(data))
                    continue
                # visitorType
                if counter == 15:
                    if data == 'Returning_Visitor':
                        rowEvidence.append(1)
                        continue
                    rowEvidence.append(0)
                    continue
                # weekend
                if counter == 16:
                    if data == 'TRUE':
                        rowEvidence.append(1)
                        continue
                    rowEvidence.append(0)
                    continue
    
            # if last index
            if counter == 17:
                if data == 'TRUE':
                    labels.append(1)
                    continue
                labels.append(0)
                continue
            
            # if just a regular int -> string, append
            rowEvidence.append(int(data))

        # add rowEvidence
        evidence.append(rowEvidence)
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    negs = labels.count(0)
    pos = labels.count(1)
    cPos = 0
    cNeg = 0
    for real, predicted in zip(labels, predictions):
        if real == 1:
            if real == predicted:
                cPos += 1
            continue
        # if actually neg
        if real == predicted:
            cNeg += 1
            
    trueP = float(cPos/pos)
    trueN = float(cNeg/negs)
    return (trueP, trueN)


if __name__ == "__main__":
    main()
