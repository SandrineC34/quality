#!/usr/bin/env python3
"""
Génère les pages HTML de la cartographie des processus à partir de fichiers Markdown.

Cette version produit la mise en page « moderne » (cf. Management.html) :
    - bandeau de navigation + hero du processus
    - sidebar (remplie par js/sidebar.js) + contenu principal
    - sections avec identifiants (general, finalite, parties, io, docs, ressources,
      activites, perf, risques, opport, logi-spN) utilisés par la sidebar

Usage :
    python3 build.py                      # convertit tous les *.md de html/Processus/ (sauf ceux commençant par _)
    python3 build.py Management.md        # un seul fichier (nom, nom sans extension, ou chemin)
    python3 build.py -o ../processus/     # dossier de sortie
    python3 build.py --css-prefix ../../../   # préfixe des chemins css/js (défaut : calculé automatiquement)

Format du .md : voir les commentaires de chaque section_xxx() ci-dessous
(les sections sont repérées par des mots-clés dans les titres « ## »).
"""
import argparse, html, os, re, sys, unicodedata, textwrap
from pathlib import Path


# ═════════════════════════════════════════════════════════════════════
#  1. UTILITAIRES GÉNÉRAUX
# ═════════════════════════════════════════════════════════════════════

def esc(s):
    """Échappe le texte pour l'insérer dans du HTML (&, <, >). Les guillemets restent tels quels."""
    return html.escape(s or "", quote=False)


def esc_attr(s):
    """Même chose, mais pour une valeur d'attribut HTML (échappe aussi les guillemets)."""
    return html.escape(s or "", quote=True)


def strip_acc(s):
    """Retire les accents et passe en minuscules : 'Étape' -> 'etape' (sert à comparer sans souci d'accents)."""
    sans_accent = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return sans_accent.lower()


def spc(n):
    """Classe CSS d'un sous-processus : les classes sp1..sp3 existent, au-delà on recommence le cycle."""
    return ((n - 1) % 3) + 1


def spnum(s):
    """Extrait le premier nombre d'un texte ('SP2' -> 2). Retourne 1 s'il n'y en a pas."""
    m = re.search(r"\d+", s or "")
    return int(m.group()) if m else 1


def split(line, n=None):
    """
    Découpe une ligne « a | b | c » sur les barres verticales entourées d'espaces.
    - si n est donné : on obtient toujours exactement n champs
      (champs manquants = chaîne vide ; les « | » en trop restent dans le dernier champ).
    """
    line = re.sub(r"\s\|$", "", line.rstrip())            # barre finale orpheline : « a | b | » -> « a | b »
    if n:
        parts = re.split(r"\s\|\s", line, maxsplit=n - 1)  # au plus n champs
    else:
        parts = re.split(r"\s\|\s", line)
    parts = [p.strip() for p in parts]
    if n:
        parts += [""] * (n - len(parts))                   # complète avec des champs vides
    return parts


# Couleur du titre de chaque cadre de logigramme (une par classe sp1..sp3)
SP_COLORS = {1: "#1e40af", 2: "#065f46", 3: "#5b21b6"}

# Avertissements collectés pendant la génération d'une page (affichés à la fin)
warnings = []


def warn(msg):
    """Enregistre un avertissement non bloquant."""
    warnings.append(msg)


# ═════════════════════════════════════════════════════════════════════
#  2. LECTURE DU FICHIER MARKDOWN
# ═════════════════════════════════════════════════════════════════════

def parse_md(path):
    """
    Lit un .md et retourne (meta, sections) :
      - meta     : dict issu de l'en-tête YAML simplifié entre deux lignes « --- »
      - sections : dict {titre du « ## » : [lignes de la section]}
    """
    # utf-8-sig : tolère un éventuel BOM en début de fichier
    text = Path(path).read_text(encoding="utf-8-sig")
    meta, body = {}, text

    # --- en-tête « --- ... --- » (métadonnées) ---
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            # on ignore les lignes sans « : » et les commentaires (#)
            if ":" in line and not line.strip().startswith("#"):
                k, v = line.split(":", 1)
                # clé normalisée : sans accent, minuscules, « - » et espaces -> « _ »
                cle = re.sub(r"[-\s]+", "_", strip_acc(k.strip()))
                # valeur : on retire un éventuel commentaire de fin de ligne (« valeur   # note »)
                meta[cle] = re.sub(r"\s+#.*$", "", v.strip())
        body = text[m.end():]                              # le reste du fichier = corps

    # --- commentaires HTML <!-- ... --> ignorés ---
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)

    # --- découpage du corps en sections « ## Titre » ---
    sections, cur = {}, None
    for line in body.splitlines():
        h = re.match(r"^##\s+(.*)$", line)
        if h and not line.startswith("###"):
            cur = h.group(1).strip()                       # nouvelle section
            sections[cur] = []
        elif cur is not None:
            sections[cur].append(line)                     # ligne rattachée à la section courante
    return meta, sections


def find(sections, *keys):
    """Retourne (titre, lignes) de la première section dont le titre contient l'un des mots-clés (sans accents)."""
    for title, lines in sections.items():
        t = strip_acc(title)
        if any(k in t for k in keys):
            return title, lines
    return None, []


def bullets(lines):
    """
    Extrait les puces « - texte » ou « * texte » d'une liste de lignes.
    Une ligne indentée qui suit une puce est considérée comme sa suite (retour à la ligne dans le .md).
    """
    items = []
    for l in lines:
        if re.match(r"^\s*[-*]\s+", l):
            items.append(re.sub(r"^\s*[-*]\s+", "", l).rstrip())    # nouvelle puce
        elif l.strip() and l[:1].isspace() and items:
            items[-1] += " " + l.strip()                            # suite de la puce précédente
    return items


def paragraph(lines):
    """Assemble les lignes non vides en un seul paragraphe."""
    return " ".join(l.strip() for l in lines if l.strip())


