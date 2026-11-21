"""Module « Unité 3 » du chapitre Allemand : Freundschaft.

Des exercices de révision sur la troisième unité d'allemand de 3e (LV2) :
se présenter et présenter sa famille, l'apparence (aussehen) et le
jugement (finden + pronom à l'accusatif), le caractère, les adverbes
vielleicht / bestimmt / wahrscheinlich, l'amitié (einander, miteinander,
vertrauen…), le comparatif, les loisirs et les adverbes de fréquence,
l'invitation et l'anniversaire, gefallen et mögen, offrir (schenken :
datif et accusatif), se plaindre avec wenn, les verbes de modalité et
sollen, le conseil (Du solltest…, l'impératif).

Les phrases sont écrites pour l'exercice, dans l'esprit du cours : on en
tire des exercices, pas des extraits. Les deux formes d'exercice (phrases
à trous, questions) et leurs indices sont décrites dans `allemand_commun`.
"""

from functools import partial

from ..engine import Module
from . import allemand_commun as commun

INTITULE = commun.intitule(3)

trous = partial(commun.trous, INTITULE)
question = partial(commun.question, INTITULE)


# --------------------------------------------------------------------------
# Séance 1 : se présenter, la famille, l'apparence
# --------------------------------------------------------------------------

PRESENTATION = trous(
    "all_u03_presentation", "Se présenter",
    "Lena pose des questions au nouveau, Simon. Complète.",
    1,
    ("Le nom : Wie heißt du? — Ich heiße… L'âge : Wie alt bist du? — Ich "
     "bin 14 (Jahre alt).",
     "Le domicile : Wo wohnst du? — Ich wohne in Berlin. L'origine : "
     "Woher kommst du? — Ich komme aus Deutschland."),
    """Lena:  Wie @p1@ du?            Simon: Ich heiße Simon.
Lena:  Wie @p2@ bist du?        Simon: Ich bin 14.
Lena:  @p3@ wohnst du?          Simon: In Berlin.
Lena:  @p4@ kommst du?          Simon: Aus Deutschland.
Simon: Und du? Ich komme @p5@ Frankreich.""",
    (
        ("p1", "1", "comment t'appelles-tu ?",
         "heißt",
         (("heiße", "« heiße » va avec « ich » ; Lena parle à « du »"),
          ("heißen", "« heißen » est l'infinitif, ou la forme de wir / "
                     "sie"),
          ("bist", "« Wie bist du? » demande comment tu es (ton "
                   "caractère), pas ton nom"))),
        ("p2", "2", "quel âge as-tu ?",
         "alt",
         (("groß", "« groß » : grand ; on demanderait ta taille"),
          ("viel", "« viel » : beaucoup"),
          ("spät", "« Wie spät ist es? » demande l'heure"))),
        ("p3", "3", "où habites-tu ?",
         "Wo",
         (("Woher", "« Woher » demande d'où l'on vient"),
          ("Wohin", "« Wohin » demande où l'on va"),
          ("Wer", "« Wer » demande qui"))),
        ("p4", "4", "d'où viens-tu ?",
         "Woher",
         (("Wo", "« Wo » demande où l'on est ; la réponse commence par "
                 "« aus »"),
          ("Wohin", "« Wohin » demande où l'on va"),
          ("Wann", "« Wann » demande quand"))),
        ("p5", "5", "je viens de France",
         "aus",
         (("von", "pour dire son origine (pays, ville), la préposition "
                  "n'est pas « von »"),
          ("nach", "« nach » dit où l'on va"),
          ("in", "« in » dit où l'on est"))),
    ),
)

FAMILLE = trous(
    "all_u03_famille", "La famille",
    "Simon présente sa famille. Complète avec le mot qui convient.",
    1,
    ("die Großeltern : les grands-parents — die Eltern : les parents — "
     "die Kinder : les enfants — die Geschwister : les frères et sœurs.",
     "der Zwillingsbruder : le frère jumeau (même âge) — das "
     "Einzelkind : l'enfant unique, qui n'a pas de frères et sœurs."),
    """Die Eltern meiner Eltern sind meine @f1@.
Tim und ich sind gleich alt: Tim ist mein @f2@.
Lisa hat keine Geschwister: Sie ist ein @f3@.
Mein Bruder und meine Schwester sind meine @f4@.""",
    (
        ("f1", "1", "mes grands-parents",
         "Großeltern",
         (("Geschwister", "« die Geschwister » : les frères et sœurs"),
          ("Eltern", "« die Eltern » : les parents ; ici, ce sont les "
                     "parents des parents"),
          ("Kinder", "« die Kinder » : les enfants"))),
        ("f2", "2", "mon frère jumeau",
         "Zwillingsbruder",
         (("Cousin", "« der Cousin » : le cousin"),
          ("Vater", "« der Vater » : le père"),
          ("Opa", "« der Opa » : le grand-père"))),
        ("f3", "3", "une enfant unique",
         "Einzelkind",
         (("Baby", "« das Baby » : le bébé"),
          ("Enkelkind", "« das Enkelkind » : le petit-enfant"),
          ("Zwilling", "« der Zwilling » : le jumeau ; Lisa n'a ni frère "
                       "ni sœur"))),
        ("f4", "4", "mes frères et sœurs",
         "Geschwister",
         (("Eltern", "« die Eltern » : les parents"),
          ("Großeltern", "« die Großeltern » : les grands-parents"),
          ("Freunde", "« die Freunde » : les amis"))),
    ),
)

REGLE_ACCUSATIF = (
    "Après « finden » (trouver), la personne jugée est complément d'objet : "
    "elle est à l'**accusatif**.",
    "Pronoms à l'accusatif : er → ihn, sie → sie, es → es, sie (pluriel) "
    "→ sie. Seul le masculin change.",
)

PRONOMS = trous(
    "all_u03_pronoms", "Je le trouve…",
    "Chacun donne son avis. Remplace la personne par le bon pronom.",
    2,
    REGLE_ACCUSATIF + (
        "Attention au genre allemand : « das Baby » est neutre, même si "
        "« le bébé » est masculin en français.",),
    """1. Simon sieht toll aus. Lena findet @a1@ cool.
2. Isabella ist nett. Anton findet @a2@ sympathisch.
3. Das Baby ist lieb. Die Mutter findet @a3@ süß.
4. Die zwei Jungs sehen intelligent aus. Frau Müller findet @a4@ klug.""",
    (
        ("a1", "Simon", "le (un garçon)",
         "ihn",
         (("er", "« er » est le pronom sujet ; après « finden », le "
                 "complément est à l'accusatif"),
          ("sie", "« sie » renvoie à une fille ou à un pluriel ; Simon "
                  "est un garçon"),
          ("ihm", "« ihm » est un datif ; « finden » demande "
                  "l'accusatif"))),
        ("a2", "Isabella", "la (une fille)",
         "sie",
         (("ihn", "« ihn » renvoie à un garçon ; Isabella est une "
                  "fille"),
          ("ihr", "« ihr » est un datif ; « finden » demande "
                  "l'accusatif"),
          ("er", "« er » est un pronom sujet masculin"))),
        ("a3", "Baby", "le (das Baby, neutre)",
         "es",
         (("ihn", "« le bébé » est masculin en français, mais quel est "
                  "le genre de « das Baby » ?"),
          ("sie", "« sie » renvoie à une fille ou à un pluriel"),
          ("ihm", "« ihm » est un datif ; « finden » demande "
                  "l'accusatif"))),
        ("a4", "Jungs", "les (pluriel)",
         "sie",
         (("ihnen", "« ihnen » est un datif pluriel ; « finden » demande "
                    "l'accusatif"),
          ("ihn", "« ihn » renvoie à un seul garçon ; ici ils sont "
                  "deux"),
          ("es", "« es » renvoie à un neutre singulier"))),
    ),
)

