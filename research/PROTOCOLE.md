# Protocole — revue fondamentale du screener autonome

Ce dossier appartient **exclusivement** au dépôt GitHub `LunaticLament/screener-quality-value`. Ne jamais modifier le site de portefeuille personnel ni le portefeuille modèle de 100 000 €.

## Distinction obligatoire

- `data/models.json` : DCF mécaniques, générés à partir de flux financiers non normalisés, **non actionnables**.
- `research/registre.json` : file de rotation, statut des dossiers et liens documentaires.
- `research/dossiers/TICKER.md` : analyse approfondie sourcée, cinq années et dernier exercice intermédiaire, moat et vulnérabilités.
- `research/modeles/TICKER.json` : modèle fondamental, hypothèses justifiées, normalisation détaillée, scénarios, reverse DCF et seuils **seulement si vérifiables**.

Un DCF automatique ne peut pas être recopié comme une valeur intrinsèque validée. Il est interdit d'inventer un FCF normalisé ou de masquer une absence d'information sous une moyenne historique.

## Filtre qualitatif avant valorisation

Évaluer et sourcer : utilité et lisibilité du modèle, avantage concurrentiel durable, qualité des marges et rendement du capital, génération de cash par action, capacité de survivre à un cycle difficile, avenir du secteur sur dix ans, allocation du capital, risques réglementaires/technologiques/concurrentiels et scénarios d'invalidation.

Conclure `conforme` ou `non conforme` seulement quand les preuves sont suffisantes. Sinon, marquer `information_indisponible` avec la preuve du blocage, sans rejeter économiquement la société. Privilégier la lecture de documents primaires.

## Normalisation et scénarios

Analyser les **cinq derniers comptes annuels réels**, le dernier compte intermédiaire et la guidance; pour chaque agrégat CFO, CAPEX, BFR, acquisitions/cessions, fiscalité, restructuration, SBC, dilution, dette et trésorerie, distinguer montant publié, retraitement chiffré, raison, source exacte et incidence par action. Ne pas déduire deux fois un BFR déjà exclu du FCF de référence. Ne pas projeter une croissance acquise par acquisitions sans son coût économique.

Méthode sectorielle : DCF par action/EV pour entreprises non financières quand le pont dette-fonds propres est cohérent ; banque ROE/TBV/capital distribuable ; assurance capital distribuable/solvabilité ; utilities approche réglementée, dette, maintenance ; holding somme des parties ; foncière AFFO/NTA.

Pour un dossier **effectivement terminé**, présenter scénarios prudent/central/optimiste avec croissance, marges, FCF normalisé par action, coût des capitaux, dilution, multiple/sortie, rendement implicite à dix ans, reverse valuation, marge de sécurité selon le risque, prix raisonnable, prix avec sécurité, et écart à une hypothèse Monde explicitée. Les résultats demeurent des appréciations d'analyste, jamais des certitudes.

## Format du registre

`research/registre.json` contient :

```json
{
  "schema_version": "1.0",
  "rotation_next": "V",
  "last_update": null,
  "cases": [
    {
      "ticker": "V",
      "status": "en_cours",
      "updated_at": "YYYY-MM-DD",
      "dossier_path": "research/dossiers/V.md",
      "model_path": "research/modeles/V.json",
      "latest_publication": "YYYY-MM-DD",
      "notes": "Sources manquantes ou étapes achevées"
    }
  ]
}
```

Le champ `status` doit être `en_cours`, `étude_achevée`, `non_conforme` ou `en_attente_de_sources`. Le dossier et le modèle doivent réellement exister avant d'ajouter leur chemin au registre. Le cas `étude_achevée` exige une normalisation chiffrée traçable et ne représente pas une recommandation d'ordre. Les modèles complets doivent conserver les champs `sources`, `annual_financials`, `normalization_bridge`, `three_scenarios`, `reverse_valuation`, `benchmark_world`, `risks`, `assumptions_asof`, `model_updated_at`, `review_level`.

À chaque exécution automatique, reprendre les sources déjà enregistrées, actualiser les données nouvelles depuis le dernier run, conduire une analyse prioritaire (initialement Visa) et sauvegarder le dossier même si la valeur intrinsèque reste incomplète. Décrire précisément ce qui empêche de le terminer. Réexaminer aussi les sociétés ayant subi un mouvement boursier important ou un changement de thèse; cela ne justifie jamais d'affirmer qu'une baisse est une opportunité.

## Affichage

La page `valorisations.html` affiche le lien et le statut de chaque dossier approfondi. Les prix des modèles automatiques restent identifiés comme « indicatifs ». Les scénarios d'un dossier approfondi sont présentés distinctement lorsqu'ils existent; ne jamais les substituer silencieusement aux modèles quantitatifs.