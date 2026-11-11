---
name: Genjustsu Pro
description: A compact bilingual workspace for inspecting and recasting short videos.
colors:
  ink: "#1d2d46"
  muted: "#59697e"
  surface: "#ffffff"
  ground: "#f5f7fa"
  rail: "#eaf0f8"
  line: "#dce3ed"
  primary: "#2357aa"
  primary-hover: "#194589"
  primary-soft: "#e8effc"
  success: "#246843"
  success-soft: "#eff7f1"
  danger: "#a73236"
  danger-soft: "#fff1f1"
  secondary: "#eef2f7"
  secondary-hover: "#e0e7f0"
  field-border: "#c8d2df"
  focus: "#8daef0"
  media-ground: "#edf1f6"
  media-dark: "#18212e"
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
    textColor: "{colors.surface}"
    rounded: "{rounded.control}"
    padding: "10px 15px"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.surface}"
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
    backgroundColor: "{colors.surface}"
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
---

# Design System: Genjustsu Pro

## Overview

**Creative North Star: "The Technical Product Catalog"**

Cool stone surfaces, deep blue ink and restrained cobalt selection give this local video tool the calm precision of a technical product catalog. The interface is compact and task-led: media, controls and processing state share a working surface.

White containers separate editable materials from inspection. Standard web controls, bilingual labels and explicit status text keep the visual language practical. Color distinguishes action, selection, success and failure; it does not decorate the workspace.

**Key Characteristics:**
- Cool neutral layers with cobalt action and selection.
- Compact, aligned controls and readable media.
- State and recovery adjacent to the task.

## Colors

The palette combines cool paper neutrals with restrained working blue; the frontmatter records the shipped values.

### Primary

- **Cobalt action** (`primary`, `primary-hover`): primary buttons, links, current workflow step and focus-related accents.
- **Pale cobalt selection** (`primary-soft`): active media tabs and provider identity tiles.

### Neutral

- **Deep blue ink** (`ink`): headings, fields and primary reading text.
- **Slate annotation** (`muted`): labels, helper copy, timing and metadata.
- **White working surface** (`surface`): materials, preview, settings and top bar.
- **Cool stone ground** (`ground`), **blue task rail** (`rail`) and **fine divider** (`line`): structural layers.
- **Secondary control** (`secondary`, `secondary-hover`): supporting filled actions.
- **Field edge** (`field-border`) and **focus blue** (`focus`): editable control boundaries and keyboard focus.
- **Media ground** (`media-ground`, `media-dark`): empty media and loaded video stage respectively.

### Semantic States

- **Approved green** (`success`, `success-soft`): configured services, approved guidance and completed output.
- **Failure red** (`danger`, `danger-soft`): errors and saved-key removal.

**The State Color Rule.** Cobalt marks action and selection; green marks approved or complete states; red marks actionable failure. Every state also has text.

## Typography

**Body and Control Font:** Native platform sans with explicit Chinese fallbacks, as recorded in frontmatter. No external font asset is loaded.

The shipped hierarchy is compact and functional. Body defaults to the body token; most working labels, helpers, metadata and fields use (12px). Section titles use the title token; review subheadings use subheading. Main buttons inherit the body size, while settings actions and media tabs use (12px). Numeric metadata uses tabular figures. Helper copy ranges from (1.7–1.9) line-height; workflow and settings explanations stop at (70ch).

**Observed exception, not canonized:** the current page heading uses the system stack at (25px), weight (650), line-height (1.4) and tracking (-.025em), stepping to (22px) and (21px) at narrower widths. System display typography is recorded as a carried craft-floor exception, not a reusable display-font prescription.

## Layout

The desktop shell has a sticky full-height task rail (216px), white top bar (70px minimum), and centered main region (1700px maximum). Main padding is (29px 32px 36px). The workbench pairs a materials column (300–355px) with a flexible viewer, separated by (24px); at widths of at least (1650px), the materials column becomes (385px). This is the shipped interpretation of the provisional 360px direction.

At (1180px) and below, the rail narrows to (184px), page padding to (24px), panels to (16px), and the materials column to (270–310px) with a (16px) gutter. At (950px) and below the rail becomes (170px) and the workspace becomes one column. Initial and source-only states keep materials first. Once the job includes guidance, the preview moves to the first grid row.

At (620px) and below, the rail becomes a top section with brand and new-task action, then horizontally scrolling recent tasks. The local footer is hidden; the top bar is (52px minimum). Main padding is (21px 16px 28px). Step labels wrap; the model annotation is hidden. Settings input/save rows stack vertically, provider headings wrap, and the settings container uses (18px) padding. The same layouts serve Chinese and English; copy is translated rather than styled as separate identities.

