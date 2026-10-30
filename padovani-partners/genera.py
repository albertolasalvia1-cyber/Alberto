#!/usr/bin/env python3
"""Genera le pagine HTML del sito Padovani & Partners.

Header, menu, elenco società, form e footer sono definiti una volta sola qui:
modifica questo file e rilancia `python3 genera.py` per aggiornare tutte le pagine.
"""
from pathlib import Path

OUT = Path(__file__).parent
PIVA = "04661560286"

ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M1 8h13M9 3l5 5-5 5"/></svg>'
CHEV = '<svg class="chev" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="m2 4 4 4 4-4"/></svg>'
UP = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M8 14V2M3 7l5-5 5 5"/></svg>'

# Società e partner. "tall" = logo quasi quadrato (AXA), mostrato più alto.
COMPANIES = [
    dict(file="unipol.html", name="UnipolSai Assicurazioni", short="Unipol", sector="Assicurazioni", logo="logo-unipolsai",
         blurb="Polizze per imprese, professionisti e famiglie con uno dei principali gruppi assicurativi italiani."),
    dict(file="axa.html", name="AXA Assicurazioni – Pegaso SRL", short="AXA", sector="Protezione assicurativa globale", logo="logo-axa", tall=True,
         blurb="Salute, tutela legale e viaggi: soluzioni complete e personalizzate, dal privato all’azienda."),
    dict(file="unibrokers.html", name="Unibrokers S.r.l.", short="Unibrokers", sector="Brokeraggio assicurativo", logo="logo-unibrokers",
         blurb="Broker indipendente dal 1997, iscritto al RUI: le migliori coperture sul mercato, senza costi aggiuntivi per il cliente."),
    dict(file="car-adviser.html", name="Car Adviser SRL", short="Car Adviser", sector="Noleggio a lungo termine", logo="logo-car-adviser",
         blurb="Servizi per la mobilità: noleggio a lungo termine e gestione del parco veicoli aziendale."),
    dict(file="librici.html", name="Antonino Librici & Partners", short="Antonino Librici", sector="Consulenza di risk management", logo="logo-librici",
         blurb="Analisi, valutazione e gestione dei rischi d’impresa, per una protezione efficace nel tempo."),
]
BY_FILE = {c["file"]: c for c in COMPANIES}

PHONES = [
    ("AXA Assicurazioni – Pegaso SRL", "049 098 2994", "+390490982994"),
    ("Unibrokers S.r.l.", "049 657 501", "+39049657501"),
]


def esc(s):
    return s.replace("&", "&amp;")


def logo(c, dark=False, lazy=False):
    src = f'img/{c["logo"]}{"-dark" if dark else ""}.png'
    cls = ' class="tall"' if c.get("tall") else ""
    load = ' loading="lazy"' if lazy else ""
    return f'<img src="{src}" alt="{esc(c["name"])}"{cls}{load}>'


def brand_logo():
    return '<span class="logo-mark" aria-hidden="true">PP</span><span class="logo-name">Padovani<br>&amp; Partners</span>'


# ---------------------------------------------------------------- struttura comune
def header(current):
    def cur(f):
        return ' aria-current="page"' if f == current else ""
    links = "\n".join(
        f'                  <li><a href="{c["file"]}"{cur(c["file"])}><b>{esc(c["name"])}</b><span>{esc(c["sector"])}</span></a></li>'
        for c in COMPANIES
    )
    return f"""  <header class="site-header">
    <div class="wrap">
      <a class="logo" href="index.html" aria-label="Padovani &amp; Partners, home">{brand_logo()}</a>
      <nav class="main-nav" id="main-nav" aria-label="Menu principale">
        <ul class="nav-list">
          <li><a class="nav-link" href="index.html#chi-siamo">Chi siamo</a></li>
          <li class="dd">
            <button class="nav-link" aria-expanded="false" aria-controls="dd-societa">Società e partner {CHEV}</button>
            <div class="dd-panel" id="dd-societa">
              <div class="wrap dd-inner">
                <div class="dd-intro">
                  <span class="label">Società e partner</span>
                  <p>Un unico interlocutore per assicurazione, brokeraggio, mobilità aziendale e gestione del rischio.</p>
                  <a class="more" href="index.html#societa">Panoramica {ARROW}</a>
                </div>
                <ul class="dd-links">
{links}
                </ul>
              </div>
            </div>
          </li>
          <li><a class="nav-link" href="index.html#metodo">Metodo</a></li>
          <li><a class="nav-link" href="contatti.html"{cur("contatti.html")}>Contatti</a></li>
          <li class="nav-cta-li"><a class="btn nav-cta" href="contatti.html#richiesta">Richiedi una consulenza</a></li>
        </ul>
      </nav>
      <button class="menu-toggle" aria-expanded="false" aria-controls="main-nav">Menu <span class="bars" aria-hidden="true"></span></button>
    </div>
  </header>"""


