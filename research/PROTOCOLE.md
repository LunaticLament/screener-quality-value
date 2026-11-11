# Protocole indépendant de valorisation approfondie

Ce dépôt est indépendant du site de portefeuille personnel et du portefeuille modèle.

## Hiérarchie des preuves
1. Chaque analyse qualitativement conforme doit expliciter le modèle économique, le moat, l'avenir à dix ans, la conversion en FCF par action, le ROIC durable, le bilan, la gouvernance et les risques d'invalidation.
2. Étudier cinq exercices annuels et la dernière publication avec dates, unités, devises, liens directs aux documents d'émetteurs.
3. Rapprocher les FCF publiés à leur base normalisée par exercice : variations de BFR, CAPEX, SBC et dilution, M&A et périmètre, éléments exceptionnels, fiscalité et dette. Ne jamais déclarer qu'une simple moyenne est un FCF normalisé.
4. Construire trois scénarios spécifiques à l'entreprise, avec la méthode sectorielle adaptée et les hypothèses explicites. Ne pas imposer de DCF industriel à une banque, un assureur, une foncière, une utility ou une holding.
5. Comparer le rendement implicite de dix ans au benchmark Monde, convention de travail 8 % non garantie, après risques/frais/fiscalité/change/risque de concentration. L'ETF World reste l'alternative par défaut.
6. Conserver les faits, calculs, hypothèses et avis distincts. Tout nombre manquant demeure NULL ; aucune recommandation ne découle d'un dossier incomplet.
7. La baisse du cours seule ne prouve rien ; une entreprise excellente trop chère reste en surveillance.
8. Documenter le dossier contradictoire : première raison de rejet, scénario adverse, seuil de rupture de la thèse.

## Registre
Le fichier research/registre.json contient schema_version, updated_at, rotation_next et dossiers.
Chaque dossier inclut ticker, date, stage (complet / incomplet / revue-requise), qualitative_status (conforme / non conforme / non conclu), thesis, method, source_urls, publication_asof, dossier_path, model_path, last_review_reason.
Ces valeurs sont documentaires et ne signifient pas validation indépendante d'une recommandation.

## Modèle sauvegardé
Enregistrer dans research/modeles/TICKER.json (quand les sources suffisent) :
ticker, status, method, analysis_date, currency, last_publication_asof,
reported_years (cinq exercices, montants, unités et source pour chaque ligne),
normalization_bridge (retraitements justifiés ligne par ligne),
normalized_fcf_per_share ou méthode sectorielle alternative,
share_count, share_count_source, scenarios (prudent, central, optimiste avec valeur/action, taux, croissance et sources),
expected_return_central, world_reference, risk_premium, buy_price, safety_price,
method_crosscheck, red_flags, thesis_kill_criteria, confidence,
outstanding_evidence, sources.
Ne jamais renseigner un chiffre non vérifié pour remplir la structure.

## Traitement automatisé
Après la mise à jour quantitative GitHub Actions, analyser une priorité de rotation et tous les événements matériellement pertinents pouvant être traités avec preuve suffisante. Préserver les dossiers passés et réviser seulement les hypothèses affectées par de nouveaux faits. Mettre à jour uniquement ce dépôt autonome, jamais un autre site.
