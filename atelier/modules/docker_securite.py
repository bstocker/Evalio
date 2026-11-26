"""Module « Sécurisation Docker », du chapitre Docker.

La séance « Sécurité et audit des images » : scanner les dépendances et
les images avec Trivy, durcir le Dockerfile (utilisateur non root,
propriétaire des fichiers, `.dockerignore`, build multi-étapes,
HEALTHCHECK), puis faire échouer le pipeline CI/CD quand une faille
grave est trouvée.

Les exercices montrent une **session de terminal**, comme au chapitre
Linux : on y lit le Dockerfile (`cat Dockerfile`), la construction, puis
la commande dont la sortie est à reproduire. La construction est rendue
muette (`-q`, `>/dev/null`) : elle n'affiche qu'un identifiant d'image
différent à chaque fois.

Chaque sortie a été relevée en construisant réellement les images sur
`python:3.13.8-slim-trixie`, la base du Dockerfile corrigé de la séance,
et en lançant Trivy 0.76 sur les dépendances de l'atelier.
"""

from dataclasses import replace

from ..engine import (Module, Pattern, _opts, debug_pattern, predict_from,
                      qcm_pattern)
from .linux_commun import lecon, predire
from .qcm_docker import _tourner

BASE = "python:3.13.8-slim-trixie"

# La construction ne dit rien d'utile : un identifiant d'image, différent
# à chaque fois. On la fait taire.
BUILD = "$ docker build -q -t app . >/dev/null"

CONSTRUCTION = (
    "`docker build -q -t app . >/dev/null` construit l'image `app` sans "
    "rien afficher : `-q` réduit la sortie à l'identifiant de l'image, et "
    "`>/dev/null` le jette.",
)


def _liste(noms):
    """Les noms d'un dossier dans l'ordre où `ls` les range dans l'image.

    L'image ne règle aucune langue : `ls` y trie octet par octet, les
    noms à point d'abord, les majuscules avant les minuscules.
    """
    return sorted(noms)


# --------------------------------------------------------------------------
# Ne pas tourner en root
# --------------------------------------------------------------------------

IDS = {
    "appuser": "uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)",
    "root": "uid=0(root) gid=0(root) groups=0(root)",
    "nobody": "uid=65534(nobody) gid=65534(nogroup) groups=65534(nogroup)",
    "www-data": "uid=33(www-data) gid=33(www-data) groups=33(www-data)",
}

UTILISATEUR = Pattern(
    key="dk_secu_user",
    name="Ne pas tourner en root",
    brief="Faire tourner l'application sous le compte créé pour elle, et "
          "non sous root.",
    why="Sans instruction USER, tout conteneur tourne en root.",
    lesson=lecon(
        "Par défaut, un conteneur exécute sa commande en **root**. Une "
        "faille dans l'application donne alors tous les droits à "
        "l'attaquant, dans le conteneur.",
        "`RUN useradd -m appuser` crée un compte ; `USER appuser` le fait "
        "endosser à toutes les instructions qui suivent, et à la commande "
        "du conteneur.",
        "`id` affiche l'utilisateur courant et son groupe, avec leurs "
        "numéros : root porte toujours le numéro 0.",
    ) + CONSTRUCTION,
    tpl="""$ cat Dockerfile
FROM %s
WORKDIR /app
RUN useradd -m appuser
COPY . /app
USER @user@
CMD ["python", "main.py"]
%s
$ docker run --rm app id""" % (BASE, BUILD),
    blanks={
        "user": ("Compte sous lequel tourne le conteneur", _opts(
            ("a", "appuser", lambda p: IDS["appuser"]),
            ("b", "root", lambda p: IDS["root"]),
            ("c", "nobody", lambda p: IDS["nobody"]),
            ("d", "www-data", lambda p: IDS["www-data"]),
        )),
    },
    ref={"user": "a"},
    rows=lambda p, get: [get("user")(p)],
    level=1,
)


# --------------------------------------------------------------------------
# Donner ses fichiers à l'application
# --------------------------------------------------------------------------

FICHIERS = (
    ("main.py", "requirements.txt"),
    ("app.py", "requirements.txt"),
    ("config.py", "main.py", "requirements.txt"),
    ("main.py", "requirements.txt", "wsgi.py"),
)


