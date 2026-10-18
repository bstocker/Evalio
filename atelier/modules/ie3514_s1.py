"""Module « IE3514 - Revision Sheet for Session 1 », du chapitre Révisions.

Des exercices de révision sur la première séance du cours IE.3514 —
Healthcare systems organization : ce qu'est la santé, la frontière entre
système de santé et système de soins, santé individuelle et santé des
populations, déterminants, continuum de santé et niveaux de prévention,
niveaux de soins, les six piliers de l'OMS et leurs interactions, les
quatre flux, les dimensions d'évaluation, et le caractère hybride du
système français.

Le cours est en anglais, les exercices en français : chaque notion garde
entre parenthèses son nom anglais, celui des diapositives, quand il aide
à la retrouver.

Deux formes :

- des **fiches à trous** (mode « compléter ») : un texte à compléter par
  des menus, et un motif qui donne, pour chaque trou, une propriété de la
  notion attendue — sa question clé, sa définition, ses acteurs. L'élève
  doit reconnaître la notion à sa propriété : le motif ne la nomme
  jamais. Chaque notion d'un menu a sa propre propriété, si bien qu'aucun
  mauvais choix ne reproduit le motif ;
- des **questions de cours** (mode QCM), sur le modèle de `docker_bases`.

Chaque exercice renvoie à la partie du cours qui porte la réponse, dans
son rappel et dans l'explication du QCM.
"""

from dataclasses import replace

from ..engine import Module, Pattern, _opts, qcm_pattern
from .qcm_docker import _tourner

# L'intitulé demandé par l'enseignant, en tête de chaque exercice.
INTITULE = (
    "The following exercises are designed to help you make the most of "
    "your revision sessions. You answer the questions, and if you get a "
    "wrong answer, you will be shown the correct answer and directed to "
    "the relevant chapter to review if you wish to improve your "
    "understanding of the course material."
)

# Les parties du cours, sous leur titre de diapositive.
PARTIES = {
    1: "What is health?",
    2: "Health system and healthcare system",
    3: "Individual health and population health",
    4: "The determinants of health",
    5: "From healthy person to patient: the health continuum",
    6: "Primary, secondary and tertiary care",
    7: "How do we break down a health system?",
    8: "The building blocks are not silos",
    9: "The four flows we will follow",
    10: "What makes a health system « good »?",
    11: "A first feature of the French system",
}


def revoir(partie, detail=""):
    """Renvoi vers la partie du cours qui porte la réponse."""
    return "partie %d du cours, « %s »%s" % (
        partie, PARTIES[partie], " — " + detail if detail else "")


def lecon(partie, detail=""):
    """Rappel d'une fiche à trous : l'intitulé, la lecture, le renvoi."""
    return (
        INTITULE,
        "Le **motif à reproduire** donne, pour chaque trou, une propriété "
        "de la notion attendue, sans la nommer. Choisissez la notion qui "
        "la possède.",
        "En cas d'erreur, revoyez la %s." % revoir(partie, detail),
    )


def _choisir(variantes, cle, majuscule=False):
    """Tirage d'une variante : le texte des cas change, pas la réponse."""
    def texte(t):
        return t[0].upper() + t[1:] if majuscule else t
    return lambda p: {nom: texte(textes[p["cas"]])
                      for nom, textes in zip(cle, variantes)}


def _menu(table, noms=None):
    """Menu des notions de `table`, chacune rendant sa propriété.

    `noms` restreint le menu et fixe son ordre, la bonne réponse en
    premier ; sans lui, toutes les notions de la table, dans son ordre.
    """
    return _opts(*[(chr(ord("a") + i), nom,
                    (lambda v: lambda p: v)(table[nom]))
                   for i, nom in enumerate(noms or table)])


# --------------------------------------------------------------------------
# Fiches à trous
# --------------------------------------------------------------------------

