"""Module « Unité 2 » du chapitre Allemand : Bei mir zu Hause.

Des exercices de révision sur la deuxième unité d'allemand de 3e (LV2) :
la maison et ses pièces, le locatif, la ville et la campagne, l'opinion
et la subordonnée en weil, la chambre et les prépositions spatiales,
stehen / liegen / hängen / sitzen, la négation kein, müssen et dürfen,
les tâches ménagères et les verbes à particule, la recette et
l'impératif, les repas et le comparatif, les mots composés, le tri des
déchets et la subordonnée en dass, la télévision, wollen et la
proposition (Sollen wir… ?).

Les phrases sont écrites pour l'exercice, dans l'esprit du cours : on en
tire des exercices, pas des extraits. Les deux formes d'exercice (phrases
à trous, questions) et leurs indices sont décrites dans `allemand_commun`.
"""

from functools import partial

from ..engine import Module
from . import allemand_commun as commun

INTITULE = commun.intitule(2)

trous = partial(commun.trous, INTITULE)
question = partial(commun.question, INTITULE)


# --------------------------------------------------------------------------
# Séance 1 : la maison, ses étages et ses pièces, le locatif
# --------------------------------------------------------------------------

ETAGES = trous(
    "all_u02_etages", "Les étages de la maison",
    "Tim fait visiter sa maison, de la cave au grenier. Complète.",
    1,
    ("der Keller : la cave — das Erdgeschoss : le rez-de-chaussée — der "
     "erste Stock : le premier étage — der zweite Stock : le deuxième "
     "étage — der Dachboden : le grenier — das Dach : le toit.",
     "Pour dire à quel étage : im Erdgeschoss, im ersten Stock, im "
     "zweiten Stock."),
    """Im @e1@ sind ein Hobbyraum und die Waschküche.
Im @e2@ sind die Küche und das Wohnzimmer.
Im @e3@ sind mein Zimmer und das Badezimmer.
Unter dem Dach ist der @e4@ mit alten Sachen.""",
    (
        ("e1", "1", "à la cave",
         "Keller",
         (("Dachboden", "« der Dachboden » est tout en haut, sous le "
                        "toit ; on commence la visite par en bas"),
          ("Erdgeschoss", "« das Erdgeschoss » : le rez-de-chaussée, au "
                          "niveau de la rue"),
          ("ersten Stock", "« der erste Stock » : le premier étage"))),
        ("e2", "2", "au rez-de-chaussée",
         "Erdgeschoss",
         (("ersten Stock", "« der erste Stock » : le premier étage, "
                           "au-dessus du rez-de-chaussée"),
          ("Keller", "« der Keller » : la cave, sous la maison"),
          ("Dach", "« das Dach » : le toit"))),
        ("e3", "3", "au premier étage",
         "ersten Stock",
         (("zweiten Stock", "« zweite » veut dire deuxième"),
          ("Erdgeschoss", "« das Erdgeschoss » : le rez-de-chaussée"),
          ("Garten", "« der Garten » : le jardin, ce n'est pas un "
                     "étage"))),
        ("e4", "4", "le grenier",
         "Dachboden",
         (("Keller", "« der Keller » est la cave : elle est sous la "
                     "maison, pas sous le toit"),
          ("Balkon", "« der Balkon » : le balcon"),
          ("Eingang", "« der Eingang » : l'entrée"))),
    ),
)

PIECES = trous(
    "all_u02_pieces", "Où fais-tu quoi ?",
    "Dis dans quelle pièce on fait chaque activité. Attention à la forme "
    "de l'article.",
    2,
    ("Pour dire où l'on est (Wo?) : in + datif. Masculin et neutre : in "
     "dem = im ; féminin : in der.",
     "die Küche (la cuisine), das Wohnzimmer (le salon), das Esszimmer "
     "(la salle à manger), das Badezimmer (la salle de bains), das "
     "Schlafzimmer (la chambre), das Arbeitszimmer (le bureau), der "
     "Garten (le jardin).",
     "« in die Küche », « in das Zimmer » (accusatif) disent où l'on va, "
     "pas où l'on est."),
    """Ich dusche @p1@.
Mama kocht @p2@.
Wir sehen @p3@ fern.
Papa arbeitet @p4@.
Mein Hund und ich spielen Fußball @p5@.""",
    (
        ("p1", "Douche", "dans la salle de bains",
         "im Badezimmer",
         (("in der Badezimmer", "« in der » est pour un mot féminin ; "
                                "« Badezimmer » est neutre, comme tous "
                                "les mots en -zimmer"),
          ("im Schlafzimmer", "« das Schlafzimmer » : la chambre à "
                              "coucher"),
          ("in das Badezimmer", "« in das » + accusatif dit où l'on va ; "
                                "ici, on dit où l'on est"))),
        ("p2", "Cuisine", "dans la cuisine",
         "in der Küche",
         (("im Küche", "« im » = in dem, pour un masculin ou un neutre ; "
                       "« Küche » est féminin"),
          ("in die Küche", "« in die » + accusatif dit où l'on va ; ici, "
                           "Mama y est déjà"),
          ("im Esszimmer", "« das Esszimmer » : la salle à manger"))),
        ("p3", "Télé", "dans le salon",
         "im Wohnzimmer",
         (("im Arbeitszimmer", "« das Arbeitszimmer » : le bureau"),
          ("in der Wohnzimmer", "« Wohnzimmer » est neutre : « in der » "
                                "est pour un féminin"),
          ("im Elternzimmer", "« das Elternzimmer » : la chambre des "
                              "parents"))),
        ("p4", "Travail", "dans le bureau",
         "im Arbeitszimmer",
         (("im Kinderzimmer", "« das Kinderzimmer » : la chambre des "
                              "enfants"),
          ("in der Arbeitszimmer", "« Arbeitszimmer » est neutre : "
                                   "« in der » est pour un féminin"),
          ("im Gästezimmer", "« das Gästezimmer » : la chambre d'amis"))),
        ("p5", "Football", "dans le jardin",
         "im Garten",
         (("in der Garten", "« in der » est pour un féminin ; « der "
                            "Garten » est masculin"),
          ("in den Garten", "« in den » + accusatif dit où l'on va ; "
                            "ici, on dit où l'on joue"),
          ("im Keller", "« der Keller » : la cave"))),
    ),
)

Q_MAISON = question(
    "all_u02_q_maison", "Les types de maison",
    "Que veut dire « das Einfamilienhaus » ?",
    "la maison individuelle",
    "Ein-familien-haus : la maison d'une seule famille, la maison "
    "individuelle.",
    (("la maison mitoyenne", "La maison mitoyenne se dit « das "
                             "Reihenhaus » (die Reihe : la rangée). "
                             "Décompose le mot : ein… Familie… Haus."),
     ("la maison à colombages", "La maison à colombages se dit « das "
                                "Fachwerkhaus ». Que veut dire « Familie » "
                                "dans le mot ?"),
     ("l'appartement", "L'appartement se dit « die Wohnung » ; le mot se "
                       "termine par « Haus ».")),
    level=1,
)

Q_O_LONG = question(
    "all_u02_q_o", "Le o long",
    "Dans « wohnen », le o est long et fermé ; dans « Dorf », il est court "
    "et ouvert. Dans quel mot le o est-il **long** ?",
    "Dachboden",
    "Dans « Boden », le o n'est suivi que d'une consonne : il est long, "
    "comme dans « wohnen ». Devant deux consonnes (Holz, Stock, kommen), "
    "il est le plus souvent court.",
    (("Holz", "Le o de « Holz » est suivi de deux consonnes, l et z : il "
              "est court, comme dans « Dorf »."),
     ("Stock", "Le o de « Stock » est suivi de « ck » : il est court."),
     ("kommen", "Le o de « kommen » est suivi d'une double consonne : il "
                "est court.")),
    level=2,
)


