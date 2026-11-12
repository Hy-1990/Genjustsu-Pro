---
name: Genjustsu Pro
description: A dark bilingual video workbench with truthful execution telemetry.
colors:
  ink: "#e4edf7"
  muted: "#9cacc1"
  surface: "#0d1622"
  ground: "#060b12"
  rail: "#08111c"
  line: "#223143"
  primary: "#83d9e9"
  primary-hover: "#b2eef6"
  primary-soft: "#142f3a"
  success: "#8cddb1"
  success-soft: "#102820"
  danger: "#ffabb1"
  danger-soft: "#2c1822"
  primary-ink: "#07121a"
  secondary: "#172638"
  secondary-hover: "#21364a"
  field: "#0a131f"
  field-border: "#30465f"
  focus: "#70b6d0"
  media-ground: "#09111b"
  media-dark: "#03070b"
  execution: "#0a1420"
  execution-border: "#2c4055"
typography:
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.6
  title:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "15px"
    fontWeight: 650
    lineHeight: 1.6
  subheading:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "14px"
    fontWeight: 600
    lineHeight: 1.6
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: 1.6
  button:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "14px"
    fontWeight: 550
    lineHeight: 1.4
  headline:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif"
    fontSize: "25px"
    fontWeight: 650
    lineHeight: 1.4
    letterSpacing: "-.025em"
  elapsed:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  badge: "4px"
  tab: "5px"
  field: "7px"
  control: "8px"
  panel: "12px"
spacing:
  tight: "4px"
  small: "8px"
  field: "10px"
  compact: "12px"
  section: "16px"
  panel: "20px"
  gutter: "24px"
  page: "32px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-ink}"
    rounded: "{rounded.control}"
    padding: "10px 15px"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.primary-ink}"
    rounded: "{rounded.control}"
    padding: "10px 15px"
  button-secondary:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "10px 15px"
  button-quiet:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "10px 15px"
  button-text:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    rounded: "{rounded.control}"
    padding: "4px 0"
  field:
    backgroundColor: "{colors.field}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "9px 10px"
  panel:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "20px"
  status-badge:
    backgroundColor: "{colors.media-ground}"
    textColor: "{colors.muted}"
    rounded: "{rounded.badge}"
    padding: "3px 8px"
  status-badge-success:
    backgroundColor: "{colors.success-soft}"
    textColor: "{colors.success}"
    rounded: "{rounded.badge}"
    padding: "3px 8px"
  preview-tab-active:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.primary}"
    rounded: "{rounded.tab}"
    padding: "5px 10px"
  execution-panel:
    backgroundColor: "{colors.execution}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "17px 20px 14px"
---

# Design System: Genjustsu Pro

## Overview

**Creative North Star: "The Execution Observatory"**

Near-black blue working surfaces, icy cyan actions and fine vector rules translate the user-pinned NEXUS telemetry direction into a compact local video tool. Pale text and restrained semantic color support precise inspection without competing with the media.

The visual language is operational: measured time, completed-stage counts and connected phase markers describe real work. Native bilingual controls and visible recovery preserve a professional, simple interface. No reference artwork or external font asset is shipped.

**Key Characteristics:**
- Near-black tonal layers with icy cyan action and selection.
- Compact native typography; monospace reserved for elapsed measurement.
- Thin connected stages with motion tied to actual execution.

## Colors

The palette is a cool dark field with one working accent; frontmatter records the actual CSS values.

### Primary

- **Icy cyan** (`primary`, `primary-hover`): primary actions, links and active work.
- **Deep cyan selection** (`primary-soft`): selected media tabs, provider tiles and transient feedback.
- **Night ink** (`primary-ink`): legible text on bright primary buttons.

### Neutral

- **Pale reading ink** (`ink`) and **slate annotation** (`muted`): main text and secondary explanation.
- **Near-black ground** (`ground`), **dark task rail** (`rail`), **blue-black surface** (`surface`) and **fine divider** (`line`): flat structural layers.
- **Secondary control** (`secondary`, `secondary-hover`): supporting filled actions.
- **Inset field** (`field`), **field edge** (`field-border`) and **focus cyan** (`focus`): input fill, boundary and keyboard focus.
- **Media well** (`media-ground`, `media-dark`): empty and loaded media respectively.
- **Execution field** (`execution`, `execution-border`): the persistent state panel and its outline.
- **Approved green** (`success`, `success-soft`) and **failure rose** (`danger`, `danger-soft`): semantic status pairs rather than additional brand accents.

**The State Color Rule.** Cyan marks action, selection and active work; green marks approved or complete states; rose marks actionable failure. Every pipeline state also has text.

## Typography

**Body and Control Font:** Native platform sans with explicit Chinese fallbacks, as recorded in frontmatter. **Measurement Font:** `ui-monospace, SFMono-Regular, Consolas, monospace`, used only for elapsed time. No external font asset is loaded.

The compact hierarchy suits an Operate surface. The workspace heading uses the headline token, decreasing to (22px) below (950px), then (21px) below (620px). Panel titles use the title token; review subheadings use subheading. Body defaults to (14px); most labels, helpers, fields and media tabs use (12px). Execution titles use (15px), weight (600), becoming (13px) on mobile. Elapsed measurement becomes (12px) on mobile. Stage-state annotations use (11px). Numeric metadata uses tabular figures. Helper line-heights range from (1.7–1.9), with long workflow and settings explanations limited to (70ch).

**The Measurement Rule.** Use monospace for elapsed measurement; use the native bilingual sans stack for workspace titles, labels and controls.

## Layout