# Les trois niveaux de prévention, et la promotion de la santé qu'on
# confond avec la prévention primaire. Chacun avec sa question (partie 5).
QUESTION_PREVENTION = {
    "prévention primaire": "« Comment l'empêcher de survenir ? »",
    "prévention secondaire": "« Comment la détecter à temps ? »",
    "prévention tertiaire": "« Comment en limiter les conséquences ? »",
    "promotion de la santé": "« Comment créer des conditions favorables, "
                             "sans viser une maladie précise ? »",
}



# Les actions des quatre lignes, une variante par tirage. La lutte contre
# le tabac et l'activité physique sont écartées : le cours les range à la
# fois dans la promotion et dans la prévention primaire.
ACTIONS = (
    ("la vaccination des nourrissons",
     "la prévention des accidents domestiques",
     "la distribution de préservatifs"),
    ("le dépistage organisé du cancer du sein",
     "le dépistage organisé du cancer colorectal",
     "la mesure de la pression artérielle"),
    ("la réadaptation cardiaque après un infarctus",
     "le suivi d'un diabète déjà installé",
     "l'éducation thérapeutique d'un patient malade"),
    ("l'éducation à la santé à l'école",
     "l'amélioration de l'environnement",
     "l'encouragement à une alimentation équilibrée"),
)

PREVENTION = Pattern(
    key="ie3514_s1_prevention",
    name="Les niveaux de prévention",
    brief="Classer quatre actions d'un territoire entre promotion de la "
          "santé et prévention primaire, secondaire ou tertiaire.",
    why="Chaque niveau répond à sa propre question.",
    lesson=lecon(5, "diapositives 5.1 à 5.7 et le tableau des trois "
                    "niveaux de prévention"),
    dims=(("cas", 0, 2),),
    derive=_choisir(ACTIONS, ("action_a", "action_b", "action_c",
                              "action_d"), True),
    tpl="""Fiche de révision : les niveaux de prévention

Quatre actions menées sur un même territoire :
  A. @action_a@
  B. @action_b@
  C. @action_c@
  D. @action_d@

L'action A relève de la @a@.
L'action B relève de la @b@.
L'action C relève de la @c@.
L'action D relève de la @d@.""",
    blanks={
        "a": ("Action A", _menu(QUESTION_PREVENTION)),
        "b": ("Action B", _menu(QUESTION_PREVENTION)),
        "c": ("Action C", _menu(QUESTION_PREVENTION)),
        "d": ("Action D", _menu(QUESTION_PREVENTION)),
    },
    ref={"a": "a", "b": "b", "c": "c", "d": "d"},
    rows=lambda p, get: ["%s. Question : %s" % (lettre.upper(), get(lettre)(p))
                         for lettre in "abcd"],
    level=4,
)


# Les niveaux de soins, et les soins de santé primaires, leur faux ami
# (partie 6). Chacun avec ce qui le caractérise.
TRAIT_NIVEAU = {
    "soins primaires": "premier contact, continuité, coordination du "
                       "parcours",
    "soins secondaires": "niveau spécialisé, atteint en général après un "
                         "premier contact",
    "soins tertiaires": "expertise rare, plateau technique complexe, "
                        "compétences concentrées",
    "soins de santé primaires (PHC)": "approche globale de la santé d'une "
                                      "société, et non niveau de soins",
}



# Deux parcours : celui du cours, et le même gradient en cardiologie.
PARCOURS = (
    ("un patient souffrant de maux de tête voit son médecin généraliste",
     "une patiente essoufflée voit son médecin traitant"),
    ("une affection neurologique est suspectée : consultation de "
     "neurologie et imagerie",
     "une maladie cardiaque est suspectée : consultation de cardiologie"),
    ("une tumeur cérébrale complexe est découverte : centre de "
     "neurochirurgie",
     "une intervention s'impose : chirurgie cardiaque"),
)

