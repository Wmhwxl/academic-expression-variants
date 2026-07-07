# Version Types

Use only the versions that fit the user's request. Default to the first five when no preference is given. Unless the user asks otherwise, every version should include both manuscript-ready English and an aligned polished Chinese counterpart.

## Default Versions

| Version | Use when | Style target |
|---|---|---|
| `faithful` | The user needs accurate translation or conservative polishing. | Minimal meaning movement, correct grammar, stable terminology. |
| `native` | The user asks for natural, idiomatic, paper-like expression. | Fluent academic prose with better information flow. |
| `concise` | The text is for abstract, title-like sentence, caption, contribution, or response summary. | Shorter and denser without losing meaning. |
| `strong` | The user needs a contribution or introduction sentence with clearer force. | Confident but evidence-bounded. |
| `reviewer_safe` | The text may be scrutinized by reviewers or contains uncertain claims. | Cautious, defensible, limitation-aware. |

## Optional Versions

| Version | Use when | Style target |
|---|---|---|
| `journal_style` | The user names a journal, venue, or family such as Nature, Cell, IEEE, NeurIPS, ICML, SSCI. | Adjusted rhetorical density and framing. |
| `method_precise` | The text describes a method, algorithm, protocol, or experimental setup. | Procedural clarity, reproducibility, and exact scope. |
| `result_neutral` | The text reports findings. | Clear result statement without inflated interpretation. |
| `discussion_balanced` | The text interprets implications or limitations. | Balanced significance, boundary conditions, and caution. |
| `rebuttal` | The text is for reviewer response. | Respectful, direct, evidence-centered, non-defensive. |
| `chinese_polished` | The user wants Chinese scholarly output as the main deliverable rather than only a Chinese counterpart. | Natural Chinese academic prose, not English-shaped translation. |

## Selection Rules

- For one sentence, keep each variant to one sentence unless the user asks for expansion.
- For one paragraph, keep paragraph structure unless reflowing improves clarity.
- For bilingual output, keep English and Chinese paired by version; do not put all English versions first and all Chinese versions later.
- For abstracts, preserve the common move order if present: problem, gap, method, result, implication.
- For contribution statements, prefer explicit subject-verb structure and avoid vague verbs such as "explore" unless the work is exploratory.
- For titles, do not output full-sentence variants unless requested.
