'use strict';
/* User center — /user?tab=fav|likes|comments|settings.
   Private page: every list loads lazily via api-site with the session
   token; logged-out visitors get a sign-in prompt instead of a bounce. */

const UC_TABS = ['fav', 'likes', 'comments', 'settings'];
const uc = { tab: 'fav', editing: false };

function ucTabFromURL() {
  const tb = new URLSearchParams(location.search).get('tab');
  return UC_TABS.includes(tb) ? tb : 'fav';
}

function ucRepoHref(itemId) {          // 'owner/name' → repos/owner__name
  const i = (itemId || '').indexOf('/');
  if (i < 0) return null;
  return `repos/${encodeURIComponent(itemId.slice(0, i))}__${encodeURIComponent(itemId.slice(i + 1))}`;
}

function ucDate(ts) {
  if (!ts) return '';
  return new Date(ts * 1000).toLocaleDateString(LANG === 'zh' ? 'zh-CN' : 'en-US');
}

function ucErr(el, e) {
  if (!el) return;
  el.textContent = authErr(e);
  el.hidden = false;
}

/* ---------- tabs ---------- */

function ucNav() {
  return `<nav class="uc-side"><div class="uc-side-in">${UC_TABS.map(k =>
    `<a class="uc-tab${k === uc.tab ? ' on' : ''}" href="user?tab=${k}" data-tab="${k}">${esc(t('uc.tab.' + k))}</a>`
  ).join('')}</div></nav>`;
}

function render() {
  const page = $('#ucPage');
  if (!zk.user) {
    page.innerHTML = `<div class="uc-empty">
      <p>${esc(t('uc.login.need'))}</p>
      <button class="auth-item auth-go" id="ucLogin" type="button">${esc(t('uc.login.go'))}</button>
    </div>`;
    $('#ucLogin').onclick = () => openAuthModal('login');
    return;
  }
  page.innerHTML = `<div class="uc-wrap">${ucNav()}`
    + `<div class="uc-body" id="ucBody"><div class="uc-loading">${esc(t('loading'))}</div></div></div>`;
  page.querySelectorAll('.uc-tab').forEach(a => {
    a.onclick = (e) => {
      e.preventDefault();
      uc.tab = a.dataset.tab;
      history.replaceState(null, '', `user?tab=${uc.tab}`);
      render();
    };
  });
  UC_LOAD[uc.tab]($('#ucBody'));
}

/* ---------- favorites / likes (shared row shape) ---------- */

async function ucLoadItems(el, kind) {
  const ep = kind === 'fav' ? '/me/favorites?site=oplugins&limit=300'
                            : '/me/likes?site=oplugins&limit=300';
  let items;
  try { items = (await api(ep)).items || []; }
  catch (e) { el.innerHTML = `<div class="uc-empty">${esc(authErr(e))}</div>`; return; }
  if (!items.length) {
    el.innerHTML = `<div class="uc-empty">${esc(t('uc.empty.' + kind))}</div>`;
    return;
  }
  const toggleEp = kind === 'fav' ? '/favorites/toggle' : '/likes/toggle';
  const whenKey = kind === 'fav' ? 'uc.fav.when' : 'uc.like.when';
  const rmKey = kind === 'fav' ? 'uc.unfav' : 'uc.unlike';
  el.innerHTML = `<div class="uc-list">${items.map(f => {
    const href = ucRepoHref(f.item_id);
    return `<div class="uc-row" data-id="${esc(f.item_id)}">
      <div class="uc-main">
        ${href ? `<a class="uc-name" href="${href}">${esc(f.item_id)}</a>` : `<span class="uc-name">${esc(f.item_id)}</span>`}
        ${f.description ? `<div class="uc-desc">${esc(f.description)}</div>` : ''}
        <span class="uc-meta">${f.lang ? esc(f.lang) : ''}${f.stars ? ' · ★ ' + fmt(f.stars) : ''}${f.forks ? ' · ⑂ ' + fmt(f.forks) : ''}${f.watchers ? ' · 👁 ' + fmt(f.watchers) : ''}${f.lang || f.stars || f.forks || f.watchers ? ' · ' : ''}${esc(t(whenKey, { t: ucDate(f.created_at) }))}</span>
      </div>
      <button class="uc-rm" type="button">${esc(t(rmKey))}</button>
    </div>`;
  }).join('')}</div>`;
  el.querySelectorAll('.uc-rm').forEach(b => {
    b.onclick = async () => {
      const row = b.closest('.uc-row');
      b.disabled = true;
      try {
        await api(toggleEp, {
          method: 'POST',
          body: JSON.stringify({ site: 'oplugins', item_id: row.dataset.id })
        });
        row.remove();
        if (!el.querySelector('.uc-row')) ucLoadItems(el, kind);
      } catch (e) { b.disabled = false; b.textContent = authErr(e); }
    };
  });
}