NIVEAUX = Pattern(
    key="ie3514_s1_niveaux",
    name="Le gradient d'orientation",
    brief="Situer chaque étape d'un parcours de soins sur les niveaux de "
          "soins.",
    why="Chaque niveau se reconnaît à ce qu'il apporte au parcours.",
    lesson=lecon(6, "diapositives 6.1 à 6.3 et « A referral gradient »"),
    dims=(("cas", 0, 1),),
    derive=_choisir(PARCOURS, ("etape1", "etape2", "etape3")),
    tpl="""Fiche de révision : un gradient d'orientation

Étape 1 : @etape1@.
  Cette étape relève des @n1@.
Étape 2 : @etape2@.
  Cette étape relève des @n2@.
Étape 3 : @etape3@.
  Cette étape relève des @n3@.""",
    blanks={
        "n1": ("Étape 1", _menu(TRAIT_NIVEAU)),
        "n2": ("Étape 2", _menu(TRAIT_NIVEAU)),
        "n3": ("Étape 3", _menu(TRAIT_NIVEAU)),
    },
    ref={"n1": "a", "n2": "b", "n3": "c"},
    rows=lambda p, get: ["Étape %d : %s" % (i, get("n%d" % i)(p))
                         for i in (1, 2, 3)],
    level=3,
)


# Les six piliers de l'OMS, chacun avec sa question (partie 7).
QUESTION_PILIER = {
    "gouvernance": "« Qui décide ? »",
    "financement": "« Qui paie, et comment circule l'argent ? »",
    "ressources humaines": "« A-t-on les bonnes compétences au bon "
                           "endroit ? »",
    "prestation de services": "« Où et comment le service est-il "
                              "délivré ? »",
    "produits médicaux et technologies": "« Avec quelles ressources "
                                         "physiques et technologiques ? »",
    "systèmes d'information": "« Quelle information circule, produite par "
                              "qui, pour qui ? »",
}


PILIERS = Pattern(
    key="ie3514_s1_piliers",
    name="Un territoire sans généralistes",
    brief="Rattacher chaque levier d'action à l'un des six piliers de "
          "l'OMS.",
    why="Une difficulté qui touche un pilier peut exiger d'en transformer "
        "plusieurs.",
    lesson=lecon(8, "« A territory short of general practitioners », avec "
                    "les six piliers de la partie 7"),
    tpl="""Fiche de révision : un territoire manque de médecins généralistes

Diagnostic spontané : « C'est uniquement un problème d'effectifs. »
L'analyse par les six piliers de l'OMS fait apparaître d'autres leviers :

  1. Les modes de rémunération pèsent sur le lieu où les
     professionnels choisissent de s'installer.
     Pilier : @l1@
  2. Les autorités peuvent créer des incitations.
     Pilier : @l2@
  3. La téléconsultation peut apporter une partie de la réponse.
     Pilier : @l3@
  4. Les données permettent de repérer les zones où les besoins
     sont les plus forts.
     Pilier : @l4@""",
    # Chaque menu écarte les piliers que le cours rattache aussi au levier :
    # la télémédecine apparaît sous la prestation de services, et la
    # réorganisation de l'offre sous la gouvernance.
    blanks={
        "l1": ("Levier 1", _menu(QUESTION_PILIER, (
            "financement", "gouvernance", "ressources humaines",
            "prestation de services"))),
        "l2": ("Levier 2", _menu(QUESTION_PILIER, (
            "gouvernance", "financement", "ressources humaines",
            "systèmes d'information"))),
        "l3": ("Levier 3", _menu(QUESTION_PILIER, (
            "produits médicaux et technologies", "systèmes d'information",
            "ressources humaines", "gouvernance"))),
        "l4": ("Levier 4", _menu(QUESTION_PILIER, (
            "systèmes d'information", "gouvernance",
            "produits médicaux et technologies", "financement"))),
    },
    ref={"l1": "a", "l2": "a", "l3": "a", "l4": "a"},
    rows=lambda p, get: ["Levier %d : %s" % (i, get("l%d" % i)(p))
                         for i in (1, 2, 3, 4)],
    level=4,
)


# Les sept dimensions d'évaluation, avec leur définition (partie 10).
DEFINITION_DIMENSION = {
    "résultats de santé": "les effets produits sur la santé : espérance "
                          "de vie, mortalité évitable",
    "accès": "la capacité effective d'obtenir les services : coût, "
             "distance, délais, disponibilité",
    "qualité et sécurité": "des soins efficaces, conformes aux preuves, "
                           "sans événement indésirable évitable",
    "équité": "à besoin égal, accès égal, sans écart lié au revenu ou au "
              "statut social",
    "efficience": "le meilleur résultat possible avec les ressources "
                  "utilisées",
    "soutenabilité": "la capacité à financer et faire fonctionner le "
                     "système dans la durée",
    "résilience": "la capacité à continuer de fonctionner et à se "
                  "réorganiser face à un choc",
}


