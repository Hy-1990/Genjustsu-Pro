# Genjustsu Pro
<!-- impeccable:product-schema 1 -->

## Platform
web

## Users
A single creator running the application locally on macOS to recast people in short videos.

## Product Purpose
Upload a source video and character references, prepare motion guidance, review it, generate a finished video with DreamAPI Seedance 2.5, and download with original audio.

## Operating Context
Local single-user browser app, Python FastAPI backend. Keys are entered on the page and stored in macOS Keychain. The user authorizes implementation and upload to Hy-1990/Genjustsu-Pro.

## Capabilities and Constraints
Retain depth + SAM, fast face mesh, and combined preparation. Replicate provides Demucs, depth, and SAM. Human input review precedes generation. Generate the selected resolution in one paid operation, without draft upgrades. DreamAPI supports real-person references, confirmed by the user. Preserve complete source audio. Chinese and English UI. Language switching changes interface labels only; core workflow instructions retain upstream wording, and user-entered prompts retain their content. No social publishing or promotional content.

## Brand Commitments
Name Genjustsu Pro. Professional and simple working interface. The user delegates remaining implementation decisions while away.

## Evidence on Hand
Upstream working pipeline and local offline tests. No independently verified new DreamAPI generation yet.

## Product Principles
- Keep source performance and original audio central.
- Make processing stages and failures understandable.
- Keep keys out of files, URLs, logs, and repository history.
- Never repeat an ambiguous paid submission automatically.
