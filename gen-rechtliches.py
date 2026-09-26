#!/usr/bin/env python3
"""
Erzeugt die sechs Rechtsseiten (DE + EN) und die 404-Seite.

Warum generiert und nicht handgeschrieben: Kopf, Fuss und Struktur sind auf
allen sieben Seiten identisch. Von Hand gepflegt laufen sie garantiert
auseinander — genau das ist im alexander-faubel-Projekt passiert, wo die
Rechtsseiten eine alte Schriftgroesse behielten.

Aufruf:  python3 gen-rechtliches.py
"""
from pathlib import Path

W = Path(__file__).parent

VORSCHAU = "https://lechcode.github.io/lilly-stradner-vorschau/"

# ── Kopf/Fuss ────────────────────────────────────────────────────────────
def seite(datei, lang, titel, beschreibung, marke, ueberschrift, inhalt,
          heim, geschwister, mitte=False):
    """geschwister: Liste (href, beschriftung) fuer den Fuss."""
    fuss = "\n        ".join(
        f'<a href="{h}">{b}</a>' for h, b in geschwister)
    klasse = ' class="mitte"' if mitte else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add('js')</script>

<!-- ENTFERNEN, sobald Impressum + Datenschutz vollstaendig sind und Lilly freigegeben hat -->
<meta name="robots" content="noindex, nofollow">

<title>{titel}</title>
<meta name="description" content="{beschreibung}">
<meta property="og:title" content="{titel}">
<meta property="og:description" content="{beschreibung}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{'de_DE' if lang == 'de' else 'en_GB'}">
<meta property="og:url" content="{VORSCHAU}{datei}">
<meta property="og:image" content="{VORSCHAU}assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="theme-color" content="#F7F3EB">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%2314100C'/%3E%3Cpath d='M16 7a9 9 0 1 0 9 9 7 7 0 1 1-7-7' fill='none' stroke='%23792427' stroke-width='2.4' stroke-linecap='round'/%3E%3C/svg%3E">
<link rel="stylesheet" href="assets/fonts.css">
<link rel="stylesheet" href="assets/tokens.css">
<link rel="stylesheet" href="assets/legal.css">
<link rel="stylesheet" href="assets/redesign.css">
</head>
<body>

<a class="skip" href="#inhalt">{'Zum Inhalt springen' if lang == 'de' else 'Skip to content'}</a>

<header class="kopf">
  <a class="wortmarke" href="{heim}">
    <img src="assets/img/siegel-120.webp" width="30" height="31" alt="">
    <b>Lilly Stradner</b>
  </a>
  <a class="zurueck" href="{heim}">{'Zurück' if lang == 'de' else 'Back'}</a>
</header>

<main id="inhalt"{klasse}>
  <div class="buehne">
    <p class="marke">{marke}</p>
    <h1>{ueberschrift}</h1>
{inhalt}
  </div>
</main>

<footer>
  <div class="buehne">
    <div class="fuss-marke">
      <img src="assets/img/siegel-120.webp" width="40" height="41" alt="">
      <span>
        <b>Lilly Stradner</b>
        <i>Spirit of Body and Breath</i>
      </span>
    </div>
    <nav class="fuss-links" aria-label="{'Rechtliches' if lang == 'de' else 'Legal'}">
        {fuss}
    </nav>
  </div>
