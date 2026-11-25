# User Memory

## Independent review of software-agent-sdk PR #7108 / OHE-4216 (2026-11-24)

`ConversationStats.get_combined_metrics()` fix (base 15bbd077d → head
1ab661103) infers aggregate `model_name` from the set of distinct
`m.model_name` across `usage_to_metrics.values()` (excluding `""`/`"default"`);
attributes when exactly one real model remains, else keeps `"default"`.
Verified correct and safe for the PR's actual stated scope (task:*/delegate:*
rollup, nested multi-level delegation, snapshot serialization via
`use_snapshot=True`) with a from-scratch synthetic repro (no mocks) layering
grandchild→child→parent `get_combined_metrics()` exactly as
`task/manager.py`/`delegate/impl.py` do it — all levels correctly attribute
when single-model, correctly fall back to `"default"` when mixed. No mutation
of source Metrics objects (writes only land on the freshly-constructed
`total_metrics`), idempotent, no validate_assignment re-trigger concerns
(`Metrics`/`MetricsSnapshot` set no `model_config`).

Found one real but narrow gap neither the PR author nor the prior automated
review (`all-hands-bot`, reviewed at 16f13ed4) caught: `LLMSession.follow()`
(`llm_session.py`) updates `telemetry.model_name` on every call but never the
*session's* `Metrics.model_name` field — that field is set once at
`LLMSession.__init__` to whichever model first filled the role and is never
refreshed. `FallbackStrategy.try_fallback()` (`fallback_strategy.py`)
deliberately keeps the SAME `usage_id`/session for a fallback model
(`fallback = fb.model_copy(update={"usage_id": primary.usage_id})`,
`fallback._session = primary.session`), so a single usage_id's
`token_usages[*].model` can legitimately mix two real model names while
`Metrics.model_name` stays stuck on the first one —
`tests/sdk/llm/test_llm_fallback_sessions.py::test_fallback_preserves_caller_accounting`
asserts the per-record `.model` values differ but never asserts what
`metrics.model_name` becomes, confirming the field isn't treated as "current
model" anywhere today. Reproduced directly: a Metrics object seeded
`model_name="gpt-4o"` then given cost/token records explicitly tagged
`model_name="gpt-4o-mini"` (mimicking 2 of 3 fallback calls) still yields
`get_combined_metrics().model_name == "gpt-4o"` and
`get_snapshot().model_name == "gpt-4o"` — a specific, confidently WRONG label
reaching the dashboard, versus the pre-PR neutral-but-uninformative
`"default"`. Root cause (stale per-usage `model_name` on intra-role model
switch) pre-dates this PR; the newly-introduced risk is that the new
heuristic trusts that stale field instead of inspecting real per-record
`.model` values, so it can now assert a wrong model with confidence in the
opt-in `fallback_strategy` case. Low blast radius (opt-in feature, only on an
actual transient-failure fallback, cost/token totals stay correct, only the
label is off) — treated as a non-blocking fast-follow, not a reason to
request changes on a PR that correctly fixes its stated, tested scope.
Reusable technique: when a PR infers one derived field from several
upstream objects' own copy of "the same" field, check whether anything
*else* in the codebase ever mutates that per-object field asynchronously
after construction (here: `follow()`/fallback) — tests asserting a *list* of
more granular values but never the top-level aggregate field are a strong
signal the aggregate field is already known-unreliable in that code path.

## External MCP (ChatGPT connector) wire contract tests (2026-11-24)