def _proprietaires(qui):
    """Sortie de `stat -c '%U:%G %n' . <fichiers>` dans /app.

    `.` est le dossier /app : WORKDIR le crée en root, avant même que le
    compte appuser n'existe, et aucun COPY n'y change rien.
    """
    def rows(p):
        return ["root:root ."] + ["%s %s" % (qui, f) for f in p["fichiers"]]
    return rows


PROPRIETAIRE = Pattern(
    key="dk_secu_chown",
    name="Donner ses fichiers à l'application",
    brief="Copier le code dans l'image en le donnant à appuser et à son "
          "groupe, qui exécutent le conteneur.",
    why="COPY écrit en root, sauf si on lui dit à qui donner les fichiers.",
    lesson=lecon(
        "`COPY` et `ADD` écrivent les fichiers en **root:root**, même "
        "quand un `USER` vient plus bas : l'ordre des instructions n'y "
        "change rien.",
        "`COPY --chown=utilisateur:groupe` donne les fichiers copiés à ce "
        "compte et à ce groupe.",
        "`stat -c '%U:%G %n'` affiche le propriétaire, le groupe puis le "
        "nom de chaque fichier. `.` désigne le dossier courant, ici /app.",
    ) + CONSTRUCTION,
    dims=(("g", 0, 3),),
    derive=lambda p: {"fichiers": FICHIERS[p["g"]],
                      "noms": " ".join(FICHIERS[p["g"]])},
    tpl="""$ cat Dockerfile
FROM %s
WORKDIR /app
RUN useradd -m appuser
@copie@
USER appuser
CMD ["python", "main.py"]
%s
$ docker run --rm app stat -c '%%U:%%G %%n' . @noms@""" % (BASE, BUILD),
    blanks={
        "copie": ("Copie du code", _opts(
            ("a", "COPY --chown=appuser:appuser . /app",
             _proprietaires("appuser:appuser")),
            ("b", "COPY . /app", _proprietaires("root:root")),
            ("c", "ADD . /app", _proprietaires("root:root")),
            ("d", "COPY --chown=appuser:root . /app",
             _proprietaires("appuser:root")),
        )),
    },
    ref={"copie": "a"},
    rows=lambda p, get: get("copie")(p),
    level=2,
)


# --------------------------------------------------------------------------
# Garder les secrets hors de l'image
# --------------------------------------------------------------------------

# Ce que le dossier du projet contient en plus du strict nécessaire.
EXTRAS = ((), ("config.py",), ("templates",), ("static",))

PROJET = (".env", ".git", "Dockerfile", "main.py", "requirements.txt")


def _projet(p):
    noms = _liste(PROJET + EXTRAS[p["g"]])
    return {"noms": noms, "avant": "  ".join(noms)}


def _copies(exclus):
    """Ce que `ls -A` montre dans /app quand `exclus` reste dehors."""
    def rows(p):
        return _liste([n for n in p["noms"] + [".dockerignore"]
                       if n not in exclus])
    return rows


DOCKERFILE_COPIE = """$ cat Dockerfile
FROM %s
WORKDIR /app
COPY . /app
CMD ["python", "main.py"]""" % BASE

IGNORER = Pattern(
    key="dk_secu_dockerignore",
    name="Garder les secrets hors de l'image",
    brief="Écrire le .dockerignore pour que ni le fichier de mots de passe "
          ".env, ni l'historique .git n'entrent dans l'image.",
    why="COPY . copie tout le dossier, fichiers cachés compris.",
    lesson=lecon(
        "`COPY . /app` copie **tout** le dossier du projet, fichiers "
        "cachés compris : un `.env` plein de mots de passe finit dans "
        "l'image, lisible par quiconque la récupère.",
        "Le dossier `.git` aussi : il garde tout l'historique, y compris "
        "les secrets effacés depuis.",
        "`.dockerignore`, à côté du Dockerfile, liste un motif par ligne. "
        "Ce qui correspond reste hors de l'image.",
        "`printf` remplace chaque `\\n` par un retour à la ligne.",
    ) + CONSTRUCTION,
    dims=(("g", 0, 3),),
    derive=_projet,
    tpl="""$ ls -A
@avant@
%s
$ printf '@motifs@' > .dockerignore
%s
$ docker run --rm app ls -A""" % (DOCKERFILE_COPIE, BUILD),
    blanks={
        "motifs": ("Contenu du .dockerignore", _opts(
            ("a", ".env\\n.git\\n", _copies((".env", ".git"))),
            ("b", ".git\\n", _copies((".git",))),
            ("c", ".env\\n", _copies((".env",))),
            ("d", "env\\n.git\\n", _copies((".git",))),
        )),
    },
    ref={"motifs": "a"},
    rows=lambda p, get: get("motifs")(p),
    level=3,
)


