#!/usr/bin/env python3
"""
Erzeugt en.html aus index.html.

Warum generiert: So ist strukturelle Gleichwertigkeit der beiden Sprach-
fassungen garantiert (I6). Jede Ersetzung wird hart geprueft — fehlt eine,
bricht das Skript ab, statt eine halb uebersetzte Seite zu schreiben.

Runde 2 (25.09.2026): komplett neu auf Lillys eigene Texte aus dem PDF
„Website Anpassungen". Das Gruppenmentoring (03b) gibt es laut Lilly NUR
auf Deutsch — alles zwischen <!--nur-de--> und <!--/nur-de--> faellt raus.

Nach jeder Aenderung an index.html erneut laufen lassen:
    python3 gen-en.py
"""
import re
import sys
from pathlib import Path

W = Path(__file__).parent
quelle = (W / "index.html").read_text(encoding="utf-8")

# Nur-deutsche Bloecke heraustrennen (inkl. Menuepunkt 03b)
s, n = re.subn(r"<!--nur-de-->.*?<!--/nur-de-->\n?", "", quelle, flags=re.S)
if n < 2:
    sys.exit(f"ABBRUCH: erwartet mind. 2 nur-de-Bloecke, gefunden {n}")

# Kommen mehrfach vor — ueberall ersetzen (mind. einmal muss es sie geben).
ALLE = [
    ('data-thema="Kennenlerncall"', 'data-thema="Introductory call"'),
    ('>Unverbindlich kennenlernen', '>Get to know me, no strings attached'),
    ('aria-label="Kapitel"', 'aria-label="Chapters"'),
]