Q_WOHER = question(
    "all_u03_q_woher", "Woher?",
    "Que veut dire « Woher kommst du? » ?",
    "D'où viens-tu ?",
    "« woher » demande l'origine : on répond avec « aus » (Ich komme aus "
    "Frankreich).",
    (("Où habites-tu ?", "« Où habites-tu ? » se dit « Wo wohnst du? ». "
                         "Que demande le « her » de « woher » ?"),
     ("Où vas-tu ?", "« Où vas-tu ? » se dit « Wohin gehst du? »."),
     ("Quand viens-tu ?", "« Quand » se dit « wann ».")),
    level=1,
)

Q_AUSSEHEN = question(
    "all_u03_q_aussehen", "Il a l'air…",
    "Comment dit-on « Il a l'air cool » ?",
    "Er sieht cool aus.",
    "« aussehen » (avoir l'air) est à particule séparable : le verbe "
    "conjugué en 2e position, « aus » à la fin.",
    (("Er aussieht cool.", "« aussehen » est à particule séparable : au "
                           "présent, la particule ne reste pas collée au "
                           "verbe."),
     ("Er sieht aus cool.", "La particule est bien séparée, mais elle va "
                            "tout à la fin de la phrase."),
     ("Er ist cool aus.", "« avoir l'air » ne se construit pas avec "
                          "« sein » : quel verbe porte la particule "
                          "« aus » ?")),
    level=2,
)

Q_IHN = question(
    "all_u03_q_ihn", "Le pronom après finden",
    "« Lena findet Simon toll. » Remplace « Simon » par un pronom.",
    "Lena findet ihn toll.",
    "Simon est le complément de « finden » : accusatif masculin, ihn.",
    (("Lena findet er toll.", "« er » est le pronom sujet. Simon est-il "
                              "le sujet de la phrase ?"),
     ("Lena findet ihm toll.", "« ihm » est un datif ; « finden » "
                               "demande un autre cas."),
     ("Lena findet sie toll.", "« sie » renverrait à une fille. Simon "
                               "est un garçon.")),
    level=2, rappel=REGLE_ACCUSATIF,
)

Q_EINZELKIND = question(
    "all_u03_q_einzelkind", "Einzelkind",
    "Que veut dire « Ich bin Einzelkind » ?",
    "Je n'ai ni frère ni sœur.",
    "« das Einzelkind » : l'enfant unique (einzeln : seul, un par un).",
    (("Je suis l'aîné.", "Le mot ne parle pas d'âge. Décompose-le : "
                         "einzel… Kind."),
     ("J'ai un frère jumeau.", "Le frère jumeau se dit « der "
                               "Zwillingsbruder »."),
     ("Je suis encore un enfant.", "« Kind » veut bien dire enfant, mais "
                                   "« einzel- » précise quelque chose de "
                                   "plus.")),
    level=1,
)

Q_JUGEND = question(
    "all_u03_q_jugend", "La langue des jeunes",
    "Que veut dire « Das geht gar nicht! » ?",
    "Ça ne va pas du tout, c'est impossible !",
    "« Das geht gar nicht! » : ce n'est pas possible, ça ne va pas du "
    "tout. « gar nicht » renforce la négation.",
    (("Ça marche !", "La phrase contient une négation renforcée : « gar "
                     "nicht »."),
     ("Il ne marche pas du tout.", "« gehen » veut dire marcher, mais ici "
                                   "le sujet est « das » : ce n'est pas "
                                   "une personne qui marche."),
     ("Je n'y vais pas.", "Le sujet est « das » (cela), pas « ich ».")),
    level=2,
)


# --------------------------------------------------------------------------
# Séance 2 : le caractère, vielleicht / bestimmt / wahrscheinlich
# --------------------------------------------------------------------------

CARACTERE_1 = trous(
    "all_u03_caractere1", "Le caractère (1)",
    "Quel est le caractère de chacun ? Choisis l'adjectif qui convient.",
    1,
    ("kontaktfreudig : sociable ≠ schüchtern : timide — gesprächig : "
     "bavard — hilfsbereit : serviable — neugierig : curieux — launisch : "
     "lunatique (die Laune : l'humeur).",
     "Pour deviner un mot, cherche le mot qu'il contient : gesprächig → "
     "sprechen, hilfsbereit → die Hilfe, neugierig → neu."),
    """Lena redet sehr viel. Sie ist @c1@.
Max spricht nicht gern mit fremden Leuten. Er ist @c2@.
Anna hilft immer allen. Sie ist @c3@.
Tim stellt immer Fragen. Er ist @c4@.
Mal hat Julia gute Laune, mal schlechte. Sie ist @c5@.""",
    (
        ("c1", "Lena", "bavarde",
         "gesprächig",
         (("schüchtern", "« schüchtern » : timide"),
          ("launisch", "« launisch » : lunatique"),
          ("faul", "« faul » : paresseux"))),
        ("c2", "Max", "timide",
         "schüchtern",
         (("kontaktfreudig", "« kontaktfreudig » : sociable, qui aime le "
                             "contact ; c'est le contraire"),
          ("neugierig", "« neugierig » : curieux"),
          ("lustig", "« lustig » : drôle"))),
        ("c3", "Anna", "serviable",
         "hilfsbereit",
         (("ungeduldig", "« ungeduldig » : impatient"),
          ("chaotisch", "« chaotisch » : désordonné"),
          ("fleißig", "« fleißig » : appliqué, travailleur"))),
        ("c4", "Tim", "curieux",
         "neugierig",
         (("gesprächig", "« gesprächig » : bavard ; Tim veut surtout "
                         "savoir"),
          ("geduldig", "« geduldig » : patient"),
          ("tierlieb", "« tierlieb » : qui aime les animaux"))),
        ("c5", "Julia", "lunatique",
         "launisch",
         (("lustig", "« lustig » : drôle"),
          ("ordentlich", "« ordentlich » : ordonné"),
          ("kreativ", "« kreativ » : créatif"))),
    ),
)

