# Inference_Agent_Using_Resolution
This is an inference engine that for a given Knowledge Base and some queries, infers if the queries are True or False 
backed by the facts in the knowledge base.

Problem Format:



Query format: Each query will be a single literal of the form Predicate(Constant_Arguments) or ~Predicate(Constant_Arguments) and will not contain any variables. Each predicate will have between 1 and 25 constant arguments. Two or more arguments will be separated by commas.



KB format: Each sentence in the knowledge base is written in one of the following forms:
1) An implication of the form p1 ∧ p2 ∧ ... ∧ pm ⇒ q, where its premise is a conjunction of literals and its conclusion is a single literal. Remember that a literal is an atomic sentence
or a negated atomic sentence.
2) A single literal: q or ~q



Note:
1. & denotes the conjunction operator.
2. | denotes the disjunction operator. 
3. => denotes the implication operator.
4. ~ denotes the negation operator.
5. No other operators besides &, =>, and ~ are used in the knowledge base.
6. There will be no parentheses in the KB except as used to denote arguments of predicates.
7. Variables are denoted by a single lowercase letter.
8. All predicates and constants are case sensitive alphabetical strings that begin with uppercase letters.
9. Each predicate takes at least one argument. Predicates will take at most 25 arguments. A given predicate name will not appear with different number of arguments.
