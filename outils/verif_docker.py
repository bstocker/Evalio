#!/usr/bin/env python3
"""Confronte les sessions du module « Exercices Docker N2 » au vrai Docker.

Chaque exercice montre une session de terminal et annonce ce qu'affiche
sa dernière commande. Cet outil rejoue la session pour de bon : il
reconstruit le décor à partir de la session elle-même (le contenu de
chaque `cat`, les noms de chaque `ls -1`), lance les commandes, puis
compare la sortie de la dernière à celle que l'application annonce.
Tous les tirages, toutes les options ; pour un « trouver le bug », la
version fautive et la version corrigée.

    python3 outils/verif_docker.py [clé …]

Il n'est pas dans la suite de tests : il lui faut un démon Docker, le
réseau pour tirer les images (alpine, python:3.12-alpine,
python:3.12-slim, nginx:alpine, postgres:16-alpine) et plusieurs
minutes. Les chemins /tmp/… des sessions sont rangés dans un dossier
temporaire : rien n'est écrit dans le vrai /tmp de la machine.
"""

import itertools, os, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
from atelier import exercises as ex
from atelier.modules.docker_n2 import APP_BACKEND

# La version corrigée de chaque « trouver le bug » : elle doit produire
# la sortie attendue, comme la version fautive produit l'obtenue.
CORRECTIONS = {
    "dk2_bug_persistance": ("docker run --rm alpine sh -c 'mkdir",
                            "docker run --rm -v /tmp/notes:/donnees alpine "
                            "sh -c 'mkdir"),
    "dk2_bug_env": ('CMD ["echo", "Cours en salle $SALLE"]',
                    'CMD echo "Cours en salle $SALLE"'),
    "dk2_bug_multi": ("COPY --from=build /app /srv",
                      "COPY --from=build /app /app"),
    "dk2_bug_reseau": ("networks: [frontendnet, backendnet]",
                       "networks: [frontendnet]"),
    "dk2_bug_proxy": ("localhost:5000", "backend:5000"),
}

# Le backend des exercices de réseau, que leur session ne montre pas.
BACKEND = {
    "backend/app.py": APP_BACKEND + "\n",
    "backend/Dockerfile": "FROM python:3.12-slim\nWORKDIR /app\n"
                          "RUN pip install --no-cache-dir flask\n"
                          "COPY app.py .\nCMD [\"python\", \"app.py\"]\n",
}


def tirages(pattern):
    specs = ex.specs(pattern)
    noms = [n for n, _a, _b in specs]
    for combo in itertools.product(*[range(a, b + 1) for _n, a, b in specs]):
        p = dict(zip(noms, combo))
        if pattern.derive:
            p.update(pattern.derive(p))
        yield p


def decouper(session):
    """[(commande, [lignes affichées])] d'une session de terminal."""
    blocs = []
    for ligne in session.split("\n"):
        if ligne.startswith("$ "):
            blocs.append((ligne[2:], []))
        else:
            blocs[-1][1].append(ligne)
    return blocs


def ecrire(chemin, texte):
    os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
    with open(chemin, "w") as fh:
        fh.write(texte)


