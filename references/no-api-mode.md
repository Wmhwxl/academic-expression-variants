# No-API Mode

Use this mode when the user has no model API keys but still wants multiple-model selection.

## Default Rule

Without API access, use ChatGPT's different models to generate multiple candidates, then use the skill rubric to judge the results.

This means:

1. The user runs the same source text and prompt in several ChatGPT models through the ChatGPT UI or another non-API interface.
2. The user pastes the labeled outputs back into Codex.
3. Codex evaluates the candidates with `style-rubric.md`.
4. Codex ranks candidates, identifies reusable phrases, rejects unsafe wording, and produces a final bilingual version.

Do not claim to have called different ChatGPT models unless their outputs are provided by the user or an actual API/tool call was made.

## When Candidates Are Not Yet Supplied

Read `chatgpt-model-prompts.md` and give the user the **Candidate Generation Prompt**. Tell them to paste the same prompt into different ChatGPT models, then return with the labeled outputs.

## When Candidates Are Supplied

Read `chatgpt-model-prompts.md` only if the user needs the handoff format. Otherwise, evaluate directly:

1. Extract candidate versions and normalize them into comparable rows.
2. Score each candidate on:
   - fidelity
   - terminology
   - academic naturalness
   - bilingual alignment
   - claim control
   - fit for the target section
3. Prefer candidates that preserve uncertainty and avoid unsupported novelty or causality.
4. Merge only phrases that are semantically compatible.
5. Output:
   - ranking table
   - best candidate
   - rejected wording and reasons
   - final fused bilingual version
   - terminology notes

## Judging Output Format

```text
| Rank | Source model | Verdict | Strengths | Problems | Use decision |
|---|---|---|---|---|---|
| 1 | ChatGPT model B | Best base | ... | ... | Use as base |

Final fused version:
English: ...
Chinese counterpart: ...

Why this version:
- ...

Avoid:
- ...
```
