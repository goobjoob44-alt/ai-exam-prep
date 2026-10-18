# 🧠 Artificial Intelligence - Complete Exam Revision Guide & Syllabus Summary

---

## 📂 Overview of Course Files

| File Name | Primary Topic | Key Highlights |
| :--- | :--- | :--- |
| [**`1_Introduction_Agent.pdf`**](pdfs/1_Introduction_Agent.pdf) | Foundations & History of AI | Intelligence definitions, 4 dimensions of AI, 8 historical eras, Intelligent agent model |
| [**`2_Agent Architecture and environment.pdf`**](pdfs/2_Agent%20Architecture%20and%20environment.pdf) | Intelligent Agents & Environments | PEAS framework, 7 environment dimensions, 5 agent architectures |
| [**`4_ Informed Search Algorithms.pdf`**](pdfs/4_%20Informed%20Search%20Algorithms.pdf) | Informed / Heuristic Search | Heuristics $h(n)$, Admissibility, Consistency, Greedy Best-First Search, $A^*$ Search |
| [**`5_Memory Bounded Search.pdf`**](pdfs/5_Memory%20Bounded%20Search.pdf) | Memory-Bounded Search | Space bottlenecks of $A^*$, $\text{IDA}^*$, $\text{RBFS}$, $\text{MA}^*$, $\text{SMA}^*$ with memory bounds |
| [**`1_Knowledge_Representations.pdf`**](pdfs/1_Knowledge_Representations.pdf) | Knowledge Representation (KR) | DIKW pyramid, KR schemes, Semantic nets, Frames, Prolog, Logic programming, Forward vs. Backward chaining |
| [**`4_Logic.pdf`**](pdfs/4_Logic.pdf) | Logic, Proofs & Quantifiers | Propositional & Predicate logic, 8 propositional rules, 4 quantifier rules, 8 proof methods |
| [**`2_List-of-Rules-of-inference.pdf`**](pdfs/2_List-of-Rules-of-inference.pdf) | Rules of Inference Reference | 16 binary truth functions table, deduction theorem, formal inference derivations |
| [**`3_logic Formule.pdf`**](pdfs/3_logic%20Formule.pdf) | Quick Reference Formula Sheet | Summary table of Logical Equivalences and Propositional Rules of Inference |

---

## 📑 Detailed PDF-by-PDF Breakdown

