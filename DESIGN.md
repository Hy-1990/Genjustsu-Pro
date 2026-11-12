---
name: Genjustsu Pro
description: A bilingual production desk in porcelain and forest by day, petroleum and citron by night.
colors:
  day-ground: "#edf1ef"
  day-surface: "#ffffff"
  day-rail: "#f7f9f7"
  day-field: "#f5f7f5"
  day-ink: "#203c36"
  day-muted: "#52665e"
  day-line: "#d6dfda"
  day-line-strong: "#b6c6be"
  day-primary: "#215e4f"
  day-primary-hover: "#164d3f"
  day-primary-ink: "#ffffff"
  day-primary-soft: "#e4eee7"
  day-accent: "#d5ec92"
  day-accent-ink: "#314a1a"
  day-success: "#286747"
  day-success-soft: "#eaf3ec"
  day-danger: "#a03734"
  day-danger-soft: "#fff0ec"
  day-warning: "#76531d"
  day-warning-soft: "#faf1de"
  day-media: "#e4e9e5"
  day-media-loaded: "#17251f"
  day-focus: "#317d65"
  day-header: "#f8faf8"
  night-ground: "#18272e"
  night-surface: "#22343b"
  night-rail: "#1d2f36"
  night-field: "#1b2c33"
  night-ink: "#edf2e9"
  night-muted: "#afc0ba"
  night-line: "#3a4e53"
  night-line-strong: "#61777a"
  night-primary: "#d6ec9a"
  night-primary-hover: "#e5f5b9"
  night-primary-ink: "#253729"
  night-primary-soft: "#354a3d"
  night-accent: "#d6ec9a"
  night-accent-ink: "#253729"
  night-success: "#a5d6b5"
  night-success-soft: "#294438"
  night-danger: "#ffb8a9"
  night-danger-soft: "#4b3535"
  night-warning: "#efd39d"
  night-warning-soft: "#443f30"
  night-media: "#1c2e34"
  night-media-loaded: "#101e24"
  night-focus: "#c8e48d"
  night-header: "#1d2e35"
typography:
  headline:
    fontFamily: "\"Manrope\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "27px"
    fontWeight: 650
    lineHeight: 1.25
    letterSpacing: "-.025em"
  brand:
    fontFamily: "\"Manrope\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "17px"
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: "-.025em"
  title:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "15px"
    fontWeight: 600
    lineHeight: 1.5
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "12px"
    fontWeight: 550
    lineHeight: 1.5
  annotation:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "11px"
    fontWeight: 400
    lineHeight: 1.5
  elapsed:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.5
rounded:
  badge: "5px"
  tab: "6px"
  field: "7px"
  notice: "8px"
  control: "9px"
  switch: "10px"
  execution: "12px"
  panel: "14px"
spacing:
  tight: "4px"
  small: "8px"
  field: "10px"
  compact: "12px"
  inspector: "18px"
  panel: "20px"
  wide: "22px"
  page: "28px"