# --------------------------------------------------------------------------
# Séance 2 : la ville ou la campagne, l'opinion, weil
# --------------------------------------------------------------------------

VILLE = trous(
    "all_u02_ville", "Ville ou campagne ?",
    "Max et Sofia parlent des avantages et des inconvénients de leur "
    "lieu de vie. Complète.",
    1,
    ("Pour juger : Das ist praktisch / toll / cool / gesund (bon pour la "
     "santé) — Das ist unpraktisch / nervig (énervant) / blöd (nul).",
     "laut (bruyant) ≠ leise (silencieux) — leider : malheureusement — "
     "immer : toujours — dort : là-bas.",
     "im Stadtzentrum : en centre-ville — auf dem Land : à la campagne — "
     "in der Nähe von : près de."),
    """Max:   Die Wohnung liegt @o1@.
Max:   Dort gibt es viele Geschäfte. Das ist @o2@!
Max:   Die Autos machen viel Lärm. Das ist @o3@!
Sofia: Wir sind viel draußen. Das ist sehr @o4@.
Sofia: Ich muss eine Stunde mit dem Bus fahren, @o5@!""",
    (
        ("o1", "1", "en centre-ville",
         "im Stadtzentrum",
         (("auf dem Land", "« auf dem Land » : à la campagne"),
          ("in einem Dorf", "« das Dorf » : le village"),
          ("in der Nähe vom Bahnhof", "« in der Nähe vom Bahnhof » : près "
                                      "de la gare"))),
        ("o2", "2", "c'est pratique",
         "praktisch",
         (("unpraktisch", "« un- » donne le contraire : pas pratique"),
          ("nervig", "« nervig » : énervant, c'est un jugement négatif"),
          ("gesund", "« gesund » : bon pour la santé"))),
        ("o3", "3", "c'est énervant",
         "nervig",
         (("toll", "« toll » : super, c'est un jugement positif"),
          ("leise", "« leise » : silencieux, le contraire du bruit"),
          ("praktisch", "« praktisch » : pratique, c'est positif"))),
        ("o4", "4", "c'est très bon pour la santé",
         "gesund",
         (("krank", "« krank » : malade, c'est le contraire"),
          ("laut", "« laut » : bruyant"),
          ("dunkel", "« dunkel » : sombre"))),
        ("o5", "5", "malheureusement",
         "leider",
         (("immer", "« immer » : toujours"),
          ("dort", "« dort » : là-bas"),
          ("oft", "« oft » : souvent"))),
    ),
)

REGLE_WEIL = (
    "Dans une subordonnée introduite par **weil** (parce que), le verbe "
    "conjugué va **à la fin**. Une virgule la sépare de la principale : "
    "Ich bleibe zu Hause, weil es regnet.",
)

WEIL = trous(
    "all_u02_weil", "Se justifier avec weil",
    "Chacun justifie ce qu'il fait. Choisis la fin de phrase qui convient.",
    3,
    REGLE_WEIL + (
        "Avec un verbe de modalité (wollen, müssen…), c'est lui qui va "
        "tout à la fin, après l'infinitif : …, weil ich schlafen will.",),
    """1. Ich trinke ein Glas Wasser, weil @w1@.
2. Ich fahre mit dem Fahrrad, weil @w2@.
3. Ich mache meine Hausaufgaben, weil @w3@.
4. Meine Nachbarn sind nervig, weil @w4@.""",
    (
        ("w1", "1", "parce que j'ai soif",
         "ich Durst habe",
         (("ich habe Durst", "après « weil », le verbe conjugué ne reste "
                             "pas en 2e position"),
          ("habe ich Durst", "après « weil », le sujet suit la "
                             "conjonction, et le verbe conjugué va "
                             "ailleurs"),
          ("ich Hunger habe", "l'ordre est juste, mais « der Hunger » "
                              "veut dire la faim"))),
        ("w2", "2", "parce que je n'aime pas prendre le bus",
         "ich nicht gern mit dem Bus fahre",
         (("ich fahre nicht gern mit dem Bus", "après « weil », où va le "
                                               "verbe conjugué ?"),
          ("ich gern mit dem Bus fahre", "l'ordre est juste, mais sans "
                                         "« nicht », on dit qu'on aime "
                                         "le bus"),
          ("ich nicht gern mit dem Bus fahren", "« fahren » n'est pas "
                                                "conjugué avec « ich »"))),
        ("w3", "3", "parce que je veux avoir une bonne note",
         "ich eine gute Note haben will",
         (("ich will eine gute Note haben", "après « weil », le verbe "
                                            "conjugué ne reste pas en 2e "
                                            "position"),
          ("ich eine gute Note will haben", "le verbe conjugué va tout à "
                                            "la fin, même après "
                                            "l'infinitif"),
          ("ich eine schlechte Note haben will", "l'ordre est juste, mais "
                                                 "« schlecht » veut dire "
                                                 "mauvais"))),
        ("w4", "4", "parce qu'ils sont toujours bruyants",
         "sie immer laut sind",
         (("sie sind immer laut", "après « weil », où va le verbe "
                                  "conjugué ?"),
          ("sie immer leise sind", "l'ordre est juste, mais « leise » "
                                   "veut dire silencieux"),
          ("sie nie laut sind", "l'ordre est juste, mais « nie » veut "
                                "dire jamais"))),
    ),
)

Q_WEIL = question(
    "all_u02_q_weil", "La place du verbe après weil",
    "Quelle phrase est correcte ?",
    "Ich wohne gern hier, weil es viel Natur gibt.",
    "Dans la subordonnée en « weil », le verbe conjugué « gibt » va à la "
    "fin.",
    (("Ich wohne gern hier, weil es gibt viel Natur.",
      "C'est l'ordre d'une phrase principale. Que devient la place du "
      "verbe après « weil » ?"),
     ("Ich wohne gern hier, weil gibt es viel Natur.",
      "Après « weil », le sujet vient tout de suite, et le verbe "
      "conjugué n'est pas en 2e position."),
     ("Ich wohne gern hier weil, es viel Natur gibt.",
      "L'ordre des mots est juste, mais la virgule est mal placée : elle "
      "sépare les deux propositions.")),
    level=3, rappel=REGLE_WEIL,
)

Q_TREFFEN = question(
    "all_u02_q_treffen", "treffen, geben, nehmen",
    "Complète : « Max ____ seine Freunde im Park. » (treffen, au présent)",
    "trifft",
    "treffen est un verbe fort en -e : du triffst, er / sie trifft. Même "
    "chose pour geben (er gibt) et nehmen (er nimmt).",
    (("trefft", "« trefft » est la forme de « ihr ». À la 3e personne du "
                "singulier, un verbe fort en -e change de voyelle."),
     ("triffst", "« -st » est la terminaison de « du ». Le sujet ici est "
                 "« Max »."),
     ("treffe", "« treffe » est la forme de « ich ».")),
    level=2,
)


# --------------------------------------------------------------------------
# Séance 3 : la chambre, les prépositions spatiales, kein
# --------------------------------------------------------------------------

