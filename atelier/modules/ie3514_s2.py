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

from ..engine import Module, Option, Pattern, one_line_per_blank, qcm_pattern
from .qcm_docker import _tourner

# Intitulé demandé par l'enseignant, en tête de chaque exercice : l'élève
# peut tomber sur n'importe lequel en premier.
INTITULE = ("The following exercises are designed to help you make the most "
            "of your revision sessions. You answer the questions, and if you "
            "get a wrong answer, you will be directed to the relevant part of "
            "the course to review, so that you can improve your understanding "
            "of the course material.")

# Lecture d'une fiche à trous, rappelée sur chacune.
FICHE = ("The sheet pairs each **problem raised** with the response the "
         "system gave to it. For each line, the output to reproduce gives "
         "the **year**, the **nature** of that response and the **part of "
         "the course** that covers it: if you make a mistake, compare the "
         "lines to find out which part to review.")

# Parties du cours de la séance 2, telles que les numérotent les
# diapositives.
PARTIES = {
    "I": "Before 1945: from social assistance to social insurance",
    "II": "1944-1946: the founding moment",
    "III": "1958-1975: building the hospital system",
    "IV": "1980-1996: the great question of regulation",
    "V": "1999-2016: universal coverage, patients' rights and care pathways",
    "VI": "2018-2020: from structures to care pathways",
    "VII": "What history helps us understand (the ten principles)",
}

# Les réponses que l'histoire a apportées : clé -> (texte du menu, année,
# nature, partie du cours). La nature reste courte et distincte d'une
# entrée à l'autre : deux réponses de la même année et de la même partie
# (LFSS, ONDAM, ARH) ne doivent pas produire la même ligne.
FAITS = {
    "assistance": ("free medical assistance (assistance médicale gratuite)",
                   "1893", "aid for sick people without resources", "I.3"),
    "accidents": ("the law on industrial accidents", "1898",
                  "occupational risk pooled", "I.4"),
    "retraites": ("the law on workers' and farmers' pensions", "1910",
                  "first cross-industry pension scheme", "I.6"),
    "assurances": ("the social insurance laws (assurances sociales)",
                   "1928-1930",
                   "compulsory insurance for some employees", "I.7"),
    "famille": ("family allowances", "1932",
                "compulsory scheme funded by employers", "I.8"),
    "cnr": ("the CNR programme (National Council of the Resistance)",
            "1944", "social security plan announced", "II.1"),
    "ordonnances": ("the ordonnances of October 1945", "1945",
                    "creation of the Sécurité sociale", "II.4"),
    "preambule": ("the Preamble to the 1946 Constitution", "1946",
                  "health guaranteed by the Nation", "II.7"),
    "chu": ("the CHU, university hospitals (Debré reform)", "1958",
            "care + teaching + research", "III.2"),
    "branches": ("the branches of the Sécurité sociale", "1967",
                 "financial separation of the major risks", "III.3"),
    "carte": ("the carte sanitaire (health map)", "1970",
              "equipment needs based on population", "III.4"),
    "convention": ("the national medical agreement (convention médicale)",
                   "1971",
                   "fees negotiated with self-employed doctors", "III.5"),
    "medicosocial": ("the law on the social and medico-social sector",
                     "1975", "older people, disability, support", "III.6"),
    "prix_journee": ("the daily rate (prix de journée)", "before 1983",
                     "payment based on length of stay", "IV.2"),
    "budget_global": ("the global budget (budget global)", "1983-1984",
                      "annual envelope per facility", "IV.2"),
    "csg": ("the CSG (general social contribution)", "1990",
            "levy on all forms of income", "IV.3"),
    "sros": ("the SROS (regional health organisation plans)", "1991",
             "regional planning by activity", "IV.4"),
    "lfss": ("the LFSS (Social Security Financing Act)", "1996",
             "annual vote by Parliament", "IV.5"),
    "ondam": ("the ONDAM (national health insurance spending target)",
              "1996", "spending path set in advance", "IV.5"),
    "arh": ("the ARH (regional hospital agencies)", "1996",
            "regional steering of hospital provision", "IV.5"),
    "cmu": ("the CMU (universal health coverage)", "1999",
            "coverage for residents without compulsory cover", "V.1"),
    "droits": ("the law on patients' rights", "2002",
               "information, dignity, participation", "V.2"),
    "traitant": ("the registered doctor (médecin traitant)", "2004",
                 "coordinated care pathway", "V.3"),
    "t2a": ("the T2A (activity-based payment)", "2004",
            "funding based on activity performed", "V.4"),
    "ars": ("the ARS, regional health agencies (HPST law)", "2009-2010",
            "single regional health authority", "V.5"),
    "puma": ("the PUMa (universal health protection)", "2016",
             "personal right: work or stable residence", "V.6"),
    "ght": ("the GHT (regional hospital groups)", "2016",
            "shared, graduated care strategy", "V.7"),
    "ma_sante": ("Ma Santé 2022 (My Health 2022)", "2018",
                 "from structures to care pathways", "VI.1"),
    "segur": ("the Ségur de la santé", "2020",
              "pay rises, investment, digital health", "VI.3"),
}

