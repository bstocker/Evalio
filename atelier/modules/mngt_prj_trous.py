"""Module « Mgt-Prj_textes à compléter » du chapitre Mngt_Prj.

Dix textes à trous de révision sur le management de projet SI : le projet
SI et ses contraintes, le triangle d'or et la qualité, de la vision au
portefeuille de projets, le cycle de vie AFNOR Z67-101, la définition du
périmètre, la matrice RACI, la gouvernance, le management des risques,
celui des coûts, puis la communication, le changement et le bilan.

Chaque texte est une fiche (mode « compléter ») : un menu par trou, et
une cible qui dit, pour chaque trou, ce que le mot doit exprimer sans le
nommer. Un mauvais choix affiche à sa place un indice — ce que veut dire
le mot choisi — qui ne nomme jamais la bonne réponse. La forme est celle
des phrases à trous du chapitre Allemand (`allemand_commun.trous`), dont
on reprend la fabrique.

Le cours accepte les synonymes exacts des réponses (« étendue » pour
« périmètre », « RETEX » pour « REX ») : aucun menu ne propose donc un
synonyme de la bonne réponse comme distracteur, et le REX est proposé
sous ses deux noms (« REX / RETEX »).

Les textes sont réécrits pour l'exercice, dans l'esprit du cours.
"""

from functools import partial

from ..engine import Module
from . import allemand_commun as commun

INTITULE = (
    "Textes à trous de révision du cours de management de projet SI. Si "
    "ta réponse est fausse, un indice t'explique ton erreur sans te donner "
    "la solution : relis-le, puis corrige."
)

trous = partial(commun.trous, INTITULE)


def rappel(texte):
    """Rappel d'une fiche : la partie du cours qu'elle fait réviser."""
    return ("Partie du cours à revoir en cas de doute : %s." % texte,)


# --------------------------------------------------------------------------
# Texte 1 : le projet SI
# --------------------------------------------------------------------------

PROJET_SI = trous(
    "mprj_projet_si", "Le projet SI",
    "Complète la définition d'un projet SI et de ses contraintes.",
    1,
    rappel("la définition du projet SI"),
    """Un projet SI est un ensemble (1) @t1@ et (2) @t2@
d'activités qui permet de (3) @t3@ une (4) @t4@ du SI,
pour répondre à un (5) @t5@ (6) @t6@ et contribuer
aux objectifs (7) @t7@ de l'entreprise.

Il a un début et une fin. Il est contraint par le (8) @t8@
qui lui est alloué, par la (9) @t9@ fixée pour atteindre ses
objectifs, et par son (10) @t10@, c'est-à-dire l'étendue
fonctionnelle et technique des (11) @t11@ attendus.""",
    (
        ("t1", "1", "qui ne dure pas indéfiniment",
         "temporaire",
         (("permanent", "« permanent » : qui dure sans fin ; c'est le "
                        "propre des opérations courantes, pas d'un projet"),
          ("répétitif", "« répétitif » : qui se reproduit à l'identique ; "
                        "un projet est unique"),
          ("informel", "« informel » : sans cadre ni règles ; un projet "
                       "est au contraire encadré"))),
        ("t2", "2", "structuré, coordonné",
         "organisé",
         (("improvisé", "« improvisé » : fait sans préparation ; un projet "
                        "se prépare"),
          ("isolé", "« isolé » : sans lien avec le reste ; les activités "
                    "d'un projet sont reliées entre elles"),
          ("facultatif", "« facultatif » : dont on peut se passer ; cela ne "
                         "dit rien de la façon dont les activités "
                         "s'enchaînent"))),
        ("t3", "3", "faire évoluer, modifier",
         "transformer",
         (("maintenir", "« maintenir » : garder en l'état ; c'est "
                        "l'exploitation courante, pas un projet"),
          ("auditer", "« auditer » : examiner sans rien changer"),
          ("documenter", "« documenter » : décrire ce qui existe, sans le "
                         "changer"))),
        ("t4", "4", "une partie, un élément",
         "composante",
         (("sauvegarde", "« sauvegarde » : une copie de sécurité des "
                         "données ; on transforme le SI lui-même"),
          ("panne", "« panne » : un incident ; la réparer relève de la "
                    "maintenance, pas d'un projet"),
          ("licence", "« licence » : un droit d'usage d'un logiciel, pas "
                      "une partie du SI à transformer"))),
        ("t5", "5", "ce qui est attendu, ce qui manque",
         "besoin",
         (("risque", "« risque » : un événement incertain qui menace le "
                     "projet ; on le gère, il ne motive pas le projet"),
          ("jalon", "« jalon » : un point de contrôle du planning"),
          ("livrable", "« livrable » : ce que produit le projet, pas ce qui "
                       "le motive"))),
        ("t6", "6", "qui vient des activités de l'entreprise et de ses "
                    "utilisateurs",
         "métier",
         (("technique", "« technique » : qui vient de l'informatique "
                        "elle-même ; relis l'origine demandée"),
          ("personnel", "« personnel » : propre à une seule personne"),
          ("imprévu", "« imprévu » : inattendu ; cela ne dit pas d'où vient "
                      "le besoin"))),
        ("t7", "7", "de long terme, fixés par la direction",
         "stratégiques",
         (("opérationnels", "« opérationnels » : de court terme, au "
                            "quotidien des équipes"),
          ("techniques", "« techniques » : propres à l'informatique"),
          ("individuels", "« individuels » : propres à chaque salarié"))),
        ("t8", "8", "les moyens financiers",
         "budget",
         (("planning", "« planning » : l'organisation des tâches dans le "
                       "temps ; la contrainte de temps vient juste après"),
          ("contrat", "« contrat » : l'engagement entre un client et un "
                      "prestataire, pas une contrainte du projet"),
          ("sponsor", "« sponsor » : la personne qui porte le projet, pas "
                      "une contrainte"))),
        ("t9", "9", "le temps disponible",
         "durée",
         (("qualité", "« qualité » : elle dépend des contraintes, elle "
                      "n'en est pas une"),
          ("méthode", "« méthode » : la façon de conduire le projet"),
          ("charge", "« charge » : la quantité de travail, en "
                     "jours-hommes, pas le temps calendaire"))),
        ("t10", "10", "ce que le projet couvre, et ce qu'il ne couvre pas",
         "périmètre",
         (("coût", "« coût » : c'est l'argent, contrainte déjà citée"),
          ("calendrier", "« calendrier » : c'est le temps, contrainte "
                         "déjà citée"),
          ("sponsor", "« sponsor » : la personne qui porte le projet"))),
        ("t11", "11", "les produits remis à la fin d'une étape ou du projet",
         "livrables",
         (("comités", "« comités » : les instances de gouvernance du "
                      "projet ; elles ne sont pas livrées"),
          ("risques", "« risques » : des événements incertains, pas des "
                      "produits attendus"),
          ("jalons", "« jalons » : des points de contrôle du planning, pas "
                     "des produits"))),
    ),
)


