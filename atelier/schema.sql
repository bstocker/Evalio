-- Journal classique, et non WAL. Le mode WAL est plus rapide, mais il
-- exige de la memoire partagee entre les processus qui ouvrent la base :
-- SQLite le documente comme inutilisable sur un systeme de fichiers
-- reseau, et l'hebergement monte precisement /home par le reseau. Le
-- gain ne vaut pas le risque de corrompre des copies d'eleves.
-- `outils/diag_base.py` dit sous quel mode tourne la base deployee.
PRAGMA journal_mode = DELETE;

-- Comptes enseignants crees par l'administrateur. Le compte administrateur
-- lui-meme n'est pas ici : il vient des variables d'environnement, et il est
-- le seul a pouvoir creer, reinitialiser ou supprimer les comptes ci-dessous.
CREATE TABLE IF NOT EXISTS teacher (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT    NOT NULL UNIQUE COLLATE NOCASE,
    password_hash TEXT    NOT NULL,
    created_by    TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL,
    last_login_at TEXT
);

CREATE TABLE IF NOT EXISTS session (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    code        TEXT    NOT NULL UNIQUE,
    title       TEXT    NOT NULL,
    patterns    TEXT    NOT NULL,              -- JSON : liste de cles de motifs
    status      TEXT    NOT NULL DEFAULT 'draft',  -- draft | open | closed
    exam_mode   INTEGER NOT NULL DEFAULT 0,       -- 1 : l'eleve ne voit pas sa reussite
    revision_mode INTEGER NOT NULL DEFAULT 0,     -- 1 : sorties de fenetre libres
    created_by  TEXT    NOT NULL DEFAULT '',      -- compte qui a cree la session
    created_at  TEXT    NOT NULL,
    opened_at   TEXT,
    closed_at   TEXT
);