BLANKS = "abcd"


def _ligne(fait):
    """Ce que produit une réponse : son année, sa nature, sa partie."""
    _menu, annee, nature, partie = FAITS[fait]
    return "%s · %s — course: part %s" % (annee, nature, partie)


def _lecon(parties):
    return (INTITULE,
            "Where to look in the course: " + "; ".join(
                "**Session 2, part %s** — %s" % (p, PARTIES[p])
                for p in parties) + ".",
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
        blanks[blank] = ("Response to problem %d" % (rang + 1), [
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
        tpl="Problem raised\n   → response given\n\n" + "\n\n".join(tpl),
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
        "rev_avant_1945", "Before 1945: the first building blocks",
        "Find the law that responded to each of the problems of the late "
        "19th century and the interwar period.",
        "Protection shifts from a logic of assistance to a logic of "
        "insurance.",
        ("I",),
        (("Helping sick people who cannot pay, subject to a means test",
          "assistance", "accidents", "assurances", "famille"),
         ("Compensating injured workers without them having to prove the "
          "employer was at fault", "accidents", "assistance", "retraites",
          "assurances"),
         ("Covering employees in industry and commerce against sickness, "
          "maternity, disability, old age and death",
          "assurances", "retraites", "famille", "ordonnances"),
         ("Bringing family policy into social protection",
          "famille", "assurances", "retraites", "medicosocial")),
        level=3,
    ),
    fiche(
        "rev_fondation", "1944-1946: three founding texts",
        "Find the text behind each of the decisions of the founding "
        "moment.",
        "The CNR sets the ambition, 1945 creates the institutions, 1946 "
        "makes it a right.",
        ("II",),
        (("Guaranteeing citizens the means of existence when they can no "
          "longer work", "cnr", "ordonnances", "preambule", "assurances"),
         ("Creating the social security bodies, funded by contributions "
          "and run with the social partners",
          "ordonnances", "cnr", "preambule", "branches"),
         ("Giving a legal basis to any later extension of coverage",
          "preambule", "cnr", "ordonnances", "droits")),
        level=3,
    ),
    fiche(
        "rev_hopital", "1958-1975: the modern hospital and its neighbours",
        "Find the reform that responded to each of the problems raised by "
        "a medicine that had become technical, specialised and costly.",
        "Each reform from 1958 to 1975 responds to the changing nature of "
        "medicine.",
        ("III",),
        (("Training professionals and doing research within the hospital "
          "itself", "chu", "carte", "convention", "branches"),
         ("Being able to discuss the sickness deficit separately from old "
          "age and family", "branches", "chu", "budget_global", "lfss"),
         ("Deciding which equipment to install, where, and for which "
          "population", "carte", "sros", "chu", "ght"),
         ("Reconciling freedom to set up practice with socialised funding "
          "of medical acts", "convention", "traitant", "carte",
          "medicosocial")),
        level=3,
    ),
    fiche(
        "rev_financer_hopital", "Funding hospitals: forty years of "
        "reforms",
        "Find the funding method or reform that responded to each of the "
        "problems of hospital funding.",
        "Each funding method corrects the perverse effect of the previous "
        "one, and creates its own.",
        ("IV", "V", "VI"),
        (("Starting point: funding the facility in proportion to the "
          "length of stays", "prix_journee", "budget_global", "t2a",
          "ondam"),
         ("Stays get longer: the longer the patient stays, the more the "
          "facility bills", "budget_global", "prix_journee", "t2a",
          "ondam"),
         ("With an annual envelope, resources freeze and actual activity "
          "barely counts", "t2a", "budget_global", "prix_journee",
          "ondam"),
         ("Activity-based funding drives volume: a move away from it is "
          "announced", "segur", "ma_sante", "t2a", "ght")),
        level=4,
    ),
    fiche(
        "rev_regulation", "1990-1996: funding and regulating",
        "Find the instrument that responded to each of the funding and "
        "steering problems from 1990 to 1996.",
        "How can a solidarity-based system be maintained while keeping "
        "spending growth under control?",
        ("IV",),
        (("Making income other than earnings from work contribute",
          "csg", "lfss", "ondam", "sros"),
         ("Giving Parliament an annual vote on the main financial "
          "orientations of the Sécurité sociale", "lfss", "ondam", "csg",
          "arh"),
         ("No longer simply recording spending after the fact", "ondam",
          "lfss", "budget_global", "csg"),
         ("Bringing the State and health insurance together to steer "
          "public and private hospital provision at regional level", "arh",
          "ars", "sros", "ght")),
        level=4,
    ),
    fiche(
        "rev_universalisation", "1999-2016: universal right, pathways, "
        "territories",
        "Find the reform that responded to each of the problems of the "
        "1999-2016 period.",
        "Coverage becomes detached from employment; the care pathway "
        "replaces the isolated medical act.",
        ("V",),
        (("Covering legal residents left outside the compulsory schemes",
          "cmu", "puma", "ordonnances", "droits"),
         ("Covering every adult in their own name, without dependant "
          "(ayant droit) status", "puma", "cmu", "droits", "ordonnances"),
         ("Replacing a series of unconnected medical acts with care "
          "organised around the patient", "traitant", "t2a", "ght",
          "convention"),
         ("Bringing public health, prevention, care and the medico-social "
          "sector under a single regional authority", "ars", "arh", "sros",
          "ght")),
        level=4,
    ),
    fiche(
        "rev_principes", "The principles and their dated decisions",
        "Find the dated decision to which each of the principles of the "
        "French system is linked.",
        "Each principle is linked to a dated decision: that link is what "
        "the exam expects.",
        ("VII",),
        (("Principle 1, solidarity: its central legacy",
          "ordonnances", "cnr", "preambule", "assurances"),
         ("Principle 2, universal coverage: the culmination of the right",
          "puma", "cmu", "ordonnances", "preambule"),
         ("Principle 4, professional freedom but collective regulation: "
          "its anchor", "convention", "traitant", "medicosocial",
          "budget_global"),
         ("Principle 7, territorialisation: its first instrument",
          "carte", "sros", "ars", "ght")),
        level=4,
    ),
    fiche(
        "rev_aujourdhui", "From the patient as actor to the Ségur",
        "Find the reform that responded to each of the problems of the "
        "recent period.",
        "The system seeks to organise itself around the patient and their "
        "care pathway.",
        ("V", "VI"),
        (("The patient is no longer the object of care but an actor who "
          "holds rights", "droits", "preambule", "traitant", "cmu"),
         ("A system too compartmentalised and too focused on medical acts "
          "in the face of ageing and chronic diseases", "ma_sante", "segur",
          "ars", "t2a"),
         ("After the Covid-19 crisis: making health professions attractive "
          "and investing in digital health", "segur", "ma_sante", "ght",
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
    ("What distinguishes the logic of **insurance** from the logic of "
     "**assistance**?",
     ("Access depends on affiliation, not on resources",
      "Access depends on a means test",
      "Funding relies mainly on the community as a whole",
      "Aid goes first to the person who cannot pay"),
     0, 3,
     "Insurance follows the chain contribution → pooling → benefit: it is "
     "affiliation that opens the right. The other three options describe "
     "assistance (need → aid).",
     "I.2"),

    ("A common exam mistake: what exactly do the ordonnances of 4 and 19 "
     "October 1945 do?",
     ("They create the Sécurité sociale and extend protection widely, "
      "without unifying it: the special schemes remain",
      "They unify all social protection into a single scheme",
      "They base coverage on residence and taxation, as in the Beveridge "
      "model",
      "They create separate national funds for sickness, old age and "
      "family"),
     0, 4,
     "The ambition was broad, but several professions wanted to keep their "
     "own scheme: 1945 generalises without unifying. The national funds "
     "per branch date from the ordonnances of 1967.",
     "II.4-II.5"),

    ("Which of these features of the French system has **remained "
     "Bismarckian**?",
     ("The role of the social partners",
      "A substantial share of funding through taxation",
      "Strong regulation by the State",
      "Coverage based on residence"),
     0, 3,
     "What remains Bismarckian is compulsory health insurance, "
     "contributions, the role of the social partners and the insurance "
     "logic. The other three features have become Beveridgean.",
     "VII (focus on principle 3)"),

    ("Why is the creation of the CSG in 1990 the clearest shift towards "
     "the Beveridge model?",
     ("It is levied on a broad range of income: universal coverage calls "
      "for universal funding",
      "It replaces the health insurance funds with a national health "
      "service",
      "It sets a national health insurance spending target every year",
      "It abolishes contributions based on wages"),
     0, 4,
     "The CSG moves from contributions on earnings to a levy on all "
     "income: it is a **partial** shift of funding to taxation. "
     "Contributions remain, and the spending target is the ONDAM of 1996.",
     "IV.3"),

    ("What perverse effect is the hospitals' **global budget** "
     "(1983-1984) criticised for?",
     ("Resources freeze and actual activity is barely taken into account",
      "The longer the patient stays, the more days the facility bills",
      "It encourages volume and raises the question of whether medical "
      "acts are appropriate",
      "It leaves hospital spending with no ceiling at all"),
     0, 3,
     "The annual envelope controls spending but ignores activity. Longer "
     "stays are the perverse effect of the daily rate; the incentive to "
     "volume is that of the T2A of 2004.",
     "IV.2"),

    ("What does the ONDAM, created by the Juppé plan, change in the logic "
     "of health insurance spending?",
     ("Spending is no longer recorded after the fact: a national path is "
      "defined in advance",
      "Parliament votes every year on the main financial orientations of "
      "the Sécurité sociale",
      "The State and health insurance jointly steer regional hospital "
      "provision",
      "Each facility receives an annual envelope to operate"),
     0, 4,
     "The ONDAM is a target set in advance. The annual vote is that of the "
     "LFSS, regional steering that of the ARH, the envelope per facility "
     "the global budget of 1983-1984.",
     "IV.5"),

    ("Which sentence sums up the change in the basis of the right brought "
     "about by the CMU (1999) and then the PUMa (2016)?",
     ("“I am covered because I belong durably to the national community "
      "of residence.”",
      "“I am covered because I have a job.”",
      "“I am covered because I have no resources.”",
      "“I am covered because my employer pays contributions for me.”"),
     0, 3,
     "The right no longer rests on employment: the PUMa ties it to work "
     "**or** to stable and legal residence, which moves France away from "
     "the pure Bismarckian model.",
     "V.1 and V.6"),

    ("According to the course, what lesson about resilience did the "
     "Covid-19 crisis bring home?",
     ("Margins and redundancies that seemed inefficient in normal times "
      "proved decisive",
      "The T2A made it possible to absorb the influx of patients without "
      "additional resources",
      "Concentrating all equipment in the CHU was enough to cope",
      "The separation between community care, hospital and the "
      "medico-social sector protected the system"),
     0, 4,
     "The crisis showed the mobilisation of professionals and the capacity "
     "to adapt, but also weaknesses: staffing, pressure on hospitals, "
     "coordination, information systems. The margins judged inefficient "
     "made the difference.",
     "VI.2"),

    ("Why is a CHU not simply “a very large hospital”?",
     ("It combines care, teaching and research, organised jointly with "
      "the universities' medical faculties",
      "It is the only facility authorised to take emergencies",
      "It is funded directly by the State, outside health insurance",
      "It brings together all the public hospitals of a territory"),
     0, 3,
     "The ordonnance of 30 December 1958 (Debré reform) creates the CHU: "
     "care + teaching + research, with joint hospital-university posts. "
     "Grouping hospitals by territory is the GHT of 2016.",
     "III.2"),

    ("Which difficulty, inherited from the 1975 law, is Ma Santé 2022 "
     "still trying to solve in 2018?",
     ("Three worlds organised separately: community care, hospital and "
      "the medico-social sector",
      "The lack of coverage for residents without a job",
      "Paying hospitals by the daily rate",
      "The absence of any planning of hospital equipment"),
     0, 4,
     "Different funders, supervisory authorities and cultures: "
     "coordinating these three worlds is the major issue of the following "
     "decades. The other three problems had already been answered: the "
     "carte sanitaire in 1970, the global budget in 1983-1984, the CMU in "
     "1999.",
     "III.6 and VI.1"),

    ("What do principles 8 (freedom and regulation) and 9 (quality and "
     "sustainability) say about the French system?",
     ("They are trade-offs, never solutions: they are played out again "
      "with every reform",
      "They are achievements of 1945 that have never been called into "
      "question",
      "They were settled once and for all by the Juppé plan",
      "They concern only public hospitals"),
     0, 4,
     "What has never been called into question since 1945 is solidarity, "
     "pooling and compulsory insurance. Principles 8 and 9, by contrast, "
     "are permanent tensions.",
     "VII (principles 7 to 10)"),

    ("Through which channel does the Bismarckian model directly feed "
     "French thinking in the 1920s?",
     ("Alsace-Moselle, returned to France after the First World War, had "
      "known the German social insurance system",
      "The Beveridge report, which France adopts as soon as it is "
      "published",
      "The programme of the National Council of the Resistance (CNR)",
      "The ordonnances drafted under the direction of Pierre Laroque"),
     0, 4,
     "Bismarck's Germany builds the first major social insurance system "
     "between 1881 and 1889; the experience of Alsace-Moselle feeds French "
     "thinking from the 1920s. The Beveridge report dates from 1942, the "
     "CNR from 1944, the ordonnances from 1945.",
     "I.5"),
)


def _question(rang, question, choices, answer, level, explanation, partie):
    choices, answer = _tourner(choices, answer, rang)
    explanation = "%s Review: part %s of the course." % (explanation, partie)
    pattern = qcm_pattern("rev_qcm_%02d" % rang, rang, question, choices,
                          answer, level, explanation)
    # « III.6 and VI.1 » -> parties III et VI, pour le rappel en tête.
    racines = []
    for racine in re.findall(r"\b([IVX]+)\b", partie):
        if racine not in racines:
            racines.append(racine)
    return replace(pattern, lesson=_lecon(racines)[:2])


PATTERNS = one_line_per_blank(
    FICHES + tuple(
        _question(number + 1, *entree)
        for number, entree in enumerate(QUESTIONS)
    )
)

MODULE = Module(
    key="ie3514_s2",
    title="IE3514 - Revision Sheet for Session 2",
    level=4,
    summary="The historical construction of the French health system, "
            "from free medical assistance in 1893 to the Ségur of 2020: "
            "challenging fill-in sheets and multiple-choice questions, each "
            "pointing to the part of the course to review.",
    keys=tuple(p.key for p in PATTERNS),
)
