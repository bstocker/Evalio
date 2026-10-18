"""Module « IE3514 - Revision Sheet for Session 3 », du chapitre Révisions.

Une fiche de révision sur la gouvernance du système de santé français, du
niveau national aux territoires : les six fonctions de la gouvernance, le
Parlement et l'ONDAM, les directions du ministère (DGS, DGOS, DSS), les
agences (HAS, ANSM, Santé publique France, CNSA, ATIH, ANS), l'Assurance
maladie, les ARS, la démocratie sanitaire et les trois cas d'étude.

Deux formes d'exercices :

- des **textes à trous** : chaque menu complète une phrase du cours. La
  sortie est une fiche de vérification, une ligne par trou : « conforme
  au cours », ou la partie et la diapositive à revoir. La cible ne dit
  donc rien de la réponse, seulement qu'il faut que tout soit conforme ;
- des **QCM**, sur le modèle de `docker_bases`.

Chaque réponse fausse renvoie à la partie du cours qui porte la bonne : la
fiche de vérification pour les textes à trous, une note sur la proposition
choisie pour les QCM. Cette note ne nomme jamais la bonne réponse ; seule
la bonne proposition porte l'explication.

Les parties et les diapositives sont celles du support de la séance 3
(IE.3514 — Healthcare systems organization).
"""

from dataclasses import replace

from ..engine import Module, Option, Pattern, qcm_pattern
from .qcm_docker import _tourner

# Le chapeau demandé par l'enseignant, rappelé en tête de chaque exercice.
INTRO = ("Ces exercices sont conçus pour vous aider à tirer le meilleur "
         "parti de vos révisions. Répondez aux questions : chaque erreur "
         "vous renvoie à la partie du cours à revoir pour mieux comprendre "
         "la notion.")


def _revoir(partie):
    """Renvoi vers le support : « partie IV.2 du cours, diapositive 23 »."""
    return "partie %s du cours, diapositive %s" % partie


# --------------------------------------------------------------------------
# Textes à trous
# --------------------------------------------------------------------------

LECON_TROUS = (
    INTRO,
    "Chaque menu complète une phrase du cours. Une seule proposition rend "
    "la phrase exacte.",
    "La fiche de vérification juge chaque trou séparément : « conforme au "
    "cours », ou la partie et la diapositive à revoir.",
)


def _texte_a_trous(key, name, brief, why, level, tpl, trous):
    """Un texte à trous : un paragraphe du cours et un menu par trou.

    `trous` est une suite de (identifiant, intitulé du menu, (bonne,
    fausse, fausse, fausse), (partie, diapositive)). La bonne proposition
    est écrite en premier ; chaque copie reçoit les menus dans son propre
    ordre (cf. `shuffled_blanks`).
    """
    blanks, ref, renvois = {}, {}, []
    for blank_id, label, propositions, partie in trous:
        blanks[blank_id] = (label, [
            Option(oid, texte, (lambda juste: lambda _p: juste)(oid == "a"))
            for oid, texte in zip("abcd", propositions)
        ])
        ref[blank_id] = "a"
        renvois.append((blank_id, _revoir(partie)))

    def rows(params, get):
        return ["Trou %d : %s" % (numero, "conforme au cours"
                                  if get(blank_id)(params)
                                  else "à revoir, " + renvoi)
                for numero, (blank_id, renvoi) in enumerate(renvois, 1)]

    return Pattern(key=key, name=name, brief=brief, why=why,
                   lesson=LECON_TROUS, tpl=tpl, blanks=blanks, ref=ref,
                   rows=rows, level=level)


FONCTIONS = _texte_a_trous(
    key="ie3514_fonctions",
    name="Gouverner n'est pas soigner",
    brief="Compléter la définition des fonctions de la gouvernance.",
    why="Chaque acteur exerce une fonction précise, distincte de la "
        "production des soins.",
    level=3,
    tpl="""La gouvernance réunit six fonctions, distinctes de la production
des soins.

[1] @t1@ : définir les règles que les acteurs doivent respecter.
    « Quelles conditions pour pratiquer la chirurgie cardiaque ? »

[2] @t2@ : répartir les ressources et structurer l'offre.
    « Combien de services spécialisés sur un territoire ? »

[3] La HAS, Santé publique France ou l'ATIH produisent une information
    indispensable ; ce qu'elles ne font pas, c'est @t3@.

[4] L'Assurance maladie finance une grande partie des soins ; en
    général, ce qu'elle ne fait pas elle-même, c'est @t4@.""",
    trous=(
        ("t1", "Fonction [1]",
         ("Réguler", "Organiser", "Décider", "Financer"),
         ("I.2", "9")),
        ("t2", "Fonction [2]",
         ("Organiser", "Réguler", "Évaluer et contrôler", "Décider"),
         ("I.2", "9")),
        ("t3", "Ce que l'expertise ne fait pas [3]",
         ("décider à la place des pouvoirs publics",
          "évaluer les médicaments et les technologies de santé",
          "surveiller l'état de santé de la population",
          "recueillir les données d'activité des hôpitaux"),
         ("XII", "47")),
        ("t4", "Ce que le financeur ne fait pas [4]",
         ("délivrer les soins",
          "rembourser les soins",
          "négocier les conventions avec les professionnels",
          "réguler une grande partie des soins de ville"),
         ("XII", "47")),
    ),
)

