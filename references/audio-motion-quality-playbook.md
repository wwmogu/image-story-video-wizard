# Audio-first motion and timing quality playbook

This playbook is a reusable quality branch for narrated still-image stories. It
does not replace the normal stage order or confirmation contract. Use it when a
preview shows jitter, judder, abrupt transitions, subtitle drift, or when a new
narration changes the visual timeline.

## Gate sequence

Use this sequence for a narrated project:

`opening probe -> user confirmation -> full narration -> complete subtitles -> master -> user acceptance`

The opening probe is a short, reviewable sample containing one complete shot and a
transition. Do not spend the full narration/render cost until the user accepts the
probe. Record these explicit decisions even when they are negative requirements:

- `music: skipped` when no background music is requested;
- `release_copy_cover: not requested` when publishing copy or a cover is out of scope;
- `cover_duration_seconds` when a cover must remain fixed during later retiming.

Each turn still uses the five-field contract from the main Skill. A machine pass can
say a file is structurally valid; only a human watch can accept motion or sync.

## Clean-base and experiment hygiene

Before every motion experiment, write down the exact clean visual base: the image
sequence, cover duration, dimensions, and any already-approved static composition.
The next base must be that clean artifact, not the previous motion output. Use a
versioned directory such as `preview/motion-v01/`, never overwrite an earlier
candidate, and mark rejected output `stale` or `needs rework` in the state/ledger.

Recommended minimum ledger columns are in
`assets/motion-ledger-template.csv`. A candidate row must identify:

- clean `base_kind` and `base_artifact`;
- versioned `output_artifact` and status;
- output width/height, fps, and measured frame count;
- internal canvas scale and motion profile;
- transition profile and whether both sides were frozen;
- filters, validation commands/results, and a human verdict.

Run the repository validator on a candidate ledger:

```bash
python3 scripts/validate_motion_ledger.py preview/motion-v01/ledger.csv
```

The validator is deliberately conservative: rows marked `stale` may preserve a
failed experiment, but only non-stale candidates are checked against the stable
recovery rules.

## Motion diagnosis and recovery ladder

Start with a 10–15 second probe. Check frame cadence, PTS, source/output dimensions,
and decode before changing parameters:

```bash
ffprobe -v error -select_streams v:0 -count_frames \
  -show_entries stream=width,height,avg_frame_rate,r_frame_rate,nb_read_frames,duration \
  -of json preview.mp4

ffprobe -v error -select_streams v:0 \
  -show_entries frame=best_effort_timestamp_time,pkt_duration_time \
  -of csv=p=0 preview.mp4

ffmpeg -v error -i preview.mp4 -f null -
```

Stable timestamps rule out one class of PTS problems but do not prove that motion
looks smooth. If the source is smaller than delivery size, repeated enlargement can
also expose shimmer or texture crawl. Estimate scale/crop change in output pixels;
sub-pixel changes followed by integer rounding can produce repeated frames and a
visible step. Treat that as a diagnostic inference, not proof.

Use the smallest recovery that answers the defect:

1. **Static control:** no single-image motion, pure dissolve. Keep this as the
   fallback and comparison control.
2. **Stable zoom:** fixed output canvas, deterministic frame/time-based scale, center
   crop, one-way motion. After `zoompan` has reproduced jitter, do not keep tuning
   it as the sole path.
3. **Accepted stable profile:** render on a 4x internal canvas, use 60fps when the
   delivery spec allows it, apply an extremely slow one-way scale, and downscale
   once to delivery size.
4. **Optional temporal smoothing:** only after the above. `minterpolate` or `tblend`
   may soften steps but can ghost around cuts; subtitles must be composited after it.

For the stable recovery profile, do not use `zoompan`, pan, blur, breathe/breathing,
or shake. If an experimental filter is retained for historical diagnosis, keep it in
a stale row and do not promote it.

## Pure gradient transition rule

For a dissolve/gradient transition, freeze the outgoing image at its final frame and
the incoming image at its first frame. Cross-fade only. Do not blur, pan, zoom,
reset scale, or accelerate either side during the transition. Resume the incoming
shot's slow motion only after the transition completes. This keeps transition
artifacts separate from shot motion.

## Native timing first, fallback second

Prefer a TTS provider's currently documented native word-level TTS timestamps. If the
documented interface is an SSE stream, retain the returned event stream as a
project-local artifact. Save:

1. the generated audio;
2. sanitized metadata (provider/model/voice/settings identifiers only—no keys,
   cookies, session URLs, or raw authorization headers);
3. the raw timing events with secrets and unrelated personal data removed.

Generate SRT/ASS from the timing events, preserving word or cue identifiers so sync
can be audited. Do not name an endpoint, event schema, model, or parameter unless it
is documented by the provider and actually observed in the current run.

Fallback timing is allowed only when native timing is unavailable or unusable:

- transcript/text weighting;
- silence boundaries from `silencedetect`;
- a single documented lead/offset applied consistently.

Label the fallback in the ledger and state. Merge ultra-short cues rather than
creating unreadable flashes; check the opening sample before authorizing full
subtitle generation.

## Audio duration changes and visual remapping

When a new narration has a different duration, do not attach it to the old visual
timeline. Remap the clean visual at the delivery frame level (preferably 60fps),
preserving cover duration, shot order, and transition rules.
Recompute and record:

- total duration and cover duration;
- video frame count and measured frame rate;
- audio/video stream parameters;
- full decode result;
- subtitle end time and any cue overflow.

Only after these checks should subtitles and the final master be rebuilt. A successful
decode does not prove visual alignment; the user must watch the opening, a middle
transition, and the ending.

## Promotion and rollback

Promote a candidate only when the ledger validator passes, structural/decode checks
pass, the opening probe is human-approved, and the relevant master is accepted. If a
gate fails, preserve the artifact, mark it stale/needs rework, and return to the
earliest affected stage. The static-plus-dissolve control is a valid rollback, not a
project failure.

### Incident record

```text
Incident:
User symptom:
Exact clean baseline artifact:
Source / delivery dimensions:
Frame rate and PTS result:
Motion filter path:
Transition path and freeze rule:
Per-frame scale step estimate:
Sample tested:
Machine checks:
Human verdict:
Next smallest change:
Promotion status: one-off / project default / reusable Skill candidate
```
