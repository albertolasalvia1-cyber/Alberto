#!/usr/bin/env python3
"""Genera le pagine HTML del sito Padovani & Partners.

Header, menu, card dei partner, form e footer sono definiti una volta sola qui:
modifica questo file e rilancia `python3 genera.py` per aggiornare tutte le pagine.
"""
from pathlib import Path

OUT = Path(__file__).parent
PIVA = "04661560286"

ICON = {
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "chev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>',
    "up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 15 6-6 6 6"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
    "umbrella": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 12a10 10 0 0 0-20 0z"/><path d="M12 12v8a2 2 0 0 0 4 0"/><path d="M12 2v1"/></svg>',
    "scale": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v18M5 21h14M3 7h18"/><path d="m6 7-3 7a3 3 0 0 0 6 0zM18 7l-3 7a3 3 0 0 0 6 0z"/></svg>',
    "car": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 17h14M5 17a2 2 0 1 1-4 0v-4l2.5-6h17L23 13v4a2 2 0 1 1-4 0"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M3 12h18"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 6-7"/></svg>',
    "award": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="6"/><path d="M8.2 13 7 22l5-3 5 3-1.2-9"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></svg>',
    "handshake": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.9-3.9a3 3 0 0 0-4.2 0l-.9.9a1 1 0 1 1-3-3l2.8-2.8a5 5 0 0 1 6.2-.6l.5.3a2 2 0 0 0 1.5.3L21 4"/><path d="m21 3 1 11h-2"/><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path d="M3 4h8"/></svg>',
}

# Pagine dei partner. "tall" = logo quasi quadrato (AXA), che va mostrato più alto.
PARTNERS = [
    dict(file="unipol.html", name="UnipolSai Assicurazioni", short="Unipol", tag="Assicurazioni", logo="logo-unipolsai.png",
         icon="umbrella", blurb="Polizze per imprese, professionisti e famiglie con uno dei principali gruppi assicurativi italiani."),
    dict(file="axa.html", name="AXA Assicurazioni – Pegaso SRL", short="AXA", tag="Protezione assicurativa globale", logo="logo-axa.png", tall=True,
         icon="shield", blurb="Salute, tutela legale, viaggi: soluzioni complete e personalizzate, dal privato all’azienda."),
    dict(file="unibrokers.html", name="Unibrokers S.r.l.", short="Unibrokers", tag="Brokeraggio assicurativo", logo="logo-unibrokers.png",
         icon="scale", blurb="Broker indipendente dal 1997: selezioniamo per te le coperture migliori sul mercato, senza costi aggiuntivi."),
    dict(file="car-adviser.html", name="Car Adviser SRL", short="Car Adviser", tag="Noleggio a lungo termine", logo="logo-car-adviser.png",
         icon="car", blurb="Servizi per la mobilità: noleggio a lungo termine e gestione del parco veicoli aziendale."),
    dict(file="librici.html", name="Antonino Librici & Partners", short="Antonino Librici", tag="Consulenza di risk management", logo="logo-librici.png",
         icon="chart", blurb="Analisi, valutazione e gestione dei rischi d’impresa, per una protezione efficace nel tempo."),
]

PHONES = [
    ("AXA Assicurazioni – Pegaso SRL", "049 098 2994", "+390490982994"),
    ("Unibrokers S.r.l.", "049 657 501", "+39049657501"),
]


def esc(s):
    return s.replace("&", "&amp;")


def logo_img(p, extra=""):
    cls = ' class="tall"' if p.get("tall") else ""
    return f'<img src="img/{p["logo"]}" alt="{esc(p["name"])}"{cls}{extra}>'