SITUATIONS = (
    ("à besoin égal, les ménages modestes obtiennent moins de soins que "
     "les autres",
     "à besoin égal, les habitants peu diplômés sont moins bien soignés"),
    ("les hôpitaux continuent de soigner pendant une cyberattaque",
     "les soins se poursuivent malgré une canicule et une rupture "
     "d'approvisionnement en médicaments"),
    ("le système fonctionne bien aujourd'hui, mais le vieillissement de "
     "la population menace son financement dans dix ans",
     "la hausse des maladies chroniques et le coût de l'innovation font "
     "douter qu'on puisse financer longtemps le système"),
    ("on dépense davantage en prévention pour économiser des "
     "hospitalisations, à résultats meilleurs",
     "on cherche le meilleur résultat possible avec les moyens "
     "disponibles, sans viser la seule baisse des coûts"),
    ("des soins conformes aux recommandations provoquent pourtant un "
     "événement indésirable évitable",
     "une infection contractée à l'hôpital aurait pu être évitée"),
)

DIMENSIONS = Pattern(
    key="ie3514_s1_dimensions",
    name="Évaluer un système de santé",
    brief="Rattacher chaque situation à la dimension d'évaluation qu'elle "
          "met en jeu.",
    why="Évaluer un système, c'est arbitrer entre des dimensions souvent "
        "en tension.",
    lesson=lecon(10, "« Seven dimensions for evaluating a health system » "
                     "et leur détail, 10.1 à 10.7"),
    dims=(("cas", 0, 1),),
    derive=_choisir(SITUATIONS, ("s1", "s2", "s3", "s4", "s5"), True),
    tpl="""Fiche de révision : les dimensions d'évaluation

  1. @s1@.
     Dimension : @d1@
  2. @s2@.
     Dimension : @d2@
  3. @s3@.
     Dimension : @d3@
  4. @s4@.
     Dimension : @d4@
  5. @s5@.
     Dimension : @d5@""",
    # La situation d'équité ne propose pas l'accès : renoncer aux soins
    # faute de moyens est aussi un défaut d'accès financier.
    blanks={
        "d1": ("Situation 1", _menu(DEFINITION_DIMENSION, (
            "équité", "efficience", "qualité et sécurité",
            "résultats de santé"))),
        "d2": ("Situation 2", _menu(DEFINITION_DIMENSION, (
            "résilience", "soutenabilité", "efficience", "accès"))),
        "d3": ("Situation 3", _menu(DEFINITION_DIMENSION, (
            "soutenabilité", "résilience", "efficience", "équité"))),
        "d4": ("Situation 4", _menu(DEFINITION_DIMENSION, (
            "efficience", "soutenabilité", "accès", "qualité et sécurité"))),
        "d5": ("Situation 5", _menu(DEFINITION_DIMENSION, (
            "qualité et sécurité", "résultats de santé", "accès",
            "équité"))),
    },
    ref={"d1": "a", "d2": "a", "d3": "a", "d4": "a", "d5": "a"},
    rows=lambda p, get: ["%d. %s" % (i, get("d%d" % i)(p))
                         for i in (1, 2, 3, 4, 5)],
    level=4,
)


# Les étapes du continuum, chacune avec son but (partie 5).
BUT_ETAPE = {
    "PRÉVENIR": "éviter l'apparition",
    "DIAGNOSTIQUER": "identifier la cause",
    "RÉADAPTER": "restaurer les capacités",
}

# Les deux bouts du continuum : l'effet, et ce qui l'accompagne.
BOUT = {
    "collectif, diffus et différé":
        "écoles, collectivités, employeurs ; financement : budgets de "
        "prévention, souvent modestes",
    "individuel, mesurable et immédiat":
        "professionnels et établissements de santé ; financement : "
        "assurance maladie, paiement à l'activité",
}



