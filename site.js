/* Shared behaviour for the inner pages (services, about): theme, text size, phone menu, language, progress bar.
   It mirrors the home page so settings chosen on one page carry over to the others. */
(function(){
  var $ = function(id){ return document.getElementById(id); };
  var root = document.documentElement;
  root.classList.add('live');

  // ---- theme and text size ----
  function setTheme(m){
    if(m === 'light' || m === 'dark') root.setAttribute('data-theme', m); else { root.removeAttribute('data-theme'); m = 'auto'; }
    try{ localStorage.setItem('cd-theme', m); }catch(e){}
    document.querySelectorAll('#themeseg button').forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.t === m ? 'true' : 'false'); });
  }
  function setText(sz){
    root.classList.toggle('text-lg', sz === 'large');
    try{ localStorage.setItem('cd-text', sz); }catch(e){}
    document.querySelectorAll('#textseg button').forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.s === sz ? 'true' : 'false'); });
  }
  var t = 'auto', z = 'normal';
  try{ t = localStorage.getItem('cd-theme') || 'auto'; z = localStorage.getItem('cd-text') || 'normal'; }catch(e){}
  setTheme(t); setText(z);
  if($('theme')) $('theme').addEventListener('click', function(){
    var cur = root.getAttribute('data-theme') || (matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
    setTheme(cur === 'dark' ? 'light' : 'dark');
  });
  if($('themeseg')) $('themeseg').addEventListener('click', function(e){ var b = e.target.closest('button'); if(b) setTheme(b.dataset.t); });
  if($('textseg')) $('textseg').addEventListener('click', function(e){ var b = e.target.closest('button'); if(b) setText(b.dataset.s); });

  // ---- phone menu ----
  var sheet = $('msheet'), mbtn = $('menubtn');
  function setMenu(open){
    if(!sheet || !mbtn) return;
    sheet.hidden = !open; mbtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    mbtn.setAttribute('aria-label', T(open ? 'Close menu' : 'Menu'));
    if(open){ var f = sheet.querySelector('a'); if(f) f.focus({preventScroll: true}); }
  }
  if(mbtn){
    mbtn.addEventListener('click', function(e){ e.stopPropagation(); setMenu(sheet.hidden); });
    sheet.addEventListener('click', function(e){ if(e.target.closest('a')) setMenu(false); });
    document.addEventListener('click', function(e){ if(!sheet.hidden && !sheet.contains(e.target) && !mbtn.contains(e.target)) setMenu(false); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && !sheet.hidden){ setMenu(false); mbtn.focus(); } });
    addEventListener('resize', function(){ if(innerWidth > 1060 && !sheet.hidden) setMenu(false); });
  }

  // ---- language: same table (i18n.json) and storage key as the home page ----
  var DICT = {}, LANG = 'en', nodes = [], attrEls = [], state = 0, waiting = [];
  function T(s){ var d = DICT[s]; return (LANG !== 'en' && d && d[LANG]) || s; }
  function collect(){
    var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null), nd;
    while((nd = w.nextNode())){
      var raw = nd.nodeValue, tr = raw.trim();
      if(!tr || !DICT[tr] || (nd.parentElement && nd.parentElement.closest('script,style,svg'))) continue;
      nodes.push({n: nd, en: tr, lead: raw.match(/^\s*/)[0], trail: raw.match(/\s*$/)[0]});
    }
    document.querySelectorAll('[aria-label],[placeholder],img[alt]').forEach(function(el){
      ['aria-label','placeholder','alt'].forEach(function(a){ var v = el.getAttribute(a); if(v && DICT[v]) attrEls.push({el: el, a: a, en: v}); });
    });
  }
  function load(cb){
    if(state === 2){ cb(); return; }
    waiting.push(cb); if(state === 1) return; state = 1;
    var v = (document.querySelector('meta[name="build"]') || {}).content || '';
    fetch('/i18n.json?v=' + encodeURIComponent(v)).then(function(r){ return r.ok ? r.json() : Promise.reject(); }).then(function(j){
      Object.keys(j.hi).forEach(function(k){ DICT[k] = {hi: j.hi[k], pa: j.pa[k]}; });
      collect(); state = 2;
    }).catch(function(){ state = 0; }).then(function(){ var q = waiting; waiting = []; q.forEach(function(f){ f(); }); });
  }
  var fonts = {};
  function font(l){
    if(l === 'en' || fonts[l]) return; fonts[l] = true;
    var lk = document.createElement('link'); lk.rel = 'stylesheet';
    lk.href = 'https://fonts.googleapis.com/css2?family=' + (l === 'hi' ? 'Noto+Sans+Devanagari' : 'Noto+Sans+Gurmukhi') + ':wght@400;500;600;700;800&display=swap';
    document.head.appendChild(lk);
  }
  var titleEn = document.title;
  function apply(l){
    font(l);
    if(l !== 'en' && state !== 2){ load(function(){ if(state === 2) apply(l); else root.classList.remove('i18n-wait'); }); return; }
    LANG = l;
    root.lang = l === 'en' ? 'en-IN' : l;
    nodes.forEach(function(o){ o.n.nodeValue = o.lead + T(o.en) + o.trail; });
    attrEls.forEach(function(o){ o.el.setAttribute(o.a, T(o.en)); });
    var h = document.querySelector('meta[name="page-title-key"]');
    document.title = (l === 'en' || !h) ? titleEn : T(h.content) + ' | ' + T('Chandigarh Multispeciality Dental Clinic');
    document.querySelectorAll('.lang button').forEach(function(b){ b.setAttribute('aria-pressed', b.dataset.l === l ? 'true' : 'false'); });
    try{ localStorage.setItem('cd-lang', l); }catch(e){}
    root.classList.remove('i18n-wait');
  }
  document.querySelectorAll('.lang').forEach(function(g){ g.addEventListener('click', function(e){
    var b = e.target.closest('button[data-l]'); if(!b) return; font(b.dataset.l); load(function(){ apply(b.dataset.l); });
  }); });
  document.querySelectorAll('.lang,#menubtn').forEach(function(el){ ['pointerenter','focusin','touchstart'].forEach(function(ev){ el.addEventListener(ev, function(){ load(function(){}); }, {passive: true, once: true}); }); });
  var saved = null; try{ saved = localStorage.getItem('cd-lang'); }catch(e){}
  if(saved === 'hi' || saved === 'pa') apply(saved);

  // ---- floating contact bar: hidden while a section's own buttons are on screen ----
  (function(){ var bar = document.getElementById('callbar'); if(!bar) return;
    if(!('IntersectionObserver' in window)){ bar.classList.remove('away'); return; }
    var seen = new Set();
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting) seen.add(e.target); else seen.delete(e.target); });
      bar.classList.toggle('away', seen.size > 0);
    }, {rootMargin: '-70px 0px 0px 0px'});
    document.querySelectorAll('.hero-cta, main .btn:not(.sm), #form, footer').forEach(function(el){ io.observe(el); });
  })();

  // ---- scroll reveals: text and photos come in as they reach the screen. Skipped for reduced motion,
  //      and for anything already on screen when the page opens, so nothing flashes. ----
  (function(){
    if(matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function(es){
      es.forEach(function(x){ if(x.isIntersecting){ x.target.classList.add('in'); io.unobserve(x.target); } });
    }, {threshold: .15});
    var limit = innerHeight * .92;
    document.querySelectorAll('main .head, .svc-photo, .svc-main, main .stat, .steps li, .team-gen, .about-find, .cta-band').forEach(function(el){
      if(el.getBoundingClientRect().top < limit) return;
      var sib = [].filter.call(el.parentElement.children, function(c){ return c.tagName === el.tagName; });
      if(el.matches('.stat, .steps li')) el.style.setProperty('--d', (Math.min(sib.indexOf(el), 5) * 90) + 'ms');
      el.classList.add('sr'); io.observe(el);
    });
    root.classList.add('anim');
  })();

  // ---- reading-progress bar and footer year ----
  var bar = $('progress');
  if(bar){
    if(window.CSS && CSS.supports('animation-timeline: scroll()')) bar.classList.add('sd');
    else addEventListener('scroll', function(){ var h = document.documentElement.scrollHeight - innerHeight; bar.style.transform = 'scaleX(' + (h > 0 ? scrollY / h : 0) + ')'; }, {passive: true});
  }
  if($('yr')) $('yr').textContent = new Date().getFullYear();
})();