components:
  day-button-primary:
    backgroundColor: "{colors.day-primary}"
    textColor: "{colors.day-primary-ink}"
    rounded: "{rounded.control}"
    padding: "10px 14px"
  day-button-primary-hover:
    backgroundColor: "{colors.day-primary-hover}"
    textColor: "{colors.day-primary-ink}"
    rounded: "{rounded.control}"
    padding: "10px 14px"
  day-button-secondary:
    backgroundColor: "{colors.day-primary-soft}"
    textColor: "{colors.day-primary}"
    rounded: "{rounded.control}"
    padding: "10px 14px"
  day-button-quiet:
    backgroundColor: "transparent"
    textColor: "{colors.day-muted}"
    rounded: "{rounded.control}"
    padding: "10px 14px"
  day-button-text:
    backgroundColor: "transparent"
    textColor: "{colors.day-primary}"
    rounded: "{rounded.control}"
    padding: "4px 0"
  day-field:
    backgroundColor: "{colors.day-field}"
    textColor: "{colors.day-ink}"
    rounded: "{rounded.field}"
    padding: "9px 10px"
  day-panel:
    backgroundColor: "{colors.day-surface}"
    textColor: "{colors.day-ink}"
    rounded: "{rounded.panel}"
    padding: "18px"
  day-status-badge:
    backgroundColor: "{colors.day-field}"
    textColor: "{colors.day-muted}"
    rounded: "{rounded.badge}"
    padding: "4px 7px"
  day-status-badge-success:
    backgroundColor: "{colors.day-success-soft}"
    textColor: "{colors.day-success}"
    rounded: "{rounded.badge}"
    padding: "4px 7px"
  day-preview-tab-active:
    backgroundColor: "{colors.day-primary-soft}"
    textColor: "{colors.day-primary}"
    rounded: "{rounded.tab}"
    padding: "5px 10px"
  night-button-primary:
    backgroundColor: "{colors.night-primary}"
    textColor: "{colors.night-primary-ink}"
    rounded: "{rounded.control}"
    padding: "10px 14px"
  night-button-primary-hover:
    backgroundColor: "{colors.night-primary-hover}"
    textColor: "{colors.night-primary-ink}"
    rounded: "{rounded.control}"
    padding: "10px 14px"
  night-button-secondary:
    backgroundColor: "{colors.night-primary-soft}"
    textColor: "{colors.night-primary}"
    rounded: "{rounded.control}"
    padding: "10px 14px"
  night-button-quiet:
    backgroundColor: "transparent"
    textColor: "{colors.night-muted}"
    rounded: "{rounded.control}"
    padding: "10px 14px"
  night-button-text:
    backgroundColor: "transparent"
    textColor: "{colors.night-primary}"
    rounded: "{rounded.control}"
    padding: "4px 0"
  night-field:
    backgroundColor: "{colors.night-field}"
    textColor: "{colors.night-ink}"
    rounded: "{rounded.field}"
    padding: "9px 10px"
  night-panel:
    backgroundColor: "{colors.night-surface}"
    textColor: "{colors.night-ink}"
    rounded: "{rounded.panel}"
    padding: "18px"
  night-status-badge:
    backgroundColor: "{colors.night-field}"
    textColor: "{colors.night-muted}"
    rounded: "{rounded.badge}"
    padding: "4px 7px"
  night-status-badge-success:
    backgroundColor: "{colors.night-success-soft}"
    textColor: "{colors.night-success}"
    rounded: "{rounded.badge}"
    padding: "4px 7px"
  night-preview-tab-active:
    backgroundColor: "{colors.night-primary-soft}"
    textColor: "{colors.night-primary}"
    rounded: "{rounded.tab}"
    padding: "5px 10px"
---

# Design System: Genjustsu Pro

## Overview

**Creative North Star: "The Contemporary Production Folder"**

Porcelain surfaces, forest actions and brushed-silver edges create the daytime desk. Petroleum surfaces and citron actions create the nighttime desk. Both use the same proportions, precise inset fields and restrained frame brackets; the media remains the central object. The user explicitly rejects a uniformly black science-fiction dashboard.

This is a compact working environment with deliberate hierarchy rather than decorative telemetry. Manrope gives Latin headings and the brand a distinct voice; native Chinese and body typography preserve familiar reading and control behavior. Appearance changes only UI tokens, preserving entered materials, playback and ongoing work.

**Key Characteristics:**
- Two intentional working environments sharing one component grammar.
- Local Manrope headings and brand, with native bilingual body and controls.
- Fine edges, inset fields, rounded folders and restrained media-frame brackets.
- Visible task state with optional detail, internal inspector scrolling and anchored generation actions.

## Colors

Frontmatter records separate `day-*` and `night-*` primitives. These map to the same CSS custom-property suffix: `day-primary` is `--primary` at `:root`, and `night-primary` is `--primary` at `:root[data-theme="dark"]`. Components consume the active custom property rather than choosing their own palette.

### Primary

- **Forest action / citron action** (`day-primary`, `night-primary`): primary buttons, selected inspection controls, links and active task markers. Their hover, ink and soft companions travel together.
- **Citron seal** (`day-accent`, `night-accent`): the small Pro mark, with its paired accent ink.

### Neutral

- **Porcelain / petroleum** (`*-ground`, `*-surface`, `*-rail`, `*-header`): page, working panels, history-tone role and toolbar layers.
- **Reading ink / annotation ink** (`*-ink`, `*-muted`): main text and explanatory copy.
- **Inset field / silver edge** (`*-field`, `*-line`, `*-line-strong`): controls, separators and stronger upload/frame outlines.
- **Media well / loaded media** (`*-media`, `*-media-loaded`): empty frame and contain-fit video surround.
- **Approved green**, **failure coral** and **warning ochre** (`*-success`, `*-danger`, `*-warning`, each with `*-soft`): semantic foreground/background pairs, not additional brand accents.
- **Focus ink** (`*-focus`): keyboard outlines in the active environment.

