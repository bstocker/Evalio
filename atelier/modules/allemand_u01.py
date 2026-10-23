"""Module « Unité 1 » du chapitre Allemand : Ferien in den DACH-Ländern.

Des exercices de révision sur la première unité d'allemand de 3e (LV2) :
l'humeur et la météo, les mots interrogatifs, les activités de vacances
et leurs lieux, l'opinion, la place du verbe, le locatif (in) et le
directif (nach), la préposition mit et le datif, les possessifs, les
verbes forts en -a et en -e, sein et haben au prétérit, le parfait.

Les phrases sont écrites pour l'exercice, dans l'esprit du cours : on en
tire des exercices, pas des extraits.

Deux formes, et dans les deux un **accompagnement** qui oriente sans
donner la réponse :

- des **phrases à trous** (mode « compléter ») : la cible donne, pour
  chaque trou, ce que la phrase doit dire (sa traduction, ou la forme
  demandée). Un choix juste reproduit la ligne de la cible ; un choix
  faux affiche à sa place un indice — ce que dit vraiment le mot choisi,
  la règle à revoir. L'indice ne nomme jamais la bonne réponse, et chaque
  indice diffère de la ligne attendue : aucun mauvais choix ne reproduit
  la cible ;
- des **questions** (mode QCM) dont chaque proposition fausse porte son
  indice. C'est un écart voulu avec `qcm_pattern`, qui laisse les
  erreurs sans commentaire : ici l'enseignant a demandé qu'on explique
  l'erreur à l'élève. L'indice dit pourquoi le choix ne convient pas,
  jamais lequel convient ; le barème, lui, compte l'essai manqué comme
  partout ailleurs.

L'élève est tutoyé, comme dans le cours.
"""

from dataclasses import replace

from ..engine import Module, Option, Pattern, qcm_pattern

INTITULE = (
    "Exercices de révision de l'unité 1. Si ta réponse est fausse, un "
    "indice t'explique ton erreur sans te donner la solution : relis-le, "
    "puis corrige."
)

LECTURE_TROUS = (
    "Pour chaque trou, la **cible** (« Motif à reproduire ») dit ce que "
    "la phrase doit exprimer. Choisis dans chaque menu le mot qui convient.",
    "Une ligne en rouge est un indice sur ton erreur : compare-la à la "
    "ligne attendue, puis corrige ton choix.",
)


def _fixe(texte):
    return lambda _params: texte


def trous(key, name, brief, level, rappel, tpl, cases):
    """Une phrase à trous, chaque trou avec sa bonne réponse et ses indices.

    `cases` : `(trou, étiquette, attendu, juste, ((faux, indice), …))`.
    La ligne du trou montre `attendu` pour le bon choix, l'indice du choix
    fait sinon.
    """
    blanks = {}
    for trou, label, attendu, juste, faux in cases:
        options = [Option("a", juste, _fixe(attendu))]
        options += [Option(chr(ord("b") + i), texte, _fixe(indice))
                    for i, (texte, indice) in enumerate(faux)]
        blanks[trou] = (label, options)
    lignes = [(trou, label) for trou, label, *_reste in cases]
    return Pattern(
        key=key,
        name=name,
        brief=brief,
        why="",
        tpl=tpl,
        blanks=blanks,
        ref={trou: "a" for trou in blanks},
        rows=lambda p, get: ["%s : %s" % (label, get(trou)(p))
                             for trou, label in lignes],
        lesson=(INTITULE,) + LECTURE_TROUS + tuple(rappel),
        level=level,
    )


def question(key, name, enonce, juste, explication, faux, level=2,
             rappel=()):
    """Une question à choix unique dont chaque erreur porte son indice."""
    choix = [juste] + [texte for texte, _indice in faux]
    pattern = qcm_pattern(key, 0, enonce, choix, 0, level, explication)
    label, options = pattern.blanks["choix"]
    indices = [None] + [indice for _texte, indice in faux]
    options = [o if indice is None
               else replace(o, note="Pas encore. %s" % indice)
               for o, indice in zip(options, indices)]
    return replace(pattern, name=name, blanks={"choix": (label, options)},
                   lesson=(INTITULE,) + tuple(rappel))


# --------------------------------------------------------------------------
# Séance 1 : humeur, météo, mots interrogatifs, présent
# --------------------------------------------------------------------------

METEO = trous(
    "all_u01_meteo", "Quel temps fait-il ?",
    "Complète la carte postale de Lena avec la météo de chaque jour.",
    1,
    ("Pour la météo, l'allemand dit souvent « es » : es regnet (il pleut), "
     "es schneit (il neige), es ist windig, es ist bewölkt. On dit aussi : "
     "die Sonne scheint, der Himmel ist blau / grau.",),
    """Liebe Oma,

am Montag: @t1@.
am Dienstag: @t2@.
am Mittwoch: @t3@.
am Donnerstag: @t4@.

Viele Grüße, deine Lena""",
    (
        ("t1", "Lundi", "il pleut",
         "es regnet",
         (("es schneit", "« es schneit » veut dire « il neige »"),
          ("es ist windig", "« windig » parle du vent, pas de la pluie"),
          ("die Sonne scheint", "« die Sonne scheint » : le soleil brille"))),
        ("t2", "Mardi", "il y a du vent",
         "es ist windig",
         (("es ist bewölkt", "« bewölkt » : le ciel est couvert de nuages"),
          ("es regnet", "« es regnet » veut dire « il pleut »"),
          ("es ist warm", "« warm » parle de la température : il fait "
                          "chaud"))),
        ("t3", "Mercredi", "le soleil brille",
         "die Sonne scheint",
         (("der Himmel ist grau", "un ciel gris n'annonce pas de soleil"),
          ("es schneit", "« es schneit » veut dire « il neige »"),
          ("es ist kalt", "« kalt » donne la température : il fait "
                          "froid"))),
        ("t4", "Jeudi", "le ciel est nuageux",
         "es ist bewölkt",
         (("es ist sonnig", "« sonnig » : il y a du soleil"),
          ("es ist windig", "« windig » parle du vent, pas des nuages"),
          ("der Himmel ist blau", "un ciel bleu est un ciel sans "
                                  "nuages"))),
    ),
)

HUMEUR = trous(
    "all_u01_humeur", "Wie geht's?",
    "Chacun dit comment il va, et quelle température il fait.",
    1,
    ("Pour dire comment on va : Mir geht's prima / gut / schlecht, ou "
     "Ich bin müde (fatigué), Ich bin traurig (triste).",
     "Pour la température : kalt (froid), warm (chaud), heiß (très "
     "chaud). Pense à l'anglais : cold, warm, hot. « ein bisschen » = un "
     "peu, « sehr » = très."),
    """Tim:   Mir geht's @h1@!
Julia: Ich bin @h2@.
Max:   Mir geht's @h3@.
Lili:  Es ist @h4@ kalt.
Sven:  Es ist sehr @h5@.""",
    (
        ("h1", "Tim", "je vais très bien",
         "prima",
         (("schlecht", "« schlecht » : ça va mal"),
          ("müde", "« müde » se dit avec « ich bin » : je suis fatigué"),
          ("traurig", "« traurig » : triste"))),
        ("h2", "Julia", "je suis fatiguée",
         "müde",
         (("traurig", "« traurig » veut dire triste, pas fatigué"),
          ("gut", "« gut » : bien — et on dirait « mir geht's gut »"),
          ("kalt", "« kalt » parle de la température, pas de la forme"))),
        ("h3", "Max", "ça ne va pas bien",
         "schlecht",
         (("gut", "« gut » : ça va bien, c'est le contraire"),
          ("prima", "« prima » : ça va très bien, c'est le contraire"),
          ("heiß", "« heiß » parle de la température : très chaud"))),
        ("h4", "Lili", "il fait un peu froid",
         "ein bisschen",
         (("sehr", "« sehr » veut dire « très », pas « un peu »"),
          ("nicht", "« nicht » est la négation : il ne fait pas froid"),
          ("zu", "« zu » veut dire « trop »"))),
        ("h5", "Sven", "il fait très chaud",
         "heiß",
         (("kalt", "« kalt » : froid — pense à l'anglais « cold »"),
          ("bewölkt", "« bewölkt » parle des nuages, pas de la "
                      "température"),
          ("windig", "« windig » parle du vent, pas de la température"))),
    ),
)