CREATE TABLE IF NOT EXISTS student (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id     INTEGER NOT NULL REFERENCES session(id) ON DELETE CASCADE,
    first_name     TEXT    NOT NULL,
    last_name      TEXT    NOT NULL,
    token          TEXT    NOT NULL UNIQUE,
    joined_at      TEXT    NOT NULL,
    last_seen_at   TEXT,
    finished_at    TEXT,
    exit_count     INTEGER NOT NULL DEFAULT 0,
    penalty_points REAL    NOT NULL DEFAULT 0,
    final_score    REAL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_student_identity
    ON student(session_id, last_name, first_name);

CREATE TABLE IF NOT EXISTS task (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  INTEGER NOT NULL REFERENCES student(id) ON DELETE CASCADE,
    pattern_key TEXT    NOT NULL,
    position    INTEGER NOT NULL,
    params      TEXT    NOT NULL,              -- JSON : {"n": 5}
    attempts    INTEGER NOT NULL DEFAULT 0,
    wrong_attempts INTEGER NOT NULL DEFAULT 0,  -- essais manques avant reussite
    solved      INTEGER NOT NULL DEFAULT 0,
    solved_at   TEXT,
    selection   TEXT    NOT NULL DEFAULT '{}', -- JSON : dernier choix
    UNIQUE(student_id, pattern_key)
);

CREATE TABLE IF NOT EXISTS incident (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES student(id) ON DELETE CASCADE,
    ordinal    INTEGER NOT NULL,               -- 1re, 2e, 3e sortie...
    kind       TEXT    NOT NULL,               -- blur | hidden | fullscreen
    penalty    REAL    NOT NULL,
    returned_ms INTEGER,                       -- delai de retour, si revenu
    created_at TEXT    NOT NULL
);

-- Chapitre QCM : les modules importes au format Excel. Les modules livres
-- avec l'application, eux, restent decrits en Python dans atelier/modules/.
CREATE TABLE IF NOT EXISTS qcm_module (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    key         TEXT    NOT NULL UNIQUE,     -- cle de module, derivee du titre
    title       TEXT    NOT NULL,
    summary     TEXT    NOT NULL DEFAULT '',
    level       INTEGER NOT NULL DEFAULT 2,
    source      TEXT    NOT NULL DEFAULT '', -- nom du fichier importe
    imported_at TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS qcm_question (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id   INTEGER NOT NULL REFERENCES qcm_module(id) ON DELETE CASCADE,
    key         TEXT    NOT NULL UNIQUE,     -- cle de motif, unique au registre
    position    INTEGER NOT NULL,
    question    TEXT    NOT NULL,
    choices     TEXT    NOT NULL,            -- JSON : les quatre propositions
    answer      INTEGER NOT NULL,            -- indice de la bonne, de 0 a 3
    level       INTEGER NOT NULL DEFAULT 2,
    explanation TEXT    NOT NULL DEFAULT ''
);

-- Sections du chapitre QCM (cf. atelier/sections.py) : des rayons crees par
-- l'enseignant, ou il range ses QCM par glisser-deposer. Un module absent
-- de qcm_placement est « sans section ». La cle de module vaut pour les
-- modules importes comme pour ceux livres avec l'application.
CREATE TABLE IF NOT EXISTS qcm_section (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    position    INTEGER NOT NULL DEFAULT 0,
    created_by  TEXT    NOT NULL DEFAULT '',
    created_at  TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS qcm_placement (
    module_key  TEXT    PRIMARY KEY,
    section_id  INTEGER NOT NULL REFERENCES qcm_section(id) ON DELETE CASCADE,
    position    INTEGER NOT NULL DEFAULT 0
);

-- Modules livres avec l'application que l'enseignant a retires du
-- catalogue. Ils vivent dans le code : on ne peut que les masquer. Leurs
-- exercices restent au registre, pour que les copies qui les citent
-- s'affichent toujours ; ils ne sont plus proposes a la composition.
CREATE TABLE IF NOT EXISTS hidden_module (
    key        TEXT PRIMARY KEY,
    hidden_by  TEXT NOT NULL DEFAULT '',
    hidden_at  TEXT NOT NULL
);

-- Demandes d'exercices envoyees au depot GitHub (cf. atelier/generation.py).
-- Les documents eux-memes sont sur le disque, dans instance/demandes/<id>/,
-- et `purged_at` dit quand ils en sont partis.
CREATE TABLE IF NOT EXISTS generation_request (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT    NOT NULL,
    quantity     INTEGER NOT NULL,
    kinds        TEXT    NOT NULL,              -- JSON : natures demandees
    chapter_key  TEXT    NOT NULL DEFAULT '',   -- chapitre existant...
    new_chapter  TEXT    NOT NULL DEFAULT '',   -- ...ou titre d'un nouveau
    instructions TEXT    NOT NULL DEFAULT '',
    files        TEXT    NOT NULL DEFAULT '[]', -- JSON : [{name, size}]
    created_by   TEXT    NOT NULL DEFAULT '',
    created_at   TEXT    NOT NULL,
    issue_number INTEGER,
    issue_url    TEXT,
    fetched_at   TEXT,                          -- telecharges par l'Action
    purged_at    TEXT                           -- supprimes du serveur
);

-- Listes de classe (cf. atelier/roster.py) : l'enseignant projette un QR
-- code, chaque eleve y inscrit son nom et son prenom. Rien a voir avec les
-- copies d'une session d'exercices : ni jeton, ni cookie, un simple releve.
CREATE TABLE IF NOT EXISTS roster (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    code        TEXT    NOT NULL UNIQUE,         -- dans l'URL du QR code
    title       TEXT    NOT NULL,                -- « B2 CDA »
    status      TEXT    NOT NULL DEFAULT 'open', -- open | closed
    created_by  TEXT    NOT NULL DEFAULT '',
    created_at  TEXT    NOT NULL,
    closed_at   TEXT
);

CREATE TABLE IF NOT EXISTS roster_entry (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    roster_id   INTEGER NOT NULL REFERENCES roster(id) ON DELETE CASCADE,
    first_name  TEXT    NOT NULL,
    last_name   TEXT    NOT NULL,
    created_at  TEXT    NOT NULL
);

-- Un eleve qui valide deux fois n'apparait qu'une fois, casse ignoree.
CREATE UNIQUE INDEX IF NOT EXISTS idx_roster_identity
    ON roster_entry(roster_id, last_name COLLATE NOCASE,
                    first_name COLLATE NOCASE);

CREATE INDEX IF NOT EXISTS idx_qcm_question_module
    ON qcm_question(module_id, position);

CREATE INDEX IF NOT EXISTS idx_task_student ON task(student_id);
CREATE INDEX IF NOT EXISTS idx_incident_student ON incident(student_id);
CREATE INDEX IF NOT EXISTS idx_student_session ON student(session_id);
