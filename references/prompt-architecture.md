# Prompt Architecture

This skill uses a source-informed prompt architecture distilled from public prompt-engineering and academic-writing prompt repositories. Do not copy external prompt text into user outputs. Use these patterns to build robust prompts for scholarly translation and rewriting.

## Design Patterns

Use these patterns when the task is complex or multi-model:

1. **Role and scope separation**: Put stable professional identity and hard constraints in the system prompt; put source text, field, venue, section, and requested variants in the user prompt.
2. **Delimited source text**: Wrap the user's source text in explicit markers so the model does not confuse instructions with content.
3. **Terminology lock**: Extract key terms, named methods, datasets, metrics, variables, and hedges before rewriting. Preserve them unless a better field-standard equivalent is needed.
4. **Meaning diagnosis first**: Identify the claim type before generating variants: background, gap, method, result, limitation, implication, or rebuttal.
5. **Version-specific objectives**: Make each version optimize a different rhetorical purpose. Do not let all variants collapse into minor synonym changes.
6. **Structured output**: Use JSON for API aggregation and Markdown tables for final human-facing answers.
7. **Self-audit pass**: Require each variant to pass fidelity, terminology, academic naturalness, and overclaiming checks.
8. **Adversarial reviewer pass**: For strong, journal-style, or rebuttal wording, check how a skeptical reviewer could object.
9. **No hidden chain-of-thought**: Ask for concise diagnostics and decisions, not full private reasoning.

## Professional Pipeline

For high-quality results, run this pipeline mentally or through prompts:

```text
Stage 1: Parse
- Determine source language and target language.
- Identify manuscript section and field.
- Extract claim type, technical terms, variables, hedges, and evidence boundaries.

Stage 2: Generate
- Produce the requested variants using version-specific objectives.
- Keep factual content fixed.
- Preserve or explicitly handle ambiguity.

Stage 3: Audit
- Compare each variant against the original.
- Flag meaning drift, overclaiming, terminology risk, and awkward phrasing.
- Revise failed variants.

Stage 4: Curate
- Remove duplicate variants.
- Recommend the version best suited to the user's likely use case.
- Provide concise terminology or phrase notes.
```

## Prompt Composition Template

```text
SYSTEM:
You are a bilingual academic writing editor. Preserve meaning, scope, uncertainty, evidence level, and technical terminology. Do not invent facts.

USER:
Task: {{translation | rewriting | polishing | multi-version generation}}
Field: {{field}}
Section: {{section}}
Target style: {{style_or_venue}}
Output language: {{language}}
Versions: {{versions}}

Source text between <source_text> tags:
<source_text>
{{input_text}}
</source_text>

Before writing, silently identify:
- claim type
- locked terminology
- evidence boundaries
- hedges and uncertainty
- possible ambiguity

Return:
- variants table or JSON
- recommended version
- concise notes
```

## Multi-Model Prompting

When calling several providers, keep the prompt identical across providers except for model-specific compatibility settings. Require the same JSON schema from every provider. Judge outputs after generation instead of letting each provider choose its own criteria.

Use low to moderate temperature:

- `0.1-0.3` for faithful translation, terminology-sensitive text, methods, results, and rebuttal.
- `0.3-0.5` for native academic prose and journal-style variants.
- Avoid high temperature for scientific claims.

## No-API Multi-Model Judging

If no APIs are configured, use ChatGPT's different models as manual candidate generators. The user should run the same prompt in each ChatGPT model, paste labeled outputs back, and let this skill judge them with the same rubric used for API results.

Keep the judging step separate from generation:

- Do not treat model identity as proof of quality.
- Prefer the candidate with the best fidelity and claim control.
- Fuse wording only when it preserves the source meaning in both English and Chinese.
- Mark rejected phrases when they overstate novelty, causality, certainty, or generality.

## Source-Informed Takeaways

Public GitHub prompt resources commonly emphasize:

- academic prompt banks organized by task such as language polishing, translation, abstract, titles, literature review, and feedback;
- splitting long text into chunks and applying a final synthesis prompt;
- structured output with Markdown tables or JSON for reliability;
- explicit delimiters around source material;
- self-review and quality gates for paper writing.

Use those ideas as prompt-design principles, not as copied prompt text.