CHAMBRE = trous(
    "all_u02_chambre", "Dans ma chambre",
    "Sofia décrit sa chambre. Choisis le meuble ou l'objet qui convient.",
    1,
    ("Les meubles : das Bett (le lit), das Sofa, der Schrank (l'armoire), "
     "das Regal (l'étagère), der Schreibtisch (le bureau), der Stuhl (la "
     "chaise), die Kommode.",
     "Les objets et la pièce : der Wecker (le réveil), der Fernseher, der "
     "Laptop, das Kissen (le coussin), der Teppich (le tapis), der "
     "Papierkorb (la corbeille), die Lampe — die Wand (le mur), die Tür "
     "(la porte), das Fenster, der Boden (le sol)."),
    """Ich schlafe in meinem @m1@.
Meine Bücher stehen im @m2@.
Ich mache meine Hausaufgaben am @m3@.
Der @m4@ klingelt jeden Morgen um 7 Uhr.
An der @m5@ hängen viele Poster.""",
    (
        ("m1", "1", "le lit",
         "Bett",
         (("Sofa", "« das Sofa » : le canapé"),
          ("Schrank", "« der Schrank » : l'armoire"),
          ("Kissen", "« das Kissen » : le coussin"))),
        ("m2", "2", "l'étagère",
         "Regal",
         (("Schrank", "« der Schrank » : l'armoire"),
          ("Papierkorb", "« der Papierkorb » : la corbeille à papier"),
          ("Teppich", "« der Teppich » : le tapis"))),
        ("m3", "3", "le bureau",
         "Schreibtisch",
         (("Stuhl", "« der Stuhl » : la chaise"),
          ("Fenster", "« das Fenster » : la fenêtre"),
          ("Boden", "« der Boden » : le sol"))),
        ("m4", "4", "le réveil",
         "Wecker",
         (("Fernseher", "« der Fernseher » : la télévision"),
          ("Laptop", "« der Laptop » : l'ordinateur portable"),
          ("Teppich", "« der Teppich » : le tapis"))),
        ("m5", "5", "le mur",
         "Wand",
         (("Tür", "« die Tür » : la porte"),
          ("Kommode", "« die Kommode » : la commode, un meuble"),
          ("Lampe", "« die Lampe » : la lampe"))),
    ),
)

REGLE_LIEU = (
    "Prépositions spatiales : auf (sur) ≠ unter (sous), vor (devant) ≠ "
    "hinter (derrière), neben (à côté de), über (au-dessus de), an (à, "
    "contre), zwischen (entre).",
    "Pour dire où se trouve quelque chose (Wo?), elles sont suivies du "
    "**datif** : masculin et neutre dem / einem, féminin der / einer, "
    "pluriel den.",
)

PREPOSITIONS = trous(
    "all_u02_prepositions", "Où est quoi ?",
    "Tim range sa chambre. Complète avec la préposition qui convient.",
    2,
    REGLE_LIEU,
    """Die Lampe steht @q1@ dem Schreibtisch.
Meine Schuhe stehen @q2@ dem Bett.
Das Poster hängt @q3@ dem Bett.
Der Stuhl steht @q4@ dem Schreibtisch.
Der Papierkorb steht @q5@ dem Bett und dem Schrank.
Meine Jacke hängt @q6@ der Tür.""",
    (
        ("q1", "Lampe", "sur le bureau",
         "auf",
         (("unter", "« unter » : sous, c'est le contraire"),
          ("über", "« über » : au-dessus de, sans toucher le meuble"),
          ("neben", "« neben » : à côté de"))),
        ("q2", "Chaussures", "sous le lit",
         "unter",
         (("auf", "« auf » : sur, c'est le contraire"),
          ("hinter", "« hinter » : derrière"),
          ("vor", "« vor » : devant"))),
        ("q3", "Poster", "au-dessus du lit",
         "über",
         (("auf", "« auf » : sur, posé dessus ; un poster accroché au mur "
                  "ne touche pas le lit"),
          ("unter", "« unter » : sous"),
          ("neben", "« neben » : à côté de"))),
        ("q4", "Chaise", "devant le bureau",
         "vor",
         (("hinter", "« hinter » : derrière, c'est le contraire"),
          ("neben", "« neben » : à côté de"),
          ("über", "« über » : au-dessus de"))),
        ("q5", "Corbeille", "entre le lit et l'armoire",
         "zwischen",
         (("neben", "« neben » : à côté d'un seul objet ; ici il y en a "
                    "deux, de part et d'autre"),
          ("hinter", "« hinter » : derrière"),
          ("vor", "« vor » : devant"))),
        ("q6", "Veste", "accrochée à la porte",
         "an",
         (("auf", "« auf » : sur, posé dessus, pour une surface "
                  "horizontale"),
          ("in", "« in » : dans ; la veste n'est pas dans la porte"),
          ("unter", "« unter » : sous"))),
    ),
)

DATIF_LIEU = trous(
    "all_u02_datif", "Le datif après une préposition de lieu",
    "Où sont les affaires de Hanna ? Complète avec la marque du datif.",
    3,
    REGLE_LIEU + (
        "Trouve d'abord le genre et le nombre du nom, puis la marque : -em "
        "(masculin, neutre), -er (féminin), -en (pluriel).",),
    """Der Ball liegt unter d@a1@ Bett (das Bett).
Die Bücher liegen neben d@a2@ Lampe (die Lampe).
Die Katze schläft auf d@a3@ Kissen (die Kissen, pluriel).
Das Regal hängt über mein@a4@ Schreibtisch (der Schreibtisch).
Der Teppich liegt vor ein@a5@ Kommode (die Kommode).""",
    (
        ("a1", "Bett", "datif neutre",
         "em",
         (("er", "« -er » est la marque du féminin ; « Bett » est "
                 "neutre"),
          ("as", "« das » n'est pas un datif : la balle est quelque part, "
                 "il faut le datif"),
          ("en", "« -en » est la marque du pluriel"))),
        ("a2", "Lampe", "datif féminin",
         "er",
         (("em", "« -em » est la marque du masculin et du neutre ; "
                 "« Lampe » est féminin"),
          ("ie", "« die » n'est pas un datif"),
          ("en", "« -en » est la marque du pluriel"))),
        ("a3", "Kissen", "datif pluriel",
         "en",
         (("em", "« -em » est la marque du singulier ; ici « die Kissen » "
                 "est un pluriel"),
          ("er", "« -er » est la marque du féminin singulier"),
          ("ie", "« die » n'est pas un datif"))),
        ("a4", "Schreibtisch", "datif masculin",
         "em",
         (("en", "« meinen » est un accusatif masculin ou un datif "
                 "pluriel : l'étagère est quelque part, et il n'y a qu'un "
                 "bureau"),
          ("er", "« -er » est la marque du féminin ; « Schreibtisch » est "
                 "masculin"),
          ("e", "il manque la marque du datif"))),
        ("a5", "Kommode", "datif féminin",
         "er",
         (("em", "« -em » est la marque du masculin et du neutre ; "
                 "« Kommode » est féminin"),
          ("e", "il manque la marque du datif"),
          ("en", "« -en » est la marque du pluriel"))),
    ),
)

