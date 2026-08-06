#!/usr/bin/env python3
"""
Erzeugt en.html aus index.html.

Warum generiert: So ist strukturelle Gleichwertigkeit der beiden Sprach-
fassungen garantiert (I6). Jede Ersetzung wird hart geprueft — fehlt eine,
bricht das Skript ab, statt eine halb uebersetzte Seite zu schreiben.

Nach jeder Aenderung an index.html erneut laufen lassen:
    python3 gen-en.py
"""
import re
import sys
from pathlib import Path

W = Path(__file__).parent
quelle = (W / "index.html").read_text(encoding="utf-8")

# (deutsch, englisch) — der Reihe nach angewendet, jede muss vorkommen.
PAARE = [
    # ── Kopf ─────────────────────────────────────────────────────────────
    ('<html lang="de">', '<html lang="en">'),
    ('<!-- ENTFERNEN, sobald Impressum + Datenschutz vollstaendig sind und Lilly freigegeben hat -->',
     '<!-- ENTFERNEN, sobald Impressum + Datenschutz vollstaendig sind und Lilly freigegeben hat -->'),
    ('<title>Somatische Prozessbegleitung &amp; Breathwork | Lilly Stradner</title>',
     '<title>Somatic process facilitation &amp; breathwork | Lilly Stradner</title>'),
    ('content="Lilly Stradner begleitet Menschen somatisch aus Mustern, Körper- und Essensthemen heraus — mit Nervensystemarbeit und Conscious Connected Breathwork. Kostenloses Kennenlerngespräch."',
     'content="Lilly Stradner accompanies people somatically out of patterns, body and food struggles — with nervous system work and Conscious Connected Breathwork. Free introductory call."'),
    ('<meta property="og:description" content="Somatische Prozessbegleitung und Conscious Connected Breathwork. Transformation ist möglich.">',
     '<meta property="og:description" content="Somatic process facilitation and Conscious Connected Breathwork. Transformation is possible.">'),
    ('<meta property="og:locale" content="de_DE">', '<meta property="og:locale" content="en_GB">'),
    ('<meta property="og:url" content="https://lechcode.github.io/lilly-stradner-vorschau/">',
     '<meta property="og:url" content="https://lechcode.github.io/lilly-stradner-vorschau/en.html">'),

    # ── Sprachumschalter: aktiv ist jetzt EN ─────────────────────────────
    ('<a class="skip" href="#inhalt">Zum Inhalt springen</a>',
     '<a class="skip" href="#inhalt">Skip to content</a>'),
    ('    <span>Kapitel</span>', '    <span>Chapters</span>'),
    ('<nav class="sprache" aria-label="Sprache wählen">',
     '<nav class="sprache" aria-label="Choose language">'),
    ('<a href="index.html" aria-current="true" hreflang="de">',
     '<a href="index.html" hreflang="de">'),
    ('<a href="en.html" hreflang="en">',
     '<a href="en.html" aria-current="true" hreflang="en">'),

    # ── Seitenreiter + Navigation ────────────────────────────────────────
    ('<nav class="rail" aria-label="Kapitel">', '<nav class="rail" aria-label="Chapters">'),
    ('<a href="#ueber-mich"  data-titel="Über mich"><span class="sr">Über mich</span></a>',
     '<a href="#ueber-mich"  data-titel="About me"><span class="sr">About me</span></a>'),
    ('<a href="#arbeit"      data-titel="Meine Arbeit"><span class="sr">Meine Arbeit</span></a>',
     '<a href="#arbeit"      data-titel="My work"><span class="sr">My work</span></a>'),
    ('<a href="#einszueins"  data-titel="1:1-Begleitung"><span class="sr">1:1-Begleitung</span></a>',
     '<a href="#einszueins"  data-titel="One-to-one"><span class="sr">One-to-one</span></a>'),
    ('<a href="#gruppen"     data-titel="Gruppen"><span class="sr">Gruppen</span></a>',
     '<a href="#gruppen"     data-titel="Groups"><span class="sr">Groups</span></a>'),
    ('<a href="#community"   data-titel="Community"><span class="sr">Community</span></a>',
     '<a href="#community"   data-titel="Community"><span class="sr">Community</span></a>'),
    ('<a href="#offline"     data-titel="Offline"><span class="sr">Offline</span></a>',
     '<a href="#offline"     data-titel="In person"><span class="sr">In person</span></a>'),
    ('<a href="#shop"        data-titel="Aufnahmen"><span class="sr">Aufnahmen</span></a>',
     '<a href="#shop"        data-titel="Recordings"><span class="sr">Recordings</span></a>'),
    ('<a href="#kontakt"     data-titel="Kontakt"><span class="sr">Kontakt</span></a>',
     '<a href="#kontakt"     data-titel="Contact"><span class="sr">Contact</span></a>'),

    ('<li><a href="#ueber-mich"><span>01</span> Über mich</a></li>',
     '<li><a href="#ueber-mich"><span>01</span> About me</a></li>'),
    ('<li><a href="#arbeit"><span>02</span> Meine Arbeit</a></li>',
     '<li><a href="#arbeit"><span>02</span> My work</a></li>'),
    ('<li><a href="#einszueins"><span>03</span> 1:1-Begleitung</a></li>',
     '<li><a href="#einszueins"><span>03</span> One-to-one</a></li>'),
    ('<li><a href="#gruppen"><span>04</span> Gruppenbegleitungen</a></li>',
     '<li><a href="#gruppen"><span>04</span> Group journeys</a></li>'),
    ('<li><a href="#offline"><span>06</span> Offline</a></li>',
     '<li><a href="#offline"><span>06</span> In person</a></li>'),
    ('<li><a href="#shop"><span>07</span> Aufnahmen</a></li>',
     '<li><a href="#shop"><span>07</span> Recordings</a></li>'),
    ('<li><a href="#kontakt"><span>08</span> Kontakt</a></li>',
     '<li><a href="#kontakt"><span>08</span> Contact</a></li>'),

    # ── Hero ─────────────────────────────────────────────────────────────
    ('alt="Lilly vor einigen Jahren: dunkler Raum, abweisender Blick in die Kamera."',
     'alt="Lilly some years ago: a dark room, a closed-off look into the camera."'),
    ('<figcaption>2016</figcaption>', '<figcaption>2016</figcaption>'),
    ('alt="Lilly heute: im Grünen, offener Blick, ruhiges Lächeln."',
     'alt="Lilly today: outdoors in the green, open gaze, a calm smile."'),
    ('<figcaption>2026</figcaption>', '<figcaption>2026</figcaption>'),
    # Das &nbsp; gehoert HINTER den Mittelpunkt, sonst haengt er am Zeilenende.
    ('<p class="marke">Somatische Prozessbegleitung ·&nbsp;Breathwork</p>',
     '<p class="marke">Somatic process facilitation ·&nbsp;Breathwork</p>'),
    ('<h1>Transformation ist möglich.</h1>', '<h1>Transformation is possible.</h1>'),
    ("""      <p class="klarstellung">Zehn Jahre. Verändert hat sich nicht mein Körper — sondern dass ich
        mich nicht mehr verstecke.</p>

      <p>Ich begleite Menschen, bei denen es hakt — im Leben, im Körper oder im Essen.</p>""",
     """      <p class="klarstellung">Ten years. What changed is not my body — it is that I no longer
        hide.</p>

      <p>I accompany people for whom something is stuck — in life, in the body or around food.</p>"""),
    ('        Lass uns sprechen', '        Let us talk'),
    # data-thema muss mituebersetzt werden — sonst steht im englischen
    # Formular ein deutsches Thema (Leonardo, Runde 2).
    ('<a class="knopf" href="#kontakt" data-thema="Kennenlerngespräch">',
     '<a class="knopf" href="#kontakt" data-thema="Introductory call">'),

    # ── 01 · Über mich ───────────────────────────────────────────────────
    ('<p class="marke reveal">01 — Über mich</p>', '<p class="marke reveal">01 — About me</p>'),
    ('<h2 class="reveal lese">Ich weiß, wie es ist, sich selbst im Weg zu stehen.</h2>',
     '<h2 class="reveal lese">I know what it is like to stand in your own way.</h2>'),
    ("""      <strong>Kurz vorweg:</strong> In diesem Kapitel spreche ich offen über Essstörung, Gewalt und
      Suizidgedanken. Wenn dir das gerade zu nah ist, spring gern direkt
      <a href="#arbeit">zu meiner Arbeit</a>.""",
     """      <strong>Before you read on:</strong> in this chapter I speak openly about an eating
      disorder, abuse and suicidal thoughts. If that feels too close right now, please skip
      ahead <a href="#arbeit">to my work</a>."""),
    ("""      <p>Ich bin in einer Familie groß geworden, die von außen nach Friede, Freude, Eierkuchen
        aussah. Innen drin habe ich früh angefangen zu essen. Viel. Ich war als Kind schon dick,
        als Jugendliche sehr dick — und ich bin in einer Welt aufgewachsen, die dafür wenig
        Freundlichkeit übrig hat.</p>""",
     """      <p>I grew up in a family that looked perfectly fine from the outside. Inside, I started
        eating early. A lot. I was a heavy child and a very heavy teenager — and I grew up in a
        world that has little kindness to spare for that.</p>"""),
    ("""      <p>Ich habe mich selbst gehasst. Ich habe geglaubt, ich sei einfach nicht diszipliniert
        genug. Fast fünfundzwanzig Jahre lang.</p>""",
     """      <p>I hated myself. I believed I simply was not disciplined enough. For almost
        twenty-five years.</p>"""),
    ("""      <p>Dann trennten sich meine Eltern. Und dann starb mein Vater, plötzlich. Er war die
        einzige sichere Bindung, die ich hatte — der eine Mensch, bei dem ich nichts sein musste.</p>

      <p>Was danach kam, war nicht Trauer, wie man sie sich vorstellt. Es war zu viel, um es zu
        fühlen. Und irgendwo darunter fing etwas in mir an zu rufen. Ich habe lange gebraucht, um
        hinzuhören.</p>""",
     """      <p>Then my parents separated. And then my father died, suddenly. He was the only secure
        attachment I had — the one person around whom I did not have to be anything.</p>

      <p>What came after was not grief the way you picture it. It was too much to feel. And
        somewhere underneath, something in me began to call. It took me a long time to listen.</p>"""),
    ("""      <p>Ich bin dem Rufen gefolgt. Zuerst in Coachings zu emotionalem Essen, wo sich schnell viel
        löste. Dann tiefer.</p>""",
     """      <p>I followed that call. First into work on emotional eating, where a lot shifted quickly.
        Then deeper.</p>"""),
    ("""      <p>Auf diesem Weg habe ich mich an etwas erinnert, das mein System zwanzig Jahre lang
        weggeschlossen hatte: Ich wurde als Fünfjährige von meinem Onkel missbraucht. Eine
        dissoziative Amnesie hatte mir die Erinnerung genommen — den Schmerz nicht. Gesehen zu
        werden war für mich lebensgefährlich geworden. Das Essen war die Antwort meines Körpers
        darauf.</p>""",
     """      <p>Along the way I remembered something my system had locked away for twenty years: I was
        abused by my uncle when I was five. A dissociative amnesia had taken the memory from me —
        not the pain. Being seen had become life-threatening for me. Eating was my body's answer
        to that.</p>"""),
    ("""      <p>Dazwischen lagen Jahre, über die ich heute ohne Scham sprechen kann: Alkohol, mit dem ich
        überhaupt erst unter Menschen gehen konnte. Depressive Phasen. Zeiten, in denen ich nicht
        mehr leben wollte. Eine Beziehung, die fünf Jahre lang wehtat und aus der ich trotzdem
        nicht rauskam.</p>""",
     """      <p>In between lay years I can speak about without shame today: alcohol, without which I
        could not be around people at all. Depressive phases. Times when I no longer wanted to
        live. A relationship that hurt for five years and that I still could not leave.</p>"""),
    ("""      <p>Mit zwanzig habe ich über fünfzig Kilo abgenommen. Durch Hungern. Es hat nichts geheilt.
        Danach war ich genauso wenig zu Hause in mir wie vorher — nur dünner, mit zwei Operationen
        und einer panischen Angst, alles wieder zuzunehmen.</p>""",
     """      <p>At twenty I lost more than fifty kilos. By starving. It healed nothing. Afterwards I
        was just as little at home in myself as before — only thinner, with two operations and a
        panicked fear of gaining it all back.</p>"""),
    ("""      <p>Ein Teil davon war nicht einmal meins. Meine Großmutter hat im Krieg gehungert. Was ich
        für meine Maßlosigkeit hielt, war zu einem Stück ihr Überleben, weitergereicht durch zwei
        Generationen. Da bin ich über das Atmen drangekommen, nicht übers Nachdenken.</p>""",
     """      <p>Part of it was not even mine. My grandmother went hungry during the war. What I took
        for my own lack of restraint was in part her survival, handed down through two
        generations. I reached that through breathing, not through thinking.</p>"""),
    ('<blockquote>„Mein Körper war nie das Problem. Und ich war es auch nie."</blockquote>',
     '<blockquote>“My body was never the problem. And neither was I.”</blockquote>'),
    ("""    <p class="lese reveal">Das ist der Satz, um den sich alles dreht, was ich heute tue. Unser
      Körper ist nicht dumm und nicht undiszipliniert. Er hat immer einen Grund. Wenn wir lernen,
      ihm wieder zuzuhören, führt er uns zurück.</p>

    <p class="lese reveal"><strong>Und damit das klar ist:</strong> Du musst nichts Schlimmes
      erlebt haben, um hier richtig zu sein. Es reicht, dass etwas nicht stimmt und du es
      satt hast.</p>""",
     """    <p class="lese reveal">That sentence is what everything I do today turns around. Our body is
      not stupid and not undisciplined. It always has a reason. When we learn to listen to it
      again, it leads us back.</p>

    <p class="lese reveal"><strong>And to be clear:</strong> you do not need to have been through
      something terrible to belong here. It is enough that something is not right and that you
      have had enough of it.</p>"""),

    # ── 02 · Meine Arbeit ────────────────────────────────────────────────
    ('<p class="marke reveal">02 — Meine Arbeit</p>', '<p class="marke reveal">02 — My work</p>'),
    ("""<h2 class="reveal lese">Wir schauen an, womit du kompensierst. Und wir gehen dahin, wo es
      herkommt.</h2>""",
     """<h2 class="reveal lese">We look at what you compensate with. And we go to where it comes
      from.</h2>"""),
    ("""      <p>Wir verstehen zuerst auf der mentalen Ebene, was in dir passiert: warum du in bestimmten
        Situationen explodierst, warum du etwas seit Jahren nicht umgesetzt bekommst, welche Sätze
        du über dich glaubst. Und dann verlassen wir den Kopf — denn verstehen allein hat noch
        niemanden verändert.</p>""",
     """      <p>First we understand on a mental level what happens inside you: why you explode in
        certain situations, why something has not moved for years, which sentences you believe
        about yourself. And then we leave the head — because understanding alone has never
        changed anyone.</p>"""),
    ('<summary><b>01</b> Zurück in den Körper</summary>',
     '<summary><b>01</b> Back into the body</summary>'),
    ("""          <p>Erst einmal lernst du wieder zu spüren. Emotionen, Körperempfindungen, Hunger und
            Sättigung — all das, was viele von uns irgendwann abgestellt haben, weil es zu viel
            war.</p>
          <p>Dazu kommt die Arbeit mit deinem Nervensystem: verstehen, was es überhaupt ist, merken,
            in welchem Zustand du gerade bist, und im Alltag Stück für Stück regulieren lernen.
            Das ist die Grundlage. Ohne sie greift alles andere ins Leere.</p>""",
     """          <p>First you learn to feel again. Emotions, bodily sensations, hunger and fullness —
            all the things many of us switched off at some point because they were too much.</p>
          <p>Alongside that comes the work with your nervous system: understanding what it even
            is, noticing which state you are in, and learning to regulate step by step in daily
            life. This is the foundation. Without it, everything else falls flat.</p>"""),
    ('<summary><b>02</b> Aufarbeiten, was darunter liegt</summary>',
     '<summary><b>02</b> Working through what lies beneath</summary>'),
    ("""          <p>Hier gehen wir an die Ursprünge: somatische Anteilearbeit, somatische Schattenarbeit,
            Bindungsthemen, Conscious Connected Breathwork. Wir schauen uns deine Trigger an,
            verstehen, wie sie zusammenhängen, und holen hoch, was lange unten lag.</p>
          <p>Das ist der Teil, der sich manchmal unangenehm anfühlt. Und der Teil, der wirklich
            etwas bewegt.</p>""",
     """          <p>Here we go to the origins: somatic parts work, somatic shadow work, attachment
            themes, Conscious Connected Breathwork. We look at your triggers, understand how they
            connect, and bring up what has been down there a long time.</p>
          <p>This is the part that sometimes feels uncomfortable. And the part that actually
            moves something.</p>"""),
    ('<summary><b>03</b> Die Systeme mitdenken</summary>',
     '<summary><b>03</b> Keeping the systems in view</summary>'),
    ("""          <p>Wir leben in Patriarchat, Kapitalismus und Neokolonialismus. Wir können uns noch so
            gründlich anschauen und heilen — diese Systeme wirken weiter auf uns.</p>
          <p>Du kannst einmal erkennen, dass du dich nicht gut genug fühlst, obwohl es nicht stimmt.
            Und am nächsten Tag erzählt dir die Welt wieder das Gegenteil. Deshalb beziehe ich das
            von Anfang an mit ein: Wir lernen zu sehen, wo diese Prägungen im Alltag zugreifen —
            damit du dich nicht darin verlierst, sondern rausgehen kannst.</p>
          <p>Ich habe Internationale Beziehungen studiert. Aus dem Studium habe ich vor allem eines
            mitgenommen: Wie sehr wir geprägt werden, und wie viel Energie es kostet, das zu
            ignorieren.</p>""",
     """          <p>We live in patriarchy, capitalism and neocolonialism. We can look at ourselves and
            heal as thoroughly as we like — these systems keep acting on us.</p>
          <p>You can recognise once that you feel not good enough although it is not true. And the
            next day the world tells you the opposite again. That is why I include this from the
            start: we learn to see where these conditionings take hold in daily life — so that you
            do not lose yourself in them, but can step out.</p>
          <p>I studied International Relations. What I took from it above all is this: how deeply
            we are shaped, and how much energy it costs to ignore that.</p>"""),
    ('alt="Lilly sitzt mit beiden Händen auf dem Herzen, Augen geschlossen."',
     'alt="Lilly sitting with both hands on her heart, eyes closed."'),
    ('<h3>Somatische Arbeit</h3>', '<h3>Somatic work</h3>'),
    ("""        <p>Somatisch heißt: über den Körper. Nicht über das Gespräch allein. Wir arbeiten mit dem,
          was gerade in dir spürbar ist — Enge, Druck, Taubheit, Wärme — und folgen dem, statt es
          wegzudenken. Dein Körper hat die Erfahrungen gespeichert. Also ist er auch der Ort, an
          dem sie sich lösen können.</p>""",
     """        <p>Somatic means: through the body. Not through conversation alone. We work with what
          is noticeable in you right now — tightness, pressure, numbness, warmth — and follow it
          instead of thinking it away. Your body stored the experiences. So it is also the place
          where they can release.</p>"""),
    ("""        <p>Eine Atemtechnik ohne Pause zwischen Ein- und Ausatmen. Sie bringt dich in einen
          veränderten Bewusstseinszustand, in dem Dinge an die Oberfläche kommen dürfen, an die du
          im Alltag nicht herankommst. Ich habe darüber Zusammenhänge in mir gefunden, die ich mir
          vorher nicht hätte erklären können.</p>""",
     """        <p>A breathing technique with no pause between the in-breath and the out-breath. It
          brings you into an altered state of consciousness in which things are allowed to surface
          that you cannot reach in everyday life. Through it I found connections in myself I could
          not have explained before.</p>"""),
    ('<h3>Wie ich arbeite</h3>', '<h3>How I work</h3>'),
    ("""      <p>Ich bin nicht die, die vorne steht und dir erklärt, wie du zu sein hast. Ich teile meine
        Erfahrung, ich teile mein Wissen, und ich halte Raum. Ich lerne von den Menschen, die ich
        begleite, genauso viel wie sie von mir.</p>
      <p>Was mir dabei am wichtigsten ist: dass du gesehen wirst. In deinem Schmerz, in deinen
        Mustern, in allem. Weil genau darin etwas passiert, das allein nicht passieren kann.</p>""",
     """      <p>I am not the one standing at the front telling you how to be. I share my experience, I
        share my knowledge, and I hold space. I learn as much from the people I accompany as they
        learn from me.</p>
      <p>What matters most to me: that you are witnessed. In your pain, in your patterns, in all
        of it. Because exactly there something happens that cannot happen alone.</p>"""),

    # ── 03 · 1:1 ─────────────────────────────────────────────────────────
    ('<p class="marke reveal">03 — 1:1-Begleitung</p>',
     '<p class="marke reveal">03 — One-to-one</p>'),
    ('<h2 class="reveal lese">Gemeinsam, über einen längeren Zeitraum.</h2>',
     '<h2 class="reveal lese">Together, over a longer stretch of time.</h2>'),
    ("""        <p>Wir arbeiten online in Sessions, und zwischen den Sessions bin ich per WhatsApp für dich
          da — denn das Leben passiert nicht in den Terminen, sondern dazwischen.</p>
        <p>Es gibt zwei Wege zu mir. Der eine ist offen für alles, was gerade hakt: ein Verlust,
          ein Schicksalsschlag, Leistungsdruck, Prokrastination, Perfektionismus, Wut, die dich
          überrollt, Einsamkeit, Ängste vor Menschen. Der andere ist für Körper- und Essensthemen —
          da kenne ich mich aus, weil ich selbst durchgegangen bin.</p>
        <p>Wie lange wir zusammenarbeiten und wie das genau aussieht, entscheiden wir nicht vorab
          im Baukasten, sondern gemeinsam im Gespräch.</p>""",
     """        <p>We work online in sessions, and between the sessions I am there for you on WhatsApp —
          because life does not happen in the appointments, it happens in between.</p>
        <p>There are two ways in. One is open to whatever is stuck right now: a loss, a blow of
          fate, pressure to perform, procrastination, perfectionism, anger that overwhelms you,
          loneliness, fear of other people. The other is for body and food themes — I know my way
          around there, because I went through it myself.</p>
        <p>How long we work together and what exactly it looks like is not decided in advance from
          a menu, but together in conversation.</p>"""),
    ('          Kostenloses Kennenlernen, 30 Minuten',
     '          Free introductory call, 30 minutes'),
    ('<a class="knopf" href="#kontakt" data-thema="Kennenlerngespräch">',
     '<a class="knopf" href="#kontakt" data-thema="Introductory call">'),
    ("""        <p style="font-size:var(--klein); color:var(--daemmer)">Wir schauen in Ruhe, ob es passt —
          und was es kostet, sage ich dir dort offen.</p>""",
     """        <p style="font-size:var(--klein); color:var(--daemmer)">We take our time to see whether it
          fits — and I will tell you openly there what it costs.</p>"""),
    ('alt="Laptop mit laufender Online-Session, daneben eine brennende Kerze."',
     'alt="A laptop with an online session running, a burning candle beside it."'),
    ('<figcaption>Die meisten Begleitungen laufen online.</figcaption>',
     '<figcaption>Most of this work happens online.</figcaption>'),
    ("""      <strong>Für wen das nicht das Richtige ist:</strong> Ich bin keine Therapeutin und mache keine
      Psychotherapie. Wenn du gerade in einer akuten Krise steckst, in einer psychischen Erkrankung,
      die Behandlung braucht, oder in einer akuten Essstörung, bist du bei einer Ärztin oder einem
      Psychotherapeuten besser aufgehoben. Sag mir das gern im Gespräch — ich bin da ehrlich zu dir.""",
     """      <strong>Who this is not right for:</strong> I am not a therapist and I do not practise
      psychotherapy. If you are currently in an acute crisis, in a mental illness that needs
      treatment, or in an acute eating disorder, you are in better hands with a doctor or a
      psychotherapist. Do tell me in our call — I will be honest with you about it."""),

    # ── 04 · Gruppen ─────────────────────────────────────────────────────
    ('<p class="marke reveal">04 — Gruppenbegleitungen</p>',
     '<p class="marke reveal">04 — Group journeys</p>'),
    ('<h2 class="reveal lese">In der Gruppe geht etwas, das allein nicht geht.</h2>',
     '<h2 class="reveal lese">In a group, something works that cannot work alone.</h2>'),
    ('alt="Ein Retreat-Raum, mehrere Menschen liegen auf Decken während einer Session."',
     'alt="A retreat room, several people lying on blankets during a session."'),
    ("""        <p>Mein erstes Gruppenmentoring lief mit somatischer Arbeit. Das nächste bekommt deutlich
          mehr Breathwork — ich arbeite gerade daran, wie es genau aussehen soll.</p>
        <p>Wenn du dabei sein möchtest, trag dich auf die Warteliste ein. Du hörst von mir, sobald
          es losgeht, und bist vor allen anderen dran.</p>""",
     """        <p>My first group mentoring ran on somatic work. The next one will have considerably
          more breathwork — I am working out exactly how it should look.</p>
        <p>If you would like to be there, put your name on the waiting list. You will hear from me
          as soon as it starts, ahead of everyone else.</p>"""),
    ('<a class="knopf-leise" href="#kontakt" data-thema="Warteliste Gruppenmentoring">Auf die Warteliste',
     '<a class="knopf-leise" href="#kontakt" data-thema="Waiting list, group mentoring">Join the waiting list'),

    # ── 05 · Community ───────────────────────────────────────────────────
    ('<p class="marke reveal">05 — Community</p>', '<p class="marke reveal">05 — Community</p>'),
    ('<h2 class="reveal lese">Heilung geschieht nicht allein.</h2>',
     '<h2 class="reveal lese">Healing does not happen alone.</h2>'),
    ("""        <p>Ich habe jahrelang versucht, alles mit mir selbst auszumachen. Allein zu heilen, online
          zu heilen, niemandem zur Last zu fallen. Es funktioniert nicht. Verbindung ist kein
          Extra — sie ist Teil der Arbeit.</p>
        <p>Deshalb baue ich eine Community auf. Einmal im Monat halte ich eine Breathwork-Session,
          einmal im Monat eine somatische Session. Die Termine stimmen wir gemeinsam ab. Dazu gibt
          es einen Ort für Fragen und dafür, sich miteinander auszutauschen.</p>
        <p>Am Anfang läuft das über WhatsApp — unkompliziert, ohne dass du dich irgendwo anmelden
          musst.</p>""",
     """        <p>For years I tried to sort everything out with myself. To heal alone, to heal online,
          to be a burden to no one. It does not work. Connection is not an extra — it is part of
          the work.</p>
        <p>That is why I am building a community. Once a month I hold a breathwork session, once a
          month a somatic session. We agree the dates together. Alongside that there is a place
          for questions and for being in exchange with each other.</p>
        <p>To begin with this runs on WhatsApp — uncomplicated, with nothing to sign up for.</p>"""),
    ('<a class="knopf-leise" href="#kontakt" data-thema="Community">Dazukommen',
     '<a class="knopf-leise" href="#kontakt" data-thema="Community">Come along'),
    ('alt="Lilly umarmt eine andere Person, beide mit geschlossenen Augen."',
     'alt="Lilly embracing another person, both with their eyes closed."'),

    # ── 06 · Offline ─────────────────────────────────────────────────────
    ('<p class="marke reveal">06 — Offline</p>', '<p class="marke reveal">06 — In person</p>'),
    ('<h2 class="reveal lese">Am liebsten im selben Raum.</h2>',
     '<h2 class="reveal lese">Best of all, in the same room.</h2>'),
    ('alt="Blick von oben in einen vorbereiteten Retreat-Raum mit Matten und Klangschalen."',
     'alt="Looking down into a prepared retreat room with mats and singing bowls."'),
    ('<figcaption>Aus vergangenen Retreats und Gruppensessions.</figcaption>',
     '<figcaption>From past retreats and group sessions.</figcaption>'),
    ("""        <p>Offline zu arbeiten ist das Schönste — im selben Raum zu sitzen, gemeinsam zu atmen,
          sich wirklich zu begegnen.</p>
        <p>Ehrlich gesagt geht es nur nicht immer. Im Winter bin ich meistens weiter weg, im Sommer
          bin ich in Deutschland, oft in Bielefeld, aber viel unterwegs.</p>
        <p>Wenn wir zufällig am selben Ort sind: Frag mich einfach. Einzelsessions gehen dann, vor
          allem Breathwork, aber auch somatische Arbeit. Und wenn du eine Gruppe zusammenbringst,
          komme ich gern zu euch.</p>""",
     """        <p>Working in person is the loveliest thing — sitting in the same room, breathing
          together, really meeting each other.</p>
        <p>Honestly, it is just not always possible. In winter I am usually further away; in summer
          I am in Germany, often in Bielefeld, but travelling a lot.</p>
        <p>If we happen to be in the same place: just ask me. Single sessions work then, breathwork
          above all, but somatic work too. And if you bring a group together, I will gladly come
          to you.</p>"""),
    ('<a class="knopf-leise" href="#kontakt" data-thema="Offline-Session">Anfragen',
     '<a class="knopf-leise" href="#kontakt" data-thema="In-person session">Get in touch'),

    # ── 07 · Aufnahmen ───────────────────────────────────────────────────
    ('<p class="marke reveal">07 — Aufnahmen</p>', '<p class="marke reveal">07 — Recordings</p>'),
    ('<h2 class="reveal lese">Zum Ausprobieren, wann immer du willst.</h2>',
     '<h2 class="reveal lese">To try out, whenever you like.</h2>'),
    ("""    <p class="lese reveal">Drei Aufnahmen, die du dir in Ruhe holen kannst — ohne Termin, ohne
      Verpflichtung. Ein guter Weg, um zu spüren, ob meine Art zu arbeiten dir liegt.</p>""",
     """    <p class="lese reveal">Three recordings you can take in your own time — no appointment, no
      commitment. A good way to sense whether my way of working suits you.</p>"""),
    ('<h3>Somatisches Yin Yoga</h3>', '<h3>Somatic yin yoga</h3>'),
    ('<p>Lange gehaltene Haltungen, in denen du dir selbst begegnest. Ruhig, langsam, tief.</p>',
     '<p>Long-held postures in which you meet yourself. Quiet, slow, deep.</p>'),
    ('<p>Eine geführte Conscious-Connected-Breathwork-Session zum Mitatmen von zu Hause.</p>',
     '<p>A guided Conscious Connected Breathwork session to breathe along with from home.</p>'),
    ('<h3>Somatische Session</h3>', '<h3>Somatic session</h3>'),
    ('<p>Eine begleitete Einheit, in der du übst, deinem Körper wieder zuzuhören.</p>',
     '<p>An accompanied session in which you practise listening to your body again.</p>'),
    ("""<a class="knopf-leise" href="#kontakt" data-thema="Aufnahmen">Schreib mir,
      welche dich interessiert""",
     """<a class="knopf-leise" href="#kontakt" data-thema="Recordings">Tell me which one
      interests you"""),
    ("""<p class="reveal" style="font-size:var(--klein); color:var(--daemmer)">Später kommt hier das
      Gruppenmentoring als Kurs dazu.</p>""",
     """<p class="reveal" style="font-size:var(--klein); color:var(--daemmer)">The group mentoring
      will join them here later as a course.</p>"""),

    # ── 08 · Werdegang ───────────────────────────────────────────────────
    ('<p class="marke reveal">Woher ich komme</p>', '<p class="marke reveal">Where I come from</p>'),
    ('<h2 class="reveal lese">Ausgebildet — und selbst durchgegangen.</h2>',
     '<h2 class="reveal lese">Trained — and lived through it myself.</h2>'),
    ('<li>Trauma-informierte Embodiment-Coach <span class="titel-hinweis">(so heißt die Ausbildung)</span></li>',
     '<li>Trauma-informed Embodiment Coach <span class="titel-hinweis">(the name of the training)</span></li>'),
    ('<li>200 Stunden Multistyle-Yoga-Ausbildung, dazu Yin Yoga</li>',
     '<li>200-hour multistyle yoga teacher training, plus yin yoga</li>'),
    ('<li>Reiki Grad 1, 2a und 2b</li>', '<li>Reiki levels 1, 2a and 2b</li>'),
    ('<li>Studium der Internationalen Beziehungen</li>',
     '<li>Degree in International Relations</li>'),
    ("""        <p>Für alle Ausbildungen habe ich Zertifikate. Wichtiger ist mir aber etwas anderes: Ich
          schicke dich nirgendwo hin, wo ich nicht selbst war.</p>""",
     """        <p>I hold certificates for all of these trainings. But something else matters more to
          me: I will not send you anywhere I have not been myself.</p>"""),
    ('alt="Lilly lacht mit geschlossenen Augen, freigestellt."',
     'alt="Lilly laughing with her eyes closed, cut out from the background."'),
    ('<h3>Wenn es gerade akut ist</h3>', '<h3>If things are acute right now</h3>'),
    ("""      <p>Meine Arbeit ersetzt keine Psychotherapie und keine ärztliche Behandlung. Wenn es dir
        gerade sehr schlecht geht, wende dich bitte an Menschen, die rund um die Uhr für dich
        da sind:</p>""",
     """      <p>My work replaces neither psychotherapy nor medical treatment. If you are in a very bad
        place right now, please turn to people who are there for you around the clock. These are
        German services — if you are elsewhere, please look up the helpline for your country:</p>"""),
    ("""        <li><b>Telefonseelsorge</b> — <a href="tel:08001110111">0800 111 0 111</a> und
          <a href="tel:08001110222">0800 111 0 222</a>, kostenlos, Tag und Nacht</li>
        <li><b>Bundesweites Info-Telefon Depression</b> — <a href="tel:08003344533">0800 33 44 533</a></li>
        <li><b>Essstörungen</b> — Beratung der BZgA: <a href="tel:022189920411">0221 89 20 411</a></li>
        <li>Im Notfall: <b>112</b> oder die nächste psychiatrische Klinik</li>""",
     """        <li><b>Telefonseelsorge</b> (crisis line) — <a href="tel:08001110111">0800 111 0 111</a>
          and <a href="tel:08001110222">0800 111 0 222</a>, free, day and night</li>
        <li><b>National depression helpline</b> — <a href="tel:08003344533">0800 33 44 533</a></li>
        <li><b>Eating disorders</b> — BZgA counselling: <a href="tel:022189920411">0221 89 20 411</a></li>
        <li>In an emergency: <b>112</b> or the nearest psychiatric hospital</li>"""),

    # ── Kontakt ──────────────────────────────────────────────────────────
    ('<p class="marke reveal">08 — Kontakt</p>', '<p class="marke reveal">08 — Contact</p>'),
    ('<h2 class="reveal lese">Schreib mir.</h2>', '<h2 class="reveal lese">Write to me.</h2>'),
    ("""    <p class="lese reveal">Egal ob Kennenlerngespräch, Warteliste, Community oder eine der
      Aufnahmen — sag mir einfach, worum es geht. Ich lese jede Nachricht selbst und melde mich
      innerhalb von zwei Werktagen bei dir.</p>""",
     """    <p class="lese reveal">Whether it is an introductory call, the waiting list, the community
      or one of the recordings — just tell me what it is about. I read every message myself and
      will get back to you within two working days.</p>"""),
    ('<label for="name">Wie heißt du?</label>', '<label for="name">What is your name?</label>'),
    ('<label for="email">Deine E-Mail-Adresse</label>',
     '<label for="email">Your email address</label>'),
    ('<label for="thema">Worum geht es?</label>', '<label for="thema">What is it about?</label>'),
    ('placeholder="Kennenlerngespräch, Warteliste, Community …"',
     'placeholder="Introductory call, waiting list, community …"'),
    ('<label for="nachricht">Magst du kurz sagen, was dich herführt? <span class="freiwillig">freiwillig</span></label>',
     '<label for="nachricht">Would you like to say briefly what brings you here? <span class="freiwillig">optional</span></label>'),
    ('placeholder="Ein Satz reicht. Oder lass es leer — wir sprechen ja."',
     'placeholder="One sentence is enough. Or leave it — we will talk anyway."'),
    ('        Bitte leer lassen <input type="text" name="botcheck" tabindex="-1" autocomplete="off">',
     '        Please leave empty <input type="text" name="botcheck" tabindex="-1" autocomplete="off">'),
    ('        Abschicken', '        Send'),

    # ── Fuss ─────────────────────────────────────────────────────────────
    ('<nav class="fuss-links" aria-label="Rechtliches">',
     '<nav class="fuss-links" aria-label="Legal">'),
    ("""        <a href="impressum.html">Impressum</a>
        <a href="agb.html">AGB</a>
        <a href="datenschutz.html">Datenschutz</a>
        <a href="en.html">English version</a>""",
     """        <a href="impressum-en.html">Legal notice</a>
        <a href="agb-en.html">Terms</a>
        <a href="datenschutz-en.html">Privacy</a>
        <a href="index.html">Deutsche Fassung</a>"""),
    ("""    <p class="handschrift">Handgebaut in Landsberg am Lech. Keine Cookies, keine Tracker,
      Schriften liegen auf diesem Server.</p>""",
     """    <p class="handschrift">Handmade in Landsberg am Lech, Germany. No cookies, no trackers,
      fonts served from this server.</p>"""),
    # ── Runde 2: Zitat, Systeme-Saeule, Körper &amp; Essen, zweiter Weg ──
    ('<blockquote>„Nichts daran war undiszipliniert oder dumm. Es hatte einen Grund."</blockquote>',
     '<blockquote>“None of it was undisciplined or stupid. It had a reason.”</blockquote>'),
    ("""          <h3>Wenn es um Körper und Essen geht</h3>
          <p>Wenn deine Essstörung Vergangenheit ist und trotzdem etwas geblieben ist — das
            Rechnen, die Scham, der Blick in jede Scheibe — dann bist du hier richtig. Es muss
            nicht akut sein. Es reicht, dass es dich müde macht.</p>""",
     """          <h3>When it is about body and food</h3>
          <p>If your eating disorder is in the past and something stayed anyway — the counting,
            the shame, the glance into every shop window — then you are in the right place. It
            does not have to be acute. It is enough that it wears you out.</p>"""),
    ("""      <p class="zweitweg">Lieber direkt per E-Mail? <b>Adresse folgt</b> — bis dahin geht es
        nur über dieses Formular.</p>""",
     """      <p class="zweitweg">Prefer email? <b>Address to follow</b> — until then this form is the
        only way.</p>"""),
    ("""          Podcast <b>Adresse fehlt</b>""", """          Podcast <b>address missing</b>"""),
    ("""          Instagram DE <b>fehlt</b>""", """          Instagram DE <b>missing</b>"""),
    ("""          Instagram EN <b>fehlt</b>""", """          Instagram EN <b>missing</b>"""),
    # ── Runde 3: gleichwertiger Block fuer den generellen Weg, Systeme sichtbar ──
    ("""          <h3>Wenn es im Leben hakt</h3>
          <p>Wenn du funktionierst und trotzdem müde bist. Wenn du Menschen anschreist, die du
            liebst, und dich danach dafür hasst. Wenn ein Verlust dich umgeworfen hat und alle
            denken, du seist längst darüber hinweg. Wenn du genau weißt, was du tun müsstest, und
            es trotzdem nicht tust. Dafür braucht es keinen Namen und keine Diagnose.</p>""",
     """          <h3>When life is stuck</h3>
          <p>When you function and are tired anyway. When you shout at people you love and hate
            yourself for it afterwards. When a loss knocked you over and everyone assumes you are
            long past it. When you know exactly what you should do and still do not do it. None of
            that needs a name or a diagnosis.</p>"""),
    ("""      <p>Und wir denken mit, in welchen Systemen das alles passiert. Du kannst einmal erkennen,
        dass du nicht zu wenig bist — und am nächsten Tag erzählt dir die Welt das Gegenteil.</p>""",
     """      <p>And we keep in view which systems all of this happens in. You can recognise once that
        you are not too little — and the next day the world tells you the opposite.</p>"""),
]