def subsections(lines):
    """Découpe une liste de lignes en sous-sections « ### Titre » -> [(titre, [lignes]), ...]."""
    subs, cur = [], None
    for l in lines:
        h = re.match(r"^###\s+(.*)$", l)
        if h:
            cur = (h.group(1).strip(), [])
            subs.append(cur)
        elif cur:
            cur[1].append(l)
    return subs


def sp_prefix(text):
    """'SP2: texte' -> (2, 'texte') ; sans préfixe -> (None, texte)."""
    m = re.match(r"^SP(\d+)\s*:\s*(.*)$", text, re.I)
    return (int(m.group(1)), m.group(2)) if m else (None, text)


def numero(ident, rang):
    """Numéro porté par un identifiant ('Obj3' -> 3) ; à défaut, son rang dans la liste (1, 2, 3…)."""
    m = re.search(r"\d+", ident or "")
    return int(m.group()) if m else rang


# ═════════════════════════════════════════════════════════════════════
#  3. PETITS COMPOSANTS HTML RÉUTILISABLES
# ═════════════════════════════════════════════════════════════════════

def sp_tag(n):
    """Pastille colorée « SP1 », « SP2 »…"""
    return f'<span class="sp-tag sp{spc(n)}">SP{n}</span>'


def tableau(classe, entetes, lignes):
    """
    Construit un tableau complet, dans un conteneur à défilement horizontal (affichage mobile).
      - classe  : classe CSS du <table> (kpi-table, risk-table, io-table…)
      - entetes : liste de libellés, ou de couples (libellé, largeur) pour fixer la largeur d'une colonne
      - lignes  : liste de <tr>…</tr> déjà construits
    """
    ths = []
    for e in entetes:
        if isinstance(e, tuple):
            ths.append(f'<th style="width:{e[1]}">{e[0]}</th>')   # colonne avec largeur imposée
        else:
            ths.append(f"<th>{e}</th>")
    return (
        '            <div style="overflow-x:auto">\n'
        f'            <table class="{classe}">\n'
        '                <thead>\n'
        f'                    <tr>{"".join(ths)}</tr>\n'
        '                </thead>\n'
        '                <tbody>\n'
        + "\n".join(lignes) + "\n"
        '                </tbody>\n'
        '            </table>\n'
        '            </div>'
    )


def note(texte):
    """Petite phrase explicative sous un titre de tableau."""
    return f'            <span class="desc-note">{texte}</span>'


# ═════════════════════════════════════════════════════════════════════
#  4. PRÉPARATION DES DONNÉES (extraction depuis le markdown)
# ═════════════════════════════════════════════════════════════════════

def preparer(meta, S):
    """
    Lit toutes les sections utiles du markdown une seule fois et retourne un dictionnaire « D »
    que les fonctions section_xxx() utilisent ensuite.
    """
    D = {"meta": meta, "S": S}
    D["g"] = lambda k, d="": meta.get(k, d)                # accès pratique aux métadonnées avec valeur par défaut

    # --- sous-processus : « - Titre | périmètre » (numérotés dans l'ordre 1, 2, 3…) ---
    _, l = find(S, "sous-processus", "sous processus")
    sps = []
    for i, it in enumerate(bullets(l), 1):
        titre, perim = split(it, 2)
        sps.append({"n": i, "titre": titre, "perim": perim})
    D["sps"] = sps
    D["sp_title"] = {s["n"]: s["titre"] for s in sps}      # {1: 'Pilotage stratégique', …}

    # --- objectifs : « - Obj1 | SP1 | description | politique1, politique2 » ---
    _, l = find(S, "objectifs")
    D["objs"] = [split(x, 4) for x in bullets(l)]
    # --- risques : « - R1 | SP1 | titre | description | mesures » ---
    _, l = find(S, "risques")
    D["risks"] = [split(x, 5) for x in bullets(l)]
    # --- opportunités : même format que les risques ---
    _, l = find(S, "opportunit")
    D["opps"] = [split(x, 5) for x in bullets(l)]

    # Tables de correspondance « id -> n° de SP » : servent à retrouver le SP d'un indicateur depuis son objectif/risque
    D["obj_sp"] = {o[0]: spnum(o[1]) for o in D["objs"]}
    D["risk_sp"] = {r[0]: spnum(r[1]) for r in D["risks"]}
    D["opp_sp"] = {o[0]: spnum(o[1]) for o in D["opps"]}

    # Numéro d'objectif (Obj3 -> 3) : détermine la couleur du badge « badge-objN »
    D["obj_num"] = {o[0]: numero(o[0], i) for i, o in enumerate(D["objs"], 1)}
    return D


# ═════════════════════════════════════════════════════════════════════
#  5. SECTIONS DE LA PAGE (une fonction = un bloc HTML)
# ═════════════════════════════════════════════════════════════════════

# Police Inter, chargée uniquement pour la mise en page moderne
FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
STYLE_INTER = """    <style>
      /* Police Inter pour la mise en page moderne uniquement */
      body.modern-layout { font-family: 'Inter', 'Segoe UI', sans-serif; }
    </style>"""


