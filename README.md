# Screener autonome Quality/Value prospectif — exploitation automatisée

## Statut opérationnel au 11 novembre 2026

- **Site public indépendant** : https://lunaticlament.github.io/screener-quality-value/
- **Valorisations et simulateur** : https://lunaticlament.github.io/screener-quality-value/valorisations.html
- **Collecte quantitative** : GitHub Actions chaque jour à 23 h 15, heure de Paris (sauf retard/incident fournisseur). Mise à jour des cours, comptes agrégés disponibles, historiques par exercice, screening et DCF indicatifs.
- **Recherche fondamentale documentaire** : tâche ChatGPT distincte « Valorisations Q/V autonomes » à 23 h 50, heure de Paris ; analyse progressive de la file de rotation et sauvegarde dans research/dossiers et research/registre.json, après collecte. La publication GitHub est relancée lors d'une modification de research.
- **Historique** : data/snapshot.json, data/valuations.json, data/model_events.json, data/run_report.json. Contrôles : tests/test_valuation.py, exécutés avant publication.
- **Portée réelle** : 36 sociétés initiales, non exhaustives mondialement. Premier lancement : 24 DCF indicatifs, 12 dossiers non valorisables en méthode standard. **Zéro recommandation validée.**
- **Sources** : Yahoo Finance via yfinance pour la partie quantitative (secondaire), puis publications d'émetteurs utilisées pour dossiers détaillés. Cinq exercices et normalisation économique restent nécessaires avant tout prix d'achat valide.
- **Méthode du DCF indicatif** : FCF économique proxy = moyenne pondérée des trois années récentes de CFO moins CAPEX et SBC lorsqu'il est connu ; flux par action, actualisation au coût des fonds propres ; pas de double retraitement de dette nette. Hypothèses génériques de croissance et de coût du capital. Ce n'est *pas* une normalisation d'entreprise.
- **Indépendance** : aucun accès en écriture ni transfert vers le site personnel, ses dépôts, ou le portefeuille modèle.

Cette version ne qualifie donc **jamais** un DCF indicatif d'opportunité d'achat. Les dossiers documentaires approfondis progressent séparément, en conservant les incertitudes et les sources.

---

# Screener Quality / Value prospectif — V1

**Nature** : outil de présélection d'actions mondiales à partir de données sourcées et de règles explicables. **Ce n'est ni un moteur de recommandations d'achat, ni une valorisation DCF, ni un flux de cotation garanti.**

## 1. Première utilisation sans connexion

Le fichier `index.html` s'ouvre directement avec un navigateur. Il contient un univers de départ de sociétés européennes, américaines et asiatiques sans inventer les cours ni les indicateurs manquants. Après l'ouverture, cliquer sur une entreprise pour consulter la fiche et renseigner, éventuellement, votre propre qualification et vos prix cibles. Exporter ensuite `research.csv` pour conserver ces modifications.

## 2. Activer les mises à jour de données

Python 3.10+ requis. Dans un terminal ouvert dans ce dossier :

```bash
python -m pip install -r requirements.txt
python refresh.py
```

Le script relit `universe.csv`, `research.csv`, récupère cours et états financiers disponibles auprès de **Yahoo Finance via la bibliothèque non officielle `yfinance`**, calcule des indicateurs financiers historiques prudents, puis reconstruit `data/snapshot.json` et `index.html`. Un échec de collecte conserve les dernières données réussies, mais celles-ci apparaissent comme anciennes dans l'interface. L'exécution peut être longue pour un univers de plusieurs dizaines de sociétés, et certains tickers peuvent ne pas répondre.

Pour tester sans réseau :

```bash
python refresh.py --offline
```

**Important :** `refresh.py --offline` ne crée aucune donnée financière. Les sources agrégées ne sont pas des rapports publiés et doivent être rapprochées de ces derniers avant toute décision. L'accès aux données peut être limité par l'éditeur ; ne pas contourner ses conditions d'utilisation. Un univers réellement exhaustif de plusieurs milliers de titres nécessite un fournisseur de données global, avec licence et capacités documentées.

## 3. Périmètre et exclusions