s = quelle
fehlend = []
for de, en in PAARE:
    if de not in s:
        fehlend.append(de[:80])
        continue
    s = s.replace(de, en, 1)

if fehlend:
    print("ABBRUCH — diese Vorlagen wurden in index.html nicht gefunden:\n", file=sys.stderr)
    for f in fehlend:
        print("  ·", f.replace("\n", " ⏎ "), file=sys.stderr)
    sys.exit(1)

(W / "en.html").write_text(s, encoding="utf-8")

# Gegenprobe: sichtbarer Text darf keine deutschen Restwoerter mehr enthalten.
sichtbar = re.sub(r"<!--.*?-->", "", s, flags=re.S)
sichtbar = re.sub(r"<(script|style)\b.*?</\1>", "", sichtbar, flags=re.S)
sichtbar = re.sub(r"<[^>]+>", " ", sichtbar)
VERDAECHTIG = ["ich ", "und ", "nicht ", "über ", "für ", "mich", "dich ",
               "Körper", "Arbeit", "Menschen", "wir ", "dass "]
treffer = sorted({w for w in VERDAECHTIG if w in sichtbar})
print(f"en.html geschrieben · {len(s)} Zeichen · {len(PAARE)} Ersetzungen")
if treffer:
    print("⚠ moeglicher deutscher Resttext:", treffer)
else:
    print("✓ kein deutscher Resttext im sichtbaren Bereich")