The viewer uses a (16:10) stage with contain-fit native video. Its minimum height steps from (330px) through (290px), (260px) and (220px); below (950px) its maximum stage height is (420px). Video has a (610px) maximum height. Primary containers use (20px) padding on wide screens. Spacing uses repeated small increments rather than a rigid mathematical scale.

**The Task Order Rule.** At single-column widths, materials lead until guidance exists; then the viewer leads for inspection.

## Elevation & Depth

The interface is flat and uses tonal layering, fine one-pixel borders and whitespace. Media sits within the panel; fields do not float. The only shipped shadow is the fixed toast: `0 7px 25px rgb(0 0 0 / 15%)`. It separates transient feedback from the work below.

**The Tonal Separation Rule.** Panels stay flat at rest; fine borders and neutral fills establish containment. Toasts alone use the shipped floating shadow.

## Shapes

Large panels have gently rounded corners (panel token). Buttons, upload zones, media stages and state blocks share the control radius. Fields use the field radius; tabs use the tab radius; status badges and reference thumbnails use the badge radius. Fine solid borders define containers and inputs; the source upload target has a dashed border. Workflow numbers and small connection markers are circular. Icons are inline stroked SVG, generally (20px) with (1.7px) strokes, scaled down for metadata actions.

## Components

### Buttons

Compact and direct. Primary buttons use cobalt with white text; supporting preparation uses the pale secondary treatment. Quiet toolbar buttons are transparent; text actions are blue with minimal padding and an underline on hover. Base controls use (10px 15px) padding and an (8px) internal gap. Generation spans the materials column with a (43px) minimum height. Hover changes primary and secondary fills; quiet buttons adopt the rail fill. Background and text transitions last (160ms). Disabled buttons have opacity (.48) and a not-allowed cursor. Keyboard focus is a (3px) focus-blue outline offset by (3px).

### Inputs / Fields

White surfaces, fine field edges and compact (9px 10px) padding. Text inputs, selects and textareas use (12px) type; selects have a (39px) minimum height. The prompt textarea has a (110px) minimum height, vertical resize and (1.75) line-height. File inputs remain real controls inside labeled upload targets; focus-within outlines expose their focus. Upload hover changes fill and border to blue. Reference uploads show a small thumbnail or SVG, a descriptive label and supporting text.

### Navigation

Recent tasks are stacked buttons in the desktop rail, with a pale blue selected fill and darker blue text; filenames truncate, metadata remains beneath. On mobile the list scrolls horizontally with items (145–180px) wide. The top bar always offers language switching and API-key settings. Settings replaces the workspace inline and offers a text back action; opening it focuses the DreamAPI password field.

### Status Badges and Workflow

Compact neutral badges communicate waiting and review states. Configured, approved and completed states use the green variant. Three numbered steps show current cobalt and completed green treatments. Progress uses a slim pulsing bar (1.7s ease-in-out); reduced-motion preference removes animation and transitions, leaving the bar at (.6) opacity. Errors use a red-tinted local block and recovery action when available. Transient feedback appears in a centered bottom toast.

### Containers and Settings

White bordered panels group materials, viewer and model-service settings. Settings has a (760px) maximum width and (25px 28px) desktop padding. DreamAPI and Replicate sections are separated by a fine divider; each contains a role description, connection status, password field, save action, provider link and conditional removal action. A muted explanatory block describes macOS Keychain storage. Settings shows connection status rather than saved secrets. DreamAPI generation and Replicate preprocessing are named adjacent to their relevant controls.

### Media Inspection and Review

Media tabs are compact rounded buttons with neutral text; the active tab has pale cobalt fill and cobalt text, with `aria-pressed` state. Available Original, Guidance, Depth, Mask and Result views depend on real job files. Switching preserves playback time after metadata loads, clamped to the new duration. The footer labels the view and offers a download link. Guidance review is an adjacent tinted block with a native checkbox, approval action and conditional re-segmentation action. Approval is disabled until the checkbox is checked. Approved and completed messages use green-tinted blocks; paid-action guidance stays with the action.

## Do's and Don'ts

### Do:
- **Do** use cobalt for primary actions and selected inspection controls.
- **Do** pair status colors with explicit text.
- **Do** let Chinese and English labels wrap where space is constrained.
- **Do** keep review, progress and recovery beside the viewer.
- **Do** retain native video controls and the current inspection time when metadata permits.

### Don't:
- **Don't** make all actions primary; use secondary, quiet and text treatments for supporting actions.
- **Don't** apply container shadows; separation comes from tone and fine borders.
- **Don't** put an empty viewer ahead of materials in the single-column initial state.
- **Don't** hide guidance behind the materials once guidance exists in the single-column workspace.
- **Don't** infer successful paid generation from the synthetic review screenshots.
