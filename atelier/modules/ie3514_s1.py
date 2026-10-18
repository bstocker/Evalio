"""Module « IE3514 - Revision Sheet for Session 1 », du chapitre Révisions.

Des exercices de révision sur la première séance du cours IE.3514 —
Healthcare systems organization : ce qu'est la santé, la frontière entre
système de santé et système de soins, santé individuelle et santé des
populations, déterminants, continuum de santé et niveaux de prévention,
niveaux de soins, les six piliers de l'OMS et leurs interactions, les
quatre flux, les dimensions d'évaluation, et le caractère hybride du
système français.

Le cours est en anglais : les exercices le sont aussi, avec les termes
des diapositives, comme l'en-tête demandé par l'enseignant.

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
    "wrong answer, you will be directed to the relevant part of the "
    "course to review, so that you can improve your understanding of the "
    "course material."
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
    10: "What makes a health system “good”?",
    11: "A first feature of the French system",
}


def revoir(partie, detail=""):
    """Renvoi vers la partie du cours qui porte la réponse."""
    return "part %d of the course, “%s”%s" % (
        partie, PARTIES[partie], " — " + detail if detail else "")


def lecon(partie, detail=""):
    """Rappel d'une fiche à trous : l'intitulé, la lecture, le renvoi."""
    return (
        INTITULE,
        "For each blank, the **target** (“Motif à reproduire”) gives a "
        "property of the expected notion, without naming it. Choose the "
        "notion that has this property.",
        "If you get it wrong, review %s." % revoir(partie, detail),
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
    "primary prevention": "“How can we stop it from occurring?”",
    "secondary prevention": "“How can we detect it in time?”",
    "tertiary prevention": "“How can we limit its consequences?”",
    "health promotion": "“How can we create favourable conditions, "
                        "without targeting a specific disease?”",
}



# Les actions des quatre lignes, une variante par tirage. La lutte contre
# le tabac et l'activité physique sont écartées : le cours les range à la
# fois dans la promotion et dans la prévention primaire.
ACTIONS = (
    ("vaccination of infants",
     "prevention of household accidents",
     "distribution of condoms"),
    ("organised breast cancer screening",
     "organised colorectal cancer screening",
     "blood pressure measurement"),
    ("cardiac rehabilitation after a heart attack",
     "follow-up of established diabetes",
     "therapeutic education of a patient who is already ill"),
    ("health education at school",
     "improvement of the environment",
     "encouragement of a balanced diet"),
)

PREVENTION = Pattern(
    key="ie3514_s1_prevention",
    name="Levels of prevention",
    brief="Classify four actions carried out in a territory as health "
          "promotion, or as primary, secondary or tertiary prevention.",
    why="Each level answers its own question.",
    lesson=lecon(5, "slides 5.1 to 5.7 and the table of the three levels "
                    "of prevention"),
    dims=(("cas", 0, 2),),
    derive=_choisir(ACTIONS, ("action_a", "action_b", "action_c",
                              "action_d"), True),
    tpl="""Revision sheet: levels of prevention

Four actions carried out in the same territory:
  A. @action_a@
  B. @action_b@
  C. @action_c@
  D. @action_d@

