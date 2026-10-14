"""Demandes d'exercices : des documents de l'enseignant à une pull request.

L'application n'écrit pas d'exercice elle-même. Elle recueille la demande
— combien, de quelle nature, pour quel chapitre — et les documents qui
doivent l'inspirer, puis ouvre une issue sur le dépôt GitHub. Une Action
y répond : elle télécharge les documents, laisse Claude Code écrire le
module comme les autres, lancer les tests, et ouvrir une pull request.
Rien n'arrive en production sans qu'un humain fusionne cette PR.

Le dépôt est public, et l'issue avec lui. Elle ne porte donc ni les
documents ni de lien pour les obtenir : seulement le numéro de la
demande. L'Action télécharge avec une clé partagée (`ATELIER_DOCS_KEY`),
connue d'elle et de l'application, jamais écrite dans l'issue.

Les documents ne servent qu'à la construction. Ils sont rangés hors du
code (`instance/demandes/`), supprimés dès que l'Action a fini, et au
plus tard `RETENTION_DAYS` jours après le dépôt.
"""

import io
import json
import os
import secrets
import shutil
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timedelta, timezone

from flask import (Blueprint, Response, abort, current_app, redirect,
                   render_template, request, url_for)
from werkzeug.utils import secure_filename

from . import exercises as ex
from .admin import require_admin, who
from .db import execute, now, query

bp = Blueprint("generation", __name__)

ISSUE_LABEL = "evalio-generation"
RETENTION_DAYS = 7

MAX_FILES = 10
MAX_TOTAL_BYTES = 25 * 1024 * 1024
MAX_QUANTITY = 20
MAX_TITLE = 120
MAX_INSTRUCTIONS = 2000

# Ce que Claude Code sait lire, directement ou en extrayant le texte. Un
# exécutable ou une archive n'a rien à faire dans une demande de cours.
ALLOWED_EXTENSIONS = {
    "pdf", "txt", "md", "csv", "json", "yaml", "yml", "html",
    "docx", "odt", "pptx", "odp", "xlsx", "ods",
    "png", "jpg", "jpeg", "gif", "webp",
    "c", "h", "py", "sh", "sql", "conf",
}

# Nature des exercices, dans les termes du moteur (`Pattern.mode`).
KINDS = (
    ("complete", "Compléter",
     "Un code à trous, des menus pour les remplir, des paramètres tirés au hasard."),
    ("predict", "Prédire la sortie",
     "Un code complet : l'élève écrit ce qu'il affiche."),
    ("debug", "Trouver le bug",
     "Un code fautif, sa sortie : l'élève choisit la cause parmi quatre."),
    ("qcm", "QCM",
     "Une question, quatre propositions, une seule juste."),
)
KIND_LABELS = {key: label for key, label, _hint in KINDS}


class BadRequest(Exception):
    """Demande refusée. Le message est montré tel quel à l'enseignant."""


class GitHubError(Exception):
    """L'issue n'a pas pu être ouverte."""


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

def enabled(config):
    """Vrai si les trois réglages de la fonctionnalité sont présents."""
    return bool(config.get("GITHUB_TOKEN") and config.get("GITHUB_REPO")
                and config.get("DOCS_KEY"))


def storage_root():
    return current_app.config["REQUESTS_DIR"]


def folder_of(request_id):
    return os.path.join(storage_root(), str(int(request_id)))


# --------------------------------------------------------------------------
# Documents : dépôt, archive, suppression
# --------------------------------------------------------------------------