CARACTERE_2 = trous(
    "all_u03_caractere2", "Le caractère (2)",
    "Chacun se décrit. Choisis l'adjectif qui convient.",
    1,
    ("fleißig : appliqué ≠ faul : paresseux — ordentlich : ordonné ≠ "
     "chaotisch : désordonné — geduldig : patient ≠ ungeduldig : "
     "impatient.",
     "tierlieb : qui aime les animaux (das Tier) — naturliebend : qui aime "
     "la nature — lustig : drôle."),
    """Ich mache immer meine Hausaufgaben. Ich bin @d1@.
Mein Schreibtisch ist immer aufgeräumt. Ich bin @d2@.
Ich warte nicht gern. Ich bin @d3@.
Ich liebe Katzen und Hunde. Ich bin @d4@.
Ich mache gern Witze. Ich bin @d5@.""",
    (
        ("d1", "1", "appliqué",
         "fleißig",
         (("faul", "« faul » : paresseux, c'est le contraire"),
          ("kreativ", "« kreativ » : créatif"),
          ("musikalisch", "« musikalisch » : doué pour la musique"))),
        ("d2", "2", "ordonné",
         "ordentlich",
         (("chaotisch", "« chaotisch » : désordonné, c'est le contraire"),
          ("faul", "« faul » : paresseux"),
          ("neugierig", "« neugierig » : curieux"))),
        ("d3", "3", "impatient",
         "ungeduldig",
         (("geduldig", "« geduldig » : patient ; c'est le contraire de "
                       "ce qu'on cherche"),
          ("schüchtern", "« schüchtern » : timide"),
          ("launisch", "« launisch » : lunatique"))),
        ("d4", "4", "j'aime les animaux",
         "tierlieb",
         (("naturliebend", "« naturliebend » : qui aime la nature "
                           "(die Natur)"),
          ("sportlich", "« sportlich » : sportif"),
          ("kontaktfreudig", "« kontaktfreudig » : sociable"))),
        ("d5", "5", "drôle",
         "lustig",
         (("langweilig", "« langweilig » : ennuyeux"),
          ("launisch", "« launisch » : lunatique"),
          ("faul", "« faul » : paresseux"))),
    ),
)

REGLE_ADVERBES = (
    "vielleicht : peut-être — bestimmt : certainement, sûrement — "
    "wahrscheinlich : probablement.",
    "Dans la phrase, l'adverbe se place juste après le verbe conjugué : "
    "Simon ist bestimmt fleißig. Il peut aussi ouvrir la phrase : le "
    "verbe reste alors en 2e position (Vielleicht passt Tim…).",
)

ADVERBES = trous(
    "all_u03_adverbes", "Peut-être, sûrement, probablement",
    "Lena devine à quel groupe de la classe vont les jumeaux. Complète.",
    2,
    REGLE_ADVERBES,
    """1. Simon ist @v1@ fleißig.
2. Tim passt @v2@ zu den Sportlichen.
3. Simon ist @v3@ rebellisch.""",
    (
        ("v1", "1", "certainement",
         "bestimmt",
         (("vielleicht", "« vielleicht » : peut-être, c'est moins sûr"),
          ("wahrscheinlich", "« wahrscheinlich » : probablement"),
          ("nie", "« nie » : jamais"))),
        ("v2", "2", "peut-être",
         "vielleicht",
         (("bestimmt", "« bestimmt » : certainement, c'est plus sûr"),
          ("immer", "« immer » : toujours"),
          ("selten", "« selten » : rarement"))),
        ("v3", "3", "probablement",
         "wahrscheinlich",
         (("vielleicht", "« vielleicht » : peut-être"),
          ("bestimmt", "« bestimmt » : certainement"),
          ("regelmäßig", "« regelmäßig » : régulièrement"))),
    ),
)

Q_ADVERBE = question(
    "all_u03_q_bestimmt", "La place de l'adverbe",
    "Quelle phrase est correcte ?",
    "Simon ist bestimmt fleißig.",
    "L'adverbe « bestimmt » se place juste après le verbe conjugué « ist », "
    "en 3e position.",
    (("Simon bestimmt ist fleißig.", "Le verbe conjugué doit rester en 2e "
                                     "position."),
     ("Bestimmt Simon ist fleißig.", "Si l'adverbe ouvre la phrase, "
                                     "qu'est-ce qui doit venir juste "
                                     "après ?"),
     ("Simon bestimmt fleißig ist.", "Le verbe conjugué ne va à la fin "
                                     "que dans une subordonnée.")),
    level=2, rappel=REGLE_ADVERBES,
)

Q_GLAUBE = question(
    "all_u03_q_glaube", "Je crois que…",
    "Quelle phrase est correcte ?",
    "Ich glaube, dass Tim zu den Sportlichen passt.",
    "« Ich glaube, dass… » (je crois que) : une virgule avant « dass », et "
    "le verbe conjugué « passt » à la fin.",
    (("Ich glaube, dass Tim passt zu den Sportlichen.",
      "C'est l'ordre d'une phrase principale. Où va le verbe conjugué "
      "après « dass » ?"),
     ("Ich glaube, weil Tim zu den Sportlichen passt.",
      "« weil » veut dire « parce que » : « je crois parce que… » ne dit "
      "pas ce que tu crois."),
     ("Ich glaube dass, Tim zu den Sportlichen passt.",
      "L'ordre est juste, mais la virgule se place avant la "
      "conjonction.")),
    level=3,
)

Q_PASSEN = question(
    "all_u03_q_passen", "Aller avec un groupe",
    "Complète : « Tim passt ____ den Sportlichen, weil er sportlich ist. »",
    "zu",
    "« passen zu » (+ datif) : aller avec, correspondre à → Tim passt zu "
    "den Sportlichen, zur Gruppe der Sportlichen.",
    (("mit", "« mit » veut dire « avec » : Tim serait avec eux, mais "
             "« passen » demande une autre préposition."),
     ("für", "« für » veut dire « pour »."),
     ("an", "« an » veut dire « à, contre » : ce n'est pas la préposition "
            "de « passen ».")),
    level=2,
)

Q_SCHUECHTERN = question(
    "all_u03_q_contraire", "Les contraires",
    "Quel est le contraire de « kontaktfreudig » (sociable) ?",
    "schüchtern",
    "Celui qui est « schüchtern » (timide) n'aime pas aller vers les "
    "autres : c'est le contraire de « kontaktfreudig ».",
    (("gesprächig", "« gesprächig » (bavard) va plutôt dans le même sens "
                    "que sociable."),
     ("neugierig", "« neugierig » veut dire curieux : ce n'est pas un "
                   "contraire."),
     ("hilfsbereit", "« hilfsbereit » veut dire serviable : ce n'est pas "
                     "un contraire.")),
    level=1,
)


# --------------------------------------------------------------------------
# Séance 3 : l'amitié, einander, le comparatif, sollen
# --------------------------------------------------------------------------