# --------------------------------------------------------------------------
# Texte 2 : le triangle d'or et la qualité
# --------------------------------------------------------------------------

TRIANGLE = trous(
    "mprj_triangle", "Le triangle d'or et la qualité",
    "Complète le texte sur les trois contraintes d'un projet et la "
    "qualité.",
    1,
    rappel("le triangle d'or et la qualité"),
    """Un projet doit respecter trois contraintes : les (1) @t1@,
les (2) @t2@ et le (3) @t3@.

La (4) @t4@ dépend de ces trois contraintes : c'est fournir
un livrable (5) @t5@ aux besoins, dans le (6) @t6@
et au (7) @t7@ prévus.""",
    (
        ("t1", "1", "l'argent dépensé",
         "coûts",
         (("risques", "« risques » : des événements incertains ; on les "
                      "gère, ils ne sont pas un sommet du triangle"),
          ("acteurs", "« acteurs » : les personnes du projet, pas une "
                      "contrainte"),
          ("livrables", "« livrables » : ce que produit le projet, pas une "
                        "contrainte"))),
        ("t2", "2", "les échéances à tenir",
         "délais",
         (("comités", "« comités » : les instances de gouvernance"),
          ("outils", "« outils » : les moyens de travail, pas une "
                     "contrainte du triangle"),
          ("bénéfices", "« bénéfices » : ce que le projet rapporte, pas une "
                        "contrainte"))),
        ("t3", "3", "le contenu : ce qui est inclus et ce qui est exclu",
         "périmètre",
         (("planning", "« planning » : c'est le temps, contrainte déjà "
                       "citée"),
          ("budget", "« budget » : c'est l'argent, contrainte déjà citée"),
          ("sponsor", "« sponsor » : la personne qui porte le projet"))),
        ("t4", "4", "ce qui résulte de l'équilibre des trois contraintes",
         "qualité",
         (("rentabilité", "« rentabilité » : le rapport entre gains et "
                          "coût ; la phrase parle de conformité aux "
                          "besoins"),
          ("sécurité", "« sécurité » : la protection du SI, qui ne se "
                       "définit pas par ces trois contraintes"),
          ("communication", "« communication » : l'échange d'informations "
                            "entre acteurs"))),
        ("t5", "5", "qui correspond exactement",
         "conforme",
         (("supérieur", "« supérieur » : aller au-delà du besoin coûte sans "
                        "rien apporter ; la qualité n'est pas le luxe"),
          ("indifférent", "« indifférent » : sans rapport avec les "
                          "besoins"),
          ("antérieur", "« antérieur » : qui vient avant ; ce n'est pas un "
                        "critère de qualité"))),
        ("t6", "6", "la durée prévue",
         "temps",
         (("désordre", "« dans le désordre » : sans organisation"),
          ("doute", "« dans le doute » : sans certitude ; ce n'est pas une "
                    "contrainte"),
          ("secret", "« dans le secret » : sans en parler ; ce n'est pas "
                     "une contrainte"))),
        ("t7", "7", "le budget",
         "coût",
         (("hasard", "« au hasard » : sans plan, le contraire d'une "
                     "prévision"),
          ("rabais", "« au rabais » : à moindre prix, au détriment de la "
                     "qualité"),
          ("mérite", "« au mérite » : selon les efforts fournis ; ce n'est "
                     "pas une contrainte"))),
    ),
)