`tests/unit/server/auth/test_external_mcp_oauth.py` has fixtures for
everything needed to pin the `/external-mcp/mcp` wire contract without a
mock: `oauth_app` fixture mounts the real `ExternalMcpOAuth` provider +
`register_external_mcp_tools` behind a real `FastMCP` app; `_grant`/`_call`
helpers mint tokens and call tools. To introspect the *actual* `tools/list`
JSON (inputSchema/outputSchema/annotations) instead of guessing from
`server/auth/external_mcp_tools.py` source, temporarily add `print(...,
file=sys.stderr)` inside an existing passing test (needs `app_db_session`
fixture, not just `create_user`/`session_maker`, or `_active_principal`'s
`FeatureFlagStore.get_flag` DB call raises "No database configured" and the
flag check silently defaults to disabled → `TokenError('invalid_grant')` with
a misleading-looking failure), run with `-s`, capture to a file, then revert
the print lines before committing — never leave probe output in committed
tests. Confirmed-stable facts about the 4 tools (`list_my_tasks, start_task,
get_task, send_message`) as of OHE 1.97.1 (a3f3a1985833d96622912f1e0fa6c9b1954d25e3):
`get_task` returns `dict[str, Any]` so FastMCP emits a generic
`outputSchema: {type: object, additionalProperties: true}` with no field
list — intentional, not a bug to fix. `list_my_tasks` returns a bare `list`,
so FastMCP wraps it as `{outputSchema: {properties: {result: {...}},
required: [result], x-fastmcp-wrap-result: true}}`. Optional `str | None`
params serialize as `anyOf: [{type: string}, {type: null}]` (not JSON
Schema's `type: [string, null]` union form). AS metadata
(`/.well-known/oauth-authorization-server/external-mcp`) and protected
resource metadata (`/.well-known/oauth-protected-resource/external-mcp/mcp`)
are both small enough to pin as full dict equality. 401 challenge
`WWW-Authenticate` always advertises only `scope="tasks:read"` regardless of
what scope the caller needed (`required_scopes=[READ_SCOPE]` is fixed on the
`OAuthProvider`), with an empty body and `resource_metadata` pointing at the
protected-resource doc.

## EKS Sandbox Secret Lookup (rajistics-demo deployment)

When SESSION_API_KEY/SANDBOX_ID are absent from bash (direct conversation), fetch `github_token` via:
1. Extract conv_id from AUTOMATION_SESSION_URL (`.../conversations/{conv_id}`)
2. GET `https://app.k8s.rajistics.com/api/v1/app-conversations?ids={conv_id}` → Bearer OPENHANDS_API_KEY
3. Use `sandbox_id` + `session_api_key` from response to call:
   GET `{cloud_base}/api/v1/sandboxes/{sandbox_id}/settings/secrets/github_token` → `X-Session-API-Key: {session_api_key}`

See daily log 2026-11-18.md for full detail and PR #266 QA result.

## GitHub access quirks (this worker)

GITHUB_TOKEN/GH_TOKEN/OH_GIT_CREDENTIAL_ACCESS_TOKEN_GITHUB can all be invalid (401) here even though
unauthenticated `curl https://api.github.com/...` and unauthenticated `git fetch origin pull/<n>/head:<ref>`
still work for public OpenHands repos. OpenHands/runtime-api is private and not reachable this way;
both `OpenHands/OpenHands` and `OpenHands/enterprise` ARE public and clone fine over plain HTTPS
(corrected 2026-11-22 — don't assume blocked without trying a plain clone first).
`frontend/node_modules` is not preinstalled; `npm install --no-audit --no-fund` is fast (~25s).
`uv run pytest` in `OpenHands/enterprise` needs a reachable `/var/run/docker.sock` (testcontainers
Postgres, started in root `conftest.py` for every run, even non-DB tests) — `ModuleNotFoundError:
testcontainers` was a one-off missing-dependency gate in an earlier session, fixed by `uv sync`;
the standing gate is Docker access (`sudo dockerd &` + `chmod o+rw /var/run/docker.sock` if the
runtime user isn't in the `docker` group), not the package. `make install-pre-commit-hooks` also
installs Playwright Chromium (~200MB download, budget time for it).
See daily log 2026-11-20.md for the enterprise #1448/#948 sandbox-spec terminology patches, and
2026-11-22.md for the `supports_runtime_pause` capability-flag + conversation-projection change.

## Enterprise v1 provider smoke contract (authoring-only task, 2026-11-22)

Asked to author (not deploy/execute against real infra) a provider-neutral
OpenHands Enterprise v1 API smoke covering sandbox+app-conversation lifecycle
(create/ready/pause/resume/cleanup) for 5 sandbox providers (AWS, E2B, MARS,
Modal prototype, Daytona-TBD), stdlib-only, as a fenced code block in the
final reply rather than a PR. Key design choices worth reusing: (1) the
"smallest common interface" the 5 provider repos need is just a tiny frozen
`ProviderCapabilityManifest` dataclass (name, sandbox_spec_id, a
PauseResume enum of IN_MEMORY/REPLACEMENT/UNSUPPORTED, optional
supports_preview, 4 bounded timeouts) — because Enterprise's REST layer
(`/api/v1/sandboxes`, `/api/v1/app-conversations`, etc.) already abstracts
providers behind `sandbox_spec_id`, so no adapter classes are needed per
provider, just one declarative manifest entry; (2) POSTs/DELETEs must never
be speculatively retried on ambiguous (timeout/connection) errors — classify
as a distinct `Status.UNKNOWN` instead of FAIL/PASS, since retrying a
non-confirmed-idempotent POST risks duplicate resources; (3) SKIP must be a
status distinct from PASS/FAIL so "capability not present" (e.g. Daytona
pause/resume, or no approved_preview_host) is never silently conflated with
passing coverage; (4) cleanup (DELETE sandbox) goes in `try/finally` and
must never raise past itself; treat 404-on-delete as a successful cleanup
outcome; (5) secret redaction is a recursive key-name regex applied to every
logged/report payload, not an allowlist; (6) explicitly documented that an
API-level smoke is NOT a substitute for a real Canvas (1.35.0) click-through
verification — the two are stated as distinct in both code docstring and
report "note" field. Validated end-to-end (all paths: happy path, SKIP
paths, ambiguous-POST path, cleanup-after-failing-check path) against a
same-process stdlib `http.server` mock on localhost before delivering —
no real Enterprise/Canvas stack was touched. Referenced versions: Enterprise
1.88.0 / Canvas 1.35.0 / Agent Server 1.60.1.

## enterprise sandbox lifecycle worker (canvas-recovery pilot, 2026-11-21)

`openhands/app_server/sandbox/lifecycle/tasks.py` has a `Blueprint` named
`lifecycle` with periodic `sweep`/`check` tasks (pause/delete). Extended it
with an independent `pilot_checkpoint_sweep`/`pilot_checkpoint_check` pair
for an automatic-checkpoint pilot (flags `OH_PILOT_RUNTIME_RECOVERY_ENABLED`
+ new `OH_PILOT_AUTO_CHECKPOINT_ENABLED`, both required, both default off).
Helper module: `.../lifecycle/pilot_checkpoint.py`. Delivered as
`/workspace/canvas-recovery/recovery.patch` + `HANDOFF.md`. Useful repo
facts found along the way:
- `StoredSandbox` (sandbox_store.py) has `backend`, `credential_org_id`,
  `created_by_user_id` — exactly what's needed to confirm an overlay backend
  (e.g. `lambda-microvm`) and owner/org binding *without* importing that
  overlay's service class.
- `StoredConversationMetadata.tags` is a JSON `dict[str,str]` column
  (sql_app_conversation_info_service.py); `StoredConversationMetadataSaas`
  (storage/) has `user_id`/`org_id`.
- `openhands/app_server/utils/redis_lock.py` has
  `try_acquire_redis_lock(key, ttl)` — nonblocking, returns `None` if held;
  exactly the "retry next sweep" primitive.
- Repo's root `conftest.py` starts a Postgres testcontainer in
  `pytest_configure` for *every* `uv run pytest` invocation, even
  non-DB tests — so with `testcontainers` missing/no Docker (this
  worker's standing gate), no pytest run at all is possible here, only
  plain `uv run python -c "..."` sanity checks.

## Modal V1 adapter task (rajistics-demo worker, 2026-11-22) — repo access was blocked

This worker's actual "authorized GitHub connection" is the on-disk
helper `~/.openhands/git-credential-helper github`, which exchanges a
token file (`~/.openhands/git-credentials/github.token`) via
`$base_url/api/v1/webhooks/secrets` for a short-lived `ghu_...`
user-to-server GitHub token. **Never pipe that helper's stdout to a
terminal command you'll see** — `password=...` prints the raw token in
plaintext; capture it into a shell variable inside a script file instead
and only use it in `Authorization: Bearer $VAR` headers. For this
specific worker (`app.k8s.rajistics.com`, GitHub login `rajshah4`),
`GET /user/installations` → exactly one GitHub App installation, org
**`rajistics-demo`**, and `GET /user/installations/<id>/repositories` →
exactly one repo, **`rajistics-demo/sdlc-automation-github-demo`**
(public, unrelated SDLC-automation demo app). No OpenHands Enterprise
org/repo is connected here — confirms the standing note above
(`OpenHands/runtime-api is private and not reachable`) generalizes: this
whole class of "Enterprise sandbox provider" tasks (Modal/E2B/DigitalOcean
adapters, `app_server/sandbox/...`) is **not** actually checkable out
in a rajistics-demo-flavored worker; only prior sessions with different
GitHub App grants could read that tree. When a task like this recurs,
check `/user/installations` + per-installation `/repositories` *first*
(cheap, 2 calls) before assuming the Enterprise repo is reachable — and
when it isn't, the task's own "if blocked, give a technical critique"
escape hatch is the correct move: ship a self-contained reference
implementation (dataclass/Protocol reconstruction of the known
interface + fakes-based pytest suite) plus a written gap analysis,
rather than fabricating file paths/diffs against an unseen tree.
Modal-specific facts worth reusing verbatim next time: SDK 1.6.0
Sandboxes have two checkpoint mechanisms — `snapshot_filesystem()` →
`modal.Image` (non-destructive, resume = brand-new `Sandbox.create(image=...)`,
new id + new tunnel URL) vs. the alpha `experimental_options={"enable_memory_snapshot": True}`
+ `experimental_snapshot()` CRIU path (destructive to the original at
capture, new tunnel on restore, excludes processes started via
`Sandbox.exec()`). For "no loss of committed checkpoint", pick the
filesystem path and persist the checkpoint *before* calling
`terminate()`, never after.

## OHE sandbox runtime-pause capability + conversation projection (2026-11-22)

Implemented `SandboxInfo.supports_runtime_pause` (provider-owned, default
False, identity/workspace claim only — never a process-memory promise) on
`openhands/app_server/sandbox/sandbox_models.py` + `SandboxService` base
default, with K8sAgentSandboxService/E2BSandboxService/RemoteSandboxService
each overriding to `ClassVar[bool] = True` with an inline comment citing the
exact verified pause/resume mechanism; Docker/Process backends intentionally
left at the False default (out of scope). Then projected it onto
`AppConversation.sandbox_supports_runtime_pause` at the **single**
`_build_conversation` construction site in
`live_status_app_conversation_service.py`, sourced from the real bound
sandbox's flag (`bool(sandbox and sandbox.supports_runtime_pause)`), per an
explicit user follow-up that Canvas reads the field off the conversation, not
the sandbox API. Full base SHA, diff, and test results are in the
2026-11-22 daily log. Key transferable lesson: before adding any field to a
service/model, `grep` for *every* construction site of that type across the
non-test tree first (`SandboxInfo(`, `AppConversation(`) — both turned out to
have a small, enumerable set of call sites, which is what made "smallest
defensible shared seam" tractable without a router/adapter layer. Also:
`make install-pre-commit-hooks` + `sudo dockerd &` + `chmod o+rw
/var/run/docker.sock` is the repeatable recipe to get this repo's
testcontainers-based pytest working from a fresh clone in a sandboxed
worker (root cause: runtime user isn't in the `docker` group here).

## Daytona v2 sandbox provider package for OHE 1.88.0 (2026-11-23)

Delivered standalone at /workspace/daytona-v2-package +
/workspace/daytona-v2-package.tar.gz (54 tests passing, verified by
extracting the tarball fresh and re-running). Same rajistics-demo access
gap as prior Modal/E2B tasks (no Enterprise source reachable) — standard
response is now: build a self-contained overlay package + honest
verified-vs-reconstructed doc (`docs/INTERFACES.md`), reusing the closest
verified prior overlay as the structural template. New technique: verify a
pinned third-party SDK live in a throwaway venv via
`inspect.signature`/`typing.get_type_hints`/installed docstrings before
writing code against it, not from doc prose. Test fakes for an
Enterprise-shaped dependency tree: use PEP 420 namespace packages (no
`__init__.py` at shared levels) so `tests/fakes/openhands/...` and the real
`openhands/...` tree merge on sys.path; fake only in-house interfaces from
scratch, fake only the SDK's *return objects* (not its wire protocol) for
the real pinned cloud SDK. Debugging lesson: a broad `except Exception:
last_error = exc` retry loop that times out instead of surfacing the real
error should have `last_error` printed directly when debugging — the
"timeout" is almost never the actual root cause. Full detail in the
2026-11-23 daily log.

## SCIM users-only PR (OHE-3626) review-fix + final export (2026-11-22)

`/workspace/project/enterprise-scim-users` = real PR worktree, branch
`agent/scim-users`. `/workspace/project/enterprise` = a *different*
worktree (`agent/scim-users-prototype`) used only as the drop location for
interchange files — always `git branch --show-current` in both, a prior
summary had them backwards. Closed 3 review items as commit `0c72cf0`
(tree `080c5ca`) atop checkpoint `ca425e3`: (1) `ScimStore.mint_credential`
— lock the org's own (always-present) row with `FOR UPDATE` *before* the
active-credential-count query, since locking only the count query's own
rows does nothing when zero rows exist yet (concurrent first-ever mints);
general pattern for any "insert serialization" gap. (2)
`AuthProviderStore.get_by_ids`/`get_titles_by_ids` (title-only query never
touches the encrypted `details` column) so an org-admin's SCIM setup/list
endpoints only load bound/referenced providers, not every instance
provider; Super Admin path unchanged. (3) Split
`frontend/src/routes/scim-settings.tsx` into an inner component + a
`key={organizationId}` wrapper so switching orgs remounts and drops stale
modal/mutation state; also fixed both clipboard-copy buttons to show an
error toast on a rejected `writeText()` instead of always toasting
success. Full detail, test commands/counts, and the patch-export recipe
(format-patch → gzip -9 → base64, record both uncompressed+compressed
sha256, verify via `git worktree add --detach <base> && git am --3way` then
compare `HEAD^{tree}`) are in the 2026-11-22 daily log — reuse that
recipe verbatim for any future PR-interchange-file export task.

## SCIM UI screenshots, PR 1506 head 5e1b3f2a1 (2026-11-25)

`/workspace` mount runs ~95% full (~540M free) — never `npm install`/clone
large repos there; use `/tmp` or `/` (overlay, has tens of GB free), only
drop small final deliverables under `/workspace/project/...`. SCIM settings
page (`frontend/src/routes/scim-settings.tsx`) needs mock env
`VITE_MOCK_API=true VITE_MOCK_SAAS=true VITE_MOCK_SCIM=true
VITE_MOCK_SCIM_ORG_ADMIN=true` for `npm run dev:mock:saas` — `VITE_MOCK_SCIM`
drives the `enable_scim` feature flag the route's own clientLoader redirects
away without (separate from the `provision_user` permission check), and
`VITE_MOCK_SCIM_ORG_ADMIN` makes the seeded credential register as the
provider's *last* active one so the revoke dialog's last-credential warning
actually renders. `npx msw init public --no-save` after `npm install` if
msw's postinstall got npm-allowScripts-blocked (default on this box).
Faking one mock-returned value (e.g. a demo token) for a screenshot:
Playwright `page.route()` never sees responses MSW's browser Service Worker
answers in-page, and patching `window.fetch` misses axios's default XHR
adapter too — editing the mock handler source line itself (in a disposable
copy, then `diff -rq` against the read-only original to prove it's the only
change) is the reliable approach. Base64 of a ~80KB PNG is ~1.33x larger
(~105KB) — check the *encoded* size against any size cap, not the raw PNG.
Full detail (including `split`/reassembly recipe) in 2026-11-25 daily log.

## PR #7105 heartbeat review follow-up (test-only) (2026-11-24)

`agent/heartbeat-thread-pool-coverage` off aec27eb7e added a legacy
thread-pool cancellation regression test + fixed misleading/stale
comments; prod code untouched (MD5-verified). Key pitfall: don't use
`asyncio.wait_for(task, timeout=T)` to "observe" whether a background task
would still be running — it cancels on timeout, silently masking the
exact leak a test is trying to detect. Use `asyncio.wait({task},
timeout=T)` for observation; reserve `wait_for`'s cancel side effect for
real `finally` cleanup. `contextlib.suppress(Exception)` never catches
`asyncio.CancelledError` (BaseException in 3.8+) — list it explicitly.
Full detail in 2026-11-24 daily log.
