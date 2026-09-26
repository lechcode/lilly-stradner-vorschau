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
    /* Kopfleiste liegt dann auf Bordeaux — CSS schaltet sie hell */
    document.documentElement.classList.toggle('nav-offen', offen);
    /* Tastatur: Seite dahinter ist bei offenem Menue nicht erreichbar,
       der Fokus springt auf den ersten Punkt (aus dem Parallel-Commit
       731d407 uebernommen, 26.09.). */
    document.querySelectorAll('main, footer, .rail').forEach(function(el){ el.inert = offen; });
    /* Kurz warten: solange das Menue noch visibility:hidden hat, ignoriert
       der Browser focus() stillschweigend (rAF war dafuer zu frueh). */
    if (offen) setTimeout(function(){ nav.querySelector('a').focus(); }, 60);
  }
  knopf.addEventListener('click', function(){
    navSetzen(nav.dataset.offen !== 'true');
  });
  /* Kennenlernen/Sprache in der Kopfleiste schliessen ein offenes Menue */
  document.querySelectorAll('.kopf a').forEach(function(a){
    a.addEventListener('click', function(){ if (nav.dataset.offen === 'true') navSetzen(false); });
  });
  nav.addEventListener('click', function(e){
    var link = e.target.closest('a');
    if (link){
      navSetzen(false);
      /* Fokus mitnehmen, sonst bleibt er nach dem Sprung oben im Kopf */
      var ziel = document.querySelector(link.getAttribute('href'));
      if (ziel){ ziel.setAttribute('tabindex', '-1'); ziel.focus({preventScroll:true}); }
    }
  });
  document.addEventListener('keydown', function(e){
    if (nav.dataset.offen !== 'true') return;
    if (e.key === 'Escape'){ navSetzen(false); knopf.focus(); }
    /* Fokus-Falle: Tab laeuft nur zwischen Kopfleiste und Menue im Kreis */
    if (e.key === 'Tab'){
      var punkte = Array.from(document.querySelectorAll('.kopf a, .kopf button, #nav a')).filter(function(el){
        var css = getComputedStyle(el);
        return el.getClientRects().length && css.visibility !== 'hidden' && css.opacity !== '0';
      });
      var erster = punkte[0], letzter = punkte[punkte.length - 1];
      if (e.shiftKey && document.activeElement === erster){ e.preventDefault(); letzter.focus(); }
      else if (!e.shiftKey && document.activeElement === letzter){ e.preventDefault(); erster.focus(); }
    }
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

  /* ── Methode: interaktives Modell (Runde 2) ──
     Welches Feld getroffen wurde, wird aus der Geometrie berechnet:
     Die Flaechen sind Masken, und Masken zaehlen beim Klicken nicht mit.
     Mittelpunkte und Radius muessen zu den <circle> in index.html passen. */
  var venn = document.querySelector('.venn');
  if (venn){
    var KREISE = [[215,210],[385,210],[300,357]], RADIUS = 165;
    var textBox = document.getElementById('methode-text');
    var lichter = venn.querySelectorAll('.lichter rect');
    var felder  = venn.querySelectorAll('.feld');
    var texte   = textBox.querySelectorAll('.feld-text');

    var feldAn = function(evt){
      var ctm = venn.getScreenCTM();
      if (!ctm) return '';
      var pt = venn.createSVGPoint();
      pt.x = evt.clientX; pt.y = evt.clientY;
      pt = pt.matrixTransform(ctm.inverse());
      var id = '';
      KREISE.forEach(function(k, i){
        var dx = pt.x - k[0], dy = pt.y - k[1];
        if (dx*dx + dy*dy <= RADIUS*RADIUS) id += (i + 1);
      });
      return id;
    };
    var markieren = function(klasse, id){
      lichter.forEach(function(r){ r.classList.toggle(klasse, r.dataset.feld === id); });
    };
    var waehlen = function(id, scrollen){
      if (!id) return;
      markieren('aktiv', id);
      felder.forEach(function(f){ f.setAttribute('aria-pressed', f.dataset.feld === id ? 'true' : 'false'); });
      texte.forEach(function(t){ t.classList.toggle('zeigen', t.dataset.feld === id); });
      textBox.classList.add('gewaehlt');
      /* Am Handy steht der Text UNTER dem Modell — einmal sanft hinschieben,
         sonst merkt man nicht, dass sich etwas getan hat. */
      if (scrollen && window.innerWidth < 900){
        var oben = textBox.getBoundingClientRect().top;
        if (oben > window.innerHeight * 0.7){
          textBox.scrollIntoView({behavior: ruhig ? 'auto' : 'smooth', block:'center'});
        }
      }
    };

    /* Das Fundament ist vorgewaehlt: So sieht man sofort, dass hier
       etwas zu entdecken ist, statt auf ein leeres Feld zu schauen. */
    waehlen('1', false);

    venn.addEventListener('click', function(e){ waehlen(feldAn(e), true); });
    venn.addEventListener('pointermove', function(e){
      if (e.pointerType === 'mouse') markieren('hover', feldAn(e));
    });
    venn.addEventListener('pointerleave', function(){ markieren('hover', ''); });
    felder.forEach(function(f){
      f.addEventListener('keydown', function(e){
        if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); waehlen(f.dataset.feld, false); }
      });
      f.addEventListener('focus', function(){ markieren('hover', f.dataset.feld); });
      f.addEventListener('blur',  function(){ markieren('hover', ''); });
    });
  }

  /* ── Kennenlernen-Knopf am Handy (Runde 2) ──
     Unter 640px schwebt er unten, sobald der Hero verlassen ist, und
     macht Platz, wenn das Formular im Bild ist. Die Klasse wirkt nur
     dort (CSS) — auf breiten Schirmen sitzt er fest in der Kopfleiste. */
  var hero = document.querySelector('.hero'),
      kontakt = document.getElementById('kontakt'),
      fuss = document.querySelector('footer');
  function ctaPruefen(){
    var nachHero = hero ? hero.getBoundingClientRect().bottom < window.innerHeight * 0.35 : true;
    var hoehe = window.innerHeight;
    var imKontakt = kontakt && kontakt.getBoundingClientRect().top < hoehe * 0.8;
    var imFuss = fuss && fuss.getBoundingClientRect().top < hoehe;
    document.body.classList.toggle('cta-zeigen', nachHero && !imKontakt && !imFuss);
  }
  window.addEventListener('scroll', ctaPruefen, {passive:true});
  window.addEventListener('resize', ctaPruefen);
  ctaPruefen();

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
