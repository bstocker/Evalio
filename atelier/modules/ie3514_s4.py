"""Module « IE3514 - Revision Sheet for Session 4 », du chapitre Révisions.

Une fiche de révision du cours IE.3514 (Healthcare systems organization),
séance 4 : soins primaires et de premier recours, médecin traitant et
parcours coordonné, professionnels de proximité, MSP et CPTS, soins non
programmés, déserts médicaux, télésanté. Le cours est en anglais : les
exercices le sont aussi, comme l'en-tête demandé par l'enseignant.

Deux formes, toutes deux de niveau difficile à très difficile :

- des questions à choix unique ;
- des textes à trous, en mode « compléter » : chaque trou a son menu, et
  la sortie donne un verdict par trou. Un trou faux renvoie à la partie
  du cours qui contient la réponse, sans dire laquelle des propositions
  était la bonne.

Les questions aussi renvoient au cours : la partie à relire est rappelée
en tête, et une réponse fausse indique les sections précises à revoir.
L'explication complète n'accompagne que la bonne réponse (cf.
`qcm_pattern`) : la livrer sur un choix faux reviendrait à la donner.
"""

from dataclasses import replace

from ..engine import Module, Option, Pattern, one_line_per_blank, qcm_pattern
from .qcm_docker import _tourner

# En-tête demandé par l'enseignant, en tête de chaque exercice.
INTITULE = (
    "The following exercises are designed to help you make the most of "
    "your revision sessions. You answer the questions, and if you get a "
    "wrong answer, you will be directed to the relevant part of the "
    "course to review, so that you can improve your understanding of the "
    "course material."
)

# Les parties du cours, par leur titre : un titre de section en dirait
# trop (« MSP ≠ CPTS »), celui de la partie oriente sans répondre.
PARTIES = {
    "I": "Primary care, first contact, community care: what are we "
         "talking about?",
    "II": "Why the general practitioner holds a central place",
    "III": "The professionals of local care",
    "V": "The forms of coordinated organisation",
    "VI": "Unscheduled care",
    "VII": "Medical deserts and access to care",
    "VIII": "Telehealth",
    "XI": "Reference: the historical milestones to remember",
}


def _lecon(partie, *suite):
    return (
        INTITULE,
        "Where to look in the course: **Session 4, part %s** — %s"
        % (partie, PARTIES[partie]),
    ) + suite


def _revoir(partie, sections):
    return "Session 4, part %s “%s”, %s" % (partie, PARTIES[partie], sections)


# --------------------------------------------------------------------------
# Questions à choix unique
# --------------------------------------------------------------------------

