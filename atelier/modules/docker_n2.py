"""Module « Exercices Docker N2 », du chapitre Docker.

La suite des premiers pas : les volumes qui séparent l'application de
ses données, le Dockerfile et ses instructions (WORKDIR, COPY, ENV,
CMD), les constructions en plusieurs étapes, puis les réseaux d'un
fichier compose.yaml qui isolent le frontend de la base de données.

Comme au chapitre Linux, chaque exercice montre une **session de
terminal** : les lignes préfixées par `$` sont les commandes tapées, les
autres ce qu'elles ont affiché. Les sorties sont celles du vrai démon
Docker et des images de la séance (alpine, python:3.12-alpine,
nginx:alpine, postgres:16-alpine) ; `outils/verif_docker.py` rejoue
chaque session, pour chaque tirage et chaque option, et les compare.
"""

from ..engine import Module, Pattern, _opts, debug_pattern, predict_from
from .linux_commun import lecon, predire

# --------------------------------------------------------------------------
# Décors
# --------------------------------------------------------------------------

# Le site à servir et un dossier de notes, côté machine. Tout en
# minuscules : l'ordre de `ls` est alors le même dans le terminal de la
# machine et dans alpine, qui trie octet par octet.
SITES = (
    (("index.html", "style.css", "tetris.js"), ("memo.txt",)),
    (("hextris.js", "index.html"), ("idees.txt", "todo.txt")),
    (("index.html", "logo.png", "menu.html"), ("brouillon.txt",)),
    (("cv.html", "index.html", "photo.jpg"), ("liste.txt", "rappels.txt")),
)

# Le fichier qu'un conteneur écrit dans le dossier partagé, et son texte.
ECRITS = (
    ("journal.txt", "bonjour"),
    ("visites.txt", "salut"),
    ("traces.txt", "coucou"),
    ("passage.txt", "hello"),
)

# Deux lignes, une par conteneur.
PAIRES = (
    ("lundi", "mardi"),
    ("pomme", "poire"),
    ("nord", "sud"),
    ("alpha", "beta"),
)

# Le contenu de menu.txt (lancé par défaut) et de tarifs.txt.
CARTES = (
    (("entree : soupe", "plat : gratin"),
     ("menu : 15 euros", "dessert : 4 euros")),
    (("entree : salade", "plat : lasagnes"),
     ("menu : 12 euros", "cafe : 2 euros")),
    (("entree : tarte", "plat : risotto"),
     ("menu : 18 euros", "boisson : 3 euros")),
    (("entree : oeufs", "plat : curry"),
     ("menu : 14 euros", "fromage : 5 euros")),
)

SALLES = ("B204", "A112", "C310", "D007")
JOURS = ("lundi", "mercredi", "jeudi", "vendredi")

# Le fichier de travail laissé dans le contexte de construction. Tous
# après « Dockerfile » et autour de « page », dans les deux tris.
BROUILLONS = ("notes.txt", "memo.txt", "todo.txt", "essai.txt")

# La page source, en minuscules sans accent : `tr a-z A-Z` ne connaît
# que l'ASCII.
PAGES = (
    ("menu du jour", "soupe et pain"),
    ("horaires", "ouvert le matin"),
    ("contact", "ecrire au secretariat"),
    ("planning", "cours de docker"),
)

MESSAGES = (
    "Hello, Flask and Docker!",
    "Bonjour depuis l'étape runtime",
    "Image multi-étapes prête",
    "Application lancée",
)

# Les trois services de la séance, et ce que chaque test vérifie. Seuls
# frontend (nginx:alpine) et database (postgres:16-alpine) ont la
# commande `ping` : ce sont eux qui lancent les tests.
TESTS = (
    ("frontend", "backend"),
    ("frontend", "database"),
    ("database", "backend"),
)

# Ordres dans lesquels les tests sont lancés, un par tirage.
ORDRES = ((0, 1, 2), (1, 2, 0), (2, 0, 1), (0, 2, 1))

# Le fichier backend/app.py de la séance, réduit à sa route d'accueil.
# Les sessions ne le montrent pas — son décorateur porte un @, le
# marqueur des gabarits — mais outils/verif_docker.py le construit.
APP_BACKEND = """from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello from Backend!"

app.run(host="0.0.0.0", port=5000)"""

PORTS = (8080, 8081, 8088, 9090)


def _lignes(lignes):
    return "\n".join(lignes)


# --------------------------------------------------------------------------
# Monter un dossier de la machine
# --------------------------------------------------------------------------

def _site(p):
    site, notes = SITES[p["g"]]
    fichier, mot = ECRITS[p["g"]]
    return {"site": list(site), "notes": list(notes),
            "visible_site": _lignes(sorted(site)),
            "visible_notes": _lignes(sorted(notes)),
            "fichier": fichier, "mot": mot}


