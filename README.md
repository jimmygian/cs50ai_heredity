# CS50AI | Lecture 2 - Uncertainty | Project 2B - [`Heredity`](https://cs50.harvard.edu/ai/2024/projects/2/heredity/)

This project is a mandatory assignment from **CS50AI – Lecture 2: "Uncertainty"**.

### 📌 Usage

To run the project locally, follow these steps:

1. **Clone the repository** to your local machine.

[TBC]

<br>

## Project Overview

### My Task

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

---

This structured approach ensures we correctly compute how likely a specific genetic and trait distribution is in the dataset.

## Conclusion
