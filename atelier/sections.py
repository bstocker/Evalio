"""Sections du chapitre QCM : des rayons que l'enseignant cree lui-meme.

Le chapitre QCM grossit a chaque import : au-dela de quelques
questionnaires, une liste a plat devient difficile a parcourir.
L'enseignant y cree donc des sections (« Docker », « Réseau », « Partiel
de janvier »…) et y range ses QCM par glisser-deposer.

Ce rangement ne sert qu'a la composition d'une session : il ne touche ni
au catalogue, ni aux copies, ni au bareme. Un QCM range nulle part reste
en bas du chapitre, sous « Sans section » ; supprimer une section y
renvoie les siens. Le rangement est commun a tous les comptes, comme le
catalogue lui-meme.

Les modules livres avec l'application se rangent comme les importes : le
placement ne retient que la cle du module.
"""

from .db import execute, get_db, now, query

TITLE_MAX = 80


def clean(title):
    """Intitule d'une section : espaces resserres, longueur bornee."""
    return " ".join(str(title or "").split())[:TITLE_MAX]


def listing():
    """Les sections, dans l'ordre de leur creation."""
    return query("SELECT * FROM qcm_section ORDER BY position, id")


def get(section_id):
    return query("SELECT * FROM qcm_section WHERE id = ?", (section_id,),
                 one=True)


def create(title, by=""):
    """Ajoute une section en fin de chapitre. Rend son identifiant."""
    last = query("SELECT COALESCE(MAX(position), 0) AS p FROM qcm_section",
                 one=True)["p"]
    return execute(
        """INSERT INTO qcm_section (title, position, created_by, created_at)
           VALUES (?, ?, ?, ?)""", (title, last + 1, by, now()))


def rename(section_id, title):
    execute("UPDATE qcm_section SET title = ? WHERE id = ?",
            (title, section_id))


def delete(section_id):
    """Supprime une section ; ses QCM retournent sous « Sans section »."""
    # Le placement part avec la section (ON DELETE CASCADE).
    execute("DELETE FROM qcm_section WHERE id = ?", (section_id,))


def place(section_id, module_keys):
    """Range `module_keys`, dans cet ordre, dans une section.

    `section_id` a None les sort de toute section. La liste est celle de
    la section d'arrivee tout entiere, telle que l'enseignant vient de la
    voir : les positions sont reecrites d'un bloc, sans trou.
    """
    db = get_db()
    if section_id is None:
        db.executemany("DELETE FROM qcm_placement WHERE module_key = ?",
                       [(key,) for key in module_keys])
    else:
        db.executemany(
            """INSERT INTO qcm_placement (module_key, section_id, position)
               VALUES (?, ?, ?)
               ON CONFLICT(module_key) DO UPDATE
                  SET section_id = excluded.section_id,
                      position = excluded.position""",
            [(key, section_id, position)
             for position, key in enumerate(module_keys)])
    db.commit()


def forget(module_key):
    """Oublie le rangement d'un module supprime."""
    execute("DELETE FROM qcm_placement WHERE module_key = ?", (module_key,))


def group(modules):
    """Repartit les modules du chapitre QCM entre les sections.

    `modules` est la liste `[(module, niveaux)]` du catalogue. Rend
    `[(section, [(module, niveaux)])]` : chaque section dans son ordre,
    meme vide — c'est la qu'on depose le premier QCM —, puis `None` pour
    les modules ranges nulle part, dans l'ordre du catalogue.
    """
    sections = listing()
    placed = {row["module_key"]: (row["section_id"], row["position"])
              for row in query("SELECT * FROM qcm_placement")}
    known = {section["id"] for section in sections}
    out = []
    for section in sections:
        inside = [(m, n) for m, n in modules
                  if placed.get(m.key, (None,))[0] == section["id"]]
        inside.sort(key=lambda item: placed[item[0].key][1])
        out.append((section, inside))
    loose = [(m, n) for m, n in modules
             if placed.get(m.key, (None,))[0] not in known]
    out.append((None, loose))
    return out
