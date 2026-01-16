# Background
This is a 90 mins Python coding exercise that would describe a problem in 4 levels. Each level would add more requirements.

# Goal
Implement Python to fully address all problems in each level within 90 mins.
For each level, you should output the corresponding implementation, because it is more realistic in real life.

During implementation, these are things ranking by importance:
1. Shorter implementation with minimal changes per level
2. Readability: pay attention to the function name and necessary concise comment

# Requirement
1. You don't know and can't predict next level's new requirements
2. You shouldn't reimplement for each level. Instead, you should try to reuse existing implementation and make minimum change if possible


# Strategy for Assessments

1.  **Don't over-engineer Level 1:** Solve the first level quickly, but keep your code clean.
2.  **Refactor early:** When Level 2 introduces a new constraint, do not be afraid to rip out a chunk of Level 1 code to make a helper function or a class. The test measures your ability to reorganize code.
3.  **Data Structures:** You will almost certainly need Hash Maps (Dictionaries) to store state by ID, and potentially Priority Queues or Sorted Sets for ordering data.


# Technical Checklist
Before the test, ensure you can implement the following in your preferred language without looking up syntax:

1.  **Hash Maps / Dictionaries:** Accessing keys, checking existence, iterating over keys.
2.  **Priority Queues / Heaps:** Custom comparators (e.g., sorting orders by Price DESC, then Time ASC).
3.  **String Parsing:** Splitting strings by space or comma, converting String to Integer/Float.
4.  **Class Design:** Don't write everything in one function. Create a `Database` class or an `OrderBook` class.