PARLEMENT = _texte_a_trous(
    key="ie3514_lfss_ondam",
    name="Le Parlement, la LFSS et l'ONDAM",
    brief="Compléter ce que le Parlement vote, et ce qu'est l'ONDAM.",
    why="Le Parlement ne vote pas seulement des règles : il fixe aussi le "
        "cadre financier.",
    level=4,
    tpl="""[1] Depuis @t1@, le Parlement vote chaque année la loi de
    financement de la sécurité sociale (LFSS).

[2] Cette loi est préparée par @t2@, qui suit aussi les recettes
    et les dépenses des branches.

[3] L'ONDAM qu'elle fixe est @t3@ : un patient
    qui tombe malade en fin d'année continue d'être soigné, même si
    beaucoup de soins ont déjà été consommés.

[4] Le Parlement agit donc à la fois comme législateur et comme
    @t4@.""",
    trous=(
        ("t1", "Année [1]",
         ("1996", "1945", "2004", "2010"),
         ("II.1", "13")),
        ("t2", "Qui prépare la LFSS ? [2]",
         ("la Direction de la sécurité sociale (DSS)",
          "la Direction générale de l'offre de soins (DGOS)",
          "la Caisse nationale de l'Assurance maladie (CNAM)",
          "la Haute Autorité de santé (HAS)"),
         ("II.1", "13")),
        ("t3", "Nature de l'ONDAM [3]",
         ("un objectif de dépenses, instrument de régulation",
          "un budget limitatif, comme les crédits d'une administration",
          "une enveloppe négociée chaque année entre la CNAM et les "
          "médecins",
          "un plafond de remboursement fixé pour chaque assuré"),
         ("II.2", "14")),
        ("t4", "Second rôle du Parlement [4]",
         ("financeur du système",
          "opérateur de soins",
          "autorité d'expertise scientifique",
          "pilote régional de l'offre"),
         ("II.1", "13")),
    ),
)

DIRECTIONS = _texte_a_trous(
    key="ie3514_directions",
    name="DGS, DGOS ou DSS ?",
    brief="Attribuer chaque mission à la bonne direction.",
    why="Les directions travaillent sur les mêmes sujets, mais pas au même "
        "point de la chaîne.",
    level=3,
    tpl="""[1] Pour le cancer, les programmes de dépistage relèvent de @t1@.

[2] La disponibilité des oncologues et les autorisations d'activités
    spécialisées relèvent de @t2@.

[3] Le Centre de crise sanitaire, qui prépare le système aux menaces
    sanitaires, est rattaché à @t3@.

[4] La tutelle de la CNAV, de la CNAF et de l'Urssaf Caisse nationale
    revient à @t4@.""",
    trous=(
        ("t1", "Direction [1]",
         ("la DGS", "la DGOS", "la DSS", "la CNAM"),
         ("III.3", "19")),
        ("t2", "Direction [2]",
         ("la DGOS", "la DGS", "la DSS", "la CNAM"),
         ("III.3", "19")),
        ("t3", "Direction [3]",
         ("la DGS", "la DGOS", "la DSS", "la CNAM"),
         ("III.1", "17")),
        ("t4", "Direction [4]",
         ("la DSS", "la DGS", "la DGOS", "la CNAM"),
         ("III.4", "20")),
    ),
)