</footer>
</body>
</html>
"""


OFFEN_DE = ('<div class="offen"><strong>An dieser Seite arbeiten wir noch.</strong> '
            'Die rot markierten Stellen füllen wir, sobald Lilly uns ihre Angaben '
            'geschickt hat. Vor der Veröffentlichung muss hier alles vollständig sein.</div>')
OFFEN_EN = ('<div class="offen"><strong>This page is still being completed.</strong> '
            'The highlighted fields will be filled in once Lilly has sent us her details. '
            'Everything here must be complete before the site goes live.</div>')

L = lambda t: f'<span class="luecke">{t}</span>'

FUSS_DE = [("index.html", "Startseite"), ("impressum.html", "Impressum"),
           ("agb.html", "AGB"), ("datenschutz.html", "Datenschutz"),
           ("en.html", "English")]
FUSS_EN = [("en.html", "Home"), ("impressum-en.html", "Legal notice"),
           ("agb-en.html", "Terms"), ("datenschutz-en.html", "Privacy"),
           ("index.html", "Deutsch")]

SEITEN = []

# ── Impressum DE ─────────────────────────────────────────────────────────
SEITEN.append(dict(
    datei="impressum.html", lang="de", heim="index.html", geschwister=FUSS_DE,
    titel="Impressum | Lilly Stradner",
    beschreibung="Impressum und Anbieterkennzeichnung nach § 5 DDG für die Website von Lilly Stradner.",
    marke="Rechtliches", ueberschrift="Impressum",
    inhalt=f"""    {OFFEN_DE}
    <div class="spalte">
      <h2>Angaben gemäß § 5 DDG</h2>
      <p>
        Lilly Stradner<br>
        {L('Straße und Hausnummer')}<br>
        {L('PLZ und Ort')}<br>
        Deutschland
      </p>

      <h2>Kontakt</h2>
      <p>
        E-Mail: {L('E-Mail-Adresse')}<br>
        Telefon: {L('optional')}
      </p>

      <h2>Umsatzsteuer</h2>
      <p>{L('Umsatzsteuer-Identifikationsnummer nach § 27 a UStG — oder der Hinweis auf die Kleinunternehmerregelung nach § 19 UStG')}</p>

      <h2>Verantwortlich für den Inhalt</h2>
      <p>Lilly Stradner, Anschrift wie oben.</p>

      <h2>Berufsbezeichnung</h2>
      <p>Lilly Stradner arbeitet als somatische Prozessbegleiterin und Breathwork-Facilitatorin.
        Diese Tätigkeit ist <strong>keine Heilkunde</strong> im Sinne des Heilpraktikergesetzes und
        <strong>keine Psychotherapie</strong>. Die Begleitung ersetzt weder eine ärztliche noch eine
        psychotherapeutische Behandlung.</p>

      <h2>Streitbeilegung</h2>
      <p>Wir sind nicht bereit und nicht verpflichtet, an einem Streitbeilegungsverfahren vor einer
        Verbraucherschlichtungsstelle teilzunehmen (§ 36 VSBG).</p>

      <h2>Bildnachweis</h2>
      <p>Alle Fotografien stammen aus dem privaten Bestand von Lilly Stradner.
        {L('Namen der Fotografinnen und Fotografen ergänzen')}</p>

      <h2>Umsetzung der Website</h2>
      <p>Gestaltung und Umsetzung: Schönbach &amp; Storz GbR, Landsberg am Lech.</p>
    </div>"""))

# ── Impressum EN ─────────────────────────────────────────────────────────
SEITEN.append(dict(
    datei="impressum-en.html", lang="en", heim="en.html", geschwister=FUSS_EN,
    titel="Legal notice | Lilly Stradner",
    beschreibung="Legal notice and provider identification under section 5 DDG for Lilly Stradner's website.",
    marke="Legal", ueberschrift="Legal notice",
    inhalt=f"""    {OFFEN_EN}
    <div class="spalte">
      <h2>Information under section 5 DDG</h2>
      <p>
        Lilly Stradner<br>
        {L('street and number')}<br>
        {L('postcode and town')}<br>
        Germany
      </p>

      <h2>Contact</h2>
      <p>
        Email: {L('email address')}<br>
        Phone: {L('optional')}
      </p>

      <h2>VAT</h2>
      <p>{L('VAT identification number under section 27a UStG — or the small-business note under section 19 UStG')}</p>

      <h2>Responsible for the content</h2>
      <p>Lilly Stradner, address as above.</p>

      <h2>Professional description</h2>
      <p>Lilly Stradner works as a somatic process facilitator and breathwork facilitator. This work
        is <strong>not medical treatment</strong> under the German Heilpraktikergesetz and
        <strong>not psychotherapy</strong>. It replaces neither medical nor psychotherapeutic care.</p>

      <h2>Dispute resolution</h2>
      <p>We are neither willing nor obliged to take part in dispute resolution proceedings before a
        consumer arbitration board (section 36 VSBG).</p>

      <h2>Image credits</h2>
      <p>All photographs come from Lilly Stradner's private collection.
        {L('add photographers’ names')}</p>

      <h2>Website</h2>
      <p>Design and build: Schönbach &amp; Storz GbR, Landsberg am Lech, Germany.</p>
    </div>"""))

# ── Datenschutz DE ───────────────────────────────────────────────────────
SEITEN.append(dict(
    datei="datenschutz.html", lang="de", heim="index.html", geschwister=FUSS_DE,
    titel="Datenschutz | Lilly Stradner",
    beschreibung="Datenschutzerklärung: Diese Website setzt keine Cookies, bindet keine externen Dienste ein und verarbeitet nur, was du selbst schickst.",
    marke="Rechtliches", ueberschrift="Datenschutz",
    inhalt=f"""    {OFFEN_DE}
    <div class="spalte">
      <h2>Kurz gesagt</h2>
      <p>Diese Website setzt <strong>keine Cookies</strong>, bindet <strong>kein Tracking</strong> und
        <strong>keine externen Dienste</strong> ein. Die Schriften liegen auf demselben Server wie die
        Seite — es entsteht keine Verbindung zu Google oder anderen Anbietern. Verarbeitet wird nur,
        was du selbst über das Formular schickst.</p>

      <h2>Verantwortliche</h2>
      <p>Lilly Stradner, {L('Anschrift')}, E-Mail {L('E-Mail-Adresse')}.</p>

      <h2>Hosting</h2>
      <p>Diese Seite wird bei <strong>GitHub Pages</strong> gehostet (GitHub Inc., 88 Colin P Kelly Jr
        Street, San Francisco, CA 94107, USA). Beim Abruf werden technisch notwendige Server-Logdaten
        verarbeitet: IP-Adresse, Datum und Uhrzeit, aufgerufene Datei, Browser und Betriebssystem.
        Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO — unser berechtigtes Interesse an einer sicher
        und zuverlässig ausgelieferten Website. Für die Übermittlung in die USA stützt sich GitHub auf
        die EU-Standardvertragsklauseln.</p>

      <h2>Kontaktformular</h2>
      <p>Wenn du das Formular nutzt, werden Name, E-Mail-Adresse, Betreff und Nachricht an Lilly
        weitergeleitet. Die Übermittlung läuft über einen Server der Schönbach &amp; Storz GbR
        (Cloudflare Workers, Standort EU). Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, wenn es um
        die Anbahnung einer Zusammenarbeit geht, sonst Art. 6 Abs. 1 lit. f DSGVO.</p>
      <p>Deine Nachricht wird gelöscht, sobald sie erledigt ist und keine gesetzlichen
        Aufbewahrungsfristen entgegenstehen.</p>

      <h2>Besondere Kategorien personenbezogener Daten</h2>
      <p>Bitte schreib uns im Formular <strong>keine Gesundheitsdaten</strong> — also nichts über
        Diagnosen, Behandlungen oder Ähnliches. Für alles Persönliche ist das vertrauliche Gespräch
        der richtige Ort, nicht das Kontaktformular.</p>

      <h2>Deine Rechte</h2>
      <ul>
        <li>Auskunft über die zu dir gespeicherten Daten (Art. 15 DSGVO)</li>
        <li>Berichtigung unrichtiger Daten (Art. 16 DSGVO)</li>
        <li>Löschung (Art. 17 DSGVO)</li>
        <li>Einschränkung der Verarbeitung (Art. 18 DSGVO)</li>
        <li>Datenübertragbarkeit (Art. 20 DSGVO)</li>
        <li>Widerspruch gegen Verarbeitungen auf Grundlage berechtigter Interessen (Art. 21 DSGVO)</li>
      </ul>
      <p>Eine Nachricht an {L('E-Mail-Adresse')} genügt. Außerdem kannst du dich bei einer
        Datenschutz-Aufsichtsbehörde beschweren (Art. 77 DSGVO).</p>

      <h2>Keine automatisierte Entscheidungsfindung</h2>
      <p>Es findet kein Profiling und keine automatisierte Entscheidungsfindung statt.</p>
    </div>"""))

# ── Datenschutz EN ───────────────────────────────────────────────────────
SEITEN.append(dict(
    datei="datenschutz-en.html", lang="en", heim="en.html", geschwister=FUSS_EN,
    titel="Privacy | Lilly Stradner",
    beschreibung="Privacy policy: this site sets no cookies, embeds no external services and processes only what you send yourself.",
    marke="Legal", ueberschrift="Privacy",
    inhalt=f"""    {OFFEN_EN}
    <div class="spalte">
      <h2>In short</h2>
      <p>This website sets <strong>no cookies</strong>, uses <strong>no tracking</strong> and embeds
        <strong>no external services</strong>. The fonts are served from the same server as the page,
        so no connection to Google or any other provider is made. The only data processed is what you
        send through the contact form yourself.</p>

      <h2>Controller</h2>
      <p>Lilly Stradner, {L('address')}, email {L('email address')}.</p>

      <h2>Hosting</h2>
      <p>This site is hosted on <strong>GitHub Pages</strong> (GitHub Inc., 88 Colin P Kelly Jr Street,
        San Francisco, CA 94107, USA). Technically necessary server logs are processed when the page is
        requested: IP address, date and time, file requested, browser and operating system. The legal
        basis is Art. 6(1)(f) GDPR — our legitimate interest in delivering the site securely and
        reliably. GitHub relies on the EU standard contractual clauses for transfers to the USA.</p>

      <h2>Contact form</h2>
      <p>If you use the form, your name, email address, subject and message are forwarded to Lilly.
        Transmission runs through a server operated by Schönbach &amp; Storz GbR (Cloudflare Workers,
        EU location). The legal basis is Art. 6(1)(b) GDPR where the message concerns starting to work
        together, otherwise Art. 6(1)(f) GDPR.</p>
      <p>Your message is deleted once it has been dealt with, unless retention periods require
        otherwise.</p>

      <h2>Special categories of personal data</h2>
      <p>Please do <strong>not</strong> send health data through the form — no diagnoses, treatments or
        similar. A confidential conversation is the right place for anything personal, not a contact
        form.</p>

      <h2>Your rights</h2>
      <ul>
        <li>Access to the data stored about you (Art. 15 GDPR)</li>
        <li>Rectification of inaccurate data (Art. 16 GDPR)</li>
        <li>Erasure (Art. 17 GDPR)</li>
        <li>Restriction of processing (Art. 18 GDPR)</li>
        <li>Data portability (Art. 20 GDPR)</li>
        <li>Objection to processing based on legitimate interests (Art. 21 GDPR)</li>
      </ul>
      <p>An email to {L('email address')} is enough. You may also lodge a complaint with a data
        protection supervisory authority (Art. 77 GDPR).</p>

      <h2>No automated decision-making</h2>
      <p>There is no profiling and no automated decision-making.</p>
    </div>"""))

# ── AGB DE ───────────────────────────────────────────────────────────────
SEITEN.append(dict(
    datei="agb.html", lang="de", heim="index.html", geschwister=FUSS_DE,
    titel="AGB | Lilly Stradner",
    beschreibung="Allgemeine Geschäftsbedingungen für die Begleitungen und Angebote von Lilly Stradner.",
    marke="Rechtliches", ueberschrift="Allgemeine Geschäftsbedingungen",
    inhalt=f"""    <div class="offen"><strong>Diese Seite ist ein Gerüst, noch kein fertiges Dokument.</strong>
      Struktur und die Punkte, auf die es ankommt, stehen. Vor der Veröffentlichung sollte eine
      Anwältin oder ein Anwalt darüberschauen — besonders über Widerruf und Haftung. Sobald Lilly
      digitale Inhalte wirklich verkauft, kommt eine Widerrufsbelehrung dazu.</div>
    <div class="spalte">
      <h2>1 · Geltungsbereich</h2>
      <p>Diese Bedingungen gelten für alle Begleitungen, Sessions, Gruppenangebote und digitalen
        Inhalte von Lilly Stradner, {L('Anschrift')}.</p>

      <h2>2 · Was diese Arbeit ist — und was nicht</h2>
      <p>Die Begleitung ist eine somatische Prozessbegleitung. Sie ist <strong>keine Heilbehandlung,
        keine Psychotherapie und kein Ersatz für ärztliche oder psychotherapeutische Hilfe</strong>.
        Es wird keine Diagnose gestellt und keine Heilung versprochen.</p>
      <p>Bei akuten psychischen Krisen, akuten Essstörungen oder behandlungsbedürftigen Erkrankungen
        ist ärztliche oder psychotherapeutische Behandlung der richtige Weg. Lilly darf eine
        Begleitung ablehnen oder beenden, wenn sie den Eindruck hat, dass etwas anderes gebraucht wird.</p>

      <h2>3 · Zustandekommen</h2>
      <p>Eine Zusammenarbeit kommt zustande, wenn beide Seiten sie ausdrücklich bestätigen — in der
        Regel nach dem kostenlosen Kennenlerngespräch. Die Darstellung der Angebote auf dieser Website
        ist noch kein bindendes Angebot.</p>

      <h2>4 · Preise und Zahlung</h2>
      <p>{L('Preise, Fälligkeit und Zahlungsweise ergänzen')}</p>

      <h2>5 · Termine und Absagen</h2>
      <p>{L('Absagefrist festlegen — üblich sind 24 oder 48 Stunden')}</p>

      <h2>6 · Digitale Inhalte</h2>
      <p>Aufnahmen und Kurse sind ausschließlich für den persönlichen Gebrauch bestimmt. Sie dürfen
        nicht weitergegeben, öffentlich gezeigt oder vervielfältigt werden.</p>
      <p>{L('Widerrufsbelehrung für digitale Inhalte ergänzen, sobald ein Verkauf stattfindet')}</p>

      <h2>7 · Mitwirkung und Eigenverantwortung</h2>
      <p>Die Teilnahme geschieht in eigener Verantwortung. Bitte gib vorab Bescheid, wenn gesundheitliche
        Gründe gegen intensive Atemarbeit sprechen könnten — dazu zählen unter anderem Schwangerschaft,
        Herz-Kreislauf-Erkrankungen, Epilepsie, Netzhautablösung, schwere psychische Erkrankungen und
        Operationen in jüngerer Zeit. Im Zweifel bitte vorher ärztlich abklären.</p>

      <h2>8 · Vertraulichkeit</h2>
      <p>Alles, was in einer Begleitung besprochen wird, bleibt vertraulich. Das gilt für beide Seiten
        und auch für Gruppenangebote.</p>

      <h2>9 · Haftung</h2>
      <p>Die Haftung für leicht fahrlässige Pflichtverletzungen ist ausgeschlossen, soweit dadurch nicht
        wesentliche Vertragspflichten, Leben, Körper oder Gesundheit betroffen sind.</p>

      <h2>10 · Schlussbestimmungen</h2>
      <p>Es gilt deutsches Recht. Sollte eine Bestimmung unwirksam sein, bleibt der Rest wirksam.</p>
    </div>"""))

# ── AGB EN ───────────────────────────────────────────────────────────────
SEITEN.append(dict(
    datei="agb-en.html", lang="en", heim="en.html", geschwister=FUSS_EN,
    titel="Terms | Lilly Stradner",
    beschreibung="Terms and conditions for Lilly Stradner's sessions, group offerings and digital content.",
    marke="Legal", ueberschrift="Terms and conditions",
    inhalt=f"""    <div class="offen"><strong>This page is a framework, not a finished document.</strong>
      The structure and the points that matter are in place. A lawyer should review it before the site
      goes live — particularly the cancellation and liability sections. A right-of-withdrawal notice
      will be added once Lilly actually sells digital content.</div>
    <div class="spalte">
      <h2>1 · Scope</h2>
      <p>These terms apply to all sessions, group offerings and digital content provided by
        Lilly Stradner, {L('address')}.</p>

      <h2>2 · What this work is — and what it is not</h2>
      <p>This is somatic process facilitation. It is <strong>not medical treatment, not psychotherapy
        and no substitute for medical or psychotherapeutic care</strong>. No diagnosis is made and no
        cure is promised.</p>
      <p>In acute psychological crises, acute eating disorders or conditions requiring treatment,
        medical or psychotherapeutic care is the right path. Lilly may decline or end a collaboration
        if she feels something else is needed.</p>

      <h2>3 · Formation of contract</h2>
      <p>A collaboration begins once both sides confirm it explicitly, usually after the free
        introductory call. The presentation of offerings on this website is not yet a binding offer.</p>

      <h2>4 · Prices and payment</h2>
      <p>{L('add prices, due dates and payment methods')}</p>

      <h2>5 · Appointments and cancellations</h2>
      <p>{L('set a cancellation window — 24 or 48 hours is common')}</p>

      <h2>6 · Digital content</h2>
      <p>Recordings and courses are for personal use only. They may not be shared, shown publicly or
        reproduced.</p>
      <p>{L('add the right-of-withdrawal notice for digital content once sales begin')}</p>

      <h2>7 · Your own responsibility</h2>
      <p>Participation is at your own responsibility. Please tell Lilly in advance if there may be
        health reasons against intensive breathwork — these include pregnancy, cardiovascular
        conditions, epilepsy, retinal detachment, severe psychiatric conditions and recent surgery.
        When in doubt, please check with a doctor first.</p>

      <h2>8 · Confidentiality</h2>
      <p>Everything discussed stays confidential. This applies to both sides and to group settings.</p>

      <h2>9 · Liability</h2>
      <p>Liability for slightly negligent breaches of duty is excluded, unless material contractual
        obligations, life, body or health are affected.</p>

      <h2>10 · Final provisions</h2>
      <p>German law applies. Should any provision be invalid, the remainder stays in force.</p>
    </div>"""))

# ── 404 ──────────────────────────────────────────────────────────────────
SEITEN.append(dict(
    datei="404.html", lang="de", heim="index.html", geschwister=FUSS_DE, mitte=True,
    titel="Seite nicht gefunden | Lilly Stradner",
    beschreibung="Diese Seite gibt es nicht (mehr). Zurück zur Startseite von Lilly Stradner.",
    marke="Fehler 404", ueberschrift="Hier ist nichts.",
    inhalt="""    <div class="spalte" style="margin-inline:auto">
      <p>Die Seite, die du suchst, gibt es nicht — oder nicht mehr.
        Vielleicht ein Tippfehler in der Adresse?</p>
      <p><a class="zurueck" href="index.html">Zur Startseite</a></p>
    </div>"""))


for s in SEITEN:
    (W / s["datei"]).write_text(seite(**s), encoding="utf-8")
    print(f"  {s['datei']}")

print(f"\n{len(SEITEN)} Seiten erzeugt.")