def header(current):
    def cur(f):
        return ' aria-current="page"' if f == current else ""
    items = "\n".join(
        f'              <li><a href="{p["file"]}"{cur(p["file"])}>{esc(p["short"])}<span>{esc(p["tag"])}</span></a></li>'
        for p in PARTNERS
    )
    return f"""  <header class="site-header">
    <div class="wrap">
      <a class="logo" href="index.html" aria-label="Padovani &amp; Partners – Home">
        <span class="logo-mark" aria-hidden="true">PP</span>
        <span class="logo-text">Padovani &amp; Partners<small>Consulenza assicurativa</small></span>
      </a>
      <nav class="main-nav" id="main-nav" aria-label="Menu principale">
        <ul>
          <li><a href="index.html"{cur("index.html")}>Home</a></li>
          <li><a href="index.html#chi-siamo">Chi siamo</a></li>
          <li class="dd">
            <button class="dd-btn" aria-expanded="false" aria-haspopup="true">Soluzioni {ICON["chev"]}</button>
            <ul class="dd-menu">
{items}
            </ul>
          </li>
          <li><a href="index.html#metodo">Come lavoriamo</a></li>
          <li><a class="btn btn-gold btn-sm" href="contatti.html"{cur("contatti.html")}>Richiedi una consulenza</a></li>
        </ul>
      </nav>
      <button class="menu-toggle" aria-label="Menu" aria-expanded="false" aria-controls="main-nav"><span></span><span></span><span></span></button>
    </div>
  </header>"""


def footer():
    sol = "\n".join(f'            <li><a href="{p["file"]}">{esc(p["short"])}</a></li>' for p in PARTNERS)
    tel = "\n".join(f'            <li><a href="tel:{t}">{esc(n)}<br>{d}</a></li>' for n, d, t in PHONES)
    return f"""  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <a class="logo" href="index.html"><span class="logo-mark" aria-hidden="true">PP</span><span class="logo-text">Padovani &amp; Partners<small>Consulenza assicurativa</small></span></a>
          <p>Soluzioni assicurative, brokeraggio, noleggio a lungo termine e risk management per aziende, professionisti e privati.</p>
        </div>
        <div>
          <h4>Soluzioni</h4>
          <ul>
{sol}
          </ul>
        </div>
        <div>
          <h4>Studio</h4>
          <ul>
            <li><a href="index.html#chi-siamo">Chi siamo</a></li>
            <li><a href="index.html#soluzioni">Le nostre soluzioni</a></li>
            <li><a href="index.html#metodo">Come lavoriamo</a></li>
            <li><a href="contatti.html">Contatti</a></li>
          </ul>
        </div>
        <div>
          <h4>Contatti</h4>
          <ul>
{tel}
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; Padovani &amp; Partners · P.IVA {PIVA}</span>
        <a href="contatti.html">Richiedi una consulenza</a>
      </div>
    </div>
  </footer>"""


def page(filename, title, description, body):
    return f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#0f2f28">
  <link rel="icon" href="img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
{header(filename)}

  <main>
{body}
  </main>

{footer()}

  <button class="to-top" aria-label="Torna su">{ICON["up"]}</button>
  <script src="js/main.js"></script>