# --------------------------------------------------------------------------
# Texte 3 : de la vision au projet
# --------------------------------------------------------------------------

VISION = trous(
    "mprj_vision", "De la vision au projet",
    "Complète le texte qui relie la vision de l'entreprise à ses "
    "projets.",
    2,
    rappel("de la vision au portefeuille de projets"),
    """La (1) @t1@ exprime ce que l'organisation veut devenir à long
terme ; la (2) @t2@ précise comment y parvenir. Elle se
décline en axes et en objectifs stratégiques (3) @t3@.

Le (4) @t4@ définit, sur (5) @t5@ ans, les grandes
orientations du SI.

Le (6) @t6@ de projets permet d'arbitrer les priorités et
d'optimiser l'allocation des ressources ; un projet qui n'y
appartient pas est dit « sauvage » ou « (7) @t7@ ».""",
    (
        ("t1", "1", "l'image de l'avenir visé",
         "vision",
         (("mission", "« mission » : la raison d'être actuelle de "
                      "l'organisation, ce qu'elle fait aujourd'hui"),
          ("stratégie", "« stratégie » : elle dit comment avancer, pas où "
                        "l'on veut aller"),
          ("charte", "« charte » : un document qui fixe des règles"))),
        ("t2", "2", "le chemin pour atteindre ce but",
         "stratégie",
         (("vision", "« vision » : elle dit où l'on veut aller, pas "
                     "comment"),
          ("comptabilité", "« comptabilité » : l'enregistrement des "
                           "dépenses et des recettes"),
          ("recette", "« recette » : la vérification d'un livrable avant "
                      "sa mise en service"))),
        ("t3", "3", "dont on peut vérifier l'atteinte par un indicateur",
         "mesurables",
         (("confidentiels", "« confidentiels » : tenus secrets ; cela ne "
                            "permet pas de vérifier qu'on les atteint"),
          ("facultatifs", "« facultatifs » : dont on peut se passer"),
          ("provisoires", "« provisoires » : appelés à changer bientôt"))),
        ("t4", "4", "le document de planification du SI à moyen terme",
         "SDSI",
         (("cahier des charges", "« cahier des charges » : il décrit les "
                                 "besoins d'un seul projet"),
          ("COPIL", "« COPIL » : un comité, pas un document"),
          ("RACI", "« RACI » : la matrice qui répartit les rôles dans un "
                   "projet"))),
        ("t5", "5", "le moyen terme",
         "3 à 5",
         (("1 à 2", "1 à 2 ans : c'est le court terme"),
          ("10 à 15", "10 à 15 ans : c'est le long terme de la vision ; le "
                      "SI change trop vite pour être planifié aussi loin"),
          ("20 à 30", "20 à 30 ans : bien trop loin pour planifier un SI"))),
        ("t6", "6", "l'ensemble des projets, géré comme un tout",
         "portefeuille",
         (("lot", "« lot » : une partie du découpage d'un seul projet"),
          ("bilan", "« bilan » : il se fait à la fin d'un projet ; il "
                    "n'arbitre pas les priorités"),
          ("calendrier", "« calendrier » : il dit quand, pas quel projet "
                         "passe en premier"))),
        ("t7", "7", "sans rattachement",
         "orphelin",
         (("pilote", "« pilote » : un projet d'essai à petite échelle"),
          ("prioritaire", "« prioritaire » : un projet hors de "
                          "l'arbitrage ne peut pas avoir été jugé "
                          "prioritaire"),
          ("stratégique", "« stratégique » : un projet hors du "
                          "portefeuille n'est justement pas aligné sur "
                          "la stratégie"))),
    ),
)


# --------------------------------------------------------------------------
# Texte 4 : le cycle de vie AFNOR Z67-101
# --------------------------------------------------------------------------