MONTER = Pattern(
    key="dk2_monter",
    name="Lister le site depuis un conteneur",
    brief="Monter le dossier /tmp/site de la machine sous /donnees, dans "
          "le conteneur, pour en lister le contenu.",
    why="Un volume relie un dossier de la machine à un dossier du conteneur.",
    lesson=lecon(
        "`-v source:cible` relie un chemin de la **machine** (à gauche) à "
        "un chemin du **conteneur** (à droite). L'ordre se lit comme "
        "celui de `-p hôte:conteneur`.",
        "Le conteneur voit, sous la cible, exactement le contenu de la "
        "source : pas une copie, le même dossier.",
        "`--rm` supprime le conteneur dès que sa commande est finie. Le "
        "dossier de la machine, lui, ne bouge pas.",
        "On peut aussi monter un seul **fichier** : la cible est alors un "
        "fichier, pas un dossier.",
    ),
    dims=(("g", 0, 3),),
    derive=_site,
    tpl="""$ ls -1 /tmp/site
@visible_site@
$ ls -1 /tmp/notes
@visible_notes@
$ docker run --rm -v @vol@ alpine ls /donnees""",
    blanks={
        "vol": ("Volume à monter", _opts(
            ("a", "/tmp/site:/donnees", lambda p: sorted(p["site"])),
            ("b", "/tmp/notes:/donnees", lambda p: sorted(p["notes"])),
            ("c", "/tmp/site:/srv",
             lambda _p: ["ls: /donnees: No such file or directory"]),
            ("d", "/tmp/site/index.html:/donnees",
             lambda _p: ["/donnees"]),
        )),
    },
    ref={"vol": "a"},
    rows=lambda p, get: get("vol")(p),
    level=1,
)


def _absent(p):
    return "cat: /tmp/site/%s: No such file or directory" % p["fichier"]


ECRIRE = Pattern(
    key="dk2_ecrire",
    name="Écrire dans le dossier partagé",
    brief="Laisser le conteneur écrire un fichier dans /tmp/site, puis le "
          "relire depuis la machine.",
    why="Un volume se monte en lecture-écriture, ou en lecture seule.",
    lesson=lecon(
        "Le troisième champ de `-v` donne les options du montage : `rw` "
        "(*read write*, le défaut) ou `ro` (*read only*).",
        "En `ro`, le conteneur peut lire le dossier mais pas y écrire : "
        "la machine, elle, garde tous ses droits.",
        "Ce que le conteneur écrit sous la cible arrive **directement** "
        "dans le dossier de la machine, et y reste après `--rm`.",
        "`;` enchaîne deux commandes, que la première réussisse ou non.",
    ),
    dims=(("g", 0, 3),),
    derive=_site,
    tpl="""$ ls -1 /tmp/site
@visible_site@
$ docker run --rm -v @vol@ alpine sh -c 'echo @mot@ > /donnees/@fichier@'; cat /tmp/site/@fichier@""",
    blanks={
        "vol": ("Volume à monter", _opts(
            ("a", "/tmp/site:/donnees:rw", lambda p: [p["mot"]]),
            ("b", "/tmp/site:/donnees:ro",
             lambda p: ["sh: can't create /donnees/%s: Read-only file system"
                        % p["fichier"], _absent(p)]),
            ("c", "/tmp/site:/srv:rw",
             lambda p: ["sh: can't create /donnees/%s: nonexistent directory"
                        % p["fichier"], _absent(p)]),
            ("d", "/tmp/notes:/donnees:rw", lambda p: [_absent(p)]),
        )),
    },
    ref={"vol": "a"},
    rows=lambda p, get: get("vol")(p),
    level=2,
)


# --------------------------------------------------------------------------
# Deux conteneurs, un même dossier
# --------------------------------------------------------------------------

def _paire(p):
    un, deux = PAIRES[p["g"]]
    return {"un": un, "deux": deux}