/* ---------- my comments ---------- */

async function ucLoadComments(el) {
  let items;
  try { items = (await api('/me/comments?site=oplugins&limit=300')).items || []; }
  catch (e) { el.innerHTML = `<div class="uc-empty">${esc(authErr(e))}</div>`; return; }
  if (!items.length) {
    el.innerHTML = `<div class="uc-empty">${esc(t('uc.empty.comments'))}</div>`;
    return;
  }
  el.innerHTML = `<div class="uc-list">${items.map(c => {
    const href = ucRepoHref(c.item_id);
    return `<div class="uc-row uc-cmt" data-cid="${c.id}">
      <div class="uc-main">
        <div class="uc-cmt-body">${esc(c.body)}</div>
        <div class="uc-meta">
          ${c.parent_id ? `<span class="uc-tag">${esc(t('uc.reply'))}</span>` : ''}
          <span class="uc-st ${c.status}">${esc(t('uc.st.' + c.status))}</span>
          ${c.likes ? `<span>${esc(t('uc.likes.count', { n: c.likes }))}</span>` : ''}
          ${href ? `<a class="uc-link" href="${href}?c=${c.id}">${esc(c.item_id)}</a>` : `<span>${esc(c.item_id)}</span>`}
          <span>${ucDate(c.created_at)}</span>
        </div>
        ${c.status === 'rejected' && c.mod_reason ? `<div class="uc-reason">${esc(c.mod_reason)}</div>` : ''}
      </div>
      <button class="uc-rm" type="button">${esc(t('uc.del'))}</button>
    </div>`;
  }).join('')}</div>`;
  el.querySelectorAll('.uc-rm').forEach(b => {
    b.onclick = async () => {
      const row = b.closest('.uc-row');
      if (!confirm(t('uc.del.confirm'))) return;
      b.disabled = true;
      try {
        await api(`/comments/${row.dataset.cid}`, { method: 'DELETE' });
        row.remove();
        if (!el.querySelector('.uc-row')) ucLoadComments(el);
      } catch (e) { b.disabled = false; b.textContent = authErr(e); }
    };
  });
}

/* ---------- settings ---------- */

function ucCard(forId, label, sub, inner, hint = '') {
  const head = forId
    ? `<label class="uc-card-t" for="${forId}">${esc(label)}</label>`
    : `<span class="uc-card-t">${esc(label)}</span>`;
  return `<section class="uc-card">
    <div class="uc-card-h">${head}${sub || ''}</div>
    ${inner}${hint ? `<p class="uc-hint">${hint}</p>` : ''}
  </section>`;
}