</body>
</html>
"""


def phone_lines(only=None):
    phones = [x for x in PHONES if x[0] == only] or PHONES
    return "\n".join(
        f'          <a class="phone-line" href="tel:{t}">{ICON["phone"]}<span><small>{esc(n)}</small><b>{d}</b></span></a>'
        for n, d, t in phones
    )


def cta(title="Hai bisogno di una consulenza?"):
    return f"""    <section class="section paper">
      <div class="wrap">
        <div class="cta-box reveal">
          <div>
            <span class="eyebrow">Parliamone</span>
            <h2>{title}</h2>
            <p>Contattaci o vieni a trovarci: troveremo la soluzione adatta a te.</p>
          </div>
          <div class="cta-actions">
            <a class="btn btn-gold" href="contatti.html">Richiedi una consulenza {ICON["arrow"]}</a>
{phone_lines()}
          </div>
        </div>
      </div>
    </section>"""


def form(name, subject):
    return f"""        <form class="form form-card reveal d1" name="{name}" method="POST" data-netlify="true" netlify-honeypot="bot-field">
          <h3>Richiedi una consulenza</h3>
          <p>{subject}</p>
          <input type="hidden" name="form-name" value="{name}">
          <p class="hidden"><label>Non compilare: <input name="bot-field"></label></p>
          <div class="form-row">
            <div class="field"><label for="{name}-nome">Nome e cognome</label><input id="{name}-nome" name="nome" autocomplete="name" required></div>
            <div class="field"><label for="{name}-tel">Telefono</label><input id="{name}-tel" name="telefono" type="tel" autocomplete="tel"></div>
          </div>
          <div class="field"><label for="{name}-email">Email</label><input id="{name}-email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="{name}-richiesta">Richiesta <small>(facoltativo)</small></label><textarea id="{name}-richiesta" name="richiesta" placeholder="Raccontaci in breve di cosa hai bisogno"></textarea></div>
          <div class="field"><label for="{name}-antispam">Domanda di sicurezza: qual è la capitale della Francia?</label><input id="{name}-antispam" name="antispam" required></div>
          <label class="consent"><input type="checkbox" name="consenso" required> Acconsento al trattamento dei dati personali per essere ricontattato in merito alla mia richiesta.</label>
          <button class="btn btn-dark" type="submit">Invia la richiesta {ICON["arrow"]}</button>
          <p class="form-msg" role="status" aria-live="polite"></p>
        </form>"""


def contact_section(name, subject, intro_title, intro_text, extra=""):
    return f"""    <section class="section dark" id="contatti">
      <div class="wrap contact-grid">
        <div class="reveal">
          <span class="eyebrow">Contatti</span>
          <h2>{intro_title}</h2>
          <p class="lead">{intro_text}</p>
          <div class="contact-points">
{extra or phone_lines()}
          </div>
        </div>
{form(name, subject)}
      </div>
    </section>"""


def other_partners(exclude):
    chips = "\n".join(
        f"""          <a class="partner-chip reveal" href="{p["file"]}"><span class="brand">{logo_img(p, ' loading="lazy"')}</span><small>{esc(p["tag"])}</small><span class="link-arrow">Scopri di più {ICON["arrow"]}</span></a>"""
        for p in PARTNERS if p["file"] != exclude
    )
    return f"""    <section class="section cream">
      <div class="wrap">
        <div class="section-head">
          <span class="eyebrow">Le altre soluzioni</span>
          <h2>Proteggi la tua azienda con noi: le soluzioni che fanno la differenza.</h2>
        </div>
        <div class="partner-strip">
{chips}
        </div>
      </div>
    </section>"""


def partner_page(p, title, description, h1, lead, hero_img, content, aside_rows, form_subject, banner=None):
    media = f'<div class="media"><img src="img/{hero_img}" alt=""></div>' if hero_img else ""
    panel_cls = "brand-panel" + ("" if hero_img else " only-logo")
    rows = "\n".join(f"            <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in aside_rows)
    banner_html = f'\n          <div class="banner reveal"><p>{banner}</p></div>' if banner else ""
    body = f"""    <section class="page-hero">
      <div class="wrap">
        <nav class="crumbs" aria-label="Percorso"><a href="index.html">Home</a><span>/</span><a href="index.html#soluzioni">Soluzioni</a><span>/</span>{esc(p["short"])}</nav>
        <div class="page-hero-grid">
          <div class="reveal">
            <span class="eyebrow">{esc(p["tag"])}</span>
            <h1>{h1}</h1>
            <p class="lead">{lead}</p>
            <div class="hero-ctas">
              <a class="btn btn-gold" href="#contatti">Richiedi una consulenza {ICON["arrow"]}</a>
            </div>
          </div>
          <div class="{panel_cls} reveal d2">
            {media}
            <div class="logo-box">{logo_img(p)}<span>{esc(p["name"])}</span></div>
          </div>
        </div>
      </div>
    </section>

    <section class="section paper">
      <div class="wrap content-grid">
        <div class="prose">
{content}{banner_html}
        </div>
        <aside class="aside-card reveal d1">
          <h3>{esc(p["name"])}</h3>
          <p class="muted">{esc(p["tag"])}</p>
          <dl>
{rows}
          </dl>
          <a class="btn btn-dark" href="#contatti">Scrivici {ICON["arrow"]}</a>
        </aside>
      </div>
    </section>

{contact_section("contatti-" + p["file"].removesuffix(".html"), form_subject, "Parliamo delle tue esigenze", "Compila il modulo: ti ricontatteremo al più presto per fissare una consulenza, senza impegno.", phone_lines(p["name"]))}