INTERROGATIFS = trous(
    "all_u01_fragen", "Les mots interrogatifs",
    "Lili interroge Max sur ses vacances. Complète ses questions.",
    1,
    ("Wer ? qui ? — Wo ? où ? — Wann ? quand ? — Was ? quoi, que ? — "
     "Wie ? comment ? — Mit wem ? avec qui ? — Wohin ? où (vers où) ?",
     "Attention aux faux amis : « wer » veut dire qui, et « wo » veut "
     "dire où."),
    """Lili: @f1@ bist du?          Max: In Österreich.
Lili: @f2@ bist du dort?   Max: Mit meiner Familie.
Lili: @f3@ ist das Wetter? Max: Es regnet.
Lili: @f4@ machst du?      Max: Ich lese viel.
Lili: @f5@ kommst du zurück? Max: Am 20. August.
Lili: @f6@ ist das?        Max: Das ist mein Bruder.""",
    (
        ("f1", "Question 1", "où es-tu ?",
         "Wo",
         (("Wer", "« Wer » demande qui : la réponse serait une personne"),
          ("Wohin", "« Wohin » demande où l'on va ; Max dit où il est"),
          ("Wann", "« Wann » demande quand : la réponse serait un "
                   "moment"))),
        ("f2", "Question 2", "avec qui es-tu là-bas ?",
         "Mit wem",
         (("Wer", "« Wer » demande qui ; la réponse commence par « mit »"),
          ("Wie", "« Wie » demande comment"),
          ("Was", "« Was » demande quoi"))),
        ("f3", "Question 3", "quel temps fait-il ?",
         "Wie",
         (("Was", "« Was ist das Wetter? » ne se dit pas : on demande "
                  "« comment » est le temps"),
          ("Wo", "« Wo » demande un lieu ; la réponse parle de météo"),
          ("Wer", "« Wer » demande qui : le temps n'est pas une "
                  "personne"))),
        ("f4", "Question 4", "que fais-tu ?",
         "Was",
         (("Wie", "« Wie » demande comment, pas quoi"),
          ("Wann", "« Wann » demande quand"),
          ("Wer", "« Wer » demande qui : faux ami, ce n'est pas "
                  "« what »"))),
        ("f5", "Question 5", "quand rentres-tu ?",
         "Wann",
         (("Wo", "« Wo » demande où ; la réponse est une date"),
          ("Wohin", "« Wohin » demande où l'on va ; la réponse est une "
                    "date"),
          ("Was", "« Was » demande quoi"))),
        ("f6", "Question 6", "qui est-ce ?",
         "Wer",
         (("Wo", "« Wo » demande où : faux ami, ce n'est pas « who »"),
          ("Was", "« Was » demande quoi, pour une chose ; ici c'est une "
                  "personne"),
          ("Wie", "« Wie » demande comment"))),
    ),
)

PRESENT = trous(
    "all_u01_present", "Le présent",
    "Conjugue les verbes au présent dans la carte postale de Hanna.",
    2,
    ("Au présent : ich -e, du -st, er/sie/es -t, wir -en, ihr -t, "
     "sie/Sie -en. Trouve d'abord le sujet, puis la terminaison qui va "
     "avec.",
     "sein et haben sont irréguliers : ich bin, du bist, er ist, wir "
     "sind, ihr seid, sie sind — ich habe, du hast, er hat, wir haben, "
     "ihr habt, sie haben."),
    """Hallo Lili!

Wir @p1@ (sein) an der Nordsee.
Mein Bruder @p2@ (schwimmen) jeden Tag.
Ich @p3@ (haben) ein Zimmer mit Blick aufs Meer.
Meine Eltern @p4@ (wandern) am Strand.
Und du, was @p5@ (machen) du?""",
    (
        ("p1", "1", "sein, avec « wir »",
         "sind",
         (("ist", "« ist » va avec er, sie, es : le sujet ici est "
                  "« wir »"),
          ("seid", "« seid » va avec « ihr » (vous), pas avec « wir »"),
          ("bin", "« bin » va avec « ich »"))),
        ("p2", "2", "schwimmen, avec « mein Bruder » (= er)",
         "schwimmt",
         (("schwimmen", "« schwimmen » est l'infinitif, ou la forme de "
                        "wir / sie (pluriel)"),
          ("schwimmst", "« -st » est la terminaison de « du »"),
          ("schwimme", "« -e » est la terminaison de « ich »"))),
        ("p3", "3", "haben, avec « ich »",
         "habe",
         (("hat", "« hat » va avec er, sie, es"),
          ("hast", "« hast » va avec « du »"),
          ("haben", "« haben » va avec wir ou sie (pluriel)"))),
        ("p4", "4", "wandern, avec « meine Eltern » (= sie, pluriel)",
         "wandern",
         (("wandert", "« -t » : er, sie, es ou ihr ; « meine Eltern » "
                      "sont plusieurs"),
          ("wanderst", "« -st » est la terminaison de « du »"),
          ("wandere", "« -e » est la terminaison de « ich »"))),
        ("p5", "5", "machen, avec « du »",
         "machst",
         (("macht", "« macht » va avec er, sie, es ou ihr"),
          ("mache", "« mache » va avec « ich »"),
          ("machen", "« machen » va avec wir ou sie (pluriel)"))),
    ),
)

Q_WER = question(
    "all_u01_q_wer", "Wer ? Wo ?",
    "Que veut dire la question « Wer fährt mit dir nach Berlin? » ?",
    "Qui va à Berlin avec toi ?",
    "« Wer » veut dire « qui » : c'est un faux ami, il ne correspond pas à "
    "l'anglais « where ».",
    (("Où vas-tu à Berlin avec lui ?",
      "« Wer » ressemble à l'anglais « where », mais c'est un faux ami. "
      "« Où » se dit « wo »."),
     ("Quand vas-tu à Berlin ?", "« Quand » se dit « wann »."),
     ("Comment vas-tu à Berlin ?", "« Comment » se dit « wie ».")),
    level=1,
)

