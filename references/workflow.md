# Guided workflow contracts

Use only the current stage section in user-facing interaction. The full sequence belongs to the Skill, not to the user.

Each stage has five fields:

- **Enter when:** required prior gate.
- **Skill acts:** work performed without asking the user to manage it.
- **Ask now:** only the minimum current input.
- **Deliver:** artifact that proves the stage work happened.
- **Gate:** explicit approval required before transition.

## START

**Enter when:** the Skill is invoked.

**Skill acts:** locate or initialize `PROJECT_STATE.json`; inspect only the supplied project scope; identify host capabilities and existing artifacts; classify new versus resumed work.

**Ask now:** if undiscoverable, ask for the project folder and whether this is new or continued work. Do not ask production questions yet.

**Deliver:** current-state summary, confirmed host, missing capability list, and first actionable request.

**Gate:** project root and resume point are correct.

## BRIEF

**Enter when:** START is confirmed.

**Skill acts:** turn the user's idea into a production brief: topic, audience, audio-first versus visual-first, platform, aspect ratio, target duration, language, narrator count, release scope, and what success means for this sample.

**Ask now:** ask at most three questions. Prefer: topic/audience, target platform/format, desired duration. Infer reversible defaults and show them for confirmation.

**Deliver:** `BRIEF.md` using `assets/brief-template.md`.

**Gate:** user confirms the brief. Channel creation, upload, or publishing is not included unless separately authorized.

## BENCHMARKS

**Enter when:** BRIEF is confirmed.

**Skill acts:** first explain that benchmark selection will directly shape script quality and downstream presentation. Prioritize user-supplied benchmarks or selection criteria: ask for the accounts or works the user genuinely wants to learn from, or at least the direction and qualities they want screened. Analyze those materials when provided. Only when the user is unwilling or unable to provide either, perform a bounded public read-only search and return at least two benchmark candidates with clear reasons.

**Ask now:** ask the user for specific learning targets or concrete screening direction. Make clear that this is a high-impact decision, not routine material collection. If the user cannot or does not want to provide them, say that the Skill can search and recommend candidates instead. Do not silently choose a direction and continue.

**Deliver:** `BENCHMARKS.md` with source, role, evidence, learn/avoid decisions, recommendation, and rights boundary.

**Gate:** user carefully confirms benchmark roles after seeing the evidence and recommendation. Do not start WRITING_PACK before this decision. Learning never means copying exact wording, images, audio, or finished footage.

## WRITING_PACK

**Enter when:** BENCHMARKS is confirmed.

**Skill acts:** read [writing and review](writing-and-review.md), then use `assets/writing-pack-manifest.md` to build one self-contained package with the reusable writer rules, only the current channel/language profile and selected examples, and the episode task/materials. Read the channel's existing feedback before selecting examples. Preserve source evidence and mark what may enter narration. Supply needed information and causal relationships instead of prewritten editorial metaphors, forced paragraph formulas, or numerical style quotas.

**Ask now:** ask only for source material that cannot be found in scope and one decision about the desired benchmark emphasis.

**Deliver:** the populated writing package and manifest, as a merged file or archive with actual content. Record the package and channel-profile versions. Do not expose secrets or internal paths in public-facing materials.

**Gate:** user confirms the package direction, not every line of source material.

## SCRIPT

**Enter when:** WRITING_PACK is confirmed.

**Skill acts:** follow [writing and review](writing-and-review.md). Preserve the user's chosen writing model; when Kimi K3 is specified, use it if available or provide the user a self-contained handoff instead of silently substituting. Preserve one complete first draft. The original guiding conversation identifies concrete issues and protected passages, then provides one copyable, bounded edit list for the writer. When the revision returns, compare actual body changes with that list, check for new errors or damaged transitions, and stop after those issues are resolved; do not begin another general style review.

**Ask now:** use the already stated preferences to review the draft and prepare the edit list without asking the user to find all problems. Give the user the ready-to-forward instruction when the writer is in another conversation. Request a user decision only for a necessary scope change, missing fact, or final acceptance. Do not ask the user to redesign the workflow.