MEDICAMENT = _texte_a_trous(
    key="ie3514_medicament",
    name="Le parcours d'un médicament remboursé",
    brief="Compléter, étape par étape, le chemin d'un médicament jusqu'à "
          "son remboursement.",
    why="Sept étapes, et presque autant d'acteurs : aucun ne décide seul.",
    level=4,
    tpl="""[1] Avant d'être vendu, un médicament reçoit une autorisation de mise
    sur le marché (AMM), délivrée par @t1@ au vu
    du rapport bénéfice/risque.

[2] La commission de la transparence de @t2@ évalue ensuite le service
    médical rendu et l'amélioration qu'il apporte.

[3] Le prix est négocié avec l'industriel par @t3@.

[4] Le taux de remboursement est fixé par @t4@ ; la décision finale de
    prise en charge revient aux pouvoirs publics.

[5] Une fois le médicament sur le marché, la pharmacovigilance relève
    de @t5@.""",
    trous=(
        ("t1", "Qui autorise ? [1]",
         ("l'ANSM ou l'Union européenne", "la HAS", "le CEPS", "l'UNCAM"),
         ("VIII.1", "40")),
        ("t2", "Qui évalue le service rendu ? [2]",
         ("la HAS", "l'ANSM", "le CEPS", "Santé publique France"),
         ("VIII.1", "40")),
        ("t3", "Qui négocie le prix ? [3]",
         ("le CEPS", "l'UNCAM", "la HAS", "la DSS"),
         ("VIII.1", "40")),
        ("t4", "Qui fixe le taux ? [4]",
         ("l'UNCAM", "le CEPS", "la HAS", "la DSS"),
         ("VIII.1", "40")),
        ("t5", "Qui surveille ? [5]",
         ("l'ANSM", "Santé publique France", "la HAS", "l'ATIH"),
         ("IV.3", "24")),
    ),
)

ARS = _texte_a_trous(
    key="ie3514_ars",
    name="L'ARS, pilote régional",
    brief="Compléter ce qui fonde l'ARS et ce dont elle dispose.",
    why="Le niveau national fixe le cadre ; l'ARS l'adapte à sa région.",
    level=4,
    tpl="""[1] Pour mettre fin à la fragmentation, les agences régionales de
    santé ont été créées par @t1@, puis installées
    en 2010.

[2] Le projet régional de santé comprend un cadre d'orientation
    stratégique à long terme et @t2@, qui fixe
    les objectifs opérationnels.

[3] La capacité de financement souple de l'ARS, pour la prévention,
    l'organisation des soins et l'innovation, s'appelle @t3@.

[4] Au plus près du terrain, l'ARS conclut avec les collectivités
    territoriales des @t4@.""",
    trous=(
        ("t1", "Texte fondateur [1]",
         ("la loi HPST de 2009",
          "la loi du 29 décembre 2011",
          "la LFSS de 1996",
          "les ordonnances de 1945"),
         ("VI.1", "32")),
        ("t2", "Second volet du projet régional [2]",
         ("un schéma régional de santé",
          "un contrat local de santé",
          "une stratégie nationale de santé",
          "un fonds d'intervention régional"),
         ("VI.3", "34")),
        ("t3", "Financement [3]",
         ("le FIR", "l'ONDAM", "le PMSI", "la LFSS"),
         ("VI.4", "35")),
        ("t4", "Accords locaux [4]",
         ("contrats locaux de santé (CLS)",
          "conventions médicales",
          "conseils territoriaux de santé (CTS)",
          "autorisations d'activité de soins"),
         ("VII.1", "37")),
    ),
)

DEMOCRATIE = _texte_a_trous(
    key="ie3514_democratie",
    name="La démocratie sanitaire, échelon par échelon",
    brief="Placer chaque instance à son échelon, et distinguer celle qui "
          "décide.",
    why="Ne jamais confondre une instance qui décide et une instance "
        "consultative.",
    level=4,
    tpl="""[1] Au niveau national, @t1@ est un organe consultatif placé auprès
    du ministre.

[2] Auprès de chaque ARS, @t2@ représente professionnels,
    établissements, collectivités, associations et usagers, et rend des
    avis sur la politique régionale.

[3] Au niveau territorial, la concertation locale passe par
    @t3@.

[4] Ces instances consultent, représentent et donnent des avis ; seule
    @t4@ décide et pilote, dans le cadre de ses compétences.""",
    trous=(
        ("t1", "Instance nationale [1]",
         ("la Conférence nationale de santé (CNS)",
          "la Haute Autorité de santé (HAS)",
          "la Caisse nationale de l'Assurance maladie (CNAM)",
          "Santé publique France"),
         ("VII.2", "38")),
        ("t2", "Instance régionale [2]",
         ("la CRSA", "le CTS", "la CNS", "le CLS"),
         ("VII.2", "38")),
        ("t3", "Instance territoriale [3]",
         ("les conseils territoriaux de santé (CTS)",
          "la CRSA",
          "les CPAM",
          "les GHT"),
         ("VII.2", "38")),
        ("t4", "Qui décide ? [4]",
         ("l'ARS", "la CRSA", "la CNS", "la CPAM"),
         ("VII.2", "38")),
    ),
)