**The Paired Environment Rule.** Resolve every semantic color through the active theme. A light surface or primary color must never be copied into night mode without its paired role.

**The Reading Ink Rule.** Use muted ink for secondary copy, not reduced opacity. Keep semantic states named in text as well as color.

## Typography

**Display Font:** Locally served variable Manrope (weights 200–800, `font-display: swap`), with explicit Chinese sans fallbacks. The asset is covered by SIL Open Font License; retain its bundled license when distributing it. **Body Font:** Native platform sans with explicit Chinese fallbacks. **Measurement Font:** Native monospace for elapsed time.

### Hierarchy

- **Headline:** the frontmatter headline role for the workspace title; compact desktop uses (23px), mobile (22px).
- **Brand:** the frontmatter brand role; mobile reduces to (15px). The small Pro seal uses native (11px), weight (650).
- **Title:** base section headings use the title role; inspector headings use (13px), execution and review headings (12px). Empty-state titles use native (18px), weight (550).
- **Body:** the body role is the inherited baseline; most explanatory copy uses (12px), with helper copy at (11px) and line-height (1.65–1.8).
- **Label:** the label role describes material controls; tabs, status badges and toolbar appearance labels use (11px). Keep natural bilingual case rather than imposed capitals.
- **Elapsed:** the elapsed role and tabular numeric metadata support measurement without becoming decoration.

**The Two Voices Rule.** Use Manrope for the brand and workspace heading; retain native bilingual sans for operational copy and controls. Reserve monospace for elapsed time.

## Layout

Desktop Studio is a viewport-height working plane from (900px) upward. A horizontal toolbar sits above the title, compact execution strip and two-column workbench. Main content is centered with a maximum width of (1840px) and default padding (24px 28px 20px). The viewer occupies the flexible left column; the inspector is (334px) with an (18px) gutter. At (1650px) upward the inspector becomes (360px), gutter (22px), inspector padding (22px). At (1099px) and below, it becomes (300px), gutter (14px), page padding (18px).

The inspector is a bounded flex column: only its inner materials/options area scrolls, while the generation footer remains outside that scroll area with a top divider. The resolution control is (86px) wide beside a flexible generation action. The viewer is also bounded and may scroll internally when review/result content requires it. Desktop video fills available space with `object-fit: contain`; its empty frame brackets disappear when video is present.

At desktop heights of (820px) or less, the toolbar reduces from (68px) to (58px); title, gutters and panel spacing compact. The source drop target becomes (66px) minimum height. Preparation uses a (32px) minimum-height button with (7px 12px) padding; source cost copy uses a (4px) top margin and (1.5) line-height. Advanced disclosure margins become (8px 0), section-divider margins (10px 0), reference uploads (62px) minimum height with (10px) padding, and creative-options top margin (6px). These reductions keep the collapsed disclosure summary visible while retaining the anchored generation footer. At desktop heights of (760px) or less, the toolbar further reduces to (54px), main vertical padding becomes (12px), and workspace subtitle plus secondary execution description are hidden to preserve editing space.

At widths (900–1099px), the later media rule sets its minimum height to (150px); the general desktop minimum is (140px). Prioritize checks at 1024×768, 1280×720, 1366×768, 1440×900 and 1920×1080.

At (760px) and below, toolbar controls wrap, secondary toolbar labels and theme labels condense, and viewer then inspector stack naturally. Media is bounded between a (260px) minimum and (400px) maximum; steps become four columns. Widths (761–899px) retain the two-column grid but use ordinary document flow, rather than the desktop height lock. Mobile history width is viewport minus (32px), and settings key rows stack.

## Elevation & Depth

A hybrid of flat tonal planes and fine edges establishes structure. Inputs are inset through fill and border rather than inner shadows. Frame brackets and stronger outline ink give the empty viewer a production-folder character. Floating history and toasts share the theme-specific ambient shadow: day `0 12px 36px rgb(22 48 36 / 14%)`, night `0 12px 36px rgb(2 15 19 / 30%)`.

