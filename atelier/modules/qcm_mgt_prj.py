"""Module QCM « Management de projet SI ».

Questionnaire demandé par l'enseignant (demande n°21), conforme au
fichier qu'il a fourni : quarante questions à choix unique, rangées par
difficulté croissante, de N1 (définitions du cours) à N4 (cas pratiques
et calculs : charge, coût des ressources, budget, RAC / RAF, criticité).

Les thèmes : projet et programme, triangle d'or, WBS et lotissement,
RACI, jalons et comités, acteurs et parties prenantes, contrats, budget
et indicateurs de suivi, risques, cycles de vie et méthodes, stratégies
de déploiement, conduite du changement et bilan de projet.

Chaque question a quatre propositions et une seule juste ; l'explication
est montrée après une bonne réponse.
"""

from ..engine import Module, qcm_pattern

# (énoncé, (quatre propositions), index de la bonne, niveau, explication)
# Les propositions gardent l'ordre du fichier de l'enseignant, où la bonne
# réponse change déjà de lettre d'une question à l'autre. L'élève reçoit de
# toute façon un ordre tiré au sort par sa copie (cf. `shuffled_blanks`).
QUESTIONS = (
    ('Selon la définition du cours, un projet SI est un ensemble…',
     ('permanent et structuré de ressources destiné à collecter, '
      'traiter et diffuser l’information.',
      'de tâches informatiques récurrentes réalisées par la DSI.',
      'temporaire et organisé d’activités permettant de transformer'
      ' une composante du SI pour répondre à un besoin métier.',
      'temporaire et organisé d’activités permettant de maintenir '
      'en conditions opérationnelles une composante du SI.'),
     2, 1,
     'Le projet transforme (conception, développement, évolution) '
     'une composante du SI ; le maintien en conditions '
     'opérationnelles relève du « Run », pas du projet. La '
     'proposition « ensemble permanent et structuré de ressources »'
     ' définit, elle, le SI lui-même.'),

    ('Quelles sont les trois contraintes du « triangle d’or » d’un '
     'projet ?',
     ('Coûts, ressources, risques.',
      'Coûts, délais, périmètre.',
      'Budget, planning, sponsor.',
      'Coûts, délais, qualité.'),
     1, 1,
     'La qualité n’est pas un sommet du triangle : elle se situe au'
     ' centre et dépend des trois contraintes coûts / délais / '
     'périmètre.'),

    ('Que signifie l’acronyme WBS ?',
     ('Work Breakdown Schedule – Planning de Découpage Projet.',
      'Web Based System – Système accessible par le Web.',
      'Workload Balance Sheet – Bilan de charge de travail.',
      'Work Breakdown Structure – Structure de Découpage Projet.'),
     3, 1,
     'La WBS est une structure (et non un planning) : elle '
     'décompose les livrables et le travail en composants plus '
     'petits.'),

    ('Dans une matrice RACI, que désigne la lettre « A » ?',
     ('Auditor (auditeur) : celui qui contrôle la conformité du '
      'projet a posteriori.',
      'Accountable (approbateur) : celui qui prend la '
      'responsabilité du résultat et s’assure que la tâche est '
      'correctement réalisée.',
      'Assistant : celui qui aide l’équipe projet ponctuellement.',
      'Accountable (approbateur) : celui qui réalise l’activité et '
      'en exécute les tâches.'),
     1, 1,
     'Celui qui réalise l’activité est le « R » (Responsible). Le «'
     ' A » porte la responsabilité du résultat.'),

    ('Qu’est-ce qu’un jalon ?',
     ('Un point d’arrêt permettant le suivi de l’avancement et la '
      'vérification de la conformité d’une étape avant de passer à '
      'la suivante.',
      'Un point d’arrêt marquant la fin définitive du projet, après'
      ' la signature du PV de recette.',
      'Une tâche de longue durée située sur le chemin critique du '
      'projet.',
      'Le document qui décrit le périmètre, les livrables, les '
      'hypothèses et les contraintes.'),
     0, 1,
     'Il existe plusieurs jalons tout au long du cycle de vie (J0 à'
     ' J6), pas uniquement en fin de projet. La proposition '
     'décrivant un document (périmètre, livrables, hypothèses, '
     'contraintes) correspond à la note de cadrage.'),

    ('À quelle fréquence se réunit généralement le COPIL (comité de'
     ' pilotage) ?',
     ('Quotidienne.',
      'Une seule fois, au lancement du projet.',
      'Mensuelle.',
      'Hebdomadaire.'),
     2, 1,
     'COPIL : mensuel ; COPROJ : hebdomadaire ; COMOP : quotidien.'),

    ('Quel acteur fournit le financement et soutient le projet à un'
     ' niveau stratégique ?',
     ('La maîtrise d’œuvre (MOE).',
      'La maîtrise d’ouvrage (MOA).',
      'Le sponsor du projet.',
      'Les utilisateurs-clés (key-users).'),
     2, 1,
     'La MOA peut « quelquefois » financer le projet, mais c’est le'
     ' sponsor qui fournit le financement et soutient le projet au '
     'niveau stratégique.'),

    ('Quel document, issu de la DSI, définit sur 3 à 5 ans les '
     'grandes orientations du SI ?',
     ('Le Schéma Directeur du Système d’Information (SDSI).',
      'Le cahier des charges.',
      'Le plan de communication.',
      'La stratégie SI.'),
     0, 1,
     'La stratégie SI est la traduction de la stratégie '
     'd’entreprise dans le SI ; le SDSI est le document qui en '
     'décline la vision cible et les trajectoires sur 3 à 5 ans.'),

    ('Selon le cours, quelle part de son temps un chef de projet '
     'consacre-t-il à communiquer ?',
     ('Entre 75 % et 90 %.',
      'Entre 25 % et 40 %.',
      'Entre 60 % et 75 %.',
      'Moins de 10 %.'),
     0, 1,
     'Réunions, rapports, tableaux de bord, reporting, livrables, '
     'mails… : le chef de projet communique 75 à 90 % de son temps.'),

    ('Comment calcule-t-on la criticité d’un risque ?',
     ('Gravité ÷ Vraisemblance.',
      'Vraisemblance + Impact.',
      'Vraisemblance × Impact.',
      'Coût × Délai.'),
     2, 1,
     'Criticité = Vraisemblance × Impact (ex. : 4 × 5 = 20).'),

    ('Quelle affirmation distingue correctement Système '
     'd’Information et système informatique ?',
     ('Le SI intègre des ressources humaines, organisationnelles et'
      ' des données ; le système informatique en est la partie '
      'technologique.',
      'Le système informatique intègre les ressources humaines et '
      'organisationnelles ; le SI en est la partie technologique.',
      'Les deux notions sont synonymes et désignent '
      'l’infrastructure matérielle et logicielle.',
      'Le système informatique englobe le SI et le complète par les'
      ' processus métier.'),
     0, 2,
     'Le système informatique est la partie technologique du SI et '
     'ne couvre pas les aspects humains et organisationnels ; la '
     'proposition qui attribue au système informatique les '
     'ressources humaines et organisationnelles inverse les deux '
     'notions.'),

    ('Quelle est la définition d’un programme selon le PMI (PMBoK) '
     '?',
     ('Un ensemble de projets gérés de façon coordonnée afin '
      'd’obtenir des gains supérieurs à ceux d’une gestion '
      'indépendante.',
      'Un regroupement de sous-projets fortement interdépendants à '
      'l’intérieur d’un même projet.',
      'Un ensemble de projets, de programmes et/ou de '
      'sous-portefeuilles gérés en commun pour atteindre un but '
      'stratégique partagé.',
      'Une structure obligatoire à laquelle tout projet doit être '
      'rattaché.'),
     0, 2,
     'Un ensemble de projets, de programmes et/ou de '
     'sous-portefeuilles gérés en commun pour un but stratégique '
     'partagé est la définition du portefeuille ; un regroupement '
     'de sous-projets fortement interdépendants est celle du lot. '
     'Un projet n’a pas forcément besoin d’appartenir à un '
     'programme.'),

    ('Quelle affirmation sur le forfait et la régie est exacte ?',
     ('Le forfait est une obligation de résultat ; la régie est une'
      ' obligation de moyens.',
      'Le forfait et la régie sont tous deux des obligations de '
      'résultat, seul le lieu de réalisation diffère.',
      'Le forfait consiste à mettre à disposition des compétences '
      'chez le client pour une durée donnée.',
      'Le forfait est une obligation de moyens ; la régie est une '
      'obligation de résultat.'),
     0, 2,
     'Forfait = prix + délai engagés (résultat) ; régie = mise à '
     'disposition de compétences (moyens), réalisée chez le client.'),

    ('Qu’est-ce que la communication unilatérale cherchée (« pull '
     '») ?',
     ('Une communication envoyée à des récepteurs spécifiques qui '
      'ont besoin de connaître l’information.',
      'Un échange d’information multidirectionnel entre deux ou '
      'plusieurs parties (réunions, visioconférences…).',
      'Une communication pour de gros volumes ou de nombreux '
      'publics, diffusée automatiquement par courriel à l’ensemble '
      'des destinataires.',
      'Une communication pour de gros volumes ou de nombreux '
      'publics, que les récepteurs consultent à leur propre '
      'discrétion (intranet, bases de leçons apprises…).'),
     3, 2,
     'Une information envoyée à des récepteurs spécifiques ou '
     'diffusée automatiquement relève du « push » ; l’échange '
     'multidirectionnel (réunions, visioconférences) est la '
     'communication interactive. Dans le « pull », c’est le '
     'récepteur qui va chercher l’information à sa discrétion.'),

    ('Qu’est-ce que le déploiement en parallèle (« double run ») ?',
     ('L’ancien et le nouveau système fonctionnent simultanément '
      'pendant une période donnée afin de comparer les résultats.',
      'Le nouveau système remplace entièrement l’ancien en une '
      'seule fois, à une date précise.',
      'Deux environnements techniques identiques coexistent et l’on'
      ' bascule progressivement le trafic de l’un vers l’autre.',
      'La nouvelle version est déployée auprès d’un échantillon '
      'restreint d’utilisateurs réels, puis élargie.'),
     0, 2,
     'Deux environnements techniques identiques avec bascule '
     'progressive du trafic correspondent au blue/green ; le '
     'remplacement total en une seule fois au Big Bang ; '
     'l’échantillon restreint d’utilisateurs réels au déploiement '
     'canari.'),

    ('Quelles pratiques caractérisent la méthode XP (eXtreme '
     'Programming) ?',
     ('Développement en binôme, adaptation du volume de travail en '
      'cours aux capacités de l’équipe, combinaison avec d’autres '
      'méthodes.',
      'Développement en binôme, refactorisation, client sur site, '
      'appropriation collective.',
      'Réunions quotidiennes courtes, réponse rapide au changement,'
      ' partage du code et des connaissances.',
      'Attention portée aux personnes, à la communauté, aux talents'
      ' et à la collaboration.'),
     1, 2,
     'La proposition associant le binôme à l’adaptation du volume '
     'de travail en cours mélange XP et Kanban ; les réunions '
     'quotidiennes courtes et la réponse rapide au changement '
     'décrivent Scrum ; l’attention aux personnes, à la communauté '
     'et aux talents décrit Crystal.'),

    ('De quoi se compose le budget d’un projet ?',
     ('Du TJM multiplié par la durée totale du projet.',
      'Des coûts humains et des frais généraux, auxquels s’ajoute '
      'la marge du prestataire.',
      'De l’agrégation des coûts, de la réserve pour imprévus et de'
      ' la réserve de management.',
      'De l’agrégation des coûts et de la réserve pour imprévus '
      'uniquement.'),
     2, 2,
     'Le budget est la somme de trois éléments ; il peut être '
     'exprimé en euros ou en jours-hommes.'),

    ('Quel est le principe du cycle en V ?',
     ('À chaque étape, une fonctionnalité supplémentaire est '
      'livrée.',
      'Les tests sont prévus pendant la phase de conception '
      'correspondante ; en cas d’échec, on revient à cette phase.',
      'Les mêmes étapes sont répétées à l’identique à chaque '
      'itération, avec un livrable par itération.',
      'Les tests sont conçus et exécutés en fin de cycle, une fois '
      'l’ensemble du développement terminé.'),
     1, 2,
     'Le cycle en V est apparu pour pallier le manque de réactivité'
     ' de la cascade, en associant chaque phase de conception à un '
     'niveau de test. La répétition à l’identique des mêmes étapes '
     'décrit le cycle itératif ; la livraison d’une fonctionnalité '
     'supplémentaire à chaque étape, le cycle incrémental ; des '
     'tests conçus en fin de cycle, la cascade.'),

    ('Que désigne le « périmètre du projet » (par opposition au '
     'périmètre du produit) ?',
     ('L’enveloppe budgétaire et la durée allouées au projet.',
      'Le travail qui doit être accompli pour livrer un produit, un'
      ' service ou un résultat possédant les caractéristiques et '
      'fonctions spécifiées.',
      'La liste des parties prenantes internes et externes du '
      'projet.',
      'Les particularités et fonctions qui caractérisent le '
      'produit, le service ou le résultat.'),
     1, 2,
     'Les particularités et fonctions qui caractérisent le produit '
     'définissent le périmètre du produit, et non celui du projet. '
     'Les deux notions peuvent se confondre dans la pratique, mais '
     'elles restent distinctes.'),

    ('Une charge de 3 ETP pendant une semaine correspond à :',
     ('un travail nécessitant 1 personne à plein temps pendant 3 '
      'semaines.',
      'un travail nécessitant 3 personnes à mi-temps pendant la '
      'semaine.',
      'un travail de 3 jours-hommes répartis sur la semaine.',
      'un travail nécessitant 3 personnes affectées à plein temps '
      'pendant toute la semaine.'),
     3, 2,
     'ETP = Équivalent Temps Plein : n ETP sur une période = n '
     'personnes à plein temps sur toute la période (soit ici '
     'environ 15 JH, pas 3).'),

    ('Selon la typologie ISO/IEC 15288:2015, qui sont les « '
     'opérateurs » ?',
     ('Ceux qui assurent le support technique et la maintenance du '
      'SI.',
      'Les organisations ou individus qui commandent et financent '
      'le projet.',
      'Ceux qui utilisent et exploitent le SI après sa livraison.',
      'Ceux qui conçoivent, développent et fournissent le SI.'),
     2, 3,
     'Ceux qui assurent le support technique et la maintenance sont'
     ' les mainteneurs ; ceux qui commandent et financent le '
     'projet, les acquéreurs ; ceux qui conçoivent, développent et '
     'fournissent le SI, les fournisseurs.'),

    ('Dans la matrice d’influence, quelle stratégie adopter pour '
     'une partie prenante à FORTE influence et FAIBLE impact ?',
     ('« Surveiller avec peu d’effort » : information complète, '
      'suivi régulier.',
      '« Minimiser les efforts » : informations essentielles, '
      'contact minimal.',
      '« Gérer de près » : engagement régulier, maintien de la '
      'satisfaction.',
      '« À garder informés » : suivi fréquent, anticipation des '
      'besoins.'),
     3, 3,
     '« Surveiller avec peu d’effort » correspond au quadrant '
     'faible influence / fort impact ; « Gérer de près » à forte '
     'influence / fort impact ; « Minimiser les efforts » à faible '
     'influence / faible impact.'),

    ('Que mesure l’indicateur RAC ?',
     ('Le volume de travail restant pour atteindre les objectifs de'
      ' la tâche ou du projet.',
      'Les coûts du projet déjà consommés.',
      'La différence entre le coût prévisionnel et le consommé '
      '(Reste À Consommer).',
      'La revue du coût d’une tâche ou d’une phase.'),
     2, 3,
     'Le volume de travail restant est le RAF (Reste À Faire) ; les'
     ' coûts déjà engagés sont le consommé ; la revue du coût d’une'
     ' tâche ou d’une phase est l’estimé.'),

    ('Dans le cycle de vie traditionnel présenté en cours (J0 à '
     'J6), à quoi correspond le jalon J3 ?',
     ('GO réalisation.',
      'GO conception.',
      'Fin projet / Go-live.',
      'GO pilotes.'),
     0, 3,
     'J0 lancement étude, J1 GO projet, J2 GO conception, J3 GO '
     'réalisation, J4 tests, J5 GO pilotes, J6 fin projet / '
     'Go-live.'),

    ('Quelle enveloppe budgétaire est destinée à couvrir les '
     'risques NON identifiés ?',
     ('L’avenant budgétaire accordé par la MOA.',
      'La réserve de management.',
      'La réserve pour imprévus.',
      'Le reste à consommer (RAC).'),
     1, 3,
     'La réserve pour imprévus couvre les risques identifiés et '
     'acceptés ; la réserve de management couvre les risques non '
     'identifiés.'),

    ('Quelle stratégie de déploiement permet une validation en '
     'conditions réelles sur un périmètre restreint et '
     'représentatif, dont les utilisateurs deviennent ensuite '
     'ambassadeurs de la solution ?',
     ('Le déploiement blue/green.',
      'Le déploiement par phases (progressif).',
      'Le déploiement Big Bang.',
      'Le déploiement pilote.'),
     3, 3,
     'Le déploiement par phases facilite aussi la conduite du '
     'changement, mais il enchaîne des étapes validées '
     'successivement ; c’est le pilote qui teste un périmètre '
     'restreint avant généralisation.'),

    ('Quel comité gère une crise majeure (dérive budgétaire, '
     'retard, incident critique), prend les décisions d’urgence et '
     'définit le plan de redressement ?',
     ('Le COTECH.',
      'Le COPIL.',
      'Le comité de changement (ad hoc).',
      'Le comité métier.'),
     2, 3,
     'Le COPIL gère les escalades des problèmes critiques et les '
     'décisions majeures, mais c’est le comité de changement, réuni'
     ' ad hoc, qui traite la crise et le plan de redressement.'),

    ('Quels livrables sont associés à l’étape « Conception '
     'détaillée » du cycle AFNOR Z67-101 ?',
     ('Rapports d’évaluation, fiches de bilan projet, '
      'capitalisation d’expérience.',
      'Note de cadrage, stratégie de l’accompagnement au '
      'changement, étude de faisabilité.',
      'Documentation, fiches de tests et suivi des corrections, '
      'rapport d’avancement.',
      'Cahier des charges, plan de conduite du changement, plan de '
      'communication, plans de tests.'),
     3, 3,
     'La note de cadrage, l’étude de faisabilité et la stratégie '
     'd’accompagnement au changement relèvent de l’étude préalable '
     '(la stratégie précède le plan de conduite du changement) ; la'
     ' documentation et les fiches de tests relèvent de la '
     'réalisation ; les rapports d’évaluation et la capitalisation '
     'd’expérience, de l’évaluation / clôture.'),

    ('Parmi les facteurs de résistance au changement, que recouvre '
     'la « perte de pouvoir » ?',
     ('La baisse de la facilité d’usage perçue, notamment l’effort '
      'nécessaire pour apprendre.',
      'La réduction de la « zone d’incertitude » liée à la '
      'détention de savoir-faire ou d’informations clés.',
      'L’insatisfaction concernant l’ergonomie du nouveau système.',
      'L’opposition à une nouvelle organisation dégradant les '
      'conditions de travail.'),
     1, 3,
     'La facilité d’usage perçue relève de la « perception des '
     'acteurs » ; l’ergonomie des « insatisfactions concernant le '
     'SI » ; la dégradation des conditions de travail de « '
     'l’opposition à la nouvelle organisation ».'),

    ('Dans la classification des parties prenantes, qui sont les « '
     'groupes d’intérêt » ?',
     ('Des individus ou organisations sans influence directe, qui '
      'ne seront pas directement affectés, mais qui pourraient '
      'avoir un intérêt significatif à la réalisation du projet.',
      'Les régulateurs qui imposent des exigences légales au SI.',
      'Des individus ou organisations dont l’intérêt est plus '
      'indirectement lié au projet.',
      'Des organisations ou individus directement impliqués dans le'
      ' projet (ressources, utilisation, clients internes).'),
     0, 3,
     'Un intérêt plus indirectement lié au projet caractérise les '
     'parties prenantes secondaires ; l’implication directe '
     '(ressources, utilisation, clients internes) caractérise les '
     'parties prenantes primaires.'),

    ('Le risque « Non-conformité RGPD » est évalué avec une '
     'vraisemblance de 3 et un impact de 4. Quelle est sa criticité'
     ' et quel traitement préconiser ?',
     ('12 – niveau élevé : traitement prioritaire.',
      '12 – niveau moyen : réduction et surveillance.',
      '7 – niveau moyen : réduction et surveillance.',
      '7 – niveau faible : acceptation ou transfert du risque.'),
     1, 4,
     '3 × 4 = 12 (et non 3 + 4). Dans l’exemple du cours, ce risque'
     ' (R3) est classé orange (moyen) ; seul R1 (4 × 5 = 20) est '
     'rouge.'),

    ('Une tâche est estimée à 10 JH. Deux personnes y sont '
     'affectées à plein temps. Quelle affirmation est exacte ?',
     ('Elle durera 5 jours, avec une charge de 10 ETP sur la '
      'période.',
      'Elle durera 5 jours, avec une charge de 2 ETP sur la '
      'période.',
      'Elle durera 10 jours, quel que soit le nombre de personnes '
      'affectées.',
      'Elle durera 20 jours, avec une charge de 2 ETP sur la '
      'période.'),
     1, 4,
     '10 JH ÷ 2 personnes = 5 jours ; 2 personnes à plein temps sur'
     ' la période = 2 ETP.'),

    ('Un chef de projet fonctionnel (TJM 700 €) intervient 10 jours'
     ' et un développeur (TJM 500 €) intervient 20 jours. Quel est '
     'le coût de ces ressources ?',
     ('1 200 €.',
      '19 000 €.',
      '12 000 €.',
      '17 000 €.'),
     3, 4,
     '700 × 10 + 500 × 20 = 7 000 + 10 000 = 17 000 €. 19 000 € '
     'correspond à une inversion des durées ; 12 000 € à (700 + '
     '500) × 10.'),

    ('Coûts agrégés : 100 k€ ; réserve pour imprévus : 10 k€ ; '
     'réserve de management : 5 k€. Quel est le budget du projet et'
     ' quelle enveloppe mobiliser si un risque non identifié '
     'survient ?',
     ('110 k€ ; la réserve de management.',
      '115 k€ ; la réserve de management.',
      '115 k€ ; la réserve pour imprévus.',
      '110 k€ ; la réserve pour imprévus.'),
     1, 4,
     'Budget = 100 + 10 + 5 = 115 k€. La réserve pour imprévus '
     'couvre les risques identifiés et acceptés ; les risques non '
     'identifiés relèvent de la réserve de management.'),

    ('Une banque doit mettre en production une nouvelle version de '
     'sa plateforme de paiement, disponible 24h/24. Aucune '
     'indisponibilité n’est tolérée et un retour instantané à la '
     'version précédente doit être possible ; le budget permet de '
     'doubler l’infrastructure. Quelle stratégie choisir ?',
     ('Le déploiement Big Bang.',
      'Le déploiement en parallèle (double run).',
      'Le déploiement canari.',
      'Le déploiement blue/green.'),
     3, 4,
     'Blue/green : deux environnements identiques, temps '
     'd’indisponibilité nul, bascule et retour quasi instantanés, '
     'adapté aux environnements critiques 24/7 (banque). Le canari '
     'expose un échantillon d’utilisateurs et gère des versions '
     'simultanées ; le double run impose double saisie.'),

    ('Une DSI remplace son SI financier. La fiabilité des données '
     'est la priorité absolue : les résultats de l’ancien et du '
     'nouveau système doivent être comparés avant l’arrêt de '
     'l’ancien. Quelle stratégie retenir et quel inconvénient '
     'anticiper ?',
     ('Le Big Bang ; il faut anticiper un retour arrière difficile.',
      'Le double run ; il faut anticiper une double infrastructure '
      'technique et une gestion complexe du trafic.',
      'Le déploiement pilote ; il faut anticiper un périmètre '
      'représentatif difficile à trouver.',
      'Le double run ; il faut anticiper une double saisie et une '
      'charge importante pour les utilisateurs.'),
     3, 4,
     'La stratégie est bien le double run, mais la « double '
     'infrastructure et gestion du trafic » est l’inconvénient du '
     'blue/green. Le double run implique coûts élevés, double '
     'saisie, double maintenance et charge pour les utilisateurs.'),

    ('Dans une matrice RACI, pour la tâche « Rédaction du cahier '
     'des charges », le chef de projet MOA est noté « R/A » et la '
     'DSI « C ». Quelle interprétation est correcte ?',
     ('La DSI valide le cahier des charges rédigé par le chef de '
      'projet MOA.',
      'Le chef de projet MOA rédige le cahier des charges et la DSI'
      ' en porte la responsabilité finale.',
      'Le chef de projet MOA rédige le cahier des charges et porte '
      'la responsabilité du résultat ; la DSI est tenue informée '
      'des décisions sans être sollicitée.',
      'Le chef de projet MOA rédige le cahier des charges et porte '
      'la responsabilité du résultat ; la DSI est sollicitée pour '
      'son expertise avant ou pendant la rédaction.'),
     3, 4,
     '« C » (Consulted) désigne celui qui est consulté pour son '
     'expertise avant ou pendant l’exécution, à ne pas confondre '
     'avec « I » (Informed), informé sans participer au travail. « '
     'R/A » signifie que le même acteur réalise l’activité et porte'
     ' la responsabilité du résultat.'),

    ('Lors du lotissement d’un projet, selon quel critère '
     'regroupe-t-on les sous-projets au sein d’un même lot ?',
     ('Relier les modules/applications ayant les interdépendances '
      'les plus faibles, afin de paralléliser les lots.',
      'Regrouper les sous-projets de budget équivalent.',
      'Relier les modules/applications ayant les interdépendances '
      'les plus fortes.',
      'Regrouper les sous-projets confiés à un même prestataire.'),
     2, 4,
     'L’objectif d’un lot est de relier les modules/applications '
     'les plus interdépendants ; les lots peuvent ensuite se '
     'chevaucher ou se paralléliser partiellement.'),

    ('Une phase a un coût prévisionnel de 50 k€ ; 30 k€ ont été '
     'consommés et l’équipe estime qu’il reste 25 JH de travail. '
     'Quelle affirmation est exacte ?',
     ('RAF = 20 k€ ; RAC = 25 JH.',
      'RAC = 80 k€ ; RAF = 25 JH.',
      'RAC = 20 k€ ; RAF = 25 JH.',
      'RAC = 20 k€ ; RAF = 5 JH.'),
     2, 4,
     'RAC = prévisionnel − consommé = 50 − 30 = 20 k€ ; le RAF est '
     'le volume de travail restant (25 JH). La proposition « RAF = '
     '20 k€ ; RAC = 25 JH » inverse les deux indicateurs.'),

    ('Quelle affirmation sur le bilan de projet (REX/RETEX) est '
     'conforme au cours ?',
     ('Il est réalisé à la clôture, après la signature du PV de '
      'recette (et à mi-parcours si le projet est long), sans '
      'chercher à désigner des responsables.',
      'Il est réalisé uniquement par la direction, une fois le '
      'projet terminé, pour évaluer le chef de projet.',
      'Il est facultatif lorsque les objectifs QCD ont été '
      'atteints.',
      'Il est réalisé à la clôture, avant la signature du PV de '
      'recette, afin d’identifier les responsables des écarts '
      'constatés.'),
     0, 4,
     'Le bilan est un moment de prise de recul : on cherche à tirer'
     ' des enseignements, pas à désigner des responsables. Il '
     'intervient après la signature du PV de recette.'),
)

PATTERNS = tuple(
    qcm_pattern("qcm_mgt_prj_%02d" % (rang + 1), rang + 1, question,
                choices, answer, level, explanation)
    for rang, (question, choices, answer, level, explanation)
    in enumerate(QUESTIONS)
)

MODULE = Module(
    key="qcm_mgt_prj",
    title="Management de projet SI",
    level=2,
    summary="Projet et triangle d'or, WBS et RACI, jalons et comités, "
            "budget et suivi, risques, cycles de vie, déploiement et "
            "conduite du changement.",
    keys=tuple(p.key for p in PATTERNS),
)