def html_entete(D):
    """
    <head>, navigation principale et hero du processus.
    Métadonnées utilisées : titre, titre_page, site, id, badge_texte, version, date,
    pilote, participants, afficher_meta (oui/non), logo.
    """
    g, pref = D["g"], D["pref"]
    ident = g("id")
    titre = g("titre")

    # Texte de l'étiquette du hero : « P1-O1 · Processus Management » (surchargeable via badge_texte)
    tag = g("badge_texte", f"{ident} · {titre}" if ident else titre)

    # Pastilles de sous-processus du hero : « SP1 – Pilotage stratégique »
    chips = "\n".join(
        f'                <span class="h-sp{spc(s["n"])}">SP{s["n"]} – {esc(s["titre"])}</span>'
        for s in D["sps"]
    )

    # Bloc « méta » du hero (pilote, participants, version) : affiché seulement si afficher_meta: oui
    meta_hero = ""
    if strip_acc(g("afficher_meta", "non")) in ("oui", "true", "1", "vrai"):
        meta_hero = f'''
        <div class="proc-hero-meta">
            <div class="proc-meta-chip">Pilote : <strong>{esc(g("pilote"))}</strong></div>
            <div class="proc-meta-chip">Participants : <strong>{esc(g("participants"))}</strong></div>
            <div class="proc-meta-chip">Version : <strong>{esc(g("version", "1.0"))} · {esc(g("date"))}</strong></div>
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(g("titre_page", titre))} - {esc(g("site", "OpenSILEX"))}</title>
    <!-- Charte existante -->
    <link rel="stylesheet" href="{pref}css/charte.css">
    <link rel="stylesheet" href="{pref}css/common.css">
    <link rel="stylesheet" href="{pref}css/processus/processus.css">
    <link rel="stylesheet" href="{pref}css/processus/table.css">
    <link rel="stylesheet" href="{pref}css/logigramme/processus.css">
    <link rel="stylesheet" href="{pref}css/processus/processus-modern.css">
    {FONT_LINK}
{STYLE_INTER}
</head>

<body class="modern-layout" data-process-id="{esc_attr(ident)}">

<!-- ══ NAVIGATION PRINCIPALE ══ -->
<header class="main-header" id="header">
    <div class="nav-container">
        <!-- Logo -->
        <div class="logo">
            <a href="{esc_attr(g("logo", "/images/Logo.svg"))}" target="_blank">
                <img src="{esc_attr(g("logo", "/images/Logo.svg"))}" alt="Logo {esc_attr(g("site", "OpenSILEX"))}">
            </a>
        </div>

        <button class="menu-toggle" aria-expanded="false" aria-controls="navMenu" onclick="toggleMenu()">☰</button>

        <nav id="navMenuWrap"></nav>

        <button class="print-btn-nav" onclick="window.print()">🖨 Imprimer</button>
    </div>
</header>

<!-- ══ HERO DU PROCESSUS ══ -->
<div class="proc-hero">
    <div class="proc-hero-inner">
        <div>
            <span class="proc-id-tag">{esc(tag)}</span>
            <h1>{esc(titre)}</h1>
            <div class="proc-hero-sub">
{chips}
            </div>
        </div>{meta_hero}
    </div>
</div>

<!-- ══ LAYOUT SIDEBAR + CONTENU ══ -->
<div class="modern-page-layout">

    <!-- ─ SIDEBAR (remplie par js/sidebar.js) ─ -->
    <aside class="modern-sidebar"></aside>

    <!-- ─ CONTENU ─ -->
    <main class="modern-content">
'''


def section_infos(D):
    """
    « Informations générales » : 3 cartes (pilotage, périmètre, mode de pilotage).
      - pilote / participants : métadonnées de l'en-tête
      - périmètre             : section « ## Sous-processus » (« - Titre | périmètre »)
      - mode de pilotage      : section « ## Mode de pilotage » (« - SP1: texte »)
    """
    g, S = D["g"], D["S"]
    style_label = 'style="color:#0A423C;font-size:.82rem;flex-shrink:0"'   # style du libellé « Pilote : »

    # Carte « Périmètre » : une ligne par sous-processus
    lignes_perim = []
    for s in D["sps"]:
        txt = s["titre"] + (f' : {s["perim"]}' if s["perim"] else "")
        lignes_perim.append(f'                    <div class="sp-line-modern">{sp_tag(s["n"])}{esc(txt)}</div>')

    # Carte « Mode de pilotage » : le préfixe « SPn: » devient une pastille, sinon texte seul
    _, l = find(S, "mode de pilotage")
    lignes_mode = []
    for n, t in (sp_prefix(x) for x in bullets(l)):
        pastille = sp_tag(n) if n else ""
        lignes_mode.append(f'                    <div class="sp-line-modern">{pastille}{esc(t)}</div>')

    return f'''        <!-- INFORMATIONS GÉNÉRALES -->
        <section class="section" id="general">
            <h2>Informations générales</h2>
            <div class="info-grid-modern">
                <div class="info-card-modern">
                    <span class="ic-label">Pilotage</span>
                    <div class="sp-line-modern"><strong {style_label}>Pilote :</strong>&nbsp;{esc(g("pilote"))}</div>
                    <div class="sp-line-modern"><strong {style_label}>Participants :</strong>&nbsp;{esc(g("participants"))}</div>
                </div>
                <div class="info-card-modern">
                    <span class="ic-label">Périmètre</span>
{chr(10).join(lignes_perim)}
                </div>
                <div class="info-card-modern">
                    <span class="ic-label">Mode de pilotage</span>
{chr(10).join(lignes_mode)}
                </div>
            </div>
        </section>
'''


def section_finalite(D):
    """« Finalité du processus » : section « ## Finalité » (un paragraphe)."""
    _, l = find(D["S"], "finalit")
    if not l:
        return ""                                          # pas de finalité -> pas de section
    return f'''        <!-- FINALITÉ -->
        <section class="section" id="finalite">
            <h2>Finalité du processus</h2>
            <div class="finalite-box">
                {esc(paragraph(l))}
            </div>
        </section>
'''


def section_parties(D):
    """« Parties prenantes » : section « ## Parties prenantes » (une puce = une pastille)."""
    _, l = find(D["S"], "parties prenantes")
    items = bullets(l)
    if not items:
        return ""
    pills = "\n".join(f'                <span class="s-pill">{esc(it)}</span>' for it in items)
    return f'''        <!-- PARTIES PRENANTES -->
        <section class="section" id="parties">
            <h2>Parties prenantes</h2>
            <div class="stakeholder-pills">
{pills}
            </div>
        </section>
'''