# (énoncé, (quatre propositions), index de la bonne, niveau, explication,
#  partie, sections à revoir)
# Comme dans qcm_docker, la bonne réponse est écrite en premier puis
# déplacée par `_tourner`.
QUESTIONS = (
    ("Among the four expressions primary care, first-contact care, "
     "community care and ambulatory care, which two describe a FUNCTION "
     "in the pathway rather than a place or a mode of practice?",
     ("Primary care and first-contact care",
      "Community care and ambulatory care",
      "Primary care and community care",
      "First-contact care and ambulatory care"),
     0, 3,
     "Primary care and first-contact care describe a functional level in "
     "the pathway. Community care (soins de ville) and ambulatory care "
     "describe a place or a mode of practice outside full hospitalisation.",
     "I", "sections I.1 to I.5"),

    ("How does the course classify a self-employed cardiologist who "
     "practises in town?",
     ("Community care, at the second level of contact",
      "First-contact care, because they practise outside hospital",
      "Hospital care, at the second or third level",
      "Primary care, because patients can consult them in town"),
     0, 3,
     "“Community” tells you WHERE, “first contact” AT WHICH LEVEL. The "
     "cardiologist practises in the community, but is generally reached "
     "after a first contact: community + second contact.",
     "I", "section I.4"),

    ("Which of these is ambulatory care but NOT community care?",
     ("Day surgery in a hospital",
      "A consultation with a general practitioner in town",
      "A home visit by a self-employed nurse",
      "Pharmaceutical advice at a community pharmacy"),
     0, 4,
     "Ambulatory care is care that does not require full inpatient "
     "admission: it includes hospital outpatient consultations and day "
     "surgery. Do not equate ambulatory with community medicine.",
     "I", "section I.5 and the glossary"),

    ("In the coordinated care pathway, the specialist consulted never "
     "sends any information back. What does the registered doctor lose?",
     ("They remain the entry point, but are no longer the coordination "
      "point",
      "They are no longer the patient's entry point into the system",
      "They lose their status, and the specialist becomes the registered "
      "doctor",
      "Nothing: the return of information is optional in the pathway"),
     0, 3,
     "The chain is patient → registered doctor → specialist → hospital → "
     "return of information → registered doctor. Without the return of "
     "information, the doctor is still the entry point but no longer the "
     "coordination point.",
     "II", "section II.4"),

    ("How does the French system make patients follow the coordinated "
     "care pathway?",
     ("With a financial incentive: outside the pathway, except in defined "
      "cases, coverage is reduced",
      "With a prohibition: a specialist may not see a patient without a "
      "referral",
      "With a compulsory registration: the regional health agency assigns "
      "every patient a doctor",
      "With a quota: each patient is entitled to a fixed number of "
      "specialist consultations"),
     0, 3,
     "Freedom is preserved, and financing is used to steer behaviour: the "
     "pathway followed is better reimbursed. A financial incentive, not a "
     "prohibition.",
     "II", "section II.5"),

    ("Which of these consultations benefits from specific direct access, "
     "outside the coordinated pathway?",
     ("A psychiatrist, for a 20-year-old patient",
      "A psychiatrist, for a 40-year-old patient",
      "A cardiologist, for a patient with heart failure",
      "A dermatologist, for a patient with a skin rash"),
     0, 4,
     "Direct access exists for example with a gynaecologist, an "
     "ophthalmologist, a stomatologist, and a psychiatrist or "
     "neuropsychiatrist for patients aged 16 to 25.",
     "II", "section II.5"),

    ("On 30 June 2025, 4.2 % of patients with a long-term condition had no "
     "registered doctor. Why does the course single out this figure?",
     ("These patients are precisely the population for whom coordination "
      "matters most",
      "It covers every French patient, so several million people are "
      "concerned",
      "It is the share of general practitioners who refuse new patients",
      "It is the share of territories classified as medical deserts"),
     0, 4,
     "The figure concerns patients with a recognised chronic condition — "
     "the very population for whom a coordinator is most needed. Hence "
     "the question: can the model rest on the registered doctor when "
     "access to a doctor is itself becoming difficult?",
     "II", "section II.6"),

    ("Since 2026, which patients can designate a referent nurse?",
     ("Patients aged 16 or over with a long-term condition, under "
      "conditions, alongside their registered doctor",
      "Any patient without a registered doctor, in place of the doctor",
      "Patients aged 16 to 25, to gain direct access to psychiatric care",
      "Only patients followed in oncology by an advanced practice nurse"),
     0, 3,
     "The referent nurse strengthens coordination alongside the "
     "registered doctor and improves the follow-up of fragile patients: "
     "coordination is becoming multi-professional.",
     "III", "section III.4 and the glossary"),

    ("A patient with a sore throat goes straight to the pharmacy: rapid "
     "test, no exclusion criterion found, antibiotic dispensed without "
     "prior prescription. Why does the course call this a real change in the "
     "architecture of the system?",
     ("The pharmacist becomes a new entry point, with its own rules, "
      "training requirement and exclusion criteria",
      "The pharmacist replaces the registered doctor as the coordinator "
      "of the pathway",
      "A new digital tool lets the doctor prescribe remotely through the "
      "pharmacy",
      "Antibiotics can now be dispensed without a prescription in every "
      "case"),
     0, 4,
     "Not a new tool bolted on, but a new path through the system: "
     "patient → pharmacist → test and treatment, or medical orientation "
     "when necessary.",
     "III", "sections III.5 and III.6"),

    ("In a territory of 80 000 inhabitants, many patients cannot find a "
     "registered doctor and every doctor's list is full. Which response "
     "matches the scale of the problem?",
     ("A CPTS, which organises the professionals of the whole territory "
      "and seeks a solution within it",
      "A new MSP, since a team built around a health project solves "
      "problems at the scale of a territory",
      "A group practice, since shared premises and secretarial support "
      "are enough to coordinate care",
      "A CPTS, because it keeps its own patient list and can take on the "
      "patients left without a doctor"),
     0, 4,
     "A practice has patients, a community has a population. The CPTS "
     "has no patient list and does not deliver care: it does not create "
     "a doctor, it organises the existing resource better. A team-level "
     "solution to a territory-level problem will not work.",
     "V", "sections V.6 to V.9"),

    ("Which statement about a health centre (centre de santé) is "
     "correct?",
     ("Its professionals are salaried, it applies direct third-party "
      "payment, and it must also have a health project",
      "Its professionals are self-employed and share premises, with no "
      "need for a health project",
      "It organises the professionals of a territory and does not "
      "deliver care itself",
      "It was written into the public health code in 2007 to fight "
      "professional isolation"),
     0, 3,
     "A health centre can be single- or multi-professional; its "
     "professionals are salaried, and like every coordinated structure it "
     "has a health project. The 2007 recognition concerns the MSP.",
     "V", "the glossary (organisations) and section V.3"),

    ("“I have had severe pain since this afternoon. My doctor is "
     "unavailable.” After medical triage, the access service judges the "
     "need rapid but not vital. What is the appropriate response?",
     ("An appointment with an available doctor",
      "Orientation to the hospital emergency department, open 24 hours "
      "a day",
      "Medical advice only, since the situation is not life-threatening",
      "Waiting for the registered doctor through the normal pathway"),
     0, 3,
     "One call, four outcomes: serious → emergency; rapid but not vital "
     "→ an available doctor; advice sufficient → medical advice; "
     "teleconsultation relevant → teleconsultation.",
     "VI", "sections VI.4 and VI.5"),

    ("A general practitioner sends photos of a skin lesion to a "
     "dermatologist for a rapid opinion; the patient takes no part in the "
     "exchange. Which form of telemedicine is this?",
     ("Tele-expertise",
      "Teleconsultation",
      "Tele-assistance",
      "Remote monitoring"),
     0, 3,
     "Tele-expertise links a professional and an expert doctor; the "
     "patient need not take part. Teleconsultation is only one category "
     "of telemedicine.",
     "VIII", "section VIII.1"),

    ("Why is the ratio “number of doctors / population” not enough to "
     "identify a medical desert?",
     ("The numerator does not measure available medical time, and the "
      "denominator does not measure need",
      "It counts hospital doctors, whereas only general practitioners "
      "should be counted",
      "It ignores teleconsultations, which now replace physical "
      "consultations",
      "It is published too late to guide the setting-up of doctors"),
     0, 4,
     "A doctor may work part time, have a very different patient list, "
     "be near or far, accept or refuse new patients; and need depends on "
     "the age structure. Localised potential accessibility (APL) "
     "measures offer against need.",
     "VII", "sections VII.1 and VII.2"),
)