# --------------------------------------------------------------------------
# Laisser le compilateur à l'étape de build
# --------------------------------------------------------------------------

FLASK = "Version: 3.1.2"
SANS_FLASK = "WARNING: Package(s) not found: flask"


def _multi(p, get):
    """Ce que montre `which gcc; pip show flask | grep Version`.

    L'image finale part de `de` et reçoit `copie` de l'étape build. gcc
    n'est que dans l'étape build ; Flask y est installé à part, dans
    /install, et ne sert que s'il est recopié dans /usr/local.
    """
    de, copie = get("de")(p), get("copie")(p)
    lignes = []
    if de == "build" or copie == "gcc":
        lignes.append("/usr/bin/gcc")
    if de == "debian":
        lignes.append("sh: 1: pip: not found")
    elif copie == "install":
        lignes.append(FLASK)
    else:
        lignes.append(SANS_FLASK)
    return lignes


MULTI_ETAPES = Pattern(
    key="dk_secu_multistage",
    name="Laisser le compilateur à l'étape de build",
    brief="Construire en deux étapes : l'image finale doit avoir Flask, "
          "mais pas gcc.",
    why="Un outil de compilation oublié dans l'image est un outil de plus "
        "pour un attaquant.",
    lesson=lecon(
        "Un Dockerfile **multi-étapes** a plusieurs `FROM`. Seule la "
        "dernière étape devient l'image ; les autres ne servent qu'à "
        "préparer des fichiers.",
        "`FROM … AS build` nomme une étape. `COPY --from=build source "
        "destination` y prend des fichiers.",
        "`pip install --prefix=/install` installe les paquets à part, "
        "dans /install : ils ne servent que recopiés là où Python les "
        "cherche, dans /usr/local.",
        "`which gcc` affiche le chemin de gcc s'il est installé, et rien "
        "sinon. `pip show flask | grep Version` affiche la version de "
        "Flask ; sans Flask, pip le signale.",
    ) + CONSTRUCTION,
    tpl="""$ cat Dockerfile
FROM %s AS build
RUN apt-get update && apt-get install -y --no-install-recommends gcc
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM @de@
COPY @copie@
WORKDIR /app
COPY . /app
CMD ["python", "main.py"]
$ cat requirements.txt
Flask==3.1.2
%s
$ docker run --rm app sh -c 'which gcc; pip show flask | grep Version'"""
        % (BASE, BUILD),
    blanks={
        "de": ("Base de l'image finale", _opts(
            ("a", BASE, lambda p: "slim"),
            ("b", "build", lambda p: "build"),
            ("c", "debian:trixie-slim", lambda p: "debian"),
        )),
        "copie": ("Ce que l'image finale reprend de l'étape build", _opts(
            ("a", "--from=build /install /usr/local", lambda p: "install"),
            ("b", "--from=build /install /install", lambda p: "ailleurs"),
            ("c", "--from=build /usr/bin/gcc /usr/bin/gcc",
             lambda p: "gcc"),
        )),
    },
    ref={"de": "a", "copie": "a"},
    rows=_multi,
    level=4,
)


# --------------------------------------------------------------------------
# Diagnostic
# --------------------------------------------------------------------------

COMPTES = ("appuser", "flaskuser", "webapp", "svc")


# Le rappel de `debug_pattern` suppose un programme ; ici l'élève lit une
# session, dont la dernière commande produit les deux sorties comparées.
LECTURE_BUG = ("Le bloc ci-dessous est une **session de terminal** : les "
               "lignes qui commencent par `$` sont les commandes tapées, les "
               "autres ce qu'elles ont affiché. Les deux sorties comparées "
               "sont celles de la **dernière** commande.",)


def _session(pattern):
    """Ajoute la lecture d'une session au rappel d'un diagnostic."""
    return replace(pattern, lesson=LECTURE_BUG + pattern.lesson)


