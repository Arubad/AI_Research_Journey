# AI Research Journey

My journey to learning advances in AI from a fundamental point of view.

A 26-week path to AI-lab research roles: breadth from Stanford CS336, math by hand, from-scratch drills with AI off, a 21-paper "break the equation" curriculum, the systems topics the papers skip, daily coding, a defensible portfolio, and the job search itself. Built from the *AI Lab Research Roadmap — Merged Master Plan* (Oct 27, 2026).

**Roadmap tracker:** https://arubad.github.io/AI_Research_Journey/

| Phase | Weeks | What | Folder |
| --- | --- | --- | --- |
| 0 | 1–2 | Stanford CS336, 17 lectures + 5 assignments | `phase-0-cs336/` |
| 1 | 3–4, then on call | Math derivations by hand, confirmed in code | `phase-1-math/` |
| 2 | from 5, weekly | 19 muscle-memory implementations, timed, AI off | `phase-2-drills/` |
| 3 | 5–20 | 21 papers, AlexNet → Flow Matching, each with break-it experiments | `phase-3-papers/` |
| 4 | 21–22 | Tokenization, inference, distributed training, evaluation, data | `phase-4-systems/` |
| 5 | daily from 3 | LeetCode 75, then NeetCode Blind 75 | `phase-5-leetcode/` |
| 6 | 23–24, then continuous | Portfolio, technical discussion, job talk, behavioral | `phase-6-portfolio/` |
| 7 | from 1, in parallel | Networking, sequencing, negotiation | `phase-7-job-search/` |

Every item carries a tag: **HAND** (write it from a blank file, AI off), **HAND→AGENT** (write the core, let an agent build the harness), or **AGENT** (delegate, but read and defend every line).

## Repository layout

```
AI_Research_Journey/
├── docs/                               GitHub Pages site (the tracker)
│   ├── index.html, assets/             page, styles, script
│   └── data/
│       ├── roadmap.json                the whole plan: text, links, videos, tags (generated)
│       └── progress.json               your committed progress (exported from the site)
├── phase-0-cs336/
│   ├── notes/L01-…md … L16-17-…md      one file per lecture
│   └── assignments/                    your clones of A1–A5
├── phase-1-math/
│   ├── derivations/M01-…md … M12-…md   one file per derivation
│   └── checks/                         the under-20-line numerical checks
├── phase-2-drills/
│   ├── 01-sdpa/ … 19-flow-matching/    README + attempts/YYYY-MM-DD.py
│   ├── tests/                          agent-built harness: test_NN.py per row
│   └── drill_log.csv
├── phase-3-papers/
│   └── module-N-…/NN-paper/            README (generated), notes.md, experiments/, figures/
├── phase-4-systems/<cluster>/          README (generated) + notes.md
├── phase-5-leetcode/                   log.csv, solutions/
├── phase-6-portfolio/                  projects.md, narratives/, rapid-fire.md, job-talk/
├── phase-7-job-search/                 README; private/ is git-ignored
├── shared/utils.py                     seeding, device pick, grad norms, param counts
├── scripts/
│   ├── build_roadmap.py                the plan as editable Python → docs/data/roadmap.json
│   └── scaffold.py                     roadmap.json → folders and READMEs
├── requirements.txt
└── Gen_Ai Dev roadmap.pdf              earlier roadmap, kept for reference
```

Why this shape:

- **Folders follow the plan's phases**, numbered so `ls` reads in study order, and each one's README is the same content as its section on the site.
- **One source of truth.** Edit `scripts/build_roadmap.py`, then run `python scripts/build_roadmap.py && python scripts/scaffold.py`. The site and every generated README update together. Your own files (`notes.md`, logs, attempts, experiments) are created once and never overwritten.
- **HAND work and AGENT work live apart.** Drill attempts are dated files you write from a blank page; the agent-maintained test harness sits in `phase-2-drills/tests/`. In paper folders, the one-line break goes in your notebook and the agent's harness goes beside it in `experiments/`.
- **Private things stay private.** Contacts, offers and negotiation notes go in `phase-7-job-search/private/` (git-ignored). Behavioral stories belong in a private repo.

## Tracking progress

The site tracks: Read / Derived / Broke it plus every experiment for each paper, CS336 lectures and assignments, math derivations, drill streaks (three under-target runs in a row clears a row), systems clusters, LeetCode counts and topics, portfolio and job-search checklists, the four gates, and your current week once you set a start date.

Everything saves in your browser immediately. To keep it in the repo, click **Download progress.json** at the bottom of the site, replace `docs/data/progress.json`, and commit. The site warns you when your browser has uncommitted changes.

## Setting up GitHub Pages (one time)

Repository **Settings → Pages → Build and deployment**: Source *Deploy from a branch*, Branch `main`, folder `/docs`.

Local preview: `python -m http.server -d docs`, then open http://localhost:8000.

## Environment

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