- Univers de départ : **36 titres sélectionnés**, non représentatifs du marché mondial complet. `universe.csv` est modifiable ; ajouter une société ne suffit pas pour la qualifier.
- Prix : dernier cours de clôture disponible (non ajusté) ; les performances 5 jours, 1 mois et 3 mois sont estimées sur 5/21/63 séances en cours ajustés lorsque disponibles.
- FCF historique : cash-flow opérationnel moins valeur absolue des CAPEX (sans retraitements du BFR ni des acquisitions).
- FCF yield : FCF historique / capitalisation ; **non calculé lorsque la devise des comptes est différente de la devise de cotation ou inconnue**.
- Croissance du FCF par action : basée sur flux publiés et actions diluées moyennes lorsqu'ils sont tous disponibles. Ce n'est **pas** une projection.
- Banques, assurances, utilities, holdings et foncières : orientation vers une **analyse sectorielle**, pas de filtre FCF générique automatique.
- Moat, ROIC durable, avenir économique, valorisation intrinsèque, rendement attendu, prime de risque face au World : non évalués automatiquement dans cette V1 faute de données vérifiées.

## 4. Règles du triage

Les déclencheurs de recherche initiaux sont les suivants, modifiables dans `screener_logic.py` (et, pour l'interface en l'état, dans la fonction JavaScript `triage` du modèle HTML) :

- variation de **5 % ou davantage en valeur absolue sur cinq séances** (surveillance des candidats déjà qualifiés), ou variation sur 21 séances ≤ -10 % ou ≥ +15 % ;
- FCF yield **historique** ≥ 6 % (hors modèles sectoriels) ;
- croissance annualisée passée du FCF/action ≥ 5 % ;
- cours observé inférieur au prix raisonnable ou avec marge de sécurité **saisi par l'analyste et dans la même devise**.

Les qualifications de qualité A/B permettent d'accéder à la priorité A uniquement avec un déclencheur, des données de marché récentes et un FCF historique identifiable. Une qualification A/B sans référence documentaire conserve le statut « à analyser ». La priorité A signifie **« à valoriser »**, jamais « investir ».

## 5. Préservation des avis d'analyste

Les avis saisis dans l'interface sont stockés si possible dans le navigateur local. Cliquez sur « Exporter mes avis », puis remplacez le fichier `research.csv` du dossier par le fichier exporté, après sauvegarde. **Les modifications faites dans le navigateur ne se répercutent pas automatiquement dans `research.csv` ni sur un site partagé.**

Champs facultatifs : `quality_grade` A/B/C/D, `moat`, `visibility`, `risk`, `price_reasonable`, `price_mos`, `intrinsic_central`, `research_currency`, `research_date`, `reference_url`, `thesis_note`.

## 6. Automatiser sur Windows

Dans le **Planificateur de tâches**, créer une tâche quotidienne à 23:00, en utilisant comme programme le chemin complet vers `python.exe`, comme arguments `refresh.py` et comme répertoire de démarrage le dossier du projet. Prévoir de journaliser la sortie et de contrôler régulièrement les erreurs. Le script reconstruit le fichier local ; il **ne publie pas** automatiquement votre site ChatGPT existant.

Sur Linux/macOS, utiliser cron ou un autre ordonnanceur équivalent avec chemins absolus.

## 7. Prochaines extensions

1. Connecteur de données financières primaires : SEC EDGAR Company Facts pour les États-Unis, sources IR/ESEF pour l'Europe, rapports officiels pour l'Asie ; normalisation par devise et période.
2. Historisation point-in-time avec révisions et contrôle anti-survivorship bias.
3. Import des valeurs intrinsèques de votre site existant, puis calcul de franchissements de seuils avec horodatage.
4. Modèles sectoriels et scénarios ; rendement futur explicite, différent du FCF yield historique.
5. Base plus large (constituants d'indices sous licence), dédoublonnage ADR/actions locales, gestion des risques et valorisations plus complètes.

## 8. Vérifications et sécurité

Les contrôles de règles sont dans `tests/test_logic.py` (tests purement fictifs et **non intégrés** dans le tableau). Exécuter `python -m pytest tests` si `pytest` est installé.

Les CSV d'entrée doivent être considérés comme des documents de travail ; ne saisissez pas de secrets dans le tableau. Les exportations sont locales au navigateur. L'absence de données n'est jamais remplacée par zéro ; un changement de cours ne constitue pas une modification de valeur intrinsèque.

## Sources techniques

- SEC, *EDGAR APIs* : https://www.sec.gov/edgar/sec-api-documentation
- yfinance, *Ticker & Download Reference* : https://ranaroussi.github.io/yfinance/reference/api/yfinance.Ticker.html
- Yahoo Finance : https://finance.yahoo.com/