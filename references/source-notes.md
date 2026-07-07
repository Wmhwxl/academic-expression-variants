# Source Notes

Use this file only when maintaining or extending the skill. Do not load it for ordinary rewriting tasks.

The prompt architecture was informed by these public GitHub repositories, using ideas rather than copied prompt text:

- `ahmetbersoz/chatgpt-prompts-for-academic-writing`: academic prompt categories such as language/style improvement, translation, proofreading, paragraph feedback, abstracts, titles, and literature-review workflows.
- `brexhq/prompt-engineering`: structured data, Markdown tables, JSON output, delimiters, and programmatic-consumption patterns.
- `trigaten/Learn_Prompting`: broad prompt-engineering taxonomy and safety/red-team framing.
- `cLin-c/paper-skill`: academic skill organization, quality gates, translation, reviewer response, journal strategy, and modular prompt-bank structure.

Maintenance rules:

- Do not paste long external prompts into this skill.
- Extract reusable design patterns: role separation, source delimiters, structured output, self-audit, quality gates, and task-specific prompt modules.
- Keep operational prompts in `prompt-pack.md`.
- Keep evaluation criteria in `style-rubric.md`.
- Keep trigger and workflow routing in `SKILL.md`.
