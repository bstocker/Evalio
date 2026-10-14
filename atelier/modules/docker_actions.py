"""Module « Tests Actions », du chapitre Docker.

Des questions de cours sur la suite des séances, après les premiers pas
de `docker_bases` : entrer dans un conteneur, y copier un fichier, monter
un répertoire de la machine, compiler avec un conteneur jetable, puis
monter un cluster Swarm et y publier un service.

Les images sont celles de la séance : le serveur httpd de quay.io et
OpenJDK sur Docker Hub.
"""

from ..engine import Module, qcm_pattern
from .docker_bases import HTTPD
from .qcm_docker import _tourner

# Répertoire servi par l'image httpd.
HTDOCS = "/usr/local/apache2/htdocs/"

# (énoncé, (quatre propositions), index de la bonne, niveau, explication)
# Comme dans qcm_docker, la bonne réponse est écrite en premier puis
# déplacée par `_tourner`.
QUESTIONS = (
    ("Que fait `docker exec -it CONTAINER_ID bash` ?",
     ("Il ouvre un terminal bash à l'intérieur du conteneur qui tourne",
      "Il lance un nouveau conteneur à partir de l'image bash",
      "Il exécute le script bash de la machine sur tous les conteneurs",
      "Il redémarre le conteneur en mode interactif"),
     0, 1,
     "`exec` lance une commande dans un conteneur **déjà en marche** ; "
     "`-it` la rend interactive. On en ressort avec `exit`, et le "
     "conteneur continue de tourner."),

    ("Un serveur httpd tourne sous le nom `web`. Quelle commande y dépose "
     "le fichier `index.html` du dossier courant, dans `%s` ?" % HTDOCS,
     ("docker cp index.html web:%s" % HTDOCS,
      "docker cp web:%s index.html" % HTDOCS,
      "docker exec index.html web:%s" % HTDOCS,
      "docker run index.html web:%s" % HTDOCS),
     0, 2,
     "`docker cp` se lit comme `cp` : la source, puis la destination. "
     "Le côté conteneur s'écrit **nom:chemin**. Inverser les deux "
     "copierait la page du conteneur vers la machine."),

    ("On lance `docker run -d -p 80:80 -v /tmp:%s:ro %s`. "
     "Que signifie le `:ro` final ?" % (HTDOCS, HTTPD),
     ("Le conteneur voit le répertoire en lecture seule : il ne peut pas "
      "y écrire",
      "La machine ne peut plus modifier son répertoire /tmp",
      "Le répertoire est copié une fois au lancement, puis plus jamais "
      "relu",
      "Le conteneur redémarre à chaque modification du répertoire"),
     0, 2,
     "`ro` pour *read only*. Le /tmp de la machine et le répertoire du "
     "conteneur restent liés : un `echo` dans /tmp/index.html côté "
     "machine change aussitôt la page servie. Seul le conteneur est "
     "privé d'écriture."),

    ("Trois serveurs httpd sont lancés avec le même `-v /tmp:%s:ro`, sur "
     "les ports 80, 81 et 82. On écrit ensuite une page dans "
     "`/tmp/index.html` sur la machine. Que montrent les trois ports ?"
     % HTDOCS,
     ("La même page, sans rien relancer",
      "La page sur le port 80 seulement, le premier lancé",
      "Rien tant que les trois conteneurs n'ont pas été redémarrés",
      "Une erreur : un répertoire ne peut être monté que dans un seul "
      "conteneur"),
     0, 3,
     "Les trois conteneurs lisent le même répertoire de la machine. "
     "C'est l'intérêt du volume : les données sont séparées de "
     "l'application, et partagées par autant de serveurs qu'on veut."),

    ("Main.java est dans /tmp. On lance "
     "`docker run --rm -v /tmp:/usr/src/myapp -w /usr/src/myapp "
     "openjdk:11 javac Main.java`. Où se trouve Main.class ensuite ?",
     ("Dans /tmp, sur la machine",
      "Nulle part : `--rm` l'a supprimé avec le conteneur",
      "Dans l'image openjdk:11, pour les prochains lancements",
      "Dans /usr/src/myapp, sur la machine"),
     0, 3,
     "`-w` place le compilateur dans /usr/src/myapp, qui **est** le /tmp "
     "de la machine grâce à `-v`. Le conteneur, lui, disparaît à la fin "
     "(`--rm`) : il n'a servi qu'à prêter son javac. Le même principe "
     "exécute ensuite `java Main`."),

    ("Le manager d'un cluster Swarm publie un service avec "
     "`docker service create --name MyWeb "
     "--publish published=80,target=80 %s`. "
     "Sur quels nœuds le port 80 répond-il ?" % HTTPD,
     ("Sur tous les nœuds du cluster, manager comme workers",
      "Sur le manager seulement, qui a créé le service",
      "Sur un seul worker, tiré au hasard",
      "Sur aucun : il faut encore lancer `docker run -p 80:80` sur "
      "chaque nœud"),
     0, 4,
     "Swarm publie le port d'un service sur **chaque** nœud du cluster, "
     "même sur ceux qui n'hébergent aucun conteneur du service : la "
     "requête est relayée jusqu'à un conteneur qui sait répondre. C'est "
     "ce qu'on observe en testant le port 80 sur les quatre nœuds."),
)


def _build(rang, question, choices, answer, level, explanation):
    choices, answer = _tourner(choices, answer, rang)
    return qcm_pattern("dk_actions_%02d" % rang, rang, question,
                       choices, answer, level, explanation)


PATTERNS = tuple(
    _build(number + 1, *entree) for number, entree in enumerate(QUESTIONS)
)

MODULE = Module(
    key="docker_actions",
    title="Tests Actions",
    level=2,
    summary="Entrer dans un conteneur, y copier un fichier, monter un "
            "répertoire de la machine, compiler avec un conteneur jetable, "
            "et publier un service sur un cluster Swarm.",
    keys=tuple(p.key for p in PATTERNS),
)
