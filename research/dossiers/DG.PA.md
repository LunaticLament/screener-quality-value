# VINCI (DG.PA) — Revue fondamentale du 19 novembre 2026

**Statut : en_attente_de_sources — aucune valeur intrinsèque validée.** Étude initiale de VINCI, rotation distincte des dossiers Visa, RELX et SAP. Les chiffres du moteur automatique ne constituent pas une valorisation.

## Sources primaires examinées

1. VINCI, *Document d'enregistrement universel 2025*, comptes arrêtés le 5 février 2026 : https://www.vinci.com/publi/vinci/vinci-document-enregistrement-universel-2025.pdf ; présentation accessible des notes et de la dette : https://www.vinci.com/publi/vinci/a11y/2025/vinci-urd/article/342/
2. VINCI, *États financiers consolidés 2025*, publiés le 6 février 2026, tableaux du compte de résultat et des flux : https://www.vinci.com/finances/resultats-et-chiffres-cles/resultats-annuels-2025
3. VINCI, *États financiers semestriels 2026*, publiés le 30 juillet 2026, compte de résultat consolidé et tableaux de flux : https://www.vinci.com/en/finance/results-and-key-figures/2026-interim-financial-statements
4. VINCI, *Document d'enregistrement universel 2025*, ventilation des flux 2024 par métier : https://www.vinci.com/publi/vinci/a11y/2025/vinci-urd/article/350/
5. VINCI, communiqué de résultats 2025 du 5 février 2026, repris par Euronext : https://live.euronext.com/fr/products/equities/company-news/2026-02-05-vinci-resultats-2025-performance-remarquable-cash-flow

**Limite de couverture :** les états annuels primaires 2021, 2022 et 2023 ne sont pas encore rapprochés ligne par ligne. Le fichier `data/financial_history.json` contient des séries secondaires agrégées ; elles ne peuvent pas remplacer cette vérification. La couverture primaire effective de cette revue est 2024–2025 et S1 2026, et non cinq exercices vérifiés.

## Indicateurs vérifiés (millions d'euros sauf mention)

| Mesure | 2024 | 2025 | Source / portée |
|---|---:|---:|---|
| Chiffre d'affaires hors travaux concessionnaires pour tiers | 71 623 | 74 599 | Comptes consolidés 2025 |
| Résultat opérationnel sur activité | 8 997 | 9 558 | Comptes consolidés 2025 |
| Charges IFRS 2 (paiements en actions) | 462 | 567 | Comptes consolidés 2025 ; charge comptable, non décaissement à retrancher mécaniquement |
| FCF publié par VINCI | ~6 800 | ~7 000 | Communiqué 2025 ; définition propre à VINCI, non FCFF industriel |
| Dette financière nette à la clôture | 20 400 | 19 100 | Document d'enregistrement universel 2025 |
| Amélioration du BFR en 2025 | — | +2 500 | Communiqué 2025 ; composante potentiellement non répétable du FCF |
| Investissements financiers nets en 2025 | — | ~1 900 | Document d'enregistrement universel ; comprend les dettes des sociétés acquises |

**S1 2026 :** chiffre d'affaires 35 597 M€ contre 34 852 M€ au S1 2025 ; résultat opérationnel sur activité 4 363 M€ contre 4 140 M€ ; charges IFRS 2 de 356 M€ contre 377 M€ ; résultat net part du groupe 2 078 M€ contre 1 896 M€ (états semestriels du 30 juillet 2026).

**Cours de référence** : 114,25 € (DG.PA, snapshot enregistré, daté du 17 novembre 2026, provenance Yahoo Finance). Il n'a pas été vérifié comme cours du 19 novembre. Le DCF de `data/models.json` repose sur quatre années agrégées et est **indicatif et non utilisable**.

## Modèle économique, avantages et risques

- **Concessions autoroutières et aéroportuaires** : actifs à longue durée, barrières d'entrée contractuelles et physiques, tarification encadrée, mais durée résiduelle des contrats, régulation, renouvellement des concessions et coûts de réinvestissement déterminants. Les flux ne peuvent être prolongés à l'infini à un taux de croissance terminal uniforme.
- **Énergies et construction** : diversification géographique, carnet de commandes de 69,8 Md€ à fin 2025 (document universel 2025) ; concurrence sur appels d'offres, marges plus faibles et volatilité du BFR. La croissance externe est régulière, avec 33 acquisitions chez VINCI Energies en 2025 : les flux acquis ne doivent pas être capitalisés sans tenir compte du prix d'acquisition.
- **Solvabilité** : dette nette / EBITDA 2025 ~1,4× selon VINCI ; ne remplace pas une analyse de l'échéancier, des engagements concessionnels, de la dette sans recours et du coût du capital.
- **Gouvernance, ROIC par métier, maintenance concessionnelle, risques de change et fiscalité future** : non suffisamment vérifiés pour conclure à une conformité qualitative définitive sur dix ans.

## Pont CFO — CAPEX — flux distribuable : points bloquants

Le FCF publié 2025 d'environ 7,0 Md€ **n'est pas un FCFE normalisé**. L'amélioration de BFR de 2,5 Md€ ne doit pas être présumée pérenne ; elle est déjà comprise dans les flux de trésorerie et ne doit pas être soustraite deux fois. Il faut rapprocher le CFO IFRS, l'impôt payé, les intérêts payés, les investissements opérationnels, les investissements de croissance concessionnels, les remboursements IFRS 16, les acquisitions et cessions, puis la dette et les minoritaires. La ventilation 2024 par segment montre explicitement des investissements opérationnels, remboursements de dettes locatives et investissements de croissance distincts. Les paiements en actions IFRS 2 sont déjà une charge de résultat, à traiter économiquement par dilution ou coût de rachat, **sans double déduction**.

Une valorisation défendable nécessitera une **somme des parties** : concessions par durée contractuelle et flux après maintenance et investissements obligatoires, activités de services par FCFF normalisé, dette nette et minoritaires attribués sans double compte. La seule application d'un DCF industriel générique au FCF consolidé est inappropriée.

## Conclusion et décision

**Pas de valeur intrinsèque, de marge de sécurité, de TRI à dix ans ni de signal d'achat calculable à ce stade.** Les données 2021–2023 et la normalisation par segment, notamment la durée résiduelle des concessions et les investissements obligatoires, font défaut. Il serait arbitraire d'en déduire un scénario central. La baisse ou le niveau du cours n'établissent pas une opportunité.

**Suite ciblée** : documents annuels 2021–2023 ; tableaux de flux 2021–2025 et S1 2026 ; échéances de concessions et investissements ; séparation maintenance/croissance ; acquisitions ; fiscalité, ROIC, dilution et dettes par métier ; DCF concession par concession + activités non concessionnelles. Ne pas rouvrir automatiquement le dossier lors de la prochaine rotation sans source nouvelle déterminante.

**Contrôle des réévaluations ≥5 % :** aucun modèle fondamental validé dans les trois dossiers précédents du registre (V, REL.L, SAP.DE) ; aucun recalcul d'une valeur intrinsèque antérieure possible. Les variations de prix depuis la dernière valorisation ne sont pas établies pour ces dossiers. Aucun autre dossier mondial n'a été vérifié au niveau requis durant cette exécution.