def section_interactions(D):
    """
    « Interactions — Données d'entrée et de sortie » : section « ## Interactions ».
    Format attendu :
        ### Nom de l'interlocuteur | Rôle
        - entrée SP1: texte
        - sortie SP2: texte
    """
    _, l = find(D["S"], "interaction")
    subs = subsections(l)
    if not subs:
        return ""

    def ul(items):
        """Liste <ul> des données (vide si aucune donnée)."""
        return "<ul>" + "".join(items) + "</ul>" if items else ""

    lignes = []
    for head, contenu in subs:
        nom, role = split(head, 2)                         # « Nom | Rôle »
        entrees, sorties = [], []
        for b in bullets(contenu):
            m = re.match(r"^(entr[ée]e|sortie)\s+SP(\d+)\s*:\s*(.*)$", b, re.I)
            if not m:
                warn(f"Interactions « {nom} » : ligne ignorée (format attendu « - entrée SP1: texte ») → {b[:50]}")
                continue
            li = f"<li>{sp_tag(int(m.group(2)))}{esc(m.group(3))}</li>"
            # on range la donnée dans la colonne entrées ou sorties selon le mot de début
            (entrees if strip_acc(m.group(1)).startswith("entr") else sorties).append(li)
        lignes.append(
            "                    <tr>\n"
            f"                        <td>{esc(nom)}</td>\n"
            f'                        <td><span class="role-badge">{esc(role)}</span></td>\n'
            f"                        <td>{ul(entrees)}</td>\n"
            f"                        <td>{ul(sorties)}</td>\n"
            "                    </tr>"
        )

    entetes = [("Interlocuteur", "18%"), ("Rôle", "10%"), ("Entrées", "36%"), ("Sorties", "36%")]
    return f'''        <!-- INTERACTIONS IO -->
        <section class="section" id="io">
            <h2>Interactions — Données d'entrée et de sortie</h2>
{tableau("io-table", entetes, lignes)}
        </section>
'''


def section_documentation(D):
    """« Documentations associées » : section « ## Documentation » (« - SP1: titre du document »)."""
    _, l = find(D["S"], "documentation")
    items = bullets(l)
    if not items:
        return ""
    cartes = []
    for it in items:
        n, t = sp_prefix(it)
        pastille = sp_tag(n) + " " if n else ""            # pastille SP facultative
        cartes.append(f'                <div class="doc-item-modern"><div>{pastille}{esc(t)}</div></div>')
    return f'''        <!-- DOCUMENTATIONS -->
        <section class="section" id="docs">
            <h2>Documentations associées</h2>
            <div class="doc-grid-modern">
{chr(10).join(cartes)}
            </div>
        </section>
'''


def section_ressources(D):
    """« Ressources » : section « ## Ressources » (« - Humaines : texte » -> carte avec titre + texte)."""
    _, l = find(D["S"], "ressources")
    items = bullets(l)
    if not items:
        return ""
    cartes = []
    for it in items:
        if ":" in it:
            k, v = it.split(":", 1)                        # « Libellé : contenu »
            cartes.append(f'                <div class="resource-card-modern"><strong>{esc(k.strip())}</strong>{esc(v.strip())}</div>')
        else:
            cartes.append(f'                <div class="resource-card-modern">{esc(it)}</div>')
    return f'''        <!-- RESSOURCES -->
        <section class="section" id="ressources">
            <h2>Ressources</h2>
            <div class="resource-grid-modern">
{chr(10).join(cartes)}
            </div>
        </section>
'''


def section_activites(D):
    """
    « Activités principales » : section « ## Activités ».
    Format attendu :
        ### SP1 | Titre de l'activité
        Texte descriptif (une ou plusieurs lignes)
    Les activités sont numérotées A1, A2… sur l'ensemble du processus.
    Un séparateur de phase est inséré à chaque changement de sous-processus.
    """
    _, l = find(D["S"], "activit")
    subs = subsections(l)
    if not subs:
        return ""

    blocs = []
    precedent = None                                       # n° du SP de l'activité précédente
    for i, (head, lignes) in enumerate(subs, 1):
        # « SP1 | titre » ; sans barre, on rattache l'activité à SP1 et on prévient
        if "|" in head:
            sp, titre = split(head, 2)
        else:
            sp, titre = "SP1", head
            warn(f"Activité « {head[:40]} » : pas de « SPn | » dans le titre, rattachée à SP1")
        n = spnum(sp)

        # Séparateur de phase quand on change de sous-processus
        if n != precedent:
            libelle = f'SP{n} – {D["sp_title"].get(n, "")}'.rstrip(" –")
            marge = "" if precedent is None else ' style="margin-top:18px"'   # pas de marge pour la 1re phase
            blocs.append(f'            <hr class="phase-sep" data-label="{esc_attr(libelle)}"{marge}>\n')

        # Étape : pastille ronde (A1, A2…) + titre + description
        blocs.append(f'''            <div class="flow-step-modern">
                <div class="flow-circle fc-sp{spc(n)}">A{i}</div>
                <div>
                    <div class="flow-title-modern">{esc(titre)}</div>
                    <p class="flow-desc-modern">{esc(paragraph(lignes))}</p>
                </div>
            </div>''')
        precedent = n

    return f'''        <!-- ACTIVITÉS -->
        <section class="section flow-section" id="activites">
            <h2>Activités principales</h2>

{chr(10).join(blocs)}
        </section>
'''


