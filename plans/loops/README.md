# Loop plans (graph-of-loops)

Parent: [`../../LOOP_GRAPH.md`](../../LOOP_GRAPH.md).

Each `<id>.md` is the only authority that loop’s maker loads. Matching `<id>.state.json` is the resume checkpoint (`pending` / `looping` / `passed` / `escalated`).

Do not spawn a nested graph. Subagents do not commit.
