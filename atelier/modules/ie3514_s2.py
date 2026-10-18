"""Module « IE3514 - Revision Sheet for Session 2 », chapitre Révisions.

La séance 2 du cours IE3514 (Healthcare systems organization) retrace la
construction historique du système de santé français, de l'assistance du
XIXe siècle au Ségur de la santé. Ce module en tire des exercices de
révision, difficiles à très difficiles :

- des **textes à trous** : une fiche « problème posé → réponse » où
  l'élève choisit, pour chaque problème, la loi, l'institution ou le sigle
  qui y a répondu. La sortie à reproduire donne l'année, la nature de la
  réponse et la partie du cours qui la traite : un essai manqué montre,
  ligne à ligne, la partie à relire ;
- des **QCM** : l'explication de la bonne réponse renvoie elle aussi à la
  partie du cours.

Chaque exercice nomme dès son rappel la partie du cours à revoir. Les
parties sont numérotées comme dans les diapositives (I.3, IV.5…).
"""

from dataclasses import replace
import re

from ..engine import Module, Option, Pattern, qcm_pattern
from .qcm_docker import _tourner

# Intitulé demandé par l'enseignant, en tête de chaque exercice : l'élève
# peut tomber sur n'importe lequel en premier.
INTITULE = ("The following exercises are designed to help you make the most "
            "of your revision sessions. You answer the questions, and if you "
            "get a wrong answer, you will be shown the correct answer and "
            "directed to the relevant chapter to review if you wish to "
            "improve your understanding of the course material.")

# Lecture d'une fiche à trous, rappelée sur chacune.
FICHE = ("La fiche associe à chaque **problème posé** la réponse que le "
         "système lui a apportée. La sortie à reproduire donne, pour chaque "
         "ligne, l'**année**, la **nature** de cette réponse et la "
         "**partie du cours** qui la traite : en cas d'erreur, comparez les "
         "lignes pour savoir quelle partie relire.")

# Parties du cours de la séance 2, telles que les numérotent les
# diapositives.
PARTIES = {
    "I": "Avant 1945 : de l'assistance à l'assurance sociale",
    "II": "1944-1946 : le moment fondateur",
    "III": "1958-1975 : la construction du système hospitalier",
    "IV": "1980-1996 : la grande question de la régulation",
    "V": "1999-2016 : universalisation, droits du patient et parcours",
    "VI": "2018-2020 : des structures aux parcours",
    "VII": "Ce que l'histoire permet de comprendre (les dix principes)",
}

