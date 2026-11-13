# Recovery and execution monitor verification

## Fixed behavior

A local polling transport failure no longer loses a paid Replicate prediction. The server persists prediction IDs and terminal status, retries safe reads, reuses completed artifacts and reconnects to the same cloud job. Prediction creation is sent once; ambiguous submissions preserve a marker and block another paid call. A new attempt requires a provider-confirmed failed/canceled state and an explicit user action.

The page shows actual processing stages, cloud queue/running state, task elapsed time and completed-step count. Errors and recovery controls sit in the sticky execution monitor. Human review is a waiting state, not a running spinner. Narrow screens reveal the current stage when it changes while preserving manual horizontal scroll between polls.

Original-footage mask repair retains existing depth segmentation coverage and fills enclosed holes, avoiding replacement with an RGB-only mask that can omit clothing. Changed guidance carries a new preview version and invalidates approval. Prompt contents remain independent of interface language.

## Evidence

- Reconnected a real existing depth prediction after local polling had stopped. The same successful task and downloaded depth were reused.
- Completed a real SAM preparation and original-footage mask repair. Reviewed all 717 guidance frames plus browser playback before approval.
- Tested source/reference loading, preview tabs, approval, direct 720p submission, task persistence, bilingual UI, narrow-screen state visibility, and invalid empty-key validation in actual Chrome. Empty-key validation rejects before writing Keychain.
- 30 isolated offline tests pass, including unchanged upstream prompt contracts, source-audio packet preservation, duration alignment, no automatic duplicate submission, cached-depth reuse, transient safe-read recovery, ambiguous-submit blocking, repair-path recovery and mask-hole filling.

## Live result

The existing paid generation completed successfully. Local restart recovery continued the saved DreamAPI task ID. The source was 29.895 seconds; generation returned 721 frames at 720×1280/24fps, and the aligned export contains 717 frames with the complete original soundtrack. All 1289 compressed audio packets match the source byte for byte. The browser played through the full exported clip and reported the download complete; downloaded bytes match the local export. Only one DreamAPI generation record was created.

This validates one single-subject Depth + SAM workflow with an image identity reference at 720p. It does not establish quality across all subjects, fast/combined mesh modes or other resolutions. Replicate queue and inference time can dominate preparation latency; HTTP 200 on a status read means the request succeeded, not that the cloud job finished. Fine facial likeness and lip-sync remain visual judgments, not guarantees from a successful status.


## Day/night Studio iteration

The PC-first layout was inspected in actual Chrome at 1024×768, 1280×720, 1366×768, 1440×900 and 1920×1080, in both appearances. Document bounds matched each viewport, with generation and download controls visible. Advanced settings scroll within the inspector while the output controls stay anchored. Theme changes preserve selected material, prompt contents and the current media URL/frame; saved appearance restores on reload. Native body/CJK typography is paired with the locally hosted Manrope heading face (SIL OFL).

Browser file-picker checks rejected an empty file, a one-second source, a source above 500 MB, and a six-second source combined with a 29-second identity video. A valid six-second video was accepted for local preview. Field feedback and dismissible toasts were checked in both languages; only UI wording changes on language switches. Audio-track validation remains authoritative on the server before a paid worker can start. No new paid generation was submitted in this appearance iteration.

The desktop appearance and upload checks were completed without additional paid generation calls. Core workflow prompt contents remain independent of interface language.
