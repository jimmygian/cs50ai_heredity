import csv
import itertools
import sys
import math
# import pandas
# import numpy

PROBS = {

    # Unconditional probabilities for having gene
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
    print("======DATA======")
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
    print(f"names: {names} \n")
    for name in names:
        print(f"people[{name}] - {"SON" if people[name]['mother'] or people[name]['father'] else "PARENT"}:\n {people[name]}")
    print(f"probabilities:\n {probabilities} \n")
    # print(f"powerset(names):\n {powerset(names)} \n")
    
    print("================\n")

    # Loop over all (sub)sets of people who might have the gene, skip the ones that don't
    # 'have_trait' is a set of all people for whom we want to compute the probability that they have the trait.
    # p = joint_probability(people, set(["Harry"]), set(["James"]), set({'James'}))
    for have_trait in powerset(names):
        # print("\nPowerset: ", have_trait)
        # Check if current set of people violates known information - returns true or false
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            # If trait was not found, skip this subset
            continue

        # Else, continue looping over for this subset
        print(f"Trait Found in subset: {have_trait} - Examining further..\n")
        
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
            #     update(probabilities, one_gene, two_genes, have_trait, p)
            print("\n")

    # # Ensure probabilities sum to 1
    # normalize(probabilities)

    # # Print results
    # for person in people:
    #     print(f"{person}:")
    #     for field in probabilities[person]:
    #         print(f"  {field.capitalize()}:")
    #         for value in probabilities[person][field]:
    #             p = probabilities[person][field][value]
    #             print(f"    {value}: {p:.4f}")


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
    # A powerset is the set of all possible subsets of a given set, including the empty set and the set itself.
    # If you have a set 𝑆 its powerset is denoted as 𝑃(𝑆). For example S={a,b} , P(S)={∅,{a},{b},{a,b}}
    # If a set has 𝑛 elements, its powerset contains 2^𝑛 subsets.
    # Powersets are important for counting all possible selections of elements.
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]



# TODO

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
    print("People: ", people)
    print("One Gene: ", one_gene)
    print("Two Genes: ", two_genes)
    print("Have Trait: ", have_trait)

    all_probs = []
    for person in people:
        # For anyone with no parents listed in the data set, 
        # use the probability distribution PROBS["gene"] 
        # to determine the probability that they have a particular number of the gene.
        if not people[person]["father"] and not people[person]["mother"]:
            print(f"'{person}' does not have parents listed.")
            print("Probability will be calculated based on PROBS['gene']")
            copies_count = 0
            copies_prob = 0
            if person in one_gene:
                copies_count = 1
                copies_prob = PROBS["gene"][1]
                print(f"{person} has 1 gene with 'p({copies_count})={copies_prob}'")
            if person in two_genes:
                copies_count = 2
                copies_prob = PROBS["gene"][2]
                print(f"{person} has 2 genes with 'p({copies_count})={copies_prob}'")
            if person not in one_gene and person not in two_genes:
                copies_count = 0
                copies_prob = PROBS["gene"][0]
                print(f"{person} has 0 genes with 'p({copies_count})={copies_prob}'")
            
            p_trait = 0   
            if person not in have_trait:
                p_trait = PROBS["trait"][copies_count][False]
                print(f"{person} does not have trait with 'p(no_trait)={p_trait}'")
            else:
                p_trait = PROBS["trait"][copies_count][True]
                print(f"{person} does not have trait with 'p(has_trait)={p_trait}'")
            
            # joint_p = round((p_trait * copies_prob), 4)
            joint_p = p_trait * copies_prob
            all_probs.append(joint_p)
            print(f"Joint Probability is: ", joint_p)


        # For anyone with parents in the data set,
        # each parent will pass one of their two genes on to their child randomly, 
        # and there is a PROBS["mutation"] chance that it mutates (goes from being the gene to not being the gene, or vice versa).
        else:
            father = people[person]["father"]
            mother = people[person]["mother"]
            parents = [father, mother]
            print(f"'{person}' has '{father}' and '{mother}' listed as parents.")
            print("PARENTS: ", father, mother)

            p = []
            for parent in parents:
                if parent in one_gene:
                    p.append({"prob": 0.5 - PROBS["mutation"], "copies": 1})
                    continue
                if parent in two_genes:
                    p.append({"prob": 1 - PROBS["mutation"], "copies": 2})
                else:
                    p.append({"prob": PROBS["mutation"], "copies": 0})

            
            # Calculate probabilities
            combine_p_of_parents = 0
            gene_count = None
            if person in one_gene:
                gene_count = 1
                combine_p_of_parents = p[0]["prob"] * (1 - p[1]["prob"]) + p[1]["prob"] * (1 - p[0]["prob"])
            elif person in two_genes:
                gene_count = 2
                combine_p_of_parents = p[0]["prob"] * p[1]["prob"]
            else:
                gene_count = 0
                combine_p_of_parents = (1 - p[0]["prob"]) * (1 - p[1]["prob"])
            
            # print(f"Combined Probability of Parents is: ", combine_p_of_parents)
            joint_p = 0
            p_trait = 0
            if person in have_trait:
                p_trait = PROBS["trait"][gene_count][True]
            else:
                p_trait = PROBS["trait"][gene_count][False]
            
            joint_p = combine_p_of_parents * p_trait
            all_probs.append(joint_p)


                
       
        # Use the probability distribution PROBS["trait"] to compute the probability that a person does or does not have a particular trait.

    print("all probs: ", all_probs)
    result = math.prod(all_probs)
    print("result: ", result, "\n\n")
    return result
        



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