CONTINUUM = Pattern(
    key="ie3514_s1_continuum",
    name="Le continuum de santé",
    brief="Compléter les étapes du continuum de santé, puis l'effet de "
          "l'action à chacun de ses bouts.",
    why="Le système accompagne une personne toute sa vie, pas seulement "
        "pendant un épisode aigu.",
    lesson=lecon(5, "« The health continuum »"),
    tpl="""Fiche de révision : le continuum de santé

PROMOUVOIR → @e2@ → DÉPISTER → @e4@ → TRAITER → @e6@ → ACCOMPAGNER

Population générale → personne à risque → patient
                    → personne handicapée ou en fin de vie

À gauche du continuum, l'effet de l'action est @gauche@.
À droite du continuum, l'effet de l'action est @droite@.""",
    blanks={
        "e2": ("2e étape", _menu(BUT_ETAPE)),
        "e4": ("4e étape", _menu(BUT_ETAPE)),
        "e6": ("6e étape", _menu(BUT_ETAPE)),
        "gauche": ("Effet à gauche", _menu(BOUT)),
        "droite": ("Effet à droite", _menu(BOUT)),
    },
    ref={"e2": "a", "e4": "b", "e6": "c", "gauche": "a", "droite": "b"},
    rows=lambda p, get: [
        "2e étape : %s" % get("e2")(p),
        "4e étape : %s" % get("e4")(p),
        "6e étape : %s" % get("e6")(p),
        "À gauche, acteurs : %s" % get("gauche")(p),
        "À droite, acteurs : %s" % get("droite")(p),
    ],
    level=3,
)


# Maladie, vécu de la maladie, santé au sens large (partie 1.2), avec ce
# que chacune représente pour le système.
ROLE_NOTION = {
    "la maladie (disease)": "ce que voient réellement les systèmes "
                            "d'information",
    "le vécu de la maladie (illness)": "ce qui déclenche le recours aux "
                                       "soins",
    "la santé au sens large (health)": "ce que le nombre d'actes ne "
                                       "suffit pas à mesurer",
}

OBSERVATIONS = (
    ("un code de diagnostic « diabète de type 2 » est saisi dans le "
     "dossier du patient",
     "une hypertension est identifiée selon des critères médicaux, puis "
     "codée"),
    ("une personne se sent malade et prend rendez-vous, alors qu'aucun "
     "examen ne révèle de pathologie",
     "un patient décrit sa fatigue et son inquiétude : c'est ce ressenti "
     "qui l'amène à consulter"),
    ("on considère l'autonomie d'une personne, ses relations sociales et "
     "la qualité de vie qu'elle perçoit",
     "on considère l'état psychique d'une personne, son environnement et "
     "sa qualité de vie perçue"),
)

NOTIONS = Pattern(
    key="ie3514_s1_notions",
    name="Trois notions à ne pas confondre",
    brief="Reconnaître, dans chaque observation, la notion en jeu : "
          "maladie, vécu de la maladie, ou santé au sens large.",
    why="La performance d'un système ne se mesure pas au seul nombre "
        "d'actes.",
    lesson=lecon(1, "diapositive 1.2 « Three notions not to be confused »"),
    dims=(("cas", 0, 1),),
    derive=_choisir(OBSERVATIONS, ("o1", "o2", "o3"), True),
    tpl="""Fiche de révision : maladie, vécu de la maladie, santé

  1. @o1@.
     Notion : @n1@
  2. @o2@.
     Notion : @n2@
  3. @o3@.
     Notion : @n3@""",
    blanks={
        "n1": ("Observation 1", _menu(ROLE_NOTION)),
        "n2": ("Observation 2", _menu(ROLE_NOTION)),
        "n3": ("Observation 3", _menu(ROLE_NOTION)),
    },
    ref={"n1": "a", "n2": "b", "n3": "c"},
    rows=lambda p, get: ["%d. %s" % (i, get("n%d" % i)(p))
                         for i in (1, 2, 3)],
    level=3,
)