PARTAGE = Pattern(
    key="dk2_partage",
    name="Relire le journal commun",
    brief="Relire, depuis un troisième conteneur, le journal que les deux "
          "premiers ont rempli.",
    why="Le chemin dans le conteneur est libre ; c'est la source qui compte.",
    lesson=lecon(
        "Plusieurs conteneurs peuvent monter le **même** dossier de la "
        "machine, chacun sous le chemin qu'il veut.",
        "`>` écrit le fichier en effaçant ce qu'il contenait, `>>` ajoute "
        "à la fin.",
        "Si la source d'un `-v` n'existe pas, Docker crée un dossier "
        "**vide** à sa place, sans rien signaler.",
    ),
    dims=(("g", 0, 3),),
    derive=_paire,
    tpl="""$ mkdir /tmp/partage
$ docker run --rm -v /tmp/partage:/a alpine sh -c 'echo @un@ > /a/journal.txt'
$ docker run --rm -v /tmp/partage:/b alpine sh -c 'echo @deux@ >> /b/journal.txt'
$ docker run --rm -v @vol@ alpine cat /c/journal.txt""",
    blanks={
        "vol": ("Volume à monter", _opts(
            ("a", "/tmp/partage:/c", lambda p: [p["un"], p["deux"]]),
            ("b", "/tmp/partage:/a",
             lambda _p: ["cat: can't open '/c/journal.txt': "
                         "No such file or directory"]),
            ("c", "/tmp/c:/c",
             lambda _p: ["cat: can't open '/c/journal.txt': "
                         "No such file or directory"]),
            ("d", "/tmp/partage/journal.txt:/c",
             lambda _p: ["cat: can't open '/c/journal.txt': "
                         "Not a directory"]),
        )),
    },
    ref={"vol": "a"},
    rows=lambda p, get: get("vol")(p),
    level=3,
)


# La prédiction tire en plus l'opérateur du second conteneur : sans cela,
# il suffirait de recopier les deux mots dans l'ordre.
def _paire_operateur(p):
    out = _paire(p)
    out["op"] = ">>" if p["o"] else ">"
    return out


_PARTAGE_PREDIT = Pattern(
    key="dk2_partage_predit",
    name="",
    brief="",
    why="",
    lesson=PARTAGE.lesson,
    dims=(("g", 0, 3), ("o", 0, 1)),
    derive=_paire_operateur,
    tpl="""$ mkdir /tmp/partage
$ docker run --rm -v /tmp/partage:/a alpine sh -c 'echo @un@ > /a/journal.txt'
$ docker run --rm -v /tmp/partage:/b alpine sh -c 'echo @deux@ @op@ /b/journal.txt'
$ docker run --rm -v /tmp/partage:/c alpine cat /c/journal.txt""",
    blanks={},
    ref={},
    rows=lambda p, _get: ([p["un"], p["deux"]] if p["op"] == ">>"
                          else [p["deux"]]),
)


PREDIRE_PARTAGE = predict_from(
    _PARTAGE_PREDIT,
    key="dk2_predire_partage",
    name="Prédire : le journal commun",
    why="Trois conteneurs, trois chemins, un seul dossier de la machine.",
    level=2,
    output_format=(
        "<ligne du journal>",
        "…",
    ),
    lesson=predire(_PARTAGE_PREDIT),
)


# --------------------------------------------------------------------------
# Une note qui ne survit pas au conteneur
# --------------------------------------------------------------------------

BUG_PERSISTANCE = debug_pattern(
    key="dk2_bug_persistance",
    name="Bug : garder une note d'un conteneur à l'autre",
    sujet="Cette suite de commandes",
    but="conserver une note écrite par un premier conteneur, pour qu'un "
        "second la relise",
    defaut="le premier conteneur n'a pas de volume : il écrit dans son "
           "propre système de fichiers, effacé avec lui par --rm",
    dims=(("g", 0, 3),),
    derive=_site,
    tpl="""$ docker run --rm alpine sh -c 'mkdir -p /donnees && echo @mot@ > /donnees/memo.txt'
$ docker run --rm -v /tmp/notes:/donnees alpine cat /donnees/memo.txt""",
    attendu=lambda p: [p["mot"]],
    obtenu=lambda _p: ["cat: can't open '/donnees/memo.txt': "
                       "No such file or directory"],
    diagnostics=(
        ("a", "Le premier conteneur n'a pas de `-v` : il écrit dans son "
              "**propre** /donnees, qui disparaît avec lui.",
         "Exact. Sans volume, tout ce qu'écrit un conteneur reste dans sa "
         "couche à lui, et `--rm` la supprime à la fin. Il faut le même "
         "`-v /tmp/notes:/donnees` sur les deux lignes : c'est la "
         "séparation de l'application et des données."),
        ("b", "Le second conteneur monte /tmp/notes en lecture seule : il "
              "ne peut pas lire le fichier.",
         "Non : aucun `:ro` n'apparaît, et un montage en lecture seule se "
         "lit très bien. C'est l'écriture qu'il interdit."),
        ("c", "`--rm` a supprimé le dossier /tmp/notes de la machine à la "
              "fin du premier conteneur.",
         "Non : `--rm` supprime le conteneur, jamais un dossier de la "
         "machine. D'ailleurs le premier conteneur ne monte rien du tout."),
        ("d", "`mkdir -p` a échoué : le dossier /donnees existait déjà.",
         "Non : `-p` ne se plaint pas d'un dossier existant, et un échec "
         "aurait affiché un message. La note a bien été écrite, mais pas "
         "au bon endroit."),
    ),
    bonne="a",
    level=2,
)


# --------------------------------------------------------------------------
# Remplacer la commande par défaut
# --------------------------------------------------------------------------

