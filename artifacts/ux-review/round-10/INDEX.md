# Round 10 capture index

Commit: `ba98814` (`git_dirty_lines`: 0)
Viewport: 1440x900; narrow home at 1024px width.

## Fixes this round

1. Studio deep links with `?session=` now open the Control workspace tab (was Studio landing).
2. Settings UX capture uses sidebar rail buttons (Settings no longer exposes `role="tab"`).
3. Round 10 capture expands the sidebar before `home-with-recent` (default collapsed hid Recent).
4. Capture routes use `?view=studio&tab=control&session=` so PID simulate shots hit Control Studio, not the landing page.
5. Studio lab captures wait on `.lab-shell` (not `.lab-surface`).
6. Dark problem diagram shots accept `.diagram-shell svg` as well as `.static-diagram`.
7. `preflight.json` `git_dirty_lines` ignores untracked files (capture output only).

## Images

- `cmdk-open-dark.png` (dark): Command palette open
- `cmdk-open-light.png` (light): Command palette open
- `cmdk-query-light.png` (light): Command palette with query
- `focus-button-dark.png` (dark): Focus on Run again
- `focus-button-light.png` (light): Focus on Run again
- `focus-composer-dark.png` (dark): Keyboard focus on composer (Tab)
- `focus-composer-light.png` (light): Keyboard focus on composer (Tab)
- `focus-tab-dark.png` (dark): Focus on Work tab
- `focus-tab-light.png` (light): Focus on Work tab
- `focus-table-row-dark.png` (dark): Focus on problems row
- `focus-table-row-light.png` (light): Focus on problems row
- `focus-tile-dark.png` (dark): Focus on example card
- `focus-tile-light.png` (light): Focus on example card
- `gallery-dark.png` (dark): Gallery
- `gallery-light.png` (light): Gallery
- `home-dark.png` (dark): home
- `home-empty-light.png` (light): Home, no recent runs, composer empty
- `home-scrolled-1024-light.png` (light): Home scrolled (1024px viewport)
- `home-scrolled-dark.png` (dark): home scrolled
- `home-with-recent-light.png` (light): Home after running the divider example
- `lab-converter-dark.png` (dark): DC-DC converter lab
- `lab-converter-light.png` (light): DC-DC converter lab
- `lab-idmt-dark.png` (dark): IDMT coordination lab
- `lab-idmt-light.png` (light): IDMT coordination lab
- `lab-lead-dark.png` (dark): Lead compensator lab
- `lab-lead-light.png` (light): Lead compensator lab
- `lab-rectifier-dark.png` (dark): Rectifier lab
- `lab-rectifier-light.png` (light): Rectifier lab
- `learn-achievements-dark.png` (dark): Achievements drawer from Learn
- `learn-achievements-light.png` (light): Achievements drawer from Learn
- `learn-landing-dark.png` (dark): Learn landing, semester rail
- `learn-landing-light.png` (light): Learn landing, semester rail
- `learn-subject-power-electronics-dark.png` (dark): Learn subject EEC-303
- `learn-subject-power-electronics-light.png` (light): Learn subject EEC-303
- `library-dark.png` (dark): Library
- `library-light.png` (light): Library
- `problem-answer-dark.png` (dark): Checked divider, Diagram tab
- `problem-answer-light.png` (light): Checked divider, Diagram tab
- `problem-circuit-checked-diagram-light.png` (light): Series RLC example, Diagram tab
- `problem-circuit-checked-light.png` (light): Series RLC example, checked summary
- `problem-circuit-checked-work-light.png` (light): Series RLC example, Work tab, checked
- `problem-control-checked-light.png` (light): First-order step, result summary checked
- `problem-control-checked-work-light.png` (light): First-order step example, Work tab, checked
- `problem-dark.png` (dark): problem
- `problem-parameters-drawer-light.png` (light): problem parameters drawer
- `problem-parameters-stale-light.png` (light): problem parameters stale
- `problem-stale-dark.png` (dark): problem stale
- `problem-work-dark.png` (dark): problem work
- `problem-work-tab-light.png` (light): Checked divider, Work tab
- `problems-empty-dark.png` (dark): problems empty
- `problems-empty-light.png` (light): problems empty
- `problems-error-dark.png` (dark): problems error
- `problems-error-light.png` (light): problems error
- `problems-list-dark.png` (dark): Problems table with runs
- `problems-list-light.png` (light): Problems table with runs
- `problems-loading-light.png` (light): problems loading
- `problems-row-hover-dark.png` (dark): problems row hover
- `problems-row-hover-light.png` (light): problems row hover
- `settings-about-dark.png` (dark): Settings About tab
- `settings-about-light.png` (light): Settings About tab
- `settings-agents-dark.png` (dark): Settings Agents tab
- `settings-agents-light.png` (light): Settings Agents tab
- `settings-appearance-dark.png` (dark): Settings Appearance tab
- `settings-appearance-light.png` (light): Settings Appearance tab
- `settings-data-dark.png` (dark): Settings Data tab
- `settings-data-light.png` (light): Settings Data tab
- `settings-engines-dark.png` (dark): Settings Engines tab
- `settings-engines-light.png` (light): Settings Engines tab
- `sidebar-collapsed-dark.png` (dark): Collapsed sidebar
- `sidebar-collapsed-light.png` (light): Collapsed sidebar
- `studio-after-resize-light.png` (light): studio after resize
- `studio-after-simulate-dark.png` (dark): studio after simulate
- `studio-before-simulate-dark.png` (dark): studio before simulate
- `studio-block-selected-after-simulate-light.png` (light): studio block selected after simulate
- `studio-block-selected-dark.png` (dark): studio block selected
- `studio-block-selected-light.png` (light): studio block selected
- `studio-circuit-series-rlc-dark.png` (dark): Circuit canvas with Series RLC preset
- `studio-circuit-series-rlc-light.png` (light): Circuit canvas with Series RLC preset
- `studio-landing-dark.png` (dark): Studio home, workspaces and labs
- `studio-landing-light.png` (light): Studio home, workspaces and labs
- `studio-layout-after-simulate-light.png` (light): Control Studio after step simulate
- `studio-layout-before-simulate-light.png` (light): Control Studio before Simulate (PID golden)
- `studio-margins-finite-dark.png` (dark): studio margins finite
- `studio-margins-finite-light.png` (light): studio margins finite
- `studio-margins-no-crossover-dark.png` (dark): studio margins no crossover
- `studio-margins-no-crossover-light.png` (light): studio margins no crossover
- `studio-step-extended-dark.png` (dark): studio step extended
- `studio-step-extended-light.png` (light): studio step extended
- `studio-step-offtarget-light.png` (light): studio step offtarget
- `studio-step-settled-dark.png` (dark): studio step settled
- `studio-step-settled-light.png` (light): studio step settled
- `studio-step-unsettled-dark.png` (dark): studio step unsettled
- `studio-step-unsettled-light.png` (light): studio step unsettled