BUG_SU = _session(debug_pattern(
    key="dk_secu_bug_su",
    name="Bug : l'application tourne encore en root",
    but="faire tourner l'application sous le compte créé pour elle",
    defaut="`RUN su` ne change d'utilisateur que le temps de son RUN ; "
           "il fallait USER",
    sujet="Ce Dockerfile",
    dims=(("g", 0, 3),),
    derive=lambda p: {"compte": COMPTES[p["g"]]},
    tpl="""$ cat Dockerfile
FROM %s
WORKDIR /app
RUN useradd -m @compte@
COPY --chown=@compte@:@compte@ . /app
RUN su @compte@
CMD ["python", "main.py"]
%s
$ docker run --rm app whoami""" % (BASE, BUILD),
    attendu=lambda p: [p["compte"]],
    obtenu=lambda _p: ["root"],
    diagnostics=(
        ("a", "`RUN su` ne change d'utilisateur que pendant son propre "
              "RUN : l'instruction suivante repart en root. Il fallait "
              "l'instruction `USER`.",
         "Exact. Chaque RUN lance un shell neuf, qui se termine avec "
         "lui : le `su` meurt avec son RUN. `USER` est la seule "
         "instruction qui change l'utilisateur de la suite et du "
         "conteneur."),
        ("b", "`useradd -m` crée un compte sans droit de connexion : `su` "
              "ne peut pas l'utiliser.",
         "Non : `-m` crée le dossier personnel du compte, rien de plus. "
         "La construction passe d'ailleurs sans erreur."),
        ("c", "`COPY --chown` a rendu les fichiers à root, et le "
              "conteneur suit le propriétaire de ses fichiers.",
         "Non : `--chown` donne bien les fichiers au compte. Et le "
         "propriétaire des fichiers ne décide jamais de l'utilisateur "
         "du conteneur."),
        ("d", "`whoami` affiche le compte qui a construit l'image, pas "
              "celui qui fait tourner le conteneur.",
         "Non : `whoami` affiche l'utilisateur du processus en cours, "
         "dans le conteneur. C'est bien root qui le lance."),
    ),
    bonne="a",
    level=2,
))


BUG_IGNORE = _session(debug_pattern(
    key="dk_secu_bug_ignore",
    name="Bug : le fichier de mots de passe dans l'image",
    but="garder .env et .git hors de l'image",
    defaut="le fichier s'appelle dockerignore, sans le point : Docker ne "
           "le lit pas",
    sujet="Ce projet",
    dims=(("g", 0, 3),),
    derive=lambda p: {
        "avant": "  ".join(_liste(PROJET + EXTRAS[p["g"]]
                                  + ("dockerignore",))),
        "noms": _liste(PROJET + EXTRAS[p["g"]]),
    },
    tpl="""$ ls -A
@avant@
$ cat dockerignore
.env
.git
.dockerignore
%s
%s
$ docker run --rm app ls -A""" % (DOCKERFILE_COPIE, BUILD),
    attendu=lambda p: [n for n in p["noms"] if n not in (".env", ".git")],
    obtenu=lambda p: _liste(p["noms"] + ["dockerignore"]),
    diagnostics=(
        ("a", "Le fichier s'appelle `dockerignore` : sans le point de "
              "tête, Docker ne le lit pas et copie tout le dossier.",
         "Exact. Docker ne cherche que `.dockerignore`, avec son point. "
         "Un fichier au nom approchant n'est qu'un fichier de plus, "
         "copié avec le reste."),
        ("b", "`COPY .` copie toujours les fichiers cachés, quoi que dise "
              "le .dockerignore.",
         "Non : un `.dockerignore` bien nommé écarte aussi les fichiers "
         "cachés. C'est même son premier usage."),
        ("c", "Il faut écrire `*.env` : un motif sans étoile ne correspond "
              "à aucun fichier.",
         "Non : un motif sans étoile désigne exactement ce nom. `.env` "
         "écarte le fichier .env."),
        ("d", "`docker build` a réutilisé une ancienne copie en cache : il "
              "fallait `--no-cache`.",
         "Non : même reconstruite de zéro, l'image recevrait le même "
         "dossier, car rien ne l'a filtré."),
    ),
    bonne="a",
    level=3,
))


# (port de l'application, port que le HEALTHCHECK interroge)
PORTS = ((4000, 5000), (5000, 4000), (8000, 8080), (8080, 8000))

