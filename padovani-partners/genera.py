#!/usr/bin/env python3
"""Genera le pagine HTML del sito Padovani & Partners.

Header, menu, card dei partner, form e footer sono definiti una volta sola qui:
modifica questo file e rilancia `python3 genera.py` per aggiornare tutte le pagine.
"""
from pathlib import Path

OUT = Path(__file__).parent
PIVA = "04661560286"

# (file, titolo card, sottotitolo card, logo, alt)
PARTNERS = [
    ("unipol.html", "Unipol", "Assicurazioni", "logo-unipolsai.png", "UnipolSai Assicurazioni"),
    ("axa.html", "AXA Assicurazioni Pegaso SRL", "Protezione Assicurativa Globale", "logo-axa.png", "AXA"),
    ("unibrokers.html", "Unibrokers SRL", "Brokeraggio assicurativo", "logo-unibrokers.png", "Unibrokers"),
    ("car-adviser.html", "Car Adviser SRL", "Noleggio a lungo termine", "logo-car-adviser.png", "Car Adviser – servizi per la mobilità"),
    ("librici.html", "Antonino Librici &amp; Partners", "Consulenza di Risk Management", "logo-librici.png", "Antonino Librici Risk Manager"),
]

NAV = [("index.html", "Home")] + [(p[0], p[1].replace(" Assicurazioni Pegaso SRL", "").replace(" SRL", "").replace(" &amp; Partners", "")) for p in PARTNERS] + [("contatti.html", "Contatti")]

ICONS = {
    "expertise": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 0 1-15.4 6.4"/><path d="M3 12A9 9 0 0 1 18.4 5.6"/><path d="M18 2v4h-4"/><path d="M6 22v-4h4"/><circle cx="12" cy="12" r="3"/></svg>',
    "handshake": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M11 6 7.5 9.5a1.5 1.5 0 0 0 2.1 2.1L12 9.2l5.6 5.6a1.4 1.4 0 0 1-2 2l-.6-.6.1.1a1.4 1.4 0 0 1-2 2l-.4-.4a1.4 1.4 0 0 1-2 2L6 15.3 2 11.3 6.8 6.5a2 2 0 0 1 2.4-.3zM13 6.6 14.8 5a2 2 0 0 1 2.6 0L22 9.4l-3.5 3.5z"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2 4 5v6c0 5 3.4 9.6 8 11 4.6-1.4 8-6 8-11V5zm-1.2 14.2-3.6-3.6 1.4-1.4 2.2 2.2 5-5 1.4 1.4z"/></svg>',
    "thumb": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M2 10h4v11H2zM8 21V10l5-8 1 .5a2 2 0 0 1 1 2.3L14.2 9H20a2 2 0 0 1 2 2.3l-1.5 8A2 2 0 0 1 18.5 21z"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5 9.5 18 20 6"/></svg>',
}


def page(filename, title, description, body):
    current = ' aria-current="page"'
    nav = "\n".join(
        f'        <li><a href="{href}"{current if href == filename else ""}>{label}</a></li>'
        for href, label in NAV
    )
    foot_nav = " ".join(f'<a href="{href}">{label}</a>' for href, label in NAV)
    return f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="icon" href="img/logo-pp.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="index.html" aria-label="Padovani &amp; Partners – Home"><img src="img/logo-pp.png" alt="Padovani &amp; Partners"></a>
      <button class="menu-toggle" aria-label="Apri il menu" aria-expanded="false" aria-controls="main-nav"><span></span><span></span><span></span></button>
      <nav class="main-nav" id="main-nav" aria-label="Menu principale">
        <ul>
{nav}
        </ul>
      </nav>
    </div>
  </header>

  <main>
{body}
  </main>

  <footer class="site-footer">
    <nav aria-label="Collegamenti">{foot_nav}</nav>
    <div>&copy; Padovani &amp; Partners P.IVA {PIVA}</div>
  </footer>

  <button class="to-top" aria-label="Torna su"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m6 15 6-6 6 6"/></svg></button>
  <script src="js/main.js"></script>