# (deutsch, englisch) — der Reihe nach angewendet, jede muss vorkommen.
PAARE = [
    # ── Kopf ─────────────────────────────────────────────────────────────
    ('<html lang="de">', '<html lang="en">'),
    ('<title>Somatische Prozessbegleitung &amp; Atemarbeit | Lilly Stradner</title>',
     '<title>Somatic process facilitation &amp; breathwork | Lilly Stradner</title>'),
    ('content="Lilly Stradner begleitet Menschen hin zu einer liebevollen Beziehung zu sich selbst und ihrem Körper — mit somatischer Arbeit, Nervensystemarbeit und Atemarbeit. Unverbindlicher Kennenlerncall."',
     'content="Lilly Stradner accompanies people towards a loving relationship with themselves and their body — through somatic work, nervous system work and breathwork. Free, no-strings introductory call."'),
    ('<meta property="og:description" content="Somatische Prozessbegleitung &amp; Atemarbeit. Transformation ist möglich.">',
     '<meta property="og:description" content="Somatic process facilitation &amp; breathwork. Transformation is possible.">'),
    ('<meta property="og:locale" content="de_DE">', '<meta property="og:locale" content="en_GB">'),
    ('<meta property="og:url" content="https://lechcode.github.io/lilly-stradner-vorschau/">',
     '<meta property="og:url" content="https://lechcode.github.io/lilly-stradner-vorschau/en.html">'),

    ('<a class="skip" href="#inhalt">Zum Inhalt springen</a>',
     '<a class="skip" href="#inhalt">Skip to content</a>'),
    ('    <span>Menü</span>', '    <span>Menu</span>'),
    ('<nav class="sprache" aria-label="Sprache wählen">',
     '<nav class="sprache" aria-label="Choose language">'),
    ('<a href="index.html" aria-current="true" hreflang="de">',
     '<a href="index.html" hreflang="de">'),
    ('<a href="en.html" hreflang="en">',
     '<a href="en.html" aria-current="true" hreflang="en">'),

    # ── Seitenreiter + Menue ─────────────────────────────────────────────
    ('data-titel="Über mich"><span class="sr">Über mich</span>',
     'data-titel="About me"><span class="sr">About me</span>'),
    ('data-titel="Meine Arbeit"><span class="sr">Meine Arbeit</span>',
     'data-titel="My work"><span class="sr">My work</span>'),
    ('data-titel="Online-Begleitungen"><span class="sr">Online-Begleitungen</span>',
     'data-titel="Online journeys"><span class="sr">Online journeys</span>'),
    ('data-titel="Online-Community"><span class="sr">Online-Community</span>',
     'data-titel="Online community"><span class="sr">Online community</span>'),
    ('data-titel="Offline &amp; Kooperationen"><span class="sr">Offline &amp; Kooperationen</span>',
     'data-titel="In person &amp; collaborations"><span class="sr">In person &amp; collaborations</span>'),
    ('data-titel="Kontakt"><span class="sr">Kontakt</span>',
     'data-titel="Contact"><span class="sr">Contact</span>'),
    ('<span>01</span> Über mich</a>', '<span>01</span> About me</a>'),
    ('<span>02</span> Meine Arbeit</a>', '<span>02</span> My work</a>'),
    ('<span>03</span> Online-Begleitungen</a>', '<span>03</span> Online journeys</a>'),
    ('<span>03a</span> 1:1-Begleitung</a>', '<span>03a</span> One-to-one journey</a>'),
    ('<span>04</span> Online-Community</a>', '<span>04</span> Online community</a>'),
    ('<span>05</span> Offline-Angebote &amp; Kooperationen</a>',
     '<span>05</span> In person &amp; collaborations</a>'),
    ('<span>→</span> Kontakt &amp; Kennenlerncall</a>',
     '<span>→</span> Contact &amp; introductory call</a>'),

    # ── Hero ─────────────────────────────────────────────────────────────
    ('alt="Lilly vor zehn Jahren in einer Höhle: weißes Shirt, Haare hochgesteckt, vorsichtiges Lächeln."',
     'alt="Lilly ten years ago in a cave: white T-shirt, hair tied up, a cautious smile."'),
    ('alt="Lilly heute am Seeufer unter einer Weide: braunes Top, tätowierter Arm, ruhiges Lächeln."',
     'alt="Lilly today on a lakeshore under a willow: brown top, tattooed arm, a calm smile."'),
    ('<h1>Transformation ist möglich.</h1>', '<h1>Transformation is possible.</h1>'),
    ('Und die Grundlage dafür: eine gesunde Beziehung zu dir selbst.',
     'And the foundation for it: a healthy relationship with yourself.'),
    ('<p class="zeile">Somatische Prozessbegleitung &amp; Atemarbeit</p>',
     '<p class="zeile">Somatic process facilitation &amp; breathwork</p>'),
    ('<p class="kern">Jahrelang habe ich mich und meinen Körper gehasst. Heute weiß ich: <em>Wir waren nie das wirkliche Problem!</em></p>',
     '<p class="kern">For years I hated myself and my body. Today I know: <em>we were never the real problem!</em></p>'),
    ('Genau deshalb begleite ich Menschen hin zu einer liebevollen Beziehung zu sich selbst und ihrem Körper ~ damit von hier aus alles andere wachsen kann.',
     'That is exactly why I accompany people towards a loving relationship with themselves and their body ~ so that everything else can grow from there.'),
    ('          Erfahre mehr über mich und meine Arbeit\n', '          Learn more about me and my work\n'),
    ('>Oder lern mich unverbindlich kennen</a>', '>Or get to know me, no strings attached</a>'),

    # ── 01 · Über mich ───────────────────────────────────────────────────
    ('<p class="marke">01 — Über mich</p>', '<p class="marke">01 — About me</p>'),
    ('<strong>Kurz vorweg:</strong> In diesem Kapitel spreche ich offen über Essstörung, Suizidgedanken und sexuelle Gewalt. Wenn dir das gerade zu nah geht, springe hier gern direkt zu <a href="#arbeit">meiner Arbeit</a>.',
     '<strong>Before you read on:</strong> in this chapter I speak openly about an eating disorder, suicidal thoughts and sexual violence. If that feels too close right now, feel free to skip straight to <a href="#arbeit">my work</a>.'),
    ('Stell dir vor, du wächst in einer augenscheinlich „ganz normalen Familie“ auf.',
     'Imagine growing up in a seemingly “perfectly normal family”.'),
    ('<p>Haus, Garten, Schule, Urlaub.<br>Doch trotzdem hasst du dich selbst abgrundtief, seitdem du denken kannst.<br>Du kannst nicht anders, als ständig zu essen, schämst dich für deinen Körper und verstehst einfach nicht, warum du so viel schlimmer bist als alle anderen.</p>',
     '<p>House, garden, school, holidays.<br>And yet you have hated yourself to the core for as long as you can remember.<br>You cannot help eating all the time, you are ashamed of your body and you simply do not understand why you are so much worse than everyone else.</p>'),
    ('<p>Trotz einer eigentlich schönen Kindheit hat schon immer „irgendetwas mit mir nicht gestimmt“. Fressanfälle. Mein Gewicht. Die Angst, aufzufallen. Depressive Phasen und Zeiten, in denen ich mir selbst weh tue und nicht mehr leben will. Drogen, emotionale Abhängigkeiten und der Zwang, mich selbst immer weiter zu optimieren.<br>Das alles unter dem Deckmantel einer Essstörung, für die ich mich selbst verurteile.</p>',
     '<p>Despite what was actually a lovely childhood, “something was always wrong with me”. Binge eating. My weight. The fear of standing out. Depressive phases and times when I hurt myself and no longer want to live. Drugs, emotional dependencies and the compulsion to keep optimising myself.<br>All of it under the cover of an eating disorder I judge myself for.</p>'),
    ('<blockquote>„Wenn ich es endlich hinkriegen würde, diszipliniert und dünn zu sein, dann wäre alles gut.“</blockquote>',
     '<blockquote>“If I could finally manage to be disciplined and thin, everything would be fine.”</blockquote>'),
    ('<p>Eine der größten Lügen, die uns unsere Gesellschaft erzählt und auch ich mir lange erzählt habe.<br><span class="beiseite">(Ich habe über 50 kg abgenommen und war trotzdem nicht glücklich. ;) )</span></p>',
     '<p>One of the biggest lies our society tells us — and one I told myself for a long time.<br><span class="beiseite">(I lost over 50 kg and still was not happy. ;) )</span></p>'),
    ('<p class="markiert">Heute weiß ich: Ob Betäubung, Kontrolle, Rückzug oder Ablenkung: Egal zu welcher Überlebensstrategie wir greifen, es sind intelligente Mechanismen von unserem System, die uns helfen, mit Dingen klarzukommen.</p>',
     '<p class="markiert">Today I know: numbing, control, withdrawal or distraction — whichever survival strategy we reach for, they are intelligent mechanisms of our system that help us cope.</p>'),
    ('alt="Lilly mit grünen Haarspitzen, ein Weinglas und eine Zigarette in der Hand."',
     'alt="Lilly with green-tipped hair, holding a glass of wine and a cigarette."'),
    ('<span>Essen, Alkohol &amp; Zigaretten</span>', '<span>Food, alcohol &amp; cigarettes</span>'),
    ('alt="Lilly in Lederjacke, Augen geschlossen, Zunge herausgestreckt, eine Zigarette zwischen den Fingern."',
     'alt="Lilly in a leather jacket, eyes closed, tongue out, a cigarette between her fingers."'),
    ('<span>Drogen &amp; Depression</span>', '<span>Drugs &amp; depression</span>'),
    ('alt="Spiegel-Selfie: Lilly sehr schlank in schwarzem Mantel und Stiefeln."',
     'alt="Mirror selfie: Lilly very thin in a black coat and boots."'),
    ('<span>Hungern, Sport &amp; Studium</span>', '<span>Starving, sport &amp; university</span>'),
    ('alt="Lilly im Krankenhausbett, mit Zugang an der Hand."',
     'alt="Lilly in a hospital bed with an IV cannula in her hand."'),
    ('<span>Hautstraffungen</span>', '<span>Skin-tightening surgery</span>'),
    ('<figcaption>Egal welche Schutzstrategie: Am Ende ist es immer eine Form von Betäubung, Flucht oder Ablenkung.</figcaption>',
     '<figcaption>Whatever the protective strategy: in the end it is always a form of numbing, escape or distraction.</figcaption>'),
    ('<p>All das bedeutet nicht, dass mit uns etwas nicht stimmt, sondern dass wir hinschauen dürfen, was dahinter eigentlich unsere Aufmerksamkeit braucht.</p>',
     '<p>None of this means something is wrong with us. It means we are allowed to look at what behind it actually needs our attention.</p>'),
    ('<p>Das musste ich allerdings erst schmerzhaft lernen.<br>Mein Kartenhaus bricht in sich zusammen, als mein Papa, die einzig wirklich sichere Person in meinem Leben, viel zu früh aus dem Nichts stirbt. †</p>',
     '<p>I had to learn that the painful way, though.<br>My house of cards collapses when my dad, the only truly safe person in my life, dies far too early, out of nowhere. †</p>'),
    ('<p>Doch gleichzeitig bricht in diesem schlimmsten Schmerz auch etwas auf.<br>Tief unter dieser Trauer beginnt ein Anteil zu rufen: „Hier steckt noch mehr dahinter.“<br>Zunächst ganz leise, doch ich folge ihm.</p>',
     '<p>And yet, in this worst pain, something also breaks open.<br>Deep beneath the grief, a part of me begins to call: “There is more to this.”<br>Very quietly at first, but I follow it.</p>'),
    ('<p>Ich beginne, mich selbst kennenzulernen, zu spüren. Reise. Coachings, Energiearbeit, eine Yogaausbildung. Mein erstes Praktikum im Coaching-Bereich.</p>',
     '<p>I begin to get to know myself, to feel. Travel. Coaching, energy work, a yoga teacher training. My first internship in coaching.</p>'),
    ('<p>Vieles ändert sich zum Positiven. Schnell sogar.<br>Doch gleichzeitig spüre ich: Irgendetwas sitzt da noch. Und ich verurteile mich immer noch dafür.</p>',
     '<p>A lot changes for the better. Quickly, even.<br>But at the same time I sense: something is still stuck there. And I still judge myself for it.</p>'),
    ('<blockquote>„Ich weiß, ich bin gut genug, nur warum fühle ich es nicht?!“</blockquote>',
     '<blockquote>“I know I am good enough — so why don’t I feel it?!”</blockquote>'),
    ('<p>Deshalb entscheide ich mich für eine Ausbildung im Bereich Trauma, Nervensystem und somatische Arbeit.<br>Und tatsächlich: Nach fünf Wochen täglicher somatischer Arbeit mit mir selbst offenbart sich mir das letzte große Puzzleteil.</p>',
     '<p>So I decide to train in trauma, the nervous system and somatic work.<br>And indeed: after five weeks of daily somatic work with myself, the last big piece of the puzzle reveals itself.</p>'),
    ('<p>Nach über 20 Jahren erinnere ich mich daran, dass ein Mann aus dem Umfeld meiner Familie mich im Alter von fünf Jahren vergewaltigt hat.</p>',
     '<p>After more than 20 years, I remember that a man from my family’s circle raped me when I was five years old.</p>'),
    ('<p>Zunächst Schock, Zweifel, Unsicherheit.<br>Und dennoch die tiefe Gewissheit: Jetzt macht auf einmal alles Sinn.</p>',
     '<p>At first shock, doubt, uncertainty.<br>And yet a deep certainty: suddenly everything makes sense.</p>'),
    ('<p>Ich nehme mich der vermutlich lebenslangen Aufgabe an, dies aufzuarbeiten. Suche mir erneut Unterstützung. Lerne, darüber zu sprechen. Mich zu zeigen. Zu fühlen, was da ist, ohne wegzulaufen.</p>',
     '<p>I take on what is probably the lifelong task of working through this. I look for support again. I learn to talk about it. To show myself. To feel what is there without running away.</p>'),
    ('<p>Mit Erfolg. Heute habe ich selbst in schwierigen Zeiten tief verinnerlicht, <strong class="glut-text">dass ich liebevoll zu mir selbst bleiben darf.</strong></p>',
     '<p>With success. Today, even in difficult times, I have deeply taken in <strong class="glut-text">that I am allowed to stay loving towards myself.</strong></p>'),
    ('<p>Und mit dieser liebevollen Beziehung zu mir selbst verstehe ich, dass mir die Vergewaltigung vor allem eins genommen hat: echte Verbindung zu anderen Menschen.<br>Wahrhaftig gesehen zu werden, war lebensgefährlich für mich geworden.</p>',
     '<p>And with this loving relationship with myself I understand that the rape took one thing from me above all: real connection with other people.<br>Being truly seen had become life-threatening for me.</p>'),
    ('<p>Dem stelle ich mich in meinem Breathwork Teacher Training und lerne:</p>',
     '<p>I face this in my breathwork teacher training and learn:</p>'),
    ('<p class="satz-gross">Gesehen werden kann heute sicher sein.</p>',
     '<p class="satz-gross">Being seen can be safe today.</p>'),
    ('<p>Mit dieser Arbeit tauche ich noch tiefer, arbeite mit dem Kriegstrauma meiner Oma, das ich in mir trage, und lege Schichten ab, die älter als meine eigene Geschichte sind.</p>',
     '<p>Through this work I go even deeper, work with my grandmother’s war trauma that I carry in me, and shed layers that are older than my own story.</p>'),
    ('<p>Du siehst, neben verschiedenen Ausbildungen prägt mich vor allem meine eigene Erfahrung.<br>Und genau darum geht es auch in meiner Arbeit: Vor allem begleite und halte ich Raum für deine Selbsterfahrung.</p>',
     '<p>So you see: besides various trainings, what shapes me most is my own experience.<br>And that is exactly what my work is about: above all, I accompany and hold space for your own self-experience.</p>'),
    ('<span>Lies hier weiter, um mehr über meine Arbeit zu erfahren.</span>',
     '<span>Read on here to learn more about my work.</span>'),
    ('<p><strong>Und damit vorab eins klar ist:</strong> Du musst nichts Schlimmes erlebt haben, um hier richtig zu sein. Es reicht, wenn du mit etwas unzufrieden bist und es verändern willst.</p>',
     '<p><strong>And just so one thing is clear from the start:</strong> you do not have to have been through something terrible to be in the right place here. It is enough that something is not right for you and you want to change it.</p>'),
    ('<p>„Nicht schlimm genug“ gibt es bei mir nicht, bzw. das schauen wir uns dann liebevoll in der gemeinsamen Arbeit an. ;)</p>',
     '<p>“Not bad enough” does not exist with me — or rather, that is something we will look at lovingly in our work together. ;)</p>'),

    # ── 02 · Meine Arbeit ────────────────────────────────────────────────
    ('<p class="marke">02 — Meine Arbeit</p>', '<p class="marke">02 — My work</p>'),
    ('<p class="szene">Stell dir vor, du machst dir an einem aufregenden Tag zwischendurch dein Lieblingsgetränk und setzt dich für einen Moment gemütlich hin.<br>Eine innere Stimme sagt dir, dafür hättest du keine Zeit. Du umarmst sie gedanklich, schließt deine Augen und schenkst dir einen tiefen Atemzug. Mhhhhhhhhh.<br>Du spürst eine sprudelnde Energie in deinem Körper, fühlst dich lebendig, aber dennoch sicher. Es ist aufregend und manchmal herausfordernd, für die Dinge loszugehen, die dir wichtig sind. Doch gleichzeitig bist du tief im Vertrauen, dass du dich selbst liebevoll durch die Höhen und Tiefen deines Lebens begleiten kannst. Du bist stolz und dankbar. Und du freust dich auf dein Date mit dir selbst, das du dir für morgen eingeplant hast …</p>',
     '<p class="szene">Imagine: on an exciting day you make yourself your favourite drink and sit down comfortably for a moment.<br>An inner voice tells you that you have no time for this. You hug it in your mind, close your eyes and give yourself a deep breath. Mhhhhhhhhh.<br>You feel a bubbling energy in your body, you feel alive and yet safe. It is exciting and sometimes challenging to go for the things that matter to you. But at the same time you trust deeply that you can lovingly accompany yourself through the highs and lows of your life. You are proud and grateful. And you are looking forward to the date with yourself that you have planned for tomorrow …</p>'),
    ('<span class="audio-text">Kurze Sprachnachricht von mir, als ich beim Schreiben dieses Textes genau diesen Moment erlebt habe. <b>Folgt bald.</b></span>',
     '<span class="audio-text">A short voice message I recorded while writing this, in exactly that moment. <b>Coming soon.</b></span>'),
    ('<li class="l1">Körper &amp; Nervensystem</li>', '<li class="l1">Body &amp; nervous system</li>'),
    ('<li class="l2">Somatische Aufarbeitung</li>', '<li class="l2">Somatic processing</li>'),
    ('<li class="l3">Systembewusstsein</li>', '<li class="l3">Systemic awareness</li>'),
    ('<p class="gross">Genau das ist das Ziel meiner Arbeit: Dass du dich selbst, deinen Körper, dein Nervensystem, deine Emotionen und Energien kennst und spürst, was du brauchst. Dass du dich sicher in dir fühlst, dir selbst vertraust und weißt, dass du dir aus einer liebevollen Beziehung zu dir dein Leben kreierst.</p>',
     '<p class="gross">That is exactly the aim of my work: that you know yourself, your body, your nervous system, your emotions and energies, and sense what you need. That you feel safe within yourself, trust yourself and know that you are creating your life from a loving relationship with yourself.</p>'),
    ('<h3>Wie machen wir das?</h3>', '<h3>How do we get there?</h3>'),
    ('<p>Meine Arbeit ist kein klassisches Coaching, sondern eine Prozessbegleitung. Das bedeutet, in unseren gemeinsamen Räumen geht es darum, Referenzerfahrungen für dein System zu kreieren, durch die du lernst, dass heute neue Wege möglich sind.<br>Diese neuen Wege gilt es dann in realistischen Schritten auch im Alltag zu üben und umzusetzen, sodass du dir Stück für Stück eine neue Realität schaffen kannst.</p>',
     '<p>My work is not classic coaching but process facilitation. In the spaces we share, we create reference experiences for your system through which you learn that new ways are possible today.<br>You then practise these new ways in realistic steps in everyday life, so that bit by bit you can create a new reality for yourself.</p>'),
    ('<p class="markiert">Alles darf da sein und gefühlt werden, sodass es sich integrieren kann und seine unterbewusste Macht verliert.</p>',
     '<p class="markiert">Everything is allowed to be there and to be felt, so that it can integrate and lose its unconscious power.</p>'),
    ('<p>Du bist genauso richtig, wie du bist, und von dort aus forschen wir gemeinsam, was es braucht. Ich halte dir den Raum, teile mein Wissen und meine Erfahrung, wir begegnen uns auf Augenhöhe.</p>',
     '<p>You are right just as you are, and from there we explore together what is needed. I hold the space for you, share my knowledge and experience, and we meet as equals.</p>'),
    ('<p>Ich arbeite trauma-informiert und gerade im 1:1 sehr individuell. Wir schauen, was du in deiner Lebensrealität brauchst.<br>Grundsätzlich basiert meine Methode „Spirit of Body and Breath“ aber auf folgenden drei ineinandergreifenden Bereichen:</p>',
     '<p>I work in a trauma-informed way and, especially one-to-one, very individually. We look at what you need in the reality of your life.<br>At its core, though, my method “Spirit of Body and Breath” rests on three interlocking areas:</p>'),
    ('<p class="methode-hinweis">Tippe auf ein Feld, um zu erfahren, worum es darin geht.</p>',
     '<p class="methode-hinweis">Tap a field to find out what it is about.</p>'),
    ('aria-label="Modell Spirit of Body and Breath: drei sich überlappende Kreise"',
     'aria-label="Spirit of Body and Breath model: three overlapping circles"'),
    ('<tspan x="140" dy="0">Körper &amp;</tspan><tspan x="140" dy="1.2em">Nervensystem</tspan>',
     '<tspan x="140" dy="-.6em">Body &amp;</tspan><tspan x="140" dy="1.2em">nervous</tspan><tspan x="140" dy="1.2em">system</tspan>'),
    ('<tspan x="460" dy="0">Somatische</tspan><tspan x="460" dy="1.2em">Aufarbeitung</tspan>',
     '<tspan x="460" dy="0">Somatic</tspan><tspan x="460" dy="1.2em">processing</tspan>'),
    ('<tspan x="300" dy="0">System-</tspan><tspan x="300" dy="1.2em">bewusstsein</tspan>',
     '<tspan x="300" dy="0">Systemic</tspan><tspan x="300" dy="1.2em">awareness</tspan>'),
    ('<tspan x="300" dy="0">Frieden mit</tspan><tspan x="300" dy="1.25em">deinen Themen</tspan>',
     '<tspan x="300" dy="0">Peace with</tspan><tspan x="300" dy="1.25em">your themes</tspan>'),
    ('<tspan x="206" dy="0">Du in unserer</tspan><tspan x="206" dy="1.25em">heutigen Welt</tspan>',
     '<tspan x="206" dy="0">You in</tspan><tspan x="206" dy="1.25em">today’s world</tspan>'),
    ('<tspan x="394" dy="0">Deine</tspan><tspan x="394" dy="1.25em">Aufgabe hier</tspan>',
     '<tspan x="394" dy="0">Your purpose</tspan><tspan x="394" dy="1.25em">here</tspan>'),
    ('<tspan x="300" dy="0">Sicherheit &amp;</tspan><tspan x="300" dy="1.25em">Selbstwert</tspan>',
     '<tspan x="300" dy="0">Safety &amp;</tspan><tspan x="300" dy="1.25em">self-worth</tspan>'),
    ('<p class="methode-leer">Wähle ein Feld im Modell.</p>', '<p class="methode-leer">Choose a field in the model.</p>'),
    ('<h4>Körper &amp; Nervensystem</h4>', '<h4>Body &amp; nervous system</h4>'),
    ('<p>Das Fundament besteht darin, überhaupt erstmal wieder eine Verbindung zu deinem Körper aufzubauen. Du lernst ihn wieder zu spüren und zuzuhören. Außerdem geht es darum, dein Nervensystem zu verstehen. Du lernst zu erkennen, wo du mit deinem Nervensystem gerade stehst, und dich darin zu navigieren. Dabei geht es nicht darum, immer ruhig und reguliert zu sein, sondern dir das zu geben, was du gerade wirklich brauchst. Dadurch brauchen wir es mit der Zeit immer weniger, zu ungesunden Mechanismen zu greifen.</p>',
     '<p>The foundation is to rebuild a connection with your body in the first place. You learn to feel it again and to listen to it. It is also about understanding your nervous system. You learn to recognise where your nervous system is right now and how to navigate it. This is not about always being calm and regulated, but about giving yourself what you truly need in the moment. Over time, we then need to reach for unhealthy mechanisms less and less.</p>'),
    ('<h4>Frieden mit deinen Themen</h4>', '<h4>Peace with your themes</h4>'),
    ('<p>Ein tiefes Vertrauen: Du kannst dich und deine Themen halten. Du trägst niemals Schuld, aber übernimmst die Verantwortung.</p>',
     '<p>A deep trust: you can hold yourself and your themes. You are never to blame, but you take responsibility.</p>'),
    ('<h4>Somatische Aufarbeitung</h4>', '<h4>Somatic processing</h4>'),
    ('<p>Hier schauen wir uns deine Geschichte und Themen an. Deine Verletzungen und Prägungen aus der Kindheit, deine heutigen Trigger, Bindungsmuster &amp; Co. Wir lernen, alles zu spüren, zu halten und zu integrieren, sodass es seine unterbewusste Macht verliert. Ich arbeite hier vor allem gerne mit somatischer Arbeit und Atemarbeit. Darunter fällt die Arbeit mit Anteilen, Schatten, Chakren, unterdrückten Emotionen, deiner Stimme und vielem mehr. Immer entsprechend deiner Wünsche und Bedürfnisse.</p>',
     '<p>Here we look at your story and your themes. Your wounds and imprints from childhood, your triggers today, attachment patterns and so on. We learn to feel, hold and integrate all of it, so that it loses its unconscious power. I especially love working with somatic work and breathwork here. That includes working with parts, shadow, chakras, suppressed emotions, your voice and much more. Always according to your wishes and needs.</p>'),
    ('<h4>Deine Aufgabe hier</h4>', '<h4>Your purpose here</h4>'),
    ('<p>In unseren Erfahrungen und Schmerzen liegen oft auch Leidenschaft und Potenzial. Was willst du wirklich aus deinem Leben machen?</p>',
     '<p>Our experiences and our pain often hold passion and potential too. What do you really want to do with your life?</p>'),
    ('<h4>Systembewusstsein</h4>', '<h4>Systemic awareness</h4>'),
    ('<p>Wir sind eben nicht einfach nur wir, sondern Wesen, die ihr Leben lang in Systemen geprägt werden. Familiensysteme, Schulsysteme, Arbeitskontexte, gesellschaftliche Systeme wie Kapitalismus, Patriarchat, Neokolonialismus und viele mehr. All diese wirken tagtäglich auf uns und werden das auch weiterhin tun. Nur wenn wir lernen, dies zu erkennen, sind wir dem nicht mehr machtlos ausgeliefert.</p>',
     '<p>We are not simply “just us” — we are beings shaped by systems all our lives. Family systems, school systems, work contexts, societal systems like capitalism, patriarchy, neocolonialism and many more. All of these act on us every day and will keep doing so. Only when we learn to recognise this are we no longer powerless in the face of it.</p>'),
    ('<h4>Du in unserer heutigen Welt</h4>', '<h4>You in today’s world</h4>'),
    ('<p>Anstatt einfach nur zu funktionieren, lerne dich in den Systemen, die dich prägen, zu halten und zu navigieren.</p>',
     '<p>Instead of just functioning, learn to hold yourself and navigate within the systems that shape you.</p>'),
    ('<h4>Sicherheit &amp; Selbstwert</h4>', '<h4>Safety &amp; self-worth</h4>'),
    ('<p>Du in deiner unantastbaren Verbindung zu dir. Auch wenn nicht immer alles Friede, Freude, Eierkuchen sein wird: Du weißt, du kannst dich liebevoll halten und begleiten.</p>',
     '<p>You, in your untouchable connection with yourself. Even if life will not always be sunshine and rainbows: you know you can lovingly hold and accompany yourself.</p>'),
    ('<span class="audio-text">Lilly erklärt das Modell. <b>Audio folgt.</b></span>',
     '<span class="audio-text">Lilly explains the model. <b>Audio coming soon.</b></span>'),
    ('<p class="gross">In meiner Arbeit liegt der Fokus darauf, vom Verstand in die Verkörperung zu kommen.</p>',
     '<p class="gross">In my work, the focus is on moving from the mind into embodiment.</p>'),
    ('<p>Wir wollen das, was wir oft schon wissen, eben auch wirklich im Hier und Jetzt lernen zu leben. Dennoch nehmen wir unseren wundervollen Kopf natürlich immer mit, eben so wie das, was sich manchmal jenseits von Worten zeigt, wenn du dafür offen bist.</p>',
     '<p>What we often already know, we want to actually learn to live, here and now. Of course we always bring our wonderful head along — just like whatever sometimes shows up beyond words, if you are open to it.</p>'),
    ('<summary><b>Für die Nerds</b> Somatische Arbeit &amp; Breathwork erklärt</summary>',
     '<summary><b>For the nerds</b> Somatic work &amp; breathwork explained</summary>'),
    ('<p class="platzhalter">Hier erkläre ich bald ausführlicher, was im Körper passiert, wenn wir somatisch arbeiten und atmen. <b>Text folgt.</b></p>',
     '<p class="platzhalter">Soon I will explain here in more detail what happens in the body when we work somatically and breathe. <b>Text coming soon.</b></p>'),
    ('<h3>Woher ich komme</h3>', '<h3>Where I come from</h3>'),
    ('<p>Und falls du wissen magst, welche Ausbildungen mich neben meiner eigenen Geschichte geprägt haben:</p>',
     '<p>And in case you would like to know which trainings have shaped me alongside my own story:</p>'),
    ('<li>Trauma-informierte Embodiment-Coach</li>', '<li>Trauma-informed embodiment coach</li>'),
    ('<li>200 Stunden Multistyle-Yoga-Ausbildung, dazu Yin Yoga</li>',
     '<li>200-hour multistyle yoga teacher training, plus Yin Yoga</li>'),
    ('<li>Reiki Grad 1, 2a und 2b</li>', '<li>Reiki levels 1, 2a and 2b</li>'),
    ('<li>Studium der Internationalen Beziehungen</li>', '<li>Degree in International Relations</li>'),
    ('alt="Lilly lacht mit geschlossenen Augen, freigestellt."',
     'alt="Lilly laughing with her eyes closed, cut out from the background."'),

    # ── 03 · Online-Begleitungen ─────────────────────────────────────────
    ('<p class="marke">03 — Online-Begleitungen</p>', '<p class="marke">03 — Online journeys</p>'),
    ('Meine Online-Begleitungen erstrecken sich über einen längeren Zeitraum und richten sich an Menschen, die wirklich etwas verändern wollen.',
     'My online journeys run over a longer period and are for people who truly want to change something.'),
    ('<p>Es geht darum umzusetzen, auszuprobieren, zu fühlen, dich selbst zu erfahren.<br>Meine Arbeit ist nicht für dich, wenn du dich berieseln lassen möchtest, auf der Suche nach einem „Quick Fix“ bist oder gerettet werden möchtest.</p>',
     '<p>It is about putting things into practice, trying things out, feeling, experiencing yourself.<br>My work is not for you if you want to be passively entertained, are looking for a “quick fix” or want to be rescued.</p>'),
    ('<blockquote>„Ich will Verantwortung für mich und meine Themen übernehmen und wünsche mir dabei einen gehaltenen Raum.“</blockquote>',
     '<blockquote>“I want to take responsibility for myself and my themes — and I would like a space that holds me while I do.”</blockquote>'),
    ('<p class="marke">03a — 1:1-Prozessbegleitung</p>', '<p class="marke">03a — One-to-one process journey</p>'),
    ('<p>Meine 1:1-Prozessbegleitung ist perfekt für dich, wenn du dich entscheidest, dich selbst endlich wirklich ernst zu nehmen.</p>',
     '<p>My one-to-one process journey is perfect for you if you decide to finally take yourself seriously.</p>'),
    ('<p>In regelmäßigen Online-Sessions via Zoom gehen wir anhand meiner Methode „Spirit of Body and Breath“ deine Themen ganzheitlich an. (<a href="#methode">siehe hier</a>)<br>Zwischen den Sessions bin ich via WhatsApp für dich da und wir checken regelmäßig miteinander ein.</p>',
     '<p>In regular online sessions via Zoom we approach your themes holistically, based on my method “Spirit of Body and Breath” (<a href="#methode">see here</a>).<br>Between sessions I am there for you on WhatsApp, and we check in with each other regularly.</p>'),
    ('<p>Es gibt zusätzliche Materialien wie Audiotrainings, aufgezeichnete Sessions, Workbooks und andere Aufgaben. Wichtig ist hier: Es gibt kein allgemeines Schema X, das du durchläufst. Wir erforschen gemeinsam, was du genau brauchst und in welchem Tempo.</p>',
     '<p>There are additional materials such as audio trainings, recorded sessions, workbooks and other exercises. What matters here: there is no one-size-fits-all scheme you are put through. Together we explore what exactly you need and at what pace.</p>'),
    ('<p class="gross">Mein Anspruch an mich selbst ist es, mit dir einen Raum zu kreieren, in dem du dich wahrhaftig gesehen fühlst und in dem ausnahmslos alles da sein darf. Genau hier liegt oft schon ein riesiger Teil der Heilung.</p>',
     '<p class="gross">What I ask of myself is to create a space with you in which you feel truly seen and in which absolutely everything is allowed to be there. This alone is often a huge part of the healing.</p>'),
    ('alt="Laptop mit laufender Online-Session, daneben eine brennende Kerze."',
     'alt="Laptop with an online session running, a lit candle beside it."'),
    ('<p class="gross">Klingt spannend? Hier kannst du dir einen 10–20 Minuten unverbindlichen Kennenlerncall buchen, in dem wir einmal kurz per Telefon einchecken, ob eine Zusammenarbeit in Frage kommt.</p>',
     '<p class="gross">Sounds exciting? Here you can book a free, no-strings 10–20 minute introductory call, in which we briefly check in by phone to see whether working together could be right.</p>'),
    ('<p>Wenn die Chemie zwischen uns stimmt, vereinbaren wir einen zweiten Call via Zoom, in dem wir uns dann nochmal ganz in Ruhe ca. 1 Stunde Zeit nehmen, alle Fragen klären &amp; Co. Auch völlig unverbindlich und kostenfrei.</p>',
     '<p>If the chemistry is right, we arrange a second call via Zoom, where we take about an hour in peace to answer all your questions and so on. Also completely free and without obligation.</p>'),
    ('Kennenlerncall buchen\n', 'Book an introductory call\n'),
    ('<strong>Für wen das nicht das Richtige ist:</strong> Ich bin keine Therapeutin und mache keine Psychotherapie. Wenn du gerade in einer akuten Krise steckst, in einer psychischen Erkrankung, die Behandlung braucht, oder in einer akuten Essstörung, bist du bei einer Ärztin oder einem Psychotherapeuten besser aufgehoben. Sag mir das gern im Gespräch — ich bin da ehrlich zu dir.',
     '<strong>Who this is not right for:</strong> I am not a therapist and I do not offer psychotherapy. If you are in an acute crisis, living with a mental illness that needs treatment, or in an acute eating disorder, a doctor or psychotherapist is the better place for you. Feel free to tell me in our call — I will be honest with you.'),

    # ── 04 · Community ───────────────────────────────────────────────────
    ('<p class="marke">04 — Online-Community</p>', '<p class="marke">04 — Online community</p>'),
    ('<p class="plakette">Kostenlos und unverbindlich</p>', '<p class="plakette">Free and without obligation</p>'),
    ('<h2>Heilung geschieht nicht allein.</h2>', '<h2>Healing does not happen alone.</h2>'),
    ('<p>So lange habe ich es alleine versucht, mir eingeredet, ich bräuchte niemanden, alleine geht es mir besser. Dabei war ich tief im Inneren einsam und Verbindung für mich einfach nicht sicher.<br><strong>Heute weiß ich: Verbindung kann wieder sicher werden und ist kein Extra, sondern Teil der Arbeit.</strong></p>',
     '<p>For so long I tried to do it alone, telling myself I did not need anyone, that I was better off on my own. Deep down I was lonely, and connection simply was not safe for me.<br><strong>Today I know: connection can become safe again, and it is not an extra — it is part of the work.</strong></p>'),
    ('<p>Deshalb baue ich eine Community auf, in der wir uns begegnen und gemeinsam an der Arbeit dranbleiben. Sie entsteht gerade, heißt, du kannst von Anfang an mitgestalten.<br>Los geht’s ganz niederschwellig über WhatsApp: Wir stimmen dort Themen und Termine ab, und je nach Nachfrage entstehen Online-Breathwork- und Somatics-Sessions mit optionalen Sharings.</p>',
     '<p>That is why I am building a community in which we meet and stay with the work together. It is just forming, which means you can help shape it from the very start.<br>We are starting in the simplest way, on WhatsApp: there we agree on topics and dates, and depending on demand, online breathwork and somatics sessions with optional sharing circles come to life.</p>'),
    ('Hier beitreten\n', 'Join here\n'),
    ('<p class="klein">Kein Spam! Du landest erstmal nur im Ankündigungskanal, dort schreibe nur ich. Ob du den Austausch-Kanälen beitrittst, entscheidest du selbst. Die Community ist kostenfrei und unverbindlich. Du zahlst nur für Sessions, zu denen du dich anmeldest, und kannst jederzeit selbstständig austreten.</p>',
     '<p class="klein">No spam! At first you only land in the announcement channel, where only I post. Whether you join the exchange channels is up to you. The community is free and without obligation. You only pay for sessions you sign up for, and you can leave on your own at any time.</p>'),
    ('<p>Ich bin gespannt, wohin das Ganze wächst.', '<p>I am curious to see where this grows.'),
    ('alt="Lilly umarmt eine andere Person, beide mit geschlossenen Augen."',
     'alt="Lilly hugging another person, both with their eyes closed."'),

    # ── 05 · Offline ─────────────────────────────────────────────────────
    ('<p class="marke">05 — Offline-Angebote &amp; Kooperationen</p>',
     '<p class="marke">05 — In person &amp; collaborations</p>'),
    ('Ob im 1:1 oder in der Gruppe: Offline zu arbeiten, liebe ich am meisten.',
     'One-to-one or in a group: working in person is what I love most.'),
    ('alt="Blick von oben in einen vorbereiteten Retreat-Raum mit Matten und Klangschalen."',
     'alt="View from above into a prepared retreat room with mats and singing bowls."'),
    ('<p>Im selben Raum zu sitzen, gemeinsam zu atmen, sich wirklich zu begegnen. Mit somatischer Arbeit und Breathwork entstehen dabei tiefe, trauma-informierte Erfahrungsräume — einzigartige Sessions und Rituale, die unter die Haut gehen.</p>',
     '<p>Sitting in the same room, breathing together, truly meeting each other. With somatic work and breathwork, deep, trauma-informed spaces of experience emerge — unique sessions and rituals that get under your skin.</p>'),
    ('<p>Ich bin viel unterwegs, aber immer offen für Anfragen: im Winter meist in Indien und Südostasien, im Sommer in Deutschland (vor allem NRW &amp; Berlin) und Europa.</p>',
     '<p>I travel a lot, but I am always open to requests: in winter mostly in India and Southeast Asia, in summer in Germany (especially North Rhine-Westphalia &amp; Berlin) and Europe.</p>'),
    ('<p>Ich biete offline Folgendes an:</p>', '<p>In person, I offer:</p>'),
    ('<li>Offline-1:1-Sessions (gerne auch in Verbindung mit Online-Begleitungen)</li>',
     '<li>One-to-one sessions in person (also in combination with an online journey)</li>'),
    ('<li>Offline-Gruppensessions zu verschiedenen Themen</li>', '<li>Group sessions in person on various themes</li>'),
    ('<li>Frauenkreise</li>', '<li>Women’s circles</li>'),
    ('<p>Hast du Interesse an einer Offline-Session oder einer Kooperation?</p>',
     '<p>Interested in an in-person session or a collaboration?</p>'),
    ('data-thema="Offline-Session / Kooperation">Lass uns ins Gespräch kommen',
     'data-thema="In-person session / collaboration">Let’s talk'),

    # ── Hilfe ────────────────────────────────────────────────────────────
    ('<h3>Wenn es gerade akut ist</h3>', '<h3>If things are acute right now</h3>'),
    ('<p>Meine Arbeit ersetzt keine Psychotherapie und keine ärztliche Behandlung. Wenn es dir gerade sehr schlecht geht, wende dich bitte an Menschen, die rund um die Uhr für dich da sind:</p>',
     '<p>My work replaces neither psychotherapy nor medical treatment. If you are in a very bad place right now, please turn to people who are there for you around the clock. These are German services — if you are elsewhere, please look up the helpline for your country:</p>'),
    ('<li><b>Telefonseelsorge</b> — <a href="tel:08001110111">0800 111 0 111</a> und <a href="tel:08001110222">0800 111 0 222</a>, kostenlos, Tag und Nacht</li>',
     '<li><b>Telefonseelsorge</b> (crisis line) — <a href="tel:08001110111">0800 111 0 111</a> and <a href="tel:08001110222">0800 111 0 222</a>, free, day and night</li>'),
    ('<li><b>Bundesweites Info-Telefon Depression</b>', '<li><b>National depression helpline</b>'),
    ('<li><b>Essstörungen</b> — Beratung der BZgA:', '<li><b>Eating disorders</b> — BZgA counselling:'),
    ('<li>Im Notfall: <b>112</b> oder die nächste psychiatrische Klinik</li>',
     '<li>In an emergency: <b>112</b> or the nearest psychiatric hospital</li>'),

    # ── Kontakt ──────────────────────────────────────────────────────────
    ('<p class="marke">Kontakt &amp; Kennenlerncall</p>', '<p class="marke">Contact &amp; introductory call</p>'),
    ('<h2>Lern mich unverbindlich kennen.</h2>', '<h2>Get to know me, no strings attached.</h2>'),
    ('<p class="lese reveal" style="text-align:center">Ob Kennenlerncall, Warteliste, Community oder eine Offline-Session — sag mir einfach, worum es geht. Ich lese jede Nachricht selbst und melde mich innerhalb von zwei Werktagen bei dir.</p>',
     '<p class="lese reveal" style="text-align:center">Whether it is an introductory call, the community or an in-person session — just tell me what it is about. I read every message myself and will get back to you within two working days.</p>'),
    ('<label for="name">Wie heißt du?</label>', '<label for="name">What is your name?</label>'),
    ('<label for="email">Deine E-Mail-Adresse</label>', '<label for="email">Your email address</label>'),
    ('<label for="thema">Worum geht es?</label>', '<label for="thema">What is it about?</label>'),
    ('placeholder="Kennenlerncall, Warteliste, Community …"', 'placeholder="Introductory call, community …"'),
    ('<label for="nachricht">Magst du kurz sagen, was dich herführt? <span class="freiwillig">freiwillig</span></label>',
     '<label for="nachricht">Would you like to say briefly what brings you here? <span class="freiwillig">optional</span></label>'),
    ('placeholder="Ein Satz reicht. Oder lass es leer — wir sprechen ja."',
     'placeholder="One sentence is enough. Or leave it — we will talk anyway."'),
    ('        Bitte leer lassen <input type="text" name="botcheck" tabindex="-1" autocomplete="off">',
     '        Please leave empty <input type="text" name="botcheck" tabindex="-1" autocomplete="off">'),
    ('        Abschicken', '        Send'),
    ('<p class="zweitweg">Lieber direkt per E-Mail? <b>Adresse folgt</b> — bis dahin geht es nur über dieses Formular.</p>',
     '<p class="zweitweg">Prefer email? <b>Address to follow</b> — until then this form is the only way.</p>'),

    # ── Fuss ─────────────────────────────────────────────────────────────
    ('<nav class="fuss-links" aria-label="Rechtliches">', '<nav class="fuss-links" aria-label="Legal">'),
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
    ("Podcast <b>Adresse fehlt</b>", "Podcast <b>address missing</b>"),
    ("Instagram DE <b>fehlt</b>", "Instagram DE <b>missing</b>"),
    ("Instagram EN <b>fehlt</b>", "Instagram EN <b>missing</b>"),
]

fehlend = []
for de, en in ALLE:
    if de not in s:
        fehlend.append(de[:80])
    s = s.replace(de, en)
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
print(f"en.html geschrieben · {len(s)} Zeichen · {len(PAARE) + len(ALLE)} Ersetzungen")
if treffer:
    print("⚠ moeglicher deutscher Resttext:", treffer)
    for w in treffer:
        i = sichtbar.find(w)
        print("   …", " ".join(sichtbar[max(0, i-60):i+40].split()))
else:
    print("✓ kein deutscher Resttext im sichtbaren Bereich")