EINANDER = trous(
    "all_u03_einander", "Les uns les autres",
    "Ce que font de bons amis. Complète avec la forme de « einander » qui "
    "convient.",
    3,
    ("« einander » exprime la réciprocité (l'un l'autre). Collé à une "
     "préposition, il en garde le sens : miteinander (l'un avec l'autre, "
     "ensemble), zueinander (l'un envers l'autre), füreinander (l'un pour "
     "l'autre), untereinander (entre eux).",),
    """1. Meine Freunde und ich lachen immer @e1@.
2. Freunde müssen nett @e2@ sein.
3. Wir sind immer @e3@ da.
4. Die Sportlichen motivieren sich @e4@.""",
    (
        ("e1", "1", "ensemble (l'un avec l'autre)",
         "miteinander",
         (("zueinander", "« zu- » : l'un envers l'autre ; on rit avec "
                         "quelqu'un"),
          ("füreinander", "« für- » : l'un pour l'autre"),
          ("untereinander", "« unter- » : entre eux, dans le groupe"))),
        ("e2", "2", "gentils les uns envers les autres",
         "zueinander",
         (("miteinander", "« mit- » : l'un avec l'autre ; on est gentil "
                          "envers quelqu'un"),
          ("füreinander", "« für- » : l'un pour l'autre"),
          ("untereinander", "« unter- » : entre eux"))),
        ("e3", "3", "là les uns pour les autres",
         "füreinander",
         (("miteinander", "« mit- » : l'un avec l'autre ; on dit « für "
                          "jemanden da sein »"),
          ("zueinander", "« zu- » : l'un envers l'autre"),
          ("untereinander", "« unter- » : entre eux"))),
        ("e4", "4", "entre eux",
         "untereinander",
         (("miteinander", "« mit- » : l'un avec l'autre, ensemble"),
          ("zueinander", "« zu- » : l'un envers l'autre"),
          ("füreinander", "« für- » : l'un pour l'autre"))),
    ),
)

AMITIE = trous(
    "all_u03_amitie", "Qu'est-ce que l'amitié ?",
    "Ayse et Anna disent ce qui compte en amitié. Complète.",
    2,
    ("seinem Freund vertrauen (+ datif) : faire confiance à son ami — ein "
     "Geheimnis bewahren : garder un secret — zusammen Spaß haben : "
     "s'amuser ensemble — sich für seinen Freund interessieren : "
     "s'intéresser à son ami — für seinen Freund da sein : être là pour "
     "son ami.",),
    """1. Ich @x1@ meiner Freundin.
2. Eine Freundin muss ein Geheimnis @x2@.
3. Wir haben zusammen @x3@.
4. Ich interessiere mich @x4@ meine Freundin.
5. Eine Freundin ist immer für mich @x5@.""",
    (
        ("x1", "1", "je fais confiance à mon amie",
         "vertraue",
         (("helfe", "« helfen » : aider"),
          ("höre", "« zuhören » : écouter ; il faudrait aussi la "
                   "particule"),
          ("interessiere", "« sich interessieren für » : s'intéresser "
                           "à"))),
        ("x2", "2", "garder un secret",
         "bewahren",
         (("erzählen", "« erzählen » : raconter, c'est tout le "
                       "contraire !"),
          ("haben", "« haben » : avoir ; un secret, on le garde"),
          ("verstehen", "« verstehen » : comprendre"))),
        ("x3", "3", "on s'amuse ensemble",
         "Spaß",
         (("Lust", "« Lust haben » : avoir envie"),
          ("Angst", "« Angst haben » : avoir peur"),
          ("Hunger", "« Hunger haben » : avoir faim"))),
        ("x4", "4", "je m'intéresse à mon amie",
         "für",
         (("an", "« sich interessieren » se construit avec une autre "
                 "préposition"),
          ("mit", "« mit » : avec"),
          ("über", "« über » : au-dessus de, ou à propos de"))),
        ("x5", "5", "elle est là pour moi",
         "da",
         (("dort", "« dort » : là-bas, loin"),
          ("weg", "« weg » : parti, absent ; c'est le contraire"),
          ("zu Hause", "« zu Hause » : à la maison"))),
    ),
)

COMPARATIF = trous(
    "all_u03_comparatif", "Comparer ses amis",
    "Thomas compare ses amis et sa famille. Choisis la forme qui "
    "convient.",
    3,
    ("Comparatif de supériorité : adjectif + -er + als → lustiger als.",
     "Avec un tréma : klug → klüger. Irréguliers : gut → besser, gern → "
     "lieber, viel → mehr.",
     "L'allemand ne forme pas le comparatif avec « mehr » + adjectif : "
     "« mehr » est le comparatif de « viel » (plus de…)."),
    """1. Mein Freund ist @k1@ als ich. (klug)
2. Ich bin @k2@ in Mathe als mein Freund. (gut)
3. Ich spiele @k3@ Basketball als Fußball. (gern)
4. Er macht @k4@ Sport als wir. (viel)
5. Meine Mutter ist @k5@ als mein Vater. (geduldig)""",
    (
        ("k1", "1", "plus intelligent",
         "klüger",
         (("kluger", "« klug » est un adjectif court en u : au "
                     "comparatif, il prend un tréma"),
          ("mehr klug", "l'allemand ne fait pas le comparatif avec "
                        "« mehr »"),
          ("klug", "il manque la marque du comparatif"))),
        ("k2", "2", "meilleur",
         "besser",
         (("guter", "« gut » a un comparatif irrégulier"),
          ("mehr gut", "l'allemand ne fait pas le comparatif avec "
                       "« mehr »"),
          ("gut", "il manque le comparatif"))),
        ("k3", "3", "je préfère (plus volontiers)",
         "lieber",
         (("gerner", "« gern » a un comparatif irrégulier"),
          ("mehr gern", "l'allemand ne fait pas le comparatif avec "
                        "« mehr »"),
          ("gern", "il manque le comparatif"))),
        ("k4", "4", "plus de sport",
         "mehr",
         (("vieler", "« viel » a un comparatif irrégulier"),
          ("viel", "il manque le comparatif"),
          ("weniger", "« weniger » : moins, c'est le contraire"))),
        ("k5", "5", "plus patiente",
         "geduldiger",
         (("mehr geduldig", "l'allemand ne fait pas le comparatif avec "
                            "« mehr »"),
          ("geduldig", "il manque la marque du comparatif"),
          ("ungeduldiger", "« ungeduldig » : impatient, c'est le "
                           "contraire"))),
    ),
)

Q_GEHEIMNIS = question(
    "all_u03_q_geheimnis", "Un secret",
    "Que veut dire « ein Geheimnis bewahren » ?",
    "garder un secret",
    "« bewahren » : garder, conserver. Un bon ami garde les secrets.",
    (("raconter un secret", "« raconter » se dit « erzählen ». "
                            "« bewahren » dit le contraire."),
     ("avoir un secret", "« avoir » se dit « haben »."),
     ("découvrir un secret", "« découvrir » se dit « entdecken » ; "
                             "« bewahren » parle de ce qu'on fait d'un "
                             "secret qu'on connaît déjà.")),
    level=2,
)


# --------------------------------------------------------------------------
# Séances 4 et 5 : les loisirs, les adverbes de fréquence
# --------------------------------------------------------------------------

REGLE_FREQUENCE = (
    "Du moins au plus fréquent : nie (jamais), selten (rarement), "
    "manchmal (parfois), ab und zu (de temps en temps), oft (souvent), "
    "regelmäßig (régulièrement), immer (toujours).",
    "L'adverbe de fréquence se place juste après le verbe conjugué, ou en "
    "tête de phrase : le verbe reste alors en 2e position.",
)