# Les réponses que l'histoire a apportées : clé -> (texte du menu, année,
# nature, partie du cours). La nature reste courte et distincte d'une
# entrée à l'autre : deux réponses de la même année et de la même partie
# (LFSS, ONDAM, ARH) ne doivent pas produire la même ligne.
FAITS = {
    "assistance": ("l'assistance médicale gratuite", "1893",
                   "aide aux malades privés de ressources", "I.3"),
    "accidents": ("la loi sur les accidents du travail", "1898",
                  "risque professionnel mutualisé", "I.4"),
    "retraites": ("la loi sur les retraites ouvrières et paysannes", "1910",
                  "premier régime de retraite interprofessionnel", "I.6"),
    "assurances": ("les assurances sociales", "1928-1930",
                   "assurance obligatoire de certains salariés", "I.7"),
    "famille": ("les allocations familiales", "1932",
                "régime obligatoire financé par les employeurs", "I.8"),
    "cnr": ("le programme du CNR", "1944",
            "plan de sécurité sociale annoncé", "II.1"),
    "ordonnances": ("les ordonnances d'octobre 1945", "1945",
                    "création de la Sécurité sociale", "II.4"),
    "preambule": ("le Préambule de la Constitution", "1946",
                  "santé garantie par la Nation", "II.7"),
    "chu": ("les CHU (réforme Debré)", "1958",
            "soin + enseignement + recherche", "III.2"),
    "branches": ("les branches de la Sécurité sociale", "1967",
                 "séparation financière des grands risques", "III.3"),
    "carte": ("la carte sanitaire", "1970",
              "besoins d'équipement selon la population", "III.4"),
    "convention": ("la convention médicale nationale", "1971",
                   "tarifs négociés avec les médecins libéraux", "III.5"),
    "medicosocial": ("la loi sur le secteur social et médico-social", "1975",
                     "personnes âgées, handicap, accompagnement", "III.6"),
    "prix_journee": ("le prix de journée", "avant 1983",
                     "paiement selon la durée du séjour", "IV.2"),
    "budget_global": ("le budget global", "1983-1984",
                      "enveloppe annuelle par établissement", "IV.2"),
    "csg": ("la CSG", "1990",
            "prélèvement sur l'ensemble des revenus", "IV.3"),
    "sros": ("les SROS", "1991",
             "planification régionale par activité", "IV.4"),
    "lfss": ("la LFSS", "1996",
             "vote annuel du Parlement", "IV.5"),
    "ondam": ("l'ONDAM", "1996",
              "trajectoire de dépense fixée à l'avance", "IV.5"),
    "arh": ("les ARH", "1996",
            "pilotage régional de l'offre hospitalière", "IV.5"),
    "cmu": ("la CMU", "1999",
            "couverture des résidents sans couverture obligatoire", "V.1"),
    "droits": ("la loi sur les droits des patients", "2002",
               "information, dignité, participation", "V.2"),
    "traitant": ("le médecin traitant", "2004",
                 "parcours de soins coordonné", "V.3"),
    "t2a": ("la T2A", "2004",
            "financement selon l'activité réalisée", "V.4"),
    "ars": ("les ARS (loi HPST)", "2009-2010",
            "pilote régional unique de la santé", "V.5"),
    "puma": ("la PUMa", "2016",
             "droit personnel : travail ou résidence stable", "V.6"),
    "ght": ("les GHT", "2016",
            "stratégie de soins commune et graduée", "V.7"),
    "ma_sante": ("Ma Santé 2022", "2018",
                 "des structures aux parcours", "VI.1"),
    "segur": ("le Ségur de la santé", "2020",
              "revalorisation, investissement, numérique", "VI.3"),
}

BLANKS = "abcd"


def _ligne(fait):
    """Ce que produit une réponse : son année, sa nature, sa partie."""
    _menu, annee, nature, partie = FAITS[fait]
    return "%s · %s — cours : partie %s" % (annee, nature, partie)


def _lecon(parties):
    return (INTITULE,
            "Cours à revoir : " + " ; ".join(
                "partie %s, « %s »" % (p, PARTIES[p]) for p in parties) + ".",
            FICHE)


def fiche(key, name, brief, why, parties, lignes, level):
    """Un texte à trous : une ligne par problème, un menu par ligne.

    `lignes` donne, pour chaque problème, son énoncé, la bonne réponse,
    puis trois réponses voisines — même époque ou même domaine — que
    l'élève doit savoir écarter.
    """
    tpl = []
    blanks = {}
    for rang, (probleme, bonne, *voisines) in enumerate(lignes):
        blank = BLANKS[rang]
        tpl.append("%d. %s\n   → @%s@" % (rang + 1, probleme, blank))
        blanks[blank] = ("Réponse au problème %d" % (rang + 1), [
            Option(chr(ord("a") + i), FAITS[fait][0],
                   lambda _p, fait=fait: _ligne(fait))
            for i, fait in enumerate((bonne,) + tuple(voisines))
        ])

    def rows(p, get):
        return ["%d. %s" % (rang + 1, get(blank)(p))
                for rang, blank in enumerate(blanks)]

    return Pattern(
        key=key,
        name=name,
        brief=brief,
        why=why,
        lesson=_lecon(parties),
        tpl="Problème posé\n   → réponse apportée\n\n" + "\n\n".join(tpl),
        blanks=blanks,
        ref={blank: "a" for blank in blanks},
        rows=rows,
        level=level,
    )


# --------------------------------------------------------------------------
# Textes à trous
# --------------------------------------------------------------------------

