/* OpenCode Plugins — main boards page (loads after common.js) */
'use strict';

const BOARD_ORDER = ['new', 'debut', 'daily', 'daily_rate', 'weekly', 'weekly_rate',
                     'monthly', 'monthly_rate', 'total', 'daily_downloads', 'daily_dl_yday'];
const CUM_BOARD = 'cumulative';   // month-only pseudo board
const PAGE = 50;

// Language pages (/langs/<slug>) reuse this file in "lang mode":
// <body data-base="../" data-lang="python" data-lang-name="Python"> — day-view
// only, boards come from data/langs/<slug>.json instead of the day files.
const DB = document.body.dataset.base || '';
// Generated data payloads live behind the API blob store (Cloudflare Pages
// caps deployments at 20k files); page links keep the relative DB base.
// The gh-pages mirror keeps its own full data/ tree — fetch it relatively
// there (CORS would block api-site from *.github.io origins anyway).
const DATA = (['localhost', '127.0.0.1'].includes(location.hostname)
  || location.hostname.endsWith('.github.io')
  || location.hostname.endsWith('.zhuikan.com')
  || location.hostname.endsWith('.oplugin.com'))
  ? `${DB}data/` : 'https://api-openplugins.zhuikan.com/data/';
const LANG_PAGE = document.body.dataset.lang || '';
const LANG_NAME = document.body.dataset.langName || '';
const TAG_PAGE = document.body.dataset.tag || '';
const TAG_NAME = document.body.dataset.tagName || '';
const SUBPAGE = TAG_PAGE ? `tags/${TAG_PAGE}` : LANG_PAGE ? `langs/${LANG_PAGE}` : '';

const state = {
  board: 'daily',
  period: 'day',
  sel: null,
  minK: 1,
  maxK: 500,
  shown: PAGE,
  items: [],
  boardMeta: {},
  index: null,
  hero: null,      // cached { top1 } for hero chart + footer stats
};


/* ---------------- rendering ---------------- */
const ICONS = {
  star: 'M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z',
  fork: 'M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0ZM5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Zm6.75.75a.75.75 0 1 0-1.5.75.75.75 0 0 0 0-1.5.75.75 0 0 0 0 1.5Zm-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Z',
  eye: 'M8 2c1.981 0 3.671.992 4.933 2.078 1.27 1.091 2.187 2.345 2.637 3.023a1.62 1.62 0 0 1 0 1.798c-.45.678-1.367 1.932-2.637 3.023C11.671 13.008 9.981 14 8 14c-1.981 0-3.671-.992-4.933-2.078C1.797 10.83.88 9.576.43 8.898a1.62 1.62 0 0 1 0-1.798c.45-.677 1.367-1.931 2.637-3.022C4.329 2.992 6.019 2 8 2ZM1.679 7.932a.12.12 0 0 0 0 .136c.411.622 1.241 1.75 2.366 2.717C5.175 11.758 6.527 12.5 8 12.5c1.473 0 2.824-.742 3.955-1.715 1.125-.967 1.954-2.096 2.366-2.717a.12.12 0 0 0 0-.136c-.412-.621-1.241-1.75-2.366-2.717C10.825 4.242 9.473 3.5 8 3.5c-1.473 0-2.824.742-3.955 1.715C5.744 6.182 4.914 7.311 4.5 7.932ZM8 10a2 2 0 1 1 0-4 2 2 0 0 1 0 4Z',
  pr: 'M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z',
  issue: 'M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z',
  tag: 'M1 7.775V2.75C1 1.784 1.784 1 2.75 1h5.025c.464 0 .91.184 1.238.513l6.25 6.25a1.75 1.75 0 0 1 0 2.474l-5.026 5.026a1.75 1.75 0 0 1-2.474 0l-6.25-6.25A1.752 1.752 0 0 1 1 7.775Zm1.5 0c0 .066.026.13.073.177l6.25 6.25a.25.25 0 0 0 .354 0l5.025-5.025a.25.25 0 0 0 0-.354l-6.25-6.25a.25.25 0 0 0-.177-.073H2.75a.25.25 0 0 0-.25.25ZM6 5a1 1 0 1 1 0 2 1 1 0 0 1 0-2Z',
  ext: 'M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2Zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1Z',
};
function icon(n, cls = 'm-ico', s = 13) {
  return `<svg viewBox="0 0 16 16" width="${s}" height="${s}" class="${cls}" fill="currentColor" aria-hidden="true"><path d="${ICONS[n]}"/></svg>`;
}
function mItem(iconName, val, unitKey, aux = true) {
  if (val == null) return '';
  const unit = t('units.' + unitKey);
  return `<span class="m${aux ? ' m-aux' : ''}" title="${unit} ${fmtFull(val)}">${icon(iconName)} ${fmt(val)}</span>`;
}