# --------------------------------------------------------------------------
# Questions de cours
# --------------------------------------------------------------------------

# (énoncé, (quatre propositions), index de la bonne, niveau, explication,
# partie du cours). Comme dans qcm_docker, la bonne réponse est écrite en
# premier puis déplacée par `_tourner`.
QUESTIONS = (
    ("Une personne n'a aucune maladie diagnostiquée, mais vit dans un "
     "logement insalubre, souffre d'isolement social, dort très mal et "
     "présente une détresse psychologique importante. Selon la définition "
     "de l'OMS, que conclure ?",
     ("Elle n'est pas en bonne santé : la santé n'est pas la seule absence "
      "de maladie",
      "Elle est en bonne santé, puisqu'aucune maladie n'a été diagnostiquée",
      "On ne peut rien conclure tant qu'un médecin n'a pas posé de "
      "diagnostic",
      "Elle est en bonne santé physique, seule dimension que retient "
      "l'OMS"),
     0, 3,
     "L'OMS définit la santé comme un état de bien-être physique, mental "
     "et social, et pas seulement comme l'absence de maladie ou "
     "d'infirmité (Constitution adoptée en 1946, en vigueur depuis 1948). "
     "Un diagnostic ne suffit ni à déclarer une personne en bonne santé, "
     "ni à la déclarer malade.",
     1),

    ("Grâce à la prévention, un système évite des hospitalisations et "
     "réalise donc moins d'actes. Que dit le cours ?",
     ("Il peut obtenir de meilleurs résultats : la performance ne se "
      "mesure pas au nombre d'actes",
      "Sa performance baisse, puisque son activité diminue",
      "Il devient moins efficient, puisque ses équipements servent moins",
      "Il ne peut être jugé que sur ses indicateurs d'activité, seuls "
      "disponibles"),
     0, 3,
     "Mesurer l'activité (consultations, admissions, actes, journées) suit "
     "une logique de volume : facile à compter, mais muet sur la santé "
     "obtenue. Mesurer les résultats (espérance de vie en bonne santé, "
     "mortalité évitable, complications évitées) suit une logique de "
     "valeur. Plus d'actes ne fait pas un meilleur système.",
     1),

    ("Lequel de ces éléments fait partie du système de santé (health "
     "system), mais **pas** du système de soins (healthcare system) ?",
     ("La formation des professionnels de santé",
      "Les services de réadaptation",
      "Les laboratoires et l'imagerie",
      "La prévention délivrée par un médecin"),
     0, 4,
     "Le système de soins réunit professionnels, établissements et "
     "fonctions de soins — dont la prévention délivrée médicalement et la "
     "réadaptation. Il ne comprend ni le financement, ni la régulation, ni "
     "la santé publique, ni la formation des professionnels, qui "
     "appartiennent au système de santé.",
     2),

    ("Quelle relation lie le système de soins (healthcare system) et le "
     "système de santé (health system) ?",
     ("Une inclusion : le système de soins est l'une des composantes du "
      "système de santé",
      "Une équivalence : les deux expressions désignent le même ensemble",
      "Une inclusion : le système de santé est l'une des composantes du "
      "système de soins",
      "Aucune : ce sont deux ensembles séparés, les soins d'un côté, la "
      "santé publique de l'autre"),
     0, 3,
     "C'est une relation d'inclusion, pas d'équivalence. Au cœur, le "
     "système de soins ; autour, la prévention et la santé publique ; puis "
     "le financement, la régulation, la formation et l'information.",
     2),

    ("Le cours distingue santé individuelle, santé des populations et "
     "santé publique. Laquelle de ces définitions est celle de la "
     "**santé publique** ?",
     ("L'action organisée de la société pour améliorer l'état de santé : "
      "surveillance, prévention, protection, promotion, régulation",
      "L'état de santé d'un groupe, mesuré par des indicateurs agrégés, et "
      "sa répartition entre sous-groupes",
      "L'état de santé d'une personne et les soins qu'elle reçoit",
      "L'ensemble des soins délivrés par les hôpitaux publics"),
     0, 4,
     "La santé des populations est un état : celui d'un groupe, "
     "mesuré par des indicateurs agrégés. La santé publique est une "
     "action : celle que la société organise pour améliorer cet "
     "état.",
     3),

    ("Un enfant asthmatique a un traitement optimisé et un suivi "
     "respiratoire régulier, mais ses crises persistent. Laquelle de ces "
     "actions agit sur un déterminant de son état **hors** du champ du "
     "médecin de famille ?",
     ("Traiter l'humidité et les moisissures du logement",
      "Renforcer l'éducation thérapeutique du patient",
      "Ajuster le traitement médicamenteux",
      "Rapprocher les consultations de suivi respiratoire"),
     0, 4,
     "Le système de soins optimise le traitement, mais l'exposition "
     "demeure : pollution de l'air, humidité et moisissures, tabagisme "
     "dans le foyer, conditions sociales de la famille. Aucun de ces "
     "leviers n'appartient au médecin de famille : il faut coopérer avec "
     "les politiques du logement, de l'environnement, de l'éducation et "
     "avec les collectivités.",
     4),

    ("Selon le cours, comment les comportements individuels "
     "(alimentation, activité physique, conduites à risque) se rattachent-"
     "ils aux autres familles de déterminants ?",
     ("Ils sont largement façonnés par l'environnement social et "
      "économique et par l'environnement physique",
      "Ils en sont indépendants : ils relèvent du seul choix de chacun",
      "Ils comptent moins que le recours au système de soins, déterminant "
      "principal de la santé",
      "Ils n'interviennent qu'après une intervention médicale"),
     0, 4,
     "Trois familles de déterminants : l'environnement social et "
     "économique, l'environnement physique, les caractéristiques et "
     "comportements individuels. Les comportements sont eux-mêmes "
     "largement façonnés par les deux premières familles, et tous agissent "
     "avant toute intervention médicale.",
     4),

    ("Laquelle de ces affirmations n'est **pas** une condition d'un "
     "dépistage pertinent, selon le cours ?",
     ("La maladie doit être rare, pour limiter le nombre de personnes à "
      "tester",
      "Le test doit être fiable, acceptable et peu invasif",
      "Un traitement doit exister, plus efficace à un stade précoce",
      "Une filière de soins doit être organisée en aval"),
     0, 4,
     "Le dépistage (prévention secondaire) suppose au contraire une "
     "maladie assez fréquente et assez grave. Mal conçu, il produit des "
     "faux positifs, des examens inutiles et du surdiagnostic.",
     5),

    ("Que souligne l'OMS à propos des soins primaires (primary care) et "
     "des soins de santé primaires (Primary Health Care, PHC) ?",
     ("Un pays peut avoir de bons soins primaires sans avoir mis en œuvre "
      "de politique de soins de santé primaires",
      "Les deux expressions désignent le même premier niveau de soins",
      "Les soins de santé primaires sont un niveau de soins plus "
      "spécialisé que les soins primaires",
      "Un pays qui a mis en œuvre les soins de santé primaires n'a plus "
      "besoin de soins primaires"),
     0, 4,
     "Les soins primaires sont un niveau de soins : premier contact, "
     "continuité, coordination des soins individuels. Les soins de santé "
     "primaires sont une approche globale, bien plus large : soins "
     "primaires, fonctions essentielles de santé publique, action sur les "
     "déterminants et participation communautaire.",
     6),

    ("Selon le cours, protéger la population contre le risque financier "
     "de la maladie est…",
     ("un objectif du système, porté par le pilier financement",
      "un effet secondaire du financement, sans en être un objectif",
      "une mission du seul pilier gouvernance",
      "hors du champ du système de santé, l'affaire des assurances "
      "privées"),
     0, 4,
     "Le pilier financement collecte les ressources, les mutualise, les "
     "répartit entre les acteurs et protège la population contre le "
     "risque financier de la maladie. Le cours insiste : c'est un "
     "objectif du système, pas un effet secondaire.",
     7),

    ("« Le nombre de médecins formés aujourd'hui produit ses effets dans "
     "dix à vingt ans. » Quelle propriété de l'approche systémique cet "
     "exemple illustre-t-il ?",
     ("Les effets sont différés",
      "Les effets se propagent d'un pilier aux autres",
      "Les effets non voulus existent toujours",
      "Les piliers fonctionnent indépendamment les uns des autres"),
     0, 4,
     "Trois propriétés : les effets se propagent (augmenter le prix d'un "
     "acte modifie l'offre, donc les délais, donc le recours aux "
     "urgences), les effets sont différés (des années, parfois des "
     "décennies), et les effets non voulus existent toujours (un "
     "indicateur de volume mal calibré encourage une activité inutile).",
     8),

    ("Le pays A dépense beaucoup plus pour la santé que le pays B. Que "
     "conclut le cours ?",
     ("Rien sur sa performance : la dépense est un intrant, jamais un "
      "indicateur de performance",
      "Le pays A a le meilleur système, puisqu'il y consacre plus de "
      "moyens",
      "Le pays B est le plus efficient, puisqu'il dépense moins",
      "Le pays A offre forcément un meilleur accès aux soins"),
     0, 3,
     "La dépense mesure ce qu'on consacre au système, jamais ce qu'il "
     "produit : c'est un dénominateur. Deux pays peuvent dépenser autant "
     "pour des choses très différentes, et une offre abondante mais mal "
     "répartie ne profite pas à toute la population.",
     10),

    ("Des stocks, des marges et des redondances : entre quelles "
     "dimensions de l'évaluation créent-ils une tension ?",
     ("L'efficience et la résilience : inutiles en temps normal, "
      "indispensables en crise",
      "L'équité et l'accès : ils profitent aux uns au détriment des "
      "autres",
      "La qualité et la sécurité : plus de stocks, moins de soins sûrs",
      "La soutenabilité et les résultats de santé : ils financent l'avenir "
      "aux dépens du présent"),
     0, 4,
     "C'est la tension à retenir : marges, stocks et redondances sont "
     "inefficients en temps normal et indispensables dans une crise "
     "(pandémie, canicule, rupture d'approvisionnement, cyberattaque). "
     "Évaluer un système, c'est arbitrer entre les dimensions, pas les "
     "maximiser toutes à la fois.",
     10),

    ("Pourquoi le cours qualifie-t-il le système français de système "
     "**hybride** ?",
     ("Né de l'assurance sociale, il a aussi les traits d'un système "
      "national fortement piloté par l'État",
      "Il mêle médecine conventionnelle et médecines alternatives",
      "Il est financé à parts égales par l'État et par les patients",
      "Il est entièrement privé en ville et entièrement public à "
      "l'hôpital"),
     0, 3,
     "Historiquement bâti sur les cotisations, les caisses et les groupes "
     "professionnels, il présente aussi les traits d'un système national "
     "piloté par l'État. L'Observatoire européen des systèmes et des "
     "politiques de santé relève une couverture universelle, un rôle "
     "majeur de l'assurance maladie obligatoire, une large part de "
     "recettes fiscales, une forte intervention de l'État et un mélange "
     "d'offreurs publics et privés.",
     11),
)


def _build(rang, question, choices, answer, level, explanation, partie):
    choices, answer = _tourner(choices, answer, rang)
    pattern = qcm_pattern(
        "ie3514_s1_q%02d" % rang, rang, question, choices, answer, level,
        "%s Pour aller plus loin, revoyez la %s." % (explanation,
                                                     revoir(partie)))
    return replace(pattern, lesson=(
        INTITULE,
        "En cas d'erreur, revoyez la %s." % revoir(partie),
    ))


FICHES = (PREVENTION, NIVEAUX, PILIERS, DIMENSIONS, CONTINUUM, NOTIONS)

PATTERNS = FICHES + tuple(
    _build(number + 1, *entree) for number, entree in enumerate(QUESTIONS)
)

MODULE = Module(
    key="ie3514_s1",
    title="IE3514 - Revision Sheet for Session 1",
    level=4,
    summary=INTITULE,
    keys=tuple(p.key for p in PATTERNS),
)