def _extension(filename):
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def check_uploads(uploads):
    """Contrôle les fichiers déposés. Rend [(nom sûr, contenu)]."""
    uploads = [u for u in uploads if u and u.filename]
    if not uploads:
        raise BadRequest("Déposez au moins un document.")
    if len(uploads) > MAX_FILES:
        raise BadRequest("%d documents au plus par demande." % MAX_FILES)

    files, total, seen = [], 0, set()
    for upload in uploads:
        name = secure_filename(upload.filename) or "document"
        if _extension(name) not in ALLOWED_EXTENSIONS:
            raise BadRequest(
                "« %s » : ce type de fichier n'est pas accepté. Formats "
                "acceptés : %s." % (upload.filename,
                                    ", ".join(sorted(ALLOWED_EXTENSIONS))))
        # Deux fichiers de même nom ne doivent pas s'écraser.
        base, dot, ext = name.rpartition(".")
        candidate, n = name, 2
        while candidate in seen:
            candidate = "%s-%d.%s" % (base, n, ext) if dot else "%s-%d" % (name, n)
            n += 1
        seen.add(candidate)

        data = upload.read()
        if not data:
            raise BadRequest("« %s » est vide." % upload.filename)
        total += len(data)
        if total > MAX_TOTAL_BYTES:
            raise BadRequest("Les documents dépassent %d Mo au total."
                             % (MAX_TOTAL_BYTES // (1024 * 1024)))
        files.append((candidate, data))
    return files


def store(request_id, files):
    folder = folder_of(request_id)
    os.makedirs(folder, exist_ok=True)
    for name, data in files:
        with open(os.path.join(folder, name), "wb") as handle:
            handle.write(data)


def purge(request_id):
    """Supprime les documents d'une demande. Idempotent."""
    shutil.rmtree(folder_of(request_id), ignore_errors=True)
    execute("UPDATE generation_request SET purged_at = ? "
            "WHERE id = ? AND purged_at IS NULL", (now(), request_id))


def purge_expired():
    """Supprime les documents déposés il y a plus de RETENTION_DAYS jours."""
    limit = (datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)) \
        .replace(microsecond=0).isoformat()
    for row in query("SELECT id FROM generation_request "
                     "WHERE purged_at IS NULL AND created_at < ?", (limit,)):
        purge(row["id"])


def archive(request_id):
    """Les documents d'une demande, en une archive zip."""
    folder = folder_of(request_id)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in sorted(os.listdir(folder)):
            zf.write(os.path.join(folder, name), arcname=name)
    return buf.getvalue()


# --------------------------------------------------------------------------
# Issue GitHub
# --------------------------------------------------------------------------

def chapter_label(row):
    if row["new_chapter"]:
        return "nouveau chapitre « %s »" % row["new_chapter"]
    chapter = next((c for c in ex.BASE_CHAPTERS if c.key == row["chapter_key"]),
                   None)
    title = chapter.title if chapter else row["chapter_key"]
    return "chapitre existant « %s » (clé `%s`)" % (title, row["chapter_key"])


def _cell(text):
    """Un texte saisi, sûr dans une cellule de tableau Markdown."""
    return str(text).replace("|", "\\|")


def issue_body(row):
    """Le corps de l'issue. Public : ni document, ni lien, ni clé."""
    kinds = ", ".join(KIND_LABELS[k] for k in json.loads(row["kinds"]))
    files = json.loads(row["files"])
    lines = [
        "Demande déposée depuis Evalio par **%s**." % (row["created_by"] or "?"),
        "",
        "| | |",
        "| --- | --- |",
        "| Intitulé du module | %s |" % _cell(row["title"]),
        "| Nombre d'exercices | %d |" % row["quantity"],
        "| Nature | %s |" % kinds,
        "| Rangement | %s |" % _cell(chapter_label(row)),
        "| Documents | %d fichier%s : %s |" % (
            len(files), "s" if len(files) > 1 else "",
            ", ".join("`%s`" % f["name"] for f in files)),
        "",
    ]
    if row["instructions"]:
        lines += ["### Consignes de l'enseignant", "", row["instructions"], ""]
    lines += [
        "---",
        "Les documents restent sur le serveur d'Evalio : l'Action "
        "`evalio-generation` les télécharge, puis les fait supprimer. Ils "
        "sont effacés au plus tard %d jours après le dépôt." % RETENTION_DAYS,
        "",
        # Lu par l'Action pour savoir quels documents télécharger.
        "<!-- evalio-demande: %d -->" % row["id"],
    ]
    return "\n".join(lines)


def create_issue(config, title, body):
    """Ouvre l'issue. Rend (numéro, url). Remplacé dans les tests."""
    payload = json.dumps({"title": title, "body": body,
                          "labels": [ISSUE_LABEL]}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.github.com/repos/%s/issues" % config["GITHUB_REPO"],
        data=payload, method="POST",
        headers={
            "Authorization": "Bearer %s" % config["GITHUB_TOKEN"],
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
            "User-Agent": "evalio",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")[:300]
        raise GitHubError("GitHub a refusé l'issue (HTTP %d) : %s"
                          % (err.code, detail)) from err
    except (urllib.error.URLError, OSError) as err:
        raise GitHubError("GitHub injoignable : %s" % err) from err
    return data["number"], data["html_url"]


# --------------------------------------------------------------------------
# Espace enseignant
# --------------------------------------------------------------------------

def _form_values(form):
    title = " ".join(form.get("title", "").split())[:MAX_TITLE]
    if not title:
        raise BadRequest("Donnez un intitulé au module.")

    try:
        quantity = int(form.get("quantity", ""))
    except ValueError:
        quantity = 0
    if not 1 <= quantity <= MAX_QUANTITY:
        raise BadRequest("Le nombre d'exercices va de 1 à %d." % MAX_QUANTITY)

    kinds = [k for k, _label, _hint in KINDS if k in form.getlist("kinds")]
    if not kinds:
        raise BadRequest("Choisissez au moins une nature d'exercice.")

    chapter_key, new_chapter = "", ""
    if form.get("placement") == "new":
        new_chapter = " ".join(form.get("new_chapter", "").split())[:MAX_TITLE]
        if not new_chapter:
            raise BadRequest("Donnez un titre au nouveau chapitre.")
    else:
        chapter_key = form.get("chapter_key", "")
        if chapter_key not in {c.key for c in ex.BASE_CHAPTERS}:
            raise BadRequest("Choisissez le chapitre qui accueillera le module.")

    instructions = form.get("instructions", "").strip()[:MAX_INSTRUCTIONS]
    return title, quantity, kinds, chapter_key, new_chapter, instructions


@bp.route("/admin/demandes", methods=("GET", "POST"))
@require_admin
def requests_page():
    config = current_app.config
    purge_expired()
    error = None
    if request.method == "POST":
        if not enabled(config):
            abort(404)
        try:
            title, quantity, kinds, chapter_key, new_chapter, instructions = \
                _form_values(request.form)
            files = check_uploads(request.files.getlist("documents"))
        except BadRequest as refus:
            error = str(refus)
        else:
            request_id = execute(
                """INSERT INTO generation_request
                     (title, quantity, kinds, chapter_key, new_chapter,
                      instructions, files, created_by, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (title, quantity, json.dumps(kinds), chapter_key, new_chapter,
                 instructions,
                 json.dumps([{"name": n, "size": len(d)} for n, d in files]),
                 who(), now()))
            store(request_id, files)
            row = query("SELECT * FROM generation_request WHERE id = ?",
                        (request_id,), one=True)
            try:
                number, url = create_issue(
                    config, "Exercices : %s" % title, issue_body(row))
            except GitHubError as err:
                # Sans issue, personne ne viendra chercher les documents.
                shutil.rmtree(folder_of(request_id), ignore_errors=True)
                execute("DELETE FROM generation_request WHERE id = ?",
                        (request_id,))
                current_app.logger.warning("Demande d'exercices : %s", err)
                error = str(err)
            else:
                execute("UPDATE generation_request SET issue_number = ?, "
                        "issue_url = ? WHERE id = ?", (number, url, request_id))
                return redirect(url_for(
                    "generation.requests_page",
                    ok="Demande envoyée : issue n°%d ouverte sur GitHub." % number))

    return render_template(
        "admin_requests.html",
        enabled=enabled(config),
        kinds=KINDS, kind_labels=KIND_LABELS,
        chapters=ex.BASE_CHAPTERS,
        rows=query("SELECT * FROM generation_request "
                   "ORDER BY created_at DESC, id DESC"),
        loads=json.loads,
        retention=RETENTION_DAYS,
        max_files=MAX_FILES, max_mb=MAX_TOTAL_BYTES // (1024 * 1024),
        max_quantity=MAX_QUANTITY,
        accept=",".join("." + e for e in sorted(ALLOWED_EXTENSIONS)),
        # Une demande refusee se represente telle que l'enseignant l'a
        # saisie ; un formulaire neuf propose « Compléter ».
        form=request.form if error else {},
        checked_kinds=request.form.getlist("kinds") if error else ["complete"],
        notice=request.args.get("ok", ""), error=error,
    )


# --------------------------------------------------------------------------
# Accès de l'Action GitHub : la clé partagée, rien d'autre
# --------------------------------------------------------------------------

def _require_key():
    key = current_app.config.get("DOCS_KEY") or ""
    given = request.headers.get("Authorization", "")
    expected = "Bearer " + key
    if not key or not secrets.compare_digest(given.encode("utf-8"),
                                             expected.encode("utf-8")):
        abort(401)


def _pending(request_id):
    row = query("SELECT * FROM generation_request WHERE id = ?",
                (request_id,), one=True)
    if row is None:
        abort(404)
    return row


@bp.get("/demandes/<int:request_id>/documents.zip")
def download(request_id):
    _require_key()
    row = _pending(request_id)
    if row["purged_at"] or not os.path.isdir(folder_of(request_id)):
        abort(410, description="Documents supprimés.")
    execute("UPDATE generation_request SET fetched_at = ? WHERE id = ?",
            (now(), request_id))
    return Response(archive(request_id), mimetype="application/zip",
                    headers={"Content-Disposition":
                             'attachment; filename="demande-%d.zip"' % request_id})


@bp.post("/demandes/<int:request_id>/termine")
def finished(request_id):
    """Appelé par l'Action à la fin de son travail, réussi ou non."""
    _require_key()
    _pending(request_id)
    purge(request_id)
    return {"ok": True}