TROUS = (FONCTIONS, PARLEMENT, DIRECTIONS, MEDICAMENT, ARS, DEMOCRATIE)


# --------------------------------------------------------------------------
# QCM
# --------------------------------------------------------------------------

# (énoncé, (quatre propositions), index de la bonne, niveau, explication,
#  (partie, diapositive))
# Comme dans qcm_docker, la bonne réponse est écrite en premier puis
# déplacée par `_tourner`.
QUESTIONS = (
    ("Une question est posée : « Quel financement pour les soins de "
     "ville ? ». Dans la grille des six fonctions de la gouvernance, de "
     "laquelle relève-t-elle ?",
     ("Financer : déterminer quelles activités sont financées, à quel "
      "niveau et selon quelles règles",
      "Organiser : répartir les ressources et structurer l'offre",
      "Réguler : définir les règles que les acteurs doivent respecter",
      "Décider : fixer les grandes orientations politiques"),
     0, 3,
     "C'est l'exemple même du cours pour la fonction « financer ». "
     "« Combien de services spécialisés sur un territoire ? » relèverait "
     "d'organiser, et « Faut-il développer la prévention ? » de décider.",
     ("I.2", "9")),

    ("Fin novembre, les dépenses d'assurance maladie dépassent déjà "
     "l'ONDAM voté pour l'année. Que se passe-t-il pour un patient qui "
     "tombe malade en décembre ?",
     ("Il est soigné et pris en charge : l'ONDAM est un objectif de "
      "dépenses, pas un budget limitatif",
      "Ses soins non urgents sont reportés à l'année suivante, faute de "
      "crédits",
      "Le Parlement doit voter une nouvelle LFSS avant tout nouveau "
      "remboursement",
      "L'ARS plafonne le nombre de consultations remboursées par assuré"),
     0, 3,
     "L'ONDAM est une trajectoire de dépenses fixée à l'avance, un "
     "instrument de régulation. La dépense réelle résulte de millions de "
     "décisions de patients, de médecins et d'établissements ; on agit "
     "ensuite sur les tarifs, les prescriptions, l'organisation et la "
     "pertinence.",
     ("II.2", "14")),

    ("Laquelle de ces propositions n'est **pas** l'une des trois "
     "orientations du projet de stratégie nationale de santé 2023-2033 ?",
     ("Garantir à chaque patient un médecin traitant à moins de trente "
      "minutes de chez lui",
      "Vivre plus longtemps en bonne santé",
      "Répondre aux besoins de santé sur l'ensemble du territoire",
      "Améliorer la résilience du système face aux crises et aux enjeux "
      "environnementaux"),
     0, 4,
     "Les trois orientations sont : vivre plus longtemps en bonne santé, "
     "répondre aux besoins sur tout le territoire, et rendre le système "
     "plus résilient. La stratégie, inscrite au code de la santé "
     "publique, fixe un cadre pluriannuel ; les niveaux régional et local "
     "le traduisent en actions.",
     ("II.3", "15")),

    ("Sur le vieillissement, quelle répartition des rôles le cours "
     "retient-il ?",
     ("La DGS prévient, la DGOS organise les soins, la DSS finance, la "
      "CNSA soutient l'autonomie",
      "La DGOS prévient, la DGS organise les soins, la DSS finance, la "
      "CNSA soutient l'autonomie",
      "La DGS prévient, la DSS organise les soins, la CNSA finance, la "
      "DGOS soutient l'autonomie",
      "La CNSA prévient, organise les soins et finance ; les directions "
      "du ministère n'interviennent pas"),
     0, 4,
     "C'est le triangle à retenir : DGS pour la santé de la population, "
     "DGOS pour l'organisation des soins, DSS pour le financement de la "
     "protection sociale. Aucune institution ne couvre seule le sujet.",
     ("III.4", "20")),

    ("Un camarade affirme : « C'est la HAS qui décide qu'un médicament "
     "sera remboursé. » Qu'en dit le cours ?",
     ("C'est faux : la HAS produit une évaluation scientifique qui éclaire "
      "une décision prise ensuite par d'autres",
      "C'est exact : la commission de la transparence de la HAS fixe le "
      "taux de remboursement",
      "C'est faux : c'est l'ANSM qui décide du remboursement en délivrant "
      "l'AMM",
      "C'est faux : le CEPS décide seul du remboursement en fixant le prix"),
     0, 4,
     "La HAS n'est qu'une brique d'expertise : l'ANSM ou l'Europe "
     "autorisent, la HAS évalue le service rendu, le CEPS négocie le "
     "prix, l'UNCAM fixe le taux, les pouvoirs publics décident et "
     "l'Assurance maladie rembourse. Expertise n'est pas décision "
     "politique.",
     ("VIII.1", "40")),

    ("L'affaire du Mediator a durablement changé la gouvernance du "
     "médicament. Quelle évolution le cours retient-il ?",
     ("L'ANSM succède à l'Afssaps en 2012, après la loi du 29 décembre "
      "2011 qui renforce la sécurité du médicament",
      "La HAS est créée en 2012 pour reprendre les missions de l'Afssaps",
      "Santé publique France naît de la fusion de l'Afssaps et de l'INPES",
      "L'Afssaps est rattachée à la CNAM pour contrôler les "
      "remboursements"),
     0, 4,
     "Le cours décrit la chaîne : incident, analyse des défaillances, "
     "changement des règles, changement des institutions, nouveaux "
     "contrôles. Le changement d'institution, ici, c'est l'ANSM qui "
     "remplace l'Afssaps.",
     ("IV.3", "24")),

    ("Santé publique France a été créée en 2016 par la fusion de trois "
     "organismes. Lequel n'en faisait **pas** partie ?",
     ("L'Afssaps",
      "L'Institut de veille sanitaire",
      "L'INPES",
      "L'EPRUS"),
     0, 4,
     "La fusion réunit l'Institut de veille sanitaire, l'INPES et "
     "l'EPRUS, pour rapprocher connaissance, surveillance, alerte, "
     "prévention et intervention. L'Afssaps, elle, est devenue l'ANSM.",
     ("IV.4", "25")),

    ("Les données du PMSI montrent qu'un service hospitalier a très peu "
     "d'activité. Quel est le rôle de l'ATIH dans la suite ?",
     ("Elle produit l'information ; d'autres acteurs, comme le ministère, "
      "l'ARS ou l'Assurance maladie, s'en servent pour décider",
      "Elle décide de fermer le service, puisqu'elle gère le PMSI",
      "Elle retire au service son autorisation d'activité",
      "Elle suspend le financement de l'établissement jusqu'à la "
      "prochaine LFSS"),
     0, 3,
     "L'ATIH recueille les données d'activité, gère le PMSI et produit "
     "des analyses médico-économiques. Elle ne décide pas qu'un hôpital "
     "doit fermer : produire l'information n'est pas décider.",
     ("IV.5 à IV.7", "26")),

    ("Pour des étudiants venus d'autres pays, quelle particularité "
     "française le cours souligne-t-il ?",
     ("Le payeur n'est pas une direction du ministère : c'est la sécurité "
      "sociale, héritage du modèle d'assurance sociale de 1945",
      "Le ministère de la Santé rembourse directement les assurés, par "
      "l'intermédiaire de la DSS",
      "Chaque ARS rembourse les assurés de sa région sur son propre budget",
      "Le Parlement fixe chaque année le montant remboursé à chaque assuré"),
     0, 3,
     "L'État définit les politiques, régule, organise, planifie et "
     "autorise ; la sécurité sociale finance, rembourse, négocie les "
     "conventions et régule une grande partie des soins de ville. Les "
     "deux travaillent ensemble sans se confondre.",
     ("V.1", "29")),

    ("Pourquoi une grande partie de la régulation des médecins, "
     "infirmiers, pharmaciens et kinésithérapeutes passe-t-elle par des "
     "conventions négociées ?",
     ("Parce qu'ils exercent en libéral : l'État ne peut pas leur donner "
      "d'instructions comme à ses fonctionnaires",
      "Parce que la loi interdit à l'État de fixer des règles pour les "
      "professions de santé",
      "Parce que l'ONDAM est voté par les représentants des professionnels",
      "Parce que les ARS n'ont aucune compétence sur les soins de ville"),
     0, 3,
     "Liberté professionnelle et financement collectif donnent la "
     "régulation conventionnelle : tarifs, rémunération, engagements, "
     "organisation, prévention se négocient avec l'Assurance maladie.",
     ("V.2", "30")),

    ("Dans le réseau de l'Assurance maladie, lequel de ces rôles revient "
     "à l'UNCAM ?",
     ("Les relations conventionnelles avec les professionnels et "
      "certaines décisions de remboursement",
      "La tête du réseau : orientations nationales, gestion du risque et "
      "données de santé",
      "Les relations locales avec les assurés : la partie la plus visible "
      "pour le patient",
      "La préparation de la LFSS et le suivi des comptes des branches"),
     0, 4,
     "L'UNCAM, Union nationale des caisses d'assurance maladie, porte les "
     "relations conventionnelles et certaines décisions sur les taux de "
     "remboursement. La tête du réseau est la CNAM, le niveau local la "
     "CPAM, et la LFSS est préparée par la DSS.",
     ("V.2", "30")),

    ("Un hôpital a les financements et les médecins pour ouvrir une "
     "activité soumise à autorisation. Que lui faut-il encore ?",
     ("L'autorisation du directeur général de l'ARS, au regard des besoins "
      "de la population et du projet régional de santé",
      "Un avis favorable de la CRSA, qui délivre les autorisations "
      "d'activité",
      "Une certification préalable de la HAS, qui vaut autorisation",
      "L'inscription de cette activité dans la LFSS de l'année"),
     0, 4,
     "« Nous avons l'argent et les médecins, donc nous ouvrons » ne suffit "
     "pas : l'ARS analyse le besoin régional et accorde ou refuse "
     "l'autorisation. La CRSA ne fait que donner des avis ; la HAS "
     "certifie la qualité une fois l'activité en place.",
     ("VIII.2", "41")),

    ("Une crise sanitaire déborde sur la sécurité, l'ordre public et la "
     "protection civile. Comment s'articulent l'ARS et le préfet ?",
     ("Leurs responsabilités sont complémentaires : l'ARS ne remplace pas "
      "le préfet",
      "L'ARS prend la direction de la sécurité et de la protection civile "
      "de la région",
      "Le préfet est dessaisi : toute crise sanitaire relève de la seule "
      "ARS",
      "Le Centre de crise sanitaire se substitue à l'ARS comme au préfet"),
     0, 4,
     "En crise, l'ARS assure veille, alerte et gestion de crise "
     "sanitaire, avec la DGS, Santé publique France, les établissements, "
     "les professionnels et le préfet. Dès que la crise dépasse le seul "
     "champ sanitaire, les deux responsabilités se complètent.",
     ("VI.5", "35")),

    ("« Viser l'égalité de résultat sans imposer une organisation "
     "strictement identique. » À quelle tension de la gouvernance cette "
     "réponse correspond-elle ?",
     ("Égalité ou différenciation territoriale",
      "Autonomie professionnelle ou régulation",
      "Besoins ou ressources",
      "Expertise ou décision politique"),
     0, 4,
     "On veut la même qualité de soins pour tous, mais les territoires "
     "diffèrent par leurs professionnels, leurs distances et leurs "
     "équipements. Ces tensions sont des arbitrages permanents, jamais "
     "des problèmes résolus.",
     ("X", "45")),
)


