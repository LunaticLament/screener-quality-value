# LVMH (MC.PA) — revue fondamentale du 23 novembre 2026

**Statut : en_attente_de_sources — aucune valeur intrinsèque validée.** Analyse du groupe LVMH, indépendante des portefeuilles. Prix de référence du snapshot : **381,95 EUR au 20/11/2026**, source secondaire Yahoo Finance via yfinance, non rapprochée à Euronext. Variation 5 séances : **−5,33 %** ; le motif économique du mouvement n'a pas été vérifié et aucune opportunité ne peut en être inférée.

## Sources et degré de vérification

1. LVMH, *2025 Universal Registration Document*, déposé AMF **31 mars 2026**, réf. D.26-0195 ; notice émetteur du **1 avril 2026** : https://www.lvmh.com/en/investors/ ; https://www.lvmh.com/en/investors/regulated-information/notices-specifying-the-availability-of-documents-french-version-only/ . Le document intégral est identifié mais ses tableaux de flux et notes n'ont pas été extraits ligne par ligne lors de cette revue : **ne pas prétendre le contraire**.
2. LVMH, *Investors and analysts*, chiffres clés 2023–2025, consultés le **23 novembre 2026** : https://www.lvmh.com/en/investors/investors-and-analysts/ . Source primaire, tableaux « Income statement » et « Profit from recurring operations » (page HTML sans pagination).
3. LVMH, *Investors and analysts*, archive affichant 2021–2023, consultée le **23 novembre 2026** : https://www.lvmh.com/it/investors/investors-and-analysts/ . Les chiffres historiques 2021–2022 restent à rapprocher des DEU correspondants.
4. LVMH, *2026 Q3 Revenue*, **12 octobre 2026**, point d'accès officiel https://www.lvmh.com/en/investors/investors-and-analysts/ . Les chiffres détaillés du trimestre et la guidance n'ont pas été extraits et ne sont pas reconstitués.
5. Dépôt interne `data/snapshot.json` généré le **23 novembre 2026** ; `data/financial_history.json` : agrégats Yahoo Finance/yfinance **secondaires et non validés**. Ne pas assimiler à des comptes audités.

## Cinq exercices : historique des performances (M EUR)

| Exercice | Chiffre d'affaires, source primaire LVMH | Résultat opérationnel courant, primaire | Marge |
|---|---:|---:|---:|
| 2021 | 64 215 | 17 151 | 26,7 % |
| 2022 | 79 184 | 21 055 | 26,6 % |
| 2023 | 86 153 | 22 802 | 26,5 % |
| 2024 | 84 683 | 19 571 | 23,1 % |
| 2025 | 80 807 | 17 755 | 22,0 % |

Le résultat opérationnel courant 2025 est inférieur de 22,1 % à 2023 ; l'hypothèse d'un retour immédiat à la marge de 2023 serait injustifiée. Mode et Maroquinerie représente **13 209 M EUR** de résultat opérationnel courant 2025 contre **16 836 M EUR** en 2023 (source primaire LVMH). Forte concentration de profit dans ce segment.

## Pont de flux provisoire — exclusivement données secondaires, non normalisées (M EUR)

| Année | CFO agrégé | CAPEX agrégé décaissé | CFO − CAPEX (proxy brut) | Actions diluées agrégées (millions) | Proxy/action EUR |
|---|---:|---:|---:|---:|---:|
| 2021 | non vérifié | non vérifié | non calculable | non vérifié | non calculable |
| 2022 | 17 835 | 5 082 | 12 753 | 502,480 | 25,38 |
| 2023 | 18 403 | 7 807 | 10 596 | 500,304 | 21,18 |
| 2024 | 18 925 | 5 552 | 13 373 | 499,681 | 26,76 |
| 2025 | 18 875 | 4 670 | 14 205 | 497,976 | 28,53 |