POSITION = trous(
    "all_u02_position", "stehen, liegen, hängen, sitzen",
    "Comment les choses sont-elles placées ? Choisis le verbe qui "
    "convient.",
    2,
    ("stehen : être posé debout, à la verticale (une lampe, un meuble) — "
     "liegen : être posé à plat, couché (un livre, un tapis) — hängen : "
     "être accroché (un poster, une veste) — sitzen : être assis.",
     "Le verbe s'accorde avec le sujet : es liegt, sie liegen."),
    """Die Lampe @s1@ auf dem Tisch.
Mein Buch @s2@ auf dem Bett.
Das Poster @s3@ an der Wand.
Meine Katze @s4@ auf dem Sofa und schaut mich an.
Die Kissen @s5@ auf dem Boden.""",
    (
        ("s1", "Lampe", "posée debout",
         "steht",
         (("liegt", "« liegen » : posé à plat ou couché ; une lampe sur "
                    "son pied est debout"),
          ("hängt", "« hängen » : accroché ; la lampe est posée sur la "
                    "table"),
          ("sitzt", "« sitzen » : être assis, pour une personne ou un "
                    "animal"))),
        ("s2", "Livre", "posé à plat",
         "liegt",
         (("steht", "« stehen » : posé debout, à la verticale"),
          ("hängt", "« hängen » : accroché"),
          ("sitzt", "« sitzen » : être assis, pour une personne ou un "
                    "animal"))),
        ("s3", "Poster", "accroché",
         "hängt",
         (("steht", "« stehen » : posé debout ; un poster au mur ne tient "
                    "pas debout tout seul"),
          ("liegt", "« liegen » : posé à plat"),
          ("sitzt", "« sitzen » : être assis"))),
        ("s4", "Chat", "assis",
         "sitzt",
         (("liegt", "« liegen » : couché, allongé"),
          ("steht", "« stehen » : debout, sur ses pattes"),
          ("hängt", "« hängen » : accroché"))),
        ("s5", "Coussins", "posés à plat (pluriel)",
         "liegen",
         (("liegt", "le bon verbe, mais « liegt » va avec un sujet "
                    "singulier ; « die Kissen » est un pluriel"),
          ("stehen", "« stehen » : posé debout"),
          ("hängen", "« hängen » : accroché"))),
    ),
)

KEIN = trous(
    "all_u02_kein", "La négation kein",
    "Julia n'a rien de ce que Tim lui demande. Complète avec la bonne "
    "forme de kein.",
    2,
    ("keinen / keine / kein sont les formes négatives de einen / eine / "
     "ein. On les traduit par « pas de ».",
     "Complément d'objet (accusatif) : masculin keinen, féminin keine, "
     "neutre kein, pluriel keine.",
     "« nicht » nie un verbe ou un adjectif ; devant un nom sans article "
     "défini, on emploie kein."),
    """Tim:   Hast du einen Laptop?
Julia: Nein, ich habe @k1@ Laptop.
Tim:   Hast du eine Schwester?
Julia: Nein, ich habe @k2@ Schwester.
Tim:   Möchtest du ein Glas Wasser?
Julia: Nein, ich möchte @k3@ Glas Wasser.
Tim:   Isst du Bonbons?
Julia: Nein, ich esse @k4@ Bonbons.""",
    (
        ("k1", "Laptop", "pas d'ordinateur portable (masculin)",
         "keinen",
         (("kein", "« kein » est la forme du neutre ; « der Laptop » est "
                   "masculin, et c'est un complément d'objet"),
          ("keine", "« keine » est la forme du féminin ou du pluriel"),
          ("nicht", "devant un nom avec « ein », la négation n'est pas "
                    "« nicht »"))),
        ("k2", "Schwester", "pas de sœur (féminin)",
         "keine",
         (("keinen", "« keinen » est la forme du masculin ; « die "
                     "Schwester » est féminin"),
          ("kein", "« kein » est la forme du neutre"),
          ("nicht", "devant un nom avec « eine », la négation n'est pas "
                    "« nicht »"))),
        ("k3", "Glas", "pas de verre (neutre)",
         "kein",
         (("keinen", "« keinen » est la forme du masculin ; « das Glas » "
                     "est neutre"),
          ("keine", "« keine » est la forme du féminin ou du pluriel"),
          ("nicht", "devant un nom avec « ein », la négation n'est pas "
                    "« nicht »"))),
        ("k4", "Bonbons", "pas de bonbons (pluriel)",
         "keine",
         (("keinen", "« keinen » est la forme du masculin singulier ; "
                     "« Bonbons » est un pluriel"),
          ("kein", "« kein » est la forme du neutre singulier"),
          ("nicht", "devant un nom sans article, la négation n'est pas "
                    "« nicht »"))),
    ),
)

Q_KEIN = question(
    "all_u02_q_kein", "Je n'ai pas de…",
    "Comment dit-on « Je n'ai pas de vélo » ? (das Fahrrad)",
    "Ich habe kein Fahrrad.",
    "« das Fahrrad » est neutre : ein Fahrrad → kein Fahrrad.",
    (("Ich habe nicht Fahrrad.", "Devant un nom, « pas de » ne se dit pas "
                                 "avec « nicht »."),
     ("Ich habe keinen Fahrrad.", "« keinen » est la forme du masculin. "
                                  "Quel est le genre de « Fahrrad » ?"),
     ("Ich habe keine Fahrrad.", "« keine » est la forme du féminin ou du "
                                 "pluriel. Quel est le genre de "
                                 "« Fahrrad » ?")),
    level=2,
)

Q_DATIF = question(
    "all_u02_q_unter", "Wo? + datif",
    "Quelle phrase est correcte ?",
    "Die Schuhe stehen unter dem Schreibtisch.",
    "« unter » dit où se trouvent les chaussures (Wo?) : datif. « der "
    "Schreibtisch » est masculin : dem.",
    (("Die Schuhe stehen unter der Schreibtisch.",
      "« der » est ici le datif du féminin. Quel est le genre de "
      "« Schreibtisch » ?"),
     ("Die Schuhe stehen unter den Schreibtisch.",
      "« den » est l'accusatif masculin : il dit où l'on met quelque "
      "chose. Ici, on dit où sont les chaussures."),
     ("Die Schuhe stehen unter das Schreibtisch.",
      "« das » est un neutre, et ce n'est pas un datif.")),
    level=3, rappel=REGLE_LIEU,
)

Q_DESWEGEN = question(
    "all_u02_q_deswegen", "Argumenter",
    "« Mein Zimmer ist klein, ____ habe ich weiße Möbel. » Quel mot veut "
    "dire « c'est pourquoi » ?",
    "deswegen",
    "« deswegen » veut dire « c'est pourquoi ». Il occupe la 1re position "
    "de sa proposition : le verbe « habe » vient juste après, en 2e.",
    (("außerdem", "« außerdem » veut dire « de plus » : il ajoute une "
                  "information, il ne donne pas une conséquence."),
     ("vor allem", "« vor allem » veut dire « surtout »."),
     ("leider", "« leider » veut dire « malheureusement ».")),
    level=2,
)


# --------------------------------------------------------------------------
# Séance 4 : vivre ensemble, müssen et dürfen, les tâches ménagères
# --------------------------------------------------------------------------

REGLE_MODAUX = (
    "ich muss : je dois — ich muss nicht : je ne suis pas obligé — ich "
    "darf : j'ai le droit — ich darf nicht : je n'ai pas le droit.",
    "müssen : ich muss, du musst, er muss, wir müssen, ihr müsst, sie "
    "müssen. dürfen : ich darf, du darfst, er darf, wir dürfen, ihr "
    "dürft, sie dürfen.",
    "Le verbe de modalité est conjugué en 2e position, l'infinitif va à "
    "la fin : Ich muss mein Zimmer aufräumen.",
)

