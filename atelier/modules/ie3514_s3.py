"""Module « IE3514 - Revision Sheet for Session 3 », du chapitre Révisions.

Une fiche de révision sur la gouvernance du système de santé français, du
niveau national aux territoires : les six fonctions de la gouvernance, le
Parlement et l'ONDAM, les directions du ministère (DGS, DGOS, DSS), les
agences (HAS, ANSM, Santé publique France, CNSA, ATIH, ANS), l'Assurance
maladie, les ARS, la démocratie sanitaire et les trois cas d'étude. Le
cours est en anglais : les exercices le sont aussi.

Deux formes d'exercices :

- des **textes à trous** : chaque menu complète une phrase du cours. La
  sortie est une fiche de vérification, une ligne par trou : « consistent
  with the course », ou la partie et la diapositive à revoir. La cible ne
  dit donc rien de la réponse, seulement qu'il faut que tout soit conforme ;
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
INTRO = ("The following exercises are designed to help you make the most "
         "of your revision sessions. You answer the questions, and if you "
         "get a wrong answer, you will be directed to the relevant part of "
         "the course to review, so that you can improve your understanding "
         "of the course material.")


def _revoir(partie):
    """Renvoi vers le support : « Session 3, part IV.2, slide 23 »."""
    return "Session 3, part %s, slide %s" % partie


# --------------------------------------------------------------------------
# Textes à trous
# --------------------------------------------------------------------------

LECON_TROUS = (
    INTRO,
    "Each menu completes a sentence from the course. Only one proposal "
    "makes the sentence correct.",
    "The review sheet judges each blank separately: “consistent with the "
    "course”, or the part and slide of the course to review.",
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
        return ["Blank %d: %s" % (numero, "consistent with the course"
                                  if get(blank_id)(params)
                                  else "to review, " + renvoi)
                for numero, (blank_id, renvoi) in enumerate(renvois, 1)]

    return Pattern(key=key, name=name, brief=brief, why=why,
                   lesson=LECON_TROUS, tpl=tpl, blanks=blanks, ref=ref,
                   rows=rows, level=level)


FONCTIONS = _texte_a_trous(
    key="ie3514_fonctions",
    name="Governing is not providing care",
    brief="Complete the definition of the functions of governance.",
    why="Each actor performs a specific function, distinct from the "
        "production of care.",
    level=3,
    tpl="""Governance brings together six functions, distinct from the
production of care.

[1] @t1@: defining the rules that actors must follow.
    “What conditions must be met to perform cardiac surgery?”

[2] @t2@: allocating resources and structuring the supply of care.
    “How many specialised departments in a given territory?”

[3] The HAS, Santé publique France or the ATIH produce essential
    information; what they do not do is @t3@.

[4] The Assurance maladie (national health insurance) finances a large
    share of care; what it generally does not do itself is @t4@.""",
    trous=(
        ("t1", "Function [1]",
         ("Regulating", "Organising", "Deciding", "Financing"),
         ("I.2", "9")),
        ("t2", "Function [2]",
         ("Organising", "Regulating", "Evaluating and monitoring",
          "Deciding"),
         ("I.2", "9")),
        ("t3", "What expertise does not do [3]",
         ("decide in place of the public authorities",
          "evaluate medicines and health technologies",
          "monitor the health status of the population",
          "collect hospital activity data"),
         ("XII", "47")),
        ("t4", "What the payer does not do [4]",
         ("deliver care",
          "reimburse care",
          "negotiate agreements with health professionals",
          "regulate a large share of community care"),
         ("XII", "47")),
    ),
)

PARLEMENT = _texte_a_trous(
    key="ie3514_lfss_ondam",
    name="Parliament, the LFSS and the ONDAM",
    brief="Complete what Parliament votes on, and what the ONDAM is.",
    why="Parliament does not only vote on rules: it also sets the "
        "financial framework.",
    level=4,
    tpl="""[1] Since @t1@, Parliament has voted each year on the social
    security financing act (LFSS).

[2] This act is prepared by @t2@, which also monitors the revenue
    and expenditure of the branches.

[3] The ONDAM (national health insurance spending target) that it sets
    is @t3@: a patient who falls ill at the end of the year
    continues to receive care, even if a lot of care has already been
    consumed.