FREQUENCE = trous(
    "all_u03_frequence", "Souvent, parfois, jamais",
    "Jana, Lukas et Martin racontent leur temps libre. Choisis l'adverbe "
    "qui convient.",
    2,
    REGLE_FREQUENCE,
    """1. Jana geht @h1@ ins Kino.
2. Sie geht @h2@ ins Schwimmbad.
3. Lukas geht @h3@ zum Skatepark.
4. Seine Clique geht @h4@ ins Eiscafé.
5. Martin treibt @h5@ Sport.
6. Er geht @h6@ ins Museum.""",
    (
        ("h1", "1", "souvent",
         "oft",
         (("selten", "« selten » : rarement, c'est le contraire"),
          ("nie", "« nie » : jamais"),
          ("manchmal", "« manchmal » : parfois"))),
        ("h2", "2", "parfois",
         "manchmal",
         (("oft", "« oft » : souvent"),
          ("immer", "« immer » : toujours"),
          ("regelmäßig", "« regelmäßig » : régulièrement"))),
        ("h3", "3", "toujours",
         "immer",
         (("nie", "« nie » : jamais, c'est le contraire"),
          ("oft", "« oft » : souvent"),
          ("ab und zu", "« ab und zu » : de temps en temps"))),
        ("h4", "4", "de temps en temps",
         "ab und zu",
         (("selten", "« selten » : rarement"),
          ("regelmäßig", "« regelmäßig » : régulièrement"),
          ("immer", "« immer » : toujours"))),
        ("h5", "5", "régulièrement",
         "regelmäßig",
         (("selten", "« selten » : rarement"),
          ("manchmal", "« manchmal » : parfois"),
          ("nie", "« nie » : jamais"))),
        ("h6", "6", "rarement",
         "selten",
         (("oft", "« oft » : souvent, c'est le contraire"),
          ("nie", "« nie » : jamais ; la cible dit que ça arrive un "
                  "peu"),
          ("immer", "« immer » : toujours"))),
    ),
)

Q_FREQUENCE = question(
    "all_u03_q_manchmal", "La place de l'adverbe de fréquence",
    "Quelle phrase est correcte ?",
    "Manchmal geht Jana ins Kino.",
    "« Manchmal » ouvre la phrase : le verbe conjugué « geht » reste en 2e "
    "position, et le sujet « Jana » passe en 3e.",
    (("Manchmal Jana geht ins Kino.", "Quand l'adverbe est en 1re "
                                      "position, qu'est-ce qui vient "
                                      "juste après ?"),
     ("Jana manchmal geht ins Kino.", "Le verbe conjugué doit rester en 2e "
                                      "position : l'adverbe se place "
                                      "après lui."),
     ("Geht manchmal Jana ins Kino.", "Un verbe en 1re position, c'est la "
                                      "forme d'une question.")),
    level=2, rappel=REGLE_FREQUENCE,
)

Q_SMS = question(
    "all_u03_q_sms", "Un SMS de Markus",
    "Markus écrit : « Lust auf Kino? ». Que te demande-t-il ?",
    "Ça te dit d'aller au cinéma ?",
    "« Lust haben auf… » : avoir envie de… « Lust auf Kino? » est une "
    "proposition de sortie.",
    (("Tu aimes le cinéma ?", "« die Lust » ne parle pas de ce qu'on "
                              "aime en général, mais d'une envie, tout "
                              "de suite."),
     ("Le cinéma est-il ouvert ?", "« Lust » veut dire envie : Markus te "
                                   "demande quelque chose à toi."),
     ("Es-tu allé au cinéma ?", "Il n'y a pas de verbe au passé : Markus "
                                "propose quelque chose.")),
    level=2,
)

Q_LOISIRS = question(
    "all_u03_q_spiele", "Les loisirs",
    "Que veut dire « Gesellschaftsspiele spielen » ?",
    "jouer à des jeux de société",
    "« die Gesellschaft » : la société, « das Spiel » : le jeu. On y joue "
    "à plusieurs, autour d'une table.",
    (("faire du sport en équipe", "« das Spiel » veut dire le jeu, pas le "
                                  "sport ; et « Gesellschaft » ?"),
     ("jouer à des jeux vidéo", "Les jeux vidéo se disent « Videospiele » "
                                "ou « Computerspiele »."),
     ("aller à une fête", "Une fête se dit « die Party » ; ici, on "
                          "« joue ».")),
    level=1,
)


# --------------------------------------------------------------------------
# Séance 6 : l'anniversaire, gefallen et mögen, offrir (schenken)
# --------------------------------------------------------------------------

GEBURTSTAG = trous(
    "all_u03_geburtstag", "L'invitation",
    "Martin invite ses amis à son anniversaire. Complète.",
    2,
    ("Inviter : Ich lade dich zu meinem Geburtstag ein (ein/laden, verbe "
     "à particule séparable).",
     "Ich werde 14 : je vais avoir 14 ans — Ich habe am 23. April "
     "Geburtstag — Ich bin am 10. Dezember geboren.",
     "Répondre : Klar komme ich! / Ich kann leider nicht kommen. Demander "
     "une réponse : Sagt Bescheid, ob ihr kommt!"),
    """Hallo Leute!
Ich @i1@ euch zu meiner Party ein.
Am Samstag @i2@ ich 14!
Ich habe nämlich am 15. Mai @i3@.
@i4@ Bescheid, ob ihr kommt!

Michael: Ich kann leider nicht @i5@.""",
    (
        ("i1", "1", "j'invite (ein/laden, avec « ich »)",
         "lade",
         (("lädt", "« lädt » va avec er, sie, es"),
          ("lädst", "« lädst » va avec « du »"),
          ("einlade", "« einladen » est à particule séparable : la "
                      "particule est déjà à la fin"))),
        ("i2", "2", "je vais avoir (14 ans)",
         "werde",
         (("habe", "en allemand, on n'« a » pas un âge"),
          ("wird", "« wird » va avec er, sie, es"),
          ("werdet", "« werdet » va avec « ihr »"))),
        ("i3", "3", "j'ai mon anniversaire",
         "Geburtstag",
         (("Geschenk", "« das Geschenk » : le cadeau"),
          ("geboren", "« geboren » se construit avec « sein » : ich bin "
                      "… geboren (je suis né)"),
          ("Party", "« die Party » : la fête"))),
        ("i4", "4", "dites-moi (ihr)",
         "Sagt",
         (("Sag", "« Sag » est l'impératif de « du » ; Martin écrit à "
                  "tous ses amis"),
          ("Sagen", "« Sagen » est la forme de wir ou de Sie, avec le "
                    "pronom"),
          ("Ihr sagt", "l'impératif n'a pas de sujet"))),
        ("i5", "5", "venir (infinitif)",
         "kommen",
         (("komme", "après « kann », le second verbe est à "
                    "l'infinitif"),
          ("kommt", "après « kann », le second verbe n'est pas "
                    "conjugué"),
          ("gekommen", "« gekommen » est le participe passé"))),
    ),
)

