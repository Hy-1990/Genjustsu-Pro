# Genjustsu Pro refactor
Date: 2026-11-11

## Intent
A professional bilingual local character replacement tool backed by the user's DreamAPI.

## Constraints
Keep existing preprocessing and original-audio restoration. Remove draft mode. macOS single-user. Page-configured secrets stored in Keychain. Publish to Hy-1990/Genjustsu-Pro.

## Key decisions
- Keep FastAPI and local media processing to reuse the functioning pipeline.
- Replace Enhancor and public temporary hosts with DreamAPI generation and storage.
- Retain Replicate for preprocessing.
- User confirms real-face support on DreamAPI.
- User asks work to continue while they go home. Remaining design and reversible implementation choices are delegated.

## Open questions
Live provider balances and input-specific generation quality require the user's own authorized test.