MODAUX = trous(
    "all_u02_modaux", "müssen ou dürfen ?",
    "Les règles de la maison. Complète avec müssen ou dürfen, à la bonne "
    "personne.",
    2,
    REGLE_MODAUX,
    """1. Ich @d1@ jeden Freitag mein Zimmer aufräumen.
2. @d2@ ich heute fernsehen? — Ja, du darfst.
3. Im Kino @d3@ man nicht telefonieren.
4. Am Sonntag @d4@ ich nicht früh aufstehen. Super!
5. Ihr @d5@ jetzt den Tisch decken!
6. Wir @d6@ am Wochenende Freunde treffen.""",
    (
        ("d1", "1", "je dois (obligation)",
         "muss",
         (("darf", "« dürfen » exprime une permission, pas une "
                   "obligation"),
          ("müssen", "« müssen » va avec wir ou sie (pluriel)"),
          ("musst", "« musst » va avec « du »"))),
        ("d2", "2", "ai-je le droit ? (permission)",
         "Darf",
         (("Muss", "« müssen » demande une obligation, pas une "
                   "permission"),
          ("Dürfen", "« dürfen » va avec wir ou sie (pluriel)"),
          ("Darfst", "« darfst » va avec « du » ; le sujet est « ich »"))),
        ("d3", "3", "on n'a pas le droit (interdiction)",
         "darf",
         (("muss", "« muss nicht » veut dire « ne pas être obligé de » : "
                   "ce n'est pas une interdiction"),
          ("dürfen", "« man » se conjugue comme er, sie, es"),
          ("darfst", "« darfst » va avec « du »"))),
        ("d4", "4", "je ne suis pas obligé",
         "muss",
         (("darf", "« darf nicht » veut dire « ne pas avoir le droit » : "
                   "ce serait une interdiction"),
          ("musst", "« musst » va avec « du »"),
          ("müssen", "« müssen » va avec wir ou sie (pluriel)"))),
        ("d5", "5", "vous devez (obligation)",
         "müsst",
         (("muss", "« muss » va avec ich ou er, sie, es"),
          ("müssen", "« müssen » va avec wir ou sie (pluriel) ; le sujet "
                     "est « ihr »"),
          ("dürft", "« dürfen » exprime une permission, pas une "
                    "obligation"))),
        ("d6", "6", "nous avons le droit (permission)",
         "dürfen",
         (("darf", "« darf » va avec ich ou er, sie, es"),
          ("müssen", "« müssen » exprime une obligation, pas une "
                     "permission"),
          ("dürft", "« dürft » va avec « ihr »"))),
    ),
)

TACHES = trous(
    "all_u02_taches", "Les tâches ménagères",
    "Le planning de Tim. Choisis la tâche de chaque jour, avec l'ordre "
    "des mots qui convient.",
    3,
    ("den Tisch decken (mettre la table) ≠ den Tisch abdecken "
     "(débarrasser) — mein Zimmer aufräumen (ranger) — mit dem Hund "
     "rausgehen (sortir le chien) — Staub saugen (passer l'aspirateur) — "
     "einkaufen (faire les courses).",
     "Le jour est en 1re position : le verbe conjugué vient en 2e, le "
     "sujet en 3e.",
     "Verbes à particule séparable : la particule va à la fin de la "
     "phrase → Ich räume mein Zimmer auf."),
    """Am Montag @t1@.
Am Dienstag @t2@.
Am Mittwoch @t3@.
Am Donnerstag @t4@.
Am Samstag @t5@.""",
    (
        ("t1", "Lundi", "je mets la table",
         "decke ich den Tisch",
         (("decke ich den Tisch ab", "« abdecken » : débarrasser la "
                                     "table, c'est le contraire"),
          ("ich decke den Tisch", "« Am Montag » est en 1re position : "
                                  "qu'est-ce qui doit venir en 2e ?"),
          ("mähe ich den Rasen", "« den Rasen mähen » : tondre la "
                                 "pelouse"))),
        ("t2", "Mardi", "je range ma chambre",
         "räume ich mein Zimmer auf",
         (("aufräume ich mein Zimmer", "« aufräumen » est à particule "
                                       "séparable : la particule ne "
                                       "reste pas collée au verbe"),
          ("räume ich auf mein Zimmer", "la particule séparée va à la fin "
                                        "de la phrase"),
          ("räume ich die Spülmaschine aus", "« die Spülmaschine "
                                             "ausräumen » : vider le "
                                             "lave-vaisselle"))),
        ("t3", "Mercredi", "je sors le chien",
         "gehe ich mit dem Hund raus",
         (("füttere ich den Hund", "« den Hund füttern » : donner à "
                                   "manger au chien"),
          ("rausgehe ich mit dem Hund", "« rausgehen » est à particule "
                                        "séparable : où va « raus » ?"),
          ("bringe ich den Müll raus", "« den Müll rausbringen » : sortir "
                                       "les poubelles"))),
        ("t4", "Jeudi", "je passe l'aspirateur",
         "sauge ich Staub",
         (("bügle ich", "« bügeln » : repasser"),
          ("wasche ich das Auto", "« das Auto waschen » : laver la "
                                  "voiture"),
          ("hänge ich die Wäsche auf", "« die Wäsche aufhängen » : "
                                       "étendre le linge"))),
        ("t5", "Samedi", "je fais les courses",
         "kaufe ich ein",
         (("einkaufe ich", "« einkaufen » est à particule séparable : la "
                           "particule va à la fin"),
          ("kaufe ich", "il manque la particule : « kaufen » seul veut "
                        "dire acheter, et il demande un complément"),
          ("putze ich", "« putzen » : faire le ménage"))),
    ),
)

Q_DARF_NICHT = question(
    "all_u02_q_darf_nicht", "Interdit ou pas obligé ?",
    "Que veut dire « Du darfst hier nicht rauchen. » ?",
    "Tu n'as pas le droit de fumer ici.",
    "« nicht dürfen » exprime une interdiction : ne pas avoir le droit "
    "de.",
    (("Tu n'es pas obligé de fumer ici.",
      "« ne pas être obligé » se dit avec un autre verbe de modalité : "
      "« nicht müssen »."),
     ("Tu dois fumer ici.",
      "« dürfen » n'exprime pas une obligation, et la phrase contient une "
      "négation."),
     ("Tu peux fumer ici.",
      "« dürfen » seul serait une permission. Que change « nicht » ?")),
    level=2, rappel=REGLE_MODAUX,
)

Q_MUSS_NICHT = question(
    "all_u02_q_muss_nicht", "Je ne suis pas obligé",
    "Comment dit-on « Je ne suis pas obligé de ranger ma chambre » ?",
    "Ich muss mein Zimmer nicht aufräumen.",
    "« nicht müssen » : ne pas être obligé de. L'infinitif aufräumen va à "
    "la fin.",
    (("Ich darf mein Zimmer nicht aufräumen.",
      "« nicht dürfen » exprime une interdiction : je n'ai pas le droit "
      "de ranger ma chambre !"),
     ("Ich muss mein Zimmer aufräumen.",
      "Sans négation, c'est une obligation : je dois ranger."),
     ("Ich räume mein Zimmer nicht auf.",
      "Cette phrase dit seulement « je ne range pas ma chambre » : il "
      "manque l'idée d'obligation.")),
    level=3, rappel=REGLE_MODAUX,
)

Q_FERNSEHEN = question(
    "all_u02_q_fernsehen", "Verbes à particule",
    "Quelle phrase est correcte ? (fern/sehen : regarder la télé)",
    "Ich sehe abends fern.",
    "« fernsehen » est à particule séparable : le verbe conjugué est en 2e "
    "position, la particule « fern » va à la fin.",
    (("Ich fernsehe abends.", "Au présent, la particule d'un verbe "
                              "séparable ne reste pas collée au verbe "
                              "conjugué."),
     ("Ich sehe fern abends.", "La particule est bien séparée, mais elle "
                               "va tout à la fin de la phrase."),
     ("Ich abends fernsehe.", "Dans une phrase déclarative, le verbe "
                              "conjugué est en 2e position.")),
    level=2,
)