def _carte(p):
    menu, tarifs = CARTES[p["g"]]
    return {"menu": list(menu), "tarifs": list(tarifs),
            "contenu_menu": _lignes(menu), "contenu_tarifs": _lignes(tarifs)}


CMD = Pattern(
    key="dk2_cmd",
    name="Afficher les tarifs sans toucher l'image",
    brief="Afficher le contenu de tarifs.txt avec l'image carte:1.0, sans "
          "modifier ni reconstruire le Dockerfile.",
    why="Ce qui suit le nom de l'image remplace le CMD du Dockerfile.",
    lesson=lecon(
        "`WORKDIR /app` choisit le dossier de travail : les commandes "
        "suivantes, et celle du conteneur, s'y exécutent.",
        "`COPY . /app` copie le dossier courant de la machine (le "
        "**contexte**) dans l'image, Dockerfile compris.",
        "`CMD` n'est qu'une commande **par défaut** : tout ce qu'on écrit "
        "après le nom de l'image dans `docker run` la remplace.",
        "`docker build -q` n'affiche que l'identifiant de l'image ; on "
        "l'envoie ici vers /dev/null.",
    ),
    dims=(("g", 0, 3),),
    derive=_carte,
    tpl="""$ ls -1
Dockerfile
menu.txt
tarifs.txt
$ cat menu.txt
@contenu_menu@
$ cat tarifs.txt
@contenu_tarifs@
$ cat Dockerfile
FROM alpine
WORKDIR /app
COPY . /app
CMD ["cat", "menu.txt"]
$ docker build -q -t carte:1.0 . > /dev/null
$ docker run --rm carte:1.0 @args@""",
    blanks={
        "args": ("Commande à lancer dans le conteneur", _opts(
            ("a", "cat tarifs.txt", lambda p: p["tarifs"]),
            ("b", "cat menu.txt", lambda p: p["menu"]),
            ("c", "ls", lambda _p: ["Dockerfile", "menu.txt", "tarifs.txt"]),
            ("d", "pwd", lambda _p: ["/app"]),
        )),
    },
    ref={"args": "a"},
    rows=lambda p, get: get("args")(p),
    level=2,
)


# --------------------------------------------------------------------------
# Les variables d'environnement
# --------------------------------------------------------------------------

def _cours(p):
    return {"salle": SALLES[p["g"]], "jour": JOURS[p["j"]]}


ENV = Pattern(
    key="dk2_env",
    name="Annoncer le cours de mardi",
    brief="Annoncer le cours de mardi, dans la même salle, sans "
          "reconstruire l'image.",
    why="ENV fixe une valeur par défaut ; `-e` la remplace au lancement.",
    lesson=lecon(
        "`ENV NOM=valeur` range une variable d'environnement **dans "
        "l'image** : chaque conteneur la reçoit au démarrage.",
        "`docker run -e NOM=valeur` la remplace pour ce conteneur-là, "
        "sans toucher à l'image.",
        "Les noms de variables distinguent majuscules et minuscules : "
        "`jour` et `JOUR` sont deux variables différentes.",
        "Écrit sans crochets, `CMD echo …` passe par un shell, qui "
        "remplace `$NOM` par sa valeur.",
    ),
    dims=(("g", 0, 3), ("j", 0, 3)),
    derive=_cours,
    tpl="""$ cat Dockerfile
FROM alpine
ENV SALLE=@salle@
ENV JOUR=@jour@
CMD echo "Cours le $JOUR en salle $SALLE"
$ docker build -q -t cours:1.0 . > /dev/null
$ docker run --rm @opt@ cours:1.0""",
    blanks={
        "opt": ("Options de docker run", _opts(
            ("a", "-e JOUR=mardi",
             lambda p: ["Cours le mardi en salle %s" % p["salle"]]),
            ("b", "-e SALLE=mardi",
             lambda p: ["Cours le %s en salle mardi" % p["jour"]]),
            ("c", "-e jour=mardi",
             lambda p: ["Cours le %s en salle %s" % (p["jour"], p["salle"])]),
            ("d", "-e JOUR=mardi -e SALLE=",
             lambda _p: ["Cours le mardi en salle"]),
        )),
    },
    ref={"opt": "a"},
    rows=lambda p, get: get("opt")(p),
    level=3,
)


