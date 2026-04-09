# Scoring

## Scoring layers

RepoScale uses a multi-layer evaluation approach. Not every layer applies to every track.

### Layer 1: Structural validation
- Did the response follow the required format?
- Are all required sections present?
- Did the model distinguish evidence from hypothesis?

### Layer 2: Automatic heuristics
- Density of references to files, commits, and artifacts
- Genericity score (how recyclable is the response across repos?)
- Length and structural quality
- Presence of explicit prioritization

### Layer 3: LLM judge
- Evaluates semantic quality using a fixed rubric
- See `prompts/judge.md` for the protocol

### Layer 4: Execution validation
Applies to implementation tracks (Implement, Agent):
- Does it compile/run?
- Do tests pass?
- Were regressions introduced?
- Does the implementation align with the stated plan?

### Layer 5: Human review
Required for:
- Calibration of automated scoring
- Useful creativity assessment
- Ambiguous cases
- Leaderboard auditing

## Primary metrics

These should appear in scoring for most tracks:

| Metric | Description |
|--------|-------------|
| **Project understanding** | Depth and accuracy of structural comprehension |
| **Evidence grounding** | Ratio of claims backed by repo artifacts |
| **Intent reconstruction** | Quality of inferred original direction |
| **Gap detection** | Identification of missing, broken, or incomplete elements |
| **Useful creativity** | Quality and plausibility of proposed extensions |
| **Prioritization** | Quality of ordering by impact, effort, risk |
| **Architectural coherence** | Respect for existing structure and constraints |
| **Actionability** | How executable is the output? |

## Secondary metrics

| Metric | Description |
|--------|-------------|
| **Hallucination rate** | Claims about nonexistent files, functions, or features |
| **Genericity rate** | How applicable is the response to any random repo? |
| **Rewrite bias** | Tendency to suggest rewriting over evolving |
| **History sensitivity** | Use of commit history and temporal signals |
| **Run stability** | Consistency across multiple runs |
| **Agentic dependency** | Performance delta between prompt-only and tool modes |

## Agent-specific metrics

For `agentic_budgeted` and `full_continuation` modes:

| Metric | Description |
|--------|-------------|
| **Step count** | Number of actions taken |
| **Tool usage** | Which tools were used and how efficiently |
| **Files inspected** | Coverage of relevant context |
| **Diff quality** | Correctness and coherence of changes |
| **Tests passed** | Execution validation results |
| **Token budget** | Total cost of the run |
| **Plan-execution alignment** | Did execution match the stated plan? |