CYCLE = trous(
    "mprj_cycle_afnor", "Le cycle de vie AFNOR Z67-101",
    "Complète le texte sur les étapes du cycle de vie d'un projet.",
    2,
    rappel("le cycle de vie AFNOR Z67-101"),
    """Le cycle générique AFNOR Z67-101 enchaîne cinq étapes :
l'(1) @t1@, la (2) @t2@, la (3) @t3@,
la (4) @t4@ et l'(5) @t5@.

Chaque étape est validée par un (6) @t6@ ; le (7) @t7@ est
un point d'arrêt qui permet de vérifier la conformité d'une
étape avant de passer à la suivante.""",
    (
        ("t1", "1", "1re étape : l'opportunité et la faisabilité",
         "étude préalable",
         (("évaluation / clôture", "« évaluation / clôture » : la dernière "
                                   "étape, pas la première"),
          ("exploitation", "« exploitation » : la vie courante du SI, après "
                           "le projet"),
          ("expression de besoin", "« expression de besoin » : un document "
                                   "remis au projet, pas une de ses cinq "
                                   "étapes"))),
        ("t2", "2", "2e étape : on décrit précisément la solution retenue",
         "conception détaillée",
         (("réalisation", "« réalisation » : on construit la solution ; "
                          "cela suppose qu'elle soit déjà décrite"),
          ("mise en œuvre", "« mise en œuvre » : on déploie la solution "
                            "chez les utilisateurs ; il faut l'avoir "
                            "construite avant"),
          ("maintenance", "« maintenance » : la vie du SI après le "
                          "projet"))),
        ("t3", "3", "3e étape : on construit la solution",
         "réalisation",
         (("conception détaillée", "« conception détaillée » : on décrit la "
                                   "solution, on ne la construit pas"),
          ("mise en œuvre", "« mise en œuvre » : on déploie une solution "
                            "déjà construite"),
          ("planification", "« planification » : elle accompagne tout le "
                            "projet, ce n'est pas une des cinq étapes"))),
        ("t4", "4", "4e étape : on déploie la solution chez les "
                    "utilisateurs",
         "mise en œuvre",
         (("réalisation", "« réalisation » : on construit la solution, sans "
                          "encore la déployer"),
          ("conception détaillée", "« conception détaillée » : on décrit la "
                                   "solution"),
          ("maintenance", "« maintenance » : la vie du SI après le "
                          "projet"))),
        ("t5", "5", "dernière étape : on fait le bilan et on ferme le "
                    "projet",
         "évaluation / clôture",
         (("étude préalable", "« étude préalable » : la première étape, pas "
                              "la dernière"),
          ("exploitation", "« exploitation » : la vie courante du SI, qui "
                           "n'est plus le projet"),
          ("expression de besoin", "« expression de besoin » : elle vient "
                                   "avant le projet, pas à la fin"))),
        ("t6", "6", "un produit ou un document remis",
         "livrable",
         (("risque", "« risque » : un événement incertain, qui ne valide "
                     "rien"),
          ("imprévu", "« imprévu » : un aléa, qui ne valide rien"),
          ("forfait", "« forfait » : un mode de contrat avec un "
                      "prestataire"))),
        ("t7", "7", "un repère placé dans le planning",
         "jalon",
         (("livrable", "« livrable » : un produit remis, pas un point "
                       "d'arrêt"),
          ("lot", "« lot » : une partie du découpage du travail"),
          ("budget", "« budget » : les moyens financiers alloués"))),
    ),
)


# --------------------------------------------------------------------------
# Texte 5 : la définition du périmètre
# --------------------------------------------------------------------------

PERIMETRE = trous(
    "mprj_perimetre", "La définition du périmètre",
    "Complète le texte sur les étapes de la définition du périmètre.",
    2,
    rappel("le management du périmètre"),
    """Définir le périmètre suit trois étapes : (1) @t1@ les
besoins (les exigences), (2) @t2@ le périmètre, puis
créer la (3) @t3@.

La définition du périmètre précise, parmi ces exigences,
celles qui seront (4) @t4@ dans le contenu du projet et
celles qui en seront (5) @t5@ ; elle aboutit à la note
de (6) @t6@.""",
    (
        ("t1", "1", "collecter auprès des parties prenantes",
         "recueillir",
         (("valider", "« valider » : approuver ce qui est déjà connu ; il "
                      "faut d'abord connaître les besoins"),
          ("chiffrer", "« chiffrer » : estimer le coût ; cela vient "
                       "après"),
          ("livrer", "« livrer » : remettre un produit ; c'est la fin du "
                     "projet, pas son début"))),
        ("t2", "2", "délimiter, fixer ce qui est couvert",
         "définir",
         (("clôturer", "« clôturer » : fermer ; on est au début du "
                       "projet"),
          ("facturer", "« facturer » : réclamer un paiement"),
          ("auditer", "« auditer » : examiner un existant, pas le "
                      "délimiter"))),
        ("t3", "3", "le découpage hiérarchique du travail en lots",
         "WBS",
         (("RACI", "« RACI » : la matrice qui répartit les rôles, pas le "
                   "travail en lots"),
          ("recette", "« recette » : la vérification d'un livrable, en fin "
                      "de réalisation"),
          ("clôture", "« clôture » : la fin du projet"))),
        ("t4", "4", "retenues, intégrées",
         "incluses",
         (("exclues", "« exclues » : laissées en dehors ; c'est l'autre "
                      "catégorie"),
          ("facturées", "« facturées » : payées ; cela ne dit pas si elles "
                        "font partie du projet"),
          ("archivées", "« archivées » : rangées pour mémoire ; cela ne dit "
                        "pas si elles font partie du projet"))),
        ("t5", "5", "laissées en dehors",
         "exclues",
         (("incluses", "« incluses » : retenues ; c'est l'autre "
                       "catégorie"),
          ("livrées", "« livrées » : remises au client ; une exigence "
                      "écartée ne l'est pas"),
          ("validées", "« validées » : approuvées ; cela ne dit pas si "
                       "elles sont retenues"))),
        ("t6", "6", "le document qui fixe objectifs, périmètre et "
                    "contraintes au lancement",
         "cadrage",
         (("frais", "« note de frais » : le remboursement d'une dépense"),
          ("service", "« note de service » : une consigne interne de la "
                      "hiérarchie"),
          ("honoraires", "« note d'honoraires » : la facture d'un "
                         "prestataire"))),
    ),
)


