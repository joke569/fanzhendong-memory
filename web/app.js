(() => {
  const ITEMS = window.MEMORIES || [];
  const LINES = window.LINES || {};
  const STORE_KEY = 'fzd_memory_v1';

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  const app = $('#app');
  const ambient = $('#ambient');
  const heroCard = $('#heroCard');
  const heroImg = $('#heroImg');
  const heroLine = $('#heroLine');
  const heroDate = $('#heroDate');
  const heroYear = $('#heroYear');
  const heroTitle = $('#heroTitle');
  const heroSubtitle = $('#heroSubtitle');
  const marqueeTrack = $('#marqueeTrack');
  const favBtn = $('#favBtn');
  const filmstrip = $('#filmstrip');
  const progressText = $('#progressText');
  const progressLine = $('#progressLine');
  const allBtn = $('#allBtn');
  const backdrop = $('#backdrop');
  const toast = $('#toast');
  const detailSheet = $('#detailSheet');
  const timelineSheet = $('#timelineSheet');
  const settingsSheet = $('#settingsSheet');

  const state = {
    favorites: new Set(),
    notes: {},
    visited: new Set(),
    lastId: '',
    reduceMotion: false,
    activeLine: 'all',
  };
  let filtered = ITEMS.slice();
  let currentId = ITEMS[0] ? ITEMS[0].id : '';
  let autoTimer = null;
  let noteTimer = null;
  let sheetOpen = false;
  let suppressClick = false;

  function load() {
    try {
      const raw = localStorage.getItem(STORE_KEY);
      if (!raw) return;
      const data = JSON.parse(raw);
      state.favorites = new Set(data.favorites || []);
      state.notes = data.notes || {};
      state.visited = new Set(data.visited || []);
      state.lastId = data.lastId || '';
      state.reduceMotion = Boolean(data.reduceMotion);
      state.activeLine = data.activeLine || 'all';
    } catch (e) {
      // localStorage may be unavailable in private mode; keep defaults
    }
  }

  function save() {
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify({
        favorites: Array.from(state.favorites),
        notes: state.notes,
        visited: Array.from(state.visited),
        lastId: state.lastId,
        reduceMotion: state.reduceMotion,
        activeLine: state.activeLine,
      }));
    } catch (e) { /* noop */ }
  }

  function lineOf(item) { return LINES[item.line] || { label: item.line, en: item.line.toUpperCase(), accent: item.accent }; }
  function imageOf(item) { return 'assets/' + item.image; }
  function indexOfCurrent() { return filtered.findIndex(i => i.id === currentId); }
  function currentItem() { return ITEMS.find(i => i.id === currentId) || ITEMS[0]; }

  function showToast(text) {
    toast.textContent = text;
    toast.classList.add('show');
    clearTimeout(showToast._t);
    showToast._t = setTimeout(() => toast.classList.remove('show'), 1900);
  }

  function setAmbient(item) {
    ambient.style.backgroundImage = `url("${imageOf(item)}")`;
  }

  function renderHero(item, animate = true) {
    if (!item) return;
    currentId = item.id;
    state.lastId = item.id;
    state.visited.add(item.id);
    save();

    const meta = lineOf(item);
    heroImg.src = imageOf(item);
    heroImg.alt = `${item.year} ${item.title}`;
    heroLine.textContent = meta.en;
    heroLine.style.color = meta.accent;
    heroDate.textContent = item.date;
    heroYear.textContent = item.year;
    heroTitle.textContent = item.title;
    heroSubtitle.textContent = item.subtitle;
    marqueeTrack.innerHTML = [item.caption, item.caption, item.caption]
      .map(t => `<span>${t}　·　</span>`).join('');
    favBtn.classList.toggle('active', state.favorites.has(item.id));
    favBtn.setAttribute('aria-label', state.favorites.has(item.id) ? '取消收藏' : '收藏');

    if (animate) {
      heroCard.classList.remove('swap');
      void heroCard.offsetWidth;
      heroCard.classList.add('swap');
    }
    setAmbient(item);
    updateProgress();
    updateFilmstripActive();
    progressLine.classList.remove('run');
    void progressLine.offsetWidth;
    if (!state.reduceMotion) progressLine.classList.add('run');
  }

  function updateProgress() {
    const total = filtered.length || 1;
    const index = Math.max(0, indexOfCurrent());
    progressText.textContent = `${String(index + 1).padStart(2, '0')} / ${String(total).padStart(2, '0')}`;
  }

  function buildFilmstrip() {
    const sequence = ITEMS.concat(ITEMS);
    filmstrip.innerHTML = sequence.map(item => `
      <button class="film-thumb" data-id="${item.id}" type="button" aria-label="${item.year} ${item.title}">
        <img src="${imageOf(item)}" alt="" loading="lazy" />
      </button>
    `).join('');
    updateFilmstripActive();
  }

  function updateFilmstripActive() {
    $$('.film-thumb', filmstrip).forEach(el => {
      el.classList.toggle('active', el.dataset.id === currentId);
    });
  }

  function setFilter(line, selectId) {
    state.activeLine = line || 'all';
    filtered = state.activeLine === 'all' ? ITEMS.slice() : ITEMS.filter(i => i.line === state.activeLine);
    if (!filtered.length) filtered = ITEMS.slice();
    $$('.dock-btn').forEach(btn => btn.classList.toggle('active', btn.dataset.line === state.activeLine));
    allBtn.classList.toggle('active', state.activeLine === 'all');
    allBtn.textContent = state.activeLine === 'all' ? '全部' : '返回全部';
    const target = selectId && filtered.find(i => i.id === selectId) ? selectId : filtered[0].id;
    renderHero(filtered.find(i => i.id === target), true);
    restartAuto();
  }

  function step(delta) {
    if (filtered.length < 2) return;
    let index = indexOfCurrent();
    if (index < 0) index = 0;
    index = (index + delta + filtered.length) % filtered.length;
    renderHero(filtered[index], true);
    restartAuto();
  }

  function restartAuto() {
    clearInterval(autoTimer);
    autoTimer = setInterval(() => {
      if (state.reduceMotion || sheetOpen || document.hidden) return;
      if (filtered.length < 2) return;
      step(1);
    }, 6800);
  }

  function openSheet(sheet) {
    closeSheets(true);
    sheetOpen = true;
    sheet.classList.add('open');
    sheet.setAttribute('aria-hidden', 'false');
    backdrop.classList.add('show');
    document.body.classList.add('sheet-open');
  }

  function closeSheets(keepBackdrop = false) {
    [detailSheet, timelineSheet, settingsSheet].forEach(s => {
      s.classList.remove('open');
      s.setAttribute('aria-hidden', 'true');
    });
    sheetOpen = false;
    if (!keepBackdrop) {
      backdrop.classList.remove('show');
      document.body.classList.remove('sheet-open');
    }
  }

  function toggleFavorite(id) {
    if (state.favorites.has(id)) {
      state.favorites.delete(id);
      showToast('已取消收藏');
    } else {
      state.favorites.add(id);
      showToast('已收藏这段回忆');
    }
    save();
    favBtn.classList.toggle('active', state.favorites.has(currentId));
    if ($('#detailFavBtn')) updateDetailFavorite(id);
  }

  function updateDetailFavorite(id) {
    const btn = $('#detailFavBtn');
    if (!btn) return;
    const active = state.favorites.has(id);
    btn.textContent = active ? '已收藏 ✓' : '收藏这段';
    btn.classList.toggle('active', active);
    btn.style.borderColor = active ? 'rgba(231,183,104,.55)' : '';
    btn.style.color = active ? 'var(--gold)' : '';
  }

  function openDetail(item) {
    if (!item) return;
    const meta = lineOf(item);
    $('#detailImg').src = imageOf(item);
    $('#detailImg').alt = `${item.year} ${item.title}`;
    $('#detailLine').textContent = meta.en;
    $('#detailLine').style.color = meta.accent;
    $('#detailDate').textContent = item.date;
    $('#detailYear').textContent = item.year;
    $('#detailTitle').textContent = item.title;
    $('#detailSubtitle').textContent = item.subtitle;
    $('#detailDesc').textContent = item.description;
    $('#detailQuote').textContent = '“' + item.quote + '”';
    $('#detailTags').innerHTML = item.tags.map(t => `<span>${t}</span>`).join('');
    const extras = [];
    if (item.colorway) extras.push(['配色', item.colorway]);
    if (item.fabric) extras.push(['面料', item.fabric]);
    if (item.spec) extras.push(['配置', item.spec]);
    extras.push(['时间', item.date]);
    $('#detailExtra').innerHTML = extras.map(([k, v]) => `<div><span>${k}</span><span>${v}</span></div>`).join('');
    $('#detailSource').textContent = `${item.source} · ${item.credit}`;
    $('#noteInput').value = state.notes[item.id] || '';
    $('#noteStatus').textContent = state.notes[item.id] ? '已保存' : '自动保存';
    updateDetailFavorite(item.id);
    $('#prevBtn').disabled = filtered.length < 2;
    $('#nextBtn').disabled = filtered.length < 2;
    openSheet(detailSheet);
    $('#detailScroll').scrollTop = 0;
    try { history.replaceState(null, '', '#detail=' + item.id); } catch (e) {}
  }

  function saveNote() {
    const item = currentItem();
    if (!item) return;
    const value = $('#noteInput').value.trim();
    if (value) state.notes[item.id] = value; else delete state.notes[item.id];
    save();
    $('#noteStatus').textContent = '已保存';
    showToast('手记已保存');
  }

  function scheduleNoteSave() {
    $('#noteStatus').textContent = '保存中…';
    clearTimeout(noteTimer);
    noteTimer = setTimeout(saveNote, 900);
  }

  function openTimeline() {
    renderTimeline($('.chip.active', $('#timelineFilters'))?.dataset.tl || 'all');
    openSheet(timelineSheet);
  }

  function renderTimeline(line) {
    const list = line === 'all' ? ITEMS : ITEMS.filter(i => i.line === line);
    $('#timelineList').innerHTML = list.map(item => `
      <button class="timeline-item" data-id="${item.id}" type="button">
        <img src="${imageOf(item)}" alt="" loading="lazy" />
        <span class="timeline-copy">
          <span>${item.date} · ${lineOf(item).en}</span>
          <strong>${item.title}</strong>
          <small>${item.subtitle}</small>
        </span>
        <em>${item.no}</em>
      </button>
    `).join('');
  }

  function openSettings() {
    $('#motionToggle').checked = state.reduceMotion;
    const visited = state.visited.size;
    $('#journeyCount').textContent = `${visited} / 22`;
    $('#journeyBar').style.width = `${Math.min(100, visited / 22 * 100)}%`;
    $('#journeyHint').textContent = visited >= 10
      ? '已解锁 · 巴黎的金色雨'
      : '继续探索，解锁隐藏回忆。';
    const achievements = [];
    if (visited >= 10) achievements.push('巴黎的金色雨');
    if (state.favorites.size >= 5) achievements.push('三线收藏家');
    $('#achievementText').textContent = achievements.length
      ? '成就：' + achievements.join(' · ')
      : '';
    openSheet(settingsSheet);
  }

  function setReduceMotion(value) {
    state.reduceMotion = Boolean(value);
    app.classList.toggle('reduce-motion', state.reduceMotion);
    save();
    if (state.reduceMotion) {
      progressLine.classList.remove('run');
      clearInterval(autoTimer);
    } else {
      progressLine.classList.add('run');
      restartAuto();
    }
    $('#motionToggle').checked = state.reduceMotion;
  }

  function clearData() {
    if (!window.confirm('确定清空所有收藏与手记吗？')) return;
    state.favorites.clear();
    state.notes = {};
    state.visited.clear();
    state.lastId = '';
    save();
    favBtn.classList.remove('active');
    $('#noteInput').value = '';
    $('#noteStatus').textContent = '自动保存';
    showToast('收藏与手记已清空');
  }

  // ---------- events ----------
  heroCard.addEventListener('click', (e) => {
    if (suppressClick) { suppressClick = false; return; }
    if (e.target.closest('#favBtn')) return;
    openDetail(currentItem());
  });
  heroCard.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openDetail(currentItem()); }
  });
  favBtn.addEventListener('click', (e) => { e.stopPropagation(); toggleFavorite(currentId); });

  $$('.dock-btn').forEach(btn => btn.addEventListener('click', () => setFilter(btn.dataset.line)));
  allBtn.addEventListener('click', () => setFilter('all'));
  $('#timelineBtn').addEventListener('click', openTimeline);
  $('#settingsBtn').addEventListener('click', openSettings);
  backdrop.addEventListener('click', () => closeSheets());
  $$('[data-close]').forEach(el => el.addEventListener('click', () => closeSheets()));

  filmstrip.addEventListener('click', (e) => {
    const btn = e.target.closest('.film-thumb');
    if (!btn) return;
    const item = ITEMS.find(i => i.id === btn.dataset.id);
    if (!item) return;
    if (filtered.every(i => i.id !== item.id)) {
      filtered = ITEMS.slice();
      state.activeLine = 'all';
      $$('.dock-btn').forEach(b => b.classList.remove('active'));
      allBtn.classList.add('active');
      allBtn.textContent = '全部';
    }
    renderHero(item, true);
    restartAuto();
  });

  $('#detailFavBtn').addEventListener('click', () => {
    toggleFavorite(currentId);
    updateDetailFavorite(currentId);
  });
  $('#saveNoteBtn').addEventListener('click', saveNote);
  $('#noteInput').addEventListener('input', scheduleNoteSave);
  $('#prevBtn').addEventListener('click', () => { step(-1); openDetail(currentItem()); });
  $('#nextBtn').addEventListener('click', () => { step(1); openDetail(currentItem()); });
  $('#timelineFilters').addEventListener('click', (e) => {
    const chip = e.target.closest('.chip'); if (!chip) return;
    $$('.chip', $('#timelineFilters')).forEach(c => c.classList.toggle('active', c === chip));
    renderTimeline(chip.dataset.tl);
  });
  $('#timelineList').addEventListener('click', (e) => {
    const row = e.target.closest('.timeline-item'); if (!row) return;
    const item = ITEMS.find(i => i.id === row.dataset.id);
    if (!item) return;
    if (filtered.every(i => i.id !== item.id)) {
      filtered = ITEMS.slice();
      state.activeLine = 'all';
      $$('.dock-btn').forEach(b => b.classList.remove('active'));
      allBtn.classList.add('active');
      allBtn.textContent = '全部';
    }
    renderHero(item, true);
    closeSheets();
    restartAuto();
  });
  $('#motionToggle').addEventListener('change', (e) => setReduceMotion(e.target.checked));
  $('#clearDataBtn').addEventListener('click', clearData);

  // swipe / keyboard
  let startY = null;
  heroCard.addEventListener('pointerdown', (e) => { startY = e.clientY; });
  heroCard.addEventListener('pointerup', (e) => {
    if (startY === null) return;
    const dy = e.clientY - startY;
    startY = null;
    if (Math.abs(dy) > 46) {
      suppressClick = true;
      step(dy < 0 ? 1 : -1);
    }
  });
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { closeSheets(); return; }
    if (sheetOpen) return;
    if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { e.preventDefault(); step(1); }
  });

  // init
  load();
  app.classList.toggle('reduce-motion', state.reduceMotion);
  buildFilmstrip();
  const startItem = ITEMS.find(i => i.id === state.lastId) || ITEMS[0];
  state.activeLine = ['career', 'jersey', 'paddle'].includes(state.activeLine) ? state.activeLine : 'all';
  filtered = state.activeLine === 'all' ? ITEMS.slice() : ITEMS.filter(i => i.line === state.activeLine);
  if (!filtered.length) { filtered = ITEMS.slice(); state.activeLine = 'all'; }
  $$('.dock-btn').forEach(btn => btn.classList.toggle('active', btn.dataset.line === state.activeLine));
  allBtn.classList.toggle('active', state.activeLine === 'all');
  allBtn.textContent = state.activeLine === 'all' ? '全部' : '返回全部';
  const initial = filtered.find(i => i.id === startItem.id) || filtered[0];
  renderHero(initial, false);
  restartAuto();
  if (state.reduceMotion) progressLine.classList.remove('run');

  // Permalink for screenshots / sharing: #detail=id, #tab=line, #sheet=timeline
  try {
    const hash = decodeURIComponent(location.hash.replace(/^#/, ''));
    const params = new URLSearchParams(hash);
    if (params.get('tab') && ['career', 'jersey', 'paddle', 'all'].includes(params.get('tab'))) {
      setFilter(params.get('tab'));
    }
    if (params.get('item')) {
      const item = ITEMS.find(i => i.id === params.get('item'));
      if (item) {
        if (filtered.every(i => i.id !== item.id)) {
          filtered = ITEMS.slice();
          state.activeLine = 'all';
          $$('.dock-btn').forEach(b => b.classList.remove('active'));
          allBtn.classList.add('active');
          allBtn.textContent = '全部';
        }
        renderHero(item, false);
      }
    }
    if (params.get('detail')) {
      const item = ITEMS.find(i => i.id === params.get('detail'));
      if (item) openDetail(item);
    } else if (params.get('sheet') === 'timeline') {
      openTimeline();
    } else if (params.get('sheet') === 'settings') {
      openSettings();
    }
  } catch (e) {}

  // service worker
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
  }
})();

