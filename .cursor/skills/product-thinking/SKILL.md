---
name: product-thinking
description: >-
  Use when designing or reviewing a product, a feature, an information
  architecture or a screen, especially B2B, operational or AI products with a
  human in the loop. Works from the jobs people need done to journeys,
  structure, screens and a heuristics check, and keeps facts apart from
  judgement.
---
# Product thinking

A short method for turning "what should this product be" into a structure people can use. Generic: it names no company, product or industry.

## When to use
- Designing a new product, area or screen, or redesigning one.
- Reviewing a design, prototype or live product.
- Any AI feature that proposes, decides or acts for a person.

## Output, in this order
1. **Facts and constraints.** What is decided, built, measured or legally required, each with a source. Then, separately, what is your judgement.
2. **Users and jobs.** Roles, and for each one or two jobs in the form "When [situation], I want to [motivation], so I can [outcome]" (Jobs to be Done; Christensen et al., *Competing Against Luck*, 2016; Intercom on job stories: https://www.intercom.com/blog/using-job-stories-design-features-ui-ux/).
3. **Journeys.** For each key role, the steps from trigger to outcome, with the moments of doubt and the moments a decision is made (user story mapping: Jeff Patton, *User Story Mapping*, 2014).
4. **Opportunities.** Tie each proposed screen or feature to an outcome and a job, not the other way round (Opportunity Solution Tree: Teresa Torres, https://www.producttalk.org/opportunity-solution-tree/).
5. **Structure.** Sitemap, navigation model, role-based views and permissions (role x action x scope). Use progressive disclosure: summary first, detail on demand (https://www.nngroup.com/articles/progressive-disclosure/).
6. **Screens.** For each: purpose, who uses it, key content, primary action, empty, loading, stale and error states.
7. **Heuristics check.** Run the checks below and list each failure with a fix.
8. **Appetite and scope.** What is in the first build, what is cut, and the risks that are unknown (Shape Up: fixed time, variable scope, https://basecamp.com/shapeup).
9. **Open questions.** Only the ones that block a decision, each with your default.

## Checks

**Usability (Nielsen's 10 heuristics, https://www.nngroup.com/articles/ten-usability-heuristics/).** System status visible; match the user's world and words; user control and undo; consistency; error prevention; recognition over recall; flexibility for experts; minimal design; help users recover from errors; help and documentation.

**Design of everyday things (Don Norman, 2013).** Each action has a visible affordance and signifier; feedback after every action; a clear mapping between control and effect; constraints that prevent errors.

**Human-AI interaction (Microsoft HAX, https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/; Google PAIR People + AI Guidebook, https://pair.withgoogle.com/guidebook).**
- Make clear what the system can do, and how well it can do it.
- Show why it did what it did; show confidence in the terms the method actually produces, not an invented percentage.
- Make it easy to invoke, dismiss and correct; scope down when unsure; let it say "I do not know".
- Time interruptions to the person's task; remember recent interactions; learn from feedback and show that it did.
- Make the boundary between suggesting and acting explicit, and show who approved an action.

**Operational and industrial screens (ISA-101 HMI lifecycle; High Performance HMI practice, e.g. Hollifield et al., *The High Performance HMI Handbook*, 2008).**
- Muted, mostly grey displays; colour reserved for abnormal states and the action that matters.
- Never colour alone: every state also has a word or icon.
- A display hierarchy from overview to detail to diagnostics.
- Show values against their limits and targets, not raw numbers alone.
- Design for the real device, light, distance and glove or panel use.

**Accessibility.** WCAG 2.2 AA (https://www.w3.org/TR/WCAG22/): contrast, keyboard, focus, target size, reduced motion.

## Rules
- Facts carry a source. Judgement is labelled as judgement. Never invent numbers, customers or quotes; use placeholders.
- Every screen answers: who is this for, what job, what is the one action.
- Every AI output shows its basis, its uncertainty and who acts.
- Prefer one shared component over many look-alikes.
- Write the open questions last and keep them few.

## Existing open skills worth reading (check licences before copying)
- product-on-purpose/pm-skills, Apache-2.0: https://github.com/product-on-purpose/pm-skills
- Uxcel-Lab/product-skills, MIT: https://github.com/Uxcel-Lab/product-skills
- plugin87/ux-ui-agent-skills, MIT: https://github.com/plugin87/ux-ui-agent-skills
- deanpeters/Product-Manager-Skills, CC BY-NC-SA 4.0 (non-commercial, do not copy into commercial work): https://github.com/deanpeters/product-manager-skills
This skill is written fresh and copies no text from them.
