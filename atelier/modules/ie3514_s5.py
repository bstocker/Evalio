"""Module « IE3514 - Revision Sheet for Session 5 », du chapitre Révisions.

Une fiche de révision sur la séance 5 du cours IE.3514 (Healthcare
systems organization) : l'hôpital français, ses missions, son
organisation, sa gouvernance et son territoire. Le cours est en anglais,
la fiche aussi : l'élève révise avec les mots qu'il a lus en séance.

Deux formes, toutes deux de niveau difficile ou très difficile :

- des textes à trous, en mode « compléter ». Le texte tient la place du
  code, chaque trou est un menu, et la « sortie » est un verdict par
  trou : ✓ si le mot choisi est celui du cours, ✗ et la section à relire
  sinon. La cible ne montre que des ✓ : elle ne dit rien des mots ;
- des questions à choix unique. Une mauvaise réponse renvoie à la section
  du cours qui la traite, sans nommer la bonne ; la bonne réponse, une
  fois trouvée, porte son explication.

Les sections citées (« III.2 Emergency departments »…) sont celles des
diapositives de la séance, numéro et titre compris.
"""

from dataclasses import replace
import re

from ..engine import Module, Option, Pattern, one_line_per_blank, qcm_pattern
from .qcm_docker import _tourner

TITLE = "IE3514 - Revision Sheet for Session 5"

# L'en-tête demandé par l'enseignant, affiché en tête de chaque exercice.
INTRO = ("The following exercises are designed to help you make the most of "
         "your revision sessions. You answer the questions, and if you get a "
         "wrong answer, you will be directed to the relevant part of the "
         "course to review, so that you can improve your understanding of "
         "the course material.")

OK, KO = "✓", "✗"


# « VIII.2 - VIII.4 The 2016 answer » : le numéro, puis le titre.
_SECTION = re.compile(r"^([IVX]+(?:\.\d+)?(?: - [IVX]+\.\d+)?) (.+)$")


def _section(section):
    """`VIII.2 - VIII.4 "The 2016 answer"` : le titre se détache du numéro."""
    numero, titre = _SECTION.match(section).groups()
    return '%s "%s"' % (numero, titre)


def _see(section):
    return "review section %s in the session 5 slides" % _section(section)


# --------------------------------------------------------------------------
# Textes à trous
# --------------------------------------------------------------------------

