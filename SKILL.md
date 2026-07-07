---
name: academic-expression-variants
description: Translate, rewrite, and polish Chinese or English research-paper text into multiple idiomatic academic expression variants. Use when the user asks for academic translation, paper-style rewriting, scientific English polishing, multiple versions of a sentence, paragraph, abstract, introduction, contribution statement, reviewer-safe wording, journal-style variants, no-API ChatGPT model candidate judging, or multi-model comparison for scholarly prose. Supports user-configured OpenAI-compatible endpoints such as OpenAI, DeepSeek, Anthropic-compatible proxies, Gemini-compatible proxies, local models, or custom chat5.4/chat5.5-style services; never provide or require bundled API keys.
---

# Academic Expression Variants

## Core Workflow

Turn the user's Chinese or English research text into multiple publication-quality variants while preserving meaning, evidence level, uncertainty, terminology, and scope. By default, provide each variant in both English and Chinese: English for manuscript use, Chinese for semantic verification and author-side comparison.

1. Identify the source language, target language, field, manuscript section, and requested venue/style if supplied.
2. If the user does not specify versions, produce the default set: faithful, native academic, concise, strong claim, and reviewer-safe.
3. Use `references/version-types.md` to choose version purposes and labels.
4. Use `references/prompt-architecture.md` when the request is complex, long, high-stakes, multi-model, journal-specific, or asks for professional prompt behavior.
5. Use `references/prompt-pack.md` for the fixed rewriting and translation prompts.
6. Use `references/style-rubric.md` to check factual fidelity, academic naturalness, terminology, concision, and overclaiming risk.
7. Use `references/field-style-notes.md` only when the user specifies a field, venue family, or section where style matters.
8. If the user has no API but wants multiple model judgment, use `references/no-api-mode.md`.
9. If the user asks to compare multiple models or use configured APIs, read `references/provider-config.md` and run `scripts/run_multi_model.py`.

## Default Output

For ordinary requests, return a compact bilingual table with:

- `Version`: faithful, native academic, concise, strong claim, reviewer-safe, or user-requested style.
- `English`: the manuscript-ready English version.
- `Chinese counterpart`: a polished Chinese counterpart that matches the English variant's meaning, rhetorical strength, and uncertainty.
- `Best for`: where this version fits, such as abstract, introduction, contribution, method, results, discussion, rebuttal, or cover letter.
- `Risk note`: any meaning drift, excessive certainty, missing context, or terminology concern.

After the table, add a short `Recommended version` note. When useful, include 3-6 bilingual terminology or phrasing notes.

## No-API Mode

Use No-API mode when the user has no API keys but wants multiple-model selection. Default rule: without API access, use ChatGPT's different models to create multiple candidates, then use this skill's rubric to judge, rank, merge, and recommend the final result.

If candidates are already pasted, evaluate them directly. If candidates are not pasted, provide a copyable prompt for the user to run in different ChatGPT models, then ask them to paste the labeled outputs back for judging.

Do not claim that Codex called ChatGPT models unless the candidates were actually supplied by the user or a configured API/tool was used.

## Hard Constraints

- Preserve the user's factual content. Do not invent citations, datasets, experiments, numbers, mechanisms, claims, limitations, or causal links.
- Keep the English and Chinese versions aligned. Do not let the Chinese counterpart add explanations or claims that the English version does not contain.
- Keep hedges when the original text is uncertain. Do not turn association into causation or preliminary evidence into proof.
- Do not make the text sound impressive by adding unsupported novelty, generality, clinical relevance, policy relevance, or state-of-the-art claims.
- Do not imitate a specific copyrighted paper's phrasing. Journal or venue style means rhetorical density, caution, structure, and tone, not copied templates.
- If the input is ambiguous, mark the ambiguity and provide a conservative variant instead of silently choosing a stronger claim.
- If the user asks for AI-detection evasion, ghostwriting misconduct, fabricated references, or unsupported result inflation, refuse that part and offer ethical academic editing instead.

## Multi-Model Mode

Use multi-model mode only when the user asks for multiple model APIs, model comparison, DeepSeek/OpenAI/custom endpoint generation, or consensus judging.

1. Confirm that the user must provide API keys through environment variables or a local config; the skill does not include keys.
2. Prefer OpenAI-compatible chat-completions endpoints for portability.
3. Run:

```bash
python scripts/run_multi_model.py --input input.txt --providers deepseek,openai,custom_chat54 --versions faithful,native,concise,strong,reviewer_safe --output variants.json
```

4. Review the JSON outputs using `references/style-rubric.md`.
5. Present the final curated bilingual variants, not raw duplicated model dumps.

## Resource Map

- `references/prompt-architecture.md`: professional prompt design patterns for this skill.
- `references/no-api-mode.md`: workflow for judging ChatGPT model candidates without API keys.
- `references/chatgpt-model-prompts.md`: copyable prompts for ChatGPT model candidate generation and judging handoff.
- `references/prompt-pack.md`: fixed system, task, variant, diagnostic, and quality-check prompts.
- `references/version-types.md`: supported version types and when to use each.
- `references/style-rubric.md`: scoring rubric and red flags.
- `references/field-style-notes.md`: compact style guidance by field, venue family, and manuscript section.
- `references/provider-config.md`: user-owned API configuration patterns.
- `references/source-notes.md`: maintenance-only notes about public GitHub inspiration sources.
- `scripts/run_multi_model.py`: stdlib-only OpenAI-compatible multi-model runner.
