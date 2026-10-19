(function () {
  var root = document.querySelector('.kww');
  if (!root) return;

  // Header shadow once the page scrolls
  var hdr = document.getElementById('kww-hdr');
  var onScroll = function () { hdr && hdr.classList.toggle('is-scrolled', window.scrollY > 10); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Desktop dropdowns: click/keyboard support (hover is handled in CSS)
  root.querySelectorAll('.has-dd > button').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var li = btn.parentElement, open = !li.classList.contains('open');
      root.querySelectorAll('.has-dd.open').forEach(function (o) { o.classList.remove('open'); o.firstElementChild.setAttribute('aria-expanded', 'false'); });
      li.classList.toggle('open', open); btn.setAttribute('aria-expanded', String(open));
    });
  });
  document.addEventListener('click', function () {
    root.querySelectorAll('.has-dd.open').forEach(function (o) { o.classList.remove('open'); o.firstElementChild.setAttribute('aria-expanded', 'false'); });
  });

  // Mobile drawer
  var drawer = document.getElementById('kww-drawer'), burger = root.querySelector('.burger');
  var setDrawer = function (open) {
    if (!drawer) return;
    drawer.classList.toggle('open', open);
    drawer.setAttribute('aria-hidden', String(!open));
    burger && burger.setAttribute('aria-expanded', String(open));
    document.documentElement.style.overflow = open ? 'hidden' : '';
  };
  burger && burger.addEventListener('click', function () { setDrawer(true); });
  drawer && drawer.querySelectorAll('[data-close]').forEach(function (b) { b.addEventListener('click', function () { setDrawer(false); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setDrawer(false); });

  // Tabs
  root.querySelectorAll('[role="tablist"]').forEach(function (list) {
    var tabs = list.querySelectorAll('[role="tab"]');
    var select = function (tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
      if (focus) tab.focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); history.replaceState(null, '', '#' + t.dataset.hash); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') select(tabs[(i + 1) % tabs.length], true);
        if (e.key === 'ArrowLeft') select(tabs[(i - 1 + tabs.length) % tabs.length], true);
      });
    });
    // Old URLs like /health-and-welfare-lasting-powers-of-attorney redirect to #health
    var h = location.hash.slice(1);
    tabs.forEach(function (t) { if (t.dataset.hash === h) select(t); });
  });

  // Reveal on scroll
  var rv = root.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -40px 0px' });
    rv.forEach(function (el) { io.observe(el); });
  } else rv.forEach(function (el) { el.classList.add('in'); });

  root.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
