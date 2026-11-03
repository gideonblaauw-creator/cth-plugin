/** @typedef {Record<string, unknown> & {
 *   id: number;
 *   bot_id: string;
 *   bot_name: string;
 *   layer: string;
 *   type: string;
 *   task: string;
 *   link: string;
 *   cause_tag: string | null;
 *   ts: string;
 *   silent_over_2h?: boolean;
 * }} BotRow
 */

const botGrid = document.getElementById('bot-grid');
const gideonStrip = document.getElementById('gideon-strip');
const gideonList = document.getElementById('gideon-list');
const feedList = document.getElementById('feed-list');
const streamStatus = document.getElementById('stream-status');
const filterLayer = document.getElementById('filter-layer');
const filterType = document.getElementById('filter-type');
const filterBot = document.getElementById('filter-bot');
const filterCause = document.getElementById('filter-cause');

/** @type {BotRow[]} */
let bots = [];
/** @type {BotRow[]} */
let events = [];
/** @type {Map<string, BotRow>} */
const eventsById = new Map();
let timerInterval = null;

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function formatDuration(ms) {
  if (ms < 0 || Number.isNaN(ms)) return '—';
  const sec = Math.floor(ms / 1000);
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = sec % 60;
  if (h > 0) return `${h}h ${m}m ${s}s`;
  if (m > 0) return `${m}m ${s}s`;
  return `${s}s`;
}

function relativeSince(iso) {
  const t = Date.parse(iso);
  if (Number.isNaN(t)) return '—';
  return formatDuration(Date.now() - t);
}

function statusLabel(type) {
  return type.replace(/_/g, ' ');
}

function passesFilters(ev) {
  const layer = filterLayer.value;
  const type = filterType.value;
  const bot = filterBot.value;
  const cause = filterCause.value;
  if (layer && ev.layer !== layer) return false;
  if (type && ev.type !== type) return false;
  if (bot && ev.bot_id !== bot) return false;
  if (cause) {
    if (cause === '__none__') {
      if (ev.cause_tag) return false;
    } else if (ev.cause_tag !== cause) {
      return false;
    }
  }
  return true;
}

function renderFeed() {
  const filtered = events.filter(passesFilters);
  if (filtered.length === 0) {
    feedList.innerHTML = '<li class="feed-empty">No events match these filters.</li>';
    return;
  }
  feedList.innerHTML = filtered
    .map((ev) => {
      const cause =
        ev.cause_tag != null && ev.cause_tag !== ''
          ? `<span class="badge">${escapeHtml(ev.cause_tag)}</span>`
          : '';
      return `<li class="feed-item" data-id="${ev.id}">
        <time datetime="${escapeHtml(ev.ts)}">${escapeHtml(new Date(ev.ts).toLocaleString())}</time>
        <div class="feed-head">
          <strong>${escapeHtml(ev.bot_name)}</strong>
          <span class="badge">${escapeHtml(ev.layer)}</span>
          <span class="badge status-${escapeHtml(ev.type)}">${escapeHtml(statusLabel(ev.type))}</span>
          ${cause}
        </div>
        <p class="feed-task">${escapeHtml(ev.task)}</p>
        <div class="feed-link"><a href="${escapeHtml(ev.link)}" target="_blank" rel="noopener noreferrer">Open link</a></div>
      </li>`;
    })
    .join('');
}

function renderBotCard(bot) {
  const stalled = bot.silent_over_2h === true;
  return `<article class="bot-card${stalled ? ' stalled' : ''}" data-bot-id="${escapeHtml(bot.bot_id)}">
    <h3 class="bot-name">${escapeHtml(bot.bot_name)}</h3>
    <div class="bot-meta">
      <span class="badge">${escapeHtml(bot.layer)}</span>
      <span class="badge status-${escapeHtml(bot.type)}">${escapeHtml(statusLabel(bot.type))}</span>
    </div>
    <p class="bot-task">${escapeHtml(bot.task)}</p>
    <div class="bot-link"><a href="${escapeHtml(bot.link)}" target="_blank" rel="noopener noreferrer">Last link</a></div>
    <p class="bot-timer" data-ts="${escapeHtml(bot.ts)}">Since last event: ${escapeHtml(relativeSince(bot.ts))}</p>
  </article>`;
}

function renderBots() {
  if (bots.length === 0) {
    botGrid.innerHTML = '<p class="feed-empty">No bot activity yet.</p>';
  } else {
    botGrid.innerHTML = bots.map(renderBotCard).join('');
  }

  const waiting = bots.filter((b) => b.type === 'needs_gideon');
  if (waiting.length === 0) {
    gideonStrip.hidden = true;
    gideonList.innerHTML = '';
  } else {
    gideonStrip.hidden = false;
    gideonList.innerHTML = waiting
      .map(
        (b) =>
          `<li><strong>${escapeHtml(b.bot_name)}</strong> — ${escapeHtml(b.task)} (<a href="${escapeHtml(b.link)}" target="_blank" rel="noopener noreferrer">link</a>)</li>`,
      )
      .join('');
  }

  syncBotFilterOptions();
}

