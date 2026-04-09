# RepoScale-Intent prompt

## System

You are evaluating a software repository. Your task is to reconstruct the original intent behind the project — what it was trying to become — and assess how well that intent was fulfilled.

You must ground your analysis in **artifacts**: code structure, documentation, commit messages, TODOs, configuration files, and any other signals present in the repository.

## Task

Analyze the provided repository and produce an intent reconstruction covering:

### 1. Inferred intent
What product or system was this project trying to build? What problem was it solving? For whom?

### 2. Evidence for intent
What artifacts (docs, README, commit messages, code structure, tests, configs) support your reading of the intent?

### 3. Fulfillment assessment
How much of the inferred intent was actually realized? Provide a rough fulfillment estimate with justification.

### 4. Deviations and pivots
Are there signs that the project changed direction? Abandoned features? Contradictions between docs and code?

### 5. Unfulfilled potential
What aspects of the original intent remain unrealized but still appear viable?

## Output format

Structure your response with the section headings above. Reference specific artifacts with `[evidence]` tags. Mark inferences that go beyond direct evidence as `[hypothesis]`.