BUG_SANTE = _session(debug_pattern(
    key="dk_secu_bug_sante",
    name="Bug : le contrôle de santé de l'application",
    but="déclarer le conteneur en bonne santé (healthy) une fois "
        "l'application lancée",
    defaut="le HEALTHCHECK interroge un autre port que celui de "
           "l'application",
    sujet="Ce Dockerfile",
    dims=(("g", 0, 3),),
    derive=lambda p: {"port": PORTS[p["g"]][0], "sonde": PORTS[p["g"]][1]},
    tpl="""$ cat Dockerfile
FROM %s
WORKDIR /app
RUN apt-get update && \\
    apt-get install -y --no-install-recommends curl && \\
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m appuser
COPY --chown=appuser:appuser . /app
USER appuser
EXPOSE @port@
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
  CMD curl -f http://localhost:@sonde@/ || exit 1
CMD ["python", "main.py", "--port", "@port@"]
%s
$ docker run -d --name web app >/dev/null
$ sleep 120
$ docker inspect --format '{{.State.Health.Status}}' web""" % (BASE, BUILD),
    attendu=lambda _p: ["healthy"],
    obtenu=lambda _p: ["unhealthy"],
    diagnostics=(
        ("a", "Le HEALTHCHECK interroge un autre port que celui sur "
              "lequel l'application écoute.",
         "Exact. L'application écoute sur le port passé à `--port` ; "
         "curl frappe à une autre porte, où personne ne répond. Après "
         "trois échecs, Docker déclare le conteneur unhealthy."),
        ("b", "curl n'est pas installé dans l'image.",
         "Non : le premier RUN l'installe. Sans lui, la sonde échouerait "
         "aussi, mais ce n'est pas le cas ici."),
        ("c", "Il manque `-p` à `docker run` : sans port publié, la sonde "
              "ne peut pas joindre l'application.",
         "Non : la sonde tourne **dans** le conteneur, et `localhost` y "
         "désigne le conteneur lui-même. `-p` ne sert qu'aux visiteurs "
         "venus de la machine."),
        ("d", "`sleep 120` ne suffit pas : le conteneur est encore en "
              "période de démarrage.",
         "Non : la période de démarrage ne dure que 10 s, et il se dirait "
         "alors « starting », pas « unhealthy »."),
    ),
    bonne="a",
    level=3,
))


# Dépendances de l'atelier : chaque jeu contient au moins une faille HIGH
# ou CRITICAL selon Trivy (pymysql 0.6.7 : CVE-2024-36039, CRITICAL ;
# cryptography 2.1.4 : six failles HIGH).
DEPENDANCES = (
    ("cryptography==2.1.4", "pymysql==0.6.7"),
    ("Flask==3.1.2", "pymysql==0.6.7"),
    ("cryptography==2.1.4", "Flask==3.1.2"),
    ("cryptography==2.1.4", "psycopg2-binary==2.6.2", "pymysql==0.6.7"),
)

TRIVY = ('docker run --rm -v "$PWD":/project '
         '-v "$HOME/.cache/trivy":/root/.cache/ aquasec/trivy:latest')

BUG_GATE = _session(debug_pattern(
    key="dk_secu_bug_gate",
    name="Bug : le job de dépendances qui laisse tout passer",
    but="échouer (code de retour non nul) dès que Trivy trouve une faille "
        "HIGH ou CRITICAL, pour bloquer le pipeline",
    defaut="sans `--exit-code 1`, Trivy rend 0 même quand il trouve des "
           "failles",
    sujet="Ce job",
    dims=(("g", 0, 3),),
    derive=lambda p: {"deps": "\n".join(DEPENDANCES[p["g"]])},
    tpl="""$ cat requirements.txt
@deps@
$ %s fs --severity HIGH,CRITICAL /project/requirements.txt >/dev/null
$ echo $?""" % TRIVY,
    attendu=lambda _p: ["1"],
    obtenu=lambda _p: ["0"],
    diagnostics=(
        ("a", "Il manque `--exit-code 1` : sans cette option, Trivy rend 0 "
              "même quand il trouve des failles.",
         "Exact. Par défaut Trivy **signale** sans **juger** : son code de "
         "retour reste 0. `--exit-code 1` le fait échouer dès qu'une faille "
         "du niveau demandé est trouvée, et le job avec lui."),
        ("b", "`>/dev/null` jette le code de retour avec l'affichage.",
         "Non : `>/dev/null` ne jette que ce que la commande écrit. Le "
         "code de retour, lui, arrive intact dans `$?`."),
        ("c", "`--severity HIGH,CRITICAL` écarte les failles CRITICAL.",
         "Non : la liste garde les deux niveaux, HIGH **et** CRITICAL."),
        ("d", "Les versions sont épinglées avec `==` : Trivy ne sait pas "
              "les analyser.",
         "C'est l'inverse : `==` donne à Trivy la version exacte à "
         "confronter aux failles connues. Ce sont les `>=` qu'il ne peut "
         "pas juger."),
    ),
    bonne="a",
    level=4,
))