Q_KARTE = question(
    "all_u01_q_karte", "La carte postale",
    "Tu écris une carte postale à ton ami Jonas. Comment la commences-tu ?",
    "Lieber Jonas,",
    "On écrit « lieber » à un garçon et « liebe » à une fille. Pour finir "
    "la carte : « Bis bald! » ou « Viele Grüße! ».",
    (("Liebe Jonas,", "« Liebe » s'adresse à une fille. Jonas est-il une "
                      "fille ?"),
     ("Bis bald, Jonas,", "« Bis bald » veut dire « à bientôt » : on "
                          "l'écrit à la fin de la carte, pas au début."),
     ("Viele Grüße, Jonas,", "« Viele Grüße » sert à finir la carte "
                             "(amitiés), pas à la commencer.")),
    level=1,
)


# --------------------------------------------------------------------------
# Séances 1 et 2 : activités de vacances, lieux, opinion
# --------------------------------------------------------------------------

ACTIVITES_1 = trous(
    "all_u01_activites_mer", "À la mer, à la montagne",
    "Dis ce que chacun fait en vacances.",
    1,
    ("In den Bergen : Ski fahren, wandern, klettern, Schlittschuh laufen.",
     "Am Meer : schwimmen / baden, sich sonnen, segeln, surfen, rudern, "
     "lesen."),
    """In den Bergen:
  Paul möchte @a1@.
  Mia möchte @a2@.
Am Meer:
  Emil möchte @a3@.
  Lea möchte @a4@.""",
    (
        ("a1", "Paul", "faire de l'escalade",
         "klettern",
         (("wandern", "« wandern » : faire de la randonnée"),
          ("Ski fahren", "« Ski fahren » : faire du ski"),
          ("Schlittschuh laufen", "« Schlittschuh laufen » : faire du "
                                  "patin à glace"))),
        ("a2", "Mia", "faire de la randonnée",
         "wandern",
         (("klettern", "« klettern » : faire de l'escalade"),
          ("reiten", "« reiten » : faire de l'équitation"),
          ("joggen", "« joggen » : faire du jogging"))),
        ("a3", "Emil", "faire de la voile",
         "segeln",
         (("surfen", "« surfen » : faire du surf ou de la planche à "
                     "voile, pas du bateau à voile"),
          ("rudern", "« rudern » : faire du canoë ou du kayak"),
          ("schwimmen", "« schwimmen » : nager"))),
        ("a4", "Lea", "bronzer",
         "sich sonnen",
         (("schwimmen", "« schwimmen » : nager"),
          ("lesen", "« lesen » : lire"),
          ("sich entspannen", "« sich entspannen » : se détendre, pas "
                              "bronzer"))),
    ),
)

ACTIVITES_2 = trous(
    "all_u01_activites_ville", "À la campagne, en ville",
    "Dis ce que chacun fait en vacances.",
    1,
    ("Auf dem Land : reiten, angeln / fischen, Rad fahren, joggen, sich "
     "entspannen, zelten.",
     "In der Stadt : ins Kino gehen, ins Konzert gehen, ein Museum "
     "besichtigen, shoppen, tanzen, Bowling spielen."),
    """Auf dem Land:
  Opa geht @b1@.
  Wir gehen @b2@.
In der Stadt:
  Anna geht @b3@.
  Ben geht @b4@.""",
    (
        ("b1", "Opa", "à la pêche",
         "angeln",
         (("reiten", "« reiten » : faire de l'équitation"),
          ("zelten", "« zelten » : faire du camping"),
          ("joggen", "« joggen » : faire du jogging"))),
        ("b2", "Nous", "faire de l'équitation",
         "reiten",
         (("Rad fahren", "« Rad fahren » : faire du vélo"),
          ("wandern", "« wandern » : faire de la randonnée"),
          ("angeln", "« angeln » : pêcher"))),
        ("b3", "Anna", "au cinéma",
         "ins Kino",
         (("ins Konzert", "« ins Konzert » : au concert"),
          ("ins Museum", "« ins Museum » : au musée"),
          ("ins Schwimmbad", "« ins Schwimmbad » : à la piscine"))),
        ("b4", "Ben", "danser",
         "tanzen",
         (("shoppen", "« shoppen » : faire du shopping"),
          ("schwimmen", "« schwimmen » : nager"),
          ("Bowling spielen", "« Bowling spielen » : jouer au "
                              "bowling"))),
    ),
)

Q_WO_SEGELN = question(
    "all_u01_q_ort", "Où faire quoi ?",
    "Wo kannst du segeln und surfen?",
    "Am Meer",
    "On fait de la voile et du surf à la mer : am Meer.",
    (("In den Bergen", "« In den Bergen » : à la montagne. Y a-t-il des "
                       "vagues et du vent de mer ?"),
     ("In der Stadt", "« In der Stadt » : en ville. Où trouve-t-on de "
                      "l'eau et du vent pour un bateau ?"),
     ("Auf dem Land", "« Auf dem Land » : à la campagne. « segeln » se "
                      "pratique sur l'eau, en général sur la mer.")),
    level=1,
)

Q_LAND = question(
    "all_u01_q_land", "Les prépositions de lieu",
    "Comment dit-on « à la campagne » ?",
    "auf dem Land",
    "On dit « auf dem Land » (littéralement « sur la campagne »), comme "
    "« auf der Insel » (sur l'île). Retiens aussi : in der Stadt, in den "
    "Bergen, am Meer.",
    (("in dem Land", "La préposition est étonnante pour un Français : "
                     "relis la règle des lieux de vacances. « in » sert "
                     "pour la ville et la montagne."),
     ("am Land", "« am » (= an dem) sert pour la mer : am Meer. Pour la "
                 "campagne, c'est une autre préposition."),
     ("in den Land", "« den » est un datif pluriel (in den Bergen) ; "
                     "« Land » est ici neutre singulier.")),
    level=2,
)

AVIS = trous(
    "all_u01_avis", "Donner son avis",
    "Chacun donne son avis sur une activité. Complète avec l'adjectif "
    "qui convient.",
    1,
    ("Avis positif : prima, toll, super, cool, gut, interessant.",
     "Avis négatif : anstrengend (fatigant), langweilig (ennuyeux), "
     "doof / blöd (nul), schrecklich (horrible), uninteressant."),
    """Wandern finde ich @o1@!
Museen besichtigen finde ich @o2@.
Joggen finde ich @o3@.
Ski fahren finde ich @o4@!""",
    (
        ("o1", "Randonnée", "c'est horrible",
         "schrecklich",
         (("langweilig", "« langweilig » : ennuyeux, moins fort "
                         "qu'horrible"),
          ("toll", "« toll » est un avis positif"),
          ("anstrengend", "« anstrengend » : fatigant"))),
        ("o2", "Musées", "c'est ennuyeux",
         "langweilig",
         (("interessant", "« interessant » est un avis positif"),
          ("anstrengend", "« anstrengend » : fatigant"),
          ("blöd", "« blöd » : nul, idiot"))),
        ("o3", "Jogging", "c'est fatigant",
         "anstrengend",
         (("schrecklich", "« schrecklich » : horrible"),
          ("doof", "« doof » : nul, idiot"),
          ("cool", "« cool » est un avis positif"))),
        ("o4", "Ski", "c'est super",
         "toll",
         (("doof", "« doof » est un avis négatif : nul"),
          ("langweilig", "« langweilig » est un avis négatif : "
                         "ennuyeux"),
          ("anstrengend", "« anstrengend » : fatigant, un avis "
                          "plutôt négatif"))),
    ),
)

