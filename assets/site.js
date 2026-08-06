(function(){
  'use strict';
  var ruhig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Diese Datei wird von index.html UND en.html geladen. Die Meldungen
     richten sich deshalb nach dem lang-Attribut der jeweiligen Seite —
     sonst antwortet das englische Formular auf Deutsch. */
  var TEXTE = {
    de: {
      fehlt:   'Mir fehlen noch dein Name oder deine E-Mail-Adresse.',
      vorschau:'Das ist noch die Vorschau — hier wird nichts verschickt. '
             + 'Sobald die Seite live geht, landet deine Nachricht direkt bei Lilly.',
      moment:  'Einen Moment …',
      da:      'Angekommen. Ich melde mich bei dir.',
      fehler:  'Das hat nicht geklappt — schreib mir gern direkt.',
      offline: 'Das hat gerade nicht geklappt. Versuch es später noch einmal.'
    },
    en: {
      fehlt:   'I still need your name or your email address.',
      vorschau:'This is still the preview — nothing is sent from here. '
             + 'Once the site goes live, your message will reach Lilly directly.',
      moment:  'One moment …',
      da:      'It arrived. I will get back to you.',
      fehler:  'That did not work — feel free to write to me directly.',
      offline: 'That did not work just now. Please try again later.'
    }
  };
  var T = TEXTE[document.documentElement.lang] || TEXTE.de;

  /* ── Ausklapp-Navigation ── */
  var knopf = document.getElementById('menue'),
      nav   = document.getElementById('nav');

  function navSetzen(offen){
    nav.dataset.offen = offen ? 'true' : 'false';
    knopf.setAttribute('aria-expanded', offen ? 'true' : 'false');
    document.body.style.overflow = offen ? 'hidden' : '';
  }
  knopf.addEventListener('click', function(){
    navSetzen(nav.dataset.offen !== 'true');
  });
  nav.addEventListener('click', function(e){
    if (e.target.closest('a')) navSetzen(false);
  });
  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape' && nav.dataset.offen === 'true'){ navSetzen(false); knopf.focus(); }
  });

  /* ── Reveals (W21: „die Teile fliegen so ein bisschen rein") ──
     Wichtig: Ein Reveal darf NIEMALS dazu fuehren, dass Inhalt dauerhaft
     unsichtbar bleibt. Der IntersectionObserver allein reicht dafuer nicht —
     in gedrosselten oder nicht malenden Renderern (Hintergrund-Tab,
     bfcache-Rueckkehr, Fernsteuerung) laeuft sein Callback nicht an, und
     die Seite waere leer. Deshalb zusaetzlich eine eigene Pruefung auf
     scroll/resize/pageshow. Genau so beim Bau aufgefallen. */
  var teile = Array.prototype.slice.call(document.querySelectorAll('.reveal'));

  function zeigen(el){ el.classList.add('da'); }

  if (ruhig || !('IntersectionObserver' in window)){
    teile.forEach(zeigen);
  } else {
    var beobachter = new IntersectionObserver(function(eintraege){
      eintraege.forEach(function(e){
        if (e.isIntersecting){ zeigen(e.target); beobachter.unobserve(e.target); }
      });
    }, {rootMargin:'0px 0px -8% 0px', threshold:0.08});
    teile.forEach(function(t){ beobachter.observe(t); });

    /* Zeitdrossel statt requestAnimationFrame: rAF steckt in derselben
       Falle wie der Observer — es laeuft nicht, wenn nicht gemalt wird. */
    var zuletzt = 0;
    function pruefen(){
      zuletzt = Date.now();
      var grenze = window.innerHeight * 0.94;
      teile = teile.filter(function(t){
        if (t.classList.contains('da')) return false;
        /* Nur die Oberkante pruefen, NICHT zusaetzlich `bottom > 0`:
           Wer ueber einen Abschnitt hinwegspringt (Sprungmarke im Menue,
           wiederhergestellte Scrollposition), haette ihn sonst fuer immer
           unsichtbar — beim Hochscrollen waeren dort leere Flaechen. */
        if (t.getBoundingClientRect().top < grenze){ zeigen(t); return false; }
        return true;
      });
      if (!teile.length){
        window.removeEventListener('scroll', anstossen);
        window.removeEventListener('resize', anstossen);
      }
    }
    function anstossen(){
      if (Date.now() - zuletzt > 90) pruefen();
    }
    window.addEventListener('scroll', anstossen, {passive:true});
    window.addEventListener('resize', anstossen);
    window.addEventListener('pageshow', anstossen);
    pruefen();
  }
  /* Beim Drucken ist nichts „im Viewport" — alles sichtbar machen. */
  if (window.matchMedia) {
    var druck = window.matchMedia('print');
    var alleZeigen = function(){ document.querySelectorAll('.reveal').forEach(zeigen); };
    if (druck.addEventListener) druck.addEventListener('change', alleZeigen);
    window.addEventListener('beforeprint', alleZeigen);
  }

  /* ── Seitenreiter markiert das aktuelle Kapitel ── */
  var marken = Array.prototype.slice.call(document.querySelectorAll('.rail a'));
  var ziele  = marken.map(function(a){ return document.querySelector(a.getAttribute('href')); });
  if ('IntersectionObserver' in window){
    var kapitel = new IntersectionObserver(function(eintraege){
      eintraege.forEach(function(e){
        if (!e.isIntersecting) return;
        var i = ziele.indexOf(e.target);
        marken.forEach(function(m, j){ m.classList.toggle('aktiv', i === j); });
      });
    }, {rootMargin:'-45% 0px -45% 0px'});
    ziele.forEach(function(z){ if (z) kapitel.observe(z); });
  }

  /* ── Glut-Linie: Fortschritt als CSS-Variable ── */
  var linie = document.querySelector('.glutlinie');
  function fortschritt(){
    if (!linie) return;
    var moeglich = document.documentElement.scrollHeight - window.innerHeight;
    var wert = moeglich > 0 ? Math.min(1, window.scrollY / moeglich) : 0;
    linie.style.setProperty('--fortschritt', wert.toFixed(4));
  }
  window.addEventListener('scroll', fortschritt, {passive:true});
  window.addEventListener('resize', fortschritt);
  fortschritt();

  /* ── Sprachwechsel behaelt die Stelle (W5, zweite Haelfte) ──
     Beide Fassungen tragen dieselben IDs. Ohne das landet man beim
     Sprachwechsel aus Kapitel 05 wieder ganz oben. */
  document.querySelectorAll('.sprache a').forEach(function(a){
    a.addEventListener('click', function(){
      if (location.hash) a.href = a.getAttribute('href').split('#')[0] + location.hash;
    });
  });

  /* ── Absicht des angeklickten Knopfes ins Formular uebernehmen ──
     Sechs verschiedene Wege enden im selben Formular. Wer sich fuer die
     Warteliste entschieden hat, soll das nicht noch einmal tippen. */
  document.querySelectorAll('a[href="#kontakt"][data-thema]').forEach(function(a){
    a.addEventListener('click', function(){
      var feld = document.getElementById('thema');
      if (feld && !feld.value) feld.value = a.dataset.thema;
    });
  });

  /* ── Formular ──
     SCHARF auf true stellen, sobald der Worker den Slug kennt:
       1. plattform/worker/recipients.js → 'lilly-stradner' eintragen
       2. Domain in ALLOWED_ORIGINS aufnehmen
       3. npx wrangler deploy
     Solange false, sagen wir ehrlich, dass nichts gesendet wird. */
  var SCHARF = false;
  var form = document.getElementById('form'),
      meldung = document.getElementById('meldung');

  form.addEventListener('submit', function(e){
    e.preventDefault();
    if (form.botcheck.value) return;
    if (!form.checkValidity()){
      meldung.style.color = '#F6C9C9';
      meldung.textContent = T.fehlt;
      return;
    }
    if (!SCHARF){
      meldung.style.color = '#C9B7A4';
      meldung.textContent = T.vorschau;
      return;
    }
    meldung.style.color = '#C9B7A4';
    meldung.textContent = T.moment;
    fetch('https://lechcode-api.nameless-waterfall-55e5.workers.dev/contact', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({
        site:'lilly-stradner',
        name: form.name.value, email: form.email.value,
        thema: form.thema.value, message: form.message.value
      })
    })
    .then(function(r){ return r.json(); })
    .then(function(d){
      meldung.style.color = d.ok ? '#7FD79E' : '#F6C9C9';
      meldung.textContent = d.meldung || (d.ok ? T.da : T.fehler);
      if (d.ok) form.reset();
    })
    .catch(function(){
      meldung.style.color = '#F6C9C9';
      meldung.textContent = T.offline;
    });
  });
})();