# --------------------------------------------------------------------------
# Texte 6 : la matrice RACI
# --------------------------------------------------------------------------

RACI = trous(
    "mprj_raci", "La matrice RACI",
    "Complète le texte qui explique les quatre lettres de la matrice "
    "RACI.",
    2,
    rappel("la matrice RACI"),
    """Dans la matrice RACI, « R » ((1) @t1@) désigne celui qui
(2) @t2@ l'activité ; « A » ((3) @t3@) celui qui prend la
responsabilité du (4) @t4@ ; « C » ((5) @t5@) les personnes
consultées pour leur (6) @t6@ ; « I » ((7) @t7@) celles qui
sont informées de l'avancement sans (8) @t8@ directement
au travail.""",
    (
        ("t1", "1", "le mot anglais de la lettre R",
         "Responsible",
         (("Accountable", "« Accountable » commence par A : celui qui rend "
                          "des comptes"),
          ("Consulted", "« Consulted » commence par C : celui qu'on "
                        "consulte"),
          ("Informed", "« Informed » commence par I : celui qu'on "
                       "informe"))),
        ("t2", "2", "exécute, fait le travail",
         "réalise",
         (("valide", "« valider » : approuver ; ce n'est pas faire le "
                     "travail"),
          ("observe", "« observer » : regarder sans agir"),
          ("finance", "« financer » : payer ; ce n'est pas faire le "
                      "travail"))),
        ("t3", "3", "le mot anglais de la lettre A",
         "Accountable",
         (("Responsible", "« Responsible » commence par R : celui qui "
                          "exécute"),
          ("Consulted", "« Consulted » commence par C : celui qu'on "
                        "consulte"),
          ("Informed", "« Informed » commence par I : celui qu'on "
                       "informe"))),
        ("t4", "4", "ce qui est obtenu à la fin",
         "résultat",
         (("matériel", "« matériel » : l'équipement ; ce n'est pas ce dont "
                       "on rend compte"),
          ("recrutement", "« recrutement » : l'embauche de personnes"),
          ("transport", "« transport » : le déplacement de biens ou de "
                        "personnes"))),
        ("t5", "5", "le mot anglais de la lettre C",
         "Consulted",
         (("Responsible", "« Responsible » commence par R : celui qui "
                          "exécute"),
          ("Accountable", "« Accountable » commence par A : celui qui rend "
                          "des comptes"),
          ("Informed", "« Informed » commence par I : celui qu'on "
                       "informe"))),
        ("t6", "6", "leurs compétences, leur savoir",
         "expertise",
         (("signature", "« signature » : approuver formellement, c'est le "
                        "rôle d'une autre lettre"),
          ("disponibilité", "« disponibilité » : avoir du temps libre ; on "
                            "consulte quelqu'un pour ce qu'il sait"),
          ("budget", "« budget » : des moyens financiers ; on consulte "
                     "quelqu'un pour ce qu'il sait"))),
        ("t7", "7", "le mot anglais de la lettre I",
         "Informed",
         (("Responsible", "« Responsible » commence par R : celui qui "
                          "exécute"),
          ("Accountable", "« Accountable » commence par A : celui qui rend "
                          "des comptes"),
          ("Consulted", "« Consulted » commence par C : celui qu'on "
                        "consulte"))),
        ("t8", "8", "prendre part",
         "participer",
         (("s'opposer", "« s'opposer » : bloquer ; cela ne décrit pas le "
                        "rôle de la lettre I"),
          ("voter", "« voter » : décider à plusieurs ; la matrice ne parle "
                    "pas de vote"),
          ("être payées", "« être payées » : recevoir un salaire ; cela "
                          "ne décrit pas le rôle de la lettre I"))),
    ),
)


# --------------------------------------------------------------------------
# Texte 7 : la gouvernance du projet
# --------------------------------------------------------------------------

COMITES = ("COPIL", "COPROJ", "COMOP", "CODIR")

SENS_COMITE = {
    "COPIL": "« COPIL » : le comité de pilotage",
    "COPROJ": "« COPROJ » : le comité de projet",
    "COMOP": "« COMOP » : le comité opérationnel",
    "CODIR": "« CODIR » : le comité de direction de l'entreprise, qui "
             "n'est pas un comité du projet",
}


