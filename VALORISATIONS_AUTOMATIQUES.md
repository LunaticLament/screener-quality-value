# Valorisations automatiques — contrôle méthodologique

## Ce que fait la tâche nocturne

1. Actualise les cours du screener (`refresh.py`).
2. Sur les sociétés industrielles/non financières, récupère les cinq exercices annuels XBRL de la SEC lorsqu'un `SEC_USER_AGENT` valide a été configuré ; sinon utilise les comptes agrégés Yahoo Finance, souvent limités à quatre ans.
3. Conserve les séries annuelles récupérées dans `data/financial_history.json` et les dates de chaque source. Les sociétés à statut spécial (banques, assureurs, utilities, holdings, foncières) sont bloquées jusqu'à l'introduction d'un modèle sectoriel crédible.
4. Produit un DCF *indicatif* en flux par action pour les sociétés disposant d'au moins trois exercices de CFO, CAPEX et actions diluées et trois FCF/action positifs consécutifs, sous réserve de concordance des devises.
5. Affiche trois sensibilités prudent/central/optimiste, la croissance requise par le cours (reverse DCF), les TRI théoriques et leur écart à l'hypothèse ETF Monde (7 % non garantie).
6. Publie `valorisations.html`, `models.json`, `rapport-valorisations.json` et met à jour le site principal du screener.

**Il n'y a aucune recommandation d'achat/vente automatique.** Les chiffres de DCF sont provisoires et non validés par un analyste. Une recherche complète nécessite notamment de normaliser les CAPEX et le BFR, comprendre les acquisitions et leurs coûts, le traitement des rémunérations en actions, la dette et l'évolution future du nombre d'actions, et de construire des hypothèses réellement spécifiques à chaque entreprise.

## Sources et permissions

- Cotations et comptes agrégés par défaut : [Yahoo Finance](https://finance.yahoo.com/), interrogé via [yfinance](https://ranaroussi.github.io/yfinance/). Ce fournisseur est une source secondaire, dont la couverture, la qualité et l'accès peuvent évoluer.
- États américains primaires optionnels : [SEC CompanyFacts](https://www.sec.gov/edgar/sec-api-documentation) (10-K, valeurs annuelles CFO, CAPEX, actions diluées, chiffre d'affaires, rémunérations en actions). La SEC exige un User-Agent d'identification et un contact valide. Dans GitHub → **Settings → Secrets and variables → Actions**, créez le secret `SEC_USER_AGENT` avec un identifiant et une adresse email professionnelle que vous contrôlez, au format `NomOrganisation Contact@exemple.com`. Ce secret n'est pas publié dans le dépôt ni affiché aux utilisateurs.
- Sans ce secret, le système continue automatiquement avec la source secondaire ; les modèles restent *non validés*.
- Le lien de source XBRL pour chaque émetteur est enregistré dans le modèle. Les séries SEC peuvent être retraitées et nécessitent toujours un rapprochement aux rapports annuels.

## Structure du calcul

`FCF brut = CFO publié − |CAPEX publiés|`.

`FCF brut/action = FCF brut / actions diluées moyennes` lorsque disponibles.

Ancre d'illustration = `min(dernier FCF brut/action, moyenne arithmétique des 3 derniers FCF bruts/action)`.

Il ne s'agit **pas** d'une « normalisation » économique des flux. Il n'y a aucun retraitement automatique inventé du BFR, des acquisitions ou du coût du capital.

Scénarios pré-paramétrés (modifiables à l'écran) : prudent `g=0 %, r=11,5 %, gT=1 %` ; central `g=3 %, r=10 %, gT=2 %` ; optimiste `g=6 %, r=9 %, gT=2,5 %`, sur **10 ans**. Cette uniformité fait des scénarios des *sensibilités*, pas des prévisions spécifiques.

`valeur = somme(FCF/action projeté / (1+r)^t) + [FCF/action_10 × (1+gT)/(r-gT)] / (1+r)^10`

Le TRI affiché résout le prix de marché comme la valeur actualisée des flux futurs et de la valeur terminale du scénario. Ce calcul ne mesure pas une probabilité de réalisation et ne prédit pas le cours de bourse. L'hypothèse World est 7 %, modifiable, sans garantie. La marge de sécurité de 20 % n'est qu'une démonstration, non un seuil approuvé.

## Cadence et limites

- Cours à chaque run quotidien 23 h 15, Paris.
- Comptes non-financiers : première collecte puis rafraîchissement au plus tard hebdomadaire. Lorsqu'une source SEC primaire est activée, contrôle quotidien des fondamentaux américains et détection des nouvelles données ; pour Yahoo, contrôle anticipé lors d'un mouvement de marché important.
- Historique financier et calculs enregistrés dans GitHub, en conservant les dates et la dernière source. Un échec temporaire ne transforme pas un chiffre ancien en donnée actuelle ; le rapport détaille les échecs.
- Aucune analyse LLM qualitative n'est exécutée dans GitHub Actions faute de connecteur et de sources attestées. L'IA de ChatGPT peut examiner en profondeur les dossiers signalés, mais ne doit pas inventer de « conformité qualitative ».
- Le périmètre reste limité à l'univers initial ; il ne s'agit **pas** d'une surveillance exhaustive de toutes les actions mondiales.

## Exécuter soi-même

```bash
pip install -r requirements.txt
python refresh.py
python build_valuations.py
python -m pytest -q tests/test_valuation_engine.py
```

Pour tester sans réseau : `python build_valuations.py --offline` (utilise le cache financier conservé, s'il existe). Pour demander une actualisation fondamentale immédiate : `python build_valuations.py --force`.

Toutes les pièces sont publiées **uniquement** dans `LunaticLament/screener-quality-value`. Le dépôt et les données du site personnel de suivi de portefeuille ne sont jamais modifiés.