# (clé, nom, niveau, texte, trous)
# Le texte porte un marqueur @bN@ par trou, dans l'ordre des menus.
# Chaque trou : (section du cours, bonne réponse, (trois leurres)).
# Un leurre n'est jamais une autre façon correcte de dire la même chose.
CLOZES = (
    ("ie5_espic", "ESPIC, the status that confuses", 3,
     "An ESPIC is a private health facility of collective interest.\n"
     "It is @b1@ in law, @b2@ in purpose,\n"
     "and able to carry @b3@ missions.",
     (("II.2 Statuses", "private",
       ("public", "university", "regional")),
      ("II.2 Statuses", "non-profit",
       ("for-profit", "commercial", "profit-sharing")),
      ("II.2 Statuses", "public hospital service",
       ("regional agency", "supervisory board", "health insurance")))),

    ("ie5_chu", "What a university hospital really is", 3,
     "Created in @b1@, the university hospital (CHU) is NOT simply\n"
     "a large hospital. On top of care, it associates @b2@\n"
     "and research, and it ensures @b3@ referral\n"
     "and innovation.",
     (("I.2 The university hospitals","1958",
       ("1970", "1996", "2016")),
      ("I.2 The university hospitals","teaching",
       ("emergency care", "hospital at home", "medico-social support")),
      ("I.2 The university hospitals","regional or inter-regional",
       ("proximity", "municipal", "primary-care")))),

    ("ie5_gouvernance", "Who does what in a public hospital", 4,
     "The pedagogical simplification worth memorising:\n"
     "  Supervisory board  ->  @b1@\n"
     "  Director           ->  @b2@\n"
     "  Executive board    ->  @b3@\n"
     "  Medical committee  ->  @b4@",
     (("V.4 - V.6 The other bodies", "orientation and control",
       ("conduct and management",
        "medico-administrative strategic steering",
        "medical strategy, quality and safety")),
      ("V.2 The director", "conduct and management",
       ("orientation and control",
        "medico-administrative strategic steering",
        "medical strategy, quality and safety")),
      ("V.4 - V.6 The other bodies",
       "medico-administrative strategic steering",
       ("orientation and control",
        "conduct and management",
        "medical strategy, quality and safety")),
      ("V.3 The medical committee", "medical strategy, quality and safety",
       ("orientation and control",
        "conduct and management",
        "medico-administrative strategic steering")))),

    ("ie5_gradation", "The three levels of gradation", 4,
     "Gradation of care distributes activities across levels.\n"
     "The first level, @b1@, covers general medicine,\n"
     "consultations and simple imaging. The second, @b2@,\n"
     "covers emergency care, surgery, maternity and critical care.\n"
     "The third, @b3@, covers rare activities, transplantation\n"
     "and rare diseases. The guiding question is not\n"
     "\"which is the best hospital?\" but \"@b4@\"",
     (("VII.1 Three levels", "proximity",
       ("territorial referral", "regional referral", "national excellence")),
      ("VII.1 Three levels", "territorial referral",
       ("proximity", "regional referral", "national excellence")),
      ("VII.1 Three levels", "regional referral",
       ("proximity", "territorial referral", "national excellence")),
      ("VII.1 Three levels", "which hospital fits this patient's need?",
       ("which hospital is the nearest?",
        "which hospital has the most beds?",
        "which hospital costs the least?")))),

    ("ie5_ambulatoire", "Fewer nights, the same need for care", 3,
     "Full hospitalisation means at least @b1@ in the facility:\n"
     "the bed is the important resource. In the ambulatory model,\n"
     "the patient is admitted @b2@, operated on, monitored,\n"
     "and discharged @b3@. Reducing hospital nights does not\n"
     "remove the need for care: it @b4@ part of it towards the\n"
     "home, community care, relatives, digital tools and coordination.",
     (("III.9 - III.10 The ambulatory shift", "one night",
       ("three nights", "one week", "one surgical procedure")),
      ("III.9 - III.10 The ambulatory shift", "in the morning",
       ("the day before", "the week before", "at night")),
      ("III.9 - III.10 The ambulatory shift", "in the evening",
       ("the next morning", "after several nights",
        "after rehabilitation")),
      ("III.9 - III.10 The ambulatory shift", "displaces",
       ("eliminates", "cancels", "concentrates in the hospital")))),

    ("ie5_autorisation", "Three functions, three actors", 3,
     "\"We have found a neurosurgeon, we start on Monday\" is not\n"
     "enough: some activities require an authorisation.\n"
     "  The State            @b1@\n"
     "  The regional agency  @b2@\n"
     "  The facility         @b3@\n"
     "and the facility is the only one that touches a patient.",
     (("VI.1 - VI.2 Authorisations", "defines the rules",
       ("organises and authorises", "delivers the care",
        "certifies quality")),
      ("VI.1 - VI.2 Authorisations", "organises and authorises",
       ("defines the rules", "delivers the care", "certifies quality")),
      ("VI.1 - VI.2 Authorisations", "delivers the care",
       ("defines the rules", "organises and authorises",
        "certifies quality")))),

    ("ie5_ght", "Territorial hospital groupings", 4,
     "Territorial hospital groupings (GHT) were created in @b1@\n"
     "to oblige @b2@ facilities to think in terms of a common\n"
     "territorial medical strategy. Their core is the @b3@,\n"
     "approved by the competent regional agencies, and certain\n"
     "functions are pooled on behalf of the grouping by the @b4@.",
     (("VIII.2 - VIII.4 The 2016 answer", "2016",
       ("2009", "2004", "1996")),
      ("VIII.2 - VIII.4 The 2016 answer", "public",
       ("private for-profit", "private non-profit", "community-care")),
      ("VIII.2 - VIII.4 The 2016 answer", "shared medical project",
       ("facility project", "regional health plan", "global budget")),
      ("VIII.2 - VIII.4 The 2016 answer", "lead facility",
       ("supervisory board", "commission of users", "regional agency")))),

    ("ie5_flux", "Why ten more beds may solve nothing", 4,
     "A hospitalisation can be @b1@ finished and\n"
     "@b2@ impossible to finish. The bed stays occupied,\n"
     "and a bed-based analysis concludes that the hospital lacks\n"
     "capacity, whereas the missing resource lies @b3@.\n"
     "Adding ten beds then solves nothing: it is a problem of\n"
     "@b4@, not of capacity.",
     (("XIII The key notion", "medically",
       ("organisationally", "financially", "legally")),
      ("XIII The key notion", "organisationally",
       ("medically", "financially", "legally")),
      ("XIII The key notion", "downstream",
       ("upstream", "inside the operating theatre",
        "in the emergency department")),
      ("XVII.6 The decisive tension", "flow",
       ("staffing", "funding", "equipment")))),
)

