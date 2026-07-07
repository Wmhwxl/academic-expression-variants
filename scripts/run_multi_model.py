#!/usr/bin/env python3
"""
OpenAI-compatible multi-model runner for academic expression variants.

This script is intentionally stdlib-only. It does not provide API keys, store
secrets, or require any specific vendor SDK.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_PROVIDERS: Dict[str, Dict[str, str]] = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "api_key_env": "OPENAI_API_KEY",
        "model": "gpt-5",
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "api_key_env": "DEEPSEEK_API_KEY",
        "model": "deepseek-chat",
    },
    "custom_chat54": {
        "base_url_env": "CHAT54_BASE_URL",
        "api_key_env": "CHAT54_API_KEY",
        "model_env": "CHAT54_MODEL",
    },
    "custom_chat55": {
        "base_url_env": "CHAT55_BASE_URL",
        "api_key_env": "CHAT55_API_KEY",
        "model_env": "CHAT55_MODEL",
    },
}

SYSTEM_PROMPT = """You are an expert bilingual academic writing editor, research translator, and journal-style prose reviewer.

Your job is to transform Chinese or English research text into publication-quality scholarly expression while preserving the author's factual content. By default, produce each expression variant in both English and Chinese.

Hard rules:
- Preserve meaning, scope, uncertainty, evidence level, and technical terminology.
- Do not invent results, citations, datasets, numbers, mechanisms, limitations, or causal claims.
- Do not add novelty, superiority, clinical relevance, policy relevance, or broad generality unless the source explicitly supports it.
- Keep hedges and epistemic status: may/can/suggest/associated with/preliminary/under these conditions.
- Produce variants that differ in rhetorical purpose, not factual content.
- Keep each English variant aligned with its Chinese counterpart in meaning, scope, uncertainty, and claim strength.
- Prefer precise, natural scholarly language over ornate, promotional, or AI-generic wording.
- If the source is ambiguous, preserve the ambiguity or state the conservative assumption in the risk note."""

VERSION_GUIDE = {
    "faithful": "Prioritize semantic fidelity and terminology accuracy. Improve grammar and readability only where needed.",
    "native": "Make the prose sound natural to an experienced researcher in the target field. Improve collocations, clause order, information flow, transitions, and academic tone.",
    "concise": "Compress without losing technical meaning. Prefer high-density academic phrasing suitable for abstracts, contribution bullets, figure captions, or response summaries.",
    "strong": "Make the contribution or finding sound clear and confident while staying within the evidence. Do not add novelty, causality, or generality that the source does not support.",
    "reviewer_safe": "Use cautious, defensible wording. Preserve limitations, uncertainty, scope boundaries, and methodological constraints.",
    "journal_style": "Adapt rhythm, density, and rhetorical framing to the requested venue or journal family. Do not copy wording from specific papers.",
    "chinese_polished": "Produce idiomatic Chinese scholarly prose with clear logic, precise terms, and restrained claims. Avoid stiff translationese.",
    "method_precise": "Clarify procedure, inputs, outputs, assumptions, optimization target, evaluation setting, and reproducibility-relevant details. Avoid promotional verbs.",
    "result_neutral": "State the observed result clearly and separate it from interpretation. Preserve metrics, comparisons, statistical language, and experimental conditions exactly.",
    "rebuttal": "Respond respectfully and directly. Acknowledge the reviewer's concern, state the action or clarification, and point to evidence without defensive language.",
}


def parse_csv(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def load_config(path: str | None) -> Dict[str, Dict[str, Any]]:
    providers = dict(DEFAULT_PROVIDERS)
    if not path:
        return providers

    config_path = Path(path)
    data = json.loads(config_path.read_text(encoding="utf-8"))
    custom = data.get("providers", {})
    if not isinstance(custom, dict):
        raise ValueError("Config file must contain an object field named 'providers'.")
    providers.update(custom)
    return providers


def resolve_provider(name: str, all_providers: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
    if name not in all_providers:
        raise ValueError(f"Unknown provider '{name}'. Add it to config JSON or use a built-in provider.")

    raw = all_providers[name]
    base_url = raw.get("base_url") or os.getenv(raw.get("base_url_env", ""))
    api_key = raw.get("api_key") or os.getenv(raw.get("api_key_env", ""))
    model = raw.get("model") or os.getenv(raw.get("model_env", ""))

    missing = []
    if not base_url:
        missing.append("base_url or base_url_env")
    if not api_key:
        missing.append(raw.get("api_key_env", "api_key"))
    if not model:
        missing.append("model or model_env")
    if missing:
        raise ValueError(f"Provider '{name}' is missing: {', '.join(missing)}")

    return {
        "name": name,
        "base_url": base_url.rstrip("/"),
        "api_key": api_key,
        "model": model,
    }


def build_user_prompt(args: argparse.Namespace, source_text: str) -> str:
    versions = parse_csv(args.versions)
    version_lines = []
    for version in versions:
        guide = VERSION_GUIDE.get(version, "Use the purpose implied by this version label.")
        version_lines.append(f"- {version}: {guide}")

    return f"""Task: Generate multiple bilingual academic expression variants.