def _question(rang, question, choices, answer, level, explanation,
              partie, sections):
    choices, answer = _tourner(choices, answer, rang)
    pattern = qcm_pattern("ie3514_s4_q%02d" % rang, rang, question,
                          choices, answer, level, explanation)
    # Les retours sont réécrits en anglais, la langue du cours. Une réponse
    # fausse oriente vers le cours : la même phrase pour les trois
    # propositions fausses, qui ne dit donc pas laquelle est juste.
    revoir = _revoir(partie, sections)
    juste = "Correct. %s See %s." % (explanation, revoir)
    faux = "Not quite. Review %s, then try again." % revoir
    label, options = pattern.blanks["choix"]
    options = [replace(o, note=juste if o.id == pattern.ref["choix"]
                       else faux)
               for o in options]
    return replace(pattern, blanks={"choix": (label, options)},
                   lesson=_lecon(partie))


QCM = tuple(_question(number + 1, *entree)
            for number, entree in enumerate(QUESTIONS))


# --------------------------------------------------------------------------
# Textes à trous
# --------------------------------------------------------------------------

def _trou(numero, propositions, revoir):
    """Menu d'un trou : la bonne proposition en premier, `a`.

    Chaque option rend sa ligne de verdict. Une proposition fausse renvoie
    à la partie du cours à relire, mais pas à la bonne réponse.
    """
    juste = "[%d] ✔" % numero
    faux = "[%d] ✘ review %s" % (numero, revoir)
    return ("Blank [%d]" % numero,
            [Option(oid, texte, lambda _p, ligne=(juste if i == 0 else faux):
                    ligne)
             for i, (oid, texte) in enumerate(zip("abcd", propositions))])


