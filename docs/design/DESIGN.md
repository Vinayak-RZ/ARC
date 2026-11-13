---
name: Learning
description: A calm technical notebook for learning one idea at a time.
colors:
  canvas: "#FAFAF9"
  surface: "#FFFFFF"
  surface-subtle: "#F5F5F4"
  surface-sunken: "#EFEFED"
  border: "#E4E4E2"
  border-strong: "#D4D4D1"
  text-primary: "#202020"
  text-secondary: "#5F5F5C"
  text-muted: "#8A8A86"
  text-inverse: "#FFFFFF"
  cobalt: "#2F6FEB"
  cobalt-50: "#EEF3FE"
  cobalt-100: "#DCE6FD"
  cobalt-700: "#1D47A3"
  cobalt-800: "#173879"
  copper: "#E07A3F"
  success: "#2F9E6A"
  warning: "#E0A526"
  critical: "#D0312D"
typography:
  display:
    fontFamily: "Geist, Inter, system-ui, sans-serif"
    fontSize: "28px"
    fontWeight: 500
    lineHeight: 1.29
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Geist, Inter, system-ui, sans-serif"
    fontSize: "20px"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Geist, Inter, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.625
    letterSpacing: "normal"
  label:
    fontFamily: "Geist, Inter, system-ui, sans-serif"
    fontSize: "11px"
    fontWeight: 600
    lineHeight: 1.45
    letterSpacing: "0.06em"
rounded:
  sm: "4px"
  md: "6px"
  full: "999px"
spacing:
  "1": "4px"
  "2": "8px"
  "3": "12px"
  "4": "16px"
  "5": "24px"
  "6": "32px"
  "7": "48px"
  "8": "64px"
components:
  button-primary:
    backgroundColor: "{colors.cobalt}"
    textColor: "{colors.text-inverse}"
    rounded: "{rounded.sm}"
    padding: "0 12px"
    height: "32px"
  button-primary-hover:
    backgroundColor: "#2459C9"
    textColor: "{colors.text-inverse}"
  chip-selected:
    backgroundColor: "{colors.cobalt-50}"
    textColor: "{colors.cobalt-700}"
    rounded: "{rounded.sm}"
    padding: "0 12px"
    height: "28px"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.sm}"
    padding: "0 12px"
    height: "36px"
---

# Design System: Learning

## 1. Overview

**Creative North Star: "The shift notebook"**

This is Cobalt UI used as a reading tool. The page is a warm-gray workspace with thin lines. Cobalt appears where you are, what is selected, and the one button that moves you on. Copper and the category tints label areas. They do not compete with the action.

The system rejects consumer course sites with hero metrics, identical card grids, and a lesson buried under marketing. It also rejects dark dashboards with purple gradients, glass panels, and glow. Desktop stays dense. A phone rearranges the same pieces so a thumb can hit them.

**Key Characteristics:**

- Quiet neutrals, one cobalt accent
- Sections, not floating cards
- One filled primary button in a region
- Phone targets at 44px, desk controls stay compact
- A word beside every colored state

## 2. Colors

Warm gray structure, cobalt for intent, status hues only for outcome.

### Primary

- **Cobalt** (`#2F6FEB`): filled primary button, brand mark, focus, the active mark in navigation and charts.
- **Cobalt tint** (`#EEF3FE`): the core-idea block and a selected control.
- **Cobalt ink** (`#1D47A3`): accent text and links at any size.

### Secondary

- **Copper** (`#E07A3F`): the second category hue, for data and area tags. It is not a second action color.

### Tertiary

- **Success, warning, critical** (`#2F9E6A`, `#E0A526`, `#D0312D`): outcome tags only, each with its tint and a word.

### Neutral

- **Canvas** (`#FAFAF9`): the page behind the workspace.
- **Surface** (`#FFFFFF`): sections and inputs.
- **Subtle surface** (`#F5F5F4`): rails, table headers, insets.
- **Ink** (`#202020`): primary text.
- **Secondary ink** (`#5F5F5C`) and **muted ink** (`#8A8A86`): support and metadata.
- **Line** (`#E4E4E2`): structure.

