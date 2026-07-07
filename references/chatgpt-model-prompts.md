# ChatGPT Model Prompts

Use these copyable prompts in No-API mode. The goal is to make ChatGPT's different models act as candidate generators, while Codex uses this skill as the judge and final editor.

## Candidate Generation Prompt

Give this prompt to the user when they have no API keys and no model candidates yet.

```text
You are an expert bilingual academic writing editor and research-paper translator.

Task:
Translate and polish the source text into five bilingual academic expression variants for a research paper.

Target field:
{{field_or_general}}

Target manuscript section:
{{section_or_unknown}}

Target venue/style, if any:
{{venue_or_none}}

Output exactly five versions:
1. Faithful
2. Native Academic
3. Concise
4. Strong Claim
5. Reviewer-Safe

For each version, provide:
- English
- Chinese counterpart
- Best for
- Risk note

Hard constraints:
- Preserve the original meaning, scope, uncertainty, terminology, and claim strength.
- Do not invent results, citations, datasets, numbers, mechanisms, limitations, or causal claims.
- Do not add unsupported novelty, superiority, generality, clinical relevance, policy relevance, or benchmark claims.
- Keep the English and Chinese versions aligned in meaning and confidence.
- If the source is ambiguous, preserve the ambiguity or state the conservative assumption in the risk note.

Source text:
<source_text>
{{source_text}}
</source_text>
```

## User Handoff Format

Ask the user to paste results back into Codex like this:

```text
Original:
{{source_text}}

Target use:
{{target_use_or_section}}

ChatGPT model A:
{{output_from_model_a}}

ChatGPT model B:
{{output_from_model_b}}

ChatGPT model C:
{{output_from_model_c}}
```

If the user knows the actual model names, keep them. If not, labels such as `model A`, `model B`, and `model C` are enough.

## Candidate Judging Prompt

Use this internally when the user pastes multiple model outputs. Do not ask the user to run this prompt unless they explicitly want a standalone judging prompt.

```text
You are judging multiple ChatGPT model outputs for academic translation and rewriting.

Original source:
<source_text>
{{source_text}}
</source_text>

Candidate outputs:
<candidate_outputs>
{{labeled_candidate_outputs}}
</candidate_outputs>

Evaluate each candidate using:
1. Fidelity to the original meaning, scope, uncertainty, and evidence level
2. Terminology consistency and field appropriateness
3. Academic naturalness
4. English-Chinese bilingual alignment
5. Claim control, especially avoiding unsupported novelty, causality, certainty, or superiority
6. Fit for the target manuscript section

Return:
1. A ranking table
2. Best base candidate
3. Rejected or risky wording with reasons
4. Reusable phrases from each candidate
5. Final fused bilingual version
6. Terminology notes

Do not prefer a candidate only because of the model name. Judge the text.
```

## Short Candidate Generation Prompt

Use this when the user wants a compact prompt:

```text
Translate and polish the following research text into five bilingual paper-style versions: Faithful, Native Academic, Concise, Strong Claim, and Reviewer-Safe. For each version, provide English, Chinese counterpart, best use case, and risk note. Preserve meaning, scope, uncertainty, terminology, and claim strength. Do not invent facts, results, citations, datasets, numbers, mechanisms, or causal claims.

Text:
{{source_text}}
```