def footer():
    comp = "\n".join(f'            <li><a href="{c["file"]}">{esc(c["name"])}</a></li>' for c in COMPANIES)
    tel = "\n".join(f'            <li>{esc(n)}<br><a href="tel:{t}">{d}</a></li>' for n, d, t in PHONES)
    return f"""  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <a class="logo" href="index.html" aria-label="Padovani &amp; Partners, home">{brand_logo()}</a>
          <p>Soluzioni assicurative, brokeraggio, noleggio a lungo termine e risk management per aziende, professionisti e privati.</p>
        </div>
        <div>
          <h4>Padovani &amp; Partners</h4>
          <ul>
            <li><a href="index.html#chi-siamo">Chi siamo</a></li>
            <li><a href="index.html#societa">Società e partner</a></li>
            <li><a href="index.html#metodo">Metodo</a></li>
            <li><a href="contatti.html">Contatti</a></li>
          </ul>
        </div>
        <div>
          <h4>Società e partner</h4>
          <ul>
{comp}
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
        <span>&copy; Padovani &amp; Partners — P.IVA {PIVA}</span>
        <a href="contatti.html#richiesta">Richiedi una consulenza</a>
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
  <meta name="theme-color" content="#0f2a24">
  <link rel="icon" href="img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,300;8..60,400;8..60,500&display=swap" rel="stylesheet">
  <script>document.documentElement.classList.add('js');</script>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
{header(filename)}

  <main>
{body}
  </main>

{footer()}

  <button class="to-top" aria-label="Torna all’inizio della pagina">{UP}</button>
  <script src="js/main.js"></script>
</body>
</html>
"""


# ---------------------------------------------------------------- blocchi
def companies_list():
    rows = "\n".join(
        f"""          <li><a class="company" href="{c["file"]}">
            <span class="brand">{logo(c, dark=True, lazy=True)}</span>
            <div class="text"><h3>{esc(c["name"])}</h3><span class="sector">{esc(c["sector"])}</span></div>
            <p>{c["blurb"]}</p>
            <span class="go" aria-hidden="true">{ARROW}</span>
          </a></li>"""
        for c in COMPANIES
    )
    return f'        <ul class="companies">\n{rows}\n        </ul>'


def contact_band():
    phones = "\n".join(f'            <a href="tel:{t}"><small>{esc(n)}</small><b>{d}</b></a>' for n, d, t in PHONES)
    return f"""    <section class="contact-band on-dark">
      <div class="wrap">
        <div>
          <span class="label">Contatti</span>
          <h2>Hai bisogno di una consulenza?</h2>
          <p class="lead">Contattaci o vieni a trovarci. Troveremo la soluzione adatta a te.</p>
        </div>
        <div>
          <div class="phones">
{phones}
          </div>
          <a class="btn btn-light" href="contatti.html#richiesta">Richiedi una consulenza {ARROW}</a>
        </div>
      </div>
    </section>"""


def form(name, subject):
    return f"""        <form class="form" name="{name}" method="POST" data-netlify="true" netlify-honeypot="bot-field">
          <input type="hidden" name="form-name" value="{name}">
          <input type="hidden" name="oggetto" value="{subject}">
          <p class="hidden"><label>Non compilare: <input name="bot-field"></label></p>
          <div class="form-row">
            <div class="field"><label for="{name}-nome">Nome e cognome</label><input id="{name}-nome" name="nome" autocomplete="name" required></div>
            <div class="field"><label for="{name}-tel">Telefono</label><input id="{name}-tel" name="telefono" type="tel" autocomplete="tel"></div>
          </div>
          <div class="field"><label for="{name}-email">Email</label><input id="{name}-email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="{name}-richiesta">Richiesta <small>(facoltativo)</small></label><textarea id="{name}-richiesta" name="richiesta"></textarea></div>
          <div class="field"><label for="{name}-antispam">Domanda di sicurezza: qual è la capitale della Francia?</label><input id="{name}-antispam" name="antispam" required></div>
          <label class="consent"><input type="checkbox" name="consenso" required> Acconsento al trattamento dei dati personali per essere ricontattato in merito alla richiesta.</label>
          <button class="btn" type="submit">Invia la richiesta {ARROW}</button>
          <p class="form-msg" role="status" aria-live="polite"></p>
        </form>"""