def _question(rang, question, choices, answer, level, explanation, partie):
    """Un QCM dont chaque mauvaise réponse renvoie au cours.

    La note d'une proposition fausse dit où relire, jamais quelle est la
    bonne : la bonne proposition, elle, garde l'explication complète.
    """
    renvoi = _revoir(partie)
    choices, answer = _tourner(choices, answer, rang)
    pattern = qcm_pattern(
        "ie3514_q%02d" % rang, rang, question, choices, answer, level,
        "%s Pour approfondir : %s." % (explanation, renvoi))
    label, options = pattern.blanks["choix"]
    options = [o if o.id == pattern.ref["choix"] else replace(
        o, note="Ce n'est pas la bonne réponse. À revoir : %s." % renvoi)
        for o in options]
    return replace(pattern, blanks={"choix": (label, options)},
                   lesson=(INTRO,))


PATTERNS = TROUS + tuple(
    _question(number + 1, *entree) for number, entree in enumerate(QUESTIONS)
)

MODULE = Module(
    key="ie3514_s3",
    title="IE3514 - Revision Sheet for Session 3",
    level=4,
    summary="La gouvernance du système de santé français, du niveau "
            "national aux territoires : six fonctions, Parlement et ONDAM, "
            "DGS, DGOS et DSS, agences, Assurance maladie, ARS, démocratie "
            "sanitaire. " + INTRO,
    keys=tuple(p.key for p in PATTERNS),
)
