"""Small helpers reused across the break-it labs.

Import from a paper's experiments/ folder with:
    import sys; sys.path.append("../../../../shared")
    from utils import set_seed, get_device, grad_norms
"""
from __future__ import annotations

import random


def set_seed(seed: int = 0) -> None:
    """Make runs repeatable so a 'broken' run differs from the baseline only by the change you made."""
    import numpy as np
    import torch

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def get_device():
    import torch

    if torch.cuda.is_available():
        return torch.device("cuda")
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def grad_norms(model) -> dict[str, float]:
    """Per-parameter gradient L2 norms. Call after loss.backward().
    Used by e.g. Paper 1 (saturating activations) and Paper 4 (removing sqrt(d_k))."""
    return {name: p.grad.norm().item() for name, p in model.named_parameters() if p.grad is not None}


def count_params(model, trainable_only: bool = True) -> int:
    """Handy for Paper 10 (LoRA) and Paper 18 (MoE): parameters vs. compute."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad or not trainable_only)
