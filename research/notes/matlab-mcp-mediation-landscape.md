# MATLAB MCP mediation landscape

Survey retrieved 2026-09-14. Product name Arc; host-facing CLI/MCP remains `electrical-engineer`. This note answers: how Arc drives MATLAB when a MathWorks licence exists, without the homework host ingesting MATLAB’s tool dump.

Reuse: [`matlab-simulink-surface.md`](matlab-simulink-surface.md), [`docs/ON_THE_HARNESS.md`](../../docs/ON_THE_HARNESS.md) “Coming next”, [`docs/PRD.md`](../../docs/PRD.md) FR20, `src/electrical_engineer/nodes/sim.py` `run-matlab-if-present` (currently always `_missing("matlab")`). Gate lock: [`docs/planning/GATE_0_SKILLS_MATLAB.md`](../../docs/planning/GATE_0_SKILLS_MATLAB.md).

## Problem

Arc must be the **only** MCP the homework host sees. Today FR20 still *permits* a peer MATLAB MCP beside Arc; that is the clumsy path [`docs/ON_THE_HARNESS.md`](../../docs/ON_THE_HARNESS.md) names. MATLAB MCP (and especially Simulink `--extension-file` tools plus coding-guideline resources) dumps on the order of **10,000 tokens** of tool/resource description into the assistant context. The host can then treat a MATLAB scalar as a lab result unless Arc stops it.

Coming next (not shipped): the coding assistant talks only to Arc. Arc decides when MATLAB is needed, calls it, and returns a short labeled result (verified or `unchecked`) plus the observation log.

Constraints that any family must keep:

- Product and CI work with **zero** MATLAB ([`docs/PRD.md`](../../docs/PRD.md) FR9/FR20).
- Checked numbers come only from a child EE verifier artifact (`run-spice`, `check-numeric`, `run-python-control`, `run-load-flow`, `run-matlab-if-present`). Peer/host/Copilot scalars are not ingest.
- Always-on host ACI stays **5–7 verbs**. Do not wrap `run-matlab-if-present` as a new host tool ([`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) §2.2).
- MATLAB MCP is a **local Go stdio binary**, not a mathworks.com login. Never store MathWorks passwords.
- MathWorks licence: MCP servers **must not be shared by multiple users**.
- As-built `run_matlab_if_present` always returns `_missing("matlab")` (`ok: false`, `unchecked: true`). Fail-closed is already the empty-machine behavior.

## Solution families

At least the nine families the mediation question actually presents. **Host tool dump** = what Layer 0 (Cursor / Claude Code / Codex / ChatGPT desktop) lists after `tools/list`. **Checked-number authority** = who may set `unchecked: false`.

| Family | Mechanism | Host tool dump | Checked-number authority | Licence / seat | CI without MATLAB | Evidence URL |
|--------|-----------|----------------|--------------------------|----------------|-------------------|--------------|
| **Kernel stdio MCP client** (recommend) | Kernel spawns `matlab-mcp-server` as a child, JSON-RPC stdio `initialize` then `tools/call`, maps results into existing `run-matlab-if-present`. Host never lists MATLAB tools. | Arc’s 5–7 verbs only | EE node: `run-matlab-if-present` is already on the FR20 allowlist | Local single-seat spawn on the student’s machine. Matches “must not be shared by multiple users.” | Binary absent → keep `_missing`. Tests talk to a fake stdio server. | https://github.com/matlab/matlab-mcp-server |
| **Peer dual-MCP** (today’s FR20 allowance) | Host `mcp.json` / Claude / Codex lists Arc **and** MATLAB MCP. | Full MATLAB tool/resource dump (~10k tokens; larger with Simulink `tools.json`) lands in homework chat | FR20: peer scalars untrusted until EE recomputes. Easy to violate in practice; Copilot must not be named verifier | Student seat, but the host holds a second live MATLAB session the assistant can poke | CI omits MATLAB MCP and still passes | https://github.com/matlab/matlab-mcp-server ; [`docs/PRD.md`](../../docs/PRD.md) FR20 ; [`docs/ON_THE_HARNESS.md`](../../docs/ON_THE_HARNESS.md) |
| **Filtered MCP proxy** | Put `mcp-proxy` or ToolHive in front of MATLAB MCP. `mcp-proxy` is a **stdio↔HTTP transport bridge**, not a filter. ToolHive `MCPToolConfig.toolsFilter` can allow-list tools, still **to the host**. | Smaller than raw Simulink dump; host still sees MATLAB verbs. Arc is no longer the only MCP. | Unchanged peer-ingest problem unless Arc also mediates | ToolHive’s remote-proxy story is multi-client / k8s-shaped — clashes with single-seat MCP licence | Extra operator; CI still needs a stub or skip | https://github.com/sparfenyuk/mcp-proxy ; https://docs.stacklok.com/toolhive/guides-k8s/customize-tools |
| **New Arc `matlab_*` host verbs** | Add `matlab_eval` / `matlab_run_file` to Arc’s ACI so the host calls MATLAB by name. | Grows past 5–7; duplicates MATLAB schemas into Arc’s `tools/list` | Could be EE if the verb only returns kernel artifacts — but ARCHITECTURE forbids wrapping providers as extra MCP tools | Same local seat | Could stub the new verbs | [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) §2.2 (do not wrap `run-matlab-if-present`) |
| **`matlab.engine` (Engine API for Python)** | `import matlab.engine`; `start_matlab()` / `connect_matlab()`; `eng.eval` / function calls. Requires installed MATLAB, **not** MATLAB Runtime. | Zero MATLAB MCP dump if used only inside the kernel | EE if wrapped in `run-matlab-if-present` | One MATLAB process per `start_matlab`; `find_matlab` / shared engine is the same single-seat story | `import matlab.engine` fails with no install; cannot be a required dep | https://www.mathworks.com/help/matlab/matlab-engine-for-python.html |
| **MATLAB REST / Production Server** | Desktop **REST Function Service** (R2024a+): `POST https://localhost:9920/matlab/feval/v1/<service>/<fn>` with `mwRESTPersonalAccessToken`. **Production Server**: `POST /<archive>/<fn>` JSON `rhs`/`nargout`, health/metrics APIs, worker pool. | Zero MCP dump | EE if wrapped — but MPS is a different product, not the student desktop verifier | REST Function Service is desktop, token in memory; **do not persist the PAT**. MPS workers are shared/centralized — MathWorks says contact them before shared MCP/server use | Needs a live MATLAB or MPS instance | https://www.mathworks.com/help/matlab/matlab_external/get-started-with-matlab-rest-function-service.html ; https://www.mathworks.com/help/mps/restful-api-and-json.html |
| **Jupyter kernel** | Official `jupyter-matlab-proxy` MATLAB kernel for notebooks; optional browser MATLAB. Default: **one MATLAB shared across notebooks**. | Not an MCP surface unless a Jupyter MCP is also attached (another dump) | Not an EE engine unless rewrapped | Shared-kernel default fights single-seat / isolated-workspace needs | Jupyter + proxy + MATLAB — too much for CI | https://github.com/mathworks/jupyter-matlab-proxy |
| **Simulink Agentic Toolkit** (Later) | Same MATLAB MCP binary plus `--extension-file=…/tools/tools.json` and `satk_initialize`. Extra tools: `model_read`, `model_edit`, `model_check`, `model_test`, `model_scan`, … | `tools/tools.json` is 22 535 bytes (~5–6k tokens of schema) on top of the five core tools and guideline resources → the ~10k host dump | Same as peer unless kernel-mediated later | MATLAB **R2023a+ with Simulink**; `model_test` wants Simulink Test | Not in P0 CI | https://github.com/matlab/simulink-agentic-toolkit |
| **COM / WSDL** | Windows **COM Automation**: ProgID `Matlab.Application` / `Matlab.Desktop.Application`, `Execute` / `Feval`. **WSDL**: `matlab.wsdl.createWSDLClient` makes MATLAB a **SOAP client** (wrong direction) and is **to-be-removed since R2025b**. | Zero MCP dump | EE if wrapped; Windows-only COM | Desktop MATLAB on Windows; not Linux CI | No MATLAB in CI; COM absent on Linux | https://www.mathworks.com/help/matlab/call-matlab-com-automation-server.html ; https://www.mathworks.com/help/matlab/ref/matlab.wsdl.createwsdlclient.html |

## MATLAB MCP tool list and args

Official MATLAB MCP Server (Go stdio binary; hosts: Claude Code/Desktop, VS Code Copilot, Codex). Product page lists the same five tools. Minimum MATLAB for the server: **R2021a+** on PATH; **session attach (`existing`/`auto`) needs R2023a+**.

| Tool | What it does | Arguments |
|------|----------------|-----------|
| `detect_matlab_toolboxes` | Installed MATLAB + toolbox names and versions. Call first when a lab needs Control System / Simscape Electrical / Signal Processing / Symbolic Math. | none documented |
| `check_matlab_code` | Read-only Code Analyzer on a `.m` file (style, deprecated APIs, performance). Does not execute. | `script_path` (string, **absolute** path to a `.m` file) |
| `evaluate_matlab_code` | Evaluate a MATLAB code string; return command-window output. Sets cwd to `project_path`. This is the numeric-lab primitive. | `code` (string); `project_path` (string, **absolute** project directory) |
| `run_matlab_file` | Execute a `.m` script; return output. | `script_path` (string, **absolute** path to a `.m` file) |
| `run_matlab_test_file` | Run a MATLAB unit-test file; return framework results. | `script_path` (string, **absolute** path to a test `.m` file) |

Resources the **host** would also ingest if MATLAB MCP were a peer (another reason not to attach it):

- `matlab_coding_guidelines` — `guidelines://coding` (`text/markdown`)
- `plain_text_live_code_guidelines` — `guidelines://plain-text-live-code` (`text/markdown`; live scripts need MATLAB R2025a+)

Custom tools (Simulink toolkit and others) load via `--extension-file=<json>` (repeatable; env `MW_MCP_SERVER_EXTENSION_FILE` is `:`/`;`-separated). P0 kernel client must **not** pass Simulink `tools.json`.

Kernel mapping (no new host verb): capability bind stays `run-matlab-if-present`; that node calls `evaluate_matlab_code` or `run_matlab_file` (and optionally `detect_matlab_toolboxes` / `check_matlab_code` before execute). Host still names `lumped-circuit-sim` / `simulate_attachment` / `propose_composition`.

## Session modes, nodesktop, telemetry, single-seat licence

CLI flags; env form is `MW_MCP_SERVER_` + uppercase + underscores (`--matlab-root` → `MW_MCP_SERVER_MATLAB_ROOT`). Flags beat env.

| Flag | Values / default | Arc implication |
|------|------------------|-----------------|
| `--matlab-root` | Install dir **without** `/bin`; else first MATLAB on PATH | Pin the student’s copy; never a campus licence password |
| `--initialize-matlab-on-startup` | `true` / default lazy (first tool call) | Prefer **lazy**: CI and zero-MATLAB machines must not spawn MATLAB at MCP boot |
| `--initial-working-folder` | else MCP Root, else `~/Documents` (Win/Mac) or `$HOME` (Linux) | Point at `./runs/<id>/` or the recipe cwd |
| `--matlab-display-mode` | `desktop` (default) or `nodesktop` | Agent path: **`nodesktop`**. GUI commands (`edit`, `open_system`, `uifigure`, …) may still open windows. Issue #104: `auto` spawn can still inject `-nodesktop` even when desktop is requested — figures then screenshot-only |
| `--matlab-session-mode` | `new` / `existing` / **`auto` (default)** | **`new`** for isolated homework runs. `existing`/`auto` need `matlab-mcp-server --setup-matlab` (installs MATLAB MCP Server Toolbox) then `shareMATLABSession()` in a running desktop (R2023a+). Do **not** pass `matlab-root` / `initial-working-folder` / `matlab-display-mode` with `existing`. Do **not** attach to a multi-user shared MATLAB |
| `--extension-file` | JSON tool defs | Omit on P0 |
| `--disable-telemetry` | default **on** (anonymized usage to MathWorks); `true` to opt out | Set **`--disable-telemetry=true`** |
| `--log-level` / `--log-folder` | `debug`…`error`; OS temp | `debug` only while diagnosing licence hangs |

**Licence / seat (must not be multi-user shared).** README “Licensing and Usage”: MCP servers may be used with MATLAB only under the MathWorks Software License Agreement **and must not be shared by multiple users**; contact MathWorks for shared or centralized server use. Kernel spawn-per-student-desktop is the compliant shape. A faculty-shared MCP, MPS worker pool, JupyterHub shared kernel, or ToolHive remote proxy is not.

Network/campus licence failure modes (already in [`matlab-simulink-surface.md`](matlab-simulink-surface.md)): VPN down → MCP setup timeouts with opaque logs; Error 15 on MCP-spawned MATLAB while interactive MATLAB works. Fail closed; do not hang the host. Never store licence passwords or REST PATs in git, env files committed to the repo, or `runs/`.

Binary: local Go stdio (`matlab-mcp-server` / platform assets). Not a MathWorks web login.

## Stub vs live (what a fake stdio server must speak)

Live path: kernel finds `matlab-mcp-server` + a licensed MATLAB → spawn stdio subprocess → MCP lifecycle → `tools/call` → parse text result into the EE artifact (`ok`, `unchecked`, paths). Missing binary, failed spawn, licence error, or timeout → same fail-closed dict as today’s `_missing("matlab")` (`ok: false`, `unchecked: true`, token `unchecked`). Never mint a checked scalar from a stub.

MCP stdio (spec 2025-11-25): newline-delimited JSON-RPC 2.0; no embedded newlines; **stdout is protocol only**; logs on stderr. Official TS/Python/Go SDKs are NDJSON, not LSP `Content-Length` (Arc’s own `electrical-engineer mcp` already writes `json.dumps(...) + "\n"`). Hosts may still send Content-Length to *Arc*; that is FR22 for the **server** side, not a reason to add the `mcp` PyPI package as a MATLAB client. A few dozen lines of subprocess NDJSON reuse the kernel’s existing JSON-RPC habits.

**Fake stdio server (CI / no MATLAB) must speak at least:**

1. **`initialize`** (JSON-RPC request, first interaction on the legacy handshake MATLAB MCP uses). Params: `protocolVersion`, `capabilities`, `clientInfo`. Result: `protocolVersion`, `capabilities.tools`, `serverInfo`. Example protocolVersion Arc already returns to hosts: `2024-11-05`.
2. **`notifications/initialized`** (notification, no `id`) — accept and ignore.
3. **`tools/list`** — return the five MATLAB tool names + `inputSchema` so the kernel client can be tested against a real-shaped list. CI does **not** forward this list to the homework host.
4. **`tools/call`** — `params.name` + `params.arguments`. Stub returns a JSON-RPC **result** with MCP `content` text (and optionally `isError: true`). It must **not** return a plausible homework number that tests could treat as checked. Prefer `isError` or a payload the kernel maps to `_missing` / `unchecked`.
5. Unknown methods → JSON-RPC error, process stays up (same fail-closed stance as Arc’s server).
6. No MATLAB process, no network, no telemetry, no passwords.

Optional for a richer stub: `ping`, `resources/list` empty. Not required for P0 if the kernel client only calls initialize + tools/call.

Do not install MATLAB Engine, Jupyter, or Production Server in CI.

## Recommendation

**Kernel stdio MCP client behind `run-matlab-if-present`. No new host verb. Fail closed if missing. Simulink Later. Never store passwords.**

Concrete P0 shape:

1. Homework host attaches **only** `electrical-engineer mcp` (existing 5–7 verbs). MATLAB MCP is not in host `mcp.json`.
2. When a capability binds `run-matlab-if-present` and a MATLAB MCP binary is on disk, the kernel spawns it (`--matlab-session-mode=new`, `--matlab-display-mode=nodesktop`, `--disable-telemetry=true`, `--initial-working-folder` = run dir). Lazy start (default).
3. Kernel client: `initialize` → `notifications/initialized` → `tools/call` (`detect_matlab_toolboxes` if the recipe names a toolbox, then `evaluate_matlab_code` / `run_matlab_file`). Long sims: raise tool timeout (toolkit docs often use ≥600s) — not a host-visible tool.
4. Result becomes an EE verifier artifact. `label` / `check-numeric` may clear `unchecked` only from that artifact (FR20 law unchanged). Provenance names the capability + `run-matlab-if-present`, never Copilot or the host.
5. No binary / no licence / spawn fail → keep `_missing("matlab")`. OSS providers stay first-class (`run-spice`, `run-python-control`, …).
6. CI: fake stdio server above; gold must not require MATLAB (FR9).
7. **Simulink Agentic Toolkit is Later.** P0 is not unsafe without it: undergrad numeric labs are `.m` evaluate/run. `.slx` read/edit/simulate tools need Simulink + `satk_initialize` + `tools.json` and would recreate the 10k dump if attached to the host. When Later ships, the **kernel** may pass `--extension-file`, still not the host.
8. Do not add `matlab.engine`, MPS, Jupyter, COM, or a proxy. Do not persist REST tokens or MathWorks passwords. MATLAB MCP is the local Go binary.

FR20’s *peer dual-MCP allowance* stays as a historical clamp (peer scalars still cannot mint checked numbers if a student turns MATLAB MCP on anyway). It is **not** the happy path. Happy path is ON_THE_HARNESS “Coming next” / Gate 0: host talks only to Arc.

## Rejects

- **Peer dual-MCP as P0 install instructions** — 10k-token dump; host can call MATLAB behind Arc’s back; ON_THE_HARNESS and Gate 0 forbid it as the intended attach.
- **Filtered proxy (mcp-proxy / ToolHive) as the mediator** — `mcp-proxy` does not filter tools; ToolHive still exposes MATLAB verbs to the host; k8s/remote-proxy is multi-user-shaped.
- **New `matlab_*` host verbs** — violates 5–7 ACI and “do not wrap providers.”
- **`matlab.engine` as the P0 driver** — reimplements Code Analyzer / toolbox detect / official MCP; extra native dep; still needs a licensed MATLAB; CI cannot import it. Optional Later fallback only if the Go binary is unusable.
- **MATLAB Production Server / REST Function Service as the homework path** — MPS is shared workers; REST PAT must not be stored; not the student-desktop MCP MathWorks already ships.
- **Jupyter MATLAB kernel** — notebook product; default shared session; not MCP; licence/workspace isolation is wrong.
- **Simulink toolkit on P0** — unsafe for *host* attach (dump). Safe to defer for *kernel* attach. `.slx` labs are Later, not a P0 blocker.
- **COM Automation** — Windows-only; MathWorks points new work at Engine-for-.NET, not COM.
- **WSDL/SOAP** — wrong direction (MATLAB as SOAP *client*); `createWSDLClient` to-be-removed since R2025b.
- **Storing MathWorks passwords, licence files, or `mwRESTPersonalAccessToken` in git or committed env** — Gate 0; never.
- **Multi-user shared MATLAB MCP** (faculty server, container pool, one `shareMATLABSession` for a lab) — forbidden by MATLAB MCP licence text.
- **Minting `unchecked: false` from a stub or from Copilot/host-typed scalars** — FR20.

## Sources

- [MATLAB MCP Server README](https://github.com/matlab/matlab-mcp-server) — retrieved 2026-09-14 — tools, args, session modes, nodesktop, telemetry, single-seat licence — primary
- [MATLAB MCP Server product page](https://www.mathworks.com/products/matlab-mcp-server.html) — retrieved 2026-09-14 — five built-in tools — vendor
- [slash-commands MCP integration](https://github.com/matlab/slash-commands/blob/main/docs/mcp-integration.md) — retrieved 2026-09-14 — flag table (`nodesktop`, `--disable-telemetry`) — primary
- [MATLAB MCP issue #104](https://github.com/matlab/matlab-mcp-server/issues/104) — retrieved 2026-09-14 — `auto` spawn vs display mode — primary
- [MATLAB MCP issue #78](https://github.com/matlab/matlab-mcp-server/issues/78) — retrieved 2026-09-14 — licence-server timeout during setup — primary
- [MATLAB Engine API for Python](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html) — retrieved 2026-09-14 — start/connect; Runtime not sufficient — vendor
- [Install MATLAB Engine for Python](https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html) — retrieved 2026-09-14 — vendor
- [Start MATLAB Engine for Python](https://www.mathworks.com/help/matlab/matlab_external/start-the-matlab-engine-for-python.html) — retrieved 2026-09-14 — vendor
- [MATLAB REST Function Service](https://www.mathworks.com/help/matlab/matlab_external/get-started-with-matlab-rest-function-service.html) — retrieved 2026-09-14 — PAT + HTTPS feval — vendor
- [Create MATLAB REST Function Services](https://www.mathworks.com/help/matlab/matlab_external/create-matlab-rest-function-services.html) — retrieved 2026-09-14 — desktop-only; tokens in memory — vendor
- [MATLAB Production Server RESTful API](https://www.mathworks.com/help/mps/restful-api-and-json.html) — retrieved 2026-09-14 — vendor
- [sparfenyuk/mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) — retrieved 2026-09-14 — stdio↔HTTP, no tool filter — primary
- [ToolHive customize tools](https://docs.stacklok.com/toolhive/guides-k8s/customize-tools) — retrieved 2026-09-14 — `toolsFilter` still host-facing — vendor
- [Simulink Agentic Toolkit](https://github.com/matlab/simulink-agentic-toolkit) — retrieved 2026-09-14 — `--extension-file`, `satk_initialize`, Later — primary
- [jupyter-matlab-proxy](https://github.com/mathworks/jupyter-matlab-proxy) — retrieved 2026-09-14 — shared MATLAB across notebooks — primary
- [MATLAB COM Automation](https://www.mathworks.com/help/matlab/call-matlab-com-automation-server.html) — retrieved 2026-09-14 — Windows-only — vendor
- [matlab.wsdl.createWSDLClient (to be removed)](https://www.mathworks.com/help/matlab/ref/matlab.wsdl.createwsdlclient.html) — retrieved 2026-09-14 — wrong direction; R2025b deprecation — vendor
- [MCP lifecycle (initialize)](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle) — retrieved 2026-09-14 — handshake — primary
- [MCP stdio transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) — retrieved 2026-09-14 — NDJSON — primary
- [Python MCP SDK stdio client example](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/stdio_client.py) — retrieved 2026-09-14 — `initialize` + `call_tool` — primary
- In-repo: [`docs/ON_THE_HARNESS.md`](../../docs/ON_THE_HARNESS.md) Coming next; [`docs/PRD.md`](../../docs/PRD.md) FR20; [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) §2.2; [`docs/planning/GATE_0_SKILLS_MATLAB.md`](../../docs/planning/GATE_0_SKILLS_MATLAB.md); `src/electrical_engineer/nodes/sim.py` `run_matlab_if_present`; [`research/notes/matlab-simulink-surface.md`](matlab-simulink-surface.md)

## Confidence

Overall confidence for this note: **high**

Official MATLAB MCP README (tools, flags, licence clause) and MathWorks Engine / REST / COM / WSDL pages were fetched 2026-09-14. Simulink `tools/tools.json` size (22 535 bytes) was read from GitHub contents API the same day. The ~10k-token host-dump figure is the product’s documented order of magnitude ([`docs/ON_THE_HARNESS.md`](../../docs/ON_THE_HARNESS.md)), not a token-counter run against a live MATLAB MCP `tools/list` in this environment (no MATLAB here). Exact MCP protocolVersion the Go binary negotiates was not executed; stub should accept the initialize handshake and echo a 2024/2025 protocolVersion. Campus licence/VPN failure modes remain operational, not API, uncertainty.