async function ucLoadSettings(el) {
  const u = zk.user;
  const nameSub = u.name_status === 'pending'
    ? `<span class="uc-st pending">${esc(t('uc.name.pending'))}</span>`
    : u.name_status === 'rejected' && u.name_reason
      ? `<span class="uc-hint-inline">${esc(t('uc.name.reason', { r: u.name_reason }))}</span>` : '';
  const mailChip = u.email_verified
    ? `<span class="uc-st approved">${esc(t('uc.verified'))}</span>`
    : `<span class="uc-st pending">${esc(t('uc.unverified'))}</span>`;
  const former = (u.former_names && u.former_names.length)
    ? u.former_names.join('、') : t('uc.former.none');
  const noRenames = (u.renames_left ?? 1) <= 0;
  const nickHtml = uc.editing
    ? `<input class="auth-in uc-sm-in" id="ucNickIn" type="text" maxlength="64"
         value="${esc(u.display_name || '')}" placeholder="${esc(t('uc.set.name.ph'))}">
       <button class="uc-btn" id="ucNickGo" type="button">${esc(t('uc.save'))}</button>
       <button class="uc-btn uc-ghost" id="ucNickCancel" type="button">${esc(t('uc.cancel'))}</button>`
    : `<b>${esc(u.display_name || u.username)}</b>${nameSub}
       <button class="uc-btn uc-ghost" id="ucNickEdit" type="button"${noRenames ? ' disabled' : ''}>${esc(t('uc.edit'))}</button>`;

  el.innerHTML =
    ucCard(null, t('uc.set.account'), '', `
      <div class="uc-acct">
        <span class="uc-f"><em>${esc(t('uc.f.username'))}</em><b>${esc(u.username)}</b></span>
        <span class="uc-f"><em>${esc(t('uc.f.nickname'))}</em>${nickHtml}</span>
        <span class="uc-f"><em>${esc(t('uc.former'))}</em><span>${esc(former)}</span></span>
      </div>
      <p class="uc-warn">${esc(t('uc.rename.warn', { n: u.renames_left ?? 0 }))}</p>
      <p class="uc-err" id="ucNickErr" hidden></p>`)
    + ucCard(null, t('uc.set.email'), mailChip, `
      <div class="uc-acct"><b>${esc(u.email || '—')}</b>
        <button class="uc-btn uc-ghost" id="ucMailBtn" type="button">${esc(t('uc.edit'))}</button></div>
      <div id="ucMailBox"></div>`)
    + (u.has_password
      ? ucCard('ucPwO', t('uc.set.pass'), '', `
        <div class="uc-acct">
          <input class="auth-in uc-sm-in" id="ucPwO" type="password" placeholder="${esc(t('uc.pass.old'))}" autocomplete="current-password">
          <input class="auth-in uc-sm-in" id="ucPwN" type="password" placeholder="${esc(t('uc.pass.new'))}" autocomplete="new-password">
          <button class="uc-btn" id="ucPwGo" type="button">${esc(t('uc.save'))}</button>
        </div>
        <p class="uc-err" id="ucPwErr" hidden></p>`)
      : ucCard(null, t('uc.set.pass'), '', '', esc(t('uc.pass.oauth'))))
    + ucCard(null, t('uc.set.bind'), '', `
      <div class="uc-binds">${['github', 'google'].map(p =>
        `<span class="uc-f"><em>${esc(p)}</em>` +
        ((u.providers || []).includes(p)
          ? `<span class="uc-st approved">${esc(t('uc.bound'))}</span>`
          : `<button class="uc-btn" data-bind="${p}" type="button">${esc(t('uc.bind.do', { p }))}</button>`) +
        `</span>`
      ).join('')}</div>
      <p class="uc-hint" id="ucBindHint" hidden></p>
      <p class="uc-err" id="ucBindErr" hidden></p>`)
    + `<section class="uc-card"><button class="uc-btn uc-danger" id="ucOut" type="button">${esc(t('uc.logout'))}</button></section>`;

  const refresh = async () => { await zkLoadUser(); renderAuthChip(); };
  const saveGo = async (btn, run, errEl) => {
    if (btn.disabled) return;
    btn.disabled = true;
    const old = btn.textContent;
    btn.textContent = t('uc.saving');
    try {
      await run();
      await refresh();
      btn.textContent = t('uc.saved');
      setTimeout(() => { btn.disabled = false; btn.textContent = old; }, 1500);
    } catch (e) {
      ucErr(errEl, e);
      btn.disabled = false; btn.textContent = old;
    }
  };

  const editBtn = $('#ucNickEdit'), cancelBtn = $('#ucNickCancel');
  if (editBtn) editBtn.onclick = () => { uc.editing = true; ucLoadSettings(el); };
  if (cancelBtn) cancelBtn.onclick = () => { uc.editing = false; ucLoadSettings(el); };
  const nickGo = $('#ucNickGo');
  if (nickGo) nickGo.onclick = () => saveGo(nickGo, () =>
    api('/auth/display_name', {
      method: 'POST',
      body: JSON.stringify({ display_name: $('#ucNickIn').value.trim() })
    }).then(r => {
      zk.user.display_name = r.display_name;
      uc.editing = false;
      ucLoadSettings(el);            // back to display state with fresh former_names
    }), $('#ucNickErr'));

  $('#ucPwGo') && ($('#ucPwGo').onclick = () => saveGo($('#ucPwGo'), async () => {
    await api('/auth/password', {
      method: 'POST',
      body: JSON.stringify({
        old_password: $('#ucPwO').value,
        password: $('#ucPwN').value
      })
    });
    $('#ucPwO').value = ''; $('#ucPwN').value = '';
  }, $('#ucPwErr')));

  $('#ucMailBtn').onclick = () => {
    $('#ucMailBox').innerHTML = `
      <div class="uc-field">
        <input class="auth-in" id="ucEmIn" type="email" maxlength="200" placeholder="${esc(t('uc.email.new'))}" autocomplete="off">
        <button class="uc-btn" id="ucEmGo" type="button">${esc(t('uc.email.send'))}</button>
      </div>
      <div class="uc-field" id="ucEmCodeWrap" hidden>
        <input class="auth-in" id="ucEmCode" type="text" inputmode="numeric" maxlength="6" placeholder="${esc(t('uc.email.code'))}" autocomplete="one-time-code">
        <button class="uc-btn" id="ucEmCf" type="button">${esc(t('uc.email.confirm'))}</button>
      </div>
      <p class="uc-hint" id="ucEmHint" hidden></p>
      <p class="uc-err" id="ucEmErr" hidden></p>`;
    $('#ucEmIn').focus();
    $('#ucEmGo').onclick = () => saveGo($('#ucEmGo'), async () => {
      const email = $('#ucEmIn').value.trim();
      await api('/auth/email', {
        method: 'POST',
        body: JSON.stringify({ email, lang: LANG })
      });
      $('#ucEmCodeWrap').hidden = false;
      const h = $('#ucEmHint');
      h.textContent = t('uc.email.sent', { e: email });
      h.hidden = false;
      $('#ucEmCode').focus();
      $('#ucEmCf').onclick = () => saveGo($('#ucEmCf'), async () => {
        await api('/auth/email/verify', {
          method: 'POST',
          body: JSON.stringify({ code: $('#ucEmCode').value.trim() })
        });
        await zkLoadUser();
        render();
      }, $('#ucEmErr'));
    }, $('#ucEmErr'));
  };

  el.querySelectorAll('[data-bind]').forEach(b => {
    b.onclick = async () => {
      b.disabled = true;
      try {
        const r = await api(`/auth/link/${b.dataset.bind}`, { method: 'POST', body: '{}' });
        location.href = API_BASE + r.url;
      } catch (e) {
        ucErr($('#ucBindErr') || null, e);
        b.disabled = false;
      }
    };
  });

  if (ucLinkMsg) {                    // OAuth bind redirect landed here
    const h = $('#ucBindHint'), e = $('#ucBindErr');
    if (ucLinkMsg.ok) {
      h.textContent = t('uc.linked', { p: ucLinkMsg.val });
      h.hidden = false;
    } else {
      const fake = { code: ucLinkMsg.val, message: ucLinkMsg.val };
      e.textContent = authErr(fake);
      e.hidden = false;
    }
    ucLinkMsg = null;
  }

  $('#ucOut').onclick = zkLogout;
}

/* ---------- boot ---------- */

const UC_LOAD = {
  fav: (el) => ucLoadItems(el, 'fav'),
  likes: (el) => ucLoadItems(el, 'likes'),
  comments: ucLoadComments,
  settings: ucLoadSettings,
};

uc.tab = ucTabFromURL();
let ucLinkMsg = null;
{                                     // OAuth bind callback flag — parse
  const m = location.hash.match(/[#&](linked|link_error)=([^&]*)/);
  if (m) ucLinkMsg = { ok: m[1] === 'linked', val: decodeURIComponent(m[2]) };
}
zkInit();                             // consumes #token + cleans the hash
if (ucLinkMsg) history.replaceState(null, '', location.pathname + location.search);
applyStaticI18n();
bindChrome(render);
document.addEventListener('zk:auth', render);
document.title = t('uc.title') + ' · OpenCode Plugins';
zkLoadUser().then(() => { renderAuthChip(); render(); });
api('/stats/view', {
  method: 'POST',
  body: JSON.stringify({ site: 'oplugins', path: location.pathname })
}).catch(() => { });   /* fire-and-forget analytics */