BUG_ENV = debug_pattern(
    key="dk2_bug_env",
    name="Bug : annoncer la salle du cours",
    sujet="Ce Dockerfile",
    but="annoncer, au lancement du conteneur, la salle rangée dans la "
        "variable SALLE",
    defaut="CMD en forme exec (entre crochets) : aucun shell ne remplace "
           "$SALLE",
    dims=(("g", 0, 3),),
    derive=lambda p: {"salle": SALLES[p["g"]]},
    tpl="""$ cat Dockerfile
FROM alpine
ENV SALLE=@salle@
CMD ["echo", "Cours en salle $SALLE"]
$ docker build -q -t salle:1.0 . > /dev/null
$ docker run --rm salle:1.0""",
    attendu=lambda p: ["Cours en salle %s" % p["salle"]],
    obtenu=lambda _p: ["Cours en salle $SALLE"],
    diagnostics=(
        ("a", "Entre crochets, le CMD lance `echo` **directement**, sans "
              "shell : personne ne remplace `$SALLE` par sa valeur.",
         "Exact. C'est le shell qui développe les variables. La forme "
         "entre crochets (*exec*) donne le texte tel quel à `echo`. "
         "`CMD echo \"Cours en salle $SALLE\"`, ou "
         "`CMD [\"sh\", \"-c\", \"echo Cours en salle $SALLE\"]`, "
         "passent par un shell."),
        ("b", "`ENV` ne sert que pendant la construction : la variable "
              "n'existe plus quand le conteneur démarre.",
         "Non : c'est `ARG` qui ne vit que pendant le build. Une variable "
         "`ENV` est rangée dans l'image et reçue par chaque conteneur."),
        ("c", "Il fallait écrire `${SALLE}` : Docker ne reconnaît pas "
              "`$SALLE` sans accolades.",
         "Non : dans un shell, les deux écritures se valent. Et entre "
         "crochets, `${SALLE}` resterait affiché tel quel, lui aussi."),
        ("d", "`echo` n'existe pas dans alpine : Docker affiche alors le "
              "texte brut du CMD.",
         "Non : `echo` a bien tourné, c'est lui qui a écrit la ligne. "
         "Une commande introuvable ferait échouer le lancement avec un "
         "message d'erreur."),
    ),
    bonne="a",
    level=3,
)


# --------------------------------------------------------------------------
# Les constructions en plusieurs étapes
# --------------------------------------------------------------------------

def _etapes(p):
    brouillon = BROUILLONS[p["g"]]
    return {"brouillon": brouillon,
            "visible": _lignes(sorted(["Dockerfile", brouillon,
                                       "page.txt"]))}


MULTI = Pattern(
    key="dk2_multi",
    name="Ne livrer que la page produite",
    brief="N'embarquer dans l'image finale que la page produite par "
          "l'étape build, et rien d'autre.",
    why="L'image finale ne contient que ce qu'on y copie explicitement.",
    lesson=lecon(
        "Un Dockerfile peut enchaîner plusieurs `FROM` : chacun ouvre une "
        "**étape**, et `AS build` lui donne un nom.",
        "Seule la **dernière** étape devient l'image. Les autres ne "
        "servent qu'à préparer des fichiers.",
        "`COPY --from=build source cible` prend la source dans l'étape "
        "build ; sans `--from`, `COPY` la prend dans le contexte, le "
        "dossier courant de la machine.",
        "Copier un dossier copie son **contenu** dans la cible.",
    ),
    dims=(("g", 0, 3),),
    derive=_etapes,
    tpl="""$ ls -1
@visible@
$ cat Dockerfile
# --- build ---
FROM alpine AS build
WORKDIR /app
COPY . .
RUN tr a-z A-Z < page.txt > page.html
# --- runtime ---
FROM alpine
WORKDIR /app
@copie@
CMD ["ls"]
$ docker build -q -t site:2.1 . > /dev/null
$ docker run --rm site:2.1""",
    blanks={
        "copie": ("Copie dans l'image finale", _opts(
            ("a", "COPY --from=build /app/page.html .",
             lambda _p: ["page.html"]),
            ("b", "COPY . .",
             lambda p: sorted(["Dockerfile", p["brouillon"], "page.txt"])),
            ("c", "COPY --from=build /app .",
             lambda p: sorted(["Dockerfile", p["brouillon"], "page.html",
                               "page.txt"])),
            ("d", "COPY --from=build /app/page.txt .",
             lambda _p: ["page.txt"]),
        )),
    },
    ref={"copie": "a"},
    rows=lambda p, get: get("copie")(p),
    level=3,
)


def _page(p):
    lignes = PAGES[p["g"]]
    out = _etapes(p)
    out.update({"lignes": list(lignes), "contenu": _lignes(lignes)})
    return out