def lignes_indicateurs(rows, table_sp, objectif=False, D=None):
    """
    Construit les <tr> d'un tableau d'indicateurs (KPI / KRI / KIO).
      rows     : lignes [ref, indicateur, cible, fréquence, calcul]
      table_sp : dict {ref -> n° SP} pour retrouver le SP à partir de l'objectif/risque/opportunité
      objectif : True pour les KPI (badge « badge-objN »), False pour KRI/KIO (badge « risk-id »)
    """
    out = []
    for ref, ind, cible, freq, calc in rows:
        if ref not in table_sp:
            warn(f"Indicateur « {ind[:40]} » : référence {ref} inconnue (SP1 utilisé par défaut)")
            n = 1
        else:
            n = table_sp[ref]
        if objectif:
            # KPI : le badge porte la couleur de l'objectif (badge-obj1, badge-obj2…)
            badge = f'<span class="badge-obj{D["obj_num"].get(ref, 1)}">{esc(ref)}</span>'
        else:
            # KRI / KIO : le badge reprend le style des identifiants de risques
            badge = f'<span class="risk-id sub-process-{spc(n)}">{esc(ref)}</span>'
        out.append(
            f'                    <tr><td>{sp_tag(n)}</td><td><strong>{esc(ind)}</strong></td>'
            f'<td class="kpi-target">{esc(cible)}</td><td>{esc(freq)}</td><td>{esc(calc)}</td><td>{badge}</td></tr>'
        )
    return out


def section_performance(D):
    """
    « Performance » : objectifs, KPI et indicateurs de fonctionnement.
      ## Objectifs                      « - Obj1 | SP1 | description | confiance, satisfaction »
      ## Indicateurs KPI                « - Obj1 | indicateur | cible | fréquence | calcul »
      ## Indicateurs de fonctionnement  « - SP1 | indicateur | définition | fréquence »
    Retourne aussi le saut de page qui suit la section.
    """
    S = D["S"]
    objs = D["objs"]
    _, l = find(S, "kpi")
    kpis = [split(x, 5) for x in bullets(l)]
    _, l = find(S, "fonctionnement")
    fonct = [split(x, 4) for x in bullets(l)]
    if not (objs or kpis or fonct):
        return ""                                          # rien à afficher

    parts = ['        <!-- PERFORMANCE -->\n        <section class="section" id="perf">\n            <h2>Performance</h2>']

    # --- tableau des objectifs ---
    if objs:
        lignes = []
        for oid, sp, desc, pol in objs:
            n = spnum(sp)
            # une pastille « politique » par valeur (séparées par , ou ;)
            pols = " ".join(
                f'<span class="politique {esc_attr(p.strip())}"></span>'
                for p in re.split(r"[,;]", pol) if p.strip()
            )
            lignes.append(
                f'                    <tr>\n'
                f'                        <td>{sp_tag(n)}</td>\n'
                f'                        <td><span class="badge-obj{D["obj_num"][oid]}">{esc(oid)}</span></td>\n'
                f'                        <td>{esc(desc)}</td>\n'
                f'                        <td>{pols}</td>\n'
                f'                    </tr>'
            )
        parts.append("            <h3>Objectifs</h3>\n" +
                     tableau("kpi-table", ["SP", "N°", "Description de l'objectif", "Lien avec la politique"], lignes))

    # --- tableau des KPI ---
    if kpis:
        parts.append(
            "            <h3>Indicateurs (KPI)</h3>\n" +
            note("Ces indicateurs mesurent l'atteinte d'un résultat attendu. Ils répondent à la question : « Est-ce qu'on atteint nos objectifs ? »") + "\n" +
            tableau("kpi-table", ["SP", "Indicateur", "Cible", "Fréquence", "Mode de calcul", "Objectif"],
                    lignes_indicateurs(kpis, D["obj_sp"], objectif=True, D=D))
        )

    # --- indicateurs de fonctionnement ---
    if fonct:
        lignes = [
            f'                    <tr><td>{sp_tag(spnum(sp))}</td><td>{esc(ind)}</td><td>{esc(defi)}</td><td>{esc(freq)}</td></tr>'
            for sp, ind, defi, freq in fonct
        ]
        parts.append(
            "            <h3>Indicateurs de fonctionnement</h3>\n" +
            note("Ces indicateurs mesurent l'activité courante. Ils répondent à la question : « Que s'est-il passé ? Combien ? »") + "\n" +
            tableau("kpi-table", ["SP", "Indicateur", "Définition / mode de calcul", "Fréquence"], lignes)
        )

    return "\n\n".join(parts) + '\n        </section>\n\n        <div class="page-break"></div>\n'


def lignes_risques(items, classe_ligne, D):
    """<tr> d'un tableau de risques ou d'opportunités : [id, SP, titre, description, mesures]."""
    out = []
    for rid, sp, titre, desc, mes in items:
        out.append(
            f'                    <tr class="{classe_ligne}"><td><span class="risk-id sub-process-{spc(spnum(sp))}">{esc(rid)}</span></td>'
            f'<td><strong>{esc(titre)}</strong></td><td>{esc(desc)}</td><td>{esc(mes)}</td></tr>'
        )
    return out


def section_risques(D):
    """
    « Analyse des Risques » : risques + KRI.
      ## Risques        « - R1 | SP1 | titre | description | mesures de maîtrise »
      ## Indicateurs KRI « - R1 | indicateur | cible | fréquence | calcul »
    """
    if not D["risks"]:
        return ""
    parts = [
        '        <!-- RISQUES -->\n        <section class="section" id="risques">\n            <h2>Analyse des Risques</h2>\n            <h3>Risques</h3>\n' +
        tableau("risk-table", ["N°", "Risque", "Description", "Actions de maîtrise / Mesures préventives"],
                lignes_risques(D["risks"], "risque-row", D))
    ]
    _, l = find(D["S"], "kri")
    kri = [split(x, 5) for x in bullets(l)]
    if kri:
        parts.append(
            "            <h3>Indicateurs (KRI)</h3>\n" +
            note("Ces indicateurs sont un signal d'alerte. Ils répondent à la question : « Y a-t-il un signal qui annonce un problème à venir ? »") + "\n" +
            tableau("kpi-table", ["SP", "Indicateur", "Cible", "Fréquence", "Mode de calcul", "Risque"],
                    lignes_indicateurs(kri, D["risk_sp"]))
        )
    return "\n\n".join(parts) + "\n        </section>\n"