[4] Parliament therefore acts both as legislator and as
    @t4@.""",
    trous=(
        ("t1", "Year [1]",
         ("1996", "1945", "2004", "2010"),
         ("II.1", "13")),
        ("t2", "Who prepares the LFSS? [2]",
         ("the Social Security Directorate (DSS)",
          "the Directorate General for Healthcare Provision (DGOS)",
          "the National Health Insurance Fund (CNAM)",
          "the National Authority for Health (HAS)"),
         ("II.1", "13")),
        ("t3", "Nature of the ONDAM [3]",
         ("a spending target, a regulatory instrument",
          "a capped budget, like the appropriations of a government "
          "department",
          "an envelope negotiated each year between the CNAM and doctors",
          "a reimbursement ceiling set for each insured person"),
         ("II.2", "14")),
        ("t4", "Parliament's second role [4]",
         ("funder of the system",
          "care provider",
          "scientific expert authority",
          "regional steering body for the supply of care"),
         ("II.1", "13")),
    ),
)

DIRECTIONS = _texte_a_trous(
    key="ie3514_directions",
    name="DGS, DGOS or DSS?",
    brief="Assign each mission to the right directorate.",
    why="The directorates work on the same topics, but not at the same "
        "point in the chain.",
    level=3,
    tpl="""[1] For cancer, screening programmes fall under @t1@.

[2] The availability of oncologists and the authorisations for
    specialised activities fall under @t2@.

[3] The Health Crisis Centre, which prepares the system for health
    threats, is attached to @t3@.

[4] Supervision of the CNAV, the CNAF and the Urssaf Caisse nationale
    falls to @t4@.""",
    trous=(
        ("t1", "Directorate [1]",
         ("the DGS", "the DGOS", "the DSS", "the CNAM"),
         ("III.3", "19")),
        ("t2", "Directorate [2]",
         ("the DGOS", "the DGS", "the DSS", "the CNAM"),
         ("III.3", "19")),
        ("t3", "Directorate [3]",
         ("the DGS", "the DGOS", "the DSS", "the CNAM"),
         ("III.1", "17")),
        ("t4", "Directorate [4]",
         ("the DSS", "the DGS", "the DGOS", "the CNAM"),
         ("III.4", "20")),
    ),
)

MEDICAMENT = _texte_a_trous(
    key="ie3514_medicament",
    name="The journey of a reimbursed medicine",
    brief="Complete, step by step, the path of a medicine up to its "
          "reimbursement.",
    why="Seven steps, and almost as many actors: none of them decides "
        "alone.",
    level=4,
    tpl="""[1] Before it can be sold, a medicine receives a marketing
    authorisation (AMM), granted by @t1@ on the basis
    of its benefit/risk ratio.

[2] The Transparency Committee of @t2@ then evaluates its medical
    benefit and the improvement it brings.

[3] The price is negotiated with the manufacturer by @t3@.

[4] The reimbursement rate is set by @t4@; the final decision on
    coverage lies with the public authorities.

[5] Once the medicine is on the market, pharmacovigilance is the
    responsibility of @t5@.""",
    trous=(
        ("t1", "Who authorises? [1]",
         ("the ANSM or the European Union", "the HAS", "the CEPS",
          "the UNCAM"),
         ("VIII.1", "40")),
        ("t2", "Who evaluates the medical benefit? [2]",
         ("the HAS", "the ANSM", "the CEPS", "Santé publique France"),
         ("VIII.1", "40")),
        ("t3", "Who negotiates the price? [3]",
         ("the CEPS", "the UNCAM", "the HAS", "the DSS"),
         ("VIII.1", "40")),
        ("t4", "Who sets the rate? [4]",
         ("the UNCAM", "the CEPS", "the HAS", "the DSS"),
         ("VIII.1", "40")),
        ("t5", "Who monitors? [5]",
         ("the ANSM", "Santé publique France", "the HAS", "the ATIH"),
         ("IV.3", "24")),
    ),
)

ARS = _texte_a_trous(
    key="ie3514_ars",
    name="The ARS, regional steering body",
    brief="Complete what the ARS is founded on and what it has at its "
          "disposal.",
    why="The national level sets the framework; the ARS adapts it to its "
        "region.",
    level=4,
    tpl="""[1] To put an end to fragmentation, the regional health agencies
    (ARS) were created by @t1@, then set up
    in 2010.