def nettoyer(racine):
    """Les conteneurs écrivent en root : on vide le dossier par Docker."""
    subprocess.run(["docker", "run", "--rm", "-v", "%s:/menage" % racine,
                    "alpine", "sh", "-c", "rm -rf /menage/* /menage/.[!.]*"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(racine, ignore_errors=True)


def rejouer(cle, session):
    """Rejoue la session ; rend (écarts du décor, sortie de la dernière)."""
    racine = tempfile.mkdtemp(prefix="verif_docker_")
    tmp, travail = os.path.join(racine, "tmp"), os.path.join(racine, "travail")
    os.makedirs(tmp)
    os.makedirs(travail)
    local = lambda texte: texte.replace("/tmp/", tmp + "/")
    blocs = decouper(session)
    compose = any("docker compose" in cmd for cmd, _ in blocs)
    if compose:
        for nom, texte in BACKEND.items():
            ecrire(os.path.join(travail, nom), texte)

    # Le décor : ce que montrent les `ls -1` et les `cat`.
    for cmd, lignes in blocs[:-1]:
        mots = cmd.split()
        if mots[:2] == ["ls", "-1"] and lignes:
            dossier = os.path.join(travail, local(mots[2]) if len(mots) > 2
                                   else ".")
            os.makedirs(dossier, exist_ok=True)
            for nom in lignes:
                if not os.path.exists(os.path.join(dossier, nom)):
                    ecrire(os.path.join(dossier, nom), nom + "\n")
        elif mots[0] == "cat" and len(mots) == 2:
            ecrire(os.path.join(travail, local(mots[1])),
                   "\n".join(lignes) + "\n")

    # Le script : chaque commande, sa sortie entre deux marqueurs.
    script = ["export COMPOSE_PROJECT_NAME=verif%d" % os.getpid()]
    for rang, (cmd, _lignes) in enumerate(blocs):
        if compose and rang == len(blocs) - 1:
            script.append("sleep 10")
        script.append("echo '@@%d'" % rang)
        script.append(local(cmd) + " 2>&1")
    script.append("echo '@@fin'")
    if compose:
        script.append("docker compose down -v > /dev/null 2>&1")
    r = subprocess.run(["bash", "-c", "\n".join(script)], cwd=travail,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True)
    nettoyer(racine)

    sorties, courant = {}, None
    for ligne in r.stdout.replace(tmp + "/", "/tmp/").split("\n"):
        if ligne.startswith("@@"):
            courant = ligne[2:]
            sorties[courant] = []
        elif courant is not None:
            sorties[courant].append(ligne.rstrip())
    ecarts = []
    for rang, (cmd, lignes) in enumerate(blocs[:-1]):
        if lignes and [l.rstrip() for l in lignes] != sorties.get(str(rang)):
            ecarts.append((cmd, lignes, sorties.get(str(rang))))
    return ecarts, sorties.get(str(len(blocs) - 1), [])


ECHECS = []


def confronter(cle, quoi, session, annonce):
    ecarts, reel = rejouer(cle, session)
    annonce = [l.rstrip() for l in annonce]
    if ecarts or reel != annonce:
        ECHECS.append((cle, quoi, session, ecarts, annonce, reel))
        print("  ÉCART", cle, quoi)


def verifie(cle):
    pattern = ex.PATTERNS[cle]
    for p in tirages(pattern):
        tirage = {k: v for k, v in p.items() if k in "gjoc"}
        if pattern.mode == "complete":
            blank = list(pattern.blanks)[0]
            for opt in pattern.blanks[blank][1]:
                choix = {blank: opt.id}
                confronter(cle, (tirage, opt.c),
                           ex.render_code(cle, p, choix),
                           ex.build_rows(cle, p, choix))
        elif pattern.mode == "predict":
            confronter(cle, tirage, ex.render_code(cle, p),
                       ex.target_rows(cle, p))
        elif pattern.mode == "debug":
            session = ex.render_code(cle, p)
            confronter(cle, (tirage, "fautif"), session,
                       ex.broken_rows(cle, p))
            avant, apres = CORRECTIONS[cle]
            assert avant in session, cle
            confronter(cle, (tirage, "corrigé"),
                       session.replace(avant, apres, 1),
                       ex.target_rows(cle, p))
    print("verifie", cle)


def main(cles):
    for cle in cles or ex.MODULE_BY_KEY["docker_n2"].keys:
        verifie(cle)
    for cle, quoi, session, ecarts, annonce, reel in ECHECS:
        print("\n=== %s %s" % (cle, quoi))
        print(session)
        for cmd, montre, vu in ecarts:
            print("décor « %s » : montré %r, obtenu %r" % (cmd, montre, vu))
        print("annoncé :", annonce)
        print("réel    :", reel)
    print("\n%d écart(s)" % len(ECHECS))
    return 1 if ECHECS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