Action A falls under @a@.
Action B falls under @b@.
Action C falls under @c@.
Action D falls under @d@.""",
    blanks={
        "a": ("Action A", _menu(QUESTION_PREVENTION)),
        "b": ("Action B", _menu(QUESTION_PREVENTION)),
        "c": ("Action C", _menu(QUESTION_PREVENTION)),
        "d": ("Action D", _menu(QUESTION_PREVENTION)),
    },
    ref={"a": "a", "b": "b", "c": "c", "d": "d"},
    rows=lambda p, get: ["%s. Question: %s" % (lettre.upper(), get(lettre)(p))
                         for lettre in "abcd"],
    level=4,
)


# Les niveaux de soins, et les soins de santé primaires, leur faux ami
# (partie 6). Chacun avec ce qui le caractérise.
TRAIT_NIVEAU = {
    "primary care": "first contact, continuity, coordination of the "
                    "pathway",
    "secondary care": "specialised level, generally reached after a "
                      "first contact",
    "tertiary care": "rare expertise, complex technical facilities, "
                     "concentrated skills",
    "Primary Health Care (PHC)": "a global approach to the health of a "
                                 "society, not a level of care",
}



# Deux parcours : celui du cours, et le même gradient en cardiologie.
PARCOURS = (
    ("a patient suffering from headaches sees their general practitioner",
     "a breathless patient sees her registered doctor"),
    ("a neurological condition is suspected: neurology consultation and "
     "imaging",
     "a heart disease is suspected: cardiology consultation"),
    ("a complex brain tumour is discovered: neurosurgery centre",
     "an operation is required: cardiac surgery"),
)

NIVEAUX = Pattern(
    key="ie3514_s1_niveaux",
    name="The referral gradient",
    brief="Place each step of a care pathway on the levels of care.",
    why="Each level is recognised by what it brings to the pathway.",
    lesson=lecon(6, "slides 6.1 to 6.3 and “A referral gradient”"),
    dims=(("cas", 0, 1),),
    derive=_choisir(PARCOURS, ("etape1", "etape2", "etape3")),
    tpl="""Revision sheet: a referral gradient

Step 1: @etape1@.
  This step falls under @n1@.
Step 2: @etape2@.
  This step falls under @n2@.
Step 3: @etape3@.
  This step falls under @n3@.""",
    blanks={
        "n1": ("Step 1", _menu(TRAIT_NIVEAU)),
        "n2": ("Step 2", _menu(TRAIT_NIVEAU)),
        "n3": ("Step 3", _menu(TRAIT_NIVEAU)),
    },
    ref={"n1": "a", "n2": "b", "n3": "c"},
    rows=lambda p, get: ["Step %d: %s" % (i, get("n%d" % i)(p))
                         for i in (1, 2, 3)],
    level=3,
)


# Les six piliers de l'OMS, chacun avec sa question (partie 7).
QUESTION_PILIER = {
    "governance": "“Who decides?”",
    "financing": "“Who pays, and how does the money flow?”",
    "human resources": "“Do we have the right skills in the right "
                       "place?”",
    "service delivery": "“Where and how is the service delivered?”",
    "medical products and technologies": "“With which physical and "
                                         "technological resources?”",
    "information systems": "“What information flows, produced by whom, "
                           "for whom?”",
}


PILIERS = Pattern(
    key="ie3514_s1_piliers",
    name="A territory without general practitioners",
    brief="Link each lever for action to one of the six WHO building "
          "blocks.",
    why="A difficulty affecting one building block may require "
        "transforming several.",
    lesson=lecon(8, "“A territory short of general practitioners”, with "
                    "the six building blocks of part 7"),
    tpl="""Revision sheet: a territory short of general practitioners

