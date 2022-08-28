import nltk
import sys
# MAY CAUSE SUBMISSION FAILURE
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    fileDict = {}
    # for every file in directory, get string of text and apply it to the dict where the filename is the key
    for file in os.listdir(directory):
        text = ""
        # read through file and build string
        with open(os.path.join(directory, file), 'r', errors="ignore") as file:
            text = file.read()
        # assign var to split filename. Split returns a tuple and the following index symbol uses the length of the tuple - 1 as the index for the filename to grab the last bit. Uncessesary but dynamic
        fileDict[os.path.split(file.name)[len(os.path.split(file.name)) - 1]] = text
    # output
    return fileDict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # tokenize
    tokens = nltk.tokenize.word_tokenize(document)
    # array to record what needs to be removed to prevent tokens changing size during processing, and thus counting too high and breaking
    toRem = []

    # loop through words to fix them, record which ones need to be fixed for after this process
    for num in range(len(tokens)):
        # tolower
        tokens[num] = tokens[num].lower()
        # check if stopword
        if tokens[num] in nltk.corpus.stopwords.words("english"):
            toRem.append(tokens[num])
            
        # check if grammar
        if tokens[num][0] in string.punctuation:
            toRem.append(tokens[num])

    for token in toRem:
        tokens.remove(token)
    
    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    wordIdfs = {}

    # for every word in every doc, words will likely have values recalculated over and over, not efficient
    for key in documents:
        for word in documents[key]:
            # check in how many docs it appears
            appearsIn = 0

            for key in documents:
                if word in documents[key]:
                    appearsIn += 1

            # calculate log, base e by default
            wordIdfs[word] = math.log(len(documents) / appearsIn)
    return wordIdfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfs = {}
    # get tf-idf sum for every file in out dir
    for key in files:
        tfidfSum = 0
        # look for every queried word in file
        for word in query:
            appearances = 0
            # look though all words to see if current word
            for term in files[key]:
                if term == word:
                    appearances += 1

            # if word appears, add to file score
            if appearances > 0:
                # add to file tf-idf sum
                tfidfSum += appearances * idfs[word]
        # add file tf-idf to dict
        tfidfs[key] = tfidfSum

    topFiles = []
    # evaluate top n files
    for i in range(n):
        currG = 0
        out = None
        # do current greatest method and remove file from dict when currG to allow next winner to be found
        for tag in tfidfs:
            if tfidfs[tag] > currG:
                currG = tfidfs[tag]
                out = tag
            
        # remove winner but add to output
        topFiles.append(out)
        tfidfs.pop(out, None)

    return topFiles


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    fidfs = {}
    # get idf sum for every sentence in out list
    for key in sentences:
        idfSum = 0
        # look for every queried word in sentence
        for word in query:
            # add to sentence tf-idf sum
            if word in sentences[key]:
                idfSum += idfs[word]
        # add file tf-idf to dict
        fidfs[key] = idfSum



    topSentences = []
    # evaluate top n sentences
    for i in range(n):
        currG = 0
        out = None
        # note ties in score
        winners = []
        # do current greatest method and remove sentence from dict when currG to allow next winner to be found
        for tag in fidfs:

            # if greater, replace
            if fidfs[tag] > currG:
                currG = fidfs[tag]
                out = tag
                # rest winners array for new score
                winners = []
                winners.append(out)

            # if equal note for query term density
            if fidfs[tag] == currG:
                winners.append(tag)

        # check for query term density need
        if len(winners) > 1:
            # record best
            currG = 0
            out = None
             # grab each proportion of words in both to words in sentence
            for key in winners:
                proportion = 0
                for word in sentences[key]:
                    if word in query:
                        proportion += 1
                # check if this sentence's proportion is currG
                if (proportion / len(sentences[key])) > currG:
                    currG = (proportion / len(sentences[key]))
                    out = key
    
        # remove winner but add to output
        topSentences.append(out)
        idfs.pop(out, None)
    return topSentences


if __name__ == "__main__":
    main()