_MULTI_PREDIT = Pattern(
    key="dk2_multi_predit",
    name="",
    brief="",
    why="",
    lesson=MULTI.lesson + (
        "`tr a-z A-Z` recopie son entrée en changeant chaque minuscule en "
        "majuscule.",
    ),
    dims=(("g", 0, 3),),
    derive=_page,
    tpl="""$ ls -1
@visible@
$ cat page.txt
@contenu@
$ cat Dockerfile
# --- build ---
FROM alpine AS build
WORKDIR /app
COPY . .
RUN tr a-z A-Z < page.txt > page.html
# --- runtime ---
FROM alpine
WORKDIR /app
COPY --from=build /app/page.html .
COPY @brouillon@ .
CMD ["sh", "-c", "ls; cat page.html"]
$ docker build -q -t site:2.2 . > /dev/null
$ docker run --rm site:2.2""",
    blanks={},
    ref={},
    rows=lambda p, _get: (sorted([p["brouillon"], "page.html"])
                          + [l.upper() for l in p["lignes"]]),
)


PREDIRE_MULTI = predict_from(
    _MULTI_PREDIT,
    key="dk2_predire_multi",
    name="Prédire : le contenu de l'image finale",
    why="Seule la dernière étape devient l'image.",
    level=3,
    output_format=(
        "<fichier de /app>",
        "…",
        "<ligne de page.html>",
        "…",
    ),
    lesson=predire(_MULTI_PREDIT),
)


BUG_MULTI = debug_pattern(
    key="dk2_bug_multi",
    name="Bug : lancer l'application Python",
    sujet="Ce Dockerfile",
    but="lancer app.py depuis une image construite en deux étapes",
    defaut="COPY --from=build dépose l'application dans /srv, alors que "
           "WORKDIR et CMD la cherchent dans /app",
    dims=(("g", 0, 3),),
    derive=lambda p: {"message": MESSAGES[p["g"]]},
    tpl="""$ cat app.py
print("@message@")
$ cat Dockerfile
# --- build ---
FROM python:3.12-alpine AS build
WORKDIR /app
COPY app.py .
# --- runtime ---
FROM python:3.12-alpine
WORKDIR /app
COPY --from=build /app /srv
CMD ["python", "app.py"]
$ docker build -q -t appli:2.1 . > /dev/null
$ docker run --rm appli:2.1""",
    attendu=lambda p: [p["message"]],
    obtenu=lambda _p: ["python: can't open file '/app/app.py': "
                       "[Errno 2] No such file or directory"],
    diagnostics=(
        ("a", "`COPY --from=build /app /srv` dépose app.py dans /srv, "
              "alors que le conteneur démarre dans /app, qui reste vide.",
         "Exact. Le CMD cherche `app.py` dans le dossier de travail, "
         "/app — le message le dit. `COPY --from=build /app /app` (ou "
         "`/app .`) remet le fichier où on l'attend."),
        ("b", "Une étape ne voit pas les autres : `--from` ne sait copier "
              "que depuis le contexte de la machine.",
         "Non : c'est justement le rôle de `--from=build`, copier depuis "
         "l'étape nommée `build`. La copie a eu lieu, mais ailleurs."),
        ("c", "`WORKDIR /app` de la seconde étape efface les fichiers "
              "copiés depuis l'étape build.",
         "Non : `WORKDIR` choisit (et crée au besoin) le dossier de "
         "travail, il n'efface rien. Il vient d'ailleurs **avant** la "
         "copie."),
        ("d", "python:3.12-alpine ne connaît pas la commande `python`, "
              "seulement `python3`.",
         "Non : le message d'erreur vient de `python` lui-même, qui a "
         "donc bien démarré. C'est le fichier qu'il ne trouve pas."),
    ),
    bonne="a",
    level=3,
)


# --------------------------------------------------------------------------
# Les réseaux d'un fichier compose.yaml
# --------------------------------------------------------------------------

# Rappel commun aux exercices de réseau : la fonction `joint` est la même
# partout, et il faut savoir la lire.
RESEAU = (
    "Dans un fichier compose.yaml, `networks:` d'un service donne la "
    "liste des réseaux auxquels son conteneur est rattaché.",
    "Deux conteneurs se joignent, **par leur nom de service**, s'ils "
    "partagent au moins un réseau. Sinon, le nom n'est même pas connu.",
    "Un conteneur rattaché à deux réseaux ne fait pas passer les autres "
    "de l'un à l'autre : il n'est pas un routeur.",
    "`joint a b` lance `ping` depuis le service `a` vers le service `b`, "
    "et n'affiche que le verdict.",
)

JOINT = ('joint() { docker compose exec $1 ping -c 1 -W 1 $2 > /dev/null '
         '2>&1 && echo "$1 -> $2 : joignable" || echo "$1 -> $2 : '
         'injoignable"; }')


def _verdicts(reseaux, ordre):
    """Une ligne par test : joignable si les deux services partagent un réseau."""
    lignes = []
    for rang in ordre:
        de, vers = TESTS[rang]
        commun = set(reseaux[de]) & set(reseaux[vers])
        lignes.append("%s -> %s : %s" % (de, vers, "joignable" if commun
                                         else "injoignable"))
    return lignes