Source language: {args.source_language}
Target language: {args.target_language}
Research field: {args.field}
Manuscript section: {args.section}
Target venue/style: {args.venue}

Source text:
<source_text>
{source_text}
</source_text>

Requested variants:
{chr(10).join(version_lines)}

Process:
1. Identify the claim type: background, gap, method, result, limitation, implication, contribution, rebuttal, or other.
2. Lock terminology: preserve named methods, datasets, variables, metrics, domain terms, and key hedges.
3. Generate each requested version with a distinct rhetorical purpose, providing both English and Chinese text.
4. Audit each version for fidelity, terminology, academic naturalness, bilingual alignment, overclaiming, and version fit.
5. Revise any version that changes the meaning or overstates the evidence.

Return valid JSON only with this schema:
{{
  "diagnosis": {{
    "claim_type": "...",
    "locked_terms": ["..."],
    "hedges_to_preserve": ["..."],
    "evidence_boundaries": ["..."],
    "ambiguities": ["..."]
  }},
  "variants": [
    {{
      "version": "faithful",
      "english_text": "...",
      "chinese_text": "...",
      "best_for": "...",
      "risk_note": "...",
      "audit": {{
        "fidelity": 1,
        "terminology": 1,
        "naturalness": 1,
        "bilingual_alignment": 1,
        "claim_control": 1
      }}
    }}
  ],
  "recommended_version": "...",
  "terminology_notes": ["..."]
}}

Do not expose chain-of-thought. Keep the factual content unchanged. If the source is ambiguous, preserve the ambiguity or mention the assumption."""


def chat_completion(provider: Dict[str, str], messages: List[Dict[str, str]], timeout: int) -> Dict[str, Any]:
    url = f"{provider['base_url']}/chat/completions"
    payload = {
        "model": provider["model"],
        "messages": messages,
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {provider['api_key']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    started = time.time()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {provider['name']}: {error_body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed for {provider['name']}: {exc}") from exc

    data = json.loads(raw)
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    parsed_content: Any
    try:
        parsed_content = json.loads(content)
    except json.JSONDecodeError:
        parsed_content = {"raw_text": content}

    return {
        "provider": provider["name"],
        "model": provider["model"],
        "elapsed_seconds": round(time.time() - started, 3),
        "content": parsed_content,
        "raw_response_id": data.get("id"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate academic expression variants using user-configured model APIs.")
    parser.add_argument("--input", required=True, help="UTF-8 text file containing the source passage.")
    parser.add_argument("--providers", required=True, help="Comma-separated provider names, e.g. deepseek,openai,custom_chat54.")
    parser.add_argument("--config", help="Optional JSON config with provider definitions.")
    parser.add_argument("--versions", default="faithful,native,concise,strong,reviewer_safe")
    parser.add_argument("--source-language", default="auto")
    parser.add_argument("--target-language", default="English")
    parser.add_argument("--field", default="general")
    parser.add_argument("--section", default="unknown")
    parser.add_argument("--venue", default="none")
    parser.add_argument("--output", default="variants.json")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--dry-run", action="store_true", help="Print the request payload without calling APIs.")
    args = parser.parse_args()

    source_text = read_text(args.input)
    user_prompt = build_user_prompt(args, source_text)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    provider_names = parse_csv(args.providers)
    all_providers = load_config(args.config)

    if args.dry_run:
        print(json.dumps({"providers": provider_names, "messages": messages}, ensure_ascii=False, indent=2))
        return 0

    results = []
    errors = []
    for provider_name in provider_names:
        try:
            provider = resolve_provider(provider_name, all_providers)
            results.append(chat_completion(provider, messages, args.timeout))
        except Exception as exc:  # Keep other providers running.
            errors.append({"provider": provider_name, "error": str(exc)})

    output = {
        "input_file": args.input,
        "versions": parse_csv(args.versions),
        "results": results,
        "errors": errors,
    }
    Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    if errors and not results:
        print(f"No provider succeeded. Errors written to {args.output}", file=sys.stderr)
        return 2
    if errors:
        print(f"Completed with {len(errors)} provider error(s). Output written to {args.output}", file=sys.stderr)
        return 1

    print(f"Output written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