Q_POSITIF = question(
    "all_u01_q_avis", "Positif ou négatif ?",
    "Lequel de ces adjectifs exprime un avis **positif** ?",
    "prima",
    "« prima » (= toll, super) exprime un avis positif.",
    (("langweilig", "« langweilig » veut dire ennuyeux : c'est négatif."),
     ("blöd", "« blöd » (= doof) veut dire nul, idiot : c'est négatif."),
     ("anstrengend", "« anstrengend » veut dire fatigant : ce n'est pas "
                     "un compliment.")),
    level=1,
)


# --------------------------------------------------------------------------
# Séance 2 : la place du verbe, le locatif, les pays de langue allemande
# --------------------------------------------------------------------------

REGLE_VERBE = (
    "Dans une phrase déclarative, le verbe conjugué est toujours en "
    "**2e position**. Si un autre élément occupe la 1re place (Heute, Am "
    "Montag, Mit dem Bus…), le sujet passe en 3e position.",
)

Q_VERBE_1 = question(
    "all_u01_q_verbe1", "La place du verbe (1)",
    "Quelle phrase est correcte ?",
    "Heute fahren wir nach Berlin.",
    "« Heute » occupe la 1re position, le verbe « fahren » la 2e, et le "
    "sujet « wir » passe en 3e position.",
    (("Heute wir fahren nach Berlin.",
      "Compte les positions : « Heute » est la 1re. Qu'est-ce qui doit "
      "venir juste après ?"),
     ("Heute wir nach Berlin fahren.",
      "Le verbe conjugué ne va pas à la fin dans une phrase déclarative : "
      "il a une place fixe."),
     ("Fahren heute wir nach Berlin.",
      "Un verbe en 1re position, c'est une question, pas une phrase "
      "déclarative.")),
    level=2, rappel=REGLE_VERBE,
)

Q_VERBE_2 = question(
    "all_u01_q_verbe2", "La place du verbe (2)",
    "Remets les éléments en ordre : « Jeden Morgen … / joggt / meine "
    "Schwester ». Quelle phrase obtiens-tu ?",
    "Jeden Morgen joggt meine Schwester.",
    "Le complément de temps « Jeden Morgen » est en 1re position, le verbe "
    "« joggt » en 2e, le sujet en 3e.",
    (("Jeden Morgen meine Schwester joggt.",
      "La phrase est construite comme en français. Où se place le verbe "
      "conjugué en allemand ?"),
     ("Jeden Morgen meine Schwester joggen.",
      "Deux erreurs : « joggen » n'est pas conjugué, et le verbe n'est "
      "pas à sa place."),
     ("Joggt jeden Morgen meine Schwester.",
      "Verbe en 1re position : c'est la forme d'une question. On veut une "
      "phrase déclarative qui commence par « Jeden Morgen ».")),
    level=2, rappel=REGLE_VERBE,
)

LOCATIF = trous(
    "all_u01_locatif", "Où es-tu ? Le locatif",
    "Lili dit où se trouvent ses amis. Complète avec la bonne forme de "
    "« in ».",
    3,
    ("Pour dire où l'on est : in + nom de ville ou de pays sans article "
     "(in Berlin, in Deutschland).",
     "Pays, régions et lieux avec article : in + datif. Masculin et "
     "neutre : in dem = im ; féminin : in der ; pluriel : in den."),
    """Sven ist @l1@ Schweiz (die Schweiz).
Meine Tante wohnt @l2@ Elsass (das Elsass).
Julia ist @l3@ Berlin.
Meine Cousine wohnt @l4@ USA (die USA, pluriel).
Wir wandern @l5@ Bergen (die Berge, pluriel).""",
    (
        ("l1", "Sven", "en Suisse",
         "in der",
         (("in", "« die Schweiz » a un article : après « in », il faut "
                 "le datif de cet article"),
          ("im", "« im » = in dem, pour un mot masculin ou neutre ; "
                 "« Schweiz » est féminin"),
          ("in den", "« in den » est le datif pluriel ; « Schweiz » est "
                     "féminin singulier"))),
        ("l2", "Tante", "en Alsace",
         "im",
         (("in der", "« in der » est pour un mot féminin ; « Elsass » "
                     "est neutre"),
          ("in", "« das Elsass » a un article : il faut le datif de cet "
                 "article"),
          ("in den", "« in den » est le datif pluriel ; « Elsass » est "
                     "singulier"))),
        ("l3", "Julia", "à Berlin",
         "in",
         (("in der", "une ville s'emploie sans article : pas de datif à "
                     "ajouter"),
          ("nach", "« nach » dit où l'on va ; ici Julia y est déjà"),
          ("im", "une ville s'emploie sans article : pas de « dem » "
                 "caché"))),
        ("l4", "Cousine", "aux États-Unis",
         "in den",
         (("in der", "« in der » est pour un mot féminin singulier ; "
                     "« die USA » est un pluriel"),
          ("in", "« die USA » a un article : il faut le datif pluriel"),
          ("im", "« im » est pour un masculin ou un neutre singulier"))),
        ("l5", "Nous", "à la montagne",
         "in den",
         (("in der", "« in der » est le datif féminin singulier ; « die "
                     "Berge » est un pluriel"),
          ("auf den", "pour la montagne, la préposition est « in » ; "
                      "« auf » sert pour la campagne (auf dem Land)"),
          ("am", "« am » sert pour la mer (am Meer)"))),
    ),
)

Q_PAYS = question(
    "all_u01_q_pays", "Où parle-t-on allemand ?",
    "Dans lequel de ces pays l'allemand n'est-il **pas** une langue "
    "officielle ?",
    "aux Pays-Bas",
    "L'allemand est langue officielle en Allemagne, en Autriche et au "
    "Liechtenstein, et l'une des langues officielles en Suisse, en "
    "Belgique, au Luxembourg et dans le Tyrol du Sud (Italie). Les "
    "Pays-Bas parlent néerlandais.",
    (("en Belgique", "En Belgique, l'allemand est l'une des langues "
                     "officielles, à côté du français et du néerlandais."),
     ("au Luxembourg", "Le Luxembourg a trois langues officielles : le "
                       "luxembourgeois, le français… et la troisième ?"),
     ("en Suisse", "La Suisse a plusieurs langues officielles, et la "
                   "majorité de ses habitants parle allemand.")),
    level=2,
)

Q_PAYS_SEUL = question(
    "all_u01_q_seule", "Langue officielle unique",
    "Dans quel pays l'allemand est-il la **seule** langue officielle ?",
    "en Autriche",
    "L'allemand est langue officielle unique en Allemagne, en Autriche et "
    "au Liechtenstein.",
    (("en Suisse", "La Suisse a plusieurs langues officielles : "
                   "l'allemand, mais aussi le français, l'italien…"),
     ("en Belgique", "En Belgique, l'allemand partage ce rôle avec le "
                     "français et le néerlandais."),
     ("au Luxembourg", "Le Luxembourg a trois langues officielles.")),
    level=2,
)


# --------------------------------------------------------------------------
# Séance 3 : le directif (nach), la préposition mit et le datif
# --------------------------------------------------------------------------