def _ordre(p):
    ordre = ORDRES[p["g"]]
    return {"ordre": ordre,
            "tests": "; ".join("joint %s %s" % TESTS[rang] for rang in ordre)}


def _liste(noms):
    return "[%s]" % ", ".join(noms)


def _compose(front, back, base):
    """Le compose.yaml de la séance, réseaux de chaque service compris."""
    return """services:
  frontend:
    image: nginx:alpine
    ports:
      - "8080:80"
    depends_on:
      - backend
    networks: %s
  backend:
    build: ./backend
    depends_on:
      - database
    networks: %s
  database:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: tpdb
      POSTGRES_USER: student
      POSTGRES_PASSWORD: student123
    networks: %s
networks:
  frontendnet:
    driver: bridge
  backendnet:
    driver: bridge""" % (front, back, base)


def _reseaux_backend(backend):
    return lambda p: _verdicts({"frontend": ["frontendnet"],
                                "backend": backend,
                                "database": ["backendnet"]}, p["ordre"])


RESEAUX = Pattern(
    key="dk2_reseaux",
    name="Relier le backend aux deux réseaux",
    brief="Placer le backend de sorte que le frontend le joigne, que le "
          "backend joigne la base, et que le frontend ne joigne pas la "
          "base.",
    why="Frontend <-> Backend <-> BDD : le backend est le seul pont.",
    lesson=lecon(*RESEAU),
    dims=(("g", 0, 3),),
    derive=_ordre,
    tpl="$ cat compose.yaml\n" + _compose("[frontendnet]", "@reseaux@",
                                          "[backendnet]") + """
$ docker compose up -d --build
$ """ + JOINT + """
$ @tests@""",
    blanks={
        "reseaux": ("Réseaux du backend", _opts(
            ("a", "[frontendnet, backendnet]",
             _reseaux_backend(["frontendnet", "backendnet"])),
            ("b", "[frontendnet]", _reseaux_backend(["frontendnet"])),
            ("c", "[backendnet]", _reseaux_backend(["backendnet"])),
            ("d", "[default]", _reseaux_backend(["default"])),
        )),
    },
    ref={"reseaux": "a"},
    rows=lambda p, get: get("reseaux")(p),
    level=3,
)


# Configurations tirées pour la prédiction : (frontend, backend, database).
CONFIGS = (
    (["frontendnet"], ["frontendnet", "backendnet"], ["backendnet"]),
    (["frontendnet"], ["backendnet"], ["frontendnet", "backendnet"]),
    (["frontendnet", "backendnet"], ["backendnet"], ["backendnet"]),
    (["frontendnet"], ["frontendnet"], ["backendnet"]),
)


def _config(p):
    front, back, base = CONFIGS[p["c"]]
    out = _ordre(p)
    out.update({"reseaux": {"frontend": front, "backend": back,
                            "database": base},
                "compose": _compose(_liste(front), _liste(back),
                                    _liste(base))})
    return out


_RESEAUX_PREDIT = Pattern(
    key="dk2_reseaux_predit",
    name="",
    brief="",
    why="",
    lesson=lecon(*RESEAU),
    dims=(("c", 0, 3), ("g", 0, 3)),
    derive=_config,
    tpl="""$ cat compose.yaml
@compose@
$ docker compose up -d --build
$ """ + JOINT + """
$ @tests@""",
    blanks={},
    ref={},
    rows=lambda p, _get: _verdicts(p["reseaux"], p["ordre"]),
)


PREDIRE_RESEAUX = predict_from(
    _RESEAUX_PREDIT,
    key="dk2_predire_reseaux",
    name="Prédire : qui joint qui ?",
    why="Pour chaque test, cherchez un réseau commun aux deux services.",
    level=4,
    output_format=(
        "<service> -> <service> : <joignable ou injoignable>",
        "<service> -> <service> : <joignable ou injoignable>",
        "<service> -> <service> : <joignable ou injoignable>",
    ),
    lesson=predire(_RESEAUX_PREDIT),
)