{other_partners(p["file"])}"""
    (OUT / p["file"]).write_text(page(p["file"], title, description, body), encoding="utf-8")


def features(items):
    cards = "\n".join(
        f"""            <div class="feature reveal d{i % 2 + 1}"><span class="num">0{i + 1}</span><h3>{t}</h3><p>{d}</p></div>"""
        for i, (t, d) in enumerate(items)
    )
    return f'          <div class="features">\n{cards}\n          </div>'


P = {p["file"]: p for p in PARTNERS}

# ================================================================ Home
areas = "\n".join(
    f"""              <li><a href="{p["file"]}"><span class="ico">{ICON[p["icon"]]}</span><span><b>{esc(p["tag"])}</b><small>{esc(p["short"])}</small></span><span class="arr">{ICON["arrow"]}</span></a></li>"""
    for p in PARTNERS
)
solutions = "\n".join(
    f"""          <a class="solution reveal d{i % 3 + 1}" href="{p["file"]}">
            <span class="brand">{logo_img(p, ' loading="lazy"')}</span>
            <span class="tag">{esc(p["tag"])}</span>
            <h3>{esc(p["name"])}</h3>
            <p>{p["blurb"]}</p>
            <span class="link-arrow">Scopri di più {ICON["arrow"]}</span>
          </a>"""
    for i, p in enumerate(PARTNERS)
)
values = [
    ("award", "Esperienza e competenza in ambito assicurativo", "Siamo un team di professionisti qualificati con anni di esperienza, pronti a guidarti nel complesso mondo delle assicurazioni aziendali, offrendo consulenza specializzata e affidabile."),
    ("target", "Consulenza assicurativa per il tuo successo", "Con le nostre soluzioni ti aiutiamo a concentrarti sulla crescita del tuo business, lasciando a noi la gestione dei rischi."),
    ("shield", "Coperture personalizzate", "Specializzati nel settore aziendale, offriamo polizze su misura che coprono rischi finanziari, responsabilità civile e tutela del patrimonio, per garantire la massima sicurezza alla tua impresa."),
    ("handshake", "Relazioni basate sulla fiducia", "Offriamo un servizio trasparente e professionale, diventando il tuo partner di riferimento per tutte le esigenze di brokeraggio e consulenza assicurativa."),
]
values_html = "\n".join(
    f"""          <div class="value reveal d{i % 2 + 1}"><span class="ico">{ICON[ic]}</span><h3>{t}</h3><p>{d}</p></div>"""
    for i, (ic, t, d) in enumerate(values)
)
steps = [
    ("Analisi", "Studiamo la tua attività e le coperture già in essere per individuare rischi ed esigenze reali."),
    ("Proposta", "Selezioniamo le soluzioni più adatte e convenienti tra compagnie italiane e internazionali."),
    ("Gestione", "Monitoriamo scadenze, premi e aggiornamenti normativi: un unico referente per tutti i contratti."),
    ("Assistenza", "Ti affianchiamo nella gestione dei sinistri, con un’assistenza completa e tempestiva."),
]
steps_html = "\n".join(
    f"""          <div class="step reveal d{i + 1}"><h3>{t}</h3><p>{d}</p></div>""" for i, (t, d) in enumerate(steps)
)

home = f"""    <section class="hero">
      <div class="wrap hero-grid">
        <div class="reveal">
          <span class="eyebrow">Padovani &amp; Partners</span>
          <h1>Proteggi il tuo business con soluzioni <em class="accent">su misura</em></h1>
          <p class="lead">Il punto di riferimento per aziende, professionisti e privati che cercano coperture personalizzate, noleggio a lungo termine e consulenza di risk management. Tu pensi alla crescita, noi alla tua tranquillità.</p>
          <div class="hero-ctas">
            <a class="btn btn-gold" href="contatti.html">Richiedi una consulenza {ICON["arrow"]}</a>
            <a class="btn btn-ghost" href="#soluzioni">Scopri le soluzioni</a>
          </div>
          <div class="hero-stats">
            <div><b>5</b><span>partner specializzati</span></div>
            <div><b>1</b><span>unico referente</span></div>
            <div><b>360°</b><span>protezione per l’impresa</span></div>
          </div>
        </div>
        <div class="glass reveal d2">
          <h2>Le nostre aree</h2>
          <ul class="area-list">
{areas}
          </ul>
        </div>
      </div>
    </section>

    <section class="section cream" id="chi-siamo">
      <div class="wrap split">
        <div class="reveal">
          <span class="eyebrow">Chi siamo</span>
          <h2>Un unico partner per proteggere tutto ciò che conta</h2>
          <p class="lead">Benvenuti in <strong>Padovani &amp; Partners</strong>. Il nostro obiettivo è offrirti la tranquillità di sapere che ogni aspetto della tua attività è protetto, lasciandoti libero di concentrarti sulla crescita del tuo business.</p>
          <p>Con una gamma completa di polizze per aziende, professionisti e privati, una divisione specializzata nel noleggio a lungo termine e la consulenza di risk management, siamo al tuo fianco per costruire un futuro sicuro e privo di preoccupazioni. Scopri come possiamo aiutarti a proteggere i tuoi asset e a gestire il tuo parco veicoli con soluzioni innovative e su misura.</p>
          <p class="quote">“Proteggi ciò che conta di più, con la nostra esperienza al tuo fianco.”</p>
        </div>
        <div class="values">
{values_html}
        </div>
      </div>
    </section>

    <section class="section darker" id="soluzioni">
      <div class="wrap">
        <div class="section-head reveal">
          <span class="eyebrow">Le nostre soluzioni</span>
          <h2>Proteggi la tua azienda con noi: le soluzioni che fanno la differenza.</h2>
          <p class="lead">Lavoriamo con partner selezionati per offrirti, da un unico interlocutore, tutto ciò che serve alla tua sicurezza e alla tua mobilità.</p>
        </div>
        <div class="solutions">
{solutions}
        </div>
      </div>
    </section>

    <section class="section paper" id="metodo">
      <div class="wrap">
        <div class="section-head reveal">
          <span class="eyebrow">Come lavoriamo</span>
          <h2>Un metodo chiaro, dalla prima analisi all’assistenza sui sinistri</h2>
        </div>
        <div class="steps">
{steps_html}
        </div>
      </div>
    </section>