[2] The regional health project comprises a long-term strategic
    orientation framework and @t2@, which sets
    the operational objectives.

[3] The ARS's flexible funding capacity, for prevention, the
    organisation of care and innovation, is called @t3@.

[4] Closest to the ground, the ARS concludes with local authorities
    @t4@.""",
    trous=(
        ("t1", "Founding text [1]",
         ("the HPST Act of 2009",
          "the Act of 29 December 2011",
          "the 1996 LFSS",
          "the 1945 ordinances"),
         ("VI.1", "32")),
        ("t2", "Second component of the regional project [2]",
         ("a regional health scheme",
          "a local health contract",
          "a national health strategy",
          "a regional intervention fund"),
         ("VI.3", "34")),
        ("t3", "Funding [3]",
         ("the FIR", "the ONDAM", "the PMSI", "the LFSS"),
         ("VI.4", "35")),
        ("t4", "Local agreements [4]",
         ("local health contracts (CLS)",
          "medical agreements (conventions)",
          "territorial health councils (CTS)",
          "authorisations for care activities"),
         ("VII.1", "37")),
    ),
)

DEMOCRATIE = _texte_a_trous(
    key="ie3514_democratie",
    name="Health democracy, level by level",
    brief="Place each body at its level, and identify the one that "
          "decides.",
    why="Never confuse a body that decides with an advisory body.",
    level=4,
    tpl="""[1] At national level, @t1@ is an advisory body attached to the
    minister.

[2] Alongside each ARS, @t2@ represents professionals,
    institutions, local authorities, associations and users, and issues
    opinions on regional policy.

[3] At territorial level, local consultation takes place through
    @t3@.