GEFALLEN = trous(
    "all_u03_gefallen", "Ce qui lui plaît",
    "Les amis cherchent un cadeau pour Martin. Complète.",
    2,
    ("« gefallen » (plaire) : ce qui plaît est le sujet, la personne est "
     "au datif → Kochen gefällt ihm. Les cadeaux gefallen ihm.",
     "« mögen » (aimer) : ich mag, du magst, er mag, wir mögen, ihr mögt, "
     "sie mögen.",
     "« sich interessieren für » : s'intéresser à — « finden » : trouver "
     "(Ich finde Musik toll)."),
    """1. Kochen @l1@ ihm.
2. Er @l2@ sich für Computerspiele.
3. Deutsche Musik @l3@ er toll.
4. Wir @l4@ Martin sehr.
5. Die Geschenke @l5@ ihm bestimmt.""",
    (
        ("l1", "1", "la cuisine lui plaît",
         "gefällt",
         (("mag", "avec « mögen », le sujet est la personne qui aime "
                  "(er mag…) ; ici le sujet est ce qui plaît"),
          ("gefallen", "« gefallen » va avec un sujet pluriel ; "
                       "« Kochen » est singulier"),
          ("interessiert", "« interessieren » se construit avec « sich "
                           "… für »"))),
        ("l2", "2", "il s'intéresse aux jeux vidéo",
         "interessiert",
         (("interessieren", "« interessieren » va avec wir ou sie "
                            "(pluriel)"),
          ("mag", "« mögen » ne se construit pas avec « sich … für »"),
          ("findet", "« finden » ne se construit pas avec « sich … "
                     "für »"))),
        ("l3", "3", "il trouve la musique allemande super",
         "findet",
         (("mag", "« toll » donne un jugement : avec « mögen », on ne "
                  "l'ajoute pas"),
          ("gefällt", "avec « gefallen », la personne est au datif "
                      "(ihm) ; ici le sujet est « er »"),
          ("interessiert", "« interessieren » se construit avec « sich "
                           "… für »"))),
        ("l4", "4", "nous aimons (mögen)",
         "mögen",
         (("mögt", "« mögt » va avec « ihr »"),
          ("mag", "« mag » va avec ich ou er, sie, es"),
          ("magen", "au pluriel, ce verbe garde son ö"))),
        ("l5", "5", "les cadeaux lui plaisent (pluriel)",
         "gefallen",
         (("gefällt", "le bon verbe, mais « gefällt » va avec un sujet "
                      "singulier ; « die Geschenke » est un pluriel"),
          ("mögen", "avec « mögen », le sujet est la personne qui aime ; "
                    "ici le sujet est ce qui plaît"),
          ("gefällst", "« gefällst » va avec « du »"))),
    ),
)

REGLE_SCHENKEN = (
    "« schenken » (offrir) a deux compléments : la personne à qui l'on "
    "offre, au **datif**, et le cadeau, à l'**accusatif** → Ich schenke "
    "meinem Freund einen Helm.",
    "Pronoms au datif : ich → mir, du → dir, er → ihm, sie → ihr, es → "
    "ihm, wir → uns, ihr → euch, sie (pluriel) → ihnen.",
    "Articles au datif : -em (masculin, neutre), -er (féminin), -en "
    "(pluriel). Accusatif masculin : -en (einen, den).",
)

PRONOMS_DATIF = trous(
    "all_u03_pronoms_datif", "Que lui offres-tu ?",
    "Lena et Tim parlent des cadeaux. Complète avec le pronom au datif.",
    3,
    REGLE_SCHENKEN,
    """1. Und dein Bruder? Was schenkst du @g1@?
2. Und deine Mutter? Willst du @g2@ Blumen schenken?
3. Und deine Eltern? Was schenkst du @g3@?
4. Meine Schwester schenkt @g4@ ein Skateboard. (à moi)
5. Dein Meerschweinchen mag Karotten. Schenkst du @g5@ eine Karotte?""",
    (
        ("g1", "Bruder", "lui (masculin)",
         "ihm",
         (("ihn", "« ihn » est l'accusatif ; le frère reçoit le cadeau : "
                  "datif"),
          ("ihr", "« ihr » renvoie à une fille ou une femme"),
          ("ihnen", "« ihnen » renvoie à plusieurs personnes"))),
        ("g2", "Mutter", "lui (féminin)",
         "ihr",
         (("sie", "« sie » est l'accusatif ; la mère reçoit les fleurs : "
                  "datif"),
          ("ihm", "« ihm » renvoie à un masculin ou un neutre"),
          ("ihnen", "« ihnen » renvoie à plusieurs personnes"))),
        ("g3", "Eltern", "leur (pluriel)",
         "ihnen",
         (("sie", "« sie » est l'accusatif ; les parents reçoivent le "
                  "cadeau : datif"),
          ("ihm", "« ihm » renvoie à une seule personne, masculin ou "
                  "neutre"),
          ("ihr", "« ihr » renvoie à une seule personne, féminin"))),
        ("g4", "Moi", "à moi",
         "mir",
         (("mich", "« mich » est l'accusatif ; c'est moi qui reçois : "
                   "datif"),
          ("dir", "« dir » veut dire « à toi »"),
          ("ihr", "« ihr » veut dire « à elle »"))),
        ("g5", "Meerschweinchen", "lui (das Meerschweinchen, neutre)",
         "ihm",
         (("es", "« es » est l'accusatif ; le cochon d'Inde reçoit la "
                 "carotte : datif"),
          ("ihr", "« ihr » renvoie à un féminin ; « das Meerschweinchen » "
                  "est neutre"),
          ("ihn", "« ihn » est un accusatif masculin"))),
    ),
)

ARTICLES = trous(
    "all_u03_articles", "Offrir : datif et accusatif",
    "Qui offre quoi à qui ? Complète chaque mot avec sa marque.",
    3,
    REGLE_SCHENKEN + (
        "Pour chaque trou, demande-toi : est-ce la personne qui reçoit "
        "(datif) ou le cadeau (accusatif) ?",),
    """1. Ich schenke mein@n1@ Mutter ein Buch. (die Mutter)
2. Du schenkst dein@n2@ Vater eine Uhr. (der Vater)
3. Wir schenken d@n3@ Lehrern Schokolade. (die Lehrer, pluriel)
4. Sie schenkt d@n4@ Meerschweinchen einen Käfig. (das Meerschweinchen)
5. Ich schenke meinem Freund ein@n5@ Fahrradhelm. (der Helm)""",
    (
        ("n1", "Mutter", "datif féminin (elle reçoit)",
         "er",
         (("em", "« -em » est la marque du masculin et du neutre ; "
                 "« Mutter » est féminin"),
          ("e", "« meine » n'est pas un datif ; la mère reçoit le "
                "cadeau"),
          ("en", "« -en » est la marque du datif pluriel"))),
        ("n2", "Vater", "datif masculin (il reçoit)",
         "em",
         (("en", "« deinen » est un accusatif : le père reçoit, il n'est "
                 "pas le cadeau"),
          ("er", "« -er » est la marque du féminin ; « Vater » est "
                 "masculin"),
          ("e", "« deine » n'est pas un datif, et « Vater » est "
                "masculin"))),
        ("n3", "Lehrer", "datif pluriel (ils reçoivent)",
         "en",
         (("em", "« -em » est la marque du singulier ; « die Lehrer » "
                 "est un pluriel"),
          ("ie", "« die » n'est pas un datif"),
          ("er", "« -er » est la marque du féminin singulier"))),
        ("n4", "Meerschweinchen", "datif neutre (il reçoit)",
         "em",
         (("as", "« das » n'est pas un datif ; le cochon d'Inde reçoit le "
                 "cadeau"),
          ("er", "« -er » est la marque du féminin ; « Meerschweinchen » "
                 "est neutre"),
          ("en", "« -en » est la marque du pluriel"))),
        ("n5", "Helm", "accusatif masculin (le cadeau)",
         "en",
         (("em", "« -em » est le datif ; le casque est le cadeau, pas "
                 "celui qui reçoit"),
          ("e", "« eine » est un féminin ; « der Helm » est masculin"),
          ("er", "« -er » est la marque du datif féminin"))),
    ),
)