Spontaneous diagnosis: “It is only a staffing problem.”
Analysis through the six WHO building blocks reveals other levers:

  1. Payment methods influence where professionals
     choose to set up their practice.
     Building block: @l1@
  2. The authorities can create incentives.
     Building block: @l2@
  3. Teleconsultation can provide part of the answer.
     Building block: @l3@
  4. Data make it possible to identify the areas where
     needs are greatest.
     Building block: @l4@""",
    # Chaque menu écarte les piliers que le cours rattache aussi au levier :
    # la télémédecine apparaît sous la prestation de services, et la
    # réorganisation de l'offre sous la gouvernance.
    blanks={
        "l1": ("Lever 1", _menu(QUESTION_PILIER, (
            "financing", "governance", "human resources",
            "service delivery"))),
        "l2": ("Lever 2", _menu(QUESTION_PILIER, (
            "governance", "financing", "human resources",
            "information systems"))),
        "l3": ("Lever 3", _menu(QUESTION_PILIER, (
            "medical products and technologies", "information systems",
            "human resources", "governance"))),
        "l4": ("Lever 4", _menu(QUESTION_PILIER, (
            "information systems", "governance",
            "medical products and technologies", "financing"))),
    },
    ref={"l1": "a", "l2": "a", "l3": "a", "l4": "a"},
    rows=lambda p, get: ["Lever %d: %s" % (i, get("l%d" % i)(p))
                         for i in (1, 2, 3, 4)],
    level=4,
)


# Les sept dimensions d'évaluation, avec leur définition (partie 10).
DEFINITION_DIMENSION = {
    "health outcomes": "the effects produced on health: life expectancy, "
                       "avoidable mortality",
    "access": "the actual ability to obtain services: cost, distance, "
              "waiting times, availability",
    "quality and safety": "effective, evidence-based care, without "
                          "avoidable adverse events",
    "equity": "equal access for equal need, with no gap linked to income "
              "or social status",
    "efficiency": "the best possible result with the resources used",
    "sustainability": "the ability to finance and run the system over "
                      "time",
    "resilience": "the ability to keep functioning and to reorganise in "
                  "the face of a shock",
}


SITUATIONS = (
    ("for equal need, low-income households receive less care than "
     "others",
     "for equal need, residents with few qualifications receive poorer "
     "care"),
    ("hospitals keep treating patients during a cyberattack",
     "care continues despite a heatwave and a shortage in the supply of "
     "medicines"),
    ("the system works well today, but population ageing threatens its "
     "financing in ten years' time",
     "the rise in chronic diseases and the cost of innovation cast doubt "
     "on whether the system can be financed for long"),
    ("more is spent on prevention to save on hospital admissions, with "
     "better results",
     "the aim is the best possible result with the available means, not "
     "merely lower costs"),
    ("care that follows the guidelines nevertheless causes an avoidable "
     "adverse event",
     "an infection contracted in hospital could have been avoided"),
)

DIMENSIONS = Pattern(
    key="ie3514_s1_dimensions",
    name="Evaluating a health system",
    brief="Link each situation to the evaluation dimension it involves.",
    why="Evaluating a system means arbitrating between dimensions that are "
        "often in tension.",
    lesson=lecon(10, "“Seven dimensions for evaluating a health system” "
                     "and their details, 10.1 to 10.7"),
    dims=(("cas", 0, 1),),
    derive=_choisir(SITUATIONS, ("s1", "s2", "s3", "s4", "s5"), True),
    tpl="""Revision sheet: the evaluation dimensions

  1. @s1@.
     Dimension: @d1@
  2. @s2@.
     Dimension: @d2@
  3. @s3@.
     Dimension: @d3@
  4. @s4@.
     Dimension: @d4@
  5. @s5@.
     Dimension: @d5@""",
    # La situation d'équité ne propose pas l'accès : renoncer aux soins
    # faute de moyens est aussi un défaut d'accès financier.
    blanks={
        "d1": ("Situation 1", _menu(DEFINITION_DIMENSION, (
            "equity", "efficiency", "quality and safety",
            "health outcomes"))),
        "d2": ("Situation 2", _menu(DEFINITION_DIMENSION, (
            "resilience", "sustainability", "efficiency", "access"))),
        "d3": ("Situation 3", _menu(DEFINITION_DIMENSION, (
            "sustainability", "resilience", "efficiency", "equity"))),
        "d4": ("Situation 4", _menu(DEFINITION_DIMENSION, (
            "efficiency", "sustainability", "access", "quality and safety"))),
        "d5": ("Situation 5", _menu(DEFINITION_DIMENSION, (
            "quality and safety", "health outcomes", "access",
            "equity"))),
    },
    ref={"d1": "a", "d2": "a", "d3": "a", "d4": "a", "d5": "a"},
    rows=lambda p, get: ["%d. %s" % (i, get("d%d" % i)(p))
                         for i in (1, 2, 3, 4, 5)],
    level=4,
)


# Les étapes du continuum, chacune avec son but (partie 5).
BUT_ETAPE = {
    "PREVENT": "avoid onset",
    "DIAGNOSE": "identify the cause",
    "REHABILITATE": "restore abilities",
}

# Les deux bouts du continuum : l'effet, et ce qui l'accompagne.
BOUT = {
    "collective, diffuse and delayed":
        "schools, local authorities, employers; financing: prevention "
        "budgets, often modest",
    "individual, measurable and immediate":
        "health professionals and facilities; financing: health "
        "insurance, activity-based payment",
}



CONTINUUM = Pattern(
    key="ie3514_s1_continuum",
    name="The health continuum",
    brief="Complete the steps of the health continuum, then the effect of "
          "action at each of its ends.",
    why="The system accompanies a person throughout their life, not only "
        "during an acute episode.",
    lesson=lecon(5, "“The health continuum”"),
    tpl="""Revision sheet: the health continuum