**Attention :** le proxy 2025 représente ~7,58 % de la capitalisation secondaire de 187,396 Md EUR, mais **ce n'est ni un rendement attendu ni un FCFE/FCFF validé**. Le prix par action et les actions diluées agrégées ne se réconcilient pas nécessairement avec la capitalisation ; nombre d'actions, titres auto-détenus et droits minoritaires à contrôler.

### Normalisation économique — points non vérifiés et traitement requis

- **BFR** : le snapshot agrégé affiche un poste `change_wc` de −575 M EUR en 2025 (contre −1 924 M en 2024 et −4 574 M en 2023) ; convention de signe et inclusion dans CFO à rapprocher au tableau IFRS. **Retraitement chiffré retenu : aucun**, afin d'éviter un double compte.
- **CAPEX maintenance/croissance** : CAPEX 2025 agrégé 4 670 M EUR ; ventilation par magasins, immobilier, production, systèmes et entretien non obtenue. **Maintenance normalisée : non calculable**. Ne pas assimiler amortissements et maintenance.
- **Acquisitions et cessions** : flux décaissés, prix différés et participations minoritaires non réconciliés ; coût de croissance externe **non calculable**.
- **SBC/dilution** : SBC absente des données secondaires, actions diluées 2025 non rapprochées aux notes ; **aucun ajustement arbitraire**.
- **Dette, loyers IFRS 16, trésorerie, minoritaires** : pont EV vers equity non vérifié ; déductions locatives et intérêts à traiter une seule fois selon FCFF/FCFE choisi.
- **Impôt de trésorerie** : non rapproché à l'impôt comptable ; fiscalité normalisée **non calculable**.
- **Change/cyclicité** : exposition au dollar et au renminbi, demande de luxe asiatique, tourisme et stocks ; aucune élasticité chiffrée défendable disponible.
- **Par action** : le tableau est un simple quotient des agrégats secondaires ; ne peut être projeté comme flux distribuable.

## Filtre qualitatif

Activités compréhensibles : marques de luxe, distribution, vins et spiritueux. Avantages plausibles : capital de marque, réseaux de distribution et savoir-faire, avec potentiel de prix premium ; **conformité non encore certifiée**, faute de rapprochement ROIC/ROE sur cinq ans, de la dynamique du cash par action et du capital investi. Vulnérabilités : concentration des profits en Mode et Maroquinerie, pression concurrentielle, contrefaçon, réglementation et droits de douane, réputation, dépendance aux tendances, exposition Chine et au change, gouvernance familiale/succession. L'avenir économique à dix ans est plausible mais le rendement sur le capital additionnel reste à démontrer.

## Valorisation et décision

**Aucun scénario prudent/central/optimiste validé, aucun reverse DCF, aucune valeur intrinsèque, aucun prix raisonnable ni marge de sécurité.** Le benchmark Monde de 7–8 % est une hypothèse comparative, pas une preuve de performance future. La forte contraction des marges entre 2023 et 2025 et l'absence d'un pont primaire CFO→FCFF/FCFE rendent arbitraire un taux de croissance terminal ou une base de cash distribuable. **Aucun ordre de bourse.**

### Critères de réfutation et prochaines recherches

Rapprocher les DEU 2021–2025, tableau de flux et notes (pages exactes à consigner), cash taxes, dette et leases, acquisitions, investissements de maintenance, actions et minoritaires ; analyser le S1 2026 et la publication T3 2026 ; expliquer les variations de prix ≥5 % par une source de marché fiable. Réfuter l'hypothèse de moat si marges, cash par action ou ROIC se dégradent durablement malgré la normalisation du cycle. Ne pas reprendre automatiquement le dossier au prochain run : poursuivre la rotation vers **RMS.PA**, sauf nouvelle source primaire déterminante.

**Couverture réelle de ce run :** une société (MC.PA) ; aucune nouvelle société hors univers initial évaluée, aucune réévaluation exhaustive des autres mouvements ≥5 %.