def _comite(trou, label, attendu, juste):
    faux = tuple((c, SENS_COMITE[c]) for c in COMITES if c != juste)
    return (trou, label, attendu, juste, faux)


FREQUENCES = ("mensuelle", "hebdomadaire", "quotidienne", "annuelle")

SENS_FREQUENCE = {
    "mensuelle": "« mensuelle » : une fois par mois",
    "hebdomadaire": "« hebdomadaire » : une fois par semaine",
    "quotidienne": "« quotidienne » : tous les jours",
    "annuelle": "« annuelle » : une fois par an, bien trop rare pour "
                "piloter un projet",
}


def _frequence(trou, label, attendu, juste):
    faux = tuple((f, SENS_FREQUENCE[f]) for f in FREQUENCES if f != juste)
    return (trou, label, attendu, juste, faux)


GOUVERNANCE = trous(
    "mprj_gouvernance", "La gouvernance du projet",
    "Complète le texte sur les trois niveaux de comités d'un projet SI.",
    2,
    rappel("la gouvernance du projet"),
    """La gouvernance d'un projet SI s'organise autour de trois niveaux
de comités :
- le (1) @t1@, de fréquence (2) @t2@, qui valide les grandes
  décisions et s'assure de l'(3) @t3@ stratégique ;
- le (4) @t4@, de fréquence (5) @t5@, qui suit l'avancement
  détaillé ;
- le (6) @t6@, de fréquence (7) @t7@, qui résout les problèmes
  techniques et métier.""",
    (
        _comite("t1", "1", "le comité de pilotage", "COPIL"),
        _frequence("t2", "2", "une fois par mois", "mensuelle"),
        ("t3", "3", "la cohérence avec les objectifs de l'entreprise",
         "alignement",
         (("hébergement", "« hébergement » : l'endroit où tournent les "
                          "serveurs, une question technique"),
          ("inventaire", "« inventaire » : la liste du matériel"),
          ("isolement", "« isolement » : l'absence de lien, le contraire "
                        "de ce que vérifie ce comité"))),
        _comite("t4", "4", "le comité de projet", "COPROJ"),
        _frequence("t5", "5", "une fois par semaine", "hebdomadaire"),
        _comite("t6", "6", "le comité opérationnel", "COMOP"),
        _frequence("t7", "7", "tous les jours", "quotidienne"),
    ),
)


# --------------------------------------------------------------------------
# Texte 8 : le management des risques
# --------------------------------------------------------------------------

RISQUES = trous(
    "mprj_risques", "Le management des risques",
    "Complète le texte sur les étapes du management des risques et les "
    "réponses à un risque.",
    3,
    rappel("le management des risques"),
    """Le management des risques comporte quatre étapes :
l'(1) @t1@ des risques, leur (2) @t2@ et leur évaluation,
la définition des plans de (3) @t3@, puis le (4) @t4@.

La criticité d'un risque se calcule en multipliant sa
(5) @t5@ par son (6) @t6@.

Face à un risque, on peut le (7) @t7@, en (8) @t8@ la
responsabilité à un tiers, ou l'(9) @t9@.""",
    (
        ("t1", "1", "le repérage, la liste des risques",
         "identification",
         (("acceptation", "« acceptation » : une réponse à un risque déjà "
                          "connu, pas une étape"),
          ("assurance", "« assurance » : un moyen de se couvrir, pas une "
                        "étape"),
          ("oubli", "« oubli » : le contraire de ce qu'on cherche"))),
        ("t2", "2", "l'étude de leurs causes et de leurs effets",
         "analyse",
         (("facturation", "« facturation » : la demande de paiement"),
          ("suppression", "« suppression » : on ne supprime pas un risque "
                          "par décret ; cette étape vient avant toute "
                          "réponse"),
          ("publication", "« publication » : la diffusion à l'extérieur"))),
        ("t3", "3", "les solutions de repli si le risque survient",
         "contournement",
         (("communication", "« plan de communication » : il relève de la "
                            "conduite du changement"),
          ("formation", "« plan de formation » : il relève de la conduite "
                        "du changement"),
          ("charge", "« plan de charge » : la répartition du travail entre "
                     "les personnes"))),
        ("t4", "4", "la surveillance dans la durée",
         "suivi",
         (("bilan", "« bilan » : il se fait une fois, à la fin du "
                    "projet"),
          ("transfert", "« transfert » : une réponse à un risque, pas une "
                        "étape"),
          ("classement", "« classement » : ranger un dossier, ce n'est pas "
                         "le surveiller"))),
        ("t5", "5", "la chance qu'il se produise",
         "probabilité",
         (("durée", "« durée » : le temps ; elle n'entre pas dans le "
                    "calcul"),
          ("date", "« date » : le jour où il survient ; elle n'entre pas "
                   "dans le calcul"),
          ("cause", "« cause » : ce qui le provoque ; on ne multiplie pas "
                    "une cause"))),
        ("t6", "6", "la gravité de ses conséquences",
         "impact",
         (("propriétaire", "« propriétaire » : la personne chargée de "
                           "suivre le risque"),
          ("numéro", "« numéro » : son rang dans le registre, qui ne dit "
                     "rien de sa criticité"),
          ("historique", "« historique » : ce qui s'est passé avant"))),
        ("t7", "7", "en diminuer la probabilité ou l'impact",
         "réduire",
         (("aggraver", "« aggraver » : le rendre pire"),
          ("cacher", "« cacher » : le dissimuler ; il reste entier"),
          ("multiplier", "« multiplier » : en augmenter le nombre"))),
        ("t8", "8", "confier à un autre (assureur, sous-traitant)",
         "transférer",
         (("refuser", "« refuser » : ne pas vouloir la prendre ; elle ne "
                      "disparaît pas pour autant"),
          ("cacher", "« cacher » : la dissimuler"),
          ("partager", "« partager » : la garder en partie ; la phrase dit "
                       "qu'elle passe à un tiers"))),
        ("t9", "9", "le garder en connaissance de cause",
         "accepter",
         (("ignorer", "« ignorer » : ne pas s'en occuper, sans l'avoir "
                      "analysé ; ce n'est pas une réponse"),
          ("oublier", "« oublier » : le perdre de vue ; ce n'est pas une "
                      "réponse"),
          ("aggraver", "« aggraver » : le rendre pire"))),
    ),
)