[4] These bodies consult, represent and give opinions; only
    @t4@ decides and steers, within the limits of its powers.""",
    trous=(
        ("t1", "National body [1]",
         ("the National Health Conference (CNS)",
          "the National Authority for Health (HAS)",
          "the National Health Insurance Fund (CNAM)",
          "Santé publique France"),
         ("VII.2", "38")),
        ("t2", "Regional body [2]",
         ("the CRSA", "the CTS", "the CNS", "the CLS"),
         ("VII.2", "38")),
        ("t3", "Territorial body [3]",
         ("the territorial health councils (CTS)",
          "the CRSA",
          "the CPAMs",
          "the GHTs"),
         ("VII.2", "38")),
        ("t4", "Who decides? [4]",
         ("the ARS", "the CRSA", "the CNS", "the CPAM"),
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
    ("The following question is asked: “What funding for community "
     "care?”. In the grid of the six functions of governance, which one "
     "does it belong to?",
     ("Financing: determining which activities are funded, at what level "
      "and under what rules",
      "Organising: allocating resources and structuring the supply of "
      "care",
      "Regulating: defining the rules that actors must follow",
      "Deciding: setting the major policy directions"),
     0, 3,
     "This is the course's own example for the “financing” function. "
     "“How many specialised departments in a given territory?” would "
     "belong to organising, and “Should prevention be developed?” to "
     "deciding.",
     ("I.2", "9")),

    ("At the end of November, health insurance spending already exceeds "
     "the ONDAM voted for the year. What happens to a patient who falls "
     "ill in December?",
     ("They are treated and covered: the ONDAM is a spending target, not "
      "a capped budget",
      "Their non-urgent care is postponed to the following year, for lack "
      "of funds",
      "Parliament must vote a new LFSS before any further reimbursement",
      "The ARS caps the number of reimbursed consultations per insured "
      "person"),
     0, 3,
     "The ONDAM is a spending trajectory set in advance, a regulatory "
     "instrument. Actual spending results from millions of decisions by "
     "patients, doctors and institutions; action is then taken on "
     "tariffs, prescriptions, organisation and appropriateness of care.",
     ("II.2", "14")),

    ("Which of these is **not** one of the three orientations of the "
     "draft national health strategy 2023-2033?",
     ("Guaranteeing every patient a registered doctor less than thirty "
      "minutes from home",
      "Living longer in good health",
      "Meeting health needs throughout the territory",
      "Improving the resilience of the system to crises and environmental "
      "challenges"),
     0, 4,
     "The three orientations are: living longer in good health, meeting "
     "needs throughout the territory, and making the system more "
     "resilient. The strategy, enshrined in the Public Health Code, sets "
     "a multi-year framework; the regional and local levels translate it "
     "into action.",
     ("II.3", "15")),

    ("On ageing, what division of roles does the course set out?",
     ("The DGS prevents, the DGOS organises care, the DSS finances, the "
      "CNSA supports autonomy",
      "The DGOS prevents, the DGS organises care, the DSS finances, the "
      "CNSA supports autonomy",
      "The DGS prevents, the DSS organises care, the CNSA finances, the "
      "DGOS supports autonomy",
      "The CNSA prevents, organises care and finances; the ministry's "
      "directorates are not involved"),
     0, 4,
     "This is the triangle to remember: DGS for population health, DGOS "
     "for the organisation of care, DSS for the financing of social "
     "protection. No single institution covers the issue on its own.",
     ("III.4", "20")),

    ("A classmate claims: “It is the HAS that decides whether a medicine "
     "will be reimbursed.” What does the course say?",
     ("That is wrong: the HAS produces a scientific evaluation that "
      "informs a decision taken afterwards by others",
      "That is right: the HAS Transparency Committee sets the "
      "reimbursement rate",
      "That is wrong: the ANSM decides on reimbursement by granting the "
      "marketing authorisation (AMM)",
      "That is wrong: the CEPS alone decides on reimbursement by setting "
      "the price"),
     0, 4,
     "The HAS is only one building block of expertise: the ANSM or the "
     "EU authorises, the HAS evaluates the medical benefit, the CEPS "
     "negotiates the price, the UNCAM sets the rate, the public "
     "authorities decide and the Assurance maladie reimburses. Expertise "
     "is not a political decision.",
     ("VIII.1", "40")),

    ("The Mediator affair (a drug safety scandal) had a lasting impact on "
     "the governance of medicines. Which change does the course "
     "highlight?",
     ("The ANSM succeeded the Afssaps in 2012, after the Act of "
      "29 December 2011 strengthening drug safety",
      "The HAS was created in 2012 to take over the missions of the "
      "Afssaps",
      "Santé publique France was born from the merger of the Afssaps and "
      "the INPES",
      "The Afssaps was attached to the CNAM to control reimbursements"),
     0, 4,
     "The course describes the chain: incident, analysis of failures, "
     "change of rules, change of institutions, new controls. The change "
     "of institution here is the ANSM replacing the Afssaps.",
     ("IV.3", "24")),

    ("Santé publique France was created in 2016 by merging three bodies. "
     "Which one was **not** among them?",
     ("The Afssaps",
      "The Institut de veille sanitaire (health surveillance institute)",
      "The INPES",
      "The EPRUS"),
     0, 4,
     "The merger brought together the Institut de veille sanitaire, the "
     "INPES and the EPRUS, to bring knowledge, surveillance, alert, "
     "prevention and intervention closer together. The Afssaps, for its "
     "part, became the ANSM.",
     ("IV.4", "25")),

    ("PMSI data show that a hospital department has very little "
     "activity. What is the role of the ATIH in what follows?",
     ("It produces the information; other actors, such as the ministry, "
      "the ARS or the Assurance maladie, use it to decide",
      "It decides to close the department, since it manages the PMSI",
      "It withdraws the department's activity authorisation",
      "It suspends the institution's funding until the next LFSS"),
     0, 3,
     "The ATIH collects activity data, manages the PMSI and produces "
     "medico-economic analyses. It does not decide that a hospital must "
     "close: producing information is not deciding.",
     ("IV.5 to IV.7", "26")),

    ("For students from other countries, which French specificity does "
     "the course emphasise?",
     ("The payer is not a ministry directorate: it is social security, "
      "a legacy of the 1945 social insurance model",
      "The Ministry of Health reimburses insured persons directly, "
      "through the DSS",
      "Each ARS reimburses the insured persons of its region from its own "
      "budget",
      "Parliament sets each year the amount reimbursed to each insured "
      "person"),
     0, 3,
     "The State defines policies, regulates, organises, plans and "
     "authorises; social security finances, reimburses, negotiates "
     "agreements and regulates a large share of community care. The two "
     "work together without merging.",
     ("V.1", "29")),

    ("Why does a large part of the regulation of doctors, nurses, "
     "pharmacists and physiotherapists go through negotiated agreements?",
     ("Because they are self-employed: the State cannot give them "
      "instructions as it does to its civil servants",
      "Because the law forbids the State from setting rules for the "
      "health professions",
      "Because the ONDAM is voted by the professionals' representatives",
      "Because the ARS have no powers over community care"),
     0, 3,
     "Professional freedom plus collective funding gives conventional "
     "regulation: tariffs, remuneration, commitments, organisation and "
     "prevention are negotiated with the Assurance maladie.",
     ("V.2", "30")),

    ("In the Assurance maladie network, which of these roles belongs to "
     "the UNCAM?",
     ("Conventional relations with health professionals and certain "
      "reimbursement decisions",
      "Heading the network: national orientations, risk management and "
      "health data",
      "Local relations with insured persons: the part most visible to "
      "the patient",
      "Preparing the LFSS and monitoring the accounts of the branches"),
     0, 4,
     "The UNCAM, the National Union of Health Insurance Funds, handles "
     "conventional relations and certain decisions on reimbursement "
     "rates. The head of the network is the CNAM, the local level is the "
     "CPAM, and the LFSS is prepared by the DSS.",
     ("V.2", "30")),

    ("A hospital has the funding and the doctors to open an activity "
     "that requires authorisation. What else does it need?",
     ("Authorisation from the director general of the ARS, in light of "
      "the population's needs and the regional health project",
      "A favourable opinion from the CRSA, which grants activity "
      "authorisations",
      "Prior certification by the HAS, which serves as authorisation",
      "The inclusion of this activity in that year's LFSS"),
     0, 4,
     "“We have the money and the doctors, so we open” is not enough: the "
     "ARS analyses regional need and grants or refuses the "
     "authorisation. The CRSA only gives opinions; the HAS certifies "
     "quality once the activity is up and running.",
     ("VIII.2", "41")),

    ("A health crisis spills over into security, public order and civil "
     "protection. How do the ARS and the prefect work together?",
     ("Their responsibilities are complementary: the ARS does not "
      "replace the prefect",
      "The ARS takes charge of security and civil protection in the "
      "region",
      "The prefect is relieved of responsibility: any health crisis falls "
      "to the ARS alone",
      "The Health Crisis Centre takes the place of both the ARS and the "
      "prefect"),
     0, 4,
     "In a crisis, the ARS ensures health surveillance, alert and health "
     "crisis management, together with the DGS, Santé publique France, "
     "institutions, professionals and the prefect. As soon as the crisis "
     "goes beyond the health field alone, the two responsibilities "
     "complement each other.",
     ("VI.5", "35")),

    ("“Aim for equal outcomes without imposing a strictly identical "
     "organisation.” Which tension of governance does this answer "
     "address?",
     ("Equality or territorial differentiation",
      "Professional autonomy or regulation",
      "Needs or resources",
      "Expertise or political decision"),
     0, 4,
     "We want the same quality of care for everyone, but territories "
     "differ in their professionals, distances and facilities. These "
     "tensions are permanent trade-offs, never solved problems.",
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
        explanation)
    # Les retours sont réécrits en anglais, la langue du cours (le moteur
    # écrit « Exact. »), comme dans ie3514_s4.
    juste = "Correct. %s To go further: %s." % (explanation, renvoi)
    faux = "That is not the right answer. Review: %s." % renvoi
    label, options = pattern.blanks["choix"]
    options = [replace(o, note=juste if o.id == pattern.ref["choix"]
                       else faux)
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
    summary="The governance of the French health system, from the national "
            "level to the territories: six functions, Parliament and the "
            "ONDAM, DGS, DGOS and DSS, agencies, Assurance maladie, ARS, "
            "health democracy. " + INTRO,
    keys=tuple(p.key for p in PATTERNS),
)