BUG_RESEAU = debug_pattern(
    key="dk2_bug_reseau",
    name="Bug : isoler la base de données",
    sujet="Ce fichier compose.yaml",
    but="isoler la base de données : seul le backend doit pouvoir la "
        "joindre, le frontend passe par lui",
    defaut="le frontend est rattaché aussi à backendnet, le réseau de la "
           "base",
    dims=(("g", 0, 3),),
    derive=_ordre,
    tpl="$ cat compose.yaml\n" + _compose("[frontendnet, backendnet]",
                                          "[frontendnet, backendnet]",
                                          "[backendnet]") + """
$ docker compose up -d --build
$ """ + JOINT + """
$ @tests@""",
    attendu=lambda p: _verdicts({"frontend": ["frontendnet"],
                                 "backend": ["frontendnet", "backendnet"],
                                 "database": ["backendnet"]}, p["ordre"]),
    obtenu=lambda p: _verdicts({"frontend": ["frontendnet", "backendnet"],
                                "backend": ["frontendnet", "backendnet"],
                                "database": ["backendnet"]}, p["ordre"]),
    diagnostics=(
        ("a", "Le frontend est rattaché à `backendnet`, le réseau de la "
              "base : il la joint directement.",
         "Exact. Deux services qui partagent un réseau se joignent, quel "
         "que soit le reste. Le frontend ne doit garder que "
         "`[frontendnet]` : il parle au backend, et lui seul parle à la "
         "base."),
        ("b", "Le backend est sur les deux réseaux : il fait passer le "
              "frontend jusqu'à la base.",
         "Non : un conteneur sur deux réseaux n'est pas un routeur, il ne "
         "relaie rien. Le backend doit d'ailleurs rester sur les deux "
         "réseaux pour joindre la base."),
        ("c", "Les deux réseaux sont en `driver: bridge` : des réseaux "
              "bridge communiquent entre eux.",
         "Non : chaque réseau bridge est isolé des autres. C'est même ce "
         "qui permet de séparer frontend et base."),
        ("d", "`depends_on` relie le frontend au backend, et donc à tout "
              "ce dont le backend dépend.",
         "Non : `depends_on` ne règle que l'**ordre de démarrage**. Il ne "
         "rattache aucun service à aucun réseau."),
    ),
    bonne="a",
    level=4,
)


# --------------------------------------------------------------------------
# Le frontend relaie vers le backend
# --------------------------------------------------------------------------

BUG_PROXY = debug_pattern(
    key="dk2_bug_proxy",
    name="Bug : relayer les requêtes vers le backend",
    sujet="Cette installation",
    but="relayer les requêtes du frontend nginx vers le backend Flask",
    defaut="proxy_pass vise localhost : dans le conteneur frontend, "
           "localhost désigne le frontend lui-même, pas le backend",
    dims=(("g", 0, 3),),
    derive=lambda p: {"port": PORTS[p["g"]]},
    tpl="""$ cat backend/Dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
$ cat frontend/default.conf
server {
    listen 80;
    location / {
        proxy_pass http://localhost:5000;
    }
}
$ cat compose.yaml
services:
  frontend:
    image: nginx:alpine
    ports:
      - "@port@:80"
    volumes:
      - ./frontend/default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - backend
  backend:
    build: ./backend
$ docker compose up -d --build
$ curl -s http://localhost:@port@ -o /dev/null -w '%{http_code}\\n'""",
    attendu=lambda _p: ["200"],
    obtenu=lambda _p: ["502"],
    diagnostics=(
        ("a", "Dans le conteneur frontend, `localhost` désigne le frontend "
              "lui-même : nginx cherche le port 5000 chez lui, où rien "
              "n'écoute.",
         "Exact. Chaque conteneur a son propre `localhost`. Entre "
         "services, on se désigne par le **nom de service** : "
         "`proxy_pass http://backend:5000;`. Le code 502 (*Bad Gateway*) "
         "est la façon dont nginx dit qu'il n'a pas pu joindre la suite."),
        ("b", "Le port 5000 du backend n'est pas publié avec `ports:` : "
              "nginx ne peut pas l'atteindre.",
         "Non : `ports:` ouvre un port **vers la machine**. Entre deux "
         "conteneurs d'un même réseau, tous les ports sont joignables sans "
         "rien publier."),
        ("c", "nginx écoute sur le port 80, alors que curl interroge un "
              "autre port de la machine.",
         "Non : la ligne `ports:` relie justement ce port de la machine "
         "au port 80 du conteneur. La preuve : nginx a répondu, avec un "
         "code d'erreur."),
        ("d", "Aucun `networks:` n'est déclaré : les deux services ne sont "
              "sur aucun réseau commun.",
         "Non : sans `networks:`, compose rattache tous les services à un "
         "réseau `default` commun. Le frontend pourrait joindre le "
         "backend… s'il le visait par son nom."),
    ),
    bonne="a",
    level=4,
)


PATTERNS = (MONTER, ECRIRE, PARTAGE, PREDIRE_PARTAGE, BUG_PERSISTANCE,
            CMD, ENV, BUG_ENV, MULTI, PREDIRE_MULTI, BUG_MULTI,
            RESEAUX, PREDIRE_RESEAUX, BUG_RESEAU, BUG_PROXY)

MODULE = Module(
    key="docker_n2",
    title="Exercices Docker N2",
    level=3,
    summary="Les volumes qui séparent l'application de ses données, le "
            "Dockerfile (WORKDIR, COPY, ENV, CMD), les constructions en "
            "plusieurs étapes et les réseaux d'un fichier compose.yaml.",
    keys=tuple(p.key for p in PATTERNS),
)