Q_WERDEN = question(
    "all_u03_q_werden", "Je vais avoir 14 ans",
    "Comment dit-on « Je vais avoir 14 ans » ?",
    "Ich werde 14.",
    "« werden » (devenir) : ich werde 14, je vais avoir 14 ans. En "
    "allemand, on n'« a » pas un âge.",
    (("Ich habe 14 Jahre.", "C'est une construction française : en "
                            "allemand, on n'emploie pas « haben » pour "
                            "l'âge."),
     ("Ich bin 14.", "« Ich bin 14 » veut dire « j'ai 14 ans » "
                     "aujourd'hui. Et quand on va les avoir ?"),
     ("Ich werde 14 haben.", "« werden » suffit, sans « haben » : il dit "
                             "déjà ce qu'on va devenir.")),
    level=2,
)

Q_MOEGEN = question(
    "all_u03_q_moegen", "mögen",
    "Complète : « Ihr ____ deutsche Musik. » (mögen, au présent)",
    "mögt",
    "mögen : ich mag, du magst, er mag, wir mögen, ihr mögt, sie mögen.",
    (("mögen", "« mögen » va avec wir ou sie (pluriel) ; le sujet est "
               "« ihr »."),
     ("mag", "« mag » va avec ich ou er, sie, es."),
     ("magt", "Au pluriel, ce verbe garde son ö : seuls ich, du, er "
              "changent de voyelle.")),
    level=2,
)

Q_DATIF = question(
    "all_u03_q_datif", "Qui reçoit ?",
    "« Ich schenke meinem Freund einen Fahrradhelm. » Quel groupe est au "
    "**datif** ?",
    "meinem Freund",
    "Le datif désigne la personne qui reçoit : « meinem » porte la marque "
    "-em du datif masculin.",
    (("einen Fahrradhelm", "C'est le cadeau : il est à l'accusatif "
                           "(einen)."),
     ("Ich", "« Ich » est le sujet : il est au nominatif."),
     ("schenke", "« schenke » est le verbe ; le datif est un groupe "
                 "nominal.")),
    level=2, rappel=REGLE_SCHENKEN,
)


# --------------------------------------------------------------------------
# Séances 7 et 8 : se plaindre avec wenn, les verbes de modalité
# --------------------------------------------------------------------------

REGLE_WENN = (
    "Pour dire ce qui t'agace : Ich hasse es, wenn… (je déteste quand…), "
    "Es ärgert mich, wenn… (ça m'agace quand…), Es nervt mich, wenn…",
    "Comme après « weil » et « dass », le verbe conjugué va **à la fin** "
    "de la subordonnée en « wenn ».",
)

WENN = trous(
    "all_u03_wenn", "Ça m'agace quand…",
    "Lena dit ce qui l'agace. Choisis la fin de phrase qui convient.",
    3,
    REGLE_WENN + (
        "« zuhören » (écouter) se construit avec le datif : sie hört mir "
        "zu.",),
    """1. Ich hasse es, wenn @w1@.
2. Es ärgert mich, wenn @w2@.
3. Ich hasse es, wenn @w3@.
4. Es nervt mich, wenn @w4@.""",
    (
        ("w1", "1", "quand ma sœur entre dans ma chambre",
         "meine Schwester in mein Zimmer kommt",
         (("meine Schwester kommt in mein Zimmer", "après « wenn », où va "
                                                   "le verbe conjugué ?"),
          ("kommt meine Schwester in mein Zimmer", "après « wenn », le "
                                                   "sujet suit la "
                                                   "conjonction"),
          ("meine Schwester in meinem Zimmer kommt", "« in meinem "
                                                     "Zimmer » (datif) "
                                                     "dit où l'on est ; "
                                                     "elle y entre"))),
        ("w2", "2", "quand elle ne m'écoute pas",
         "sie mir nicht zuhört",
         (("sie hört mir nicht zu", "après « wenn », le verbe conjugué ne "
                                    "reste pas en 2e position"),
          ("sie mich nicht zuhört", "« zuhören » se construit avec le "
                                    "datif ; « mich » est un accusatif"),
          ("sie mir zuhört", "il manque la négation"))),
        ("w3", "3", "quand je dois faire mes devoirs",
         "ich meine Hausaufgaben machen muss",
         (("ich muss meine Hausaufgaben machen", "après « wenn », le verbe "
                                                 "conjugué ne reste pas "
                                                 "en 2e position"),
          ("ich meine Hausaufgaben muss machen", "le verbe conjugué va "
                                                 "tout à la fin, après "
                                                 "l'infinitif"),
          ("ich meine Hausaufgaben machen darf", "l'ordre est juste, mais "
                                                 "« dürfen » exprime une "
                                                 "permission"))),
        ("w4", "4", "quand mes parents me grondent",
         "meine Eltern mit mir schimpfen",
         (("meine Eltern schimpfen mit mir", "après « wenn », où va le "
                                             "verbe conjugué ?"),
          ("meine Eltern mit mir schimpft", "« meine Eltern » est un "
                                            "pluriel"),
          ("meine Eltern mit mir lachen", "l'ordre est juste, mais "
                                          "« lachen » veut dire rire"))),
    ),
)

REGLE_MODAUX = (
    "können : pouvoir, être capable — dürfen : avoir le droit — müssen : "
    "devoir, être obligé — sollen : devoir, parce qu'un autre le demande "
    "(un ordre, un conseil) — wollen : vouloir.",
    "sollen : ich soll, du sollst, er soll, wir sollen, ihr sollt, sie "
    "sollen.",
)

