---
description: [Deep Anti-Hallucination & Deterministic Grounding Protocol]
---

# Deep Anti-Hallucination Audit

This workflow transforms the engine into a "Zero-Knowledge Prover" by enforcing strict grounding, Factored CoVe, and adversarial XML sandboxing.

## Phase 1: Grounding & Evidence (The Zero-Inference Rule)
- **Zero-Inference**: Do not guess. Cite specific script IDs or historical years.
- **Verification**: If a result violates binary logic, discard it immediately.

## Phase 2: Factored Chain-of-Verification (CoVe)
1. **The Draft**: Generate the most probable result.
2. **Question Planning**: Create 5 skeptic questions testing the draft.
3. **Blind Execution**: Answer questions using only raw data lookups (independent of the draft).
4. **Final Revision**: Revision MUST match the draft 100%, or output "INCONSISTENCY DETECTED."

## Phase 3: Adversarial Logic Debate (Agent A vs Agent B)
- **Agent A (The Statistician)**: Attempts to prove "Overfitting" (p > 0.05).
- **Agent B (The Pattern Architect)**: Proves result using Tamil Phonetic and Lo Shu.
- Result must survive a 3-turn debate.

## Phase 4: Deterministic Anchor (XML Sandboxing)
Restrict the engine to a `<Context_Constraint>` sandbox using only uploaded scripts and datasets. Cite exact **Line Numbers** for every logic point.
