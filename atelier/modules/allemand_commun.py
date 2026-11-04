"""Ce que les modules du chapitre Allemand ont en commun.

Deux formes d'exercice, et dans les deux un **accompagnement** qui oriente
sans donner la réponse :

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

Chaque module passe son intitulé (« Exercices de révision de l'unité
n… ») en premier argument des deux fabriques. L'élève est tutoyé, comme
dans le cours.
"""

from dataclasses import replace

from ..engine import Option, Pattern, qcm_pattern


def intitule(unite):
    return ("Exercices de révision de l'unité %d. Si ta réponse est fausse, "
            "un indice t'explique ton erreur sans te donner la solution : "
            "relis-le, puis corrige." % unite)


LECTURE_TROUS = (
    "Pour chaque trou, la **cible** (« Motif à reproduire ») dit ce que "
    "la phrase doit exprimer. Choisis dans chaque menu le mot qui convient.",
    "Une ligne en rouge est un indice sur ton erreur : compare-la à la "
    "ligne attendue, puis corrige ton choix.",
)


def _fixe(texte):
    return lambda _params: texte


def trous(intitule, key, name, brief, level, rappel, tpl, cases):
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
        lesson=(intitule,) + LECTURE_TROUS + tuple(rappel),
        level=level,
        per_blank=True,
    )


def question(intitule, key, name, enonce, juste, explication, faux, level=2,
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
                   lesson=(intitule,) + tuple(rappel))