**The Trace Rule.** Cobalt is on every screen as a trace: current navigation, focus, a selected control. The solid fill is only the primary button, the brand mark, and a small badge.

**The One Action Rule.** At most one filled primary button in a region.

## 3. Typography

**Display Font:** Geist (Inter, then the system sans)
**Body Font:** Geist
**Label/Mono Font:** Geist for labels, Geist Mono for figures and code

**Character:** One technical sans. Weight and size carry hierarchy. No display face in a button or a label.

### Hierarchy

- **Display** (500, 28px, 36px line): the page title.
- **Title** (600, 20px, 28px line): section titles.
- **Body** (400, 16px, 26px line): lesson prose. Keep a reading measure near 65–75 characters on the desk.
- **Label** (600, 11px, uppercase, 0.06em tracking): crumbs, eyebrows, table headers. 11px is the floor, and only labels use it.

**The Weight Rule.** A key figure inside a sentence is weight 600, not a second color.

## 4. Elevation

Depth is tonal. Surfaces step from canvas to white to subtle gray. Sections have no shadow.

### Shadow Vocabulary

- **Menu** (`0 1px 2px rgba(32, 32, 32, 0.04), 0 4px 12px rgba(32, 32, 32, 0.05)`): popovers and floating bars only.

**The Flat Section Rule.** A lesson block does not lift. If it needs a shadow, it is a menu, not content.

## 5. Components

### Buttons

- **Shape:** 4px corners.
- **Primary:** cobalt fill, inverse text, 32px tall on the desk. On a phone the lesson's main button grows to a 44px thumb target.
- **Hover / Focus:** fill deepens to `#2459C9`. Focus is a 2px cobalt ring.
- **Secondary:** white, 1px line, ink text.

### Chips

- **Style:** subtle gray fill, 4px corners, 28px on the desk.
- **State:** pressed chips use the cobalt tint, a cobalt-200 line, and cobalt ink. On a phone, chips are at least 44px tall.

### Cards / Containers

- **Corner Style:** 6px for a section, 4px for an inset.
- **Background:** white section on the canvas.
- **Shadow Strategy:** none.
- **Border:** 1px line.
- **Internal Padding:** 24px on the desk, 16px on a phone.

### Inputs / Fields

- **Style:** 36px, 1px line, 4px corners, white fill. 44px tall on a phone.
- **Focus:** cobalt line plus the focus ring.

### Navigation

- **Desk:** a 56px icon rail on the left. The crumb bar names Library and each area.
- **Phone:** the rail moves to the bottom and gains word labels for Library and each area that has lessons. The crumb keeps Library, the current area, and the page name. It wraps instead of clipping. Targets are at least 44px. The bottom bar clears the home-indicator inset.

### Lesson outline

On the desk, the outline sticks beside the reading. On a phone it becomes one horizontal row of section links above the lesson, with the selected section on a cobalt tint. No side stripe.

## 6. Do's and Don'ts

### Do:

- **Do** keep cobalt as a trace, and save the solid fill for the one action.
- **Do** give a phone its own arrangement: bottom navigation, 44px targets, one column.
- **Do** put a word next to every success, warning, and critical color.
- **Do** keep the desk dense. Compact 32px buttons and 28px chips stay on wide screens.

### Don't:

- **Don't** look like a consumer course site with hero metrics, identical card grids, and a lesson buried under marketing.
- **Don't** use dark dashboards with purple gradients, glass panels, and glow.
- **Don't** squeeze a desktop table onto a phone until the words stack one letter wide.
- **Don't** ship navigation that only works with a pointer.
- **Don't** use a side stripe wider than 1px as decoration. A 2px mark is only an active indicator.
- **Don't** put a gradient on text, or a glass card behind a lesson.