def _texte(key, name, brief, why, level, partie, tpl, trous, note):
    """Un texte à trous : un verdict par trou, dans l'ordre du texte."""
    blanks = {"t%d" % n: _trou(n, propositions, _revoir(partie, sections))
              for n, (propositions, sections) in enumerate(trous, 1)}
    return Pattern(
        key=key,
        name=name,
        brief=brief,
        why=why,
        lesson=_lecon(
            partie,
            "Choose one proposal per blank, then check: each blank gets its "
            "own verdict, ✔ or ✘, and a wrong blank tells you which section "
            "of the course to review.",
        ),
        tpl=tpl,
        blanks=blanks,
        ref={blank_id: "a" for blank_id in blanks},
        rows=lambda _p, get: [get(blank_id)(_p) for blank_id in blanks],
        level=level,
        teacher_note=note,
    )


TEXTES = (
    _texte(
        "ie3514_s4_c01", "Four terms, two axes",
        "Complete the text on the four expressions that describe local care.",
        "Two of them describe a function, the other two a place or a mode.",
        3, "I",
        """“Primary care” and “first-contact care” describe a
[1] @t1@ in the pathway.

“Community care” (soins de ville) describes a
[2] @t2@ of practice outside full hospitalisation.

A hospital outpatient consultation is
[3] @t3@ care, but it is not community care.""",
        ((("FUNCTIONAL LEVEL", "PLACE", "PROFESSION", "FINANCING MODE"),
          "sections I.1 to I.3"),
         (("PLACE or MODE", "FUNCTIONAL LEVEL", "FIRST CONTACT",
           "SECOND LEVEL"),
          "section I.4"),
         (("ambulatory", "primary", "first-contact", "community"),
          "section I.5")),
        "Diapositives I.1 à I.5 et glossaire 1/2.",
    ),
    _texte(
        "ie3514_s4_c02", "The 2004 compromise",
        "Complete the text on the registered family doctor (médecin "
        "traitant).",
        "Keep freedom of choice while creating a point of coordination.",
        3, "II",
        """In [1] @t1@, France introduced the registered family doctor.

The aim was to keep freedom of choice while creating a point of
[2] @t2@.

The coordinated pathway is enforced by
[3] @t3@.""",
        ((("2004", "1971", "2007", "2016"), "sections II.3 and XI"),
         (("coordination", "prescription", "registration", "specialisation"),
          "section II.3"),
         (("a financial incentive: better reimbursement inside the pathway",
           "a prohibition on consulting a specialist directly",
           "a quota of consultations allowed per patient",
           "a referral letter required for every specialist, without "
           "exception"),
          "section II.5")),
        "Diapositives II.3 à II.5 et XI.",
    ),
    _texte(
        "ie3514_s4_c03", "A practice and a community",
        "Complete the text comparing the MSP and the CPTS.",
        "A practice has patients; a community has a population.",
        4, "V",
        """An MSP (maison de santé pluriprofessionnelle) is a
[1] @t1@ organised around a shared health project.

A CPTS is an organisation of professionals at the scale of a
[2] @t2@.

Unlike an MSP, a CPTS
[3] @t3@.""",
        ((("TEAM", "TERRITORY", "BUILDING", "HOSPITAL DEPARTMENT"),
          "sections V.3 and V.4"),
         (("TERRITORY", "TEAM", "BUILDING", "REGION"), "sections V.6 and V.7"),
         (("has no patient list of its own and does not deliver care",
           "has no health project",
           "must gather all its members under one roof",
           "can only associate self-employed doctors"),
          "sections V.6 to V.9")),
        "Diapositives V.3 à V.9. Piège du trou 3 : MSP et CPTS ont toutes "
        "deux un projet de santé.",
    ),
    _texte(
        "ie3514_s4_c04", "When the practices are closed",
        "Complete the text on the organisation of unscheduled care.",
        "Not every request should end up in an emergency department.",
        4, "VI",
        """The [1] @t1@ (PDSA)
provides a medical response outside normal practice opening hours.

The [2] @t2@ (SAS)
is a coordinated response between community care and emergency
medical aid, notably through the number [3] @t3@.""",
        ((("out-of-hours ambulatory care", "healthcare access service",
           "specialised care team", "territorial professional health "
           "community"),
          "section VI.3 and the glossary"),
         (("healthcare access service", "out-of-hours ambulatory care",
           "primary care team", "France Santé network"),
          "section VI.4 and the glossary"),
         (("15", "17", "18", "114"), "section VI.4")),
        "Diapositives VI.3 et VI.4, glossaire 2/2. Le cours ne cite que "
        "le 15 ; aucun distracteur n'est le 116 117, qu'on pourrait "
        "défendre selon les régions.",
    ),
    _texte(
        "ie3514_s4_c05", "Five forms of telemedicine",
        "Complete the definitions of three forms of telemedicine.",
        "Teleconsultation is only one category of telemedicine.",
        3, "VIII",
        """Remote monitoring:
[1] @t1@.

Tele-assistance:
[2] @t2@.

The response given in the context of medical regulation is
[3] @t3@.""",
        ((("data collected at a distance, interpreted by the professional",
           "a patient and a doctor consult by video",
           "a professional asks an expert doctor for an opinion",
           "a professional helps another during a procedure"),
          "section VIII.1"),
         (("a professional helps another during a procedure",
           "a patient and a doctor consult by video",
           "a professional asks an expert doctor for an opinion",
           "data collected at a distance, interpreted by the professional"),
          "section VIII.1"),
         (("also a telemedicine act", "a teleconsultation",
           "not a telemedicine act", "a tele-expertise"),
          "section VIII.1")),
        "Diapositive VIII.1 et glossaire 2/2.",
    ),
    _texte(
        "ie3514_s4_c06", "Milestones and the problems they address",
        "Complete the dates of three reforms of local care.",
        "Each reform answers a specific problem.",
        4, "XI",
        """[1] @t1@: multidisciplinary practices are recognised,
to fight professional isolation.

[2] @t2@: territorial professional health communities are created,
to coordinate actors at the scale of a population.

[3] @t3@: the France Santé network, to structure the first-contact
offer and make it legible.""",
        ((("2007", "2004", "2016", "2020"), "section XI"),
         (("2016", "2007", "2009-10", "2020"), "section XI"),
         (("2026", "2016", "2020", "2004"), "sections IX and XI")),
        "Tableau des jalons (XI) et diapositive IX.",
    ),
)


PATTERNS = one_line_per_blank(QCM + TEXTES)

MODULE = Module(
    key="ie3514_s4",
    title="IE3514 - Revision Sheet for Session 4",
    level=4,
    summary="Revision of IE.3514 session 4: primary and first-contact "
            "care, the registered doctor and the coordinated care pathway, "
            "local health professionals, MSP and CPTS, unscheduled care, "
            "medical deserts, telehealth. Each wrong answer points to the "
            "part of the course to review.",
    keys=tuple(p.key for p in PATTERNS),
)
