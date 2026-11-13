# UX review round 2 (in progress)

## Form control borders (item 8 override)

Tokens in `ui/src/tokens.css`:

| Token | Light | Contrast vs `#FFFFFF` | Contrast vs canvas `#FAFAF9` |
|-------|-------|----------------------|------------------------------|
| `--ee-border-input` | `#8C8C87` | **3.38:1** | **3.23:1** |
| `--ee-border-input-hover` | `#7A7A75` | **4.31:1** | **4.13:1** |

Dark theme (surface `#1A1A18`, canvas `#121211`):

| Token | Dark | vs surface | vs canvas |
|-------|------|------------|-----------|
| `--ee-border-input` | `#757570` | **3.76:1** | **4.05:1** |
| `--ee-border-input-hover` | `#6A6A65` | **3.21:1** | **3.45:1** |

Focus: `outline: 2px solid #2F6FEB; outline-offset: 2px` on inputs, selects, textareas, parameter fields, composer textarea, Problems search, and Cmd+K input. Divider hairlines remain `--ee-color-hairline`.

Contrast computed with WCAG relative luminance (non-text UI ≥ 3:1).
