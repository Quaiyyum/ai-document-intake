# Dataset split

Chosen once with `random.Random(42)` over the 50 sorted tender doc_ids; never changed afterwards.

| Set | Count | Used for |
| --- | --- | --- |
| GOLD TEST SET | 10 | Accuracy measurement only. Never used for prompt tuning. |
| DEV SET | 5 | Prompt and schema tuning only. |
| Volume | 35 | Extracted for workflow volume; not labelled. |

## Gold test set

- GETS-2026-0002
- GETS-2026-0006
- GETS-2026-0007
- GETS-2026-0008
- GETS-2026-0009
- GETS-2026-0015
- GETS-2026-0016
- GETS-2026-0018
- GETS-2026-0035
- GETS-2026-0041

## Dev set

- GETS-2026-0003
- GETS-2026-0004
- GETS-2026-0011
- GETS-2026-0037
- GETS-2026-0048