IN_NACH = trous(
    "all_u01_in_nach", "in ou nach ?",
    "Nora raconte ses projets. Complète avec « in » ou « nach ».",
    2,
    ("Wo? (où l'on est) : in + ville ou pays → Ich bin in Wien.",
     "Wohin? (où l'on va) : nach + ville ou pays sans article → Ich fahre "
     "nach Wien. Les verbes fahren, fliegen, gehen indiquent un "
     "déplacement ; wohnen, sein, bleiben une position fixe.",
     "Un pays avec article prend « in » + accusatif pour la direction : "
     "Ich fahre in die Schweiz."),
    """Ich wohne @d1@ Lyon.
Morgen fliege ich @d2@ Österreich.
@d3@ Wien besichtige ich das Hundertwasserhaus.
Dann fahre ich @d4@ Schweiz.
Am Ende fahre ich zurück @d5@ Frankreich.""",
    (
        ("d1", "1", "j'habite à Lyon",
         "in",
         (("nach", "« nach » indique une direction ; « wohnen » "
                   "exprime-t-il un déplacement ?"),
          ("in die", "« in die » + accusatif indique une direction, et "
                     "une ville n'a pas d'article"),
          ("am", "« am » sert pour la mer (am Meer)"))),
        ("d2", "2", "je vais (en avion) en Autriche",
         "nach",
         (("in", "« in Österreich » dit où l'on est ; « fliegen » est "
                 "un déplacement"),
          ("in die", "« Österreich » s'emploie sans article : pas de "
                     "« in die »"),
          ("mit", "« mit » veut dire « avec »"))),
        ("d3", "3", "à Vienne (j'y suis déjà)",
         "In",
         (("Nach", "Nora est déjà à Vienne quand elle visite : ce n'est "
                   "pas une direction"),
          ("Mit", "« mit » veut dire « avec »"),
          ("Am", "« am » sert pour la mer"))),
        ("d4", "4", "je vais en Suisse",
         "in die",
         (("nach", "« nach » s'emploie avec un nom de pays sans "
                   "article ; « die Schweiz » en a un"),
          ("in der", "« in der » + datif dit où l'on est ; ici on y "
                     "va"),
          ("in", "il manque l'article de « die Schweiz »"))),
        ("d5", "5", "je rentre en France",
         "nach",
         (("in", "« zurückfahren » est un déplacement : où va-t-elle ?"),
          ("in die", "« Frankreich » s'emploie sans article"),
          ("mit", "« mit » veut dire « avec »"))),
    ),
)

Q_WOHIN = question(
    "all_u01_q_wohin", "Wo ? Wohin ?",
    "Réponse : « Ich fahre nach Salzburg. » Quelle était la question ?",
    "Wohin fährst du?",
    "« nach Salzburg » dit où l'on va : la question est « Wohin? ».",
    (("Wo bist du?", "« Wo » demande où l'on est. La réponse parle-t-elle "
                     "d'une position, ou d'un trajet ?"),
     ("Wann fährst du?", "« Wann » demande quand ; la réponse ne donne "
                         "aucun moment."),
     ("Mit wem fährst du?", "« Mit wem » demande avec qui ; la réponse ne "
                            "nomme personne.")),
    level=2,
)

MIT_DATIF = trous(
    "all_u01_mit", "mit + datif",
    "La classe part en voyage. Complète avec l'article au datif.",
    2,
    ("La préposition « mit » (avec) est toujours suivie du **datif**.",
     "Datif : masculin der → dem, neutre das → dem, féminin die → der, "
     "pluriel die → den (et le nom prend souvent un -n)."),
    """Wir fahren mit @m1@ Bus (der Bus).
Ich sitze mit @m2@ Freundin Emma (die Freundin).
Herr Weber kommt mit @m3@ Auto (das Auto).
Wir wandern mit @m4@ deutschen Schülern (die Schüler, pluriel).""",
    (
        ("m1", "Bus", "datif masculin",
         "dem",
         (("der", "« der » est le datif du féminin ; « Bus » est "
                  "masculin"),
          ("den", "« den » est le datif pluriel"),
          ("die", "après « mit », pas de nominatif : il faut le datif"))),
        ("m2", "Freundin", "datif féminin",
         "meiner",
         (("meinem", "« -em » est la marque du masculin et du neutre ; "
                     "« Freundin » est féminin"),
          ("meine", "« meine » n'est pas un datif : « mit » demande le "
                    "datif"),
          ("meinen", "« -en » est la marque du datif pluriel"))),
        ("m3", "Auto", "datif neutre",
         "dem",
         (("das", "« das » n'est pas un datif : « mit » demande le "
                  "datif"),
          ("der", "« der » est le datif du féminin ; « Auto » est "
                  "neutre"),
          ("den", "« den » est le datif pluriel"))),
        ("m4", "Schülern", "datif pluriel",
         "den",
         (("dem", "« dem » est le datif singulier masculin ou neutre ; "
                  "ici c'est un pluriel"),
          ("der", "« der » est le datif féminin singulier"),
          ("die", "« die » n'est pas un datif"))),
    ),
)

DATIF_FIN = trous(
    "all_u01_datif", "Les marques du datif",
    "Une journée en ville. Complète chaque mot avec la marque du datif.",
    3,
    ("Après « mit » et après « in » (lieu où l'on est), on emploie le "
     "datif.",
     "Marques du datif : -em au masculin et au neutre, -er au féminin, "
     "-en au pluriel (dem / einem / seinem, der / einer / seiner, den / "
     "seinen)."),
    """Tom verbringt den Tag mit sein@e1@ Freund Paul (der Freund).
Sie kaufen Brot in ein@e2@ Bäckerei (die Bäckerei).
Dann picknicken sie in d@e3@ Park (der Park).
Am Abend essen sie mit d@e4@ Eltern (die Eltern, pluriel).""",
    (
        ("e1", "Freund", "datif masculin",
         "em",
         (("er", "« -er » est la marque du féminin ; « Freund » est "
                 "masculin"),
          ("en", "« -en » est la marque du pluriel"),
          ("e", "il manque la marque du datif"))),
        ("e2", "Bäckerei", "datif féminin",
         "er",
         (("em", "« -em » est la marque du masculin et du neutre ; "
                 "« Bäckerei » est féminin"),
          ("en", "« -en » est la marque du pluriel"),
          ("e", "il manque la marque du datif"))),
        ("e3", "Park", "datif masculin",
         "em",
         (("er", "« -er » est la marque du féminin ; « Park » est "
                 "masculin"),
          ("en", "« -en » est la marque du pluriel"),
          ("ie", "« die » n'est pas un datif"))),
        ("e4", "Eltern", "datif pluriel",
         "en",
         (("em", "« -em » est la marque du singulier masculin ou "
                 "neutre ; « Eltern » est un pluriel"),
          ("er", "« -er » est la marque du féminin singulier"),
          ("ie", "« die » n'est pas un datif"))),
    ),
)


# --------------------------------------------------------------------------
# Séance 4 : les possessifs, les verbes forts en -a et en -e
# --------------------------------------------------------------------------

