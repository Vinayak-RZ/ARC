# UI diagram examples (agent copy sources)

Copy these into `runs/<run_id>/` (rename to `graph.json` or `control_diagram.json`).

| File | Write as | Domain |
|------|----------|--------|
| `rlc_graph.json` | `graph.json` | Series RLC sheet |
| `unity_feedback_control_diagram.json` | `control_diagram.json` | Control |
| `power_fault_control_diagram.json` | `control_diagram.json` | Power LG SLD |
| `protection_control_diagram.json` | `control_diagram.json` | Protection 50/51 |
| `drives_control_diagram.json` | `control_diagram.json` | DC drive |

Validate:

```bash
python scripts/check_ui_diagram_artifacts.py --examples
```

Gold copies: `eval/gold/ui-diagrams/` (same content).