def section_opportunites(D):
    """
    « Analyses des Opportunités » : opportunités + KIO.
      ## Opportunités   « - O1 | SP1 | titre | description | mesure de surveillance »
      ## Indicateurs KIO « - O1 | indicateur | cible | fréquence | calcul »
    """
    if not D["opps"]:
        return ""
    parts = [
        '        <!-- OPPORTUNITÉS -->\n        <section class="section" id="opport">\n            <h2>Analyses des Opportunités</h2>\n            <h3>Opportunités</h3>\n' +
        tableau("risk-table", ["N°", "Opportunité", "Description", "Mesure de surveillance"],
                lignes_risques(D["opps"], "opport-row", D))
    ]
    _, l = find(D["S"], "kio")
    kio = [split(x, 5) for x in bullets(l)]
    if kio:
        parts.append(
            "            <h3>Indicateurs (KIO)</h3>\n" +
            tableau("kpi-table", ["SP", "Indicateur", "Cible", "Fréquence", "Mode de calcul", "Opportunité"],
                    lignes_indicateurs(kio, D["opp_sp"]))
        )
    return "\n\n".join(parts) + "\n        </section>\n"


# Définition des pointes de flèche SVG (une seule fois par page, partagée par tous les logigrammes)
SVG_DEFS = '''        <svg width="0" height="0" style="position:absolute"><defs>
            <marker id="arr-head-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 Z" fill="#6b7280"/></marker>
            <marker id="arr-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 Z" fill="#1f2937"/></marker>
        </defs></svg>
'''


def section_logigrammes(D):
    """
    « Logigramme — SPn · titre » : une section par « ## Logigramme SPn » (ou « ## Logigramme SP1 – titre »).
    Chaque logigramme est dessiné en SVG par logigramme().
    """
    logis = [(t, ls) for t, ls in D["S"].items() if strip_acc(t).startswith("logigramme")]
    if not logis:
        return ""
    blocs = ["        <!-- LOGIGRAMMES -->\n" + SVG_DEFS]
    for titre_md, lignes in logis:
        n = spnum(titre_md)                                # SP concerné, lu dans le titre du « ## »
        titre = D["sp_title"].get(n, titre_md)             # titre du SP (défini dans « ## Sous-processus »)
        svg = logigramme(n, titre, bullets(lignes))
        blocs.append(f'''        <section class="section logigramme-section" id="logi-sp{n}">
            <h2>Logigramme — SP{n} · {esc(titre)}</h2>
            <div style="overflow-x:auto">
{svg}
            </div>
        </section>
''')
    return "\n".join(blocs)


def html_pied(D):
    """Pied de page du document (version / date), footer du site et scripts JS."""
    g, pref = D["g"], D["pref"]
    return f'''        <!-- PIED DE PAGE DOC -->
        <section class="section">
            <div class="footer" style="text-align:right;font-size:.75rem;color:#547068;border-top:1px solid #D0E8DF;padding-top:10px">
                <span contenteditable="true">Version {esc(g("version", "1.0"))}</span> |
                <span contenteditable="true">Mise à jour : {esc(g("date"))}</span>
            </div>
        </section>

    </main><!-- /modern-content -->
</div><!-- /modern-page-layout -->

<!-- ══ FOOTER ══ -->
<footer class="nav-footer" id="footer">
    <div class="container">
        <div class="footer-links"></div>
        <p>&copy; {esc(g("annee", "2025"))} {esc(g("copyright", "Cellule OpenSILEX"))}. Tous droits réservés.</p>
    </div>
</footer>

<script src="{pref}js/navigation.js"></script>
<script src="{pref}js/sidebar.js"></script>

</body>
</html>
'''


def render(meta, S):
    """Assemble la page complète : en-tête + toutes les sections + pied de page."""
    D = preparer(meta, S)
    D["pref"] = meta.get("prefixe_css", meta.get("css_prefix", "../../../"))   # préfixe des chemins css/js

    # Ordre d'apparition des blocs dans la page
    blocs = [
        html_entete(D),
        section_infos(D),
        section_finalite(D),
        section_parties(D),
        section_interactions(D),
        section_documentation(D),
        section_ressources(D),
        section_activites(D),
        section_performance(D),
        section_risques(D),
        section_opportunites(D),
        section_logigrammes(D),
        html_pied(D),
    ]
    # On ignore les blocs vides (section absente du .md) et on sépare par une ligne vide
    return "\n".join(b for b in blocs if b)


# ═════════════════════════════════════════════════════════════════════
#  6. LOGIGRAMME SVG
# ═════════════════════════════════════════════════════════════════════

def wrap(t, w):
    """Coupe un texte en lignes de w caractères maximum (au moins une ligne, même vide)."""
    return textwrap.wrap(t, w) or [""]