POSSESSIFS = trous(
    "all_u01_possessifs", "Les possessifs",
    "Avec qui chacun passe-t-il ses vacances ? Complète avec le "
    "possessif.",
    3,
    ("1. Qui possède ? ich → mein, du → dein, er → sein, sie (elle) → "
     "ihr, wir → unser, ihr → euer, sie (ils) → ihr.",
     "2. Quel genre, quel nombre a le nom ? 3. Après « mit », datif : "
     "-em (masculin, neutre), -er (féminin), -en (pluriel).",
     "Au singulier, le possessif dépend du possesseur : « sein » pour un "
     "garçon, « ihr » pour une fille — comme his / her en anglais."),
    """Lili spielt mit @s1@ Bruder (der Bruder).
Tim ist mit @s2@ Cousinen (die Cousinen, pluriel).
Ich bin mit @s3@ Familie (die Familie).
Und du, bist du mit @s4@ Eltern (die Eltern, pluriel)?
Wir sind mit @s5@ Hund (der Hund).""",
    (
        ("s1", "Lili", "son frère (à elle)",
         "ihrem",
         (("seinem", "« sein » renvoie à un possesseur masculin ; Lili "
                     "est une fille"),
          ("ihrer", "le bon possesseur, mais « -er » est la marque du "
                    "féminin ; « Bruder » est masculin"),
          ("ihr", "il manque la marque du datif après « mit »"))),
        ("s2", "Tim", "ses cousines (à lui)",
         "seinen",
         (("ihren", "« ihr » renvoie à une possesseuse ; Tim est un "
                    "garçon"),
          ("seiner", "le bon possesseur, mais « -er » est le datif "
                     "féminin singulier ; ici c'est un pluriel"),
          ("seine", "« seine » n'est pas un datif : « mit » le "
                    "demande"))),
        ("s3", "Moi", "ma famille",
         "meiner",
         (("meinem", "« -em » est la marque du masculin et du neutre ; "
                     "« Familie » est féminin"),
          ("deiner", "« dein » veut dire « ton » ; qui parle ici ?"),
          ("meine", "« meine » n'est pas un datif : « mit » le "
                    "demande"))),
        ("s4", "Toi", "tes parents",
         "deinen",
         (("deinem", "« -em » est la marque du singulier ; « Eltern » "
                     "est un pluriel"),
          ("meinen", "« mein » veut dire « mon, mes » ; Lili parle à "
                     "« du »"),
          ("deiner", "« -er » est le datif féminin singulier"))),
        ("s5", "Nous", "notre chien",
         "unserem",
         (("unserer", "« -er » est la marque du féminin ; « Hund » est "
                      "masculin"),
          ("eurem", "« euer » veut dire « votre » ; le sujet est "
                    "« wir »"),
          ("unseren", "« -en » est la marque du datif pluriel"))),
    ),
)

Q_POSSESSIF = question(
    "all_u01_q_ihr", "sein ou ihr ?",
    "Comment dit-on « Julia est avec son père » ?",
    "Julia ist mit ihrem Vater.",
    "Le possesseur est Julia, une fille : « ihr ». « Vater » est masculin, "
    "et « mit » demande le datif : -em.",
    (("Julia ist mit seinem Vater.",
      "En français « son » ne dit pas qui possède. En allemand, si : à "
      "qui est le père ?"),
     ("Julia ist mit ihrer Vater.",
      "Le possesseur est juste, mais « -er » est la marque du féminin. "
      "Quel est le genre de « Vater » ?"),
     ("Julia ist mit ihr Vater.",
      "« mit » est toujours suivi du datif : il manque une terminaison.")),
    level=3,
)

FORTS = trous(
    "all_u01_forts", "Les verbes forts",
    "Leo et Lisa partent en voyage. Conjugue les verbes au présent.",
    2,
    ("Verbes forts en -a : le a devient ä à la 2e et 3e personne du "
     "singulier (fahren → du fährst, er fährt ; schlafen, tragen, "
     "laufen).",
     "Verbes forts en -e : le e devient i ou ie à la 2e et 3e personne du "
     "singulier (essen → er isst ; lesen → er liest ; helfen → er hilft ; "
     "nehmen → er nimmt).",
     "Aux autres personnes (ich, wir, ihr, sie), la voyelle ne change "
     "pas."),
    """Leo @v1@ (fahren) mit dem Auto nach Berlin.
Er @v2@ (essen) ein Sandwich.
Lisa @v3@ (lesen) ein Buch.
Du @v4@ (schlafen) im Auto.
Leo @v5@ (tragen) die Koffer.
Lisa @v6@ (helfen) ihm.""",
    (
        ("v1", "1", "fahren, avec « er »",
         "fährt",
         (("fahrt", "à la 3e personne du singulier, la voyelle d'un "
                    "verbe fort en -a change ; « fahrt » est la forme de "
                    "« ihr »"),
          ("fährst", "« -st » est la terminaison de « du »"),
          ("fahren", "c'est l'infinitif, ou la forme de wir / sie"))),
        ("v2", "2", "essen, avec « er »",
         "isst",
         (("esst", "« esst » est la forme de « ihr » : à « er », le e "
                   "d'un verbe fort change"),
          ("ist", "« ist » vient du verbe sein (être), pas de essen"),
          ("esse", "« esse » est la forme de « ich »"))),
        ("v3", "3", "lesen, avec « sie » (Lisa)",
         "liest",
         (("lest", "« lest » est la forme de « ihr » : à « sie » (elle), "
                   "le e devient « ie »"),
          ("lese", "« lese » est la forme de « ich »"),
          ("lesen", "c'est l'infinitif, ou la forme de wir / sie "
                    "(pluriel)"))),
        ("v4", "4", "schlafen, avec « du »",
         "schläfst",
         (("schlafst", "à « du », la voyelle d'un verbe fort en -a "
                       "change"),
          ("schläft", "« schläft » est la forme de er, sie, es ; "
                      "« du » prend « -st »"),
          ("schlaft", "« schlaft » est la forme de « ihr »"))),
        ("v5", "5", "tragen, avec « er »",
         "trägt",
         (("tragt", "« tragt » est la forme de « ihr » : à « er », le a "
                    "devient ä"),
          ("trägst", "« -st » est la terminaison de « du »"),
          ("trage", "« trage » est la forme de « ich »"))),
        ("v6", "6", "helfen, avec « sie » (Lisa)",
         "hilft",
         (("helft", "« helft » est la forme de « ihr » : à « sie » "
                    "(elle), le e d'un verbe fort change"),
          ("hilfst", "« -st » est la terminaison de « du »"),
          ("helfe", "« helfe » est la forme de « ich »"))),
    ),
)

Q_FORTS = question(
    "all_u01_q_nehmen", "nehmen",
    "Complète : « Lisa ____ ihre Tasche. » (nehmen, au présent)",
    "nimmt",
    "nehmen est un verbe fort en -e : er / sie / es nimmt (attention, le h "
    "disparaît et le m double).",
    (("nehmt", "« nehmt » est la forme de « ihr ». À « sie » (elle), un "
               "verbe fort en -e change de voyelle."),
     ("nimmst", "« -st » est la terminaison de « du ». Le sujet ici est "
                "« Lisa »."),
     ("nehme", "« nehme » est la forme de « ich ».")),
    level=3,
)

Q_DENN = question(
    "all_u01_q_denn", "Lier ses phrases",
    "« Ich bade nicht, ____ das Wasser ist zu kalt. » Quel mot de liaison "
    "donne le sens « car » ?",
    "denn",
    "« denn » veut dire « car ». Comme und, oder et aber, il ne change pas "
    "l'ordre des mots : « das Wasser ist… ».",
    (("aber", "« aber » veut dire « mais » : il oppose, il n'explique "
              "pas."),
     ("oder", "« oder » veut dire « ou » : il propose un choix."),
     ("dann", "« dann » veut dire « ensuite » : il indique l'ordre des "
              "actions, pas une cause.")),
    level=2,
)

