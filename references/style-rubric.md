# Style Rubric

Use this rubric to review generated variants. For multi-model outputs, score each candidate from 1 to 5 and keep the best non-overlapping versions.

## Scoring

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Fidelity | Preserves claim, scope, uncertainty, and relations. | Minor phrasing drift but recoverable. | Changes meaning, evidence, or relation. |
| Terminology | Terms are consistent and field-appropriate. | Mostly correct but some generic wording. | Uses wrong or unstable technical terms. |
| Academic naturalness | Sounds like fluent scholarly prose. | Understandable but slightly stiff or generic. | Translationese, promotional, or awkward. |
| Bilingual alignment | English and Chinese match in meaning, scope, uncertainty, and claim strength. | Minor differences but no major factual drift. | One language adds, omits, or strengthens claims. |
| Precision | Clear agents, objects, mechanisms, and boundaries. | Some vague references or overloaded clauses. | Ambiguous or misleading. |
| Claim control | No unsupported strengthening. | Slightly stronger than source but not dangerous. | Adds causality, novelty, superiority, or universality. |
| Version fit | Clearly matches the version purpose. | Partially matches. | Same as another version or wrong rhetorical mode. |

## Red Flags

Reject or revise any variant that:

- Adds "first", "novel", "state-of-the-art", "significant", "robust", "comprehensive", or "causal" without support.
- Converts "may", "can", "suggest", "is associated with" into "does", "proves", "leads to", or "causes".
- Introduces unprovided quantitative changes, p-values, benchmarks, datasets, sample sizes, or application domains.
- Turns a method description into a result claim.
- Makes reviewer-facing text defensive, emotional, or dismissive.
- Replaces a precise technical term with a broader popular term.
- Lets the Chinese counterpart explain more than the English version, or lets the English version claim more than the Chinese source.

## Preferred Moves

- Put the main claim in the main clause.
- Use active voice when it clarifies agency.
- Use hedging deliberately: "may", "can", "suggests", "is consistent with", "under these conditions".
- Prefer field-standard verbs: "estimate", "derive", "evaluate", "demonstrate", "characterize", "quantify", "validate", "ablate", "benchmark".
- Remove empty intensifiers such as "very", "extremely", "remarkably", and "highly" unless the source justifies them.
- Preserve contrastive logic: "whereas", "while", "in contrast", "however", and "although" often carry the author's argument structure.
- Prefer exact relational language: "improves over", "is associated with", "is consistent with", "reduces", "predicts", "estimates", "enables", or "requires" only when supported.
- Turn vague academic filler into testable statements. Avoid "it is meaningful to", "plays an important role", and "has great significance" unless the concrete significance is stated.

## Diagnostic Questions

Ask these briefly before or during revision when the source is complex:

- What is the sentence doing: background, gap, method, result, interpretation, limitation, or rebuttal?
- What terms must not change?
- What uncertainty must be preserved?
- What evidence boundary prevents a stronger claim?
- Do the English and Chinese variants carry the same level of confidence?
- What reader objection is most likely?

## Revision Operators

Use these operators to improve prose without changing facts:

- **De-stack nouns**: Convert long noun chains into clearer prepositional or relative clauses.
- **Promote the claim**: Move the main finding or method action into the main clause.
- **Tighten scope**: Add "in this setting", "under these conditions", or "for this class of..." only when the source implies that boundary.
- **Align verbs**: Match verbs to evidence type: "observe" for empirical observation, "estimate" for statistical inference, "show" for demonstrated result, "suggest" for tentative interpretation.
- **Remove meta-commentary**: Delete "this paper mainly studies" when a direct action sentence is better.

## Final Recommendation

Recommend the version with the best balance for the user's likely context:

- Abstract or caption: concise.
- Introduction or contribution: native or strong.
- Method: faithful or method_precise.
- Results: result_neutral.
- Discussion or limitation: reviewer_safe or discussion_balanced.
- Rebuttal: rebuttal or reviewer_safe.