**Deliver:** preserved original body, `review/SCRIPT-REVIEW.md` with issues/actions/protected scope, the writer's complete revised `SCRIPT.md`, and a short result of the change comparison. Use fresh filenames if originals already exist. Keep counting and unresolved facts separate from narration, and record the user's actual feedback in the channel profile or project feedback file.

**Gate:** the user confirms the final script before marking it `已确认`. A complete but slightly short draft may be accepted without padding; a hollow draft or necessary material gap is `需要返工` and returns to WRITING_PACK. Large restructuring needs a specific reason and the user's decision. Do not perform second-round padding.

## VOICE

**Enter when:** SCRIPT is confirmed.

**Skill acts:** check whether a chosen TTS service is locally configured. If access is missing, guide the user through the current official application and local configuration path, verifying the official instructions when they may have changed; never request the plaintext key. For the established Doubao path, use current Seed-TTS 2.0 rather than a legacy generation. Select a representative approximately twenty-second sample and generate five to ten same-text voice auditions. After voice selection, generate a small set of rate auditions. Prefer the provider's documented subtitle/word-timestamp response (including an SSE event stream when that is the documented interface); save audio, sanitized metadata, and raw timing events before deriving SRT/ASS. Use text weights, `silencedetect`, or a uniform lead only as a recorded fallback.

**Ask now:** first ask whether access is configured, without requesting plaintext credentials. Then ask the user to choose the best voice; only after that ask for rate preference.

**Deliver:** voice audition set, confirmed voice/rate record, final narration, the native timing event stream when available, and derived SRT/ASS. Record why a fallback timing method was used when native timestamps are unavailable.

**Gate:** user confirms voice and full narration. Do not treat model or parameter suggestions as acceptance.

## STORYBOARD

**Enter when:** VOICE is confirmed.

**Skill acts:** use actual narration duration and timestamps to calculate image cadence and create `STORYBOARD.csv`. Each row includes shot ID, audio start/end, narration excerpt, visual intent, characters, text-card need, and status.

**Ask now:** present two concrete cadence options with real counts. Recommended default for a first audio-first project is 10–12 seconds per image; offer 6–8 seconds when the user wants faster visual motion and accepts more images.

**Deliver:** complete storyboard and count summary.

**Gate:** user confirms cadence, image count, and representative storyboard sections.

## VISUAL_STYLE

**Enter when:** STORYBOARD is confirmed.

**Skill acts:** request one to three reference images or propose two to three directions derived from the brief and benchmarks. Extract stable style variables: medium, palette, line/texture, lighting, composition, aspect ratio, negative constraints, subtitle style, and text-card style. Produce three to five pilot prompts or images.

**Ask now:** ask the user to choose or reject the pilot. Ask one targeted follow-up about the largest visible problem when rejected.

**Deliver:** `VISUAL_STYLE.md`, chosen pilot images, and frozen text treatment.

**Gate:** user explicitly confirms image style and text treatment. Do not write the full image prompt manifest before this.

## CHARACTER_ANCHORS

**Enter when:** VISUAL_STYLE is confirmed.

**Skill acts:** detect recurring characters and decide whether strict identity continuity is needed. For each strict character, create a face anchor and full-body anchor with age, body, clothing, footwear, and era details. Skip this stage for scenery-only or non-recurring characters.

**Ask now:** ask the user to approve or adjust each main character's identity, not every incidental character.

**Deliver:** `characters/` anchor images and character cards.

**Gate:** required anchors are confirmed, or the stage is explicitly `已跳过`.

## IMAGE_PROMPTS

**Enter when:** VISUAL_STYLE and any required CHARACTER_ANCHORS are confirmed.

**Skill acts:** create `IMAGE_PROMPTS.md` mapped one-to-one to storyboard IDs. Each prompt carries reference rules, identity constraints, frozen style, specific scene, composition, output format, and negative constraints. Start with a three-to-five-shot pilot manifest.

**Ask now:** tell the user exactly which pilot prompts to run, where to run them, how to name results, and what to return for review.

**Deliver:** pilot prompt manifest, then full manifest only after pilot approval.