# --------------------------------------------------------------------------
# Texte 9 : le management des coûts
# --------------------------------------------------------------------------

COUTS = trous(
    "mprj_couts", "Le management des coûts",
    "Complète le texte sur les contrats, le coût d'une ressource et le "
    "budget.",
    3,
    rappel("le management des coûts"),
    """Le (1) @t1@ engage le prestataire sur une obligation de
(2) @t2@, alors que la (3) @t3@ correspond à une
obligation de (4) @t4@.

Le (5) @t5@ est le coût journalier moyen d'une ressource,
interne ou externe.

Le budget additionne l'agrégation des coûts, la réserve pour
(6) @t6@ (risques identifiés et acceptés) et la réserve de
(7) @t7@ (risques non identifiés).""",
    (
        ("t1", "1", "le contrat à prix fixé d'avance",
         "forfait",
         (("devis", "« devis » : une estimation chiffrée avant commande, "
                    "pas un mode de contrat"),
          ("jalon", "« jalon » : un point de contrôle du planning"),
          ("lot", "« lot » : une partie du découpage du travail"))),
        ("t2", "2", "le prestataire s'engage sur ce qui est livré",
         "résultat",
         (("moyens", "« moyens » : le prestataire ne s'engage que sur les "
                     "efforts fournis ; c'est l'autre type de contrat"),
          ("présence", "« présence » : ce n'est pas une obligation "
                       "contractuelle du cours"),
          ("discrétion", "« discrétion » : ce n'est pas une obligation qui "
                         "distingue les contrats"))),
        ("t3", "3", "le contrat où l'on paie le temps passé",
         "régie",
         (("recette", "« recette » : la vérification d'un livrable"),
          ("réserve", "« réserve » : une somme mise de côté dans le "
                      "budget"),
          ("facture", "« facture » : la demande de paiement, pas un mode "
                      "de contrat"))),
        ("t4", "4", "le prestataire s'engage sur les efforts fournis",
         "moyens",
         (("résultat", "« résultat » : le prestataire s'engage sur ce qui "
                       "est livré ; c'est l'autre type de contrat"),
          ("délai", "« délai » : ce n'est pas l'une des deux obligations "
                    "du cours"),
          ("secret", "« secret » : ce n'est pas une obligation qui "
                     "distingue les contrats"))),
        ("t5", "5", "le sigle du taux journalier moyen",
         "TJM",
         (("SDSI", "« SDSI » : le schéma directeur du SI"),
          ("WBS", "« WBS » : le découpage du travail en lots"),
          ("REX", "« REX » : le retour d'expérience"))),
        ("t6", "6", "les aléas des risques connus",
         "imprévus",
         (("investissements", "« investissements » : des dépenses "
                              "prévues, pas une réserve pour les "
                              "risques"),
          ("salaires", "« salaires » : ils font partie des coûts déjà "
                       "agrégés"),
          ("bénéfices", "« bénéfices » : ce que l'entreprise gagne, pas "
                        "une réserve"))),
        ("t7", "7", "la réserve tenue par la direction pour l'inconnu",
         "management",
         (("trésorerie", "« trésorerie » : l'argent disponible de "
                         "l'entreprise, hors du budget du projet"),
          ("change", "« change » : la conversion entre monnaies"),
          ("marchandises", "« marchandises » : des biens achetés pour être "
                           "revendus"))),
    ),
)


