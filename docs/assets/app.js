/* AI Lab Research Roadmap — tracker.
   Content: data/roadmap.json. Committed progress: data/progress.json.
   Changes made on the page live in localStorage until exported and committed. */
(() => {
  "use strict";
  const STORE = "arj-progress-v2";
  const STAGES = [
    { key: "read", label: "Read", hint: "Day 1" },
    { key: "derive", label: "Derived", hint: "Day 2" },
    { key: "lab", label: "Broke it", hint: "Day 3" },
  ];
  const TAG_CLASS = { "HAND": "t-hand", "HAND→AGENT": "t-mixed", "AGENT": "t-agent" };
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  let R, baseline, S;
  let filter = "all", query = "";

  // ---------------------------------------------------------------- helpers
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  // `code`, [label](url), **bold**; $math$ is left for KaTeX.
  function rich(s) {
    const codes = [];
    let t = esc(s).replace(/`([^`]+)`/g, (_, c) => (codes.push(c), `\u0000${codes.length - 1}\u0000`));
    t = t.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    t = t.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    return t.replace(/\u0000(\d+)\u0000/g, (_, i) => `<code>${codes[i]}</code>`);
  }
  const paras = (arr) => (arr || []).map((p) => `<p class="prose">${rich(p)}</p>`).join("");
  const tag = (t) => (t ? `<span class="tag ${TAG_CLASS[t] || ""}">${esc(t)}</span>` : "");
  const sources = (s) => (s ? `<p class="sources">Sources: ${rich(s)}</p>` : "");
  const extLink = (l) => `<a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)}</a>`;
  const today = () => new Date().toISOString().slice(0, 10);
  const daysSince = (d) => Math.floor((Date.parse(today()) - Date.parse(d)) / 864e5);
  const math = (el) => window.renderMathInElement && renderMathInElement(el, {
    delimiters: [{ left: "$", right: "$", display: false }], throwOnError: false,
    output: window.__KATEX_OUTPUT__ || "htmlAndMathml",
  });
  const ytEmbed = (id) => `https://www.youtube-nocookie.com/embed/${id}?rel=0`;
  const ytWatch = (id) => `https://www.youtube.com/watch?v=${id}`;
  const plEmbed = (list) => `https://www.youtube-nocookie.com/embed/videoseries?list=${list}`;
  const plWatch = (list) => `https://www.youtube.com/playlist?list=${list}`;

  // ---------------------------------------------------------------- state
  const blankPaper = (p) => ({ read: false, derive: false, lab: false, experiments: p.experiments.map(() => false), started: "", finished: "", notes: "" });
  function normalise(raw) {
    raw = raw || {};
    const papers = {};
    for (const p of R.papers) {
      const r = (raw.papers && raw.papers[p.n]) || {};
      papers[p.n] = { ...blankPaper(p), ...r, experiments: p.experiments.map((_, i) => !!(r.experiments && r.experiments[i])) };
    }
    return {
      startDate: raw.startDate || "",
      papers,
      checks: { ...(raw.checks || {}) },
      streaks: { ...(raw.streaks || {}) },
      counts: { ...(raw.counts || {}) },
    };
  }
  function serialise(st) {
    const papers = {};
    for (const p of R.papers) {
      const s = st.papers[p.n], b = blankPaper(p);
      if (Object.keys(b).some((k) => JSON.stringify(s[k]) !== JSON.stringify(b[k]))) papers[p.n] = s;
    }
    const pick = (o, keep) => Object.fromEntries(Object.entries(o).filter(([, v]) => keep(v)));
    return {
      startDate: st.startDate,
      papers,
      checks: pick(st.checks, Boolean),
      streaks: pick(st.streaks, (v) => v && (v.n || v.last)),
      counts: pick(st.counts, Boolean),
    };
  }
  const paperStatus = (s) => (s.read && s.derive && s.lab ? "done" : s.read || s.derive || s.lab || s.experiments.some(Boolean) ? "doing" : "todo");
  const chk = (k) => !!S.checks[k];
  const streakOf = (id) => (S.streaks[id] && S.streaks[id].n) || 0;

  function save() {
    try { localStorage.setItem(STORE, JSON.stringify({ updated: today(), ...serialise(S) })); } catch (_) {}
    refresh();
  }

  // ---------------------------------------------------------------- progress maths
  function phaseProgress(id) {
    const ph = R.phases.find((p) => p.id === id);
    const frac = (done, total) => ({ done, total });
    switch (id) {
      case "p0": {
        const keys = [...ph.lectures.map((l) => "p0." + l.id), ...ph.assignments.map((a) => "p0." + a.id)];
        return frac(keys.filter(chk).length, keys.length);
      }
      case "p1": return frac(ph.rows.reduce((a, r) => a + chk(`p1.${r.id}.derive`) + chk(`p1.${r.id}.code`), 0), ph.rows.length * 2);
      case "p2": return frac(ph.drills.filter((d) => streakOf(d.id) >= 3).length, ph.drills.length);
      case "p3": return frac(R.papers.reduce((a, p) => a + STAGES.filter((s) => S.papers[p.n][s.key]).length, 0), 63);
      case "p4": return frac(ph.clusters.filter((c) => chk("p4." + c.id)).length, ph.clusters.length);
      case "p5": {
        const topics = ph.topics.filter((t) => chk("p5." + t.id)).length;
        const solved = ph.lists.reduce((a, l) => a + Math.min(+S.counts[l.id] || 0, l.total), 0);
        const total = ph.lists.reduce((a, l) => a + l.total, 0);
        return frac(topics + solved, ph.topics.length + total);
      }
      case "p6": {
        const keys = [...ph.portfolio, ...ph.prep].map((x) => "p6." + x.id);
        return frac(keys.filter(chk).length, keys.length);
      }
      case "p7": {
        const keys = ph.groups.flatMap((g) => g.items.map((i) => "p7." + i.id));
        return frac(keys.filter(chk).length, keys.length);
      }
    }
    return frac(0, 1);
  }
  const moduleFrac = (mid) => {
    const ps = R.papers.filter((p) => p.module === mid);
    return ps.reduce((a, p) => a + STAGES.filter((s) => S.papers[p.n][s.key]).length, 0) / (ps.length * 3);
  };
  function currentWeek() {
    if (!S.startDate) return null;
    const d = daysSince(S.startDate);
    if (Number.isNaN(d)) return null;
    return Math.floor(d / 7) + 1;
  }

  // ---------------------------------------------------------------- section builders
  const section = (id, heading, sub, body, cls = "") =>
    `<section class="sec ${cls}" id="${id}" aria-labelledby="${id}-h">
       <header class="sec-head"><h2 id="${id}-h">${heading}</h2>${sub ? `<p class="sec-sub">${esc(sub)}</p>` : ""}</header>
       ${body}
     </section>`;
  const check = (key, label, extra = "") =>
    `<label class="tick ${extra}"><input type="checkbox" data-check="${key}" ${chk(key) ? "checked" : ""}><span>${label}</span></label>`;

  function overviewHTML() {
    const m = R.meta;
    const tags = m.tags.map((t) => `
      <tr><th scope="row">${tag(t.tag)}</th><td>${rich(t.meaning)}</td><td>${rich(t.rule)}</td></tr>`).join("");
    return section("overview", "How to use this roadmap", "", `
      <div class="dash">
        <div class="dash-now" id="dash-now"></div>
        <div class="dash-bench">
          <div class="bench-head">
            <h3>21 papers</h3>
            <p class="legend"><span class="key key-read"></span>Read <span class="key key-derive"></span>Derived <span class="key key-lab"></span>Broke it</p>
          </div>
          <div class="bench-map" id="bench-map">${R.modules.map((mod) => `
            <div class="bench-module" data-phase2="${mod.id >= 6}">
              <span class="bench-module-label">M${mod.id}</span>
              <div class="bench-cells">${R.papers.filter((p) => p.module === mod.id).map((p) => `
                <button type="button" class="cell" data-goto="${p.n}" aria-label="Paper ${p.n}: ${esc(p.short)}">
                  ${STAGES.map((st) => `<span class="band b-${st.key}"></span>`).join("")}
                  <span class="num"><b>${p.n}</b></span>
                </button>`).join("")}</div>
            </div>`).join("")}
          </div>
        </div>
      </div>
      ${paras(m.intro)}
      <div class="table-wrap"><table class="grid tags-table">
        <thead><tr><th>Tag</th><th>Meaning</th><th>Rule of thumb</th></tr></thead>
        <tbody>${tags}</tbody></table></div>
      ${paras(m.afterTags)}`);
  }

  function interviewsHTML() {
    const iv = R.interviews;
    const rows = iv.rounds.map((r) => `
      <tr><th scope="row" data-label="Round">${esc(r.round)}<span class="share">${esc(r.share)}</span></th>
      <td data-label="What they are testing">${rich(r.testing)}</td>
      <td data-label="What passing looks like">${rich(r.passing)}</td>
      <td data-label="Where this roadmap covers it">${esc(r.where)}</td></tr>`).join("");
    return section("interviews", esc(iv.title), "", `
      ${paras([iv.intro])}
      <div class="share-bar" aria-hidden="true">${iv.rounds.filter((r) => r.share.startsWith("~")).map((r) =>
        `<span style="flex:${parseInt(r.share.slice(1))}"><b>${esc(r.share)}</b> ${esc(r.round)}</span>`).join("")}</div>
      <div class="table-wrap"><table class="grid stack">
        <thead><tr><th>Round</th><th>What they are testing</th><th>What passing looks like</th><th>Where this roadmap covers it</th></tr></thead>
        <tbody>${rows}</tbody></table></div>
      ${paras([iv.after])}${sources(iv.sources)}`);
  }

  const playlistHTML = (pl) => `
    <figure class="player playlist">
      <div class="frame"><iframe src="${plEmbed(pl.list)}" title="${esc(pl.title)} (YouTube playlist)" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div>
      <figcaption>${esc(pl.title)} <a href="${plWatch(pl.list)}" target="_blank" rel="noopener">Open playlist on YouTube</a></figcaption>
    </figure>`;

  function phaseHead(ph) { return `Phase ${ph.num}: ${esc(ph.title)}`; }

  function p0HTML(ph) {
    const rows = ph.lectures.map((l) => `
      <tr>
        <td class="c-tick" data-label="Watched">${check("p0." + l.id, `<span class="sr">Watched lecture ${esc(l.n)}</span>`, "solo")}</td>
        <th scope="row" data-label="Lecture">${l.links.map((k) => `<a href="${esc(k.url)}" target="_blank" rel="noopener">L${esc(k.label.replace("Lecture ", ""))}</a>`).join("–")}</th>
        <td data-label="Topic">${esc(l.topic)}</td>
        <td data-label="Why it shows up in interviews">${rich(l.why)}</td>
        <td data-label="Paper(s) it unlocks">${esc(l.papers)}</td>
        <td data-label="Assignment">${esc(l.assignment)}</td>
      </tr>`).join("");
    const assigns = ph.assignments.map((a) => `
      <li>${check("p0." + a.id, `<a href="${esc(a.url)}" target="_blank" rel="noopener">${esc(a.label)}</a>`)} ${tag(a.tag)}</li>`).join("");
    return section(ph.id, phaseHead(ph), ph.weeks, `
      ${paras(ph.intro)}
      ${playlistHTML(ph.playlist)}
      <div class="table-wrap"><table class="grid stack lectures">
        <thead><tr><th class="c-tick"><span class="sr">Watched</span></th><th>Lecture</th><th>Topic</th><th>Why it shows up in interviews</th><th>Paper(s) in Phase 3 it unlocks</th><th>Assignment</th></tr></thead>
        <tbody>${rows}</tbody></table></div>
      <h3 class="sub-h">Assignments</h3>
      <ul class="checklist inline">${assigns}</ul>
      ${paras(ph.after)}${sources(ph.sources)}`);
  }

  function p1HTML(ph) {
    const rows = ph.rows.map((r) => `
      <tr>
        <th scope="row" data-label="Area">${esc(r.area)}</th>
        <td data-label="Derive by hand"><div class="cell-check">${check(`p1.${r.id}.derive`, '<span class="sr">Derived</span>', "solo")}<span>${rich(r.derive)}</span></div></td>
        <td data-label="Confirm in code (HAND, under 20 lines)"><div class="cell-check">${r.code === "—" ? '<span class="tick-spacer"></span>' : check(`p1.${r.id}.code`, '<span class="sr">Confirmed in code</span>', "solo")}<span>${rich(r.code)}</span></div></td>
        <td data-label="Used in paper">${esc(r.paper)}</td>
      </tr>`).join("");
    return section(ph.id, phaseHead(ph), ph.weeks, `
      ${paras(ph.intro)}
      <div class="table-wrap"><table class="grid stack">
        <thead><tr><th>Area</th><th>Derive by hand</th><th>Confirm in code (HAND, under 20 lines)</th><th>Used in paper</th></tr></thead>
        <tbody>${rows}</tbody></table></div>
      ${paras(ph.after)}${sources(ph.sources)}`);
  }

  function streakHTML(d) {
    const n = streakOf(d.id), last = S.streaks[d.id] && S.streaks[d.id].last;
    return `<div class="streak" data-drill="${d.id}">
      <span class="pips" aria-label="${n} of 3 runs under target in a row">${[0, 1, 2].map((i) => `<i class="${i < n ? "on" : ""}"></i>`).join("")}</span>
      <button type="button" class="mini" data-streak="hit">Under target</button>
      <button type="button" class="mini quiet" data-streak="miss">Missed</button>
      <span class="last">${last ? (daysSince(last) === 0 ? "today" : daysSince(last) + "d ago") : ""}</span>
    </div>`;
  }
  function p2HTML(ph) {
    const rows = ph.drills.map((d) => `
      <tr data-row="${d.id}">
        <td class="c-num" data-label="Row">${d.row}</td>
        <th scope="row" data-label="Implementation">${rich(d.name)}</th>
        <td class="c-time" data-label="Time target">${esc(d.target)}</td>
        <td data-label="Must get right">${rich(d.must)}</td>
        <td data-label="Drilled in">${esc(d.where)}</td>
        <td data-label="Streak">${streakHTML(d)}</td>
      </tr>`).join("");
    return section(ph.id, phaseHead(ph), ph.weeks, `
      ${paras(ph.intro)}
      <p class="hint">Log each timed attempt: <b>Under target</b> adds to the streak, <b>Missed</b> resets it. Three in a row clears the row.</p>
      <div class="table-wrap"><table class="grid stack drills">
        <thead><tr><th class="c-num">#</th><th>Implementation</th><th>Time target</th><th>Must get right</th><th>Drilled in</th><th>Streak</th></tr></thead>
        <tbody>${rows}</tbody></table></div>
      ${paras(ph.after)}
      ${playlistHTML(ph.playlist)}
      ${sources(ph.sources)}`);
  }

  function paperHTML(p) {
    const s = S.papers[p.n];
    const links = [
      ...p.paper.map((l) => `<li class="pdf">${extLink(l)}</li>`),
      ...p.resources.map((l) => `<li class="res">${extLink(l)}</li>`),
    ].join("");
    const stages = STAGES.map((st) => `
      <label class="stage ${st.key}" title="${st.hint}">
        <input type="checkbox" data-stage="${st.key}" ${s[st.key] ? "checked" : ""}><span>${st.label}</span>
      </label>`).join("");
    const exps = p.experiments.map((x, i) => `
      <li class="exp ${s.experiments[i] ? "done" : ""}">
        <input type="checkbox" id="e${p.n}-${i}" data-exp="${i}" ${s.experiments[i] ? "checked" : ""} aria-label="Experiment ${i + 1} done">
        <div><label for="e${p.n}-${i}">${tag(x.tag)}</label><p class="exp-body">${rich(x.body)}</p></div>
      </li>`).join("");
    const videos = p.videos.map((v) => `
      <figure class="player">
        <div class="frame" data-yt="${esc(v.id)}" data-title="${esc(v.title)}"></div>
        <figcaption>${esc(v.title)} <a href="${ytWatch(v.id)}" target="_blank" rel="noopener">Watch on YouTube</a></figcaption>
      </figure>`).join("");
    return `
    <article class="paper" id="paper-${p.n}" data-n="${p.n}" data-status="${paperStatus(s)}">
      <div class="paper-head">
        <div class="paper-num" aria-hidden="true">${p.n}</div>
        <div class="paper-id">
          <h4 class="paper-title">${esc(p.short)} <span class="yr">(${esc(p.year)})</span></h4>
          ${p.title !== p.short ? `<p class="paper-full">${esc(p.title)}</p>` : ""}
          <ul class="paper-links">${links}</ul>
        </div>
        <fieldset class="stages"><legend class="sr">Progress on ${esc(p.short)}</legend>${stages}</fieldset>
        <button type="button" class="linkish toggle" aria-expanded="false" aria-controls="body-${p.n}">Open study plan and videos</button>
      </div>
      <div class="paper-body" id="body-${p.n}" hidden>
        <div class="videos">${videos}</div>
        <div class="paper-cols">
          <div>
            <h5>Study approach</h5>
            <p class="prose">${rich(p.approach)}</p>
            ${p.hooks ? `<h5>Interview hooks</h5><p class="prose hook">${rich(p.hooks)}</p>` : ""}
          </div>
          <div>
            <h5>Break-it experiments</h5>
            <ol class="exps">${exps}</ol>
            ${p.note ? `<p class="note">${rich(p.note)}</p>` : ""}
          </div>
        </div>
        <div class="journal">
          <label class="j-notes">Notes
            <textarea data-field="notes" placeholder="Three questions you can't answer yet, derivation snags, what broke and why…">${esc(s.notes)}</textarea>
          </label>
          <label>Started<input type="date" data-field="started" value="${esc(s.started)}"></label>
          <label>Finished<input type="date" data-field="finished" value="${esc(s.finished)}"></label>
        </div>
      </div>
    </article>`;
  }

  function p3HTML(ph) {
    const mods = R.modules.map((m) => `
      <div class="module" data-module="${m.id}">
        <h3 class="module-head">Module ${m.id} — ${esc(m.title)} <span>(papers ${R.papers.filter((p) => p.module === m.id).map((p) => p.n).join(", ")})</span></h3>
        ${R.papers.filter((p) => p.module === m.id).map(paperHTML).join("")}
      </div>`).join("");
    return section(ph.id, phaseHead(ph), ph.weeks, `
      ${paras(ph.intro)}
      <div class="toolbar" role="search">
        <div class="filters" role="group" aria-label="Show papers by status">
          <button type="button" class="chip" data-filter="all" aria-pressed="true">All</button>
          <button type="button" class="chip" data-filter="todo" aria-pressed="false">Not started</button>
          <button type="button" class="chip" data-filter="doing" aria-pressed="false">In progress</button>
          <button type="button" class="chip" data-filter="done" aria-pressed="false">Done</button>
        </div>
        <label class="search"><span class="sr">Search papers</span><input type="search" id="search" placeholder="Search papers, ideas, code…"></label>
      </div>
      <div id="papers">${mods}<p class="empty" id="empty" hidden>No papers match. Clear the search or pick another filter.</p></div>
      ${paras(ph.after)}${sources(ph.sources)}`);
  }

  function p4HTML(ph) {
    const cards = ph.clusters.map((c) => `
      <article class="cluster">
        <h3>${check("p4." + c.id, esc(c.name), "head-tick")}</h3>
        <dl>
          <dt>Read</dt><dd>${rich(c.read)}</dd>
          <dt>Must master</dt><dd>${rich(c.master)}</dd>
          <dt>HAND implementation</dt><dd>${rich(c.hand)}</dd>
          <dt>Known interview question</dt><dd class="q">${rich(c.question)}</dd>
        </dl>
      </article>`).join("");
    return section(ph.id, phaseHead(ph), ph.weeks, `${paras(ph.intro)}<div class="clusters">${cards}</div>${paras(ph.after)}${sources(ph.sources)}`);
  }

  function p5HTML(ph) {
    const lists = ph.lists.map((l) => {
      const v = Math.min(+S.counts[l.id] || 0, l.total);
      return `<div class="counter">
        <a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)}</a>
        <label><span class="sr">Problems solved in ${esc(l.label)}</span>
          <input type="number" min="0" max="${l.total}" step="1" value="${v}" data-count="${l.id}"> / ${l.total}</label>
        <span class="meter"><i style="width:${(v / l.total) * 100}%"></i></span>
      </div>`;
    }).join("");
    const rows = ph.topics.map((t) => `
      <tr>
        <td class="c-tick" data-label="Fluent">${check("p5." + t.id, `<span class="sr">Fluent in ${esc(t.topic)}</span>`, "solo")}</td>
        <th scope="row" data-label="Topic">${esc(t.topic)}</th>
        <td data-label="Reach fluency in">${esc(t.reach)}</td>
        <td data-label="ML tie-in">${esc(t.tie)}</td>
      </tr>`).join("");
    return section(ph.id, phaseHead(ph), ph.weeks, `
      ${paras(ph.intro)}
      <div class="counters">${lists}</div>
      <div class="table-wrap"><table class="grid stack">
        <thead><tr><th class="c-tick"><span class="sr">Fluent</span></th><th>Topic</th><th>Reach fluency in</th><th>ML tie-in</th></tr></thead>
        <tbody>${rows}</tbody></table></div>
      ${paras(ph.after)}${sources(ph.sources)}`);
  }

  function p6HTML(ph) {
    return section(ph.id, phaseHead(ph), ph.weeks, `
      ${paras(ph.intro)}
      <ol class="checklist">${ph.portfolio.map((x) => `<li>${check("p6." + x.id, rich(x.text))}</li>`).join("")}</ol>
      ${paras([ph.afterPortfolio])}
      <div class="prep">${ph.prep.map((x) => `
        <div class="prep-item">${check("p6." + x.id, `<strong>${esc(x.title)}.</strong>`, "head-tick")}<p class="prose">${rich(x.text)}</p></div>`).join("")}</div>
      ${sources(ph.sources)}`);
  }

  function p7HTML(ph) {
    const groups = ph.groups.map((g) => {
      const tagName = g.ordered ? "ol" : "ul";
      return `<h3 class="sub-h">${esc(g.title)}</h3>
        <${tagName} class="checklist">${g.items.map((i) => `<li>${check("p7." + i.id, rich(i.text))}</li>`).join("")}</${tagName}>`;
    }).join("");
    return section(ph.id, phaseHead(ph), ph.weeks, `${paras(ph.intro)}${groups}${paras(ph.after)}${sources(ph.sources)}`);
  }

  function timelineHTML() {
    const T = R.timeline;
    const lanes = T.lanes.map((ln, li) => `
      <div class="tl-lane-name" style="grid-row:${li + 2}">${esc(ln.name)}</div>
      ${ln.bands.map((b, bi) => `<div class="tl-band ${ln.key ? "spine" : ""} ${ln.muted ? "muted" : ""}" data-lane="${li}" data-band="${bi}"
         style="grid-row:${li + 2};grid-column:${b.from + 1} / ${b.to + 2}" title="Weeks ${b.from}–${b.to}"><i class="fill"></i><span>${esc(b.label)}</span></div>`).join("")}`).join("");
    const weeks = Array.from({ length: T.weeks }, (_, i) => i + 1)
      .map((w) => `<div class="tl-wk" style="grid-column:${w + 1}">${w === 1 || (w - 1) % 4 === 0 ? "Wk " + w : ""}</div>`).join("");
    const gates = T.gates.map((g) => `
      <button type="button" class="gate" data-gate="${g.id}" aria-pressed="${chk("gate." + g.id)}" style="grid-column:${g.week + 1}">
        <i aria-hidden="true"></i><span>${esc(g.label)}</span><small>wk ${g.week}</small>
      </button>`).join("");
    return `
      <div class="tl">
        <h3>${esc(T.title)}</h3>
        <p class="tl-cap">${esc(T.caption)}. Click a diamond when you pass the gate.</p>
        <div class="tl-scroll"><div class="tl-grid" style="--weeks:${T.weeks};--lanes:${T.lanes.length}">
          <div class="tl-corner"></div>${weeks}${lanes}
          <div class="tl-now" id="tl-now" hidden></div>
          <div class="tl-gates">${gates}</div>
        </div></div>
        <p class="prose">${rich(T.after)}</p>
      </div>`;
  }

  function executionHTML() {
    const E = R.execution;
    return section("execution", "Execution: the weekly loop and the 26-week timeline", "", `
      ${paras([E.intro])}
      <ol class="loop-steps">${E.steps.map((s) => `
        <li><p class="loop-day">${esc(s.day)}</p><h3>${esc(s.title)} ${tag(s.tag)}</h3><p>${rich(s.body)}</p></li>`).join("")}</ol>
      <div class="start">
        <label>Week 1 started on <input type="date" id="start-date" value="${esc(S.startDate)}"></label>
        <span id="week-label"></span>
      </div>
      ${timelineHTML()}
      ${sources(E.sources)}`);
  }

  function resourcesHTML() {
    const X = R.resources;
    return section("resources", "Master resource index", "", `
      <p class="prose">${rich(X.intro)}</p>
      <div class="table-wrap"><table class="grid stack">
        <thead><tr><th>Resource</th><th>Use it for</th><th>Phase</th></tr></thead>
        <tbody>${X.rows.map((r) => `<tr><th scope="row" data-label="Resource">${r.links.map(extLink).join(" · ")}</th><td data-label="Use it for">${rich(r.use)}</td><td data-label="Phase">${esc(r.phase)}</td></tr>`).join("")}</tbody>
      </table></div>`);
  }

  function syncHTML() {
    return section("sync", "Saving your progress", "", `
      <p class="prose">Ticks, streaks and notes save in this browser straight away. To keep them in the repo (and see them on any device), download <code>progress.json</code> and commit it to <code>docs/data/</code>.</p>
      <p class="sync-state" id="sync-state"></p>
      <div class="sync-actions">
        <button type="button" class="btn" id="export">Download progress.json</button>
        <label class="btn btn-quiet">Load a progress file<input type="file" id="import" accept="application/json" hidden></label>
        <button type="button" class="btn btn-quiet" id="reset">Discard local changes</button>
      </div>`);
  }

  // ---------------------------------------------------------------- render + wire
  const NAV = () => [
    { id: "overview", label: "Overview" },
    { id: "interviews", label: "Interviews" },
    ...R.phases.map((p) => ({ id: p.id, label: `Phase ${p.num}`, sub: p.nav, phase: p.id })),
    { id: "execution", label: "Timeline" },
    { id: "resources", label: "Resources" },
    { id: "sync", label: "Save progress" },
  ];

  function render() {
    const P = Object.fromEntries(R.phases.map((p) => [p.id, p]));
    $("#byline").textContent = `${R.meta.date} · ${R.meta.author}`;
    const [t1, t2] = R.meta.title.split(" — ");
    $("#title").innerHTML = esc(t1) + (t2 ? `<span class="h1-sub">${esc(t2)}</span>` : "");
    $("#rail").innerHTML = NAV().map((n) => `
      <li><a href="#${n.id}" data-nav="${n.id}"><span class="r-label">${esc(n.label)}</span>${n.sub ? `<span class="r-sub">${esc(n.sub)}</span>` : ""}${n.phase ? `<span class="r-bar"><i data-bar="${n.phase}"></i></span>` : ""}</a></li>`).join("");
    $("#content").innerHTML = [
      overviewHTML(), interviewsHTML(),
      p0HTML(P.p0), p1HTML(P.p1), p2HTML(P.p2), p3HTML(P.p3), p4HTML(P.p4), p5HTML(P.p5), p6HTML(P.p6), p7HTML(P.p7),
      executionHTML(), resourcesHTML(), syncHTML(),
    ].join("");
    math($("#content"));
  }

  function setOpen(card, open) {
    const t = $(".toggle", card);
    t.setAttribute("aria-expanded", open);
    t.textContent = open ? "Close study plan" : "Open study plan and videos";
    $(".paper-body", card).hidden = !open;
    if (open) $$(".frame[data-yt]:not(.loaded)", card).forEach((f) => {
      f.classList.add("loaded");
      f.innerHTML = `<iframe src="${ytEmbed(f.dataset.yt)}" title="${f.dataset.title} (YouTube)" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>`;
    });
  }
  function openPaper(n) {
    filter = "all"; query = "";
    const sb = $("#search"); if (sb) sb.value = "";
    $$(".chip").forEach((c) => c.setAttribute("aria-pressed", c.dataset.filter === "all"));
    applyFilter();
    const card = $("#paper-" + n);
    setOpen(card, true);
    card.scrollIntoView({ block: "start" });
    $(".toggle", card).focus({ preventScroll: true });
  }

  function applyFilter() {
    const q = query.trim().toLowerCase();
    let shown = 0;
    for (const p of R.papers) {
      const card = $("#paper-" + p.n);
      const hay = [p.short, p.title, p.year, p.approach, p.hooks, ...p.experiments.map((x) => x.body), ...p.videos.map((v) => v.title), ...p.resources.map((r) => r.label)].join(" ").toLowerCase();
      const ok = (filter === "all" || paperStatus(S.papers[p.n]) === filter) && (!q || hay.includes(q));
      card.hidden = !ok; if (ok) shown++;
    }
    $$("#papers .module").forEach((m) => (m.hidden = !$$(".paper", m).some((c) => !c.hidden)));
    $("#empty").hidden = shown > 0;
  }

  function stampStart(card, s) {
    if (!s.started) { s.started = today(); $('[data-field="started"]', card).value = s.started; }
  }

  function wire() {
    const C = $("#content");
    C.addEventListener("change", (e) => {
      const t = e.target;
      if (t.dataset.check) { S.checks[t.dataset.check] = t.checked; return save(); }
      if (t.dataset.count) { S.counts[t.dataset.count] = Math.max(0, Math.min(+t.max, Math.round(+t.value || 0))); t.value = S.counts[t.dataset.count]; return save(); }
      if (t.id === "start-date") { S.startDate = t.value; return save(); }
      if (t.id === "import") return importFile(t);
      const card = t.closest(".paper"); if (!card) return;
      const s = S.papers[card.dataset.n];
      if (t.dataset.stage) {
        s[t.dataset.stage] = t.checked;
        if (t.checked) stampStart(card, s);
        if (paperStatus(s) === "done" && !s.finished) { s.finished = today(); $('[data-field="finished"]', card).value = s.finished; }
      } else if (t.dataset.exp !== undefined) {
        s.experiments[+t.dataset.exp] = t.checked;
        t.closest(".exp").classList.toggle("done", t.checked);
        if (t.checked) stampStart(card, s);
      } else if (t.dataset.field) {
        s[t.dataset.field] = t.value;
      } else return;
      card.dataset.status = paperStatus(s);
      save();
    });
    C.addEventListener("input", (e) => {
      if (e.target.dataset.field === "notes") {
        S.papers[e.target.closest(".paper").dataset.n].notes = e.target.value;
        clearTimeout(C._t); C._t = setTimeout(save, 400);
      } else if (e.target.id === "search") { query = e.target.value; applyFilter(); }
    });
    C.addEventListener("click", (e) => {
      const t = e.target;
      const toggle = t.closest(".toggle");
      if (toggle) return setOpen(toggle.closest(".paper"), toggle.getAttribute("aria-expanded") !== "true");
      const cell = t.closest("[data-goto]");
      if (cell) { e.preventDefault(); return openPaper(cell.dataset.goto); }
      const chip = t.closest(".chip");
      if (chip) {
        filter = chip.dataset.filter;
        $$(".chip").forEach((x) => x.setAttribute("aria-pressed", x === chip));
        return applyFilter();
      }
      const sb = t.closest("[data-streak]");
      if (sb) {
        const wrap = sb.closest(".streak"), id = wrap.dataset.drill;
        const cur = streakOf(id);
        S.streaks[id] = { n: sb.dataset.streak === "hit" ? Math.min(3, cur + 1) : 0, last: today() };
        wrap.outerHTML = streakHTML(R.phases.find((p) => p.id === "p2").drills.find((d) => d.id === id));
        return save();
      }
      const gate = t.closest("[data-gate]");
      if (gate) {
        const k = "gate." + gate.dataset.gate;
        S.checks[k] = !chk(k);
        gate.setAttribute("aria-pressed", S.checks[k]);
        return save();
      }
      if (t.id === "export") return exportFile();
      if (t.id === "reset") {
        if (!confirm("Replace this browser's progress with the version committed to the repo?")) return;
        try { localStorage.removeItem(STORE); } catch (_) {}
        S = normalise(baseline); return rerender();
      }
    });
  }

  function exportFile() {
    const blob = new Blob([JSON.stringify({ updated: today(), ...serialise(S) }, null, 2) + "\n"], { type: "application/json" });
    const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(blob), download: "progress.json" });
    document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }
  async function importFile(input) {
    const f = input.files[0]; if (!f) return;
    try { S = normalise(JSON.parse(await f.text())); save(); rerender(); }
    catch (_) { alert("That file isn't a valid progress.json. Choose a file downloaded from this page."); }
    input.value = "";
  }
  function rerender() { render(); applyFilter(); refresh(); }

  // ---------------------------------------------------------------- live summary
  function refresh() {
    // bench + paper count
    let papersDone = 0;
    for (const p of R.papers) {
      const s = S.papers[p.n], cell = $(`.cell[data-goto="${p.n}"]`);
      STAGES.forEach((st) => $(".b-" + st.key, cell).classList.toggle("on", !!s[st.key]));
      cell.classList.remove("next");
      if (paperStatus(s) === "done") papersDone++;
    }
    const next = R.papers.find((p) => paperStatus(S.papers[p.n]) !== "done");
    if (next) $(`.cell[data-goto="${next.n}"]`).classList.add("next");

    // rail bars + overall
    let sumFrac = 0;
    for (const ph of R.phases) {
      const { done, total } = phaseProgress(ph.id), f = total ? done / total : 0;
      sumFrac += f;
      const bar = $(`[data-bar="${ph.id}"]`); if (bar) bar.style.width = `${f * 100}%`;
    }
    const overall = Math.round((sumFrac / R.phases.length) * 100);
    const wk = currentWeek();
    const gatesPassed = R.timeline.gates.filter((g) => chk("gate." + g.id)).length;
    const drillsClear = phaseProgress("p2").done;
    $("#status").innerHTML = `
      <div class="stat big"><b>${overall}%</b><span>of the plan</span></div>
      <div class="stat"><b>${papersDone}</b><span>of 21 papers</span></div>
      <div class="stat"><b>${drillsClear}</b><span>of 19 drills on target</span></div>
      <div class="stat"><b>${gatesPassed}</b><span>of 4 gates passed</span></div>
      <div class="stat"><b>${wk ? (wk > 26 ? "26+" : wk) : "–"}</b><span>${wk ? "current week" : "set a start date"}</span></div>`;

    // "now" card
    let nowTxt = "";
    if (next) {
      const s = S.papers[next.n];
      const step = !s.read ? "read it (Day 1)" : !s.derive ? "derive and watch (Day 2)" : "break it (Day 3)";
      nowTxt += `<p class="now-line">Next paper: <a href="#paper-${next.n}" data-goto="${next.n}">#${next.n} ${esc(next.short)}</a>, ${step}.</p>`;
    } else nowTxt += `<p class="now-line">All 21 papers done.</p>`;
    if (wk) {
      const T = R.timeline, active = [];
      T.lanes.forEach((ln) => ln.bands.forEach((b) => { if (wk >= b.from && wk <= b.to) active.push(b.label); }));
      const upcoming = T.gates.find((g) => !chk("gate." + g.id));
      nowTxt += `<p class="now-line">Week ${Math.min(wk, 26)} plan: ${active.map(esc).join("; ") || "past the 26 weeks"}.</p>`;
      if (upcoming) nowTxt += `<p class="now-line">Next gate: ${esc(upcoming.label)}, ${upcoming.week - wk >= 0 ? `due in ${upcoming.week - wk} week${upcoming.week - wk === 1 ? "" : "s"}` : `${wk - upcoming.week} week${wk - upcoming.week === 1 ? "" : "s"} overdue`}.</p>`;
    } else {
      nowTxt += `<p class="now-line muted">Set your start date in <a href="#execution">Timeline</a> to see which week you're in.</p>`;
    }
    $("#dash-now").innerHTML = nowTxt;

    // timeline fills + now line
    R.timeline.lanes.forEach((ln, li) => ln.bands.forEach((b, bi) => {
      let f = 0;
      if (b.modules) f = b.modules.reduce((a, m) => a + moduleFrac(m), 0) / b.modules.length;
      else if (b.assign) f = b.assign.filter((a) => chk("p0." + a)).length / b.assign.length;
      else if (b.phase) f = phaseProgress(b.phase).done / phaseProgress(b.phase).total;
      const el = $(`.tl-band[data-lane="${li}"][data-band="${bi}"] .fill`);
      if (el) el.style.width = `${f * 100}%`;
    }));
    const now = $("#tl-now");
    if (wk && wk >= 1 && wk <= 26) { now.hidden = false; now.style.gridColumn = `${wk + 1}`; now.setAttribute("aria-label", `You are in week ${wk}`); }
    else now.hidden = true;
    $("#week-label").textContent = wk ? (wk > 26 ? "You're past week 26." : `You're in week ${wk}.`) : "";

    // sync state
    const dirty = JSON.stringify(serialise(S)) !== JSON.stringify(serialise(normalise(baseline)));
    const st = $("#sync-state");
    st.classList.toggle("dirty", dirty);
    st.textContent = dirty
      ? "This browser has changes that aren't in the repo yet. Download progress.json and commit it."
      : "This browser matches the progress committed to the repo.";
  }

  // highlight current section in the rail
  function spy() {
    const links = Object.fromEntries($$("[data-nav]").map((a) => [a.dataset.nav, a]));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          Object.values(links).forEach((a) => a.removeAttribute("aria-current"));
          const a = links[en.target.id];
          if (a) { a.setAttribute("aria-current", "true"); a.scrollIntoView({ block: "nearest", inline: "nearest" }); }
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    $$(".sec").forEach((s) => io.observe(s));
  }

  async function init() {
    // window.__ROADMAP__ / __PROGRESS__ let a single-file preview embed the data.
    const [rm, pr] = await Promise.all([
      window.__ROADMAP__ || fetch("data/roadmap.json").then((r) => r.json()),
      window.__PROGRESS__ || fetch("data/progress.json", { cache: "no-store" }).then((r) => (r.ok ? r.json() : {})).catch(() => ({})),
    ]);
    R = rm; baseline = pr;
    let local = null;
    try { local = JSON.parse(localStorage.getItem(STORE) || "null"); } catch (_) {}
    S = normalise(local || baseline);
    render(); wire(); applyFilter(); refresh(); spy();
    const m = location.hash.match(/^#paper-(\d+)$/);
    if (m) openPaper(m[1]);
    else if (location.hash) { const el = $(location.hash); if (el) el.scrollIntoView(); }
  }

  init().catch((err) => {
    $("#content").innerHTML = `<p class="empty">The roadmap data didn't load (${esc(err.message)}). If you opened index.html straight from disk, serve the docs folder instead, for example with <code>python -m http.server -d docs</code>.</p>`;
    console.error(err);
  });
})();
