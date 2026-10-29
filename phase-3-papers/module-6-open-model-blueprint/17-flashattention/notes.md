# Paper 17: FlashAttention — my notes

## Day 1 — Read and question
Three questions I can't answer yet:
1.
2.
3.

## Day 2 — Derive and watch
Core derivation, by hand:

```
(paste or photograph it; link images from ./figures/)
```

## Day 3 — Break it
| Experiment | What I changed | What happened | Why |
| --- | --- | --- | --- |
| HAND: Tiled online softmax over a 10,000-vector in chunks of 100, … | | | |
| HAND→AGENT: Naive `Q @ K.T` at N=16,384 (CUDA OOM) vs `F.scaled_dot_prod… | | | |
| AGENT: The Triton FlashAttention-2 kernel from CS336 A2 — you must … | | | |

## Explain it aloud
Ten minutes with an LLM as examiner, no notes. Gaps found:

## Two-line conclusion