**The Working Plane Rule.** Keep working panels flat. Reserve the ambient shadow for floating history and transient feedback.

## Shapes

Large folders use the panel radius; execution and toast surfaces use the execution radius. Buttons, uploads, review blocks and media wells share the control radius. Fields, tabs and badges step down deliberately. Fine solid edges define fields and dividers; the source drop target alone uses a dashed outline. Inline SVG icons normally use (19px) boxes and (1.65px) rounded strokes. Circular execution markers express real state; the plus/minus disclosure indicator is a text affordance, not an icon system.

## Components

### Buttons

Compact, gently rounded and direct. Primary uses the theme's primary/primary-ink pair; secondary uses primary-soft/primary; quiet is transparent with muted ink; text actions use primary ink with minimal padding. Base padding is (10px 14px), gap (8px), weight (550). Hover changes fill/ink over (180ms); enabled active controls move down (1px). Disabled opacity is (.48). Focus uses a (2px) active-theme outline offset (3px). The generation action is (36px) minimum height beside resolution.

### Inputs / Fields

Inset theme fill and one-pixel divider edge, (9px 10px) padding, field radius, native (12px) type. Selects have a (36px) minimum height. Prompt textareas start at (105px), resize vertically and use (1.65) line-height. Invalid fields receive the danger outline and adjacent named feedback. File targets retain real inputs and focus-within outlines; filenames may wrap anywhere. Requirements precede upload; validation covers format, size and video duration before submission.

### Navigation

The top toolbar exposes task creation, history, paired day/night selection, language and keys. Appearance uses an inset segmented group with surface/ink selected state and `aria-pressed`. Theme choice persists locally and is applied before stylesheet paint; absent a stored choice, system appearance seeds it. History is a floating (330px) drawer rather than a permanent rail, with selected tasks in primary-soft/primary, truncated filenames and secondary metadata. Outside click and Escape close it; its close action returns focus to the trigger.

### Chips / Status

Neutral badges use field/muted and approved badges use success-soft/success. Small rounded rectangles use (4px 7px) padding and native (11px) type. The model label is a compact outlined annotation with tabular figures, hidden on mobile.

### Cards / Containers

Viewer and inspector use unshadowed surface fills and the panel radius. The viewer has default padding (17px 20px 12px), inspector (18px), with compact responsive overrides. Settings uses the same material, capped at (760px), with provider sections divided by fine rules. Loaded video remains contain-fit with native playback controls; available media tabs expose `aria-pressed` and retain playback time where metadata permits.

### Execution and Review

The compact strip always carries current state, actual stage count and desktop elapsed time. Detailed stages begin collapsed behind an `aria-expanded` control. Real backend stages drive completion, active, waiting and error markers; no fabricated percentage appears. Main execution rings rotate at (1s), stage rings at (1.2s); the thin status bar pulses over (1.7s). Reduced-motion preference removes animation and transitions while retaining textual state. Unchanged polling preserves strip position.

Review uses primary-soft with a native checkbox and explicit approval; success blocks use success-soft. Original audio and paid-generation explanation remain adjacent to their relevant workflow action. Theme and language changes preserve source materials and user-entered prompt content.

### Upload Targets and Feedback

Source upload is centered and dashed; reference upload is a compact horizontal solid-edged row with optional thumbnail. Both use field fill, stronger edges and a primary-soft hover. Toasts float at top right, use danger or success semantic pairs, include a real close control, and use alert/status roles appropriately. Errors persist for (14s), success for (5s); hover pauses dismissal, mouse leave grants (8s). Matching field-level errors remain available beside the upload control.

## Do's and Don'ts

### Do:
- **Do** resolve all UI colors through the active day/night semantic pair.
- **Do** keep the generation footer outside the scrolling inspector on desktop.
- **Do** use inline stroked SVG for interface icons and native video controls for inspection.
- **Do** preserve entered prompts, source media and ongoing task state when switching appearance or language.
- **Do** keep constraints near uploads and errors readable in both field feedback and dismissible toasts.

### Don't:
- **Don't** turn night mode into a uniformly black science-fiction dashboard.
- **Don't** add shadows to every working panel; reserve them for floating history and toasts.
- **Don't** invent completion percentages, decorative metrics or pipeline states.
- **Don't** replace Manrope headings with a system display face or apply Manrope to all operational copy.
