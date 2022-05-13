import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # init new dict for probabilities
    probzzDict = {}
    for i in corpus:
        probzzDict[i] = 0

    # get neighbors
    neighbors = corpus[page]
    # calculate probability of each neighbor
    propProb = 0
    if len(neighbors) > 0:
        propProb = DAMPING / len(neighbors)
    # give proportional probability to each neighbor
    for i in neighbors:
        probzzDict[i] += propProb

    # get propProb for the 15% random roll; if no links exist this 15% becomes 100%
    randomProb = 0
    if len(neighbors) > 0:
        randomProb = (1 - DAMPING) / len(corpus)
    else:
        randomProb = 1 / len(corpus)
    # add prob to all 
    for i in probzzDict:
        # NOTE: i is a key
        probzzDict[i] += randomProb

    return probzzDict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probzzDict = {}
    for i in corpus:
        probzzDict[i] = 0

    # get a random sample from all keys in corpus
    currSamp = list(corpus.keys())
    currSamp = currSamp[random.randrange(len(corpus))]

    # every time a page is rolled, add +1 to its probzzDict value; then at the end divide all values by sample count to get percentages
    for i in range(n):
        # get probabilities for this sample to generate next
        probzz = transition_model(corpus, currSamp, damping_factor)
        keys = list(probzz.keys())

        # get new sample by using random.choices which randomly selects a value from a given array, given another arry contating the probability of eahc index of pkeys in its indices.
        sample = random.choices(keys, probzz.values())
        # get first index of returned data which contains result
        sample = sample[0]
        # add +1 to occurences of new sample
        probzzDict[sample] += 1

        # rest sample
        currSamp = sample

    for i in probzzDict:
        probzzDict[i] /= SAMPLES
    return probzzDict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probzzDict = {}
    for i in corpus:
        # start by assuming that probability of all is 1 / length of corpus
        probzzDict[i] = 1 / len(corpus)

    # while percentage changes are significant, loop through every page in corpus and run the interative algorithm
    changeFactor = 1.0

    # condition to break loop (ALL CHANGE BY LESS THAT ) .001
    canBreak = False
    while not canBreak:
        # Set canBreak to true for it to be verified later
        canBreak = True

        # make a temp clone and modify new vals after
        prevSamp = probzzDict.copy()

        # for every index in the corpus, do the algo
        for i in probzzDict:
            # run the equation to get prob
            firstProb = (1-damping_factor) / len(corpus)

            # to get the second prob, loop over all parents of current page, get their prob and div by the amount of links in the page, add the result of each parent to the second prob to
            # illustrate the sigma loop, then mult by .85 to proportionalize the prob
            
            # get parents, this includes pages with no links!!!
            parents = []
            for j in corpus:
                if i in corpus[j]:
                    parents.append(j)
                if len(corpus[j]) == 0:
                    parents.append(j)
            
            # calc second prob from parents
            secondProb = 0
            for j in parents:
                thisProb = prevSamp[j]
                # += becasue of sigma notattion (sum of all iterations)
                # dividing by amount of links in corpus to spread out prob evenly, if a page has more links pointing at it it will be given more prob fractions and thus be more likely
                # dont div by zero
                if len(corpus[j]) != 0:
                    secondProb += thisProb / len(corpus[j])
                else:
                    # if no links, assume it links to all including self
                    secondProb += thisProb / len(corpus)
           
            # if no change keep first prob
            if secondProb == 0:
                probzzDict[i] = firstProb
                continue
            else:
                # find how much prob changed by
                # if our current prob is the same as our new prob, no change occured due to no links, which cancels the multiplication and leaves probzz - firstProb (will be equal
                # since no parents means no second prob EVER)
                if prevSamp[i] != firstProb + (damping_factor * secondProb):
                    probzzDict[i] = firstProb + (damping_factor * secondProb)
                    changeFactor = abs(prevSamp[i] - (firstProb + (damping_factor * secondProb)))

                    # check if change > 0.001
                    if changeFactor > 0.001:
                        canBreak = False
    return probzzDict


if __name__ == "__main__":
    main()
