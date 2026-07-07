# Provider Configuration

The skill never includes API keys. Users provide keys through environment variables or a local JSON config.

`scripts/run_multi_model.py` uses OpenAI-compatible `/chat/completions` endpoints. This covers OpenAI, DeepSeek, many proxy services, local gateways, and custom chat5.4/chat5.5-style services if they expose a compatible API.

If the user has no API keys, do not use this script. Use `no-api-mode.md`: the user generates candidates in different ChatGPT models manually and pastes them back for rubric-based judging.

## Environment Variables

Common examples:

```bash
OPENAI_API_KEY=...
DEEPSEEK_API_KEY=...
CHAT54_API_KEY=...
CHAT54_BASE_URL=https://your-chat54-endpoint.example/v1
CHAT54_MODEL=chat5.4
CHAT55_API_KEY=...
CHAT55_BASE_URL=https://your-chat55-endpoint.example/v1
CHAT55_MODEL=chat5.5
```

PowerShell example:

```powershell
$env:DEEPSEEK_API_KEY = "..."
$env:CHAT54_BASE_URL = "https://your-chat54-endpoint.example/v1"
$env:CHAT54_API_KEY = "..."
$env:CHAT54_MODEL = "chat5.4"
```

## JSON Config

Create a local config file such as `model-providers.json` outside the skill folder or in the working project:

```json
{
  "providers": {
    "deepseek": {
      "base_url": "https://api.deepseek.com/v1",
      "api_key_env": "DEEPSEEK_API_KEY",
      "model": "deepseek-chat"
    },
    "openai": {
      "base_url": "https://api.openai.com/v1",
      "api_key_env": "OPENAI_API_KEY",
      "model": "gpt-5"
    },
    "custom_chat54": {
      "base_url_env": "CHAT54_BASE_URL",
      "api_key_env": "CHAT54_API_KEY",
      "model_env": "CHAT54_MODEL"
    },
    "custom_chat55": {
      "base_url_env": "CHAT55_BASE_URL",
      "api_key_env": "CHAT55_API_KEY",
      "model_env": "CHAT55_MODEL"
    }
  }
}
```

## CLI Examples

Generate a dry-run payload without calling any API:

```bash
python scripts/run_multi_model.py --input input.txt --providers deepseek --dry-run
```

Call configured providers:

```bash
python scripts/run_multi_model.py \
  --input input.txt \
  --config model-providers.json \
  --providers deepseek,openai,custom_chat54 \
  --versions faithful,native,concise,strong,reviewer_safe \
  --output variants.json
```

## Built-In Provider Defaults

If no JSON config is supplied, the script knows these names:

- `openai`: `https://api.openai.com/v1`, key env `OPENAI_API_KEY`, model `gpt-5`
- `deepseek`: `https://api.deepseek.com/v1`, key env `DEEPSEEK_API_KEY`, model `deepseek-chat`
- `custom_chat54`: base URL env `CHAT54_BASE_URL`, key env `CHAT54_API_KEY`, model env `CHAT54_MODEL`
- `custom_chat55`: base URL env `CHAT55_BASE_URL`, key env `CHAT55_API_KEY`, model env `CHAT55_MODEL`

If a provider is missing a key or base URL, the script fails with a configuration error and does not guess credentials.