def contact_section(name, subject, phones, cls="alt"):
    rows = "\n".join(f'            <a href="tel:{t}"><small>{esc(n)}</small><b>{d}</b></a>' for n, d, t in phones)
    return f"""    <section class="section {cls}" id="richiesta">
      <div class="wrap contact-grid">
        <div class="intro">
          <span class="label">Richiesta di consulenza</span>
          <h2>Parliamo delle tue esigenze</h2>
          <p>Compila il modulo: sarai ricontattato al più presto per fissare un appuntamento, senza impegno.</p>
          <div class="contact-phones">
{rows}
          </div>
        </div>
{form(name, subject)}
      </div>
    </section>"""


def others(exclude):
    items = "\n".join(
        f"""          <a href="{c["file"]}"><span class="brand">{logo(c, dark=True, lazy=True)}</span><span>{esc(c["sector"])}</span><span class="more">{esc(c["short"])} {ARROW}</span></a>"""
        for c in COMPANIES if c["file"] != exclude
    )
    return f"""    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <div><span class="label">Società e partner</span><h2>Le altre realtà con cui lavoriamo</h2></div>
          <p>Proteggi la tua azienda con noi: le soluzioni che fanno la differenza.</p>
        </div>
        <div class="others">
{items}
        </div>
      </div>
    </section>"""


def features(items):
    cells = "\n".join(f"            <div><h3>{t}</h3><p>{d}</p></div>" for t, d in items)
    return f'          <div class="features">\n{cells}\n          </div>'


def bullet_list(items):
    lis = "\n".join(f"            <li>{i}</li>" for i in items)
    return f'          <ul class="list">\n{lis}\n          </ul>'