FICHES = (
    fiche(
        "rev_avant_1945", "Avant 1945 : les premières briques",
        "Retrouver la loi qui répond à chacun des problèmes de la fin du "
        "XIXe siècle et de l'entre-deux-guerres.",
        "La protection passe d'une logique d'assistance à une logique "
        "d'assurance.",
        ("I",),
        (("Aider le malade qui ne peut pas payer, sous condition de "
          "ressources", "assistance", "accidents", "assurances", "famille"),
         ("Indemniser l'ouvrier blessé sans qu'il ait à prouver la faute de "
          "l'employeur", "accidents", "assistance", "retraites",
          "assurances"),
         ("Couvrir des salariés de l'industrie et du commerce contre la "
          "maladie, la maternité, l'invalidité, la vieillesse et le décès",
          "assurances", "retraites", "famille", "ordonnances"),
         ("Faire entrer la politique familiale dans la protection sociale",
          "famille", "assurances", "retraites", "medicosocial")),
        level=3,
    ),
    fiche(
        "rev_fondation", "1944-1946 : trois textes fondateurs",
        "Retrouver le texte qui porte chacune des décisions du moment "
        "fondateur.",
        "Le CNR fixe l'ambition, 1945 crée les institutions, 1946 en fait "
        "un droit.",
        ("II",),
        (("Garantir aux citoyens les moyens d'existence quand le travail ne "
          "le permet plus", "cnr", "ordonnances", "preambule", "assurances"),
         ("Créer les organismes de sécurité sociale, financés par des "
          "cotisations et gérés avec les partenaires sociaux",
          "ordonnances", "cnr", "preambule", "branches"),
         ("Donner un fondement juridique à toute extension ultérieure de la "
          "couverture", "preambule", "cnr", "ordonnances", "droits")),
        level=3,
    ),
    fiche(
        "rev_hopital", "1958-1975 : l'hôpital moderne et ses voisins",
        "Retrouver la réforme qui répond à chacun des problèmes posés par "
        "une médecine devenue technique, spécialisée et coûteuse.",
        "Chaque réforme de 1958 à 1975 répond au changement de nature de "
        "la médecine.",
        ("III",),
        (("Former les professionnels et faire de la recherche au sein même "
          "de l'hôpital", "chu", "carte", "convention", "branches"),
         ("Pouvoir parler du déficit de la maladie indépendamment de la "
          "vieillesse et de la famille", "branches", "chu", "budget_global",
          "lfss"),
         ("Décider quels équipements installer, où, et pour quelle "
          "population", "carte", "sros", "chu", "ght"),
         ("Concilier liberté d'installation et financement socialisé des "
          "actes", "convention", "traitant", "carte", "medicosocial")),
        level=3,
    ),
    fiche(
        "rev_financer_hopital", "Financer l'hôpital : quarante ans de "
        "réformes",
        "Retrouver le mode de financement ou la réforme qui répond à "
        "chacun des problèmes du financement hospitalier.",
        "Chaque mode de financement corrige l'effet pervers du précédent, "
        "et crée le sien.",
        ("IV", "V", "VI"),
        (("Point de départ : financer l'établissement en proportion de la "
          "durée des séjours", "prix_journee", "budget_global", "t2a",
          "ondam"),
         ("Les séjours s'allongent : plus le patient reste, plus "
          "l'établissement facture", "budget_global", "prix_journee", "t2a",
          "ondam"),
         ("Avec une enveloppe annuelle, les moyens se figent et l'activité "
          "réelle compte à peine", "t2a", "budget_global", "prix_journee",
          "ondam"),
         ("Le financement à l'activité pousse au volume : on annonce en "
          "sortir", "segur", "ma_sante", "t2a", "ght")),
        level=4,
    ),
    fiche(
        "rev_regulation", "1990-1996 : financer et réguler",
        "Retrouver l'instrument qui répond à chacun des problèmes de "
        "financement et de pilotage de 1990 à 1996.",
        "Comment maintenir un système solidaire tout en maîtrisant la "
        "croissance de la dépense ?",
        ("IV",),
        (("Faire contribuer d'autres revenus que ceux du travail",
          "csg", "lfss", "ondam", "sros"),
         ("Donner au Parlement un vote annuel sur les grandes orientations "
          "financières de la Sécurité sociale", "lfss", "ondam", "csg",
          "arh"),
         ("Cesser de constater la dépense après coup", "ondam", "lfss",
          "budget_global", "csg"),
         ("Associer l'État et l'assurance maladie pour piloter régionalement "
          "l'offre hospitalière publique et privée", "arh", "ars", "sros",
          "ght")),
        level=4,
    ),
    fiche(
        "rev_universalisation", "1999-2016 : droit universel, parcours, "
        "territoires",
        "Retrouver la réforme qui répond à chacun des problèmes de la "
        "période 1999-2016.",
        "La couverture se détache de l'emploi, le parcours remplace l'acte "
        "isolé.",
        ("V",),
        (("Couvrir les résidents réguliers restés hors des régimes "
          "obligatoires", "cmu", "puma", "ordonnances", "droits"),
         ("Couvrir chaque adulte en son nom propre, sans statut d'ayant "
          "droit", "puma", "cmu", "droits", "ordonnances"),
         ("Remplacer une succession d'actes indépendants par un recours "
          "organisé autour du patient", "traitant", "t2a", "ght",
          "convention"),
         ("Réunir sous un seul pilote régional santé publique, prévention, "
          "soins et médico-social", "ars", "arh", "sros", "ght")),
        level=4,
    ),
    fiche(
        "rev_principes", "Les principes et leurs décisions datées",
        "Retrouver la décision datée à laquelle se rattache chacun des "
        "principes du système français.",
        "Chaque principe se rattache à une décision datée : c'est ce lien "
        "que l'examen attend.",
        ("VII",),
        (("Principe 1, la solidarité : son héritage central",
          "ordonnances", "cnr", "preambule", "assurances"),
         ("Principe 2, la couverture universelle : l'aboutissement du droit",
          "puma", "cmu", "ordonnances", "preambule"),
         ("Principe 4, liberté professionnelle mais régulation collective : "
          "son ancrage", "convention", "traitant", "medicosocial",
          "budget_global"),
         ("Principe 7, la territorialisation : son premier instrument",
          "carte", "sros", "ars", "ght")),
        level=4,
    ),
    fiche(
        "rev_aujourdhui", "Du patient acteur au Ségur",
        "Retrouver la réforme qui répond à chacun des problèmes de la "
        "période récente.",
        "Le système cherche à s'organiser autour du patient et de son "
        "parcours.",
        ("V", "VI"),
        (("Le patient n'est plus l'objet des soins mais un acteur titulaire "
          "de droits", "droits", "preambule", "traitant", "cmu"),
         ("Un système trop cloisonné et trop centré sur les actes face au "
          "vieillissement et aux maladies chroniques", "ma_sante", "segur",
          "ars", "t2a"),
         ("Après la crise du Covid-19 : rendre les métiers attractifs et "
          "investir dans le numérique en santé", "segur", "ma_sante", "ght",
          "ondam")),
        level=3,
    ),
)


