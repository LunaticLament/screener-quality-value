# Schneider Electric (SU.PA) — revue fondamentale du 21 novembre 2026

**Statut : en_attente_de_sources — aucune valeur intrinsèque validée.** Étude menée sur le périmètre autonome Quality/Value. Le DCF automatique de `data/models.json` est indicatif et exclu de la conclusion.

## Sources primaires consultées
- Schneider Electric, Document d'enregistrement universel 2025, 27 mars 2026 : https://www.se.com/fr/fr/download/document/2025-DEU/ (document disponible, rapprochement détaillé des pages non terminé).
- Schneider Electric, Document d'enregistrement universel 2024 : https://www.se.com/ww/en/assets/564/document/510443/2024-universal-registration-document.pdf (tableaux de flux 2023 et 2024).
- Schneider Electric, communiqué résultats annuels 2025, 26 février 2026 : https://www.se.com/ww/fr/assets/342/document/528237/Communique-resultats-annuels-2025.pdf
- Schneider Electric, résultats T3 2026, 16 octobre 2026 : https://www.se.com/ww/fr/about-us/investor-relations/financial-results/
- Schneider Electric, informations réglementées, consultées le 21 novembre 2026 : https://www.se.com/ww/en/about-us/investor-relations/regulatory-information/overview// (émission obligataire de 10 Md$ annoncée le 18 novembre pour financer l'acquisition de PTC).
- Archives des rapports annuels 2021-2025 : https://www.se.com/ww/fr/about-us/investor-relations/regulatory-information/annual-reports/

## Vérification des séries et flux
Les données agrégées secondaires de `data/financial_history.json` couvrent seulement 2022-2025 ; elles ne peuvent pas remplacer les cinq exercices primaires 2021-2025.
| Année | CFO (M€) | CAPEX (M€) | FCF CFO-CAPEX (M€) | Qualité |
|---|---:|---:|---:|---|
| 2021 | non rapproché | non rapproché | non calculé | compte primaire à extraire |
| 2022 | 4 354 | 1 093 | 3 261 | agrégateur secondaire, non validé |
| 2023 | 5 907 | 1 365 | 4 542 | agrégateur secondaire ; **le DEU 2024 publie un FCF de 4 594 M€ fondé sur CAPEX nets de 1 313 M€** |
| 2024 | 5 580 | 1 419 | 4 161 | agrégateur secondaire ; **le DEU 2024 publie un FCF de 4 216 M€ fondé sur CAPEX nets de 1 364 M€** |
| 2025 | 6 131 | 1 543 | 4 588 | agrégateur secondaire, non validé |

**Alerte de définition :** les écarts 2023/2024 entre CAPEX agrégés et CAPEX nets publiés (52 M€ et 55 M€) interdisent de mélanger les séries sans pont documenté. Le CFO 2024 de 5 580 M€ comprend une consommation de BFR de 728 M€, déjà intégrée ; ne pas la soustraire deux fois. En 2023, le BFR a généré 378 M€.

## Qualité et risques
- Activité : équipements de distribution électrique, gestion de l'énergie, automatismes et logiciels industriels ; exposition favorable à l'électrification, à la modernisation des réseaux et aux centres de données.
- Moat possible : gamme intégrée, base installée, intégration logicielle, réseau commercial et coûts de changement. **La durabilité du ROIC économique et du pricing power n'est pas encore prouvée sur cinq exercices.**
- Le T3 2026 indique une croissance organique de 17 % et une contribution prix positive dans les produits ; cette croissance ponctuelle n'établit pas un taux perpétuel.
- **Événement majeur :** acquisition annoncée de PTC, financement obligataire de 10 Md$ annoncé le 18 novembre 2026. Le modèle doit intégrer dette pro forma, intérêts, change USD/EUR, prix d'acquisition, cash acquis, synergies, intégration, risques d'exécution et dilution éventuelle. Le seul historique pré-acquisition est insuffisant.
- Autres risques : cycle industriel, demande centres de données, concurrence, réglementation et risques de disruption technologique, gouvernance/allocation du capital.

## Pont économique et décision
CFO – CAPEX n'est pas un FCFE distribuable validé. Les composantes CAPEX maintenance/croissance, capitalisation de développement, SBC, acquisitions récurrentes, fiscalité cash, BFR normatif, dette pro forma PTC, intérêts, minoritaires et actions diluées doivent être chiffrées à partir des comptes primaires. Sans ces éléments, scénarios prudent/central/optimiste, reverse DCF, rendement implicite à 10 ans, comparaison World 7-8 %, prix raisonnable et marge de sécurité **ne sont pas calculables sans arbitraire**. Aucun ordre de bourse.

## Suite ciblée
1. Extraire le tableau CFO-CAPEX-SBC-BFR 2021-2025 directement des DEU avec pages et conventions homogènes.
2. Rapprocher le financement PTC/Cognite et les effets pro forma sur la dette, le coût du capital et les flux par action.
3. Vérifier dernier S1 2026, guidance 2026, actions diluées, maintenance et ROIC.
4. Réexaminer uniquement si des données nouvelles permettent une base normalisée défendable ; ne pas reprendre automatiquement le lendemain.

**Couverture nouvelle hors univers initial : aucune société supplémentaire valorisée lors de cette exécution.** Contrôle exhaustif des mouvements >=5 % des dossiers déjà achevés : non effectué, aucune valeur validée identifiée dans le registre actuel.