def company_page(c, title, description, h1, lead, content, aside, subject):
    rows = "\n".join(f"              <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in aside)
    phones = [x for x in PHONES if x[0] == c["name"]] or PHONES
    body = f"""    <section class="page-head on-dark">
      <div class="page-globe" aria-hidden="true"><canvas data-globe="small"></canvas></div>
      <div class="wrap">
        <nav class="crumbs intro" aria-label="Percorso"><a href="index.html">Home</a><span>/</span><a href="index.html#societa">Società e partner</a><span>/</span>{esc(c["short"])}</nav>
        <div class="page-head-grid">
          <div>
            <span class="label intro" style="--d:.1s">{esc(c["sector"])}</span>
            <h1 class="split">{h1}</h1>
            <p class="lead intro" style="--d:.7s">{lead}</p>
          </div>
          <div class="brand intro" style="--d:.8s">{logo(c)}</div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap content-grid">
        <div class="prose">
{content}
        </div>
        <aside class="sidebar">
          <span class="label">Riferimenti</span>
          <h3>{esc(c["name"])}</h3>
          <p class="sector">{esc(c["sector"])}</p>
          <dl>
{rows}
          </dl>
          <a class="btn" href="#richiesta">Richiedi una consulenza</a>
        </aside>
      </div>
    </section>

{contact_section("richiesta-" + c["file"].removesuffix(".html"), subject, phones)}

{others(c["file"])}"""
    (OUT / c["file"]).write_text(page(c["file"], title, description, body), encoding="utf-8")


# ================================================================ Home
strip = "\n".join(
    f'          <a href="{c["file"]}" data-reveal style="--d:{0.9 + i * 0.08:.2f}s"><span class="sector">{esc(c["sector"])}</span><b>{esc(c["name"])}</b>{ARROW}</a>'
    for i, c in enumerate(COMPANIES)
)
cards = "\n".join(
    f"""          <a class="card3d" href="{c["file"]}" data-reveal style="--d:{i * 0.08:.2f}s">
            <span class="sheen" aria-hidden="true"></span>
            <span class="brand">{logo(c, lazy=True)}</span>
            <span class="body">
              <span class="sector">{esc(c["sector"])}</span>
              <h3>{esc(c["name"])}</h3>
              <p>{c["blurb"]}</p>
            </span>
            <span class="more">Scopri {ARROW}</span>
          </a>"""
    for i, c in enumerate(COMPANIES)
)
pillars = [
    ("Esperienza e competenza", "Un team di professionisti qualificati, con anni di esperienza, pronti a guidarti nel complesso mondo delle assicurazioni aziendali con una consulenza specializzata e affidabile."),
    ("Consulenza per il tuo successo", "Con le nostre soluzioni ti aiutiamo a concentrarti sulla crescita del tuo business, lasciando a noi la gestione dei rischi."),
    ("Coperture personalizzate", "Specializzati nel settore aziendale, offriamo polizze su misura per rischi finanziari, responsabilità civile e tutela del patrimonio."),
    ("Relazioni basate sulla fiducia", "Un servizio trasparente e professionale: il tuo partner di riferimento per ogni esigenza di brokeraggio e consulenza assicurativa."),
]
pillars_html = "\n".join(
    f'          <div class="pillar" data-reveal style="--d:{i * 0.08:.2f}s"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(pillars)
)
facts = [
    ("5", None, "Società e partner", "per assicurazione, brokeraggio, mobilità e gestione del rischio"),
    ("1997", "1975", "Anno di fondazione", "di Unibrokers S.r.l., broker iscritto al Registro Unico degli Intermediari"),
    ("20", None, "Anni di esperienza", "nel brokeraggio assicurativo, a tutela degli interessi del cliente", ),
]
def fact(i, n, fr, t, d):
    start = f' data-from="{fr}"' if fr else ""
    plus = "<sup>+</sup>" if n == "20" else ""
    return f'          <div class="fact" data-reveal style="--d:{i * 0.1:.1f}s"><span class="num"><span data-count="{n}"{start}>{n}</span>{plus}</span><h3>{t}</h3><p>{d}</p></div>'


facts_html = "\n".join(fact(i, *f) for i, f in enumerate(facts))
steps = [
    ("Analisi", "Studiamo l’attività e le coperture già in essere per individuare rischi ed esigenze reali."),
    ("Proposta", "Selezioniamo le soluzioni più adatte e convenienti tra compagnie italiane e internazionali."),
    ("Gestione", "Seguiamo scadenze, premi e aggiornamenti normativi, con un unico referente per tutti i contratti."),
    ("Assistenza", "Affianchiamo il cliente nella gestione dei sinistri, con un’assistenza completa."),
]
steps_html = "\n".join(
    f'          <li data-reveal style="--d:{i * 0.08:.2f}s"><span class="dot" aria-hidden="true"></span><span class="phase">Fase {i + 1}</span><h3>{t}</h3><p>{d}</p></li>'
    for i, (t, d) in enumerate(steps)
)

home = f"""    <section class="hero on-dark">
      <div class="hero-globe" aria-hidden="true"><canvas data-globe="hub"></canvas></div>
      <div class="wrap hero-content">
        <span class="label intro" style="--d:.1s">Padovani &amp; Partners</span>
        <h1 class="split">Proteggi il tuo business con soluzioni personalizzate e servizi su misura</h1>
        <p class="lead intro" style="--d:.75s">Il punto di riferimento per chi cerca soluzioni assicurative personalizzate, servizi dedicati al noleggio a lungo termine e consulenza di risk management.</p>
        <div class="hero-actions intro" style="--d:.85s">
          <a class="btn btn-light" href="contatti.html#richiesta">Richiedi una consulenza</a>
          <a class="more" href="#societa">Società e partner {ARROW}</a>
        </div>
      </div>
      <div class="wrap">
        <nav class="hero-strip" aria-label="Società e partner">
{strip}
        </nav>
      </div>
    </section>

    <section class="section" id="chi-siamo">
      <div class="wrap">
        <span class="label" data-reveal>Chi siamo</span>
        <p class="statement-fill">Il nostro obiettivo è offrirti la tranquillità di sapere che ogni aspetto della tua attività è protetto, lasciandoti libero di concentrarti sulla crescita del tuo business.</p>
        <div class="about">
          <h2 data-reveal>Un unico punto di riferimento per la protezione dell’impresa</h2>
          <p data-reveal style="--d:.1s">Con una gamma completa di polizze per aziende, professionisti e privati, una divisione specializzata nel noleggio a lungo termine e la consulenza di risk management, siamo al tuo fianco per costruire un futuro sicuro e privo di preoccupazioni: per proteggere i tuoi asset e gestire il tuo parco veicoli con soluzioni innovative e su misura.</p>
        </div>
        <div class="pillars">
{pillars_html}
        </div>
      </div>
    </section>

    <section class="section alt facts-section">
      <div class="wrap facts">
{facts_html}
      </div>
    </section>

    <section class="section companies-3d on-dark" id="societa">
      <div class="wrap">
        <div class="section-head">
          <div><span class="label" data-reveal>Società e partner</span><h2 data-reveal style="--d:.08s">Proteggi la tua azienda con noi: le soluzioni che fanno la differenza</h2></div>
          <p data-reveal style="--d:.16s">Un unico interlocutore per assicurazione, brokeraggio, mobilità aziendale e gestione del rischio, insieme a partner selezionati.</p>
        </div>
      </div>
      <div class="wrap cards3d-wrap">
        <div class="cards3d">
{cards}
        </div>
      </div>
    </section>

    <section class="section" id="metodo">
      <div class="wrap">
        <div class="section-head">
          <div><span class="label" data-reveal>Metodo</span><h2 data-reveal style="--d:.08s">Dall’analisi dei rischi all’assistenza sui sinistri</h2></div>
          <p data-reveal style="--d:.16s">Un percorso chiaro, seguito da un unico referente in ogni fase.</p>
        </div>
        <div class="steps-wrap">
          <div class="track" aria-hidden="true"><span></span></div>
          <ol class="steps">
{steps_html}
          </ol>
        </div>
      </div>
    </section>

{contact_band()}"""
(OUT / "index.html").write_text(page(
    "index.html", "Padovani & Partners — Consulenza assicurativa, brokeraggio e risk management",
    "Padovani & Partners: consulenza assicurativa, brokeraggio, noleggio a lungo termine e risk management per aziende, professionisti e privati.",
    home), encoding="utf-8")

# ================================================================ AXA
company_page(
    BY_FILE["axa.html"], "AXA Assicurazioni – Pegaso SRL | Padovani & Partners",
    "AXA Assicurazioni – Pegaso SRL: protezione assicurativa globale, soluzioni su misura per privati e aziende.",
    "Protezione assicurativa globale: soluzioni su misura per privati e aziende",
    "Soluzioni assicurative complete e personalizzate, progettate per garantire una protezione globale e rispondere alle specifiche esigenze di ogni cliente, dal privato all’azienda.",
    """          <span class="label">Perché sceglierci</span>
          <h2>Sicurezza a 360°</h2>
          <p>Siamo il tuo punto di riferimento per la consulenza assicurativa e il brokeraggio, con un approccio professionale e orientato al cliente. Proteggi ciò che conta di più, con la nostra esperienza al tuo fianco.</p>
""" + features([
        ("Coperture sanitarie complete", "Le nostre polizze sanitarie coprono ogni fase della tutela della salute: dalla prevenzione alla cura, fino all’assistenza. Soluzioni su misura per garantirti sicurezza in ogni momento della vita."),
        ("Tutela legale per ogni ambito", "Protezione completa per privati, aziende e holding. Le polizze di tutela legale offrono un supporto affidabile per gestire eventuali controversie e garantire la massima tranquillità."),
        ("Polizze viaggi personalizzabili", "Viaggia senza pensieri grazie a polizze viaggio con copertura sanitaria illimitata e moduli flessibili, adattabili a ogni esigenza personale o professionale."),
        ("Un unico interlocutore", "Un referente dedicato per tutte le coperture, dalla scelta della polizza alla gestione dei sinistri."),
    ]),
    [("Referente aziendale", "Nardo Stefano"), ("Codice RUI", "A000331871"), ("Telefono", '<a href="tel:+390490982994">049 098 2994</a>')],
    "AXA Assicurazioni – Pegaso SRL",
)

# ================================================================ Unibrokers
UB_RUI = "B000014279"
company_page(
    BY_FILE["unibrokers.html"], "Unibrokers S.r.l. — Brokeraggio assicurativo | Padovani & Partners",
    "Unibrokers S.r.l.: servizi di consulenza e brokeraggio assicurativo a Padova dal 1997.",
    "Servizi di consulenza e brokeraggio assicurativo",
    "Dal 1997 tuteliamo gli interessi dei nostri clienti: analizziamo le esigenze, selezioniamo le coperture migliori sul mercato e assistiamo nella gestione dei sinistri.",
    f"""          <span class="label">La società</span>
          <h2>Oltre vent’anni di brokeraggio indipendente</h2>
          <p><strong>Unibrokers S.r.l.</strong> è una società di brokeraggio assicurativo fondata nel 1997, con sede a Padova, iscritta al Registro Unico degli Intermediari (R.U.I.) con il numero {UB_RUI}, sotto la vigilanza di IVASS.</p>
          <p>La nostra missione è garantire la tutela degli interessi del cliente, offrendo soluzioni su misura per la gestione dei rischi. Analizziamo le esigenze assicurative, proponiamo le migliori coperture contrattuali e collaboriamo con compagnie italiane e internazionali per garantire il massimo vantaggio. Supportiamo inoltre i clienti nella gestione dei sinistri, assicurando un’assistenza completa.</p>
          <h2>Perché sceglierci</h2>
          <p>Siamo il tuo partner di fiducia per una consulenza assicurativa completa e personalizzata. La nostra esperienza ci permette di gestire sia le polizze sottoscritte attraverso di noi sia quelle già in essere.</p>
""" + features([
        ("Gestione completa delle polizze", "Monitoriamo le scadenze contrattuali e ci occupiamo dell’incasso dei premi, trasferendoli alle compagnie competenti."),
        ("Aggiornamenti costanti", "Informiamo i clienti su nuovi prodotti assicurativi, modifiche legislative e opportunità di aggiornamento delle polizze in corso."),
        ("Personalizzazione", "Concordiamo con i clienti eventuali integrazioni o modifiche, per garantire che le coperture siano sempre adeguate."),
        ("Nessun costo aggiuntivo", "Il servizio non comporta oneri economici per il cliente: il broker è remunerato direttamente dalle compagnie assicurative."),
    ]) + """
          <h2>I vantaggi di affidarsi a noi</h2>
""" + bullet_list([
        "<strong>Unico referente</strong> per la gestione di tutti i contratti assicurativi.",
        "<strong>Consulenza imparziale</strong>, grazie all’indipendenza dalle compagnie assicurative.",
        "<strong>Trattative flessibili</strong> con le principali compagnie italiane e straniere.",
        "<strong>Ottimizzazione dei costi e delle garanzie</strong>, senza costi aggiuntivi per il cliente.",
    ]) + """
          <h2>I nostri servizi</h2>
""" + bullet_list([
        "<strong>Consulenza indipendente</strong> — in qualità di broker operiamo in completa autonomia, selezionando la copertura più adatta e conveniente tra le migliori compagnie sul mercato.",
        "<strong>Assistenza dedicata</strong> — un unico punto di riferimento per tutte le esigenze assicurative, con semplicità e trasparenza nella gestione dei contratti.",
        "<strong>Libertà di scelta</strong> — trattiamo con compagnie italiane e internazionali per ottenere le migliori condizioni economiche e di copertura.",
    ]) + """
          <p class="statement">Affidati a Unibrokers per la gestione completa e personalizzata delle tue polizze. Richiedi una consulenza gratuita: ti aiuteremo a semplificare e ottimizzare il tuo pacchetto assicurativo.</p>""",
    [("Amministratore unico, broker", "Nalin Roberta"), ("Responsabile commerciale", "Saggin Enrico"),
     ("Telefono", '<a href="tel:+39049657501">049 657 501</a>'), ("Iscrizione RUI", UB_RUI)],
    "Unibrokers S.r.l.",
)

# ================================================================ Pagine non visibili nel video
# Testi provvisori: da sostituire con quelli definitivi.
company_page(
    BY_FILE["unipol.html"], "UnipolSai Assicurazioni | Padovani & Partners",
    "UnipolSai Assicurazioni: polizze per aziende, professionisti e privati.",
    "Coperture assicurative per imprese, professionisti e famiglie",
    "Attraverso UnipolSai Assicurazioni offriamo una gamma completa di polizze per proteggere l’attività, il patrimonio e le persone.",
    """          <span class="label">Soluzioni</span>
          <h2>Una consulenza costruita sulle tue esigenze</h2>
          <p>Ti accompagniamo nella scelta delle coperture più adatte, con un’analisi attenta delle esigenze e un unico referente per ogni necessità.</p>
""" + features([
        ("Imprese", "Coperture per rischi finanziari, responsabilità civile e tutela del patrimonio aziendale."),
        ("Professionisti", "Responsabilità civile professionale e tutela dell’attività, su misura per la professione."),
        ("Privati e famiglie", "Soluzioni per la casa, la salute e la persona."),
        ("Sinistri", "Assistenza in ogni fase, dalla denuncia alla liquidazione."),
    ]),
    [("Ambito", "Assicurazioni"), ("Informazioni", '<a href="contatti.html">Contatta lo studio</a>')],
    "UnipolSai Assicurazioni",
)

company_page(
    BY_FILE["car-adviser.html"], "Car Adviser SRL — Noleggio a lungo termine | Padovani & Partners",
    "Car Adviser SRL: noleggio a lungo termine e servizi per la mobilità di aziende, professionisti e privati.",
    "Noleggio a lungo termine e servizi per la mobilità",
    "La divisione dedicata alla mobilità: soluzioni di noleggio a lungo termine e gestione del parco veicoli, per aziende, professionisti e privati.",
    """          <span class="label">Mobilità</span>
          <h2>Il parco veicoli, senza pensieri</h2>
          <p>Scegli il veicolo: al resto pensiamo noi, con soluzioni innovative e su misura.</p>
""" + features([
        ("Un canone, tutto incluso", "Un’unica rata mensile che comprende assicurazione, manutenzione e assistenza."),
        ("Flotte aziendali", "Gestione completa del parco veicoli, per concentrarsi sull’attività."),
        ("Consulenza su misura", "Scelta di veicolo, durata e chilometraggio più adatti alle esigenze."),
        ("Costi certi", "Spese prevedibili e pianificabili nel tempo."),
    ]),
    [("Ambito", "Noleggio a lungo termine"), ("Informazioni", '<a href="contatti.html">Contatta lo studio</a>')],
    "Car Adviser SRL",
)

company_page(
    BY_FILE["librici.html"], "Antonino Librici & Partners — Risk management | Padovani & Partners",
    "Antonino Librici & Partners: consulenza di risk management per le imprese.",
    "Consulenza di risk management per l’impresa",
    "Analisi, valutazione e gestione dei rischi aziendali, per costruire una protezione efficace e sostenibile nel tempo.",
    """          <span class="label">Risk management</span>
          <h2>Conoscere i rischi per governarli</h2>
          <p>Un programma di risk management ben costruito riduce l’esposizione dell’impresa e rende più efficaci le coperture assicurative.</p>
""" + features([
        ("Analisi dei rischi", "Mappatura dei rischi operativi, finanziari e di responsabilità dell’impresa."),
        ("Strategie di protezione", "Definizione delle coperture e delle misure di prevenzione più adatte."),
        ("Ottimizzazione dei costi", "Garanzie calibrate sui rischi reali, senza sovrapposizioni né scoperture."),
        ("Monitoraggio continuo", "Revisione periodica del programma assicurativo al variare dell’attività."),
    ]),
    [("Ambito", "Risk management"), ("Informazioni", '<a href="contatti.html">Contatta lo studio</a>')],
    "Antonino Librici & Partners",
)

# ================================================================ Contatti
contatti = f"""    <section class="page-head on-dark">
      <div class="page-globe" aria-hidden="true"><canvas data-globe="small"></canvas></div>
      <div class="wrap">
        <nav class="crumbs intro" aria-label="Percorso"><a href="index.html">Home</a><span>/</span>Contatti</nav>
        <span class="label intro" style="--d:.1s">Contatti</span>
        <h1 class="split">Hai bisogno di una consulenza?</h1>
        <p class="lead intro" style="--d:.6s">Contattaci o vieni a trovarci. Troveremo la soluzione adatta a te.</p>
      </div>
    </section>

{contact_section("richiesta-generale", "Richiesta generale", PHONES, cls="")}

    <section class="section alt">
      <div class="wrap">
        <div class="section-head">
          <div><span class="label">Società e partner</span><h2>Le realtà con cui lavoriamo</h2></div>
          <p>Proteggi la tua azienda con noi: le soluzioni che fanno la differenza.</p>
        </div>
{companies_list()}
      </div>
    </section>"""
(OUT / "contatti.html").write_text(page(
    "contatti.html", "Contatti | Padovani & Partners",
    "Contatta Padovani & Partners per una consulenza assicurativa, di noleggio a lungo termine o di risk management.",
    contatti), encoding="utf-8")

print("Pagine generate in", OUT.resolve())
