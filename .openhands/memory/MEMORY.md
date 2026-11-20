# User Memory

## EKS Sandbox Secret Lookup (rajistics-demo deployment)

When SESSION_API_KEY/SANDBOX_ID are absent from bash (direct conversation), fetch `github_token` via:
1. Extract conv_id from AUTOMATION_SESSION_URL (`.../conversations/{conv_id}`)
2. GET `https://app.k8s.rajistics.com/api/v1/app-conversations?ids={conv_id}` → Bearer OPENHANDS_API_KEY
3. Use `sandbox_id` + `session_api_key` from response to call:
   GET `{cloud_base}/api/v1/sandboxes/{sandbox_id}/settings/secrets/github_token` → `X-Session-API-Key: {session_api_key}`

See daily log 2026-11-18.md for full detail and PR #266 QA result.