function syncBotFilterOptions() {
  const current = filterBot.value;
  const ids = [...new Set(bots.map((b) => b.bot_id))].sort();
  filterBot.innerHTML =
    '<option value="">All bots</option>' +
    ids
      .map((id) => {
        const name = bots.find((b) => b.bot_id === id)?.bot_name ?? id;
        return `<option value="${escapeHtml(id)}">${escapeHtml(name)}</option>`;
      })
      .join('');
  if (ids.includes(current)) filterBot.value = current;
}

function updateTimers() {
  document.querySelectorAll('.bot-timer[data-ts]').forEach((el) => {
    const ts = el.getAttribute('data-ts');
    if (ts) el.textContent = `Since last event: ${relativeSince(ts)}`;
  });
}

function upsertEvent(ev) {
  if (ev.id == null) return;
  const id = Number(ev.id);
  if (eventsById.has(id)) return;
  eventsById.set(id, /** @type {BotRow} */ (ev));
  events.unshift(/** @type {BotRow} */ (ev));
  if (events.length > 500) {
    const removed = events.pop();
    if (removed) eventsById.delete(removed.id);
  }
}

function mergeBotFromEvent(ev) {
  const idx = bots.findIndex((b) => b.bot_id === ev.bot_id);
  const row = /** @type {BotRow} */ ({
    ...ev,
    silent_over_2h: false,
  });
  const lastTs = Date.parse(String(ev.ts));
  const twoHours = 2 * 60 * 60 * 1000;
  row.silent_over_2h = Number.isNaN(lastTs) || Date.now() - lastTs > twoHours;

  if (idx >= 0) {
    const existingTs = Date.parse(String(bots[idx].ts));
    if (!Number.isNaN(existingTs) && existingTs > lastTs) return;
    bots[idx] = row;
  } else {
    bots.push(row);
  }
  bots.sort((a, b) => a.bot_id.localeCompare(b.bot_id));
}

async function loadBots() {
  const res = await fetch('/bots');
  if (!res.ok) throw new Error('Failed to load bots');
  const data = await res.json();
  bots = data.bots ?? [];
  renderBots();
}

async function loadEvents() {
  const res = await fetch('/events?limit=200');
  if (!res.ok) throw new Error('Failed to load events');
  const data = await res.json();
  events = [];
  eventsById.clear();
  for (const ev of data.events ?? []) {
    upsertEvent(ev);
  }
  renderFeed();
}

function setStreamState(state) {
  streamStatus.classList.remove('live', 'reconnecting');
  if (state === 'live') {
    streamStatus.textContent = 'Live';
    streamStatus.classList.add('live');
  } else if (state === 'reconnecting') {
    streamStatus.textContent = 'Reconnecting…';
    streamStatus.classList.add('reconnecting');
  } else {
    streamStatus.textContent = 'Connecting…';
  }
}

function connectStream() {
  const es = new EventSource('/stream');

  es.onopen = () => setStreamState('live');

  es.onmessage = (msg) => {
    try {
      const ev = JSON.parse(msg.data);
      upsertEvent(ev);
      mergeBotFromEvent(ev);
      renderBots();
      renderFeed();
    } catch {
      /* ignore malformed */
    }
  };

  es.onerror = () => {
    setStreamState('reconnecting');
    es.close();
    window.setTimeout(connectStream, 2000);
  };
}

filterLayer.addEventListener('change', renderFeed);
filterType.addEventListener('change', renderFeed);
filterBot.addEventListener('change', renderFeed);
filterCause.addEventListener('change', renderFeed);

async function init() {
  try {
    await Promise.all([loadBots(), loadEvents()]);
  } catch (err) {
    feedList.innerHTML = `<li class="feed-empty">Could not load data: ${escapeHtml(err.message)}</li>`;
  }
  connectStream();
  timerInterval = window.setInterval(() => {
    updateTimers();
    const twoHours = 2 * 60 * 60 * 1000;
    document.querySelectorAll('.bot-card[data-bot-id]').forEach((card) => {
      const timer = card.querySelector('.bot-timer[data-ts]');
      const ts = timer?.getAttribute('data-ts');
      const lastTs = ts ? Date.parse(ts) : NaN;
      const stalled = Number.isNaN(lastTs) || Date.now() - lastTs > twoHours;
      card.classList.toggle('stalled', stalled);
    });
  }, 1000);
}

init();

window.addEventListener('beforeunload', () => {
  if (timerInterval) clearInterval(timerInterval);
});