{cta()}"""
(OUT / "index.html").write_text(page(
    "index.html", "Padovani & Partners — Consulenza assicurativa, brokeraggio e risk management",
    "Padovani & Partners: consulenza assicurativa, brokeraggio, noleggio a lungo termine e risk management per aziende, professionisti e privati.",
    home), encoding="utf-8")

# ================================================================ AXA
partner_page(
    P["axa.html"], "AXA Assicurazioni – Pegaso SRL | Padovani & Partners",
    "AXA Assicurazioni – Pegaso SRL: protezione assicurativa globale, soluzioni su misura per privati e aziende.",
    "Protezione assicurativa globale, su misura per privati e aziende",
    "Soluzioni assicurative complete e personalizzate, progettate per garantire una protezione globale e rispondere alle specifiche esigenze di ogni cliente, dal privato all’azienda.",
    "hero-axa.jpg",
    """          <h2>Perché sceglierci</h2>
          <p>Siamo il tuo punto di riferimento per la <strong>consulenza assicurativa</strong> e il <strong>brokeraggio</strong>, con un approccio professionale e orientato al cliente.</p>
""" + features([
        ("Coperture sanitarie complete", "Le nostre polizze sanitarie coprono ogni fase della tutela della salute: dalla prevenzione alla cura, fino all’assistenza. Soluzioni su misura per garantirti sicurezza in ogni momento della vita."),
        ("Tutela legale per ogni ambito", "Protezione completa per privati, aziende e holding. Le nostre polizze di tutela legale offrono un supporto affidabile per gestire eventuali controversie e garantire la massima tranquillità."),
        ("Polizze viaggi personalizzabili", "Viaggia senza pensieri grazie a polizze viaggio con copertura sanitaria <strong>illimitata</strong> e moduli flessibili, adattabili a ogni esigenza personale o professionale."),
        ("Sicurezza a 360°", "Proteggi ciò che conta di più, con la nostra esperienza al tuo fianco: un unico interlocutore per tutte le tue coperture."),
    ]),
    [("Referente aziendale", "Nardo Stefano"), ("Codice RUI", "A000331871"), ("Telefono", '<a href="tel:+390490982994">049 098 2994</a>')],
    "Ti ricontatteremo per una consulenza sulle soluzioni AXA.",
)

# ================================================================ Unibrokers
UB_RUI = "B000014279"
partner_page(
    P["unibrokers.html"], "Unibrokers S.r.l. — Brokeraggio assicurativo | Padovani & Partners",
    "Unibrokers S.r.l.: servizi di consulenza e brokeraggio assicurativo a Padova dal 1997.",
    "Consulenza e brokeraggio assicurativo indipendente",
    "Dal 1997 tuteliamo gli interessi dei nostri clienti: analizziamo le esigenze, selezioniamo le coperture migliori sul mercato e ti seguiamo anche nella gestione dei sinistri.",
    "hero-unibrokers.jpg",
    f"""          <h2>Chi siamo</h2>
          <p><strong>Unibrokers S.r.l.</strong> è una società di brokeraggio assicurativo fondata nel 1997, con sede a Padova, iscritta al <strong>Registro Unico degli Intermediari</strong> (R.U.I.) con il numero {UB_RUI}, sotto la vigilanza di IVASS.</p>
          <p>Grazie a oltre 20 anni di esperienza nel settore assicurativo, la nostra missione è garantire la <strong>tutela degli interessi del cliente</strong>, offrendo soluzioni su misura per la gestione dei rischi. Analizziamo le esigenze assicurative, proponiamo le migliori coperture contrattuali e collaboriamo con compagnie italiane e internazionali per garantire il massimo vantaggio. Inoltre supportiamo i clienti nella gestione dei sinistri, assicurando un’assistenza completa.</p>
          <h2>Perché sceglierci</h2>
          <p>Siamo il tuo partner di fiducia per una consulenza assicurativa completa e personalizzata. La nostra esperienza ci permette di gestire sia le polizze sottoscritte attraverso di noi sia quelle già in essere.</p>
