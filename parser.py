from queue import Queue
import nltk
nltk.download('punkt')
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
NP -> N | N P Det | N Adv | Det N | Adj N | N P N
VPH -> V | V Det Adj | V NP Adj NP | V Det NP | V P Det NP | V P NP | Conj N V | V Adv 
VP -> VPH | VPH Adj Adj NP NP NP | VPH NP P NP Conj VPH | VPH Conj VPH | VPH Conj NP VPH Adv | VPH N | VPH VPH | VPH Det NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    # tokenize sentence
    tokens = nltk.word_tokenize(sentence)


    # grab all words with at least one alphabetical character
    for token in tokens:
        word = token.lower()
        for letter in word:
            if letter in alphabet:
                words.append(word)
                break
    print(words)
    return words

# array to keep track of noun phrase chunks
NPCs = []
def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """         
    # Subtrees autopmatically grasps all possible subtrees within structure, loop through them
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            isChunk = True
            # counter to skip first index, as fro some reason the subtree considers itself a subtree
            counter = 0

            for nsub in subtree.subtrees():
                # if NP and not self
                if nsub.label() == "NP" and counter > 0:
                    isChunk = False
                    break
                counter += 1

            if isChunk == True:
                NPCs.append(subtree)

    # when no more subtrees to process, spit up, until the first function returns filled NPCs
    return NPCs


if __name__ == "__main__":
    main()