# --------------------------------------------------------------------------
# QCM
# --------------------------------------------------------------------------

# (énoncé, (quatre propositions), index de la bonne, niveau, explication,
# partie du cours). Comme dans qcm_docker, la bonne réponse est écrite en
# premier puis déplacée par `_tourner`.
QUESTIONS = (
    ("Qu'est-ce qui distingue la logique d'**assurance** de la logique "
     "d'**assistance** ?",
     ("L'accès dépend de l'affiliation, et non des ressources",
      "L'accès dépend d'un examen des ressources",
      "Le financement repose principalement sur la collectivité",
      "L'aide va d'abord à la personne qui ne peut pas payer"),
     0, 3,
     "L'assurance suit la chaîne cotisation → mutualisation → prestation : "
     "c'est l'affiliation qui ouvre le droit. Les trois autres propositions "
     "décrivent l'assistance (besoin → aide).",
     "I.2"),

    ("Erreur fréquente à l'examen : que font, au juste, les ordonnances "
     "des 4 et 19 octobre 1945 ?",
     ("Elles créent la Sécurité sociale et généralisent la protection, sans "
      "l'unifier : les régimes spéciaux subsistent",
      "Elles unifient toute la protection sociale dans un régime unique",
      "Elles fondent la couverture sur la résidence et l'impôt, comme le "
      "modèle de Beveridge",
      "Elles créent des caisses nationales distinctes pour la maladie, la "
      "vieillesse et la famille"),
     0, 4,
     "L'ambition était large, mais plusieurs professions ont voulu garder "
     "leur propre régime : 1945 généralise sans unifier. Les caisses "
     "nationales par branche datent des ordonnances de 1967.",
     "II.4-II.5"),

    ("Lequel de ces traits du système français est **resté bismarckien** ?",
     ("La place des partenaires sociaux",
      "Une part substantielle de financement par l'impôt",
      "Une forte régulation par l'État",
      "Une couverture fondée sur la résidence"),
     0, 3,
     "Restent bismarckiens l'assurance maladie obligatoire, les "
     "cotisations, la place des partenaires sociaux et la logique "
     "d'assurance. Les trois autres traits sont devenus beveridgiens.",
     "VII (zoom sur le principe 3)"),

    ("Pourquoi la création de la CSG en 1990 est-elle le glissement le plus "
     "net vers le modèle de Beveridge ?",
     ("Elle prélève sur un large ensemble de revenus : une couverture "
      "universelle appelle un financement universel",
      "Elle remplace les caisses d'assurance maladie par un service "
      "national de santé",
      "Elle fixe chaque année un objectif national de dépenses d'assurance "
      "maladie",
      "Elle supprime les cotisations assises sur les salaires"),
     0, 4,
     "La CSG passe des cotisations sur le travail à un prélèvement sur tous "
     "les revenus : c'est une fiscalisation **partielle** du financement. "
     "Les cotisations demeurent, et l'objectif de dépenses est l'ONDAM de "
     "1996.",
     "IV.3"),

    ("Quel est l'effet pervers reproché au **budget global** des hôpitaux "
     "(1983-1984) ?",
     ("Les moyens se figent et l'activité réelle est à peine prise en compte",
      "Plus le patient reste longtemps, plus l'établissement facture de "
      "journées",
      "Il incite au volume et pose la question de la pertinence des actes",
      "Il laisse la dépense hospitalière sans aucun plafond"),
     0, 3,
     "L'enveloppe annuelle maîtrise la dépense mais ignore l'activité. Le "
     "séjour qui s'allonge est l'effet pervers du prix de journée ; "
     "l'incitation au volume, celui de la T2A de 2004.",
     "IV.2"),

    ("Que change l'ONDAM, créé par le plan Juppé, dans la logique de la "
     "dépense d'assurance maladie ?",
     ("On ne constate plus la dépense après coup : on définit à l'avance "
      "une trajectoire nationale",
      "Le Parlement vote chaque année les grandes orientations financières "
      "de la Sécurité sociale",
      "L'État et l'assurance maladie pilotent ensemble l'offre hospitalière "
      "régionale",
      "Chaque établissement reçoit une enveloppe annuelle pour fonctionner"),
     0, 4,
     "L'ONDAM est un objectif fixé à l'avance. Le vote annuel est celui de "
     "la LFSS, le pilotage régional celui des ARH, l'enveloppe par "
     "établissement le budget global de 1983-1984.",
     "IV.5"),

    ("Quelle phrase résume le changement de fondement du droit opéré par la "
     "CMU (1999) puis la PUMa (2016) ?",
     ("« Je suis couvert parce que j'appartiens durablement à la communauté "
      "nationale de résidence. »",
      "« Je suis couvert parce que j'ai un emploi. »",
      "« Je suis couvert parce que je n'ai pas de ressources. »",
      "« Je suis couvert parce que mon employeur cotise pour moi. »"),
     0, 3,
     "Le droit cesse de reposer sur l'emploi : la PUMa l'attache au "
     "travail **ou** à la résidence stable et régulière, ce qui éloigne la "
     "France du modèle bismarckien pur.",
     "V.1 et V.6"),

    ("Selon le cours, quelle leçon de résilience la crise du Covid-19 "
     "a-t-elle rappelée ?",
     ("Les marges et les redondances qui paraissaient inefficaces en temps "
      "normal se sont révélées décisives",
      "La T2A a permis d'absorber l'afflux de patients sans moyens "
      "supplémentaires",
      "Concentrer tous les équipements dans les CHU a suffi à faire face",
      "Le cloisonnement entre ville, hôpital et médico-social a protégé le "
      "système"),
     0, 4,
     "La crise a montré la mobilisation des professionnels et la capacité "
     "d'adaptation, mais aussi des fragilités : effectifs, tensions "
     "hospitalières, coordination, systèmes d'information. Les marges "
     "jugées inefficaces ont fait la différence.",
     "VI.2"),

    ("Pourquoi un CHU n'est-il pas simplement « un très grand hôpital » ?",
     ("Il associe soin, enseignement et recherche, organisés conjointement "
      "avec les facultés",
      "Il est le seul établissement autorisé à accueillir les urgences",
      "Il est financé directement par l'État, hors assurance maladie",
      "Il regroupe tous les hôpitaux publics d'un territoire"),
     0, 3,
     "L'ordonnance du 30 décembre 1958 (réforme Debré) crée les CHU : "
     "soin + enseignement + recherche, avec des postes "
     "hospitalo-universitaires. Le regroupement territorial, ce sont les "
     "GHT de 2016.",
     "III.2"),

    ("Quelle difficulté, héritée de la loi de 1975, Ma Santé 2022 "
     "cherche-t-elle encore à résoudre en 2018 ?",
     ("Trois univers organisés séparément : soins de ville, hôpital et "
      "médico-social",
      "L'absence de couverture des résidents sans emploi",
      "Le paiement des hôpitaux au prix de journée",
      "L'absence de toute planification des équipements hospitaliers"),
     0, 4,
     "Financeurs, tutelles et cultures distincts : la coordination des trois "
     "univers est le grand sujet des décennies suivantes. Les trois autres "
     "problèmes ont déjà reçu leur réponse : la carte sanitaire en 1970, le "
     "budget global en 1983-1984, la CMU en 1999.",
     "III.6 et VI.1"),

    ("Que disent les principes 8 (liberté et régulation) et 9 (qualité et "
     "soutenabilité) du système français ?",
     ("Ce sont des arbitrages, jamais des solutions : ils sont rejoués à "
      "chaque réforme",
      "Ce sont des acquis de 1945 qui n'ont jamais été remis en question",
      "Ils ont été tranchés une fois pour toutes par le plan Juppé",
      "Ils ne concernent que l'hôpital public"),
     0, 4,
     "Ce qui n'a jamais été remis en question depuis 1945, ce sont la "
     "solidarité, la mutualisation et l'assurance obligatoire. Les "
     "principes 8 et 9, eux, sont des tensions permanentes.",
     "VII (principes 7 à 10)"),

    ("Par quel canal le modèle bismarckien nourrit-il directement la "
     "réflexion française des années 1920 ?",
     ("L'Alsace-Moselle, revenue à la France après la Première Guerre "
      "mondiale, avait connu les assurances sociales allemandes",
      "Le rapport Beveridge, que la France adopte dès sa publication",
      "Le programme du Conseil national de la Résistance",
      "Les ordonnances rédigées sous la direction de Pierre Laroque"),
     0, 4,
     "L'Allemagne de Bismarck bâtit entre 1881 et 1889 le premier grand "
     "système d'assurance sociale ; l'expérience de l'Alsace-Moselle "
     "irrigue la réflexion française dès les années 1920. Le rapport "
     "Beveridge date de 1942, le CNR de 1944, les ordonnances de 1945.",
     "I.5"),
)


def _question(rang, question, choices, answer, level, explanation, partie):
    choices, answer = _tourner(choices, answer, rang)
    explanation = "%s À revoir : partie %s du cours." % (explanation, partie)
    pattern = qcm_pattern("rev_qcm_%02d" % rang, rang, question, choices,
                          answer, level, explanation)
    # « III.6 et VI.1 » -> parties III et VI, pour le rappel en tête.
    racines = []
    for racine in re.findall(r"\b([IVX]+)\b", partie):
        if racine not in racines:
            racines.append(racine)
    return replace(pattern, lesson=_lecon(racines)[:2])


PATTERNS = FICHES + tuple(
    _question(number + 1, *entree) for number, entree in enumerate(QUESTIONS)
)

MODULE = Module(
    key="ie3514_s2",
    title="IE3514 - Revision Sheet for Session 2",
    level=4,
    summary="Construction historique du système de santé français, de "
            "l'assistance de 1893 au Ségur de 2020 : textes à trous et QCM "
            "difficiles, chacun renvoyant à la partie du cours à revoir.",
    keys=tuple(p.key for p in PATTERNS),
)