""" + features([
        ("Gestione completa delle polizze", "Monitoriamo le scadenze contrattuali e ci occupiamo dell’incasso dei premi, trasferendoli alle compagnie competenti."),
        ("Aggiornamenti costanti", "Informiamo i clienti su nuovi prodotti assicurativi, modifiche legislative e opportunità di aggiornamento delle polizze in corso."),
        ("Personalizzazione", "Concordiamo con i clienti eventuali integrazioni o modifiche, per garantire che le coperture siano sempre adeguate."),
        ("Nessun costo aggiuntivo", "Il nostro servizio non comporta oneri per il cliente: il broker è remunerato direttamente dalle compagnie assicurative."),
    ]) + """
          <h2>I vantaggi di affidarsi a noi</h2>
          <ul class="checklist">
            <li><strong>Unico referente</strong> per la gestione di tutti i contratti assicurativi.</li>
            <li><strong>Consulenza imparziale</strong>, grazie alla nostra indipendenza dalle compagnie assicurative.</li>
            <li><strong>Trattative flessibili</strong> con le principali compagnie italiane e straniere.</li>
            <li><strong>Ottimizzazione dei costi e delle garanzie</strong>, senza costi aggiuntivi per il cliente.</li>
          </ul>
          <h2>I nostri servizi</h2>
          <ul class="checklist">
            <li><strong>Consulenza indipendente</strong>: in qualità di broker operiamo in completa autonomia, selezionando la copertura più adatta e conveniente tra le migliori compagnie sul mercato.</li>
            <li><strong>Assistenza dedicata</strong>: un unico punto di riferimento per tutte le esigenze assicurative, con semplicità e trasparenza nella gestione dei contratti.</li>
            <li><strong>Libertà di scelta</strong>: trattiamo con compagnie italiane e internazionali per ottenere le migliori condizioni economiche e di copertura.</li>
          </ul>""",
    [("Amministratore unico, broker", "Nalin Roberta"), ("Responsabile commerciale", "Saggin Enrico"),
     ("Telefono", '<a href="tel:+39049657501">049 657 501</a>'), ("Iscrizione RUI", UB_RUI)],
    "Richiedi una consulenza gratuita sul tuo pacchetto assicurativo.",
    banner="Affidati a Unibrokers per la gestione completa e personalizzata delle tue polizze. Richiedi una consulenza gratuita e scopri come semplificare e ottimizzare il tuo pacchetto assicurativo.",
)

# ================================================================ Pagine senza contenuto nel video
# Testi provvisori: da sostituire con quelli definitivi.
partner_page(
    P["unipol.html"], "UnipolSai Assicurazioni | Padovani & Partners",
    "UnipolSai Assicurazioni: polizze per aziende, professionisti e privati.",
    "Coperture assicurative per imprese, professionisti e famiglie",
    "Attraverso UnipolSai Assicurazioni offriamo una gamma completa di polizze per proteggere la tua attività, il tuo patrimonio e le persone a cui tieni.",
    None,
    """          <h2>Cosa possiamo fare per te</h2>
          <p>Ti accompagniamo nella scelta delle coperture più adatte, con un’analisi attenta delle tue esigenze e un unico referente per ogni necessità.</p>