# --------------------------------------------------------------------------
# Texte 10 : communication, changement et bilan
# --------------------------------------------------------------------------

COMMUNICATION = trous(
    "mprj_communication", "Communication, changement et bilan",
    "Complète le texte sur la communication, la conduite du changement et "
    "le bilan de projet.",
    3,
    rappel("la communication, la conduite du changement et le bilan de "
           "projet"),
    """La communication (1) @t1@ est la plus efficace pour assurer
une même compréhension par tous ; la communication (2) @t2@
garantit la diffusion, mais pas la compréhension.

La conduite du changement vise l'(3) @t3@ du nouveau SI par
les (4) @t4@ ; ses livrables sont le plan de (5) @t5@,
le plan de (6) @t6@ et les supports de formation.

Enfin, le bilan de projet (ou (7) @t7@) permet de (8) @t8@
les leçons apprises, sans chercher à désigner des (9) @t9@.""",
    (
        ("t1", "1", "un échange dans les deux sens, en direct (réunion, "
                    "appel)",
         "interactive",
         (("push", "« push » : on envoie l'information, sans échange"),
          ("pull", "« pull » : on met l'information à disposition, chacun "
                   "va la chercher"),
          ("écrite", "« écrite » : un support, pas un mode d'échange "
                     "du cours"))),
        ("t2", "2", "l'information est envoyée aux destinataires (courriel, "
                    "note)",
         "push",
         (("interactive", "« interactive » : un échange en direct, qui "
                          "assure la compréhension"),
          ("pull", "« pull » : l'information attend qu'on vienne la "
                   "chercher ; rien ne garantit qu'elle soit reçue"),
          ("orale", "« orale » : un support, pas un mode d'échange du "
                    "cours"))),
        ("t3", "3", "le fait de faire sien, d'adopter",
         "appropriation",
         (("installation", "« installation » : une opération technique ; "
                           "un SI installé n'est pas forcément adopté"),
          ("achat", "« achat » : l'acquisition, pas l'adoption"),
          ("exportation", "« exportation » : la vente à l'étranger"))),
        ("t4", "4", "ceux qui se serviront du SI",
         "utilisateurs",
         (("fournisseurs", "« fournisseurs » : ils vendent à l'entreprise ; "
                           "ils ne travaillent pas avec le nouveau SI"),
          ("actionnaires", "« actionnaires » : les propriétaires du capital"),
          ("concurrents", "« concurrents » : les autres entreprises du "
                          "marché"))),
        ("t5", "5", "informer et expliquer le changement",
         "communication",
         (("formation", "« plan de formation » : il développe les "
                        "compétences, ce n'est pas la ligne attendue"),
          ("charge", "« plan de charge » : la répartition du travail"),
          ("contournement", "« plan de contournement » : il relève du "
                            "management des risques"))),
        ("t6", "6", "développer les compétences",
         "formation",
         (("communication", "« plan de communication » : il informe et "
                            "explique, ce n'est pas la ligne attendue"),
          ("financement", "« plan de financement » : il dit d'où vient "
                          "l'argent"),
          ("contournement", "« plan de contournement » : il relève du "
                            "management des risques"))),
        ("t7", "7", "le retour d'expérience",
         "REX / RETEX",
         (("SDSI", "« SDSI » : le schéma directeur du SI"),
          ("PV", "« PV » : un procès-verbal de réunion"),
          ("TJM", "« TJM » : le taux journalier moyen"))),
        ("t8", "8", "garder et réutiliser pour les projets suivants",
         "capitaliser",
         (("oublier", "« oublier » : le contraire de ce que vise le "
                      "bilan"),
          ("facturer", "« facturer » : réclamer un paiement"),
          ("masquer", "« masquer » : cacher ; le bilan partage les "
                      "leçons"))),
        ("t9", "9", "ceux à qui l'on reprocherait les erreurs",
         "responsables",
         (("volontaires", "« volontaires » : ceux qui se proposent ; ce "
                          "n'est pas ce que le bilan évite"),
          ("gagnants", "« gagnants » : ceux qui l'emportent ; un bilan "
                       "n'est pas un concours"),
          ("successeurs", "« successeurs » : ceux qui reprennent le "
                          "projet ; le bilan leur sert justement"))),
    ),
)


PATTERNS = (
    PROJET_SI, TRIANGLE, VISION, CYCLE, PERIMETRE,
    RACI, GOUVERNANCE, RISQUES, COUTS, COMMUNICATION,
)

MODULE = Module(
    key="mngt_prj_trous",
    title="Mgt-Prj_textes à compléter",
    level=2,
    summary="Dix textes à trous pour réviser le management de projet SI : "
            "projet SI, triangle d'or, de la vision au portefeuille, cycle "
            "AFNOR Z67-101, périmètre, RACI, gouvernance, risques, coûts, "
            "communication et bilan. " + INTITULE,
    keys=tuple(p.key for p in PATTERNS),
)