</body>
</html>
"""


def features(items, icon=None):
    out = []
    for ic, title, text in items:
        out.append(f"""        <div class="feature reveal">
          {ICONS[icon or ic]}
          <div><h3>{title}</h3><p>{text}</p></div>
        </div>""")
    return '      <div class="features">\n' + "\n".join(out) + "\n      </div>"


def partner_cards(title, exclude=None):
    cards = []
    for href, name, sub, logo, alt in PARTNERS:
        if href == exclude:
            continue
        cards.append(f"""        <article class="card reveal">
          <div class="logo"><img src="img/{logo}" alt="{alt}" loading="lazy"></div>
          <h3>{name}</h3>
          <p class="sub">{sub}</p>
          <a class="btn" href="{href}">Scopri di più</a>
        </article>""")
    return f"""    <section class="section section-band">
      <div class="wrap">
        <h2 class="partners-title">{title}</h2>
        <div class="cards">
{chr(10).join(cards)}
        </div>
      </div>
    </section>"""


def cta(title, button=True):
    btn = '\n        <p><a class="btn btn-green btn-upper" href="contatti.html">Contattaci</a></p>' if button else ""
    return f"""    <section class="section section-dark cta center">
      <div class="wrap">
        <h2>{title}</h2>
        <h3>contattaci o vieni a trovarci</h3>
        <p>Troveremo la soluzione adatta a te.</p>{btn}
      </div>
    </section>"""


def contact(form_name, info_html):
    return f"""    <section class="section section-dark" id="contatti">
      <div class="wrap contact-grid">
        <div class="contact-info reveal">
{info_html}
        </div>
        <form class="form reveal" name="{form_name}" method="POST" data-netlify="true" netlify-honeypot="bot-field">
          <input type="hidden" name="form-name" value="{form_name}">
          <p class="hidden"><label>Non compilare: <input name="bot-field"></label></p>
          <div class="field"><label for="{form_name}-nome">Nome e Cognome</label><input id="{form_name}-nome" name="nome" autocomplete="name" required></div>
          <div class="field"><label for="{form_name}-email">Email</label><input id="{form_name}-email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="{form_name}-tel">Tel</label><input id="{form_name}-tel" name="telefono" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="{form_name}-richiesta">Richiesta (facoltativo)</label><textarea id="{form_name}-richiesta" name="richiesta"></textarea></div>
          <div class="field">
            <label for="{form_name}-antispam">Domanda di sicurezza (Antispam)</label>
            <p class="question">La capitale della Francia?</p>
            <input id="{form_name}-antispam" name="antispam" required>
          </div>
          <button class="btn btn-green" type="submit">Invia</button>
          <p class="form-msg" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>"""


def why(title_html, intro, items):
    return f"""    <section class="section section-dark">
      <div class="wrap">
        <h2 class="section-title">{title_html}</h2>
        {f'<p class="lead">{intro}</p>' if intro else ''}
      </div>
    </section>
    <section class="section section-teal">
      <div class="wrap">
{features(items, icon="check")}
      </div>
    </section>"""


def partner_page(filename, title, description, hero_img, hero_alt, h1, intro_html, why_intro, why_items,
                 extra_html, cta_html, contact_form, contact_info):
    img = f'    <img class="page-hero-img" src="img/{hero_img}" alt="{hero_alt}">\n' if hero_img else ""
    body = f"""{img}    <section class="section section-dark page-intro">
      <div class="wrap">
        <h1>{h1}</h1>
{intro_html}
        <p class="center"><a class="btn btn-upper" href="#contatti">Contattaci</a></p>
      </div>
    </section>
{why("Perché sceglierci?", why_intro, why_items)}
{extra_html}
{cta_html}
{contact(contact_form, contact_info)}
{partner_cards("Proteggi la tua azienda con noi:<br>le assicurazioni che fanno la differenza.", exclude=filename)}"""
    (OUT / filename).write_text(page(filename, title, description, body), encoding="utf-8")


# ---------------------------------------------------------------- Home
home = f"""    <section class="section section-dark hero">
      <div class="wrap">
        <h1>Proteggi il tuo business con soluzioni personalizzate e servizi su misura</h1>
        <p>Benvenuti in <strong>Padovani &amp; Partners</strong>, il punto di riferimento per chi cerca soluzioni personalizzate, servizi dedicati al noleggio a lungo termine e risk manager. Il nostro obiettivo è offrirti la tranquillità di sapere che ogni aspetto della tua attività è protetto, lasciandoti libero di concentrarti sulla crescita del tuo business.</p>
        <p>Con una gamma completa di polizze per aziende, professionisti e privati, una divisione specializzata nel noleggio a lungo termine e consulenza di risk management, siamo al tuo fianco per costruire un futuro sicuro e privo di preoccupazioni. Scopri come possiamo aiutarti a proteggere i tuoi asset e a gestire il tuo parco veicoli con soluzioni innovative e su misura.</p>
        <p class="center"><a class="btn btn-upper" href="contatti.html">Contattaci</a></p>
      </div>
    </section>
    <section class="section section-teal">
      <div class="wrap">
{features([
    ("expertise", "Esperienza e competenza in ambito assicurativo", "Siamo un team di professionisti qualificati con anni di esperienza, pronti a guidarti nel complesso mondo delle assicurazioni aziendali, offrendo consulenza specializzata e affidabile."),
    ("handshake", "Consulenza assicurativa per il tuo successo", "Con le nostre soluzioni, ti aiutiamo a concentrarti sulla crescita del tuo business, lasciando a noi la gestione dei rischi."),
    ("shield", "Coperture personalizzate", "Specializzati nel settore <strong>AZIENDALE</strong>, offriamo polizze su misura che coprono rischi finanziari, responsabilità civile e tutela del patrimonio, per garantire la massima sicurezza alla vostra impresa."),
    ("thumb", "Relazioni basate sulla fiducia", "Offriamo un servizio trasparente e professionale, diventando il tuo partner di riferimento per tutte le esigenze di brokeraggio e consulenza assicurativa."),
])}
      </div>
    </section>
{partner_cards("Proteggi la tua azienda con noi:<br>le soluzioni che fanno la differenza.")}
{cta("Hai bisogno di una consulenza?")}"""
(OUT / "index.html").write_text(page(
    "index.html", "Padovani & Partners",
    "Padovani & Partners: consulenza assicurativa, brokeraggio, noleggio a lungo termine e risk management per aziende, professionisti e privati.",
    home), encoding="utf-8")

# ---------------------------------------------------------------- AXA
partner_page(
    "axa.html", "AXA Assicurazioni – Pegaso SRL | Padovani & Partners",
    "AXA Assicurazioni – Pegaso SRL: protezione assicurativa globale, soluzioni su misura per privati e aziende.",
    "hero-axa.jpg", "Protezione assicurativa globale AXA",
    "Protezione Assicurativa Globale: Soluzioni su Misura per Privati e Aziende",
    "        <p>Offriamo soluzioni assicurative complete e personalizzate, progettate per garantire una protezione globale e rispondere alle specifiche esigenze di ogni cliente, dal privato all’azienda.</p>",
    None,
    [
        (None, "Coperture Sanitarie Complete", "Le nostre polizze sanitarie coprono ogni fase della tutela della salute: dalla prevenzione alla cura, fino all’assistenza. Soluzioni su misura per garantirti sicurezza in ogni momento della vita."),
        (None, "Tutela Legale per Ogni Ambito", "Protezione completa per privati, aziende e holding. Le nostre polizze di tutela legale offrono un supporto affidabile per gestire eventuali controversie e garantire la massima tranquillità."),
        (None, "Polizze Viaggi Personalizzabili", "Viaggia senza pensieri grazie a polizze viaggio con copertura sanitaria <strong>illimitata</strong> e moduli flessibili, adattabili a ogni esigenza personale o professionale."),
        (None, "Sicurezza a 360°", "Siamo il tuo punto di riferimento per la <strong>consulenza assicurativa</strong> e il <strong>brokeraggio</strong>, con un approccio professionale e orientato al cliente. Proteggi ciò che conta di più, con la nostra esperienza al tuo fianco."),
    ],
    "",
    cta("Hai bisogno di una consulenza assicurativa?", button=False),
    "contatti-axa",
    """          <h2>AXA Assicurazioni – Pegaso SRL</h2>
          <p>Referenti aziendali: Nardo Stefano – codice RUI A000331871</p>
          <p>Tel: <a href="tel:+390490982994">049/0982994</a></p>""",
)

# ---------------------------------------------------------------- Unibrokers
UB_RUI = "B000014279"
partner_page(
    "unibrokers.html", "Unibrokers S.r.l. | Padovani & Partners",
    "Unibrokers S.r.l.: servizi di consulenza e brokeraggio assicurativo a Padova dal 1997.",
    "hero-unibrokers.jpg", "Unibrokers – consulenza e brokeraggio assicurativo",
    "Servizi di consulenza e brokeraggio assicurativo",
    f"""        <p><strong>Unibrokers S.r.l.</strong> è una società di brokeraggio assicurativo fondata nel 1997, con sede a Padova, e iscritta al <strong>Registro Unico degli Intermediari</strong> (R.U.I.) con il numero {UB_RUI}, sotto la vigilanza di IVASS.</p>
        <p>Grazie a oltre 20 anni di esperienza nel settore assicurativo, la nostra missione è garantire la <strong>tutela degli interessi del cliente</strong>, offrendo soluzioni su misura per la gestione dei rischi. Analizziamo le esigenze assicurative, proponiamo le migliori coperture contrattuali e collaboriamo con compagnie assicurative italiane e internazionali per garantire il massimo vantaggio. Inoltre, supportiamo i clienti nella gestione dei sinistri, assicurando un’assistenza completa.</p>""",
    "Siamo il tuo partner di fiducia per una consulenza assicurativa completa e personalizzata. La nostra esperienza ci permette di gestire sia le polizze sottoscritte attraverso di noi che quelle già in essere. I principali vantaggi includono:",
    [
        (None, "Gestione completa delle polizze", "Monitoriamo le scadenze contrattuali e ci occupiamo dell’incasso dei premi, trasferendoli alle compagnie competenti."),
        (None, "Aggiornamenti costanti", "Informiamo i clienti su nuovi prodotti assicurativi, modifiche legislative e opportunità di aggiornamento delle polizze in corso."),
        (None, "Personalizzazione", "Concordiamo con i clienti eventuali integrazioni o modifiche, per garantire che le coperture siano sempre adeguate."),
    ],
    """    <section class="section section-dark">
      <div class="wrap">
        <h2 class="section-title">I Vantaggi di Affidarsi a Noi</h2>
        <p class="lead">Scegliere Unibrokers significa beneficiare di un approccio professionale e orientato al cliente, con vantaggi concreti:</p>
        <ul class="bullets">
          <li><strong>Unico referente</strong> per la gestione di tutti i contratti assicurativi.</li>
          <li><strong>Consulenza imparziale</strong>, grazie alla nostra indipendenza dalle compagnie assicurative.</li>
          <li><strong>Trattative flessibili</strong> con le principali compagnie italiane e straniere.</li>
          <li><strong>Ottimizzazione dei costi e delle garanzie</strong>, senza costi aggiuntivi per il cliente.</li>
        </ul>
        <h2 class="section-title" style="margin-top:1.4em">I Nostri Servizi</h2>
        <p class="lead">Unibrokers offre un’ampia gamma di servizi per rispondere a tutte le esigenze assicurative:</p>
        <ul class="bullets">
          <li><strong>Consulenza indipendente</strong>: In qualità di broker assicurativo, operiamo in completa autonomia, selezionando la copertura più adatta e conveniente tra le migliori compagnie sul mercato.</li>
          <li><strong>Nessun costo aggiuntivo</strong>: Il nostro servizio non comporta oneri economici per il cliente, poiché il broker è remunerato direttamente dalle compagnie assicurative.</li>
          <li><strong>Assistenza dedicata</strong>: Offriamo un unico punto di riferimento per tutte le esigenze assicurative, garantendo semplicità e trasparenza nella gestione dei contratti.</li>
          <li><strong>Libertà di scelta</strong>: Trattiamo con compagnie italiane e internazionali per ottenere le migliori condizioni economiche e di copertura.</li>
        </ul>
      </div>
    </section>""",
    """    <section class="section section-teal banner">
      <div class="wrap">
        <h2>Affidati a Unibrokers S.r.l. per la gestione completa e personalizzata delle tue polizze assicurative. Richiedi una consulenza gratuita e scopri come possiamo aiutarti a semplificare e ottimizzare il tuo pacchetto assicurativo.</h2>
      </div>
    </section>""",
    "contatti-unibrokers",
    f"""          <h2>Unibrokers S.r.l.</h2>
          <p><strong>Referenti aziendali:</strong></p>
          <p>NALIN ROBERTA, amministratore unico, broker</p>
          <p>SAGGIN ENRICO, responsabile commerciale</p>
          <p>Tel: <a href="tel:+39049657501">049/657501</a></p>
          <p>ISCR.RUI UNIBROKER: {UB_RUI}</p>""",
)

# ---------------------------------------------------------------- Pagine senza contenuto nel video
# Testi provvisori: da sostituire con quelli definitivi del sito originale.
partner_page(
    "unipol.html", "UnipolSai Assicurazioni | Padovani & Partners",
    "UnipolSai Assicurazioni: polizze per aziende, professionisti e privati.",
    None, "",
    "UnipolSai Assicurazioni: coperture per aziende, professionisti e privati",
    "        <p>Attraverso UnipolSai Assicurazioni offriamo una gamma completa di polizze per proteggere la tua attività, il tuo patrimonio e la tua famiglia, con soluzioni costruite sulle tue esigenze.</p>",
    None,
    [
        (None, "Polizze per le imprese", "Coperture per rischi finanziari, responsabilità civile e tutela del patrimonio aziendale."),
        (None, "Protezione per privati e famiglie", "Soluzioni per la casa, la salute e la persona, per vivere ogni giorno con serenità."),
        (None, "Consulenza dedicata", "Un unico referente che ti segue nella scelta delle coperture e nella gestione dei sinistri."),
    ],
    "",
    cta("Hai bisogno di una consulenza assicurativa?", button=False),
    "contatti-unipol",
    """          <h2>Unipol Assicurazioni</h2>
          <p>Compila il modulo: ti ricontatteremo al più presto per fissare una consulenza.</p>""",
)

partner_page(
    "car-adviser.html", "Car Adviser SRL – Noleggio a lungo termine | Padovani & Partners",
    "Car Adviser SRL: noleggio a lungo termine e servizi per la mobilità di aziende, professionisti e privati.",
    None, "",
    "Noleggio a lungo termine: servizi per la mobilità",
    "        <p>Con Car Adviser SRL, la nostra divisione dedicata alla mobilità, ti aiutiamo a gestire il tuo parco veicoli con soluzioni di noleggio a lungo termine innovative e su misura, per aziende, professionisti e privati.</p>",
    None,
    [
        (None, "Un canone, tutto incluso", "Un’unica rata mensile che comprende assicurazione, manutenzione e assistenza."),
        (None, "Flotte aziendali", "Gestione completa del parco veicoli, per concentrarti solo sulla tua attività."),
        (None, "Consulenza su misura", "Ti aiutiamo a scegliere veicolo, durata e chilometraggio più adatti alle tue esigenze."),
    ],
    "",
    cta("Hai bisogno di una consulenza?", button=False),
    "contatti-car-adviser",
    """          <h2>Car Adviser SRL</h2>
          <p>Compila il modulo: ti ricontatteremo al più presto con una proposta di noleggio.</p>""",
)

partner_page(
    "librici.html", "Antonino Librici & Partners – Risk Management | Padovani & Partners",
    "Antonino Librici & Partners: consulenza di risk management per le imprese.",
    None, "",
    "Consulenza di Risk Management",
    "        <p>Con Antonino Librici &amp; Partners accompagniamo le imprese nell’analisi, nella valutazione e nella gestione dei rischi aziendali, per costruire una protezione efficace e sostenibile nel tempo.</p>",
    None,
    [
        (None, "Analisi dei rischi", "Mappatura dei rischi operativi, finanziari e di responsabilità della tua impresa."),
        (None, "Strategie di protezione", "Definizione delle coperture e delle misure di prevenzione più adatte."),
        (None, "Monitoraggio continuo", "Revisione periodica del programma assicurativo al variare dell’attività."),
    ],
    "",
    cta("Hai bisogno di una consulenza?", button=False),
    "contatti-librici",
    """          <h2>Antonino Librici &amp; Partners</h2>
          <p>Compila il modulo: ti ricontatteremo al più presto per fissare una consulenza.</p>""",
)

# ---------------------------------------------------------------- Contatti
contatti = f"""    <section class="section section-dark page-intro">
      <div class="wrap">
        <h1>Contattaci</h1>
        <p class="center">Hai bisogno di una consulenza? Contattaci o vieni a trovarci: troveremo la soluzione adatta a te.</p>
      </div>
    </section>
{contact("contatti", '''          <h2>Padovani &amp; Partners</h2>
          <p><strong>AXA Assicurazioni – Pegaso SRL</strong><br>Tel: <a href="tel:+390490982994">049/0982994</a></p>
          <p><strong>Unibrokers S.r.l.</strong><br>Tel: <a href="tel:+39049657501">049/657501</a></p>
          <p>P.IVA ''' + PIVA + '''</p>''')}
{partner_cards("Proteggi la tua azienda con noi:<br>le soluzioni che fanno la differenza.")}"""
(OUT / "contatti.html").write_text(page(
    "contatti.html", "Contatti | Padovani & Partners",
    "Contatta Padovani & Partners per una consulenza assicurativa, di noleggio a lungo termine o di risk management.",
    contatti), encoding="utf-8")

print("Pagine generate in", OUT.resolve())