CLOZE_LESSON = (
    INTRO,
    "Choose one word or phrase per blank, then check: each blank gets "
    "%s when it matches the course, %s and the section to review "
    "otherwise." % (OK, KO),
)


def _cloze(key, name, level, text, trous):
    blanks, ref = {}, {}
    for rang, (_section, bonne, leurres) in enumerate(trous, start=1):
        blank_id = "b%d" % rang
        options = [Option("a", bonne, True)]
        options += [Option(lettre, leurre, False)
                    for lettre, leurre in zip("bcd", leurres)]
        blanks[blank_id] = ("Blank %d" % rang, options)
        ref[blank_id] = "a"

    def rows(_params, get):
        lignes = []
        for rang, (section, _bonne, _leurres) in enumerate(trous, start=1):
            if get("b%d" % rang):
                lignes.append("Blank %d: %s consistent with the course"
                              % (rang, OK))
            else:
                lignes.append("Blank %d: %s not consistent - %s"
                              % (rang, KO, _see(section)))
        return lignes

    return Pattern(
        key=key,
        name=name,
        brief="Complete the text so that it says what the course says.",
        why="Every blank has exactly one answer consistent with the "
            "session 5 slides.",
        lesson=CLOZE_LESSON,
        tpl=text,
        blanks=blanks,
        ref=ref,
        rows=rows,
        level=level,
    )


# --------------------------------------------------------------------------
# Questions à choix unique
# --------------------------------------------------------------------------

