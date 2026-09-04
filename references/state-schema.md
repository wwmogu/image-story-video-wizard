# Project state contract

`PROJECT_STATE.json` is the single source for workflow position. It is not a log of secrets or a substitute for the actual artifacts.

## Required top-level fields

```json
{
  "schema_version": 1,
  "project_id": "slug-or-uuid",
  "title": "Human-readable title",
  "project_root": "/absolute/project/path",
  "host": {
    "name": "codex|workbuddy|other",
    "capabilities": {
      "local_files": true,
      "model_routing": false,
      "logged_in_browser": false,
      "tts": false,
      "image_generation": false,
      "hyperframes": false,
      "render": false
    }
  },
  "current_stage": "START",
  "stage_status": "进行中",
  "pending_request": "Confirm project root and whether this is new or resumed work.",
  "next_stage": "BRIEF",
  "decisions": {},
  "artifacts": {},
  "stage_history": [],
  "created_at": "ISO-8601 timestamp",
  "updated_at": "ISO-8601 timestamp"
}
```

## Allowed stages

`START`, `BRIEF`, `BENCHMARKS`, `WRITING_PACK`, `SCRIPT`, `VOICE`, `STORYBOARD`, `VISUAL_STYLE`, `CHARACTER_ANCHORS`, `IMAGE_PROMPTS`, `IMAGE_GENERATION`, `ASSET_QC`, `MUSIC`, `PREVIEW`, `FINAL_RENDER`, `FEEDBACK`.

## Allowed statuses

`未开始`, `进行中`, `待确认`, `已确认`, `需要返工`, `已跳过`.

## Update rules

1. Update state after creating a material artifact, reaching a gate, receiving a gate decision, or changing hosts.
2. Before entering a stage, append the prior stage result to `stage_history` with timestamp and artifact paths.
3. `pending_request` must name the one current user action. It must not contain the full future checklist.
4. Store decisions as facts with source and status, for example:

```json
"decisions": {
  "aspect_ratio": {
    "value": "16:9",
    "source": "user",
    "status": "已确认"
  }
}
```

5. Artifact paths must be absolute inside `PROJECT_STATE.json`. Public deliverables must not expose private paths.
6. Never store plaintext API keys, cookies, login URLs, redemption codes, or tokens.
7. When returning to an earlier stage, do not delete downstream artifacts. Mark them in `artifacts` as `stale: true` until regenerated or re-confirmed.

## Quality-branch records

The base schema remains compatible with existing projects. Store quality-branch
facts inside the existing `decisions` and `artifacts` objects; do not add secrets or
provider session data. Useful records include:

```json
{
  "decisions": {
    "music": {"value": "skipped", "source": "user", "status": "已确认"},
    "release_copy_cover": {"value": "not requested", "source": "user", "status": "已确认"},
    "timing_source": {"value": "native-word-timestamps", "source": "tts-response", "status": "已确认"}
  },
  "artifacts": {
    "motion_probe_v01": {
      "path": "/absolute/project/preview/motion-v01/probe.mp4",
      "base": "/absolute/project/preview/clean-visual.mp4",
      "ledger": "/absolute/project/preview/motion-v01/ledger.csv",
      "status": "已做待验",
      "stale": false
    },
    "old-motion-experiment": {
      "path": "/absolute/project/preview/motion-v00/old.mp4",
      "status": "stale",
      "stale": true,
      "needs_rework": true
    }
  }
}
```

For motion records, the ledger is the source of truth for the clean base, filter
profile, internal canvas, fps, frame count, transition freeze, validation result,
and human verdict. Keep provider-specific timing payloads in a project-local file
with secrets removed; keep only its path and method in state.

## Resume behavior

On resume:

1. Validate the state file with `scripts/project_state.py validate`.
2. Confirm that the latest required artifact still exists.
3. Tell the user the latest confirmed gate and the single pending request.
4. Continue from `current_stage`; do not repeat already confirmed questions.

## Delivery status mapping

- No material artifact: `未做`.
- Artifact exists but user has not accepted the relevant gate: `已做待验`.
- User accepted the final master: `已验收`.
