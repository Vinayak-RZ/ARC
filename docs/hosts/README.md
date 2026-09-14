# Host adapters

Arc is the electrical-engineering lab your coding assistant loads: a local
command line, a local MCP connection, and course-method files.

Cursor, Claude Code, Codex, and **ChatGPT desktop** are supported assistants.
They are not the only way to run it. `electrical-engineer` plus the local
window is a complete path with no assistant. Why Arc is not a generic command
line or MCP, and why the numbers stay deterministic:
[`ON_THE_HARNESS.md`](../ON_THE_HARNESS.md).

There is no `init-host` helper. Copy or symlink skills. Point the assistant at:

```text
electrical-engineer mcp
```

**Same lab on every assistant:** same tools, same gates, unverified numbers
labeled. Same lab does not mean identical IDE screens.

**Tools the assistant can call:** list lab recipes, look up a citation, open
the local window, run a short simulation, propose a combination of allowed
checks, read the labeled result. Replay a named recipe is the command-line /
test path. This checkout has 27 named lab recipes. If none fits, the assistant
proposes allowed checks and Arc validates then runs. Photo / compose /
control-diagram never wait in chat: you get a
link to the local window. On a large assignment the assistant writes
`./runs/<id>/plan.md` first, then the explanation. Load at most two packs for
the homework, not every pack. Do not copy EE packs into this repo’s
`.cursor/skills/`.

**Not supported as v1 assistants:** ChatGPT in the browser or on a phone,
Claude Desktop, GitHub Copilot, Gemini CLI.

**Pack helpers:** copy [`../../hosts/adapters/`](../../hosts/adapters/README.md)
into *your* homework project (Claude Task / Codex / Cursor). At most two
packs. They share the saved run folder. Arc does not start those helpers.

**MATLAB today:** you may enable MathWorks MCP next to Arc. Those numbers stay
unverified until Arc recomputes them ([`../PRD.md`](../PRD.md) FR20).
**Coming next:** Arc will call MATLAB (and other agents) itself so the
assistant does not ingest MATLAB's huge tool list. See
[`ON_THE_HARNESS.md`](../ON_THE_HARNESS.md).

- [Cursor](cursor.md)
- [Claude Code](claude-code.md)
- [OpenAI / Codex](openai.md)
- [ChatGPT desktop](chatgpt-desktop.md)