# --------------------------------------------------------------------------
# Séance 6 : la recette, les quantités, l'impératif
# --------------------------------------------------------------------------

RECETTE = trous(
    "all_u02_recette", "Les ingrédients",
    "Complète la liste des ingrédients du gâteau marbré.",
    1,
    ("die Packung : le paquet — das Päckchen : le sachet — die Prise : la "
     "pincée — der Esslöffel : la cuillère à soupe — der Teelöffel : la "
     "cuillère à café — die Messerspitze : la pointe de couteau.",
     "das Mehl : la farine — der Zucker : le sucre — das Salz : le sel — "
     "der Pfeffer : le poivre — der Zimt : la cannelle — das Backpulver : "
     "la levure chimique."),
    """Zutaten:
- 280 g @r1@
- 1 @r2@ Salz
- 4 @r3@ Kakaopulver
- 1 Messerspitze @r4@
- 1 @r5@ Vanillezucker""",
    (
        ("r1", "1", "de la farine",
         "Mehl",
         (("Zucker", "« der Zucker » : le sucre"),
          ("Salz", "« das Salz » : le sel"),
          ("Backpulver", "« das Backpulver » : la levure chimique"))),
        ("r2", "2", "une pincée",
         "Prise",
         (("Päckchen", "« das Päckchen » : le sachet"),
          ("Esslöffel", "« der Esslöffel » : la cuillère à soupe"),
          ("Packung", "« die Packung » : le paquet"))),
        ("r3", "3", "des cuillères à soupe",
         "Esslöffel",
         (("Teelöffel", "« der Teelöffel » : la cuillère à café, plus "
                        "petite (der Tee : le thé)"),
          ("Prisen", "« die Prise » : la pincée"),
          ("Messerspitzen", "« die Messerspitze » : la pointe de "
                            "couteau"))),
        ("r4", "4", "de la cannelle",
         "Zimt",
         (("Salz", "« das Salz » : le sel"),
          ("Pfeffer", "« der Pfeffer » : le poivre"),
          ("Mehl", "« das Mehl » : la farine"))),
        ("r5", "5", "un sachet",
         "Päckchen",
         (("Packung", "« die Packung » : le paquet, plus grand"),
          ("Prise", "« die Prise » : la pincée"),
          ("Esslöffel", "« der Esslöffel » : la cuillère à soupe"))),
    ),
)

REGLE_IMPERATIF = (
    "Impératif, 2e personne du singulier (du) : on part de la forme de "
    "« er » et on enlève le -t → er kommt → komm! On ajoute souvent un "
    "-e (mache!, rühre!), mais jamais quand la voyelle est devenue i ou "
    "ie (er nimmt → nimm!, er liest → lies!).",
    "2e personne du pluriel (ihr) : on garde la forme de « ihr » et on "
    "enlève le sujet → ihr kommt → kommt!",
    "L'impératif n'a pas de sujet.",
)

IMPERATIF = trous(
    "all_u02_imperatif", "L'impératif",
    "Julia explique la recette à Tim (du), puis à ses deux frères (ihr). "
    "Mets les verbes à l'impératif.",
    3,
    REGLE_IMPERATIF,
    """Zu Tim:
  @i1@ die Butter mit dem Zucker! (rühren)
  @i2@ die Eier! (trennen)
  @i3@ das Mehl! (nehmen)
  @i4@ das Rezept genau! (lesen)
Zu ihren Brüdern:
  @i5@ die Form mit Butter ein! (einfetten)
  @i6@ den Teig in die Form! (gießen)""",
    (
        ("i1", "1", "rühren, à « du »",
         "Rühre",
         (("Rührst", "« -st » est la terminaison de « du » au présent ; à "
                     "l'impératif, elle disparaît"),
          ("Rührt", "« Rührt » est l'impératif de « ihr » ; Julia parle à "
                    "Tim seul"),
          ("Du rührst", "l'impératif n'a pas de sujet"))),
        ("i2", "2", "trennen, à « du »",
         "Trenne",
         (("Trennt", "« Trennt » est l'impératif de « ihr »"),
          ("Trennst", "« -st » est la terminaison du présent ; à "
                      "l'impératif, elle disparaît"),
          ("Trennen", "« Trennen » est la forme de wir ou de Sie, et il "
                      "faudrait le pronom"))),
        ("i3", "3", "nehmen, à « du »",
         "Nimm",
         (("Nehme", "« nehmen » est un verbe fort en -e : à l'impératif "
                    "de « du », on garde la voyelle de la forme de « er »"),
          ("Nimmst", "« -st » est la terminaison du présent ; à "
                     "l'impératif, elle disparaît"),
          ("Nehmt", "« Nehmt » est l'impératif de « ihr »"))),
        ("i4", "4", "lesen, à « du »",
         "Lies",
         (("Lese", "« lesen » est un verbe fort : à l'impératif de "
                   "« du », on garde la voyelle de la forme de « er »"),
          ("Liest", "« liest » est le présent (er liest) : il reste le "
                    "-t"),
          ("Lest", "« Lest » est l'impératif de « ihr »"))),
        ("i5", "5", "einfetten, à « ihr »",
         "Fettet",
         (("Fette", "« Fette » est l'impératif de « du » ; Julia parle à "
                    "ses deux frères"),
          ("Ihr fettet", "l'impératif n'a pas de sujet"),
          ("Einfettet", "« einfetten » est à particule séparable : la "
                        "particule « ein » est déjà à la fin"))),
        ("i6", "6", "gießen, à « ihr »",
         "Gießt",
         (("Gieß", "« Gieß » est l'impératif de « du »"),
          ("Gießen", "« Gießen » est la forme de wir ou de Sie, et il "
                     "faudrait le pronom"),
          ("Ihr gießt", "l'impératif n'a pas de sujet"))),
    ),
)

Q_BRAUCHEN = question(
    "all_u02_q_brauchen", "brauchen",
    "Comment dit-on « J'ai besoin d'une fourchette » ?",
    "Ich brauche eine Gabel.",
    "« brauchen » (avoir besoin de) est suivi d'un complément direct, "
    "sans préposition. « die Gabel » est féminin : eine Gabel.",
    (("Ich brauche von einer Gabel.", "En français, on dit « besoin "
                                      "de » ; en allemand, « brauchen » "
                                      "n'a pas de préposition."),
     ("Ich brauche einen Gabel.", "« einen » est la forme du masculin. "
                                  "Quel est le genre de « Gabel » ?"),
     ("Ich brauche ein Messer.", "La phrase est correcte, mais « das "
                                 "Messer » veut dire le couteau.")),
    level=2,
)

Q_BACKT = question(
    "all_u02_q_backt", "L'impératif de ihr",
    "La mère de Julia et de Tim leur dit : « ____ den Kuchen 60 Minuten! » "
    "(backen)",
    "Backt",
    "Elle parle à deux enfants : impératif de « ihr », la forme du présent "
    "sans le sujet (ihr backt → backt!).",
    (("Back", "« Back » est l'impératif de « du » ; elle parle à deux "
              "enfants."),
     ("Ihr backt", "L'impératif n'a pas de sujet."),
     ("Backen", "« Backen » est la forme de wir ou de Sie, avec le "
                "pronom : Backen wir! Backen Sie!")),
    level=2, rappel=REGLE_IMPERATIF,
)


# --------------------------------------------------------------------------
# Séance 7 : les repas, le comparatif, les mots composés
# --------------------------------------------------------------------------

REGLE_COMPARATIF = (
    "X > Y : adjectif + -er + als → Max ist größer als Tim.",
    "X = Y : so + adjectif + wie → Max ist so groß wie Tim. X n'atteint "
    "pas Y : nicht so + adjectif + wie.",
    "Beaucoup d'adjectifs courts en a, o, u prennent un tréma : alt → "
    "älter, groß → größer, jung → jünger. Irrégulier : gut → besser.",
)