# (énoncé, (quatre propositions), index de la bonne, niveau, section,
#  explication). Comme dans qcm_docker, la bonne réponse est écrite en
# premier puis déplacée par `_tourner`.
QUESTIONS = (
    ("French general and paediatric emergency structures recorded 21.3 "
     "million attendances in 2024. Which reading of this figure is "
     "consistent with the course?",
     ("The emergency department is above all a function of assessment and "
      "orientation: many patients are assessed, receive care and return "
      "home without being hospitalised",
      "Each attendance leads to an admission, so emergency activity is best "
      "measured by counting admissions",
      "The figure measures the occupancy of emergency department beds",
      "The figure fell compared with 2023, a sign that the ambulatory shift "
      "is emptying emergency departments"),
     0, 3, "III.2 Emergency departments",
     "The emergency department is a function of assessment and orientation, "
     "not only a door for admission. Measuring it in admissions misses most "
     "of what it does. The 2024 figure was up 2.5 % on 2023."),

    ("An emergency department is saturated. In the course's analysis, which "
     "of these causes lies DOWNSTREAM of the department?",
     ("No place is available in rehabilitation for patients who are ready "
      "to leave",
      "Primary care is insufficient in the territory",
      "Imaging is unavailable when the department needs it",
      "The population is ageing and precarity is rising"),
     0, 3, "III.3 A systemic revealer",
     "Lack of beds, no place in rehabilitation, no medico-social solution "
     "and difficulty returning home are downstream causes. Primary care, "
     "ageing and precarity are upstream; imaging is inside the hospital. "
     "A saturated emergency department is often the symptom of a problem "
     "of the system."),

    ("A newspaper writes: \"the hospital lost 200 beds this year, so its "
     "capacity fell\". Why does the course consider this reasoning weak?",
     ("Beds, partial hospitalisation places and hospital-at-home capacity "
      "are different units that can move in different directions",
      "DREES does not publish bed counts, so the figure cannot be checked",
      "Every bed closed is automatically replaced by a hospital-at-home "
      "place, so capacity never changes",
      "Bed counts only concern private clinics, not public hospitals"),
     0, 3, "I.4 A caution",
     "The number of beds is no longer the only indicator of hospital "
     "capacity. As section II.1 shows, beds (367,100), partial "
     "hospitalisation places (91,000) and hospital at home (25,400 "
     "patients at a time) are three units: quoting one of them as "
     "\"hospital capacity\" is meaningless."),

    ("According to the figures quoted in the course (DREES, end of 2024), "
     "which statement about the French hospital landscape is correct?",
     ("There are about 1,330 public hospitals, 655 private non-profit "
      "facilities and 980 private clinics",
      "Private clinics outnumber public hospitals, which are now a minority "
      "of facilities",
      "Private non-profit facilities are the most numerous of the three "
      "categories",
      "The figures confirm that public hospitals do complex medicine and "
      "private clinics simple medicine"),
     0, 4, "II.3 A genuinely mixed landscape",
     "About 2,962 facilities: 1,330 public, 655 private non-profit, 980 "
     "private for-profit. The mix depends on authorisations, specialties, "
     "equipment, the territory and the medical project, not on a "
     "public = complex / private = simple caricature."),

    ("Which statement about hospital at home (HAD) is correct?",
     ("It is a hospitalisation: a health facility activity with the same "
      "obligations, for care that would otherwise require admission",
      "It is a home nursing service that lies outside the remit of health "
      "facilities",
      "It is a form of partial hospitalisation: day hospital without an "
      "overnight stay",
      "It is a medico-social solution used once hospital care is over"),
     0, 3, "III.8 Hospital at home",
     "HAD = hospitalisation, not \"a nurse who visits the house\": complex "
     "dressings, intravenous treatments, certain chemotherapies, palliative "
     "care… What the patient needs is a hospital organisation around them, "
     "not necessarily a hospital building."),

    ("Why does the course speak of a technical \"platform\" rather than a "
     "\"department\" for imaging, the laboratory or the operating theatre?",
     ("Because a single resource, such as one CT scanner, serves several "
      "specialties at once, which is exactly where queues form",
      "Because these activities are outsourced to private operators",
      "Because a platform holds equipment only and has no professionals of "
      "its own",
      "Because a platform is reserved for patients in critical care"),
     0, 3, "III.4 - III.5 Critical care and technical platforms",
     "One CT scanner serves neurology, trauma, emergency, oncology and "
     "surgery. A platform is a transversal resource, and transversal "
     "resources are where queues form."),

    ("Which of these decisions does NOT belong to the director of a public "
     "hospital?",
     ("Deciding a patient's medical diagnosis",
      "Setting the general organisation of the facility",
      "Conducting human resources policy",
      "Contracting on behalf of the facility"),
     0, 3, "V.2 The director",
     "The director, president of the executive board, conducts the general "
     "policy: strategy, organisation, resources, finances, investment, human "
     "resources, contracting. The medical decision stays with the "
     "professionals: management authority meets medical autonomy."),

    ("Which statement about the executive board (directoire) is correct?",
     ("It is presided over by the director, with the president of the "
      "medical committee as vice-president, and a majority from the "
      "medical, pharmaceutical, midwifery and dental professions",
      "It is presided over by the president of the medical committee and "
      "made up mainly of administrative managers",
      "It rules on strategy and exercises permanent control over the "
      "management",
      "It analyses complaints and claims, and its report feeds the medical "
      "committee's work on quality"),
     0, 4, "V.4 - V.6 The other bodies",
     "The executive board prepares and conducts the facility project and "
     "advises the director: medico-administrative strategic steering. "
     "Ruling on strategy and controlling the management is the supervisory "
     "board; analysing complaints is the commission of users."),

    ("Why does the course insist that low volume is not only a financial "
     "problem?",
     ("Because expertise needs cases: a team that treats too few patients "
      "cannot maintain its skills, which is a quality problem",
      "Because low volume increases distances and delays for patients",
      "Because the regional agency withdraws funding automatically below a "
      "set threshold",
      "Because low volume always leads to a shortage of beds"),
     0, 4, "VI.3 Why regulate at all?",
     "An over-abundance of equipment produces unnecessary costs, dispersed "
     "professionals, low activity per team and difficulty maintaining "
     "expertise. Distances and delays are the cost of the opposite excess, "
     "too much concentration: proximity versus expertise."),

    ("A patient with a suspected stroke calls the emergency number. The "
     "ambulance drives past the nearest hospital, which has no stroke unit. "
     "Which principle of the course does this illustrate?",
     ("Geographical proximity is not the same as an appropriate facility: "
      "speed of access to the right technical level matters more than "
      "distance",
      "Every hospital should hold a stroke unit to avoid such transfers",
      "The ambulatory shift: the patient should be treated without being "
      "hospitalised",
      "The autonomy of three neighbouring hospitals has produced a "
      "coordination failure"),
     0, 3, "VII.2 Example (stroke)",
     "The appropriate facility has imaging and a stroke unit; a very complex "
     "case goes to a referral centre with interventional neuroradiology or "
     "neurosurgery. Gradation asks which hospital fits the patient's need, "
     "not which one is nearest."),

    ("What does the course say a territorial hospital grouping (GHT) "
     "achieves?",
     ("It does not remove coordination problems; it creates a framework in "
      "which to address them",
      "It removes divergent interests by merging its facilities into a "
      "single legal entity",
      "It frees its facilities from the approval of the regional agency",
      "It solves the scarcity of human resources by moving all staff to the "
      "lead facility"),
     0, 4, "VIII.7 Honest limits",
     "Divergent interests, fear of losing an activity, distance, complex "
     "governance, heterogeneous information systems, scarce human resources "
     "and a feeling of centralisation remain. A structure is rarely a "
     "solution; it is a place where a solution can be negotiated."),

    ("Which hospital financing mode carries the risk of encouraging volume?",
     ("Activity-based payment",
      "The per-diem price",
      "The global budget",
      "A diversified logic based on missions, quality and territorial "
      "needs"),
     0, 4, "XI Financing",
     "Activity-based payment links resources to activity, hence the risk of "
     "encouraging volume. The per-diem price risks long stays; the global "
     "budget controls expenditure but barely takes real activity into "
     "account."),
)

