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
    # The goal here is to examine different possible trait distributions among the people.
    
    # p = joint_probability(people, set(["Harry"]), set(["James"]), set({'James'}))
    # update(probabilities, set(["Harry"]), set(["James"]), set({'James'}), 0.00123353453)
    # normalize({'Harry': {'gene': {2: 0.000292184739, 1: 0.014499220722, 0: 0.017026184539}, 'trait': {True: 0.00847974553006, False: 0.02333784446994001}}, 'James': {'gene': {2: 0.00628615, 1: 0.016247280000000003, 0: 0.009284159999999996}, 'trait': {True: 0.03181759000000002, False: 0}}, 'Lily': {'gene': {2: 0.00011515, 1: 0.0004342800000000001, 0: 0.031268159999999996}, 'trait': {True: 0, False: 0.03181759000000002}}})
    
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
        
        # print(f"Subset '{have_trait}' includes at least one person with the trait. - Examining further..\n")
    
        # Else, continue looping over for this subset
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
    # print("People: ", people)
    # print("One Gene: ", one_gene)
    # print("Two Genes: ", two_genes)
    # print("Have Trait: ", have_trait)

    all_probs = []
    
    for person in people:
        # Get person's gene count
        gene_count = 1 if person in one_gene else (2 if person in two_genes else 0)
        
        # If no parents listed in person, use base probability
        if not people[person]["father"] and not people[person]["mother"]:
            # print(f"'{person}' does not have parents listed.")
            # print("Probability will be calculated based on PROBS['gene']")
  
            copies_prob = PROBS["gene"][gene_count]
            # print(f"{person} has {gene_count} genes with p({gene_count})={copies_prob}")

        else:
            # Person has parents, calculate probability based on inheritance
            father, mother = people[person]["father"], people[person]["mother"]

            p_mother = 0.5 if mother in one_gene else (1 - PROBS["mutation"] if mother in two_genes else PROBS["mutation"])
            p_father = 0.5 if father in one_gene else (1 - PROBS["mutation"] if father in two_genes else PROBS["mutation"])

            if gene_count == 1:
                copies_prob = p_mother * (1 - p_father) + (1 - p_mother) * p_father
            elif gene_count == 2:
                copies_prob = p_mother * p_father
            else:
                copies_prob = (1 - p_mother) * (1 - p_father)

            # print(f"{person} inherits probability: {copies_prob}")

        # Compute trait probability
        if person in have_trait:
            p_trait = PROBS["trait"][gene_count][True]
        else:
            p_trait = PROBS["trait"][gene_count][False]
        # print(f"{person} {'has' if person in have_trait else 'does not have'} trait with p={p_trait}")

        # Compute joint probability
        joint_p = copies_prob * p_trait
        all_probs.append(joint_p)
        # print(f"Joint probability for {person}: {joint_p}\n")

    # Compute final joint probability
    result = math.prod(all_probs)
    # print("Final joint probability:", result, "\n\n")
    return result


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # The update function adds a new joint distribution probability 
    # to the existing probability distributions in `probabilities`.
    updated_probabilities = probabilities.copy()

    for person in probabilities:
        # Get gene count for person
        gene_count = 1 if person in one_gene else (2 if person in two_genes else 0)
        # print(f"{person} has {gene_count} genes.")

        # by adding `p` to the appropriate value in each distribution...
        # Update probabilities[person]["gene"] for person
        updated_probabilities[person]["gene"][gene_count] += p 

        # Update probabilities[person]["trait"] for person
        updated_probabilities[person]["trait"][person in have_trait] += p

    # print(updated_probabilities)
    probabilities = updated_probabilities


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    print(probabilities)
    # for every probability distribution
    # We need to do a( value_1 + value_2 + ... + value_n) = 1
    # a = 1 / ( value_1 + value_2 + ... + value_n)
    normalized_probabilities = probabilities.copy()
    for person in probabilities:
        # Normalize gene
        genes = probabilities[person]["gene"]
        traits = probabilities[person]["trait"]

        # Get normalization value (a)
        summation_genes = 0
        for gene in genes:
            summation_genes += genes[gene]
        aG = 1 / summation_genes

        summation_traits = 0
        for trait in traits:
            summation_traits += traits[trait]
        aT = 1 / summation_traits

        # Update probabilities
        for gene in genes:
            normalized_probabilities[person]["gene"][gene] = aG * genes[gene]
        for trait in traits:
            normalized_probabilities[person]["trait"][trait] = aG * traits[trait]
    
    probabilities = normalized_probabilities





if __name__ == "__main__":
    main()