MODAUX = trous(
    "all_u03_modaux", "Les verbes de modalité",
    "Lukas et ses amis parlent de ce qu'ils peuvent, veulent ou doivent "
    "faire. Choisis le verbe qui convient.",
    2,
    REGLE_MODAUX,
    """1. Meine Mutter sagt, ich @m1@ den Müll rausbringen.
2. @m2@ du auch pünktlich sein?
3. Wir Schüler @m3@ höflich zu den Lehrern sein.
4. Ihr @m4@ euch gegenseitig respektieren!
5. Ich @m5@ auch mal meine Ruhe haben!
6. Ich @m6@ es meinen Eltern nicht sagen, ich traue mich nicht.""",
    (
        ("m1", "1", "on me demande de (sollen, avec « ich »)",
         "soll",
         (("will", "« wollen » exprime ta propre volonté ; ici c'est la "
                   "mère qui le demande"),
          ("kann", "« können » exprime une capacité"),
          ("darf", "« dürfen » exprime une permission"))),
        ("m2", "2", "sollen, avec « du »",
         "Sollst",
         (("Soll", "« soll » va avec ich ou er, sie, es"),
          ("Sollt", "« sollt » va avec « ihr »"),
          ("Sollen", "« sollen » va avec wir ou sie (pluriel)"))),
        ("m3", "3", "sollen, avec « wir »",
         "sollen",
         (("sollt", "« sollt » va avec « ihr »"),
          ("soll", "« soll » va avec ich ou er, sie, es"),
          ("sollst", "« sollst » va avec « du »"))),
        ("m4", "4", "sollen, avec « ihr »",
         "sollt",
         (("sollen", "« sollen » va avec wir ou sie (pluriel)"),
          ("soll", "« soll » va avec ich ou er, sie, es"),
          ("sollst", "« sollst » va avec « du »"))),
        ("m5", "5", "je veux (volonté)",
         "will",
         (("soll", "« sollen » : c'est un autre qui le demande"),
          ("muss", "« müssen » exprime une obligation"),
          ("darf", "« dürfen » exprime une permission"))),
        ("m6", "6", "je ne peux pas (capacité)",
         "kann",
         (("darf", "« nicht dürfen » : ne pas avoir le droit ; ici "
                   "Lukas n'ose pas"),
          ("will", "« wollen » exprime une volonté"),
          ("soll", "« sollen » exprime une demande d'un autre"))),
    ),
)

Q_WENN = question(
    "all_u03_q_wenn", "Es ärgert mich, wenn…",
    "Que veut dire « Es ärgert mich, wenn sie herumkommandiert » ?",
    "Ça m'agace quand elle donne des ordres à tout le monde.",
    "« Es ärgert mich » : ça m'agace. « wenn » : quand (chaque fois que).",
    (("Je suis content quand elle donne des ordres.",
      "« ärgern » veut dire agacer, énerver : ce n'est pas un sentiment "
      "positif."),
     ("Ça m'agace parce qu'elle donne des ordres.",
      "« parce que » se dirait « weil ». « wenn » dit autre chose."),
     ("Ça l'agace quand je donne des ordres.",
      "« mich » renvoie à moi, et « sie » est le sujet de la subordonnée : "
      "qui commande ?")),
    level=3, rappel=REGLE_WENN,
)


# --------------------------------------------------------------------------
# Séance 9 : les conflits, donner un conseil
# --------------------------------------------------------------------------

REGLE_CONSEIL = (
    "Donner un conseil : Du solltest + infinitif à la fin → Du solltest "
    "mit Markus sprechen (tu devrais parler à Markus).",
    "Ou l'impératif : on part de la forme de « er » sans le -t. Pour un "
    "verbe fort en -e, on garde le i ou le ie : er spricht → sprich!",
)

Q_SOLLTEST = question(
    "all_u03_q_solltest", "Tu devrais…",
    "Tu conseilles à Timo de parler à Markus. Que dis-tu ?",
    "Du solltest mit Markus sprechen.",
    "« Du solltest… » (tu devrais) donne un conseil ; l'infinitif "
    "« sprechen » va à la fin.",
    (("Du solltest mit Markus sprichst.", "Après « solltest », le second "
                                          "verbe n'est pas conjugué."),
     ("Du musst nicht mit Markus sprechen.", "« nicht müssen » veut dire "
                                             "« ne pas être obligé » : ce "
                                             "n'est pas un conseil."),
     ("Du darfst nicht mit Markus sprechen.", "« nicht dürfen » est une "
                                              "interdiction.")),
    level=3, rappel=REGLE_CONSEIL,
)

Q_SPRICH = question(
    "all_u03_q_imperatif", "Le conseil à l'impératif",
    "Complète le conseil : « ____ mit Markus! » (sprechen, à « du »)",
    "Sprich",
    "sprechen est un verbe fort en -e : er spricht → sprich! (sans -t, "
    "sans -e final, sans sujet).",
    (("Spreche", "Un verbe fort en -e garde à l'impératif la voyelle de "
                 "la forme de « er »."),
     ("Sprichst", "« -st » est la terminaison de « du » au présent : à "
                  "l'impératif, elle disparaît."),
     ("Sprecht", "C'est l'impératif de « ihr » ; tu parles à Timo seul.")),
    level=3, rappel=REGLE_CONSEIL,
)

Q_STREIT = question(
    "all_u03_q_streit", "Les Streitschlichter",
    "Qui sont les « Streitschlichter » dans une école allemande ?",
    "des élèves médiateurs qui aident à régler les conflits",
    "« der Streit » : la dispute ; « schlichten » : apaiser, régler. Les "
    "Streitschlichter sont des médiateurs : il faut être patient, à "
    "l'écoute et compréhensif.",
    (("des élèves qui aident leurs camarades à faire leurs devoirs",
      "Le mot contient « Streit » : de quoi parle-t-il ?"),
     ("des professeurs qui punissent les élèves",
      "Ce sont des élèves, et leur rôle n'est pas de punir."),
     ("des élèves qui protègent leurs camarades des professeurs",
      "« der Streit » veut dire la dispute : ils interviennent quand des "
      "élèves se disputent.")),
    level=2,
)


PATTERNS = (
    PRESENTATION, FAMILLE, PRONOMS, Q_WOHER, Q_AUSSEHEN, Q_IHN,
    Q_EINZELKIND, Q_JUGEND,
    CARACTERE_1, CARACTERE_2, ADVERBES, Q_ADVERBE, Q_GLAUBE, Q_PASSEN,
    Q_SCHUECHTERN,
    EINANDER, AMITIE, COMPARATIF, Q_GEHEIMNIS,
    FREQUENCE, Q_FREQUENCE, Q_SMS, Q_LOISIRS,
    GEBURTSTAG, GEFALLEN, PRONOMS_DATIF, ARTICLES, Q_WERDEN, Q_MOEGEN,
    Q_DATIF,
    WENN, MODAUX, Q_WENN,
    Q_SOLLTEST, Q_SPRICH, Q_STREIT,
)

MODULE = Module(
    key="allemand_u03",
    title="Unité 3 — Freundschaft",
    level=2,
    summary="Révisions de l'unité 3 : se présenter, la famille, le "
            "caractère, l'amitié (einander), le comparatif, les loisirs et "
            "leur fréquence, l'anniversaire, offrir (datif et accusatif), "
            "wenn, les verbes de modalité et le conseil. " + INTITULE,
    keys=tuple(p.key for p in PATTERNS),
)
