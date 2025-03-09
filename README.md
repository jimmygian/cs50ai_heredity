
# CS50AI | Lecture 2 - Uncertainty | Project 2B - [Heredity](https://cs50.harvard.edu/ai/2024/projects/2/heredity/)

This project is a mandatory assignment from **CS50AI – Lecture 2: "Uncertainty"**. It involves computing the joint probability of specific genetic and trait configurations within a family dataset, using concepts from probability, genetics, and inheritance.

---

## 📌 Usage

To run the project locally, follow these steps:

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-username/heredity.git
   cd heredity
   ```

2. **Run the Project**  
   Execute the program using Python:
   ```bash
   python heredity.py data.csv
   ```

3. **View the Results**  
   The program outputs each person's probability distributions for gene copies and trait expression, ensuring that the probabilities are normalized (i.e., they sum to 1).

<br>

## Project Overview

In this project, the goal is to determine the likelihood of various genetic and trait configurations across a family tree. By considering both the inheritance rules (including mutation probabilities) and the observed traits, the program calculates the overall joint probability of a given scenario. The problem requires iterating over all possible combinations of gene and trait assignments and then summing the probabilities that match known evidence.

---

## My Task

- **Implement Core Functions:**  
  I implemented the key functions to calculate joint probabilities, update probability distributions, and normalize the final results.
  
- **Handling Genetic Inheritance:**  
  I ensured that the implementation correctly factors in the genetic contributions from both parents, incorporating the mutation rate.

- **Validation Against Known Data:**  
  The program validates configurations against provided evidence (whether an individual is known to have or not have the trait), skipping inconsistent scenarios.

---

## Implementation Explanation

### Explaining `joint_probability()`

This function `joint_probability(people, one_gene, two_genes, have_trait)` is calculating the probability of a specific genetic and trait configuration for a given set of people. Essentially, it's trying to answer:

    "What is the probability that everyone in the dataset has exactly the genes and traits as specified?"

This is done by combining **genetic inheritance probabilities** and **trait probabilities** for all individuals, based on the given arguments.


**Example**:

> ```python
> joint_probability(people, one_gene={"Harry"}, two_genes={"James"}, have_trait={"Lilly"})
> ```
> This means we calculate the probability that:
> - **Harry** has 1 gene.
> - **James** has 2 genes.
> - **Lily** has the trait (regardless of genes).
> - Everyone else has **0 genes** and **does not have the trait**.

---
<br>

**How It Works**

The function computes probabilities separately for each person:

#### **1. Individual Probability Formula**
For each person:

> **P(Person) = P(Gene Count) × P(Trait | Gene Count)**

How we determine `P(Gene Count)` depends on whether the person has listed parents.

<br>

#### **2. Gene Probability Calculation**
- **Case 1: No Parents (Base Probability)**  
  If the person has no parents listed, their probability is taken directly from `PROBS["gene"]`.

- **Case 2: Has Parents (Inheritance Rules)**  
  If the person has parents, their gene probability depends on inheritance.

Each parent can pass the gene with a certain probability:
(MUTATION: _P = 0.01_)

- **0 copies:** Passes the gene **only by mutation** → _P = 0.01_
- **1 copy:** Passes the gene **50% of the time** → _P = 0.5_
- **2 copies:** Passes the gene **almost always** → _P = 0.99_

For a child, the probability of having a specific gene count is:

- **P(0 genes)** = (1 - P_mother) × (1 - P_father)
- **P(1 gene)** = P_mother × (1 - P_father) + (1 - P_mother) × P_father
- **P(2 genes)** = P_mother × P_father

<br>

#### **3. Final Joint Probability Calculation**
Once we compute probabilities for all individuals, we multiply them together:

**P(Total) = P(Harry) × P(James) × P(Lily)**

This gives the final joint probability of the entire configuration.

This structured approach ensures we correctly compute how likely a specific genetic and trait distribution is in the dataset.

---

### Other Key Functions

- **`update(probabilities, one_gene, two_genes, have_trait, p)`**  
  This function adds the joint probability `p` to the running totals for each individual's gene and trait distributions. It ensures that every possible configuration contributes correctly to the overall probability calculations.

- **`normalize(probabilities)`**  
  After aggregating probabilities across all configurations, this function normalizes the distributions so that the probabilities for gene counts and trait presence for each individual sum to 1. This step is crucial for maintaining valid probability distributions.

---

## Conclusion

This project combines fundamental concepts of genetics and probability to compute the likelihood of various inheritance scenarios. By iterating over all possible configurations and carefully incorporating both base and conditional probabilities (including mutation effects), the implementation provides an accurate model for predicting genetic traits within a family.

For any questions or further discussion, please refer to the [CS50AI Heredity Project page](https://cs50.harvard.edu/ai/2024/projects/2/heredity/).