function langDot(lang) {
  if (!lang) return '';
  const c = LANG_COLORS[lang] || '#8b949e';
  const inner = `<span class="lang-dot" style="background:${c}"></span>${esc(lang)}`;
  const slug = state.langSlugs && state.langSlugs[lang];
  // link to the language's static page when one exists (index.json "langs")
  return slug
    ? `<a class="lang-tag" href="${DB}langs/${slug}">${inner}</a>`
    : `<span class="lang-tag">${inner}</span>`;
}

function badges(e) {
  let s = '';
  if (e.approx) s += `<span class="badge-approx" title="${t('badge.approx')}">≈</span>`;
  if (e.stale) s += `<span class="badge-stale" title="${t('badge.stale')}">⧗</span>`;
  return s;
}

function rowSideHTML(e) {
  if (e.growth != null) {
    const r = e.rate != null ? `<span class="rate-pill${e.rate >= 100 ? ' hot' : ''}">${fmtPct(e.rate)}</span>` : '';
    return `<div class="row-growth"><span class="up-tri">▲</span>+${fmt(e.growth)}</div>${r}`;
  }
  return `<div class="row-stars-big">${icon('star', 'm-ico', 14)} ${fmtFull(e.stars)}</div>`;
}

function nameLinkHTML(e) {
  const fn = esc(e.full_name);
  return `<a class="row-link" href="${DB}repos/${encodeURIComponent(e.owner)}__${encodeURIComponent(e.name)}" title="${esc(t('open.detail', { r: e.full_name }))}">`
    + `<span class="row-owner">${esc(e.owner)}</span><span class="row-sep">/</span>`
    + `<span class="row-repo">${esc(e.name)}</span></a>`
    + `<a class="ext-link" href="https://github.com/${fn}" target="_blank" rel="noopener" title="${esc(t('open.gh', { r: e.full_name }))}">${icon('ext', 'ext-ico', 12)}</a>`;
}

function tagPillsHTML(e) {
  const tp = e.tag_pages || [];
  const pills = (e.topics || []).slice(0, 4).map(t => {
    const sl = String(t).toLowerCase();
    const internal = tp.includes(sl);
    const href = internal ? `${DB}tags/${encodeURIComponent(sl)}`
                          : `https://www.npmjs.com/search?q=${encodeURIComponent(t)}`;
    return `<a class="row-tag" href="${href}"${internal ? '' : ' target="_blank" rel="noopener"'}>${esc(t)}</a>`;
  }).join('');
  return pills ? `<div class="row-tags">${pills}</div>` : '';
}