# --------------------------------------------------------------------------
# Prédiction
# --------------------------------------------------------------------------

PREDIRE_USER = predict_from(
    UTILISATEUR,
    key="dk_secu_predire_user",
    name="Prédire : qui fait tourner le conteneur",
    why="USER décide de l'identité du conteneur.",
    level=2,
    output_format=("uid=XXXX(XXXX) gid=XXXX(XXXX) groups=XXXX(XXXX)",),
    lesson=predire(UTILISATEUR),
)

PREDIRE_CHOWN = predict_from(
    PROPRIETAIRE,
    key="dk_secu_predire_chown",
    name="Prédire : à qui sont les fichiers de /app",
    why="COPY --chown ne donne que ce qu'il copie.",
    level=3,
    output_format=("<propriétaire>:<groupe> .",
                   "<propriétaire>:<groupe> <fichier>",
                   "…"),
    lesson=predire(PROPRIETAIRE),
)

PREDIRE_IGNORE = predict_from(
    IGNORER,
    key="dk_secu_predire_ignore",
    name="Prédire : ce qui entre dans l'image",
    why="Le .dockerignore filtre ce que COPY . emporte.",
    level=3,
    output_format=("<un nom par ligne, dans l'ordre de ls>",),
    lesson=predire(IGNORER),
)

PREDIRE_MULTI = predict_from(
    MULTI_ETAPES,
    key="dk_secu_predire_multistage",
    name="Prédire : ce que garde l'image finale",
    why="Seule la dernière étape devient l'image.",
    level=4,
    output_format=("<une ligne par résultat : chemin trouvé, version, ou "
                   "message de pip>",),
    lesson=predire(MULTI_ETAPES),
)


# --------------------------------------------------------------------------
# Questions de cours
# --------------------------------------------------------------------------