**Gate:** pilot prompts produce acceptable results before full prompt expansion.

## IMAGE_GENERATION

**Enter when:** pilot prompts are confirmed.

**Skill acts:** route to manual or API mode. In manual ChatGPT mode, default to one prompt and one image per fresh conversation, issue manageable batches, and map each result to its shot ID. In API mode, explain estimated count/cost, verify authorization, run a small batch, then continue. Do not invoke video-generation models for this slideshow assembly stage.

**Ask now:** ask the user to choose manual versus API only after showing the tradeoff. For logged-in browser work, confirm the correct account and allowed read/write boundary.

**Deliver:** numbered generated images and generation ledger with failures or retries.

**Gate:** all required images exist or missing shots are explicitly accepted.

## ASSET_QC

**Enter when:** the image batch is complete enough to inspect.

**Skill acts:** check counts, IDs, dimensions, corrupt files, style drift, repeated composition, identity drift, era violations, embedded borders, and text baked into images. Generate a replacement list rather than silently accepting weak assets.

**Ask now:** show only the replacement candidates and reasons; ask the user to approve replacements or accept specific exceptions.

**Deliver:** frozen image manifest and `review/image-qc.md`.

**Gate:** image set is confirmed for assembly.

## MUSIC

**Enter when:** ASSET_QC is confirmed.

**Skill acts:** ask whether music is needed. If no, mark `已跳过` and record `music: skipped` in decisions. If yes, generate or source two to three short audition candidates within the authorized tool path, then plan a low-presence bed or a few emotion components. Narration remains dominant.

**Ask now:** ask whether to skip music; if not, ask the user to choose from auditions.

**Deliver:** music choice and mix plan.

**Gate:** music is confirmed or explicitly skipped.

## PREVIEW

**Enter when:** images are confirmed and music is confirmed or skipped.

**Skill acts:** assemble the project, preferably with HyperFrames when available. In a host with the bundled HyperFrames skills, load the `hyperframes` mandatory entry point before touching the composition and follow its routing instructions. Align images, subtitles, text cards, and music to narration timestamps. For motion repair, create an opening probe from a clean visual base, use the motion ledger, and keep the probe on a separate versioned path. Run structural checks and create a reviewable preview. Do not final-render yet.

**Ask now:** first request one decision on the opening probe: motion/transition accepted, or one named defect and time range. After that gate, tell the user what to review in the preview: opening minute, chapter transitions, character first appearances, text/subtitle collisions, and ending. Ask for specific changes or approval.

**Deliver:** preview, review board or representative frames, and issue list.

**Gate:** user approves preview. A general earlier “go ahead” is not sufficient.

## FINAL_RENDER

**Enter when:** PREVIEW is confirmed.

**Skill acts:** render the master, validate container/audio/video properties, extract representative frames from the final file, and watch or request a full human watch. If narration was regenerated or its duration changed, remap the clean visual at the delivery frame level while preserving cover duration, then recompute duration, stream parameters, and decode checks. Preserve the editable project and prior candidates.

**Ask now:** ask for acceptance after presenting the actual master and checks. Do not publish automatically.

**Deliver:** master video, project files, check report, and delivery note.

**Gate:** status is `已做待验` until the user accepts; then set `已验收`.

## FEEDBACK

**Enter when:** the user later provides real platform results.

**Skill acts:** record actual production time, manual intervention, playback/retention/feedback data, and identify the smallest workflow change for the next episode. Follow [writing and review](writing-and-review.md) to retain actual wording corrections and user judgments in the channel profile; select only relevant, current lessons for later packs. For a new account with 7–15 days of weak results, review topic choice and script first, then present an evidence-based choice between changing the niche and repairing those inputs. After three to five stable, accepted scripts exist, offer to extract the channel's own writing template or Skill. Do not infer performance from render success, treat merely used scripts as gold samples, or freeze a channel template from one sample.

**Ask now:** request only the available real results and the user's qualitative judgment.

**Deliver:** next-episode change list and project-level defaults worth freezing after several episodes.

**Gate:** no final gate; the next project starts from confirmed defaults rather than copying unverified assumptions.