Q_ZUERST = question(
    "all_u01_q_zuerst", "Raconter dans l'ordre",
    "Quelle phrase est correcte ?",
    "Zuerst fährt Diana zu ihren Großeltern.",
    "« Zuerst » occupe la 1re position : le verbe conjugué vient en 2e, le "
    "sujet en 3e. « Diana » est une fille : « ihren Großeltern ».",
    (("Zuerst Diana fährt zu ihren Großeltern.",
      "Après un connecteur de temps en 1re position, où se place le "
      "verbe conjugué ?"),
     ("Zuerst fährt Diana zu seinen Großeltern.",
      "L'ordre des mots est juste. Mais à qui sont les grands-parents ? "
      "Diana est une fille."),
     ("Zuerst fahrt Diana zu ihren Großeltern.",
      "« fahrt » est la forme de « ihr ». fahren est un verbe fort en -a : "
      "que devient sa voyelle à la 3e personne ?")),
    level=3, rappel=REGLE_VERBE,
)


# --------------------------------------------------------------------------
# Séance 6 : sein et haben au prétérit
# --------------------------------------------------------------------------

PRETERIT = trous(
    "all_u01_preterit", "sein et haben au prétérit",
    "Sven raconte ses vacances, terminées. Complète avec sein ou haben "
    "au prétérit.",
    2,
    ("sein au prétérit : ich war, du warst, er/sie/es war, wir waren, "
     "ihr wart, sie/Sie waren.",
     "haben au prétérit : ich hatte, du hattest, er/sie/es hatte, wir "
     "hatten, ihr hattet, sie/Sie hatten.",
     "Le récit est au passé : les formes du présent (bin, ist, habe, "
     "hat…) ne conviennent pas."),
    """Hi Lili,
ich @r1@ (sein) in Liechtenstein bei meinem Onkel.
Wir @r2@ (haben) tolles Wetter.
Die Berge @r3@ (sein) sehr hoch.
Und du, @r4@ (haben) du schöne Ferien?
Bis bald, Sven""",
    (
        ("r1", "1", "sein au prétérit, avec « ich »",
         "war",
         (("bin", "« bin » est au présent ; les vacances sont "
                  "terminées"),
          ("waren", "« waren » va avec wir ou sie (pluriel)"),
          ("warst", "« warst » va avec « du »"))),
        ("r2", "2", "haben au prétérit, avec « wir »",
         "hatten",
         (("haben", "« haben » est au présent ; le récit est au passé"),
          ("hatte", "« hatte » va avec ich ou er, sie, es"),
          ("hattet", "« hattet » va avec « ihr »"))),
        ("r3", "3", "sein au prétérit, avec « die Berge » (= sie, "
                    "pluriel)",
         "waren",
         (("war", "« war » va avec ich ou er, sie, es ; « die Berge » "
                  "est un pluriel"),
          ("sind", "« sind » est au présent"),
          ("wart", "« wart » va avec « ihr »"))),
        ("r4", "4", "haben au prétérit, avec « du »",
         "hattest",
         (("hast", "« hast » est au présent"),
          ("hatte", "« hatte » va avec ich ou er, sie, es"),
          ("hattet", "« hattet » va avec « ihr »"))),
    ),
)

Q_PRETERIT = question(
    "all_u01_q_hattet", "Hattet ihr…?",
    "Que veut dire « Hattet ihr schöne Ferien? » ?",
    "Vous aviez de belles vacances ?",
    "« hattet » est le prétérit de haben avec « ihr » (vous, plusieurs "
    "amis) : c'est une question au passé.",
    (("Avez-vous de belles vacances ?", "Le verbe est-il au présent ? "
                                        "Le présent serait « habt »."),
     ("Étiez-vous en vacances ?", "« hattet » vient de haben (avoir), "
                                  "pas de sein (être)."),
     ("Avais-tu de belles vacances ?", "« ihr » ne veut pas dire « tu » : "
                                       "on s'adresse à plusieurs "
                                       "personnes.")),
    level=2,
)


# --------------------------------------------------------------------------
# Séances 7 à 9 : le parfait
# --------------------------------------------------------------------------

PARTICIPES = trous(
    "all_u01_participes", "Le participe passé",
    "Ben raconte sa journée. Choisis le participe passé de chaque verbe.",
    3,
    ("Verbes faibles : ge + radical + t (spielen → gespielt, machen → "
     "gemacht, zelten → gezeltet).",
     "Verbes forts : ge + radical (qui peut changer) + en (essen → "
     "gegessen, lesen → gelesen, treffen → getroffen, finden → "
     "gefunden).",
     "Dans la phrase, l'auxiliaire est en 2e position et le participe "
     "passé à la fin."),
    """Ich habe Fußball @g1@ (spielen).
Dann habe ich eine Pizza @g2@ (essen).
Ich habe meine Freunde @g3@ (treffen).
Wir haben ein Picknick @g4@ (machen).
Am Abend habe ich ein Buch @g5@ (lesen).""",
    (
        ("g1", "spielen", "verbe faible",
         "gespielt",
         (("gespielen", "spielen est un verbe faible : son participe ne "
                        "finit pas en -en"),
          ("spielt", "il manque le « ge- » du participe passé"),
          ("gespielte", "il y a une lettre de trop à la fin"))),
        ("g2", "essen", "verbe fort",
         "gegessen",
         (("gesst", "essen est un verbe fort : son participe finit en "
                    "-en"),
          ("geesst", "essen est un verbe fort : son participe finit en "
                     "-en, pas en -t"),
          ("gessen", "le participe commence par « ge- », suivi de tout "
                     "le radical « ess- »"))),
        ("g3", "treffen", "verbe fort",
         "getroffen",
         (("getrefft", "treffen est un verbe fort : participe en -en, et "
                       "sa voyelle change"),
          ("getreffen", "la terminaison est juste, mais la voyelle du "
                        "radical change ; regarde la liste des verbes "
                        "forts"),
          ("getrifft", "« trifft » est la forme du présent (er trifft), "
                       "pas le participe"))),
        ("g4", "machen", "verbe faible",
         "gemacht",
         (("gemachen", "machen est un verbe faible : participe en -t"),
          ("macht", "il manque le « ge- » du participe passé"),
          ("gemächt", "machen est un verbe faible : sa voyelle ne change "
                      "pas"))),
        ("g5", "lesen", "verbe fort",
         "gelesen",
         (("gelest", "lesen est un verbe fort : participe en -en"),
          ("geliest", "« liest » est la forme du présent (er liest) ; le "
                      "participe garde ici la voyelle de l'infinitif"),
          ("lesen", "c'est l'infinitif : il manque le « ge- »"))),
    ),
)