# (énoncé, (quatre propositions), index de la bonne, niveau, explication)
# Comme dans qcm_docker, la bonne réponse est écrite en premier puis
# déplacée par `_tourner`.
QUESTIONS = (
    ("Qu'est-ce qu'un SBOM ?",
     ("L'inventaire des bibliothèques, avec leurs versions, qui composent "
      "une image ou une application",
      "La liste des failles corrigées dans la dernière version d'une "
      "image",
      "Le fichier qui décrit comment construire une image",
      "Le rapport de Trivy une fois les failles graves écartées"),
     0, 1,
     "SBOM pour *Software Bill of Materials* : la nomenclature du "
     "logiciel. C'est elle que Trivy confronte aux bases de failles "
     "connues (CVE)."),

    ("Dans le Dockerfile de départ de l'atelier, qu'est-ce qui pose "
     "problème avec `FROM python:3.7` ?",
     ("Cette version n'est plus maintenue : ses failles ne sont plus "
      "corrigées",
      "Python 3.7 ne sait pas faire tourner Flask",
      "Une image Python ne peut pas servir de base à un Dockerfile",
      "Le numéro de version empêche Docker de télécharger l'image"),
     0, 1,
     "Une base ancienne embarque des paquets que plus personne ne "
     "corrige. Le Dockerfile corrigé part d'une version récente et "
     "allégée : `%s`." % BASE),

    ("Quelle commande analyse les dépendances déclarées dans "
     "`requirements.txt`, sans construire d'image ?",
     ("trivy fs /project/requirements.txt",
      "trivy image /project/requirements.txt",
      "docker build -t requirements.txt .",
      "docker scan requirements.txt"),
     0, 2,
     "`fs` (*filesystem*) analyse des fichiers ; `image` analyse une "
     "image déjà construite. Lancé dans un conteneur, Trivy lit le "
     "dossier monté avec `-v \"$PWD\":/project`."),

    ("Pourquoi préférer `COPY` à `ADD` pour mettre le code dans l'image ?",
     ("`ADD` sait aussi télécharger une URL et décompresser une archive : "
      "il peut faire entrer plus que prévu",
      "`COPY` chiffre les fichiers pendant la copie",
      "`ADD` ne copie que les fichiers cachés",
      "`COPY` vérifie les failles des fichiers qu'il copie"),
     0, 2,
     "`COPY` ne fait qu'une chose : copier depuis le dossier du projet. "
     "`ADD` en fait davantage, sans contrôle, d'où la règle de la "
     "checklist : COPY, avec `--chown`."),

    ("Dans le job `Dockerfile` du pipeline, on lit `needs: Dependances`. "
     "Que se passe-t-il si Trivy fait échouer le job `Dependances` ?",
     ("Le job Dockerfile n'est pas lancé, ni Deploy qui attend Dockerfile : "
      "rien n'est déployé",
      "Le job Dockerfile se lance quand même, mais en mode avertissement",
      "GitHub relance Dependances jusqu'à ce qu'il réussisse",
      "Deploy se lance directement, puisque Dockerfile n'a pas échoué"),
     0, 2,
     "`needs` enchaîne les jobs : chacun attend la réussite du précédent. "
     "C'est le *gating* : une faille grave arrête la chaîne avant le "
     "déploiement."),

    ("Pourquoi vider `/var/lib/apt/lists/*` dans **le même** `RUN` que "
     "`apt-get install` ?",
     ("Chaque RUN ajoute une couche : effacé dans un RUN suivant, le "
      "cache resterait stocké dans la couche précédente",
      "apt-get refuse d'installer un second paquet tant que le cache "
      "est plein",
      "Le cache contient les mots de passe de l'utilisateur root",
      "Sinon Trivy ne peut pas lire les paquets installés"),
     0, 3,
     "Une couche ne s'efface pas : un RUN suivant ne fait que masquer "
     "les fichiers, qui pèsent toujours dans l'image. Installer et "
     "nettoyer dans le même RUN, c'est ne jamais les écrire dans une "
     "couche."),

    ("Le `requirements.txt` de l'atelier déclare `Flask>=1.1.2`, "
     "`Jinja2>=2.11.2`… et Trivy n'y signale rien. Pourquoi s'en méfier ?",
     ("Les versions ne sont pas épinglées : Trivy ne sait pas laquelle "
      "sera installée, et ne peut pas la confronter aux failles connues",
      "Trivy ne connaît pas les paquets Python",
      "Trivy ignore les fichiers qui s'appellent requirements.txt",
      "Le scan ne regarde que les failles CRITICAL"),
     0, 3,
     "Avec `>=`, aucune version précise n'est écrite : le fichier n'est "
     "pas analysé. Épinglées avec `==`, comme dans "
     "`database-requirements.txt`, les mêmes dépendances révèlent leurs "
     "failles. D'où la règle : épingler les versions critiques."),

    ("Pour analyser l'image `imgvulne:1.1` avec Trivy lancé dans un "
     "conteneur, pourquoi ajoute-t-on "
     "`-v /var/run/docker.sock:/var/run/docker.sock` ?",
     ("Pour que Trivy joigne le démon Docker de la machine, qui détient "
      "l'image construite",
      "Pour que Trivy puisse publier l'image sur Docker Hub",
      "Pour enregistrer le rapport dans le dossier courant",
      "Pour garder en cache la base des failles entre deux scans"),
     0, 3,
     "L'image n'existe que dans le démon Docker de la machine. Monter "
     "son socket donne à Trivy, enfermé dans son conteneur, le moyen de "
     "la demander. Le cache, lui, est le second `-v`, vers "
     "`/root/.cache/`."),
)


def _question(rang, question, choices, answer, level, explanation):
    choices, answer = _tourner(choices, answer, rang)
    return qcm_pattern("dk_secu_q%02d" % rang, rang, question,
                       choices, answer, level, explanation)


QCM = tuple(_question(number + 1, *entree)
            for number, entree in enumerate(QUESTIONS))


PATTERNS = (UTILISATEUR, PROPRIETAIRE, IGNORER, MULTI_ETAPES,
            PREDIRE_USER, PREDIRE_CHOWN, PREDIRE_IGNORE, PREDIRE_MULTI,
            BUG_SU, BUG_IGNORE, BUG_SANTE, BUG_GATE) + QCM

MODULE = Module(
    key="docker_securite",
    title="Sécurisation Docker",
    level=3,
    summary="Scanner dépendances et images avec Trivy, durcir le "
            "Dockerfile (utilisateur non root, propriétaire des fichiers, "
            ".dockerignore, build multi-étapes, HEALTHCHECK) et bloquer le "
            "pipeline CI/CD sur une faille grave.",
    keys=tuple(p.key for p in PATTERNS),
)