QCM_LESSON = (INTRO,)


def _question(rang, question, choices, answer, level, section, explanation):
    """Une question du cours, montée sur `qcm_pattern`.

    `qcm_pattern` ne commente que la bonne réponse. Ici, une mauvaise
    réponse renvoie en plus à la section du cours qui la traite — sans
    nommer la bonne, que l'élève pourrait sinon recocher.
    """
    choices, answer = _tourner(choices, answer, rang)
    pattern = qcm_pattern("ie5_q%02d" % rang, rang, question, choices,
                          answer, level)
    label, options = pattern.blanks["choix"]
    bonne = pattern.ref["choix"]
    options = [replace(o, note=("Correct. %s (Section %s.)"
                                % (explanation, _section(section)))
                       if o.id == bonne else
                       "Not quite: %s, then try again." % _see(section))
               for o in options]
    return replace(pattern, blanks={"choix": (label, options)},
                   lesson=QCM_LESSON)


PATTERNS = one_line_per_blank(
    tuple(_cloze(*entree) for entree in CLOZES)
    + tuple(_question(number + 1, *entree)
            for number, entree in enumerate(QUESTIONS))
)

MODULE = Module(
    key="ie3514_s5",
    title=TITLE,
    level=3,
    summary=INTRO,
    keys=tuple(p.key for p in PATTERNS),
)