function rowHTML(e, dispRank = e.rank) {
  // state.sel 为 YYYY-MM 时用月末近似日，避免 Invalid Date → NaN 天
  const selEnd = state.sel && state.sel.length > 7 ? state.sel : `${state.sel}-28`;
  const ageDays = Math.floor((new Date(selEnd + 'T00:00:00') - new Date(e.created_at)) / 86400000);
  const ageChip = state.board === 'new' && e.created_at && Number.isFinite(ageDays) && ageDays >= 0
    ? `<span class="row-age">${t('age', { n: ageDays })}</span>`
    : '';
  return `<div class="rank-row" data-fn="${esc(e.full_name)}" style="animation-delay:${Math.min(dispRank * 12, 400)}ms">
    <span class="row-rank${dispRank <= 3 ? ' top' : ''}"${dispRank !== e.rank ? ` title="${esc(t('rank.prerank', { n: e.rank }))}"` : ''}>${dispRank}</span>
    <a class="row-avatar" href="${DB}repos/${encodeURIComponent(e.owner)}__${encodeURIComponent(e.name)}"><img src="${esc(e.avatar || `https://github.com/${e.owner}.png?size=96`)}" alt="" loading="lazy" width="48" height="48" onerror="this.outerHTML='<i class=\\'av-fb\\'>${esc((e.name || '?')[0].toUpperCase())}</i>'"></a>
    <div class="row-body">
      <div class="row-name">
        ${nameLinkHTML(e)}${badges(e)}${ageChip}
      </div>
      <div class="row-meta">
        ${langDot(e.language)}
        <span class="m m-stars" title="${t('units.stars')} ${fmtFull(e.stars)}">${icon('star')} ${fmt(e.stars)}</span>
        ${mItem('dl', e.downloads30d, 'downloads30d', false)}
        ${mItem('dl', e.downloads_month, 'downloads_month')}
        ${mItem('pr', e.prs, 'prs')}
        ${mItem('issue', e.issues, 'issues')}
        ${mItem('tag', e.releases, 'releases')}
      </div>
      ${e.description ? `<div class="row-desc">${esc(e.description)}</div>` : ''}
      <div class="row-foot"><div class="row-soc"></div>${tagPillsHTML(e)}</div>
    </div>
    <div class="row-side">
      ${e.series && e.series.length > 1 ? `<div class="row-spark">${sparkline(e.series)}</div>` : ''}
      ${rowSideHTML(e)}
    </div>
  </div>`;
}

function podiumHTML(e, idx) {
  const medal = ['🥇', '🥈', '🥉'][idx];
  const metric = e.growth != null ? `+${fmt(e.growth)}` : fmtFull(e.stars);
  const unit = e.growth != null ? 'stars' : '';
  const rate = e.rate != null ? `<span class="rate-pill${e.rate >= 100 ? ' hot' : ''}">${fmtPct(e.rate)}</span>` : '';
  return `<div class="podium-card p${idx + 1}" data-fn="${esc(e.full_name)}">
    <div class="podium-rank">${medal}</div>
    <a class="podium-avatar" href="${DB}repos/${encodeURIComponent(e.owner)}__${encodeURIComponent(e.name)}"><img src="${esc(e.avatar || `https://github.com/${e.owner}.png?size=128`)}" alt="" loading="lazy" onerror="this.outerHTML='<i class=\\'av-fb\\'>${esc((e.name || '?')[0].toUpperCase())}</i>'"></a>
    <div class="podium-name">${nameLinkHTML(e)}${badges(e)}</div>
    <div class="podium-desc">${esc(e.description || '—')}</div>
    <div class="podium-metric" style="color:${e.growth != null ? 'var(--green)' : 'var(--text)'}">${metric}${unit ? ` <span class="unit">${unit}</span>` : ''}</div>
    <div class="podium-sub">${langDot(e.language)}<span>★ ${fmtFull(e.stars)}</span>${rate}</div>
    ${e.series && e.series.length > 1 ? `<div class="podium-spark">${sparkline(e.series)}</div>` : ''}
    <div class="row-foot"><div class="row-soc"></div>${tagPillsHTML(e)}</div>
  </div>`;
}

function windowLabel() {
  const b = state.boardMeta;
  if (state.board === 'new') return t('window.new');
  if (state.board === 'debut') return t('window.debut');
  if (state.board === 'total' || state.board === CUM_BOARD || state.board === 'year_growth') {
    if (b.window_start && b.window_days != null)
      return t('window.range', { s: b.window_start, e: state.sel, d: b.window_days });
    return '';
  }
  if (b.window_start && b.window_days != null) {
    const approx = b.window_days < ({ daily: 1, weekly: 7, monthly: 30,
      daily_downloads: 1, daily_dl_yday: 1 }[state.board.replace('_rate', '')] || 0);
    return t('window.range', { s: b.window_start, e: state.sel, d: b.window_days }) + (approx ? t('window.approx') : '');
  }
  return '';
}

function renderList() {
  const items = state.items;
  const podium = items.slice(0, 3);
  const rest = items.slice(3, state.shown);
  $('#podiumWrap').innerHTML = podium.length >= 3 ? `<div class="podium">${podium.map(podiumHTML).join('')}</div>` : '';
  $('#listWrap').innerHTML = rest.length
    ? `<div class="rank-list">${rest.map((e, i) => rowHTML(e, i + 4)).join('')}</div>`
      + (items.length > state.shown
        ? `<div class="load-more-wrap"><button class="load-more" id="loadMore">${t('load.more', { n: items.length - state.shown })}</button></div>`
        : '')
    : '';
  const lb = $('#loadMore');
  if (lb) lb.onclick = () => { state.shown += PAGE; renderList(); };
  hydrateSocial();
}

/* ---- social strip per row: one batched API call for all visible items ---- */
async function hydrateSocial() {
  const els = [...document.querySelectorAll('#podiumWrap [data-fn], #listWrap [data-fn]')]
    .filter(el => el.querySelector('.row-soc') && !el.querySelector('.row-soc').dataset.done);
  if (!els.length || typeof api !== 'function') return;
  const ids = [...new Set(els.map(el => el.dataset.fn))].slice(0, 60);
  let soc;
  try {
    soc = (await api(`/social/batch?site=oplugins&ids=${encodeURIComponent(ids.join(','))}`)).items || {};
  } catch { return; }   /* API down → rows just stay clean */
  els.forEach(el => {
    const s = soc[el.dataset.fn];
    const mount = el.querySelector('.row-soc');
    if (!s || mount.dataset.done) return;
    mount.dataset.done = '1';
    const sv = s.viewer || {};
    const [o, n] = el.dataset.fn.split('/');
    const url = `${DB}repos/${encodeURIComponent(o)}__${encodeURIComponent(n)}`;
    mount.innerHTML = `<button class="soc-ic${sv.liked ? ' on' : ''}" data-act="likes" type="button" title="${esc(t('soc.like'))}">♥ <b>${fmt(s.likes)}</b></button>
      <button class="soc-ic${sv.faved ? ' on' : ''}" data-act="favorites" type="button" title="${esc(t('soc.fav'))}">★ <b>${fmt(s.favs)}</b></button>
      <a class="soc-ic" href="${url}#rpCm" title="${esc(t('cm.title'))}">💬 <b>${fmt(s.comments)}</b></a>`;
    mount.querySelectorAll('button.soc-ic').forEach(btn => {
      btn.onclick = async () => {
        if (!zk.user) { openAuthModal('login'); return; }
        btn.disabled = true;
        try {
          const r = await api(`/${btn.dataset.act}/toggle`, {
            method: 'POST',
            body: JSON.stringify({ site: 'oplugins', item_id: el.dataset.fn })
          });
          const on = r.liked ?? r.faved;
          btn.classList.toggle('on', !!on);
          const bb = btn.querySelector('b');
          bb.textContent = fmt(Math.max(0, (parseInt(bb.textContent.replace(/\D/g, '')) || 0) + (on ? 1 : -1)));
        } catch (e) {
          if (e.code === 'unverified_email') openAuthModal('verify');
        }
        btn.disabled = false;
      };
    });
  });
}
document.addEventListener('zk:auth', () => {
  document.querySelectorAll('.row-soc').forEach(e => { e.innerHTML = ''; delete e.dataset.done; });
  hydrateSocial();
});

function setEmpty(msg, pct, opts = {}) {
  $('#emptyState').hidden = false;
  $('#podiumWrap').innerHTML = '';
  $('#listWrap').innerHTML = '';
  $('#monthDetail').hidden = true;
  $('#emptyText').textContent = msg || t('empty.nodata');
  const h2 = $('#emptyState h2');
  if (h2) h2.textContent = opts.title || t('empty.title');
  const prog = $('#emptyState .progress');
  if (prog) prog.style.display = pct != null ? '' : 'none';
  $('#progressBar').style.width = `${Math.min(100, pct || 0)}%`;
  $('#progressHint').textContent = pct != null ? t('progress.hint', { p: Math.round(pct) }) : '';

  const acts = opts.actions || [];
  $('#emptyActions').innerHTML = acts.length
    ? acts.map((a, i) => `<button class="empty-btn" data-act="${i}">${esc(a.label)}</button>`).join('')
    : '';
  $('#emptyActions').querySelectorAll('.empty-btn').forEach((b, i) => {
    b.onclick = () => acts[i].run();
  });

  const pv = opts.preview;
  const rows = pv && pv.items.length ? pv.items : [];
  $('#emptyState').classList.toggle('has-preview', rows.length > 0);
  $('#emptyPreview').innerHTML = rows.length
    ? `<div class="empty-preview-title">${esc(t('preview.top', { t: pv.title, n: rows.length }))}</div>`
      + rows.map(e => `<a class="preview-row" href="${DB}repos/${encodeURIComponent(e.owner)}__${encodeURIComponent(e.name)}">
          <span class="preview-rank">${e.rank}</span>
          <span class="preview-name"><span class="row-owner">${esc(e.owner)}</span>/${esc(e.name)}</span>
          <span class="preview-stars">★ ${fmt(e.stars)}</span>
        </a>`).join('')
    : '';
}

function clearEmpty() {
  $('#emptyState').hidden = true;
  $('#emptyState').classList.remove('has-preview');
  $('#emptyActions').innerHTML = '';
  $('#emptyPreview').innerHTML = '';
}

/* ---------------- data loading ---------------- */
function boardLabel(k) { return t('board.' + k); }

function buildEmptyCtx(boards, period) {
  const order = period === 'month'
    ? ['new', 'total', CUM_BOARD]
    : ['new', 'total', 'daily', 'weekly', 'monthly'];
  const avail = order.filter(k => boards[k] && boards[k].items && boards[k].items.length);
  const actions = avail.slice(0, 2).map(k => ({
    label: t('empty.view', { b: boardLabel(k) }),
    run: () => { state.board = k; state.shown = PAGE; syncURL(); renderAll(); },
  }));
  const first = avail[0];
  const preview = first
    ? { title: boardLabel(first), items: boards[first].items.slice(0, 8) }
    : null;
  return { actions, preview };
}

function resetFilter() {
  state.minK = 1; state.maxK = 500; state.shown = PAGE;
  $('#minK').value = 1; $('#maxK').value = 500;
  syncURL(); loadView();
}

async function loadView() {
  clearEmpty();
  $('#monthDetail').hidden = true;
  $('#yearWrap').hidden = true;
  state.items = [];
  state.boardMeta = {};
  $('#windowInfo').textContent = '';
  let emptyCtx = {};
  let rawCount = 0;

  const idx = state.index;
  let data;
  try {
    data = SUBPAGE ? await j(`${DATA}${SUBPAGE}.json`)
      : await j(state.period === 'day' ? `${DATA}days/${state.sel}.json`
        : state.period === 'month' ? `${DATA}months/${state.sel}.json`
        : `${DATA}years/${state.sel}.json`);
  } catch {
    const pct = idx ? Math.min(100, idx.snapshot_days / 31 * 100) : 0;
    setEmpty(t('empty.acc'), pct);
    return;
  }
  if (SUBPAGE) {
    state.sel = data.date || state.sel;
    // a board can be absent per-language (e.g. debut is global-history only)
    if (!(data.boards || {})[state.board]) state.board = 'daily';
    const board = (data.boards || {})[state.board] || { items: [] };
    state.boardMeta = board;
    rawCount = (board.items || []).length;
    state.items = filterItems(board.items || []);
    if (!state.items.length) emptyCtx = buildEmptyCtx(data.boards || {}, 'day');
    document.title = TAG_PAGE ? t('title.tag', { g: TAG_NAME })
      : t('title.langboard',
        { l: LANG_NAME, b: boardLabel(state.board), s: state.sel });
  } else if (state.period === 'day') {
    const board = (data.boards || {})[state.board] || { items: [] };
    state.boardMeta = board;
    rawCount = (board.items || []).length;
    state.items = filterItems(board.items || []);
    if (!state.items.length) emptyCtx = buildEmptyCtx(data.boards || {}, 'day');
    document.title = t('title.board', { b: boardLabel(state.board), s: state.sel });
  } else if (state.period === 'month') {
    const src = state.board === CUM_BOARD ? data.cumulative : ((data.boards || {})[state.board] || { items: [] });
    state.boardMeta = src;
    rawCount = (src.items || []).length;
    state.items = filterItems(src.items || []);
    if (!state.items.length) {
      const all = { ...(data.boards || {}) };
      if (data.cumulative) all.cumulative = data.cumulative;
      emptyCtx = buildEmptyCtx(all, 'month');
    }
    // month extras
    if (data.daily_top10 && data.daily_top10.length) {
      $('#monthDetail').hidden = false;
      $('#monthTop10').innerHTML = data.daily_top10.map(day => `
        <div class="top10-day">
          <div class="top10-date">${day.date}</div>
          <div class="top10-items">${day.items.map(e =>
            `<span class="top10-chip"><a href="${DB}repos/${encodeURIComponent(e.owner)}__${encodeURIComponent(e.name)}"><span class="row-owner">${esc(e.owner)}</span>/${esc(e.name)}</a> <b>+${fmt(e.growth)}</b></span>`).join('')}
          </div>
        </div>`).join('');
    }
    document.title = t('title.board', {
      b: state.board === CUM_BOARD ? t('title.cum') : boardLabel(state.board), s: state.sel });
  } else { // year
    const growth = data.growth || { items: [] };
    state.boardMeta = growth;
    rawCount = (growth.items || []).length;
    state.items = filterItems(growth.items || []);
    if (!state.items.length && state.index.months && state.index.months.length) {
      emptyCtx = { actions: [{
        label: t('empty.viewmonth'),
        run: () => { state.period = 'month'; state.sel = state.index.months[state.index.months.length - 1]; state.board = 'daily'; state.shown = PAGE; syncURL(); renderAll(); },
      }], preview: null };
    }
    // months grid
    $('#yearWrap').hidden = false;
    $('#monthGrid').innerHTML = (data.months || []).map(m => {
      const [y, mo] = m.split('-');
      const mName = LANG === 'zh' ? t('month.name', { y, m: Number(mo) })
        : t('month.name', { y, m: MONTHS_EN[Number(mo) - 1] });
      const isPartial = m === (data.months || [])[data.months.length - 1] && data.partial;
      return `<div class="month-card${isPartial ? ' partial' : ''}" data-month="${m}">
        <div class="m-name">${mName}</div>
        <div class="m-sub">${isPartial ? t('month.partial') : t('month.full')}</div>
      </div>`;
    }).join('');
    document.querySelectorAll('.month-card').forEach(c => {
      c.onclick = () => { state.period = 'month'; state.sel = c.dataset.month; state.board = 'daily'; syncURL(); renderAll(); };
    });
    document.title = t('title.year', { s: state.sel });
  }

  $('#windowInfo').textContent = windowLabel();
  if (!state.items.length) {
    if (rawCount > 0) {
      setEmpty(t('empty.filter.text'), null, {
        title: t('empty.filter.title'),
        actions: [{ label: t('empty.reset'), run: resetFilter }],
      });
      return;
    }
    const pct = state.index ? Math.min(100, state.index.snapshot_days / 31 * 100) : 0;
    if (pct >= 100) setEmpty(t('empty.win'), null, { ...emptyCtx, title: t('empty.win.title') });
    else setEmpty(t('empty.acc'), pct, emptyCtx);
    return;
  }
  state.shown = PAGE;
  renderList();
}

function filterItems(items) {
  const lo = (state.minK || 0) * 1000;
  const hi = (state.maxK > 0 ? state.maxK : Infinity) * 1000;
  return items.filter(e => (e.stars ?? 0) >= lo && (e.stars ?? 0) <= hi).slice(0, 200);
}

/* ---------------- controls ---------------- */
function boardTabsForPeriod() {
  if (state.period === 'year') return [];           // year view is single-board
  const tabs = [...BOARD_ORDER];
  if (state.period === 'month') tabs.push(CUM_BOARD);
  // language pages have no debut board (it needs cross-day board history)
  if (TAG_PAGE) return [];   // tag pages carry a single star-sorted list
  return LANG_PAGE ? tabs.filter(b => b !== 'debut') : tabs;
}

function renderTabs() {
  const tabs = boardTabsForPeriod();
  $('#boardTabs').innerHTML = tabs.map(b => {
    const active = state.board === b ? ' active' : '';
    const href = b === CUM_BOARD ? `${DB}b/monthly` : `${DB}b/${b}`;
    return `<a class="tab-btn${active}" data-board="${b}" href="${href}">${boardLabel(b)}</a>`;
  }).join('');
  $('#boardTabs').style.display = tabs.length ? 'flex' : 'none';
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.onclick = ev => {
      if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey || ev.button) return;
      ev.preventDefault();
      state.board = btn.dataset.board; state.shown = PAGE; syncURL(); renderAll();
    };
  });
}

function renderSelOptions() {
  const idx = state.index;
  const sel = $('#selDate');
  let opts = [];
  if (state.period === 'day') opts = idx.dates.map(x => [x, x]);
  else if (state.period === 'month') opts = idx.months.map(x => [x, x + (x === idx.months[idx.months.length - 1] ? t('sel.ongoing') : '')]);
  else opts = idx.years.map(x => [x, LANG === 'zh' ? x + ' 年' : x]);
  sel.innerHTML = opts.map(([v, tx]) => `<option value="${v}">${tx}</option>`).join('');
  sel.value = state.sel;
}

function validSel() {
  const idx = state.index;
  const list = state.period === 'day' ? idx.dates : state.period === 'month' ? idx.months : idx.years;
  return list.includes(state.sel) ? state.sel : list[list.length - 1];
}

function syncURL() {
  const p = new URLSearchParams();
  p.set('period', state.period);
  p.set('sel', state.sel);
  if (state.period !== 'year') p.set('board', state.board);
  p.set('min', state.minK); p.set('max', state.maxK);
  history.pushState(null, '', '?' + p.toString());
  /* SPA 切换不产生新页面加载——手动给百度统计补一条 pageview */
  if (typeof _hmt !== 'undefined') _hmt.push(['_trackPageview', location.pathname + location.search]);
}

function readURL() {
  const p = new URLSearchParams(location.search);
  state.period = ['day', 'month', 'year'].includes(p.get('period')) ? p.get('period') : 'day';
  state.sel = p.get('sel');
  // /b/<board>[/<date>] static pages carry their target in body data-attrs
  const bb = document.body.dataset.board, bs = document.body.dataset.sel;
  if (bb && BOARD_ORDER.includes(bb)) state.board = bb;
  if (bs) state.sel = bs;
  state.minK = Math.max(0, parseInt(p.get('min') || '1', 10) || 0);
  state.maxK = Math.max(0, parseInt(p.get('max') || '500', 10) || 0);
  const b = p.get('board');
  if (state.period === 'month' && b === CUM_BOARD) state.board = CUM_BOARD;
  else if (BOARD_ORDER.includes(b)) state.board = b;
  else state.board = 'daily';   // landing default = 日飙升榜
  $('#minK').value = state.minK; $('#maxK').value = state.maxK;
}

/* ---------------- hero + footer stats ---------------- */
async function loadHeroData() {
  const idx = state.index;
  if (!state.hero) {
    state.hero = { top1: null };
    try {
      const latest = await j(SUBPAGE
        ? `${DATA}${SUBPAGE}.json`
        : `${DATA}days/${idx.latest_day}.json`);
      const top1 = latest.boards?.daily?.items?.[0]
        || latest.boards?.new?.items?.[0]
        || latest.boards?.total?.items?.[0];
      if (top1) state.hero.top1 = top1;
    } catch { /* keep null */ }
  }
  renderHero();
  renderFootStats();
}

function renderHero() {
  const top1 = state.hero && state.hero.top1;
  const chart = $('#hvChart'), cap = $('#hvCap');
  if (top1 && top1.series && top1.series.length > 1) {
    chart.innerHTML = sparkline(top1.series, 620, 150, 6, 'sparkFill', 'sparkStroke');
    const g = top1.growth != null ? `+${fmtFull(top1.growth)}` : fmtFull(top1.stars);
    cap.innerHTML = `<a href="${DB}repos/${encodeURIComponent(top1.owner)}__${encodeURIComponent(top1.name)}">`
      + `<b>${esc(top1.full_name)}</b> ${g}</a>`
      + `<span class="hv-cap-sub">${t('hv.cap', { n: top1.series.length })}</span>`;
  } else {
    chart.innerHTML = `<svg class="hv-radar" viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <circle cx="24" cy="24" r="20" stroke="url(#sparkStroke)" stroke-width="1.5" opacity="0.4"/>
      <circle cx="24" cy="24" r="12" stroke="url(#sparkStroke)" stroke-width="1" opacity="0.3"/>
      <circle cx="24" cy="24" r="4" fill="url(#sparkStroke)"/>
      <g class="radar-sweep"><line x1="24" y1="24" x2="38" y2="10" stroke="#58a6ff" stroke-width="1.5" stroke-linecap="round"/></g>
    </svg>`;
    cap.textContent = '';
  }
}

function renderFootStats() {
  const idx = state.index;
  const top1 = state.hero && state.hero.top1;
  const g = top1 && top1.growth != null ? '+' + fmtFull(top1.growth) : '–';
  const fresh = idx && idx.generated_at ? ' · ' + t('fresh', { t: timeAgo(idx.generated_at) }) : '';
  $('#footStats').textContent = idx
    ? t('foot.stats', {
        r: fmtFull(idx.repo_count || 0),
        d: idx.snapshot_days || 0,
        s: (idx.first_day || '').slice(5) || '–',
        e: (idx.latest_day || '').slice(5) || '–',
        g }) + fresh
    : '';
}

/* ---------------- boot ---------------- */
async function renderAll() {
  state.sel = validSel();
  renderTabs();
  renderSelOptions();
  document.querySelectorAll('.seg-btn').forEach(b =>
    b.classList.toggle('active', b.dataset.period === state.period));
  await loadView();
}

/* ------------- header search — remote: api-openplugins.zhuikan.com/search ------- */
const search = { hits: [], active: -1, err: false };

function repoUrl(fn) { return `${DB}repos/${fn.replace('/', '__')}`; }

function mark(text, q) {
  const i = text.toLowerCase().indexOf(q);
  if (i < 0) return esc(text);
  return esc(text.slice(0, i)) + '<mark>' + esc(text.slice(i, i + q.length))
    + '</mark>' + esc(text.slice(i + q.length));
}

function searchRow(e, q, i) {
  const sub = e.description ? `<span class="sr-sub">${esc(e.description)}</span>` : '';
  return `<a class="sr-row${i === search.active ? ' on' : ''}" href="${esc(repoUrl(e.item_id))}">
    <img class="sr-av" src="https://github.com/${esc(e.owner)}.png?size=64" alt="" loading="lazy" width="30" height="30" onerror="this.outerHTML='<i class=\\'sr-av-fb av-fb\\'>${esc(((e.name || e.item_id || '?').split('/').pop())[0].toUpperCase())}</i>'">
    <span class="sr-main">
      <span class="sr-name">${mark(e.item_id, q)}</span>
      ${sub}
    </span>
    <span class="sr-side">${langDot(e.lang)}<span class="sr-stars">${icon('star', 'm-ico', 12)} ${fmt(e.stars)}</span></span>
  </a>`;
}

function renderSearchDrop(q, scope) {
  const drop = $('#searchDrop');
  if (!q || q.length < 2) { drop.hidden = true; return; }
  if (search.err) {
    drop.innerHTML = `<div class="sr-none">${esc(t('search.err'))}</div>`;
  } else if (!search.hits.length) {
    drop.innerHTML = `<div class="sr-none">${esc(t(`search.none.${scope}`))}</div>`;
  } else {
    drop.innerHTML = search.hits.slice(0, 12).map((h, i) => searchRow(h, q, i)).join('')
      + `<div class="sr-foot">${esc(t('search.count', { n: search.hits.length }))}</div>`;
  }
  drop.hidden = false;
}

let searchSeq = 0;
async function runSearch(q, scope) {
  if (!q || q.length < 2) { search.hits = []; return; }
  const seq = ++searchSeq;
  try {
    const d = await api(`/search?q=${encodeURIComponent(q)}&site=oplugins&type=${scope}&limit=15`);
    if (seq !== searchSeq) return;                  // stale response
    search.hits = (d.items || []).filter(h => h && h.item_id);
    search.err = false;
    search.active = search.hits.length ? 0 : -1;
  } catch {
    if (seq !== searchSeq) return;
    search.hits = []; search.err = true;
  }
}

function initSearch() {
  const wrap = $('#searchWrap'), input = $('#searchInput'),
    drop = $('#searchDrop'), scopeSel = $('#searchScope');
  if (!wrap || !input) return;

  const scope = () => (scopeSel && scopeSel.value) || 'repo';
  const doSearch = async () => {
    const q = input.value.trim().toLowerCase();
    await runSearch(q, scope());
    renderSearchDrop(q, scope());
  };

  let deb = null;
  input.addEventListener('input', () => {
    clearTimeout(deb);
    deb = setTimeout(doSearch, 200);
  });
  input.addEventListener('focus', () => {
    if (input.value.trim().length >= 2) drop.hidden = false;
  });
  if (scopeSel) scopeSel.addEventListener('change', () => {
    input.dataset.i18nPh = `search.ph.${scope()}`;   // lang switch picks it up
    input.dataset.i18nAria = input.dataset.i18nPh;
    input.placeholder = t(input.dataset.i18nPh);
    input.focus();
    if (input.value.trim().length >= 2) doSearch();
  });
  input.addEventListener('keydown', (e) => {
    const n = Math.min(search.hits.length, 12);
    if (e.key === 'ArrowDown' && n) {
      e.preventDefault();
      search.active = (search.active + 1) % n;
      renderSearchDrop(input.value.trim().toLowerCase(), scope());
    } else if (e.key === 'ArrowUp' && n) {
      e.preventDefault();
      search.active = (search.active - 1 + n) % n;
      renderSearchDrop(input.value.trim().toLowerCase(), scope());
    } else if (e.key === 'Enter' && search.active >= 0) {
      const h = search.hits[search.active];
      if (h) location.href = repoUrl(h.item_id);
    } else if (e.key === 'Escape') {
      drop.hidden = true;
      input.blur();
    }
  });
  document.addEventListener('click', (e) => {
    if (!wrap.contains(e.target)) drop.hidden = true;
  });
}

async function init() {
  document.documentElement.classList.add('m-enter');
  zkInit();
  initSearch();
  zkLoadUser().then(renderAuthChip);
  api('/stats/view', { method: 'POST', body: JSON.stringify({ site: 'oplugins', path: location.pathname }) })
    .catch(() => { });   /* fire-and-forget analytics */
  readURL();
  applyStaticI18n();
  try {
    state.index = await j(`${DATA}index.json`);
  } catch (e) {
    setEmpty(t('empty.init'), 0);
    return;
  }
  state.langSlugs = Object.fromEntries(
    (state.index.langs || []).map(x => [x.lang, x.slug]));
  if (SUBPAGE) {
    // day-view only: hide period picker, date select and month/year sections
    state.period = 'day';
    document.querySelectorAll(
      '#periodSeg, #selDate, label[for="selDate"], #monthDetail, #yearWrap')
      .forEach(el => { el.hidden = true; });
    document.title = TAG_PAGE ? t('title.tag', { g: TAG_NAME })
      : t('title.lang', { l: LANG_NAME });
  }
  if (!state.sel) state.sel = state.index.latest_day;
  await renderAll();
  loadHeroData();   // fire and forget; renders hero chart + footer stats when done

  // events
  bindChrome(() => { renderHero(); renderFootStats(); renderAll(); });
  $('#selDate').onchange = (e) => { state.sel = e.target.value; syncURL(); loadView(); };
  document.querySelectorAll('.seg-btn').forEach(btn => {
    btn.onclick = () => {
      state.period = btn.dataset.period;
      state.sel = null;
      // keep the current board across period switches; only remap the
      // month-only cumulative board when leaving month view
      if (state.board === CUM_BOARD && state.period !== 'month') {
        state.board = 'monthly';
      }
      renderAll();
      syncURL();
    };
  });
  $('#applyFilter').onclick = () => {
    state.minK = Math.max(0, parseInt($('#minK').value || '0', 10) || 0);
    state.maxK = Math.max(0, parseInt($('#maxK').value || '0', 10) || 0);
    state.shown = PAGE;
    syncURL(); loadView();
  };
  window.addEventListener('popstate', () => { readURL(); renderAll(); });
}

init();
