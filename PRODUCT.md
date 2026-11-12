# Genjustsu Pro
<!-- impeccable:product-schema 1 -->

## Platform
web

## Users
A single creator running the application locally on macOS or Windows to recast people in short videos.

## Product Purpose
Upload a source video and character references, prepare motion guidance, review it, generate a finished video with DreamAPI Seedance 2.5, and download with original audio.

## Operating Context
Local single-user browser app, Python FastAPI backend. Keys are entered on the page and stored in macOS Keychain or Windows Credential Manager. The user authorizes implementation and upload to Hy-1990/Genjustsu-Pro.

## Capabilities and Constraints
Retain depth + SAM, fast face mesh, and combined preparation. Replicate provides Demucs, depth, and SAM. Human input review precedes generation. Generate the selected resolution in one paid operation, without draft upgrades. DreamAPI supports real-person references, confirmed by the user. Preserve complete source audio. Chinese and English UI. Language switching changes interface labels only; core workflow instructions retain upstream wording, and user-entered prompts retain their content. No social publishing or promotional content.

## Brand Commitments
Name Genjustsu Pro. The user rejects a uniformly black science-fiction dashboard and asks for intentional day/night appearances, stronger visual craft, a PC-first single-screen Studio, and clear upload requirements/toasts. Prioritize 1366×768, 1440×900 and wider desktop displays. The user delegates this iteration while at lunch.

## Evidence on Hand
Upstream working pipeline, isolated offline tests, and a real 29.9-second depth/SAM plus image-reference workflow completed at 720p, with source-audio packet equality, browser playback/download and same-task restart recovery verified. Other live mode/resolution combinations remain unverified.

## Product Principles
- Keep source performance and original audio central.
- Make processing stages and failures understandable.
- Keep keys out of files, URLs, logs, and repository history.
- Never repeat an ambiguous paid submission automatically.