COMPARATIF = trous(
    "all_u02_comparatif", "Le comparatif",
    "On compare. Choisis la forme qui convient.",
    3,
    REGLE_COMPARATIF,
    """1. Obelix ist @c1@ als Asterix. (groß)
2. Asterix ist so @c2@ wie Obelix. (nett)
3. Mein Bruder ist @c3@ als ich. (alt)
4. Abends essen die Franzosen @c4@ als die Deutschen.
5. Das Essen in der Kantine ist @c5@ wie zu Hause.
6. Mein Kuchen ist @c6@ als dein Kuchen! (gut)""",
    (
        ("c1", "1", "plus grand",
         "größer",
         (("großer", "« groß » est un adjectif court en o : au "
                     "comparatif, il prend un tréma"),
          ("groß", "il manque la marque du comparatif"),
          ("mehr groß", "l'allemand ne fait pas le comparatif avec "
                        "« mehr » : on ajoute une terminaison"))),
        ("c2", "2", "aussi gentil",
         "nett",
         (("netter", "avec « so … wie », l'adjectif ne prend pas la "
                     "marque du comparatif"),
          ("mehr nett", "avec « so … wie », on garde l'adjectif seul, et "
                        "« mehr » ne sert pas au comparatif"),
          ("nicht nett", "« nicht nett » : pas gentil ; la cible dit "
                         "« aussi »"))),
        ("c3", "3", "plus âgé",
         "älter",
         (("alter", "« alt » est un adjectif court en a : au comparatif, "
                    "il prend un tréma"),
          ("alt", "il manque la marque du comparatif"),
          ("jünger", "« jünger » : plus jeune, c'est le contraire"))),
        ("c4", "4", "plus tard",
         "später",
         (("früher", "« früher » : plus tôt, c'est le contraire"),
          ("spät", "il manque la marque du comparatif"),
          ("so spät", "« so spät » se construit avec « wie » : aussi "
                      "tard"))),
        ("c5", "5", "n'est pas aussi bon",
         "nicht so gut",
         (("so gut", "« so gut wie » : aussi bon ; il manque la "
                     "négation"),
          ("besser", "« besser » veut dire meilleur, et se construit "
                     "avec « als »"),
          ("nicht so besser", "avec « so … wie », l'adjectif reste sans "
                              "comparatif"))),
        ("c6", "6", "meilleur",
         "besser",
         (("guter", "« gut » a un comparatif irrégulier"),
          ("güter", "« gut » a un comparatif irrégulier, qui ne se forme "
                    "pas avec un tréma"),
          ("mehr gut", "l'allemand ne fait pas le comparatif avec "
                       "« mehr »"))),
    ),
)

COMPOSES = trous(
    "all_u02_composes", "Le genre des mots composés",
    "Quel est l'article de chaque mot composé ?",
    2,
    ("Un mot composé se lit de droite à gauche : die Kuchenform = la "
     "forme (le moule) à gâteau.",
     "Son genre est celui du **dernier** mot : der Kuchen + die Form → "
     "die Kuchenform."),
    """@g1@ Kuchenform   (der Kuchen + die Form)
@g2@ Backpulver    (backen + das Pulver)
@g3@ Mittagessen   (der Mittag + das Essen)
@g4@ Vanillezucker (die Vanille + der Zucker)
@g5@ Papiertonne   (das Papier + die Tonne)""",
    (
        ("g1", "Kuchenform", "le moule à gâteau",
         "die",
         (("der", "c'est l'article de « Kuchen », le premier mot ; le "
                  "genre vient du dernier"),
          ("das", "aucun des deux mots n'est neutre"))),
        ("g2", "Backpulver", "la levure chimique",
         "das",
         (("der", "le dernier mot, « Pulver », n'est pas masculin"),
          ("die", "le dernier mot, « Pulver », n'est pas féminin"))),
        ("g3", "Mittagessen", "le déjeuner",
         "das",
         (("der", "c'est l'article de « Mittag », le premier mot ; le "
                  "genre vient du dernier"),
          ("die", "aucun des deux mots n'est féminin"))),
        ("g4", "Vanillezucker", "le sucre vanillé",
         "der",
         (("die", "c'est l'article de « Vanille », le premier mot ; le "
                  "genre vient du dernier"),
          ("das", "aucun des deux mots n'est neutre"))),
        ("g5", "Papiertonne", "la poubelle à papier",
         "die",
         (("das", "c'est l'article de « Papier », le premier mot ; le "
                  "genre vient du dernier"),
          ("der", "aucun des deux mots n'est masculin"))),
    ),
)

Q_ABENDBROT = question(
    "all_u02_q_repas", "Les repas en Allemagne",
    "Comment s'appelle le repas froid (pain, beurre, fromage, "
    "charcuterie) que beaucoup d'Allemands prennent le soir ?",
    "das Abendbrot",
    "Le soir, on mange traditionnellement froid en Allemagne : c'est "
    "l'Abendbrot (der Abend : le soir, das Brot : le pain).",
    (("das Mittagessen", "« der Mittag » : midi. C'est le repas de la mi-"
                         "journée."),
     ("das Frühstück", "« das Frühstück » : le petit-déjeuner, le "
                       "matin."),
     ("Kaffee und Kuchen", "C'est la pause de l'après-midi, vers 15 "
                           "heures, avec une part de gâteau.")),
    level=1,
)

Q_SO_WIE = question(
    "all_u02_q_so_wie", "so … wie",
    "« Der Brunch ist in Frankreich so beliebt wie in Deutschland. » Cela "
    "veut dire que le brunch est…",
    "aussi apprécié en France qu'en Allemagne",
    "« so + adjectif + wie » exprime l'égalité : aussi… que.",
    (("plus apprécié en France qu'en Allemagne",
      "« plus… que » se dirait avec un comparatif en -er et « als » : "
      "beliebter als."),
     ("moins apprécié en France qu'en Allemagne",
      "« moins… que » se dirait « nicht so beliebt wie » : il manque "
      "« nicht »."),
     ("apprécié en France, mais pas en Allemagne",
      "La phrase ne contient aucune négation : elle compare deux pays.")),
    level=2, rappel=REGLE_COMPARATIF,
)

Q_COMPOSE = question(
    "all_u02_q_compose", "Former un mot composé",
    "Comment dit-on « le gâteau au beurre » ?",
    "der Butterkuchen",
    "Le mot principal, « der Kuchen », est à la fin et donne l'article ; "
    "« Butter » le précise et se place devant. On écrit le tout en un "
    "seul mot.",
    (("die Kuchenbutter", "Lis le mot de droite à gauche : « Kuchenbutter » "
                          "serait du beurre à gâteau."),
     ("der Butter Kuchen", "Un mot composé s'écrit en un seul mot, sans "
                           "espace."),
     ("die Butterkuchen", "L'ordre est juste, mais l'article vient du "
                          "dernier mot : quel est le genre de « Kuchen » "
                          "?")),
    level=2,
)


# --------------------------------------------------------------------------
# Séance 8 : l'environnement, la subordonnée en dass
# --------------------------------------------------------------------------

REGLE_DASS = (
    "« dass » (que) introduit une subordonnée : Er will, dass… (il veut "
    "que), Er findet, dass… (il trouve que), Er sagt, dass… (il dit "
    "que).",
    "Comme après « weil » : une virgule avant « dass », le sujet juste "
    "après, et le verbe conjugué à la fin.",
)

