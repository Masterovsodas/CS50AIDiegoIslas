import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having amounts of gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue
       
        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    caseProbzz = []
    for person in people:
        # person is a dict KEY!!!
        # gauge what prob condition to calculate. Essentially, how many genes and yes/no trait are we calculating the prob for
        # one gene condis
        if person in one_gene and have_trait:

            # check if parents
            if people[person]["mother"]:
                # for one gene calc prob af getting from either parent and NOT the other
                mother = people[person]["mother"]
                father = people[person]["father"]
                
                mom = 1
                notMom = 1
                # get prob mother and not mother
                if mother in two_genes:
                    # add prob that mom gives gene
                    mom *= 0.99
                    notMom *= 0.01
                elif mother in one_gene:
                    mom *= .50
                    notMom *= .50
                else:
                    # prob that gene from mom mutates
                    mom *= PROBS["mutation"]
                    notMom *= .99
                
                dad = 1
                notDad = 1
                # get prob dad and not dad
                if father in two_genes:
                   # add prob that mom gives gene
                    dad *= 0.99
                    notDad*= 0.01
                elif father in one_gene:
                    dad *= .50
                    notDad *= .50
                else:
                    # prob that gene from mom mutates
                    dad *= PROBS["mutation"]
                    notDad *= .99
                
                combinedProb = (mom * notDad) + (dad * notMom)
                # check if person has / has no trait, and factor in that probability to the whole prob for the person case (gene #, hastrait)
                if person in have_trait:
                    combinedProb *= PROBS["trait"][1][True]
                else:
                    combinedProb *= PROBS["trait"][1][False]
                # add prob
                caseProbzz.append(combinedProb)
            else:
                # else calculate raw prob
                if person in have_trait:
                    caseProbzz.append(PROBS["gene"][1] * PROBS["trait"][1][True])
                else:
                    caseProbzz.append(PROBS["gene"][1] * PROBS["trait"][1][False])

        # two gene condis
        elif person in two_genes:
            # check if parents
            if people[person]["mother"]:
                # for two gene, calc prob of getting from both parents given
                mother = people[person]["mother"]
                father = people[person]["father"]
                
                mom = 1
                # get prob mother and not mother
                if mother in two_genes:
                    # add prob that mom gives gene
                    mom *= 0.99
                elif mother in one_gene:
                    mom *= .50
                else:
                    # prob that gene from mom mutates
                    mom *= PROBS["mutation"]
                  
                dad = 1
                # get prob dad and not dad
                if father in two_genes:
                    # add prob that mom gives gene
                    dad *= 0.99
                elif father in one_gene:
                    dad *= .50
                else:
                    # prob that gene from mom mutates
                    dad *= PROBS["mutation"]
                
                combinedProb = dad * mom
                # check if person has / has no trait, and factor in that probability to the whole prob for the person case (gene #, hastrait)
                if person in have_trait:
                    combinedProb *= PROBS["trait"][2][True]
                else:
                    combinedProb *= PROBS["trait"][2][False]
                # add prob
                caseProbzz.append(combinedProb)
            else:
                # else calculate raw prob
                if person in have_trait:
                    caseProbzz.append(PROBS["gene"][2] * PROBS["trait"][2][True])
                else:
                    caseProbzz.append(PROBS["gene"][2] * PROBS["trait"][2][False])

        # no gene, but yes/no trait
        else: 
            if people[person]["mother"]:
                # for zero gene, calc prob of getting from Neither parents and yes/no trait
                mother = people[person]["mother"]
                father = people[person]["father"]
                    
                NotMom = 1
                # get prob mother and not mother
                if mother in two_genes:
                    # add prob that mom gives gene
                    NotMom *= PROBS["mutation"]
                elif mother in one_gene:
                    NotMom *= .50
                else:
                    # prob that gene from mom doesnt mutate
                    NotMom *= 0.99
                    
                NotDad = 1
                # get prob mother and not mother
                if father in two_genes:
                    # add prob that mom gives gene
                    NotDad *= PROBS["mutation"]
                elif father in one_gene:
                    NotDad *= .50
                else:
                    # prob that gene from dad doesnt mutate
                    NotDad = 0.99
                    
                combinedProb = NotDad * NotMom
                # check if person has / has no trait, and factor in that probability to the whole prob for the person case (gene #, hastrait)
                if person in have_trait:
                    combinedProb *= PROBS["trait"][0][True]
                else:
                    combinedProb *= PROBS["trait"][0][False]
                # add prob
                caseProbzz.append(combinedProb)
            else:
                # else calculate raw prob
                if person in have_trait:
                    caseProbzz.append(PROBS["gene"][0] * PROBS["trait"][0][True])
                else:
                    caseProbzz.append(PROBS["gene"][0] * PROBS["trait"][0][False])
    
    finalProb = 1
    for i in caseProbzz:
        finalProb *= i
        
    return finalProb


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # person is a key!

        # update prob
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
        # add trait probzz
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p
    return 0


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:

        whole = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        # gene probzz first
        if whole != 1:
            # make probabilities percentages of the whole
            probabilities[person]["gene"][0] /= whole
            probabilities[person]["gene"][1] /= whole
            probabilities[person]["gene"][2] /= whole

        # do for trait 
        traitWhole = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]

        if traitWhole != 1:
            probabilities[person]["trait"][True] /= traitWhole
            probabilities[person]["trait"][False] /= traitWhole
    return 0


if __name__ == "__main__":
    main()
