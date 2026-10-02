/* ── Control Room — live clock and date ── */

(function () {
  const clockEl = document.getElementById('cr-clock');
  const dateEl  = document.getElementById('cr-date');

  function pad(n) { return String(n).padStart(2, '0'); }

  function tick() {
    const now = new Date();
    const h   = now.getHours();
    const m   = pad(now.getMinutes());
    const s   = pad(now.getSeconds());
    const ampm = h >= 12 ? 'PM' : 'AM';
    const h12  = h % 12 || 12;
    if (clockEl) clockEl.textContent = `Updated ${pad(h12)}:${m}:${s} ${ampm}`;
  }

  function setDate() {
    if (!dateEl) return;
    const now = new Date();
    dateEl.textContent = now.toLocaleDateString('en-US', {
      weekday: 'long',
      year:    'numeric',
      month:   'long',
      day:     'numeric',
    });
  }

  tick();
  setDate();
  setInterval(tick, 1000);
}());
