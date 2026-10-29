#!/usr/bin/env python3
"""Source for docs/data/roadmap.json — the AI Lab Research Roadmap (Merged Master Plan, Oct 27 2026).

Text follows the merged plan. Links are the merged plan's own links, as-is.
YouTube walkthroughs come from the original 21-paper roadmap (the merged plan names
them by title only); direct-download PDFs from that roadmap are kept next to each paper.

Inline markup used in strings: `code`, **bold**, [label](url), $latex$.
Edit this file, then run:  python scripts/build_roadmap.py && python scripts/scaffold.py
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs/data/roadmap.json"

# ---------------------------------------------------------------- shared links
ALISA = "https://github.com/soasme/alisa-roadmap"
BLOG = "https://alisawuffles.github.io/blog/job-search/"
BOOK_LLMS = "https://alisawuffles.notion.site/alisa-s-book-of-llms"
MATH_NOTES = "https://alisawuffles.notion.site/math-notes"
CS336 = "https://cs336.stanford.edu/spring2025/"
CS336_PL = "PLoROMvodv4rOY23Y0BoGoBGgQ1zmU_MT_"
ZTH_PL = "PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ"
YT_PL = "https://www.youtube.com/playlist?list="
TRACE = "http://cs336.stanford.edu/spring2025-lectures/?trace=var/traces/lecture_{:02d}.json"
GHL = "https://github.com/stanford-cs336/spring2025-lectures/blob/"
LECT = {
    1: TRACE.format(1), 2: TRACE.format(2),
    3: GHL + "e9cb2488fdb53ea37f0e38924ec3a1701925cef3/nonexecutable/2025%20Lecture%203%20-%20architecture.pdf",
    4: GHL + "98455ec198c9a88ec1ab2b1c4058662431b54ce3/nonexecutable/2025%20Lecture%204%20-%20MoEs.pdf",
    5: GHL + "main/nonexecutable/2025%20Lecture%205%20-%20GPUs.pdf",
    6: TRACE.format(6),
    7: GHL + "4eff81bee0a853217209e163936b264f03572b66/nonexecutable/2025%20Lecture%207%20-%20Parallelism%20basics.pdf",
    8: TRACE.format(8),
    9: GHL + "fb79eb018fa047bf99c4c785dcbbd62fff361e54/nonexecutable/2025%20Lecture%209%20-%20Scaling%20laws%20basics.pdf",
    10: TRACE.format(10),
    11: GHL + "00191bba00d6d64621dc46ccaed9122681413a24/nonexecutable/2025%20Lecture%2011%20-%20Scaling%20details.pdf",
    12: TRACE.format(12), 13: TRACE.format(13), 14: TRACE.format(14),
    15: GHL + "61eddac004df975466cff0329b615f2d24230069/nonexecutable/2025%20Lecture%2015%20-%20RLHF%20Alignment.pdf",
    16: GHL + "e94e33f433985e57036b25215dff2a4292e67a4f/nonexecutable/2025%20Lecture%2016%20-%20RLVR.pdf",
    17: TRACE.format(17),
}
A = {1: "https://github.com/stanford-cs336/assignment1-basics",
     2: "https://github.com/stanford-cs336/assignment2-systems",
     3: "https://github.com/stanford-cs336/assignment3-scaling",
     4: "https://github.com/stanford-cs336/assignment4-data",
     5: "https://github.com/stanford-cs336/assignment5-alignment"}
A1_HANDOUT = "https://github.com/stanford-cs336/assignment1-basics/blob/main/cs336_spring2025_assignment1_basics.pdf"
SB = "https://jax-ml.github.io/scaling-book/"
CS224N = "https://web.stanford.edu/class/cs224n/readings/cs224n-self-attention-transformers-2023_draft.pdf"
ILL_GPT2 = "https://jalammar.github.io/illustrated-gpt2/"
CS231N = "https://cs231n.github.io/optimization-2/"
IVISON = "https://ivison.id.au/2026/02/09/policy-gradient.html"
WENG = "https://lilianweng.github.io/posts/2018-04-08-policy-gradient/"
HUYEN = "https://huyenchip.com/ml-interviews-book/"
NANOGPT = "https://github.com/karpathy/build-nanogpt"
MINBPE = "https://github.com/karpathy/minbpe"
CLEANRL = "https://github.com/vwxyzjn/cleanrl"
RLHFBOOK = "https://rlhfbook.com/"
MURALI = "https://gitlostmurali.com/blog/grpo-intro"
LC75 = "https://leetcode.com/studyplan/leetcode-75/"
BLIND75 = "https://neetcode.io/practice/practice/blind75"
RUNPOD = "https://runpod.io/pricing"
LAMBDA = "https://lambda.ai/pricing"
LAMBERT = "https://natolambert.com/writing/ai-phd-job-hunt"
ABS = "https://arxiv.org/abs/"
PDF = "https://arxiv.org/pdf/"

def L(n):  # markdown link to a CS336 lecture
    return f"[CS336 L{n}]({LECT[n]})"

def link(label, url): return {"label": label, "url": url}
def vid(title, yt_id): return {"title": title, "id": yt_id}
def exp(tag, body): return {"tag": tag, "body": body}

H, HA, AG = "HAND", "HAND→AGENT", "AGENT"

# ---------------------------------------------------------------- top matter
meta = {
    "title": "AI Lab Research Roadmap — Merged Master Plan",
    "date": "Oct 27, 2026",
    "author": "@Arush",
    "intro": [
        f"This plan merges three sources into one sequence: your 21-paper \"Break the Equation\" curriculum (Modules 1–8), the [alisa-roadmap]({ALISA}) GitHub knowledge map, and the blog it was compiled from, [Alisa Liu's Notes on the Industry Job Search]({BLOG}) (Research Scientist at OpenAI; 57 interviews, 11 companies, 4 offers). Her central finding sets the priority order here: technical skill and implementation fluency are evaluated far more than research experience, and research experience is mostly what gets you the first interview.",
        "**The by-hand vs coding-agent rule.** Labs now expect you to use agents for real work, but interviews are run with AI off. So every item below carries one of three tags.",
    ],
    "tags": [
        {"tag": H, "meaning": "Muscle memory. Write it from a blank file with AI off, under a time target, repeatedly.",
         "rule": "Anything that fits in 15–60 lines and shows up in ML-coding rounds: attention, a decoder block, BPE, sampling, a training loop, NumPy backprop, Adam, LoRA, RoPE, a KV cache, the DPO/GRPO loss."},
        {"tag": HA, "meaning": "Write the core once by hand so you own it, then hand the variations, sweeps, plots and scaffolding to a coding agent.",
         "rule": "The \"break it\" experiments: you write the 10-line change that breaks the equation; the agent builds the harness, dataset loader, logging and plots around it."},
        {"tag": AG, "meaning": "Delegate the build; your job is to specify it, read every line, run it, and be able to explain any design choice in it.",
         "rule": "Triton kernels, distributed training scaffolding, full RLHF loops with TRL, MoE training infra, diffusion samplers, anything that is in a project on your CV but would never be asked as a 30-minute whiteboard."},
    ],
    "afterTags": [
        "The test for a CV project is simple: if an interviewer opens any file in it and asks \"why is this here?\", you answer without hesitation. Being able to reproduce the whole file by hand is not required; being able to reproduce the boilerplate core (the model, the loss, the loop) is.",
        "**Reading order.** Phases run roughly in sequence but overlap on purpose: LeetCode (Phase 5) is a daily 30-minute habit from week 3 onward, and the paper curriculum (Phase 3) is the spine that the CS336 lectures and the muscle-memory drills hang off. Every section links its sources inline; the full index is at the end.",
    ],
}

interviews = {
    "title": "What AI-lab interviews actually test",
    "intro": "ML coding is the single most common round, and \"implement a Transformer / decoding strategy / classic ML algorithm from scratch in PyTorch\" is its modal question. Everything else in this roadmap is weighted by the table below, which is Alisa's own breakdown (approximate shares from the GitHub map).",
    "rounds": [
        {"round": "ML coding", "share": "~50%", "testing": "Can you implement what you claim to know, fluently, with AI off? PyTorch is a must; NumPy only for backward passes.", "passing": "Decoder block with causal masking from a blank file; beam search or top-p sampling clean on first run.", "where": "Phase 2 (drills), Phase 3 (papers)"},
        {"round": "Technical discussion", "share": "~20%", "testing": "Two flavors: (a) design an experiment to answer a research question and defend it under pushback; (b) rapid-fire breadth (\"What is 5D parallelism? PPO vs GRPO? Ways to encode position?\").", "passing": "Crisp, opinionated answers; you can name trade-offs without notes.", "where": "Phase 0, Phase 4, Phase 6"},
        {"round": "General coding", "share": "~20%", "testing": "LeetCode-style, sometimes with ML flavor; the patterns leak into ML coding rounds.", "passing": "Mediums consistently under 25 minutes.", "where": "Phase 5"},
        {"round": "Behavioral", "share": "~10%", "testing": "Specific stories mapped to leadership / conflict / failure / impact, plus a serious question on AI safety.", "passing": "STAR answers retrieved instantly, no reconstruction.", "where": "Phase 6"},
        {"round": "Math (some companies)", "share": "varies", "testing": "Pen-and-paper derivations: MLE = cross-entropy, KL both directions, backprop, Adam bias correction, SVD/low-rank.", "passing": "You derive, not recall.", "where": "Phase 1"},
        {"round": "Research discussion + job talk", "share": "varies", "testing": "Why you chose the problems you did; what you'd do with 10x compute; the company's recent papers.", "passing": "80% of the talk on first-author work; every baseline choice defensible.", "where": "Phase 6"},
    ],
    "after": f"Two practical notes from the blog that shape the schedule: each interview is \"a class you never attended with three days to cram,\" so keep swappable per-topic notes (she kept a [running LLM notebook]({BOOK_LLMS}) and a [math notebook]({MATH_NOTES})); and sleep beats last-minute cramming — her first technical interview was lost to an off-by-one error on two hours of sleep.",
    "sources": f"[alisa-roadmap README]({ALISA}) · [Notes on the Industry Job Search]({BLOG})",
}

# ---------------------------------------------------------------- phase 0
lectures = [
    ("1", "Overview, tokenization", "BPE appears in almost every ML-coding round", "— (Phase 4 tokenization)", "A1 Basics out", [1]),
    ("2", "PyTorch, resource accounting", "Memory math (params, activations, KV) comes up constantly", "#12 Chinchilla, #17 FlashAttention", "A1", [2]),
    ("3", "Architectures, hyperparameters", "Backbone of every architecture question: pre-norm, RMSNorm, SwiGLU, RoPE", "#4 Transformer, #16 LLaMA", "A1", [3]),
    ("4", "Mixture of experts", "Expect \"implement a top-k router\" asks", "#18 Switch / DeepSeek-V3", "—", [4]),
    ("5", "GPUs", "Arithmetic intensity, memory- vs compute-bound", "#17 FlashAttention", "A2 Systems out", [5]),
    ("6", "Kernels, Triton", "Required at infra-heavy labs", "#17 FlashAttention", "A2", [6]),
    ("7", "Parallelism basics", "\"Train a 70B model on 8x80GB — walk me through it\"", "#16 Llama 3", "A2", [7]),
    ("8", "Parallelism (Percy)", "Same question, deeper: ZeRO stages, TP/PP/DP trade-offs", "— (Phase 4)", "A2", [8]),
    ("9", "Scaling laws basics", "Chinchilla math is non-negotiable", "#12 Chinchilla", "A3 Scaling out", [9]),
    ("10", "Inference", "KV cache size formula, speculative decoding, PagedAttention", "#16 LLaMA (GQA)", "—", [10]),
    ("11", "Scaling laws details", "IsoFLOP curves, parametric loss fits, LR schedule pitfalls", "#12 Chinchilla", "A4 Data out", [11]),
    ("12", "Evaluation", "\"How would you know your model got better?\"", "#15 CoT (GSM8K)", "—", [12]),
    ("13–14", "Data I, Data II", "Curation and dedup are underrated and commonly asked", "#6 GPT-3 (data section)", "A4", [13, 14]),
    ("15", "Alignment: SFT/RLHF", "Post-training is now core knowledge", "#11 InstructGPT, #13 DPO", "A5 Alignment out", [15]),
    ("16–17", "Alignment: RL / RLVR, RL (Percy)", "PPO vs GRPO is a standard rapid-fire question", "#8 PPO, #19 GRPO/R1", "A5", [16, 17]),
]
phase0 = {
    "id": "p0", "nav": "CS336 breadth", "num": 0, "title": "Breadth first — Stanford CS336", "weeks": "weeks 1–2",
    "intro": [f"Watch all 17 lectures of [Stanford CS336: Language Modeling from Scratch]({CS336}) ([YouTube playlist]({YT_PL}{CS336_PL})) before any deep dive. Alisa started her search this way; it gives the skeleton that organizes every scattered concept, and its five assignments are the best self-study implementation track that exists. Watch at 1.5x, take notes, draw one diagram per lecture. Do not pause to implement yet."],
    "playlist": {"title": "Stanford CS336: Language Modeling from Scratch", "list": CS336_PL},
    "lectures": [{"id": f"L{n}", "n": n, "topic": t, "why": w, "papers": p, "assignment": a,
                  "links": [{"label": f"Lecture {k}", "url": LECT[k]} for k in ks]} for n, t, w, p, a, ks in lectures],
    "assignments": [
        {"id": "A1", "label": "A1 Basics", "url": A[1], "tag": H},
        {"id": "A2", "label": "A2 Systems", "url": A[2], "tag": HA},
        {"id": "A3", "label": "A3 Scaling", "url": A[3], "tag": HA},
        {"id": "A4", "label": "A4 Data", "url": A[4], "tag": HA},
        {"id": "A5", "label": "A5 Alignment", "url": A[5], "tag": HA},
    ],
    "after": [f"**Assignment plan.** [A1 Basics]({A[1]}) is HAND: tokenizer, model, optimizer, training loop, written with autocomplete off (the course itself asks for this). Alisa calls it crucial because implementing and debugging a Transformer comes up so often that it must become muscle memory. A2, A3, A4, A5 are HAND→AGENT: write the core (the online-softmax tile, the IsoFLOP fit, the dedup pass, the GRPO loss) yourself, let agents build the harnesses. Compute for self-study: a single H100 runs ~$2–3/hour on [RunPod]({RUNPOD}) or [Lambda]({LAMBDA}); debug on CPU first."],
    "sources": f"[CS336 Spring 2025 schedule]({CS336}) · [alisa-roadmap README]({ALISA})",
}

# ---------------------------------------------------------------- phase 1
math_rows = [
    ("Probability", "Bernoulli → Binomial → Gaussian limit; 68-95-99.7; CLT; multivariate Gaussian", "Sample 10k Bernoullis, plot the binomial mean converging to a Gaussian", "#9 DDPM (Gaussian forward process)"),
    ("Probability", "MLE: show minimizing cross-entropy is maximizing log-likelihood", "Train logistic regression with both losses, assert identical gradients", "#4 Transformer (LM loss)"),
    ("Probability", "MAP: show L2 regularization equals a Gaussian prior", "Compare `weight_decay` vs explicit log-prior term", "#2 Adam (L2 vs AdamW)"),
    ("Information theory", "Entropy; derive perplexity = exp(H); cross-entropy vs KL", "Compute PPL of a tiny LM two ways", "#12 Chinchilla (loss curves)"),
    ("Information theory", "KL(P ‖ Q) vs KL(Q ‖ P): mode-seeking vs mass-covering; which direction the RLHF penalty uses and why", "Fit a 1-Gaussian to a 2-Gaussian mixture under each direction, plot", "#11 InstructGPT, #13 DPO"),
    ("Linear algebra", "Matmul FLOPs: (m×k)@(k×n) = 2mnk; derive 6ND for Transformer training", "Count FLOPs for a 124M GPT-2 by hand, check with `torch.utils.flop_counter`", "#12 Chinchilla, #17 FlashAttention"),
    ("Linear algebra", "SVD $A = U \\Sigma V^\\top$; Eckart–Young: rank-r truncation minimizes Frobenius error", "SVD a fine-tuned ΔW, plot singular values, verify most mass is in top-r", "#10 LoRA"),
    ("Linear algebra", "Eigendecomposition of symmetric matrices; matrix norms (L1, L2, Frobenius, nuclear) and what each regularizes", "—", "#10 LoRA"),
    ("Calculus", "Chain rule for a 2-layer MLP; Jacobians for vector→vector maps", "NumPy forward+backward for linear → softmax → cross-entropy, no autograd; assert against `torch.autograd`", "#1 AlexNet"),
    ("Calculus", "Attention gradient: $\\partial\\,\\mathrm{softmax}(QK^\\top/\\sqrt{d})V / \\partial Q$", "Confirm the √d_k variance argument numerically", "#4 Transformer"),
    ("Optimization", "Adam update rule; why m̂ and v̂ need bias correction at step 1", "Your 25-line Adam from Module 1, with and without correction", "#2 Adam"),
    ("Optimization", "Policy gradient: the log-derivative trick, reward-to-go, why a state-only baseline is unbiased", "REINFORCE on a 3-armed bandit, with and without baseline, plot variance", "#8 PPO, #19 GRPO"),
]
phase1 = {
    "id": "p1", "nav": "Math foundations", "num": 1, "title": "Math foundations", "weeks": "weeks 3–4, then on call",
    "intro": ["At least one company will run a dedicated math interview, from logic puzzles to pen-and-paper derivations. Everything here is HAND: derive on paper, then confirm numerically in a 10-line script. Each derivation is paired with the paper in Phase 3 that uses it, so the math is never studied in isolation."],
    "rows": [{"id": f"M{i+1}", "area": a, "derive": d, "code": c, "paper": p} for i, (a, d, c, p) in enumerate(math_rows)],
    "after": [f"**Study order.** Read [CS231n backprop notes]({CS231N}) first (the NumPy backward pass is asked verbatim). Then Hamish Ivison's [Introduction to Policy Gradient for LMs]({IVISON}), which derives REINFORCE → baselines → importance weighting → group-relative advantages in LM notation; read it before touching PPO or GRPO. Supplement with Lilian Weng's [Policy Gradient Algorithms]({WENG}) and Chip Huyen's [ML Interviews Book]({HUYEN}) to find gaps."],
    "sources": f"[alisa-roadmap README, Phase 2]({ALISA}) · [Notes on the Industry Job Search]({BLOG})",
}

# ---------------------------------------------------------------- phase 2
drills = [
    ("Scaled dot-product attention", "10 min", "The √d_k scaling, −∞ (not 0) in the causal mask, softmax over the key axis", "#4 Transformer"),
    ("Multi-head attention", "20 min", "Split heads → attend → merge via reshape or `einsum`; output projection W_O", "#4 Transformer"),
    ("Full pre-norm decoder block", "30 min", "LN → MHA → residual → LN → FFN (4×d_model, GeLU or SwiGLU) → residual; parameter count by hand", "#4, #16 LLaMA"),
    ("BPE tokenizer", "45 min", "Build vocab from a corpus; encode a new string; state the merge-step complexity", "CS336 A1, Phase 4"),
    ("Top-k / top-p sampling with temperature", "15 min", "Temperature before filtering; masking that keeps at least one token", "CS336 L10"),
    ("Beam search", "20 min", "Track log-probs across B beams; handle EOS and length normalization", "CS336 L10"),
    ("Full training loop", "20 min", "Forward, loss, `backward()`, optimizer step, scheduler step, grad clipping, eval split", "#2 Adam, #6 GPT-3"),
    ("NumPy backprop", "45 min", "Linear → softmax → cross-entropy, analytic gradients, no autograd", "#1 AlexNet, Phase 1"),
    ("Adam optimizer", "15 min", "m, v, bias correction, decoupled weight decay", "#2 Adam"),
    ("LoRA wrapper around `nn.Linear`", "10 min", "B = 0 init, A ~ N(0, σ²), α/r scaling, merge for inference", "#10 LoRA"),
    ("RoPE", "15 min", "Complex rotation of Q and K; dot product depends only on m − n", "#16 LLaMA"),
    ("KV cache for generation", "20 min", "Prefill vs decode; append K, V per step; compute only the new Q", "CS336 L10"),
    ("GQA / MQA attention", "15 min", "n_kv_heads < n_heads via `repeat_interleave`; KV-cache memory drops by n_heads/n_kv_heads", "#16 LLaMA"),
    ("DPO loss", "10 min", "`-logsigmoid(β((πw−refw)−(πl−refl))).mean()`", "#13 DPO"),
    ("GRPO advantage + clipped loss", "20 min", "Group-normalized advantages, importance ratio with stop-gradient on old log-probs, clip", "#19 GRPO"),
    ("PPO clipped surrogate + GAE", "30 min", "`min(rA, clip(r,1−ε,1+ε)A)`, GAE recursion, value loss, entropy bonus", "#8 PPO"),
    ("Online (tiled) softmax", "20 min", "Running max and denominator rescaled by exp(m_old − m_new); `allclose` vs `F.softmax`", "#17 FlashAttention"),
    ("Top-k MoE router", "20 min", "Softmax gate, top-2 dispatch, load-balancing auxiliary loss", "#18 MoE"),
    ("Flow-matching loss + Euler sampler", "15 min", "x_t = (1−t)x₀ + t x₁, v_θ ≈ x₁ − x₀, Euler loop", "#21 Flow Matching"),
]
DRILL_SLUGS = ["sdpa", "multi_head_attention", "decoder_block", "bpe_tokenizer", "sampling", "beam_search",
               "training_loop", "numpy_backprop", "adam", "lora", "rope", "kv_cache", "gqa", "dpo_loss",
               "grpo_loss", "ppo_loss", "online_softmax", "moe_router", "flow_matching"]
phase2 = {
    "id": "p2", "nav": "Muscle-memory drills", "num": 2, "title": "Muscle-memory implementations", "weeks": "from week 5, repeated weekly",
    "intro": ["This is the HAND list: the boilerplate core you must reproduce from a blank file, with every AI tool off, under the time target. Alisa's rule, which the CS336 honor code also enforces: practice with AI assistance completely off, because you will underestimate your reliance otherwise. Rotate through the table once a week until every row is under target three times in a row; after that, one timed row per day keeps it warm."],
    "drills": [{"id": f"D{i+1}", "row": i + 1, "slug": DRILL_SLUGS[i], "name": n, "target": t, "must": m, "where": w}
               for i, (n, t, m, w) in enumerate(drills)],
    "playlist": {"title": "Karpathy — Neural Networks: Zero to Hero", "list": ZTH_PL},
    "after": [
        f"**Reference implementations to read once, then close.** Karpathy's [build-nanogpt]({NANOGPT}) and [minbpe]({MINBPE}) ([Neural Networks: Zero to Hero playlist]({YT_PL}{ZTH_PL})), [The Illustrated GPT-2]({ILL_GPT2}), and the [CS224N self-attention and Transformers notes]({CS224N}). Read them before the first drill, never during one.",
        "**AGENT work around the drills.** Have a coding agent build you a drill harness: a repo with one `test_<row>.py` per row that asserts your from-scratch output against the PyTorch reference, plus a timer. You write the implementation files; the agent writes and maintains the tests.",
    ],
    "sources": f"[alisa-roadmap README, Phase 3]({ALISA}) · [Notes on the Industry Job Search]({BLOG})",
}

# ---------------------------------------------------------------- phase 3 papers
modules = [
    {"id": 1, "title": "Optimization and depth", "slug": "optimization-depth"},
    {"id": 2, "title": "The Transformer era", "slug": "transformer-era"},
    {"id": 3, "title": "Reinforcement learning and generative modeling", "slug": "rl-generative"},
    {"id": 4, "title": "Scaling, adaptation and alignment", "slug": "scaling-adaptation-alignment"},
    {"id": 5, "title": "Reasoning", "slug": "reasoning"},
    {"id": 6, "title": "The modern open-model blueprint", "slug": "open-model-blueprint"},
    {"id": 7, "title": "Reasoning RL", "slug": "reasoning-rl"},
    {"id": 8, "title": "Modern generative modeling", "slug": "modern-generative"},
]

papers = [
 dict(n=1, module=1, slug="alexnet", short="AlexNet", year="2012",
  title="ImageNet Classification with Deep Convolutional Neural Networks",
  paper=[link("Paper", "https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html"),
         link("PDF", "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf")],
  videos=[vid("AlexNet Paper Walkthrough", "TWyp0_DEwCI")], resources=[],
  approach="Sections 3–4: non-saturating ReLU (6x faster than tanh), overlapping pooling, PCA color augmentation, dropout p=0.5.",
  hooks="\"Why did depth + GPUs + regularization unlock representation learning?\"",
  experiments=[exp(HA, "Swap ReLU for tanh/sigmoid in a 5-layer CIFAR-10 CNN, plot per-layer `param.grad.norm()`."),
               exp(HA, "Remove dropout and weight decay, watch train acc hit 100% while val loss explodes.")]),
 dict(n=2, module=1, slug="adam", short="Adam", year="2014",
  title="Adam: A Method for Stochastic Optimization",
  paper=[link("Paper", ABS + "1412.6980"), link("PDF", PDF + "1412.6980.pdf")],
  videos=[vid("Adam Optimizer Explained in Detail", "N5AynalXD9g"), vid("Gradient Descent Made Better", "XHF2jW_U3iM")], resources=[],
  approach="Algorithm 1 and Section 3 (bias correction). How $m_t$ (momentum) and $v_t$ (uncentered variance) combine AdaGrad and RMSProp.",
  hooks="(math round): derive the update, explain why bias correction matters at step 1.",
  experiments=[exp(H, "25-line custom `torch.optim.Optimizer`; delete the $/(1-\\beta_1^t)$ and $/(1-\\beta_2^t)$ divisions and watch the first steps jump because $v_1 \\approx 0$."),
               exp(HA, "Sweep L2-in-gradient vs decoupled AdamW across LRs.")]),
 dict(n=3, module=1, slug="resnet", short="ResNet", year="2015",
  title="Deep Residual Learning for Image Recognition",
  paper=[link("Paper", ABS + "1512.03385"), link("PDF", PDF + "1512.03385.pdf")],
  videos=[vid("ResNet Explained in <10 Mins", "o_3mboe1jYI"), vid("W&B ResNet Paper Reading", "nspf00KpU-g")], resources=[],
  approach="Separate vanishing gradients (fixed by BatchNorm) from the degradation problem (deeper plain nets have higher training error). Why $F(x) = H(x) - x$ is easier than learning identity.",
  hooks="\"What training failure do residuals prevent?\" (asked in the Transformer section too).",
  experiments=[exp(HA, "`out = block(x) + alpha * x` with alpha ∈ {0, 1}, 20- vs 56-layer on CIFAR-10; watch the 56-layer plain net lose."),
               exp(HA, "Zero-init the last BatchNorm γ in each block so blocks start as identity (the same trick reappears in #20 DiT).")]),
 dict(n=4, module=2, slug="transformer", short="Attention Is All You Need", year="2017",
  title="Attention Is All You Need",
  paper=[link("Paper", ABS + "1706.03762"), link("PDF", PDF + "1706.03762.pdf")],
  videos=[vid("Yannic Kilcher Walkthrough", "iDulhoQ2pro"), vid("Umar Jamil Code & Tensor Shapes", "bCz4OMemCcA")],
  resources=[link("CS224N notes", CS224N), link("Illustrated GPT-2", ILL_GPT2), link("CS336 L3", LECT[3])],
  approach="Section 3.2 and Table 1. Why $\\mathrm{softmax}(QK^\\top/\\sqrt{d_k})V$ stops variance growing with $d_k$; $O(1)$ max path length.",
  hooks=f"**Must master (rapid-fire):** parameter count for d_model=1024, 16 heads, 24 layers, 50K vocab; why FFN expands to 4×d_model; pre-norm vs post-norm gradient flow; LayerNorm vs RMSNorm; ReLU → GeLU → SwiGLU; why modern models drop dropout; what individual heads learn; sinusoidal vs learned vs RoPE vs ALiBi ([RoPE paper]({ABS}2104.09864), [ALiBi paper]({ABS}2108.12409)) and why absolute encodings fail past training length.",
  experiments=[exp(H, "Remove `/ math.sqrt(d_k)` at d_k=512, feed random normal Q, K, inspect `Q.grad` — softmax goes one-hot and gradients vanish."),
               exp(H, "Change −inf to 0 in the causal mask; val loss collapses to ~0 while generation is garbage.")],
  note="This is the single most-asked implementation; the full decoder block is Phase 2 row 3."),
 dict(n=5, module=2, slug="vit", short="ViT", year="2020",
  title="An Image is Worth 16x16 Words",
  paper=[link("Paper", ABS + "2010.11929"), link("PDF", PDF + "2010.11929.pdf")],
  videos=[vid("Yannic Kilcher ViT Walkthrough", "Gl48KciWZp0")], resources=[],
  approach="How 16×16 patching removes CNN inductive biases (locality, translation equivariance). Figure 7: RGB PCA filters, position-embedding cosine similarity, attention distance by depth. Takeaway: scale beats inductive bias past ~14M images.",
  hooks="",
  experiments=[exp(HA, "Tiny ViT vs ResNet-18 on 5k CIFAR-10 images; ResNet wins."),
               exp(H, "Zero `pos_embedding`, shuffle patches, verify the [CLS] output is identical (permutation equivariance).")]),
 dict(n=6, module=2, slug="gpt3", short="GPT-3", year="2020",
  title="Language Models are Few-Shot Learners",
  paper=[link("Paper", ABS + "2005.14165"), link("PDF", PDF + "2005.14165.pdf")],
  videos=[vid("Yannic Kilcher GPT-3 Walkthrough", "SY5PvZrJhLE"), vid("Karpathy: Reproduce GPT-2 (124M)", "l8pRSuU81PU")],
  resources=[link("Karpathy build-nanogpt (repo)", NANOGPT), link("CS336 L2", LECT[2]), link("CS336 L13", LECT[13]), link("CS336 L14", LECT[14])],
  approach="Figure 1.2 and Section 3: in-context learning with no weight updates; scaling curves on WordScramble and translation. Read the data section (Common Crawl filtering, dedup) alongside CS336 Data lectures.",
  hooks="",
  experiments=[exp(HA, "Follow build-nanogpt and log tokens/sec as you enable `set_float32_matmul_precision('high')`, bf16 autocast, `torch.compile`, FlashAttention, and vocab padding 50257 → 50304."),
               exp(AG, "Few-shot label-flipping (Great movie → Negative) on an open 7B model to see scale override priors.")]),
 dict(n=7, module=3, slug="dqn", short="DQN", year="2013",
  title="Playing Atari with Deep Reinforcement Learning",
  paper=[link("Paper", ABS + "1312.5602"), link("PDF", PDF + "1312.5602.pdf")],
  videos=[vid("Yannic Kilcher DQN Walkthrough", "rFwQDDbYTm4")], resources=[],
  approach="The deadly triad (function approximation, bootstrapping, off-policy). Why experience replay breaks temporal correlation and why a target network stabilizes moving Bellman targets.",
  hooks="",
  experiments=[exp(H, "100-line DQN on `CartPole-v1`; set replay buffer = batch_size, or update the target net every step — Q-values diverge."),
               exp(HA, "Frame-stacking ablation.")]),
 dict(n=8, module=3, slug="ppo", short="PPO", year="2017",
  title="Proximal Policy Optimization Algorithms",
  paper=[link("Paper", ABS + "1707.06347"), link("PDF", PDF + "1707.06347.pdf")],
  videos=[vid("UC Berkeley CS285: Policy Gradients", "KZd508qGFt0"), vid("John Schulman: TRPO & PPO", "xvRrgxcpaHY")],
  resources=[link("Ivison: Policy Gradient for LMs (read first)", IVISON), link("CleanRL ppo.py", CLEANRL), link("CS336 L16", LECT[16]), link("CS336 L17", LECT[17])],
  approach="Trace why vanilla PG collapses when one step moves the policy too far. Equation 7 (clipped surrogate) and GAE. First-order clipping buys TRPO-style trust-region stability cheaply.",
  hooks="**Rapid-fire:** PPO vs GRPO — PPO keeps a learned value/critic, GRPO replaces it with group-normalized rewards.",
  experiments=[exp(HA, "In CleanRL's `ppo.py` on LunarLander, delete `torch.clamp(ratio, 1−ε, 1+ε)` and raise `update_epochs` 4 → 20; KL spikes, policy collapses to one action."),
               exp(HA, "Disable advantage normalization and watch variance explode.")]),
 dict(n=9, module=3, slug="ddpm", short="DDPM", year="2020",
  title="Denoising Diffusion Probabilistic Models",
  paper=[link("Paper", ABS + "2006.11239"), link("PDF", PDF + "2006.11239.pdf")],
  videos=[vid("Stanford CS236: Score & Diffusion", "VsllsC2JMGY"), vid("Umar Jamil DDPM Code & Math", "I1sPXkm2NH4")], resources=[],
  approach="Derive the closed-form forward jump $x_t = \\sqrt{\\bar\\alpha_t}\\,x_0 + \\sqrt{1-\\bar\\alpha_t}\\,\\epsilon$. Section 3.2: why predicting $\\epsilon$ with MSE equals the ELBO and score matching.",
  hooks="",
  experiments=[exp(HA, "Tiny DDPM on MNIST; switch the U-Net target from $\\epsilon$ to $x_0$ and see blurry samples (Table 2)."),
               exp(HA, "Set the Langevin noise $z = 0$ at every reverse step and watch deterministic sampling fail under the DDPM formulation.")]),
 dict(n=10, module=4, slug="lora", short="LoRA", year="2021",
  title="LoRA: Low-Rank Adaptation of Large Language Models",
  paper=[link("Paper", ABS + "2106.09685"), link("PDF", PDF + "2106.09685.pdf")],
  videos=[vid("Umar Jamil LoRA Math & Code", "PXWYUTMt-AU"), vid("AI Coffee Break LoRA Ablations", "KEv-F5UkhxU")], resources=[],
  approach="Intrinsic rank (Li et al. 2018). Section 4: freeze $W_0$, inject $\\Delta W = (\\alpha/r)BA$, $B = 0$ and $A \\sim \\mathcal{N}(0, \\sigma^2)$; Tables 5–6: adapting $W_q$ and $W_v$ at r=4 beats $W_q$ alone at r=64.",
  hooks=f"**Rapid-fire:** which layers to adapt (q, v vs all linear); when LoRA loses to full fine-tuning; [QLoRA]({ABS}2305.14314) (NF4 base + bf16 adapters, double quantization); adapters, prefix tuning, IA³. SVD from Phase 1 is the math.",
  experiments=[exp(H, "15-line `nn.Linear` wrapper. Init both A and B to zero (gradients identically zero, a saddle) or both Gaussian (ΔW ≠ 0 at step 0, corrupting the base)."),
               exp(HA, "Rank sweep r ∈ {1, 4, 64}; plot singular values of ΔW.")]),
 dict(n=11, module=4, slug="instructgpt", short="InstructGPT", year="2022",
  title="Training language models to follow instructions with human feedback",
  paper=[link("Paper", ABS + "2203.02155"), link("PDF", PDF + "2203.02155.pdf")],
  videos=[vid("Stanford CS224N: RLHF Lecture", "SXpJ9EmG3s4"), vid("Umar Jamil RLHF Math & Code", "qGyFrqc34yc")],
  resources=[link("CS336 L15", LECT[15]), link("Nathan Lambert's RLHF Book", RLHFBOOK)],
  approach="The SFT → reward model → PPO-ptx pipeline. Bradley–Terry loss $-\\log\\sigma(r(x, y_w) - r(x, y_l))$; the per-token KL penalty $\\beta \\log(\\pi_{RL}/\\pi_{SFT})$ as the anti-reward-hacking term.",
  hooks="**Rapid-fire:** why SFT masks loss on prompt tokens; a 1.3B aligned model is preferred over 175B unaligned.",
  experiments=[exp(AG, "Build the toy RLHF loop (GPT-2 policy, DistilBERT sentiment reward, TRL)."),
               exp(H, "Set β = 0 and watch the policy degenerate into \"excellent! best! 10/10!\" — Goodhart's law live.")]),
 dict(n=12, module=4, slug="chinchilla", short="Chinchilla", year="2022",
  title="Training Compute-Optimal Large Language Models",
  paper=[link("Paper", ABS + "2203.15556"), link("PDF", PDF + "2203.15556.pdf")],
  videos=[vid("Chinchilla Scaling Laws Explained", "PZXN7jm9IC0")],
  resources=[link("CS336 L9", LECT[9]), link("CS336 L11", LECT[11]), link("CS336 A3", A[3])],
  approach=f"[Kaplan et al. (2020)]({ABS}2001.08361) vs Hoffmann: three IsoFLOP methods, $L(N, D) = E + A/N^\\alpha + B/D^\\beta$, FLOPs ≈ 6ND, ~20 tokens/parameter.",
  hooks="The equation every candidate must know cold: $N^* \\propto C^{0.5}$, $D^* \\propto C^{0.5}$. Also: why tokenizer efficiency shifts the frontier; the emergent-abilities debate (real phase transitions vs metric artifacts).",
  experiments=[exp(H, "NumPy script for $L(N, D) = 1.69 + 406.4/N^{0.34} + 410.7/D^{0.28}$ under $C = 6ND$; plot loss vs N per FLOP budget."),
               exp(HA, "Train a tiny Transformer 2,000 steps with `CosineAnnealingLR(T_max=10000)` vs `T_max=2000` and see why Kaplan was fooled by not decaying to zero.")]),
 dict(n=13, module=4, slug="dpo", short="DPO", year="2023",
  title="Direct Preference Optimization: Your Language Model is Secretly a Reward Model",
  paper=[link("Paper", ABS + "2305.18290"), link("PDF", PDF + "2305.18290.pdf")],
  videos=[vid("Umar Jamil DPO Derivation & Code", "hvGa5Mba4c8")],
  resources=[link("CS336 A5 optional part 2", A[5])],
  approach="Derive Section 4 on paper: solve the KL-constrained reward maximization for $r(x, y) = \\beta \\log(\\pi_\\theta/\\pi_{ref}) + \\beta \\log Z(x)$, plug into Bradley–Terry, watch $Z(x)$ cancel. Any LM is implicitly a reward model; RLHF becomes stable binary cross-entropy with no critic and no online sampling.",
  hooks="",
  experiments=[exp(H, "The 6-line loss (Phase 2 row 14)."),
               exp(H, "Remove `ref_logps` (naive unlikelihood training) or set β = 0.001 vs 5.0; probability mass collapses onto degenerate tokens.")]),
 dict(n=14, module=4, slug="mamba", short="Mamba", year="2023",
  title="Mamba: Linear-Time Sequence Modeling with Selective State Spaces",
  paper=[link("Paper", ABS + "2312.00752"), link("PDF", PDF + "2312.00752.pdf")],
  videos=[vid("Mamba Author Talk (COLM Oral)", "X-7rgesJaGM"), vid("Umar Jamil Mamba & S4 Math", "8Q_tqwpTpVU")], resources=[],
  approach="Continuous SSM → zero-order-hold discretization → why LTI models (S4) fail selective copying and induction heads. Input-dependent $B, C, \\Delta$ break the convolution, requiring a parallel associative scan (Blelloch 1990). $O(N)$ with Transformer-quality modeling.",
  hooks="",
  experiments=[exp(HA, "Synthetic selective-copying dataset; static LTI recurrence vs selective ($B_t = W_B x_t$); LTI fails to filter variable-spaced noise."),
               exp(H, "Blelloch prefix-sum scan in PyTorch, $O(N)$ sequential → $O(\\log N)$ parallel.")]),
 dict(n=15, module=5, slug="chain-of-thought", short="Chain-of-Thought", year="2022",
  title="Chain-of-Thought Prompting Elicits Reasoning in Large Language Models",
  paper=[link("Paper", ABS + "2201.11903"), link("PDF", PDF + "2201.11903.pdf")],
  videos=[vid("Stanford CS25: Jason Wei on CoT", "3gb-ZkVRemQ"), vid("CMU CS 11-768: Tool & Code Agents", "jXChFB4JSyw")],
  resources=[link("CS336 L12 (evaluation)", LECT[12])],
  approach="Why few-shot prompting has a flat scaling curve on GSM8K. CoT as adaptive test-time compute via an externalized scratchpad (Nye et al. 2021). Emergent at scale when intermediate states are materialized as tokens.",
  hooks="",
  experiments=[exp(AG, "Harness that force-decodes a wrong intermediate step (\"14 × 3 = 99\") on GSM8K and measures whether the model self-corrects."),
               exp(HA, "Self-consistency, K=10 samples at T=0.7 with majority vote; expect +10–15% over greedy.")]),
 dict(n=16, module=6, slug="llama", short="LLaMA and Llama 3", year="2023, 2024",
  title="LLaMA (2023) and Llama 3 (2024)",
  paper=[link("LLaMA paper", ABS + "2302.13971"), link("LLaMA PDF", PDF + "2302.13971.pdf"), link("Llama 3 paper", ABS + "2407.21783")],
  videos=[vid("Umar Jamil LLaMA Math Breakdown", "Mn_9W1nCFLo"), vid("Coding LLaMA 2 From Scratch", "oM4VmoabDAI")],
  resources=[link("GQA paper", ABS + "2305.13245"), link("Scaling book ch. 6", SB + "applied-training"), link("Scaling book ch. 8", SB + "applied-inference")],
  approach="Contrast every block with #4: pre-RMSNorm, SwiGLU, RoPE (relative position via 2D complex rotation), GQA. Inference-optimal models over-train small architectures on 15T+ tokens and shrink the KV cache via GQA.",
  hooks="**Rapid-fire:** KV cache size = 2 × n_layers × seq_len × d_model × bytes (a 70B model at 128K tokens in bf16 needs ~200 GB); GQA reduces it by n_heads/n_kv_heads.",
  experiments=[exp(H, "RoPE in 15 lines via `torch.polar`; verify $\\langle \\mathrm{RoPE}(q, m), \\mathrm{RoPE}(k, n) \\rangle$ depends only on $m - n$; then exceed `max_seq_len` without frequency scaling."),
               exp(HA, "Profile VRAM with $H_{kv} = 32$ vs 4.")]),
 dict(n=17, module=6, slug="flashattention", short="FlashAttention", year="2022, 2023",
  title="FlashAttention (2022) and FlashAttention-2 (2023)",
  paper=[link("FlashAttention paper", ABS + "2205.14135"), link("FlashAttention PDF", PDF + "2205.14135.pdf"), link("FlashAttention-2 paper", ABS + "2307.08691")],
  videos=[vid("Tri Dao: Optimizing Attention", "cPwt1Y10gjI"), vid("FlashAttention in Triton From Scratch", "zy8ChVd_oTM")],
  resources=[link("CS336 L5", LECT[5]), link("CS336 L6", LECT[6]), link("CS336 A2", A[2]), link("Scaling book ch. 1 (rooflines)", SB + "roofline")],
  approach="Memory-bound vs compute-bound (arithmetic intensity). Standard attention writes an $O(N^2)$ matrix to HBM; Section 3's tiling and online softmax (running max $m$, running sum $\\ell$) keep it exact and in SRAM.",
  hooks="**Rapid-fire:** \"Flash Attention doesn't change the math, so why is it 5–10x faster?\"",
  experiments=[exp(H, "Tiled online softmax over a 10,000-vector in chunks of 100, `allclose` vs `F.softmax`."),
               exp(HA, "Naive `Q @ K.T` at N=16,384 (CUDA OOM) vs `F.scaled_dot_product_attention`."),
               exp(AG, "The Triton FlashAttention-2 kernel from CS336 A2 — you must be able to explain every tile boundary, not write it blind.")]),
 dict(n=18, module=6, slug="mixture-of-experts", short="Switch Transformers and DeepSeek-V3", year="2021, 2024",
  title="Switch Transformers (2021) and DeepSeek-V3 (2024)",
  paper=[link("Switch paper", ABS + "2101.03961"), link("Switch PDF", PDF + "2101.03961.pdf"),
         link("DeepSeek-V3 paper", ABS + "2412.19437"), link("DeepSeek-V3 PDF", PDF + "2412.19437.pdf")],
  videos=[vid("Yannic Kilcher Switch Transformers", "5n2bc30059Q"), vid("Mixtral MoE & Sliding Window", "UiX8K-xBUpE")],
  resources=[link("CS336 L4", LECT[4])],
  approach="Replacing the dense FFN with E experts + a top-k router decouples parameters (capacity) from FLOPs per token. Routing collapse and its fixes: load-balancing auxiliary loss vs DeepSeek-V3's auxiliary-loss-free bias adjustment. Conditional compute is how 600B+ models serve fast.",
  hooks="",
  experiments=[exp(H, "Mini MoE with 8 experts and a top-2 softmax router, no balancing loss; histogram of expert utilization over 500 steps shows 1–2 experts taking >95% and the rest dying."),
               exp(HA, "Add the aux loss, then the bias trick, re-plot.")]),
 dict(n=19, module=7, slug="deepseek-r1-grpo", short="DeepSeekMath and DeepSeek-R1", year="2024, 2025",
  title="DeepSeekMath (2024, GRPO) and DeepSeek-R1 (2025)",
  paper=[link("DeepSeekMath paper", ABS + "2402.03300"), link("DeepSeek-R1 paper", ABS + "2501.12948"), link("DeepSeek-R1 PDF", PDF + "2501.12948.pdf")],
  videos=[vid("Yannic Kilcher: GRPO & DeepSeekMath", "bAWV_yrqx4w"), vid("Coding GRPO From Scratch in PyTorch", "FRledQUbKyU")],
  resources=[link("Murali's Lightweight Guide to GRPO (no RL prerequisite)", MURALI), link("Ivison's policy-gradient notes (goes as far as CISPO)", IVISON),
             link("CS336 L16", LECT[16]), link("CS336 L17", LECT[17]), link("CS336 A5", A[5])],
  approach="Connect #8 PPO + #15 CoT. GRPO drops the critic: sample G completions per prompt, $\\hat{A}_i = (r_i - \\mathrm{mean}(r))/\\mathrm{std}(r)$, importance ratio with stop-gradient on old log-probs, clip at ε.",
  hooks="Know the neighbors: RLOO (leave-one-out), REINFORCE++, VinePPO, CISPO; why most 2025 implementations set the KL coefficient β = 0 (clipping already bounds the step); on- vs off-policy trade-off; the \"forking tokens\" result.",
  experiments=[exp(AG, "Build the mini-GRPO loop (TRL or Unsloth) on Qwen2.5-1.5B with GSM8K or Countdown and a rule-based reward (+1 format, +2 correct)."),
               exp(H, "The loss itself (Phase 2 row 15)."),
               exp(HA, "G = 8 → 2, advantages become too noisy; plot `<think>` length growing over steps.")]),
 dict(n=20, module=8, slug="diffusion-transformers", short="DiT", year="2023",
  title="Scalable Diffusion Models with Transformers",
  paper=[link("Paper", ABS + "2212.09748"), link("PDF", PDF + "2212.09748.pdf")],
  videos=[vid("DiT Explanation & PyTorch Code", "aSLDXdc2hkk"), vid("Stanford CS25: Transformers in Diffusion", "L45iAba2DAw")], resources=[],
  approach="#5 ViT + #9 DDPM. Patchify latents into tokens; adaLN-Zero injects t and class c by predicting $(\\gamma, \\beta, \\alpha)$ with the final linear layer zero-initialized so each block starts as identity. More GFLOPs → lower FID.",
  hooks="",
  experiments=[exp(H, "One DiT block with the conditioning MLP; zero-init its final linear vs Xavier and watch early convergence speed (the ResNet zero-γ trick again)."),
               exp(AG, "The full latent-diffusion training scaffold.")]),
 dict(n=21, module=8, slug="flow-matching", short="Flow Matching", year="2023",
  title="Flow Matching for Generative Modeling",
  paper=[link("Paper", ABS + "2210.02747"), link("PDF", PDF + "2210.02747.pdf")],
  videos=[vid("Yannic Kilcher Flow Matching", "7NNxK3CqaDk"), vid("MIT 6.S184: Flow Matching & Diffusion", "firXjwZ_6KI")], resources=[],
  approach="Contrast with #9. Straight-line interpolation $x_t = (1-t)x_0 + t x_1$, train $v_\\theta(x_t, t) \\approx x_1 - x_0$, sample with an ODE solver. Straight optimal-transport paths give good samples in 10–20 Euler steps instead of 1,000.",
  hooks="",
  experiments=[exp(H, "50-line 2D flow matching on Two Moons / Swiss Roll, 3-layer MLP, Euler loop with N=5 steps vs DDPM at N=5; plot trajectories.")]),
]
for p in papers:
    p.setdefault("note", "")

phase3 = {
    "id": "p3", "nav": "21-paper curriculum", "num": 3, "title": "The 21-paper curriculum, merged with the concept deep-dives", "weeks": "weeks 5–20",
    "intro": ["Your paper sequence stays intact; what changes is that each paper now also carries the interview questions and \"what to master\" items from Alisa's map, and each experiment carries a HAND / HAND→AGENT / AGENT tag. The weekly loop per paper (Day 1 read, Day 2 derive and watch, Day 3 break it) is in the Execution section. Paper 1 (AlexNet) is already done in your notebook; start at Paper 2."],
    "after": ["**What goes on the CV from this phase.** Two or three of the HAND→AGENT experiments, polished into small public repos with a README that states the hypothesis, the one-line change that broke the equation, and the plot. Candidates: the Transformer scaling/masking ablation (#4), the MoE routing-collapse study (#18), and the GRPO group-size study (#19). These are the ones you can defend line by line in a technical discussion."],
    "sources": f"your 21-paper roadmap PDF · [alisa-roadmap README, Phase 1]({ALISA}) · [Ivison, Introduction to Policy Gradient for LMs]({IVISON}) · [Manohar, Lightweight Guide to GRPO]({MURALI})",
}

# ---------------------------------------------------------------- phase 4
phase4 = {
    "id": "p4", "nav": "Systems and infra", "num": 4, "title": "Systems and infra topics the papers skip", "weeks": "weeks 21–22, plus rapid-fire review",
    "intro": ["Five topic clusters from Alisa's map have no paper in your curriculum but appear constantly in rapid-fire technical discussions. Each gets a reading, a small HAND implementation, and the specific question it is known to unlock."],
    "clusters": [
        {"id": "C1", "name": "Tokenization", "slug": "tokenization",
         "read": f"{L(1)}; [minbpe]({MINBPE}); [CS336 A1 handout]({A1_HANDOUT})",
         "master": "BPE merge algorithm; WordPiece vs SentencePiece; pre-tokenization and Unicode normalization; why \" hello\" and \"hello\" differ; vocab-size trade-off (fewer tokens per sentence vs more embedding params); why bad tokenization hurts code and multilingual models",
         "hand": "BPE from a corpus, 45 min (Phase 2)",
         "question": "\"Time complexity of the merge step?\" \"Why does tokenizer efficiency shift the Chinchilla frontier?\""},
        {"id": "C2", "name": "Inference and the KV cache", "slug": "inference-kv-cache",
         "read": f"{L(10)}; [Scaling book ch. 7]({SB}inference); [PagedAttention / vLLM]({ABS}2309.06180); [speculative decoding]({ABS}2211.17192)",
         "master": "Prefill (parallel) vs decode (sequential); KV cache size = 2 × n_layers × seq_len × d_model × bytes; what happens when VRAM runs out; speculative decoding (~2–3x); PagedAttention as OS-style virtual memory; greedy vs beam vs top-k vs top-p vs temperature and the failure modes of each",
         "hand": "KV cache for generation, 20 min; top-k/top-p and beam search (Phase 2)",
         "question": "\"70B model, 96 layers, d_model 8192, bf16, one 128K sequence — how much KV memory?\" (~200 GB)"},
        {"id": "C3", "name": "Distributed training", "slug": "distributed-training",
         "read": f"{L(7)}–[8]({LECT[8]}); [Scaling book ch. 3]({SB}sharding), [ch. 5]({SB}training), [ch. 12 (GPUs)]({SB}gpus); [ZeRO]({ABS}1910.02054); [Megatron-LM]({ABS}1909.08053); [CS336 A2]({A[2]})",
         "master": "Data parallel (AllReduce gradients) vs tensor parallel (split weight matrices, AllGather activations) vs pipeline parallel (micro-batches to shrink the bubble) vs expert parallel; ZeRO stages 1–3; rematerialization, gradient accumulation, host offload; roofline reasoning (compute vs memory vs communication bound); \"5D parallelism\"",
         "hand": "A memory-math worksheet: params, grads, Adam states, activations per GPU under each scheme (HAND, on paper); the distributed trainer itself is AGENT, from CS336 A2",
         "question": "\"8 × 80 GB A100s, 70B model — walk me through memory math and parallelism strategy.\" \"What is 5D parallelism?\""},
        {"id": "C4", "name": "Evaluation", "slug": "evaluation",
         "read": L(12),
         "master": "Perplexity vs downstream benchmarks; contamination; pass@k; LM-as-judge pitfalls; why a benchmark gain can be a metric artifact (ties into the emergence debate)",
         "hand": "A pass@k estimator from n samples (10 lines)",
         "question": "\"How would you know if your model got better?\""},
        {"id": "C5", "name": "Data", "slug": "data",
         "read": f"{L(13)}–[14]({LECT[14]}); [CS336 A4]({A[4]}); GPT-3 and Llama 3 data sections",
         "master": "Common Crawl → usable text: language ID, quality filters, exact and fuzzy dedup (MinHash), PII removal; data mixing and curriculum",
         "hand": "MinHash dedup on a small corpus (HAND→AGENT)",
         "question": "\"Design a filtering pipeline and tell me how you'd validate it.\""},
    ],
    "after": [f"**The scaling book.** [How to Scale Your Model]({SB}) (Austin et al., Google DeepMind) is the reference for the infra cluster. Read chapters 1, 4, 5 and 7 in full and work the exercises; skim 2, 3 and 12 for notation; chapters 6 and 8 (training and serving Llama 3) are the worked examples to reproduce the arithmetic for on paper."],
    "sources": f"[alisa-roadmap README, Phase 1 and 2 sections]({ALISA}) · [CS336 Spring 2025]({CS336}) · [How to Scale Your Model]({SB})",
}

# ---------------------------------------------------------------- phase 5
phase5 = {
    "id": "p5", "nav": "General coding", "num": 5, "title": "General coding fluency", "weeks": "30 minutes daily from week 3",
    "intro": [f"Target: LeetCode Mediums consistently under 25 minutes, with AI off. This is a daily habit, not a phase, because algorithmic patterns leak into ML-coding rounds (top-K heaps are decoding; sliding windows are sliding-window attention; DP is beam search and edit distance). Alisa's two lists are the whole syllabus: [LeetCode 75]({LC75}) first, then [NeetCode Blind 75]({BLIND75})."],
    "lists": [{"id": "LC75", "label": "LeetCode 75", "url": LC75, "total": 75}, {"id": "B75", "label": "NeetCode Blind 75", "url": BLIND75, "total": 75}],
    "topics": [{"id": f"T{i+1}", "topic": t, "reach": r, "tie": m} for i, (t, r, m) in enumerate([
        ("Arrays, strings, hash maps", "The base of most problems", "Tokenizer merge tables"),
        ("Two pointers / sliding window", "Fixed and variable windows", "Sliding-window attention, local masks"),
        ("Binary search", "Including search on the answer space", "Hyperparameter bisection, top-p cutoff"),
        ("Stacks, queues", "BFS/DFS traversal patterns", "Beam-search frontier"),
        ("Trees", "DFS, BFS, LCA; trees disguised as graphs", "Parse trees, MCTS-style search"),
        ("Graphs", "BFS, DFS, topological sort, Dijkstra", "Autograd DAG ordering, pipeline schedules"),
        ("Dynamic programming", "1D and 2D; memo vs tabulation; edit distance, coin change, LCS", "Viterbi, CTC, beam search"),
        ("Heaps / priority queues", "Top-K problems", "Top-k sampling, beam search"),
        ("Sorting", "Quick, merge, heap; time and space for each", "Length-bucketing batches"),
    ])],
    "after": ["Keep a one-line log per problem (pattern, time, mistake). Every two weeks, redo the five slowest."],
    "sources": f"[alisa-roadmap README, Phase 4]({ALISA}) · [Notes on the Industry Job Search, Appendix]({BLOG})",
}

# ---------------------------------------------------------------- phase 6
phase6 = {
    "id": "p6", "nav": "Portfolio and interviews", "num": 6, "title": "Research portfolio, technical discussion, job talk, behavioral", "weeks": "weeks 23–24, then continuous",
    "intro": ["Research gets you the interview; this phase makes sure you can defend it. Alisa's framing: the technical-discussion round is the most underrated, and the behavioral round is the one she failed first by assuming she was \"obviously well-behaved\" and then going blank.",
              "**Build the portfolio (AGENT-heavy, HAND-defensible).** As a student without a PhD paper trail, your CV projects are the research record. Aim for three public projects by week 20, each with a hypothesis, an ablation, a plot, and a README written in the \"why I did it\" voice:"],
    "portfolio": [
        {"id": "PF1", "text": "One from the Phase 3 break-it experiments (see the CV note at the end of Phase 3)."},
        {"id": "PF2", "text": f"One systems project: a from-scratch GPT-2 124M reproduction on [build-nanogpt]({NANOGPT}) with your own throughput log, or [CS336 A2]({A[2]})'s FlashAttention-2 Triton kernel with a benchmark table."},
        {"id": "PF3", "text": f"One post-training project: the mini-GRPO or DPO run from [CS336 A5]({A[5]}), with reward curves and a failure-mode study (β = 0, G = 2)."},
    ],
    "afterPortfolio": "For each, the HAND core (model, loss, loop) is yours; the harness, sweeps and plots are the agent's; and you must be able to answer \"why is this line here?\" for every file. Write the design-choice list before you consider a project done.",
    "prep": [
        {"id": "PR1", "title": "Technical and research discussion prep", "text": "For every project, write a one-page \"why\" narrative, not a \"what\" summary: every major design choice with its defensible reason, what you tried that failed, what you would do differently, and what you would do with 10x the compute. Form opinions on three to five research directions you believe in right now. Tailor the pitch to the role: interviewers are tired, so hit the keywords of the team's area."},
        {"id": "PR2", "title": "Rapid-fire set, out loud", "text": "Drill the rapid-fire set out loud, with AI as the examiner: ways to encode position; 5D parallelism; PPO vs GRPO; pre- vs post-norm; LoRA layer choice; why Flash Attention is faster without changing the math; the KV-cache formula; Chinchilla's N* and D*. Read the target company's last six months of papers and reference them naturally."},
        {"id": "PR3", "title": "Job talk (if asked)", "text": "45–60 minutes, 80%+ on first-author or lead-author work, second-author and ongoing work in the last 10 minutes. Expect deep Q&A on every baseline and experimental choice; rehearse with people who push back hard."},
        {"id": "PR4", "title": "Behavioral", "text": "Write down five to ten memorable stories now and map each to leadership, conflict, failure, impact, collaboration in STAR form, so retrieval is instant. Prepare specific answers to \"Why this company?\" and to \"What is your view on AI safety and responsible development?\" — frontier labs ask the second one seriously and want a considered position. After every interview, record notes the same day; they feed the next cram."},
    ],
    "sources": f"[alisa-roadmap README, Phases 5–7]({ALISA}) · [Notes on the Industry Job Search]({BLOG})",
}

# ---------------------------------------------------------------- phase 7
phase7 = {
    "id": "p7", "nav": "Getting in the door", "num": 7, "title": "Getting in the door — networking, sequencing, negotiation", "weeks": "from week 1, in parallel",
    "intro": ["One referral is worth roughly forty cold applications (cold applications reply at ~1–2%, referrals at ~20%+), so the pipeline is built months before you need it, in parallel with everything above."],
    "groups": [
        {"title": "Build the referral pipeline (from week 1)", "ordered": False, "items": [
            {"id": "N1", "text": "Be visible at NeurIPS, ICML, ICLR, ACL, EMNLP — talk to people, don't just attend. Workshops and poster sessions are easier entry points for a student."},
            {"id": "N2", "text": "Collaborate across institutions; co-authors become referrers. Open-source contributions to repos labs actually use (vLLM, TRL, nanoGPT forks, CS336 leaderboards) are the student equivalent."},
            {"id": "N3", "text": "Reach out informally months before searching: nobody refers a stranger. Reconnecting with people you haven't spoken to in years is normal and expected."},
            {"id": "N4", "text": "Ask advisors, classmates and collaborators who already moved to industry. Use friends and recruiters to learn which teams actually have headcount; that can matter more than your preparation."},
        ]},
        {"title": "Sequence the applications", "ordered": True, "items": [
            {"id": "S1", "text": "Apply to less-desired companies first; they are practice, not consolation prizes. Watch your stamina — do not burn out before the companies you care about."},
            {"id": "S2", "text": "Do not open your top-choice processes until you hold at least one offer; leverage multiplies."},
            {"id": "S3", "text": "Time processes so offers land close together. Deadlines are flexible and recruiters expect you to finish other processes, but investigate each company's reputation for \"exploding\" offers."},
            {"id": "S4", "text": "Customize prep per company: recent papers, research agenda, product. Each interview is a slightly different class with three days to cram, so keep per-topic notes you can swap in."},
        ]},
    ],
    "after": ["**Negotiate.** The work is not done at the offer. Initial offers leave room by design and recruiters will say so. Before every recruiter call, write down what you will and will not share and a few lines you can say verbatim; anticipate their questions. Lean on friends for market data points. A few weeks of effort here can equal years of pay difference at the initial number."],
    "sources": f"[alisa-roadmap README, Phase 8]({ALISA}) · [Notes on the Industry Job Search]({BLOG}) · [Nathan Lambert, AI PhD job hunt]({LAMBERT})",
}

# ---------------------------------------------------------------- execution + timeline
execution = {
    "intro": "Each paper takes three days; the remaining two weekdays go to CS336 assignments and the portfolio. This keeps your original Day 1–3 loop and adds Alisa's two habits: explain it aloud, and keep running notes.",
    "steps": [
        {"day": "Day 1", "title": "Read and question", "tag": H, "body": "Read the paper's methodology, equations and ablation tables, not the intro. Write three questions you cannot yet answer."},
        {"day": "Day 2", "title": "Derive and watch", "tag": H, "body": f"Watch the paired walkthrough, then write the core derivation by hand (the √d_k variance argument, the DPO cancellation, the GRPO advantage). Add the result to your running LLM notebook."},
        {"day": "Day 3", "title": "Break it", "tag": HA, "body": "Run the experiment: you write the one change that breaks the equation; a coding agent builds the harness, data loader and plots. Save the plot and a two-line conclusion."},
        {"day": "Then", "title": "Explain it aloud", "tag": "", "body": "Ten minutes with an LLM as examiner, no notes. If you cannot explain it simply, you do not know it yet; repeat Day 2."},
        {"day": "Weekend", "title": "Drills and review", "tag": "", "body": "One full timed drill rotation from Phase 2 (AI off) and the week's LeetCode review."},
    ],
    "sources": f"your 21-paper roadmap PDF · [alisa-roadmap README, The Study System That Works]({ALISA}) · [Notes on the Industry Job Search]({BLOG})",
}

# Week bands read off the plan's 26-week chart (start week, end week inclusive).
timeline = {
    "title": "Twenty-six weeks: breadth first, then papers and drills, then interview prep",
    "caption": "Bands are weeks; diamonds are gates you must pass before moving on",
    "weeks": 26,
    "lanes": [
        {"name": "Breadth and math", "bands": [{"label": "CS336", "from": 1, "to": 2, "phase": "p0"}, {"label": "Math", "from": 3, "to": 4, "phase": "p1"}]},
        {"name": "Papers (Phase 3)", "key": True, "bands": [
            {"label": "M1", "from": 3, "to": 4, "modules": [1]}, {"label": "M2 (4–6)", "from": 5, "to": 8, "modules": [2]},
            {"label": "M3 (7–9)", "from": 9, "to": 11, "modules": [3]}, {"label": "M4 (10–14)", "from": 12, "to": 16, "modules": [4]},
            {"label": "M5+6", "from": 17, "to": 19, "modules": [5, 6]}, {"label": "M7+8", "from": 20, "to": 21, "modules": [7, 8]}]},
        {"name": "CS336 assignments", "bands": [
            {"label": "A1 Basics", "from": 3, "to": 6, "assign": ["A1"]}, {"label": "A5 RL", "from": 14, "to": 16, "assign": ["A5"]},
            {"label": "A2 Sys", "from": 17, "to": 19, "assign": ["A2"]}, {"label": "A3+A4", "from": 21, "to": 22, "assign": ["A3", "A4"]}]},
        {"name": "Drills + LeetCode", "bands": [{"label": "Weekly timed drills, daily LeetCode, all with AI off", "from": 3, "to": 26}]},
        {"name": "Portfolio + prep", "bands": [{"label": "Three portfolio repos", "from": 12, "to": 22}, {"label": "Prep", "from": 23, "to": 24}, {"label": "Mocks", "from": 25, "to": 26}]},
        {"name": "Networking", "muted": True, "bands": [{"label": "Conferences, collaborators and referrals, built months before you apply", "from": 1, "to": 26}]},
    ],
    "gates": [
        {"id": "G1", "label": "Decoder block in 30 min, AI off", "week": 9},
        {"id": "G2", "label": "3 repos started", "week": 17},
        {"id": "G3", "label": "Drills on target", "week": 22},
        {"id": "G4", "label": "First applications", "week": 26},
    ],
    "after": "The Papers lane is the spine; the gates are pass/fail checkpoints — if a gate fails, extend that band by a week rather than skipping ahead. Networking runs the full length because referrals take months to build.",
}

# ---------------------------------------------------------------- resource index
resources = {
    "intro": "Paper links are inline in Phase 3, and the YouTube walkthroughs named there are embedded with each paper (links from the original 21-paper roadmap).",
    "rows": [
        {"links": [link("alisa-roadmap (GitHub)", ALISA)], "use": "The knowledge map this plan merges; interview-type breakdown; rapid-fire questions", "phase": "All"},
        {"links": [link("Notes on the Industry Job Search — Alisa Liu", BLOG)], "use": "Primary source: timeline, interview types, preparation, negotiation", "phase": "All"},
        {"links": [link("Alisa's Book of LLMs (Notion)", BOOK_LLMS)], "use": "Model for your own running LLM notes", "phase": "0, 3, 4"},
        {"links": [link("Alisa's math notes (Notion)", MATH_NOTES)], "use": "Model for your math-interview notes", "phase": "1"},
        {"links": [link("Stanford CS336: Language Modeling from Scratch", CS336), link("YouTube", YT_PL + CS336_PL)], "use": "The breadth skeleton; 17 lectures", "phase": "0"},
        {"links": [link("CS336 A1 Basics", A[1]), link("A2 Systems", A[2]), link("A3 Scaling", A[3]), link("A4 Data", A[4]), link("A5 Alignment", A[5])], "use": "The implementation track", "phase": "0, 2, 3, 4"},
        {"links": [link("CS224N: Self-Attention and Transformers notes", CS224N)], "use": "Read before the attention drills", "phase": "2"},
        {"links": [link("The Illustrated GPT-2 — Jay Alammar", ILL_GPT2)], "use": "Visual walkthrough before implementing", "phase": "2"},
        {"links": [link("CS231n: Backpropagation", CS231N)], "use": "The NumPy backward pass", "phase": "1, 2"},
        {"links": [link("Introduction to Policy Gradient for LMs — Hamish Ivison", IVISON)], "use": "REINFORCE → baselines → importance weighting → GRPO/CISPO, in LM notation", "phase": "1, 3"},
        {"links": [link("Lightweight Guide to GRPO — Murali Manohar", MURALI)], "use": "GRPO with no RL prerequisite; clipping, off-policy, KL = 0", "phase": "3"},
        {"links": [link("Policy Gradient Algorithms — Lilian Weng", WENG)], "use": "Reference survey for the RL papers", "phase": "1, 3"},
        {"links": [link("RLHF Book — Nathan Lambert", RLHFBOOK)], "use": "Post-training end to end", "phase": "3"},
        {"links": [link("How to Scale Your Model — Austin et al.", SB)], "use": "Rooflines, Transformer math, parallelism, inference", "phase": "4"},
        {"links": [link("ML Interviews Book — Chip Huyen", HUYEN)], "use": "Gap-finding across classic ML", "phase": "1, 6"},
        {"links": [link("build-nanogpt", NANOGPT), link("minbpe", MINBPE), link("Zero to Hero playlist — Karpathy", YT_PL + ZTH_PL)], "use": "Reference implementations for GPT-2 and BPE", "phase": "2, 3"},
        {"links": [link("CleanRL", CLEANRL)], "use": "Single-file PPO for the break-it experiment", "phase": "3"},
        {"links": [link("LeetCode 75", LC75), link("NeetCode Blind 75", BLIND75)], "use": "Daily coding", "phase": "5"},
        {"links": [link("RunPod", RUNPOD), link("Lambda", LAMBDA)], "use": "~$2–3/hr H100 for self-study runs", "phase": "0, 3"},
        {"links": [link("Nathan Lambert: AI PhD job hunt", LAMBERT)], "use": "Second data point on timelines", "phase": "7"},
    ],
}

data = dict(meta=meta, interviews=interviews,
            phases=[phase0, phase1, phase2, phase3, phase4, phase5, phase6, phase7],
            modules=modules, papers=papers, execution=execution, timeline=timeline, resources=resources)

assert len(papers) == 21
OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {OUT.relative_to(OUT.parent.parent.parent)}: 21 papers, "
      f"{sum(len(p['experiments']) for p in papers)} experiments, "
      f"{sum(len(p['videos']) for p in papers)} videos")