def logigramme(n, titre, items):
    """
    Dessine le logigramme du sous-processus n en SVG, de haut en bas.
    Chaque puce du .md décrit un élément :
        - entrée: texte                                   -> capsule d'entrée
        - étape [A1]: titre | sous-titre                  -> rectangle
        - décision: question | oui/non | titre | détail | retour A1
                                                          -> losange + boîte latérale (+ boucle de retour si « retour Ax »)
        - sortie: texte                                   -> capsule de sortie
    """
    c = spc(n)                                             # classe de couleur (1..3)
    W = 700                                                # largeur du dessin
    CX = 350                                               # axe central vertical
    GAP = 26                                               # espace vertical entre deux éléments
    svg = []                                               # lignes SVG accumulées
    A = svg.append
    y = 36                                                 # position verticale courante (sous le bandeau de titre)
    steps = {}                                             # id d'étape -> (ordonnée du centre, bord droit) pour les boucles
    pending_loops = []                                     # boucles de retour à tracer à la fin : (y, id cible, rang)
    last_bottom = None                                     # bas de l'élément précédent (origine de la flèche suivante)
    loop_k = 0                                             # rang de la boucle (décale chaque boucle vers la droite)

    def arrow_from(prev_bottom, to_y):
        """Flèche verticale entre le bas de l'élément précédent et le haut du suivant."""
        if prev_bottom is not None:
            A(f'<line class="arr" x1="{CX}" y1="{prev_bottom}" x2="{CX}" y2="{to_y}" marker-end="url(#arr-head)"/>')

    for it in items:
        # Reconnaît « type [id] : reste » ; le type peut être entrée / étape / décision / sortie / ?
        m = re.match(r"^(entr[ée]e|sortie|étape|etape|d[ée]cision|\?)\s*(?:\[(\w+)\])?\s*:?\s*(.*)$", it, re.I)
        if not m:
            warn(f"Logigramme SP{n} : ligne ignorée → {it[:50]}")
            continue
        kind = strip_acc(m.group(1))                       # type sans accents
        sid = m.group(2)                                   # identifiant facultatif entre crochets
        rest = m.group(3)                                  # contenu après le « : »

        # ── ENTRÉE : capsule arrondie en haut du logigramme ──
        if kind.startswith("entree"):
            lines = wrap(rest, 70)
            h = 30 + 14 * (len(lines) - 1)                 # hauteur selon le nombre de lignes
            w = min(max(max(len(x) for x in lines) * 6.6 + 40, 200), 520)   # largeur selon le texte, bornée
            A(f'<rect class="node-term" x="{CX - w/2:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="15"/>')
            for i, ln in enumerate(lines):
                A(f'<text class="lbl-title" x="{CX}" y="{y + 20 + 14*i}" text-anchor="middle">{esc(ln)}</text>')
            last_bottom = y + h
            y = last_bottom + GAP

        # ── ÉTAPE : rectangle avec titre et sous-titre ──
        elif kind.startswith("etape"):
            titre_e, sub = split(rest, 2)
            label = f"{sid} — {titre_e}" if sid else titre_e     # « A1 — Titre »
            sl = wrap(sub, 80) if sub else []                    # sous-titre sur plusieurs lignes si besoin
            h = 52 + 14 * max(0, len(sl) - 1)
            arrow_from(last_bottom, y)
            A(f'<rect class="node-sp{c}" x="110" y="{y}" width="480" height="{h}" rx="6"/>')
            A(f'<text class="lbl-title" x="{CX}" y="{y+19}" text-anchor="middle">{esc(label)}</text>')
            for i, ln in enumerate(sl):
                A(f'<text class="lbl-sub" x="{CX}" y="{y+36+14*i}" text-anchor="middle">{esc(ln)}</text>')
            if sid:
                steps[sid] = (y + h / 2, 590)              # mémorise le centre et le bord droit pour les boucles
            last_bottom = y + h
            y = last_bottom + GAP

        # ── DÉCISION : losange, branche latérale, branche principale vers le bas ──
        elif kind.startswith("decision") or kind == "?":
            q, branch, bt, bs, retour = split(rest, 5)
            branch = strip_acc(branch) or "non"            # branche latérale : « non » par défaut
            other = "oui" if branch == "non" else "non"    # la branche principale est l'autre réponse
            ql = wrap(q, 17)[:3]                           # question sur 3 lignes maximum
            hh = 26 + 7 * max(0, len(ql) - 2)              # demi-hauteur du losange
            H = 2 * hh
            hw = 88                                        # demi-largeur du losange
            arrow_from(last_bottom, y)
            cy = y + hh                                    # ordonnée du centre du losange
            A(f'<polygon class="node-dec" points="{CX},{y} {CX+hw},{cy} {CX},{y+H} {CX-hw},{cy}"/>')
            for i, ln in enumerate(ql):
                A(f'<text class="lbl-aside" x="{CX}" y="{cy - 7*(len(ql)-1) + 14*i + 4}" text-anchor="middle">{esc(ln)}</text>')

            # branche latérale (à droite du losange)
            sl = wrap(bs, 28) if bs else []
            bh = max(44, 30 + 14 * len(sl))                # hauteur de la boîte latérale
            bx, bw = 490, 180                              # position et largeur de la boîte latérale
            cls_lbl = "no" if branch == "non" else "yes"   # couleur du libellé Oui/Non
            A(f'<line class="arr" x1="{CX+hw}" y1="{cy}" x2="{bx}" y2="{cy}" marker-end="url(#arr-head)"/>')
            A(f'<text class="{cls_lbl}" x="{CX+hw+10}" y="{cy-6}">{branch.capitalize()}</text>')
            # boîte « boucle » (retour en arrière) ou « refus » (fin de parcours)
            classe_boite = "node-loop" if retour else "node-refus"
            A(f'<rect class="{classe_boite}" x="{bx}" y="{cy-bh/2:.0f}" width="{bw}" height="{bh}" rx="6"/>')
            A(f'<text class="lbl-title" x="{bx+bw/2:.0f}" y="{cy-bh/2+17:.0f}" text-anchor="middle">{esc(bt)}</text>')
            for i, ln in enumerate(sl):
                A(f'<text class="lbl-sub" x="{bx+bw/2:.0f}" y="{cy-bh/2+33+14*i:.0f}" text-anchor="middle">{esc(ln)}</text>')
            if retour:
                # on retient la boucle ; elle sera tracée à la fin, quand toutes les étapes seront connues
                cible = re.sub(r"^retour\s*", "", retour, flags=re.I).strip("[] ")
                pending_loops.append((cy, cible, loop_k))
                loop_k += 1

            # branche principale (vers le bas) : libellé de la réponse opposée
            last_bottom = y + H
            y = last_bottom + GAP
            cls_main = "yes" if other == "oui" else "no"
            A(f'<text class="{cls_main}" x="{CX+5}" y="{last_bottom+16}">{other.capitalize()}</text>')

        # ── SORTIE : capsule de fin ──
        elif kind.startswith("sortie"):
            lines = wrap(rest, 60)
            h = 32 + 14 * (len(lines) - 1)
            w = min(max(max(len(x) for x in lines) * 6.6 + 40, 220), 520)
            arrow_from(last_bottom, y)
            A(f'<rect class="node-out" x="{CX - w/2:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="16"/>')
            for i, ln in enumerate(lines):
                A(f'<text class="lbl-title" x="{CX}" y="{y + 21 + 14*i}" text-anchor="middle">{esc(ln)}</text>')
            last_bottom = y + h
            y = last_bottom + GAP

    # ── Boucles de retour : tracées après coup, car il faut connaître toutes les étapes ──
    for cy, tid, k in pending_loops:
        if tid not in steps:
            warn(f"Logigramme SP{n} : « retour {tid} » ne correspond à aucune étape [id]")
            continue
        ty, tx = steps[tid]                                # centre et bord droit de l'étape cible
        xx = 680 + 7 * k                                   # colonne de la boucle (décalée si plusieurs boucles)
        A(f'<path class="arr-loop" d="M670 {cy:.0f} L{xx} {cy:.0f} L{xx} {ty:.0f} L{tx} {ty:.0f}" marker-end="url(#arr-head-gray)"/>')

    # ── Assemblage : cadre + titre du SP, puis tous les éléments dessinés ──
    H = int((last_bottom or y) + 20)                       # hauteur totale du dessin
    entete = f'''            <svg class="logi-svg" width="100%" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" style="display:block;margin-bottom:8px">
                <title>SP{n} — {esc(titre)}</title>
                <rect class="frame-sp{c}" x="0" y="0" width="{W}" height="24" rx="0" style="stroke-dasharray:none;"/>
                <text class="lbl-sp" x="{CX}" y="16" text-anchor="middle" style="fill:{SP_COLORS[c]};">SP{n} — {esc(titre)}</text>
'''
    return entete + "\n".join("                " + s for s in svg) + "\n            </svg>"