""" + features([
        ("Polizze per le imprese", "Coperture per rischi finanziari, responsabilità civile e tutela del patrimonio aziendale."),
        ("Professionisti", "Responsabilità civile professionale e tutela dell’attività, su misura per la tua professione."),
        ("Privati e famiglie", "Soluzioni per la casa, la salute e la persona, per vivere ogni giorno con serenità."),
        ("Assistenza sui sinistri", "Ti affianchiamo in ogni fase, dalla denuncia alla liquidazione."),
    ]),
    [("Area", "Assicurazioni"), ("Per informazioni", '<a href="contatti.html">Contatta lo studio</a>')],
    "Ti ricontatteremo per una consulenza sulle soluzioni UnipolSai.",
)

partner_page(
    P["car-adviser.html"], "Car Adviser SRL — Noleggio a lungo termine | Padovani & Partners",
    "Car Adviser SRL: noleggio a lungo termine e servizi per la mobilità di aziende, professionisti e privati.",
    "Noleggio a lungo termine e servizi per la mobilità",
    "Con Car Adviser, la nostra divisione dedicata alla mobilità, ti aiutiamo a gestire il tuo parco veicoli con soluzioni di noleggio innovative e su misura.",
    None,
    """          <h2>La mobilità, senza pensieri</h2>
          <p>Per aziende, professionisti e privati: scegli il veicolo, noi pensiamo a tutto il resto.</p>
""" + features([
        ("Un canone, tutto incluso", "Un’unica rata mensile che comprende assicurazione, manutenzione e assistenza."),
        ("Flotte aziendali", "Gestione completa del parco veicoli, per concentrarti solo sulla tua attività."),
        ("Consulenza su misura", "Ti aiutiamo a scegliere veicolo, durata e chilometraggio più adatti alle tue esigenze."),
        ("Costi certi", "Nessuna sorpresa: spese prevedibili e pianificabili nel tempo."),
    ]),
    [("Area", "Noleggio a lungo termine"), ("Per informazioni", '<a href="contatti.html">Contatta lo studio</a>')],
    "Ti ricontatteremo con una proposta di noleggio su misura.",
)

partner_page(
    P["librici.html"], "Antonino Librici & Partners — Risk management | Padovani & Partners",
    "Antonino Librici & Partners: consulenza di risk management per le imprese.",
    "Consulenza di risk management per la tua impresa",
    "Analizziamo, valutiamo e gestiamo i rischi aziendali per costruire una protezione efficace e sostenibile nel tempo.",
    None,
    """          <h2>Conoscere i rischi per governarli</h2>
          <p>Un programma di risk management ben costruito riduce l’esposizione dell’impresa e rende più efficaci le coperture assicurative.</p>
""" + features([
        ("Analisi dei rischi", "Mappatura dei rischi operativi, finanziari e di responsabilità della tua impresa."),
        ("Strategie di protezione", "Definizione delle coperture e delle misure di prevenzione più adatte."),
        ("Ottimizzazione dei costi", "Garanzie calibrate sui rischi reali, senza sovrapposizioni né scoperture."),
        ("Monitoraggio continuo", "Revisione periodica del programma assicurativo al variare dell’attività."),
    ]),
    [("Area", "Risk management"), ("Per informazioni", '<a href="contatti.html">Contatta lo studio</a>')],
    "Ti ricontatteremo per fissare una consulenza di risk management.",
)

# ================================================================ Contatti
contatti = f"""    <section class="page-hero">
      <div class="wrap">
        <nav class="crumbs" aria-label="Percorso"><a href="index.html">Home</a><span>/</span>Contatti</nav>
        <div class="reveal">
          <span class="eyebrow">Contatti</span>
          <h1>Hai bisogno di una consulenza?</h1>
          <p class="lead">Contattaci o vieni a trovarci: troveremo la soluzione adatta a te.</p>
        </div>
      </div>
    </section>

{contact_section("contatti", "Compila il modulo, ti ricontatteremo al più presto.", "Scrivici o chiamaci", "Raccontaci di cosa hai bisogno: ti metteremo in contatto con il professionista giusto per la tua richiesta.")}

{other_partners(None)}"""
(OUT / "contatti.html").write_text(page(
    "contatti.html", "Contatti | Padovani & Partners",
    "Contatta Padovani & Partners per una consulenza assicurativa, di noleggio a lungo termine o di risk management.",
    contatti), encoding="utf-8")

print("Pagine generate in", OUT.resolve())