The desktop shell has a sticky full-height task rail (216px), top bar (70px minimum), and centered main region (1700px maximum). Main padding is (24px 28px 32px). Materials occupy (300–355px) beside a flexible viewer, separated by (24px); at widths of at least (1650px), materials become (385px). The execution panel spans the work area above the two columns and sticks below the top bar. The viewer sticks at (290px) on desktop.

At (1180px) and below, the rail narrows to (184px), main padding to (24px), panels to (16px), and materials to (270–310px) with a (16px) gutter. At (950px) and below the rail becomes (170px), the workbench becomes one column, and the viewer stops sticking. Materials lead until guidance exists; then the viewer leads for inspection.

At (620px) and below, the rail becomes a top section with brand, new-task action and horizontally scrolling history. The top bar is (52px minimum), with execution sticking below it. Main padding is (21px 16px 28px). Execution descriptions and secondary stage annotations are hidden, but phase labels remain. The phase strip scrolls horizontally; changed state reveals the current, failed or waiting phase, while unchanged polling preserves its position. Settings input/save rows stack and provider headings wrap. Chinese and English share the same layout.

The media well has a (16:10) aspect ratio and contain-fit native video. Its minimum height is (280px), overridden to (290px) at compact desktop, (260px) at single-column widths and (220px) on mobile. Desktop video and stage maximum height is `min(46vh, 480px)`; mobile caps both at (360px). Repeated small spacing increments form a compact working rhythm.

## Elevation & Depth

Flat surfaces use subtle dark tonal differences and one-pixel borders. Fields sit within panels and media sits within an inset well. The only shipped shadow is the fixed toast: `0 7px 25px rgb(0 0 0 / 15%)`, separating transient feedback from the work below.

**The Tonal Separation Rule.** Panels stay flat at rest; fine borders and dark tonal layers establish containment. Toasts alone use the shipped floating shadow.

## Shapes

Large panels have gently rounded corners using the panel token. Buttons, uploads, media wells and state blocks share the control radius; fields use the field radius, tabs the tab radius, and badges and thumbnails the badge radius. Fine solid borders define containment; the source drop target uses a dashed border. Pipeline markers are circular and connected by fine rules. Icons are inline stroked SVG, generally (20px) with (1.7px) strokes.

## Components

### Buttons

Compact and direct. Primary actions use bright cyan with dark text. Supporting actions use the dark secondary fill; quiet actions are transparent and text actions have minimal padding. Base padding is (10px 15px) with an (8px) gap; generation has a (43px) minimum height. Hover changes fill or text; transitions last (160ms). Disabled opacity is (.55) with a not-allowed cursor. Keyboard focus is a (3px) cyan outline offset by (3px).

### Inputs / Fields

Dark inset fills, fine blue edges and (9px 10px) padding. Fields use (12px) type; selects have a (39px) minimum height. The prompt textarea has a (110px) minimum height, vertical resize and (1.75) line-height. Real file inputs remain inside labeled upload targets with focus-within outlines. The source target is (110px) minimum height; after guidance it condenses to (72px). Reference uploads retain the local filename or localized saved-reference identity after language changes, including video references without thumbnails.

### Navigation

Recent tasks are stacked rail buttons, with a blue selected fill and pale cyan text. Filenames truncate and metadata stays beneath. Mobile history scrolls with items (145–180px) wide. The slim top bar offers language and API-key settings; settings replaces the workbench inline and focuses the DreamAPI password field.

### Status Badges and Containers

Small neutral badges use the media-ground fill. Configured, approved and complete states use green. Materials, viewer and settings use dark bordered panels. Settings has a (760px) maximum width and (25px 28px) desktop padding, with provider sections divided by a fine rule. Saved keys appear only as connection status. Errors use rose text on a dark rose block. Toasts use pale text on the deep cyan fill.

### Execution Sequence

The signature panel combines a real stage count, elapsed time and connected phase markers. The initial eight-phase sequence is upload, vocals, depth, masks, guidance, review, generation and audio restoration; actual job phases come from the backend, including face tracking when applicable. Completed phases use green checks; active phases use cyan rotating rings; human review uses a cyan outlined waiting marker; failure uses rose. No synthetic completion percentage is shown. Error and recovery actions remain inside this panel.

The main work indicator spins at (1s linear); active phase rings at (1.2s linear). The thin work bar pulses opacity from (.35) to (1) over (1.7s ease-in-out). Reduced-motion preference removes animation and transitions, retaining visible state and a (.6) opacity bar. Motion represents actual work, not decoration.

### Media Inspection and Review

Media tabs use neutral text, with deep cyan fill and cyan text when selected. Available Original, Guidance, Depth, Mask and Result views depend on real files. Tabs expose `aria-pressed`; switching retains playback time where metadata permits, clamped to duration. Review is an adjacent tinted block with a native checkbox, approval and conditional re-segmentation. Approved and completed messages use green-tinted blocks. Native video controls remain available; paid-action explanations stay with the action.

## Do's and Don'ts

### Do:
- **Do** use icy cyan for primary actions and selected inspection controls.
- **Do** pair stage colors with explicit text and distinct markers.
- **Do** let Chinese and English labels wrap where space is constrained.
- **Do** reveal the current, failed or review stage when pipeline state changes.
- **Do** retain native video controls and the current inspection time when metadata permits.

### Don't:
- **Don't** make all actions primary; use secondary, quiet and text treatments for supporting actions.
- **Don't** add decorative network graphs, invented metrics or fabricated completion percentages.
- **Don't** apply container shadows; separation comes from tone and fine borders.
- **Don't** restart pipeline animation or reset horizontal position during unchanged polling.
- **Don't** use the elapsed-time monospace as a display or body font.