# ═════════════════════════════════════════════════════════════════════
#  7. PROGRAMME PRINCIPAL : recherche des .md puis génération
# ═════════════════════════════════════════════════════════════════════

def main():
    # --- arguments de la ligne de commande ---
    ap = argparse.ArgumentParser(description="Génère les pages HTML des processus à partir des fichiers .md")
    ap.add_argument("files", nargs="*", help="fichiers .md (défaut : tous ceux de html/Processus/)")
    ap.add_argument("-o", "--out", default=None, help="dossier de sortie (défaut : à côté du .md)")
    ap.add_argument("--css-prefix", default=None, help="forcer le préfixe des chemins css/js")
    a = ap.parse_args()

    root = Path(__file__).resolve().parent                 # dossier du projet = dossier de ce script
    proc_dir = root / "html" / "Processus"                 # dossier où sont rangés les .md

    # --- indexation de tous les .md de html/Processus/ (sous-dossiers compris) ---
    # Les fichiers dont le nom commence par « _ » (modèles, brouillons) sont ignorés.
    md_map = {}
    if proc_dir.is_dir():
        for p in sorted(proc_dir.rglob("*.md")):
            if p.name.startswith("_"):
                continue
            if p.name in md_map:
                # deux fichiers de même nom dans des sous-dossiers différents : on prévient
                print(f"⚠ Doublon « {p.name} » : {md_map[p.name].relative_to(root)} conservé, {p.relative_to(root)} ignoré")
                continue
            md_map[p.name] = p
    else:
        print(f"⚠ Dossier introuvable : {proc_dir}")

    # --- liste des fichiers à convertir ---
    files = []
    erreurs = 0
    if a.files:
        for f in a.files:
            p = Path(f)
            if p.exists():                                         # 1) chemin valide tel quel
                files.append(p)
            elif p.name in md_map:                                 # 2) nom exact trouvé dans html/Processus/
                files.append(md_map[p.name])
            elif (p.stem + ".md") in md_map:                       # 3) nom sans extension (ex. « Management »)
                files.append(md_map[p.stem + ".md"])
            else:
                # 4) dernier essai : comparaison sans tenir compte de la casse ni des accents
                cible = strip_acc(p.stem)
                trouve = [v for k, v in md_map.items() if strip_acc(Path(k).stem) == cible]
                if trouve:
                    files.append(trouve[0])
                else:
                    print(f"✘ Fichier introuvable : {f}")
                    erreurs += 1
    else:
        files = list(md_map.values())                              # sans argument : tous les .md indexés

    if not files:
        print("Aucun fichier .md à traiter.")
        sys.exit(1)

    # --- génération page par page ---
    for f in files:
        warnings.clear()                                           # avertissements propres à ce fichier
        meta, S = parse_md(f)

        # dossier de sortie : option -o, sinon à côté du .md
        out_dir = (Path(a.out) if a.out else f.parent).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)

        # préfixe des chemins css/js : forcé en option, sinon calculé depuis la position de la page par rapport à la racine
        meta["prefixe_css"] = a.css_prefix or (os.path.relpath(root, out_dir).replace(os.sep, "/") + "/")

        dest = out_dir / (f.stem + ".html")
        dest.write_text(render(meta, S), encoding="utf-8")

        print(f"✔ {f.name} → {dest.relative_to(root) if root in dest.parents else dest}")
        for w in warnings:
            print("   ⚠", w)

    sys.exit(1 if erreurs else 0)


if __name__ == "__main__":
    main()