DASS = trous(
    "all_u02_dass", "Rapporter avec dass",
    "Les amis de Tim parlent d'environnement. Choisis la fin de phrase "
    "qui convient.",
    3,
    REGLE_DASS,
    """1. Meine Mutter will, dass @z1@.
2. Tim sagt, dass @z2@.
3. Hanna findet, dass @z3@.
4. Sofia sagt, dass @z4@.""",
    (
        ("z1", "1", "que nous mangions bio",
         "wir Bio essen",
         (("wir essen Bio", "après « dass », le verbe conjugué ne reste "
                            "pas en 2e position"),
          ("essen wir Bio", "après « dass », le sujet suit la conjonction, "
                            "et le verbe va ailleurs"),
          ("ihr Bio esst", "l'ordre est juste, mais « ihr » veut dire "
                           "vous"))),
        ("z2", "2", "qu'on doit recycler les déchets",
         "man den Müll recyceln muss",
         (("man muss den Müll recyceln", "après « dass », où va le verbe "
                                         "conjugué ?"),
          ("man den Müll muss recyceln", "le verbe conjugué va tout à la "
                                         "fin, après l'infinitif"),
          ("man den Müll wegwerfen muss", "l'ordre est juste, mais "
                                          "« wegwerfen » veut dire "
                                          "jeter"))),
        ("z3", "3", "que les fruits bio ont meilleur goût",
         "Bioobst besser schmeckt",
         (("Bioobst schmeckt besser", "après « dass », où va le verbe "
                                      "conjugué ?"),
          ("Bioobst schlechter schmeckt", "l'ordre est juste, mais "
                                          "« schlechter » veut dire "
                                          "moins bon"),
          ("Bioobst besser schmecken", "« das Obst » est un singulier : "
                                       "le verbe ne va pas au pluriel"))),
        ("z4", "4", "que nous achetons des produits régionaux",
         "wir regionale Produkte kaufen",
         (("wir kaufen regionale Produkte", "après « dass », où va le "
                                            "verbe conjugué ?"),
          ("wir regionale Produkte kauft", "« kauft » ne va pas avec "
                                           "« wir »"),
          ("wir regionale Produkte wegwerfen", "l'ordre est juste, mais "
                                               "« wegwerfen » veut dire "
                                               "jeter"))),
    ),
)

Q_DASS = question(
    "all_u02_q_dass", "La subordonnée en dass",
    "Quelle phrase est correcte ?",
    "Meine Schwester sagt, dass sie kein Fleisch isst.",
    "Une virgule avant « dass », le sujet « sie » juste après, et le verbe "
    "conjugué « isst » à la fin.",
    (("Meine Schwester sagt, dass sie isst kein Fleisch.",
      "C'est l'ordre d'une phrase principale. Où va le verbe conjugué "
      "après « dass » ?"),
     ("Meine Schwester sagt dass, sie kein Fleisch isst.",
      "L'ordre des mots est juste, mais la virgule se place avant la "
      "conjonction."),
     ("Meine Schwester sagt, weil sie kein Fleisch isst.",
      "« weil » veut dire « parce que » : « elle dit parce qu'elle… » n'a "
      "pas de sens. Il faut le mot qui veut dire « que ».")),
    level=3, rappel=REGLE_DASS,
)

Q_MUELL = question(
    "all_u02_q_muell", "Le tri des déchets",
    "En Allemagne, où jette-t-on une boîte de conserve en métal ?",
    "in den gelben Sack",
    "Le sac jaune reçoit les emballages en plastique et les boîtes de "
    "conserve en métal.",
    (("in die Biomülltonne", "La poubelle « bio » reçoit les déchets "
                             "organiques : épluchures, restes de "
                             "repas…"),
     ("in die Papiertonne", "« das Papier » : le papier. Une boîte de "
                            "conserve est en métal."),
     ("in den Glascontainer", "« das Glas » : le verre. Une boîte de "
                              "conserve est en métal.")),
    level=2,
)


# --------------------------------------------------------------------------
# Séance 9 : le conseil de famille, wollen, la proposition, la durée
# --------------------------------------------------------------------------

Q_WOLLEN = question(
    "all_u02_q_wollen", "wollen",
    "Complète : « Meine Eltern ____, dass wir früh ins Bett gehen. »",
    "wollen",
    "wollen : ich will, du willst, er will, wir wollen, ihr wollt, sie "
    "wollen. « Meine Eltern » = sie (pluriel).",
    (("will", "« will » va avec ich ou er, sie, es ; « meine Eltern » "
              "sont plusieurs."),
     ("wollt", "« wollt » va avec « ihr »."),
     ("willst", "« willst » va avec « du ».")),
    level=2,
)

Q_SOLLEN = question(
    "all_u02_q_sollen", "Faire une proposition",
    "Tu proposes à ton ami d'aller au cinéma. Que dis-tu ?",
    "Sollen wir ins Kino gehen?",
    "« Sollen wir…? » (et si on… ?) et « Wir könnten… » (on pourrait…) "
    "servent à faire une proposition.",
    (("Müssen wir ins Kino gehen?", "« müssen » demande une obligation : "
                                    "« est-ce qu'on doit… ? »."),
     ("Dürfen wir ins Kino gehen?", "« dürfen » demande une permission : "
                                    "« a-t-on le droit… ? »."),
     ("Wir sollen ins Kino gehen.", "Sans inversion, ce n'est plus une "
                                    "question : « nous sommes censés "
                                    "aller au cinéma ».")),
    level=3,
)

Q_DAUER = question(
    "all_u02_q_dauer", "Wie lange?",
    "« Der Film fängt um 20 Uhr 15 an und endet um 22 Uhr. » Wie lange "
    "dauert er?",
    "eine Stunde und 45 Minuten",
    "« anfangen » : commencer, « enden » : finir, « dauern » : durer. De "
    "20 h 15 à 22 h, il s'écoule 1 h 45.",
    (("zwei Stunden und 15 Minuten", "Refais le calcul : de 20 h 15 à "
                                     "21 h 15, puis de 21 h 15 à 22 h."),
     ("45 Minuten", "Le film dure plus d'une heure : de 20 h 15 à 21 h 15, "
                    "il n'est pas fini."),
     ("um 22 Uhr", "« um 22 Uhr » répond à « wann? » (quand ?). "
                   "« Wie lange? » demande combien de temps.")),
    level=2,
)


PATTERNS = (
    ETAGES, PIECES, Q_MAISON, Q_O_LONG,
    VILLE, WEIL, Q_WEIL, Q_TREFFEN,
    CHAMBRE, PREPOSITIONS, DATIF_LIEU, POSITION, KEIN, Q_KEIN, Q_DATIF,
    Q_DESWEGEN,
    MODAUX, TACHES, Q_DARF_NICHT, Q_MUSS_NICHT, Q_FERNSEHEN,
    RECETTE, IMPERATIF, Q_BRAUCHEN, Q_BACKT,
    COMPARATIF, COMPOSES, Q_ABENDBROT, Q_SO_WIE, Q_COMPOSE,
    DASS, Q_DASS, Q_MUELL,
    Q_WOLLEN, Q_SOLLEN, Q_DAUER,
)

MODULE = Module(
    key="allemand_u02",
    title="Unité 2 — Bei mir zu Hause",
    level=2,
    summary="Révisions de l'unité 2 : la maison et la chambre, locatif et "
            "prépositions de lieu, weil et dass, kein, müssen et dürfen, "
            "tâches ménagères, recette et impératif, comparatif, mots "
            "composés, environnement. " + INTITULE,
    keys=tuple(p.key for p in PATTERNS),
)