PROMOTE → @e2@ → SCREEN → @e4@ → TREAT → @e6@ → SUPPORT

General population → person at risk → patient
                   → person with a disability or at the end of life

At the left end of the continuum, the effect of action is @gauche@.
At the right end of the continuum, the effect of action is @droite@.""",
    blanks={
        "e2": ("Step 2", _menu(BUT_ETAPE)),
        "e4": ("Step 4", _menu(BUT_ETAPE)),
        "e6": ("Step 6", _menu(BUT_ETAPE)),
        "gauche": ("Effect at the left end", _menu(BOUT)),
        "droite": ("Effect at the right end", _menu(BOUT)),
    },
    ref={"e2": "a", "e4": "b", "e6": "c", "gauche": "a", "droite": "b"},
    rows=lambda p, get: [
        "Step 2: %s" % get("e2")(p),
        "Step 4: %s" % get("e4")(p),
        "Step 6: %s" % get("e6")(p),
        "Left end, actors: %s" % get("gauche")(p),
        "Right end, actors: %s" % get("droite")(p),
    ],
    level=3,
)


# Maladie, vécu de la maladie, santé au sens large (partie 1.2), avec ce
# que chacune représente pour le système.
ROLE_NOTION = {
    "disease": "what information systems actually see",
    "illness": "what triggers the use of care",
    "health in the broad sense": "what the number of procedures alone "
                                 "cannot measure",
}

OBSERVATIONS = (
    ("a diagnosis code “type 2 diabetes” is entered in the patient's "
     "record",
     "hypertension is identified according to medical criteria, then "
     "coded"),
    ("a person feels ill and makes an appointment, although no "
     "examination reveals any pathology",
     "a patient describes their fatigue and anxiety: it is this feeling "
     "that leads them to see a doctor"),
    ("a person's autonomy, social relationships and perceived quality of "
     "life are taken into account",
     "a person's mental state, environment and perceived quality of life "
     "are taken into account"),
)

NOTIONS = Pattern(
    key="ie3514_s1_notions",
    name="Three notions not to be confused",
    brief="Recognise the notion at stake in each observation: disease, "
          "illness, or health in the broad sense.",
    why="The performance of a system is not measured by the number of "
        "procedures alone.",
    lesson=lecon(1, "slide 1.2 “Three notions not to be confused”"),
    dims=(("cas", 0, 1),),
    derive=_choisir(OBSERVATIONS, ("o1", "o2", "o3"), True),
    tpl="""Revision sheet: disease, illness, health

  1. @o1@.
     Notion: @n1@
  2. @o2@.
     Notion: @n2@
  3. @o3@.
     Notion: @n3@""",
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
    ("A person has no diagnosed disease, but lives in unsanitary housing, "
     "suffers from social isolation, sleeps very badly and shows "
     "significant psychological distress. According to the WHO "
     "definition, what can be concluded?",
     ("This person is not in good health: health is not merely the "
      "absence of disease",
      "This person is in good health, since no disease has been diagnosed",
      "Nothing can be concluded until a doctor has made a diagnosis",
      "This person is in good physical health, the only dimension the WHO "
      "considers"),
     0, 3,
     "The WHO defines health as a state of physical, mental and social "
     "well-being, and not merely the absence of disease or infirmity "
     "(Constitution adopted in 1946, in force since 1948). A diagnosis is "
     "not enough either to declare a person healthy or to declare them "
     "ill.",
     1),

    ("Thanks to prevention, a system avoids hospital admissions and "
     "therefore performs fewer procedures. What does the course say?",
     ("It can achieve better results: performance is not measured by the "
      "number of procedures",
      "Its performance falls, since its activity decreases",
      "It becomes less efficient, since its equipment is used less",
      "It can only be judged on its activity indicators, the only ones "
      "available"),
     0, 3,
     "Measuring activity (consultations, admissions, procedures, bed "
     "days) follows a volume logic: easy to count, but silent on the "
     "health achieved. Measuring outcomes (healthy life expectancy, "
     "avoidable mortality, complications avoided) follows a value logic. "
     "More procedures do not make a better system.",
     1),

    ("Which of these elements belongs to the health system, but **not** "
     "to the healthcare system?",
     ("The training of health professionals",
      "Rehabilitation services",
      "Laboratories and imaging",
      "Prevention delivered by a doctor"),
     0, 4,
     "The healthcare system brings together professionals, facilities "
     "and care functions — including medically delivered prevention and "
     "rehabilitation. It does not include financing, regulation, public "
     "health or the training of professionals, which belong to the "
     "health system.",
     2),

    ("What is the relationship between the healthcare system and the "
     "health system?",
     ("Inclusion: the healthcare system is one of the components of the "
      "health system",
      "Equivalence: the two expressions refer to the same whole",
      "Inclusion: the health system is one of the components of the "
      "healthcare system",
      "None: they are two separate wholes, care on one side, public "
      "health on the other"),
     0, 3,
     "It is a relationship of inclusion, not equivalence. At the core, "
     "the healthcare system; around it, prevention and public health; "
     "then financing, regulation, training and information.",
     2),

    ("The course distinguishes individual health, population health and "
     "public health. Which of these definitions is that of **public "
     "health**?",
     ("The organised action of society to improve health status: "
      "surveillance, prevention, protection, promotion, regulation",
      "The health status of a group, measured by aggregate indicators, "
      "and its distribution across subgroups",
      "The health status of a person and the care they receive",
      "All the care delivered by public hospitals"),
     0, 4,
     "Population health is a state: that of a group, measured by "
     "aggregate indicators. Public health is an action: the one society "
     "organises to improve that state.",
     3),

    ("A child with asthma has optimised treatment and regular respiratory "
     "follow-up, but the attacks persist. Which of these actions works on "
     "a determinant of the child's condition **outside** the family "
     "doctor's remit?",
     ("Treating the damp and mould in the home",
      "Strengthening the patient's therapeutic education",
      "Adjusting the drug treatment",
      "Scheduling respiratory follow-up visits more often"),
     0, 4,
     "The healthcare system optimises treatment, but the exposure "
     "remains: air pollution, damp and mould, smoking in the household, "
     "the family's social conditions. None of these levers belongs to the "
     "family doctor: cooperation is needed with housing, environment and "
     "education policies, and with local authorities.",
     4),

    ("According to the course, how do individual behaviours (diet, "
     "physical activity, risk behaviours) relate to the other families of "
     "determinants?",
     ("They are largely shaped by the social and economic environment and "
      "by the physical environment",
      "They are independent of them: they are purely a matter of "
      "individual choice",
      "They matter less than the use of the healthcare system, the main "
      "determinant of health",
      "They only come into play after a medical intervention"),
     0, 4,
     "Three families of determinants: the social and economic "
     "environment, the physical environment, individual characteristics "
     "and behaviours. Behaviours are themselves largely shaped by the "
     "first two families, and all of them act before any medical "
     "intervention.",
     4),

    ("According to the course, which of these statements is **not** a "
     "condition for relevant screening?",
     ("The disease must be rare, to limit the number of people to test",
      "The test must be reliable, acceptable and minimally invasive",
      "A treatment must exist that is more effective at an early stage",
      "A care pathway must be organised downstream"),
     0, 4,
     "Screening (secondary prevention) on the contrary requires a disease "
     "that is frequent enough and serious enough. Poorly designed, it "
     "produces false positives, unnecessary examinations and "
     "overdiagnosis.",
     5),

    ("What does the WHO emphasise about primary care and Primary Health "
     "Care (PHC)?",
     ("A country can have good primary care without having implemented "
      "a Primary Health Care policy",
      "The two expressions refer to the same first level of care",
      "Primary Health Care is a more specialised level of care than "
      "primary care",
      "A country that has implemented Primary Health Care no longer needs "
      "primary care"),
     0, 4,
     "Primary care is a level of care: first contact, continuity, "
     "coordination of individual care. Primary Health Care is a global "
     "approach, much broader: primary care, essential public health "
     "functions, action on determinants and community participation.",
     6),

    ("According to the course, protecting the population against the "
     "financial risk of illness is…",
     ("an objective of the system, carried by the financing building "
      "block",
      "a side effect of financing, without being one of its objectives",
      "a task for the governance building block alone",
      "outside the scope of the health system, a matter for private "
      "insurers"),
     0, 4,
     "The financing building block collects resources, pools them, "
     "allocates them among actors and protects the population against "
     "the financial risk of illness. The course insists: this is an "
     "objective of the system, not a side effect.",
     7),

    ("“The number of doctors trained today produces its effects in ten to "
     "twenty years.” Which property of the systems approach does this "
     "example illustrate?",
     ("Effects are delayed",
      "Effects spread from one building block to the others",
      "Unintended effects always exist",
      "The building blocks work independently of one another"),
     0, 4,
     "Three properties: effects spread (raising the price of a procedure "
     "changes supply, hence waiting times, hence the use of emergency "
     "departments), effects are delayed (by years, sometimes decades), "
     "and unintended effects always exist (a poorly calibrated volume "
     "indicator encourages unnecessary activity).",
     8),

    ("Country A spends much more on health than country B. What does the "
     "course conclude?",
     ("Nothing about its performance: spending is an input, never a "
      "performance indicator",
      "Country A has the better system, since it devotes more resources "
      "to it",
      "Country B is more efficient, since it spends less",
      "Country A necessarily offers better access to care"),
     0, 3,
     "Spending measures what is devoted to the system, never what it "
     "produces: it is a denominator. Two countries can spend the same "
     "amount on very different things, and an abundant but poorly "
     "distributed supply does not benefit the whole population.",
     10),

    ("Stocks, margins and redundancies: between which evaluation "
     "dimensions do they create a tension?",
     ("Efficiency and resilience: useless in normal times, essential in "
      "a crisis",
      "Equity and access: they benefit some at the expense of others",
      "Quality and safety: more stocks, less safe care",
      "Sustainability and health outcomes: they finance the future at the "
      "expense of the present"),
     0, 4,
     "This is the tension to remember: margins, stocks and redundancies "
     "are inefficient in normal times and essential in a crisis "
     "(pandemic, heatwave, supply shortage, cyberattack). Evaluating a "
     "system means arbitrating between dimensions, not maximising them "
     "all at once.",
     10),

    ("Why does the course describe the French system as a **hybrid** "
     "system?",
     ("Born of social insurance, it also has the features of a national "
      "system strongly steered by the State",
      "It combines conventional medicine and alternative medicine",
      "It is financed in equal shares by the State and by patients",
      "It is entirely private in community care and entirely public in "
      "hospitals"),
     0, 3,
     "Historically built on contributions, insurance funds and "
     "occupational groups, it also has the features of a national system "
     "steered by the State. The European Observatory on Health Systems and "
     "Policies notes universal coverage, a major role for mandatory health "
     "insurance, a large share of tax revenue, strong State intervention "
     "and a mix of public and private providers.",
     11),
)


def _build(rang, question, choices, answer, level, explanation, partie):
    choices, answer = _tourner(choices, answer, rang)
    pattern = qcm_pattern(
        "ie3514_s1_q%02d" % rang, rang, question, choices, answer, level,
        explanation)
    # `qcm_pattern` préfixe la bonne réponse d'un « Exact. » : on le
    # réécrit en anglais, avec le renvoi au cours. Les propositions
    # fausses restent sans commentaire, comme dans `qcm_pattern`.
    juste = "Correct. %s To go further, review %s." % (explanation,
                                                       revoir(partie))
    label, options = pattern.blanks["choix"]
    options = [replace(o, note=juste) if o.id == pattern.ref["choix"]
               else o for o in options]
    return replace(pattern, blanks={"choix": (label, options)}, lesson=(
        INTITULE,
        "If you get it wrong, review %s." % revoir(partie),
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