### 1. `1_Introduction_Agent.pdf` — Foundations and History of AI
* **Instructor / Department:** Prof. Alok Choudhury, Dept. of CSE, SoT, ADBU.
* **Core Concepts:**
  * **DIKW Hierarchy:** Data (disconnected facts) $\to$ Information (contextualized facts) $\to$ Knowledge (patterns & understanding "how") $\to$ Wisdom / Intelligence (principles & understanding "why").
  * **Four Perspectives / Dimensions of AI:**
    1. *Thinking Humanly:* Cognitive modeling, introspective psychology.
    2. *Acting Humanly:* Turing Test approach (NLP, KR, automated reasoning, machine learning).
    3. *Thinking Rationally:* Laws of thought, syllogisms, formal logic.
    4. *Acting Rationally:* Rational agent approach (doing the right thing to achieve the best expected outcome).
  * **Multidisciplinary Foundations of AI:**
    * *Philosophy* (Logic, epistemology, mind-body connection)
    * *Mathematics* (Logic, probability, computation, undecidability, NP-completeness)
    * *Economics* (Decision theory, game theory, operations research)
    * *Neuroscience* (Biological neurons, brain functioning)
    * *Psychology* (Cognitive science, perception, behaviorism)
    * *Computer Engineering* (Hardware execution, parallel processing)
    * *Control Theory & Cybernetics* (Feedback loops, homeostatic systems)
    * *Linguistics* (Knowledge representation, natural language syntax & semantics)
  * **Milestones in AI History:**
    * *1943–1955:* Gestation (McCulloch-Pitts artificial neurons, Turing's "Computing Machinery and Intelligence").
    * *1956:* Birth of AI at the Dartmouth College Workshop (John McCarthy coins "Artificial Intelligence").
    * *1952–1969:* Early Enthusiasm (General Problem Solver, Newell & Simon, early neural nets).
    * *1966–1973:* Dose of Reality (Combinatorial explosion, Minsky & Papert Perceptrons critique, AI Winter I).
    * *1969–1979:* Knowledge-Based / Expert Systems (DENDRAL, MYCIN).
    * *1980–present:* AI Industry & Expert Systems boom.
    * *1986–present:* Neural Network renaissance (Backpropagation, Rumelhart & Hinton).
    * *Modern AI:* Probabilistic reasoning, big data, deep learning, foundation models.

---

### 2. `2_Agent Architecture and environment.pdf` — Intelligent Agents & Environments
* **Instructor / Department:** Prof. Alok Choudhury, Dept. of CSE, SoT, ADBU.
* **Definition of an Agent:**
  $$\text{Agent} = \text{Architecture} + \text{Program}$$
  An agent perceives its environment through **Sensors** and acts upon it through **Actuators**.
* **PEAS Framework:**
  * **P**erformance measure: Success metric.
  * **E**nvironment: External world/context.
  * **A**ctuators: Mechanisms to take actions.
  * **S**ensors: Devices/inputs providing percepts.
  * *Standard Exam Case Studies:* Automated Taxi Driver, Medical Diagnosis Agent, Satellite Analysis System, Part-picking Assembly Robot.
* **Environment Characteristics (Dimensions):**
  1. **Fully Observable vs. Partially Observable:** Complete state access vs. sensory limitations / noise.
  2. **Deterministic vs. Stochastic (vs. Strategic):** Next state strictly fixed by current state + action vs. probabilistic / multi-agent actions.
  3. **Episodic vs. Sequential:** Current action has no effect on future episodes vs. current decisions impact future choices.
  4. **Static vs. Dynamic (vs. Semi-dynamic):** Environment doesn't change during deliberation vs. changes constantly (semi-dynamic: environment static but time-score decays).
  5. **Discrete vs. Continuous:** Countable distinct states/percepts/actions vs. continuous real-valued parameters.
  6. **Single-Agent vs. Multi-Agent:** Solo agent vs. competitive/cooperative interactions.
  7. **Known vs. Unknown:** Known physics/rules of environment vs. agent must explore and learn.
* **The 5 Agent Architectures:**
  1. **Simple Reflex Agent:** Direct lookup `condition -> action` based purely on current percept.
  2. **Model-Based Reflex Agent:** Maintains internal state estimating unobserved aspects of the world.
  3. **Goal-Based Agent:** Uses goal states to evaluate which sequence of actions achieves desired outcomes.
  4. **Utility-Based Agent:** Evaluates states via a continuous utility function (maximizes trade-offs, satisfaction, speed vs. safety).
  5. **Learning Agent:** Separated into *Learning Element*, *Performance Element*, *Critic*, and *Problem Generator*.

---

### 3. `4_ Informed Search Algorithms.pdf` — Heuristic Search & $A^*$
* **Heuristics ($h(n)$):**
  * An informed estimate of the cheapest path cost from node $n$ to the goal.
  * Formulated using problem relaxations (solving a simplified problem).
* **Properties of Heuristic Functions:**
  * **Admissibility:** $0 \le h(n) \le h^*(n)$ (never overestimates the true cost to reach the goal).
  * **Consistency (Monotonicity):** $h(n) \le c(n, a, n') + h(n')$ (triangle inequality). Guaranteed admissibility if consistent.
* **Best-First Search:**
  * Node selection based on evaluation function $f(n)$ using a priority queue.
* **Greedy Best-First Search:**
  * $f(n) = h(n)$.
  * Always expands the node that appears closest to the goal.
  * *Properties:* Incomplete (can get trapped in loops), Non-optimal, Time complexity $O(b^m)$, Space complexity $O(b^m)$.
* **$A^*$ Search Algorithm:**
  * Evaluation function:
    $$f(n) = g(n) + h(n)$$
    * $g(n)$: Exact path cost accumulated from the start node to $n$.
    * $h(n)$: Estimated heuristic cost from $n$ to the goal.
  * *Optimality:* $A^*$ is optimal with tree search if $h(n)$ is admissible, and optimal with graph search if $h(n)$ is consistent.
  * *Contours:* Expands outwards along concentric contours of monotonically increasing $f$-cost.
  * *Critical Limitation:* **Space Complexity** $O(b^d)$ — memory gets exhausted long before compute time runs out!

---

### 4. `5_Memory Bounded Search.pdf` — Memory-Bounded Heuristic Search
* **Objective:** Solve the $O(b^d)$ space bottleneck of $A^*$ without sacrificing optimality or completeness.
* **Core Algorithms:**
  1. **$\text{IDA}^*$ (Iterative Deepening $A^*$):**
     * Analogous to Iterative Deepening DFS, but cutoff uses $f\text{-limit}$ instead of depth.
     * Each iteration performs DFS over nodes with $f(n) \le f\text{-limit}$.
     * Next limit = smallest $f(n)$ that exceeded the previous limit.
     * *Space Complexity:* $O(b \cdot d)$ (linear!).
     * *Time Complexity:* $O(b^d)$; worst case with fine-grained real costs expands up to $O(N^2)$ nodes.
     * *Drawback:* "Uses too little memory" — does not store past search history between iterations.
  2. **$\text{RBFS}$ (Recursive Best-First Search):**
     * Linear space $O(b \cdot d)$ algorithm that mimics Best-First search.
     * Maintains $f\text{-limit}$ corresponding to the best alternative path available at any ancestor.
     * If current child $f > f\text{-limit}$, backtracks and replaces parent's $f$-value with the best forgotten child value.
     * *Properties:* Complete, optimal with admissible $h(n)$, but can suffer from frequent "mind-changes" (thrashing).
  3. **$\text{SMA}^*$ (Simplified Memory-Bounded $A^*$):**
     * Uses **all** available memory buffer $M$.
     * Expands newest best leaf node.
     * When memory is full: drops the **shallowest, highest $f$-cost (oldest worst)** node from memory.
     * Backs up the dropped node's $f$-value into its parent.
     * If all other branches look worse, parent can regenerate the dropped node.
     * *Completeness:* Guaranteed if memory size $M \ge d$ (shallowest goal depth).
     * *Optimality:* Guaranteed if memory size $M \ge d^*$ (optimal path fits in memory).

---

### 5. `1_Knowledge_Representations.pdf` — Knowledge Representation, Logic & Rules
* **Author / Reference:** RC Chakraborty (`myreaders.info`), Lectures 15–22 (79 slides).
* **Core Topics:**
  * **Nature of Knowledge:**
    * *Tacit Knowledge:* Informal, embodied, difficult to articulate, derived from experience/insight.
    * *Explicit Knowledge:* Formal, embedded, easy to articulate, communicate, and codify.
    * *Declarative Knowledge ("Knowing That"):* Describing facts, axioms, states, relationships.
    * *Procedural Knowledge ("Knowing How"):* Step-by-step algorithms, instructions, rules of execution.
  * **Knowledge Representation (KR) System Requirements:**
    1. *Representational Adequacy:* Ability to capture all required domain knowledge.
    2. *Inferential Adequacy:* Ability to manipulate representations to derive new knowledge.
    3. *Inferential Efficiency:* Ability to focus inferencing in the most promising directions.
    4. *Acquisitional Efficiency:* Ease of adding new knowledge (automatic vs. human).
  * **KR Schemes:**
    * *Relational Knowledge:* Relational tables of entities and attributes.
    * *Inheritable Knowledge:* Semantic Networks and Frames (slots and fillers).
      * `IsA` link: Class inclusion (subset relation).
      * `Instance` link: Class membership (element relation).
      * Property inheritance algorithm.
    * *Inferential Knowledge:* Predicate logic deduction.
    * *Declarative vs. Procedural Knowledge:* Comparative analysis (SQL vs. procedural C++).
  * **KR Using Predicate Logic:**
    * Constants, Variables, Functions, Predicates.
    * Quantifiers: Universal ($\forall x$) & Existential ($\exists x$), Universe of Discourse.
    * Well-Formed Formulas (WFF), Atomic Formulas.
    * Representing computable functions (recursive factorial, triangular functions).
    * Resolution Refutation Principle in Logic.
  * **Production Systems & Rules:**
    * Rule structure: `IF <condition> THEN <action>`
    * Rule types: Knowledge Declarative Rules, Inference Procedural Rules, Meta-rules.
    * Architecture: Working Memory + Rule Base + Inference Engine.
    * **Forward Chaining (Data-Driven):** Starts from facts in working memory $\to$ fires matching rules $\to$ derives conclusions.
      * *Conflict Set:* Rules whose conditions match current facts.
      * *Conflict Resolution Strategies:*
        1. **Refractory:** A rule cannot fire twice on the same data (prevents loops).
        2. **Recency:** Prefer rules matching newly added facts (time-tags).
        3. **Specificity:** Prefer rules with more specific conditions.
    * **Backward Chaining (Goal-Driven):** Starts with hypothesis/goal $\to$ works backward to establish required sub-goals and premises.
    * **Comparison:** Forward Chaining suits design/synthesis; Backward Chaining suits diagnosis/expert consultation (e.g., MYCIN).
    * **Logic Programming (Prolog):**
      * Syntax: Atoms, numbers, variables (uppercase), compound terms (`functor(args)` with arity).
      * Program clauses: Facts (unit clauses `father(X,Y).`), Rules (`head :- body.`), Queries (`?- goal.`).
      * Equation: $\text{Algorithm} = \text{Logic} + \text{Control}$.

---

### 6. `4_Logic.pdf`, `2_List-of-Rules-of-inference.pdf`, & `3_logic Formule.pdf` — Logic, Formulas & Proofs
* **Propositional Logic Foundations:**
  * Declarative statements with binary truth values ($\text{True} = 1$, $\text{False} = 0$).
  * Precedence: $\neg > \land > \lor > \to > \leftrightarrow$.
  * Tautologies (always True), Contradictions (always False), Contingencies (neither).
  * Complete 16 Binary Truth Functions Table (NOR, NAND, XOR, XNOR, Implication, Converse, etc.).
* **Key Logical Equivalences:**
  * **De Morgan’s Laws:** $\neg(p \land q) \equiv \neg p \lor \neg q$, $\neg(p \lor q) \equiv \neg p \land \neg q$
  * **Conditional Equivalence:** $(p \to q) \equiv (\neg p \lor q)$
  * **Contrapositive Equivalence:** $(p \to q) \equiv (\neg q \to \neg p)$
  * **Distributive Laws:** $p \land (q \lor r) \equiv (p \land q) \lor (p \land r)$
  * **Absorption Laws:** $p \lor (p \land q) \equiv p$
* **Rules of Inference (Propositional Logic):**
  1. **Modus Ponens:** $[p \land (p \to q)] \vdash q$
  2. **Modus Tollens:** $[\neg q \land (p \to q)] \vdash \neg p$
  3. **Hypothetical Syllogism:** $[(p \to q) \land (q \to r)] \vdash (p \to r)$
  4. **Disjunctive Syllogism:** $[(p \lor q) \land \neg p] \vdash q$
  5. **Addition:** $p \vdash (p \lor q)$
  6. **Simplification:** $(p \land q) \vdash p$
  7. **Conjunction:** $p, q \vdash (p \land q)$
  8. **Resolution:** $[(p \lor q) \land (\neg p \lor r)] \vdash (q \lor r)$
* **Rules of Inference for Quantified Statements:**
  1. **Universal Instantiation (UI):** $\forall x P(x) \vdash P(c)$ (for any $c$).
  2. **Universal Generalization (UG):** $P(c)$ for arbitrary $c \vdash \forall x P(x)$.
  3. **Existential Instantiation (EI):** $\exists x P(x) \vdash P(c)$ (for some specific element $c$).
  4. **Existential Generalization (EG):** $P(c)$ for some element $c \vdash \exists x P(x)$.
  5. **Universal Modus Ponens:** $\forall x (P(x) \to Q(x)), P(a) \vdash Q(a)$.
* **Mathematical Proof Techniques:**
  1. **Direct Proof:** Assume $p$ is true $\to$ deduce $q$ using definitions and axioms (e.g., $n$ is odd $\implies n^2$ is odd).
  2. **Proof by Contraposition:** Assume $\neg q$ is true $\to$ deduce $\neg p$.
  3. **Proof by Contradiction (*Reductio ad absurdum*):** Assume $\neg p \to$ deduce contradiction $F$ (e.g., $\sqrt{2}$ is irrational; infinitude of primes).
  4. **Proof by Cases:** Break domain into exhaustive cases $(p_1 \lor \dots \lor p_n) \to q$.
  5. **Without Loss of Generality (WLOG):** Exploit symmetry in variables.
  6. **Constructive Existence Proof:** Find a concrete witness $c$ satisfying $P(c)$ (e.g., Ramanujan taxicab number $1729 = 10^3 + 9^3 = 12^3 + 1^3$).
  7. **Non-constructive Existence Proof:** Prove existence via contradiction without explicitly naming the entity (e.g., irrational $x, y$ such that $x^y$ is rational).
  8. **Uniqueness Proof:** Prove existence $P(x)$, then assume $P(y) \implies y = x$.
  9. **Counterexamples:** Disprove $\forall x P(x)$ by identifying a single case where $P(c)$ fails.

---

## 🎯 High-Yield Exam Preparation Checklist

- [ ] **Distinguish Uninformed vs. Informed Search:** Be ready to write the cost functions: $f(n) = g(n)$ (Uniform Cost), $f(n) = h(n)$ (Greedy), $f(n) = g(n) + h(n)$ ($A^*$).
- [ ] **Heuristic Properties:** State the exact formulas for Admissibility and Consistency. Remember: Consistency $\implies$ Admissibility, but the converse is not always true.
- [ ] **Memory-Bounded Search:** Contrast $\text{IDA}^*$ (too little memory) vs. $\text{SMA}^*$ (uses all memory buffer $M$ and drops shallowest highest-$f$ leaf).
- [ ] **PEAS Table:** Practice drawing the PEAS matrix for an Autonomous Taxi, Medical Diagnostician, and Vacuum Robot.
- [ ] **Agent Architectures:** Diagram the 5 types of agents from memory.
- [ ] **Logic Proofs:** Solve the Socrates syllogism and the Weather/Canoe trip deduction step-by-step using named inference rules.
- [ ] **Forward vs. Backward Chaining:** Compare algorithm direction, working memory usage, and conflict resolution (Refractory, Recency, Specificity).
- [ ] **Prolog Syntax:** Differentiate facts, rules, and compound terms (`head :- body.`).