AUXILIAIRE = trous(
    "all_u01_auxiliaire", "haben ou sein ?",
    "Les amis de Lili racontent leurs vacances au parfait. Choisis "
    "l'auxiliaire.",
    3,
    ("Au parfait, la plupart des verbes prennent **haben**.",
     "Les verbes de **déplacement** prennent **sein** : gehen, fahren, "
     "fliegen, kommen, schwimmen, reiten, wandern, klettern… À retenir "
     "aussi : ich bin zu Hause geblieben.",
     "Attention : le français ne suit pas toujours la même règle (« nous "
     "avons randonné » → wir sind gewandert)."),
    """Max @x1@ nach Wien gefahren.
Wir @x2@ viel gewandert.
Julia @x3@ viele Museen besichtigt.
Ich @x4@ zu Hause geblieben.
Tim @x5@ ein Eis gegessen.""",
    (
        ("x1", "Max", "Max est allé à Vienne",
         "ist",
         (("hat", "« fahren » exprime un déplacement : quel auxiliaire "
                  "prennent ces verbes ?"),
          ("sind", "le bon auxiliaire, mais « sind » va avec un sujet "
                   "pluriel ; « Max » est seul"),
          ("habe", "« habe » va avec « ich », et l'auxiliaire n'est pas "
                   "le bon"))),
        ("x2", "Nous", "nous avons fait beaucoup de randonnée",
         "sind",
         (("haben", "le français dit « nous avons », mais « wandern » "
                    "est un déplacement : en allemand, l'auxiliaire "
                    "change"),
          ("ist", "le bon auxiliaire, mais « ist » va avec er, sie, "
                  "es ; le sujet est « wir »"),
          ("hat", "« wandern » est un déplacement, et « hat » ne va pas "
                  "avec « wir »"))),
        ("x3", "Julia", "Julia a visité beaucoup de musées",
         "hat",
         (("ist", "« besichtigen » (visiter) n'exprime pas un "
                  "déplacement"),
          ("haben", "le bon auxiliaire, mais « haben » va avec un sujet "
                    "pluriel"),
          ("sind", "« besichtigen » n'exprime pas un déplacement, et "
                   "« sind » est un pluriel"))),
        ("x4", "Moi", "je suis resté à la maison",
         "bin",
         (("habe", "« bleiben » est l'exception à retenir : il ne "
                   "s'agit pas d'un déplacement, et pourtant…"),
          ("ist", "le bon auxiliaire, mais « ist » va avec er, sie, es"),
          ("hat", "« bleiben » est une exception, et « hat » ne va pas "
                  "avec « ich »"))),
        ("x5", "Tim", "Tim a mangé une glace",
         "hat",
         (("ist", "« essen » (manger) n'exprime pas un déplacement"),
          ("hatte", "« hatte » est le prétérit : au parfait, "
                    "l'auxiliaire est au présent"),
          ("habe", "« habe » va avec « ich » ; le sujet est « Tim »"))),
    ),
)

Q_PARFAIT_ORDRE = question(
    "all_u01_q_gestern", "La phrase au parfait",
    "Quelle phrase est correcte ?",
    "Gestern habe ich meine Freunde getroffen.",
    "« Gestern » en 1re position, l'auxiliaire « habe » en 2e, le sujet "
    "en 3e, et le participe passé à la fin.",
    (("Gestern ich habe meine Freunde getroffen.",
      "Après « Gestern » en 1re position, qu'est-ce qui vient en 2e ?"),
     ("Gestern habe ich getroffen meine Freunde.",
      "L'auxiliaire est bien placé. Mais où va le participe passé dans "
      "une phrase au parfait ?"),
     ("Gestern bin ich meine Freunde getroffen.",
      "« treffen » (rencontrer) n'exprime pas un déplacement : quel "
      "auxiliaire prend-il ?")),
    level=3,
)

Q_ANRUFEN = question(
    "all_u01_q_anrufen", "Verbes à particule",
    "Quel est le participe passé de « an/rufen » (appeler au téléphone) ?",
    "angerufen",
    "Verbe à particule séparable : « ge- » se place entre la particule et "
    "le radical : an-ge-rufen.",
    (("geanrufen", "Pour un verbe à particule séparable, « ge- » ne se "
                   "place pas devant la particule."),
     ("angeruft", "rufen est un verbe fort : son participe finit en -en."),
     ("anrufen", "C'est l'infinitif : il manque « ge- ».")),
    level=3,
)

Q_IEREN = question(
    "all_u01_q_ieren", "Verbes en -ieren",
    "« Ich habe mit meiner Oma ____. » (telefonieren, au parfait)",
    "telefoniert",
    "Les verbes en -ieren ne prennent pas « ge- » : on enlève -en et on "
    "ajoute -t. telefonieren → telefoniert.",
    (("getelefoniert", "Les verbes en -ieren ont une particularité au "
                       "parfait : ils ne prennent pas un élément que "
                       "prennent les autres verbes."),
     ("telefonieren", "C'est l'infinitif : le participe passé a une "
                      "autre terminaison."),
     ("telefonierte", "Il y a une lettre de trop à la fin.")),
    level=3,
)

Q_BEKOMMEN = question(
    "all_u01_q_bekommen", "Préfixes inséparables",
    "« Ich habe von Tim ein Geschenk ____. » (bekommen, au parfait)",
    "bekommen",
    "Les verbes à préfixe inséparable (be-, ent-, er-, ver-, zer-, emp-, "
    "ge-, miss-) ne prennent pas « ge- » : bekommen → bekommen.",
    (("gebekommen", "« be- » est un préfixe inséparable : ces verbes ne "
                    "prennent pas d'élément en plus au participe."),
     ("bekommt", "« bekommt » est le présent (er bekommt) ; après « habe », "
                 "il faut le participe passé."),
     ("gekommen", "« gekommen » vient de « kommen » (venir) : le préfixe "
                  "« be- » a disparu, et le sens avec.")),
    level=3,
)

Q_WEIL = question(
    "all_u01_q_weil", "Le parfait après weil",
    "Lili explique son retard : « …, weil wir so lange über unsere "
    "Ferien ____. »",
    "geredet haben",
    "Dans une subordonnée avec « weil », le verbe conjugué (ici "
    "l'auxiliaire) va tout à la fin, juste après le participe passé.",
    (("haben geredet", "Dans une subordonnée introduite par « weil », "
                       "l'ordre n'est pas celui d'une phrase "
                       "déclarative. Où va le verbe conjugué ?"),
     ("geredet hat", "L'ordre est juste, mais le sujet est « wir »."),
     ("geredet sind", "L'ordre est juste, mais « reden » (parler) "
                      "n'exprime pas un déplacement.")),
    level=4,
)


PATTERNS = (
    METEO, HUMEUR, INTERROGATIFS, Q_WER, PRESENT, Q_KARTE,
    ACTIVITES_1, ACTIVITES_2, Q_WO_SEGELN, Q_LAND, AVIS, Q_POSITIF,
    Q_VERBE_1, Q_VERBE_2, LOCATIF, Q_PAYS, Q_PAYS_SEUL,
    IN_NACH, Q_WOHIN, MIT_DATIF, DATIF_FIN,
    POSSESSIFS, Q_POSSESSIF, FORTS, Q_FORTS, Q_DENN, Q_ZUERST,
    PRETERIT, Q_PRETERIT,
    PARTICIPES, AUXILIAIRE, Q_PARFAIT_ORDRE, Q_ANRUFEN, Q_IEREN, Q_BEKOMMEN,
    Q_WEIL,
)

MODULE = Module(
    key="allemand_u01",
    title="Unité 1 — Ferien in den DACH-Ländern",
    level=2,
    summary="Révisions de l'unité 1 : météo, activités de vacances, place "
            "du verbe, in / nach / mit et le datif, possessifs, verbes "
            "forts, prétérit de sein et haben, parfait. " + INTITULE,
    keys=tuple(p.key for p in PATTERNS),
)
