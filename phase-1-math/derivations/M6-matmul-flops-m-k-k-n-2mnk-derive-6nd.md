# M6 · Linear algebra

**Derive by hand:** Matmul FLOPs: (m×k)@(k×n) = 2mnk; derive 6ND for Transformer training

**Confirm in code:** Count FLOPs for a 124M GPT-2 by hand, check with `torch.utils.flop_counter`

**Used in:** #12 Chinchilla, #17 FlashAttention

## Derivation

## Numerical check

Script: `../checks/m6.py`

## What I got wrong the first time
