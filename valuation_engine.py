"""Calculs de prévalorisation transparents. Aucune recommandation sans revue humaine.

L'ancre FCF = une capacité illustrative de trésorerie liée aux flux reportés;
ce n'est jamais une « normalisation » des FCF ni une valeur intrinsèque validée.
"""
from __future__ import annotations

import math
from datetime import date
from statistics import mean

ASSUMPTIONS = {
    "prudent": {"growth": 0.00, "discount": 0.115, "terminal_growth": 0.01},
    "central": {"growth": 0.03, "discount": 0.10, "terminal_growth": 0.02},
    "optimiste": {"growth": 0.06, "discount": 0.09, "terminal_growth": 0.025},
}
HORIZON = 10
WORLD_REFERENCE = 0.07  # Hypothèse modifiable, non anticipation de marché.
MOS_EXAMPLE = 0.20   # Sensibilité pure, à adapter au risque.


def finite(value):
    try:
        f = float(value)
        return f if math.isfinite(f) else None
    except (ValueError, TypeError, OverflowError):
        return None


def positive(value):
    f = finite(value)
    return f if f is not None and f > 0 else None


def dcf_per_share(base, growth, discount, terminal_growth, horizon=HORIZON):
    """Proxy FCFE, sous hypothèse de dette stable; terminal cohérent avec r>g.

    Calculs de flux pour actionnaires, pas EV/WACC, et non flux actualisés certifiés.
    """
    base = positive(base)
    if base is None or not -0.75 < growth < 0.50 or not 0.02 < discount < 0.50 or not -0.05 < terminal_growth < discount - 0.015:
        return None
    projections = [base * (1 + growth) ** t for t in range(1, horizon + 1)]
    terminal = projections[-1] * (1 + terminal_growth) / (discount - terminal_growth)
    pv_flows = sum(v / (1 + discount) ** t for t, v in enumerate(projections, 1))
    pv_terminal = terminal / (1 + discount) ** horizon
    return {"value": pv_flows + pv_terminal, "annual_flows": projections,
            "terminal_value": terminal, "pv_flows": pv_flows, "pv_terminal": pv_terminal,
            "terminal_share": pv_terminal / (pv_flows + pv_terminal)}


def implied_irr(price, flows, terminal):
    price = positive(price)
    if not price or not flows or terminal <= 0:
        return None
    def npv(rate):
        return sum(v / (1 + rate) ** t for t, v in enumerate(flows, 1)) + terminal / (1 + rate) ** len(flows) - price
    lo, hi = -0.80, 1.00
    if npv(lo) * npv(hi) > 0:
        return None
    for _ in range(75):
        mid = (lo + hi) / 2
        if npv(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def reverse_growth(price, base, discount=0.10, terminal_growth=0.02):
    price = positive(price)
    if price is None or positive(base) is None:
        return None
    lo, hi = -0.3, 0.4
    def model(g):
        res = dcf_per_share(base, g, discount, terminal_growth)
        return res["value"] if res else None
    a,b=model(lo),model(hi)
    if a is None or b is None or not a <= price <= b:
        return None
    for _ in range(75):
        mid=(lo+hi)/2
        if model(mid) < price:
            lo=mid
        else:
            hi=mid
    return (lo+hi)/2


def annual_metric_rows(periods):
    rows=[]
    for period, v in sorted(periods.items()):
        cfo=finite(v.get("cfo"))
        capex=finite(v.get("capex"))
        shares=positive(v.get("diluted_shares"))
        rev=positive(v.get("revenue"))
        fcf=(cfo-abs(capex)) if cfo is not None and capex is not None else None
        fcfps=fcf/shares if fcf is not None and shares else None
        rows.append({"period": period, "cfo": cfo, "capex": abs(capex) if capex is not None else None,
                     "fcf": fcf, "diluted_shares": shares, "fcf_per_share": fcfps,
                     "revenue": rev, "fcf_margin": fcf/rev if fcf is not None and rev else None,
                     "sbc": finite(v.get("sbc"))})
    return rows[-8:]


def calculate(company, history, cfg=None):
    cfg = cfg or {}
    name=company.get("name") or company.get("ticker")
    ticker=company.get("ticker")
    model=company.get("model")
    result={"ticker":ticker,"name":name,"model":model,"region":company.get("region"),
            "currency":company.get("currency"),"price":finite(company.get("price")),
            "price_asof":company.get("price_asof"),"market_url":company.get("market_url"),
            "status":"non_modélisable","validation":"Aucune recommandation",
            "source_url":history.get("source_url"),"source_type":history.get("source_type"),
            "source_name":history.get("source_name"),"last_fetch":history.get("fetched_at"),
            "financial_asof":None,"coverage_years":0,"scenarios":{},"warnings":[],
            "quality_grade":company.get("quality_grade"),"quality_reference":company.get("reference_url"),
            "method":"DCF actionnaire indicatif (proxy FCF après CAPEX)",
            "world_reference": WORLD_REFERENCE,"mos_example":MOS_EXAMPLE,
            "assumptions_approval":"non approuvées","normalization":"non réalisée"}
    warnings=result["warnings"]
    if model!="corporate":
        result["status"]="modèle_sectoriel_requis"
        result["method"]={"bank":"ROE / P-TBV et capital distribuable",
                          "insurance":"Capital distribuable / solvabilité",
                          "utility":"DCF régulé, dette et CAPEX de maintenance",
                          "reit":"EPRA NTA / AFFO", "holding":"Somme des parties"}.get(model,"Méthode spécifique")
        warnings.append("Aucune valorisation automatique générique autorisée pour ce secteur.")
        return result
    periods=history.get("annual",{})
    rows=annual_metric_rows(periods)
    rows=rows[-5:]
    result["annuals"]=rows
    result["coverage_years"]=len([x for x in rows if x["fcf_per_share"] is not None])
    result["financial_asof"]=rows[-1]["period"] if rows else None
    if not rows:
        warnings.append("Historique CFO, CAPEX et actions diluées indisponible.")
        return result
    if company.get("currency")!=history.get("currency"):
        warnings.append("Devise des comptes différente de la devise de cotation; conversion non effectuée.")
        return result
    last=[x for x in rows if x["fcf_per_share"] is not None]
    if len(last)<3:
        warnings.append("Moins de trois exercices de FCF par action exploitables.")
        return result
    positives=[x for x in last[-3:] if x["fcf_per_share"]>0]
    if len(positives)<3:
        warnings.append("Les trois derniers FCF par action ne sont pas tous positifs; pas d'extrapolation automatique.")
        return result
    recent=last[-3:]
    anchor=min(recent[-1]["fcf_per_share"],mean(x["fcf_per_share"] for x in recent))
    if not positive(anchor):
        warnings.append("Ancre de FCF par action non positive.")
        return result
    result["anchor_fcfps"]=anchor
    result["anchor_formula"]="min(dernier FCF/action publié, moyenne des 3 derniers FCF/action) — approximation mécanique, pas une normalisation"
    result["anchor_bridge"] = {"latest_fcfps": recent[-1]["fcf_per_share"],
                               "mean_last_three_fcfps": mean(x["fcf_per_share"] for x in recent),
                               "selected_fcfps": anchor, "normalization_adjustments": None,
                               "normalization_status": "Non réalisée : FCF brut historique uniquement"}
    result["coverage_years"]=len(last)
    if len(last)<5:
        warnings.append("Historique inférieur aux cinq exercices exigés pour une validation fondamentale complète.")
    if not company.get("quality_grade") or not company.get("reference_url"):
        warnings.append("Moat et avenir économique à dix ans non documentés : statut indicatif uniquement.")
    if history.get("source_type")!="primary":
        warnings.append("États financiers agrégés d'une source secondaire; rapprochement aux comptes annuels requis.")
    if result["price"] is None:
        warnings.append("Cours indisponible : calcul du rendement implicite impossible.")
    if result["price_asof"]:
        try:
            age=(date.today()-date.fromisoformat(result["price_asof"][:10])).days
            if age>10: warnings.append("Cours antérieur de plus de dix jours : rendement implicite à revalider.")
        except ValueError: warnings.append("Date de cotation invalide")
    if rows[-1]["sbc"] is not None and rows[-1]["fcf"] is not None and rows[-1]["fcf"]>0:
        ratio=abs(rows[-1]["sbc"])/rows[-1]["fcf"]
        result["sbc_to_fcf"]=ratio
        if ratio>=0.15: warnings.append("Rémunération en actions significative (≥15 % du FCF brut); coût économique non ajusté.")
    assumptions={}
    for scenario,defaults in ASSUMPTIONS.items():
        custom={key:finite(cfg.get(f"{scenario}_{key}")) for key in ("growth","discount","terminal_growth")}
        a={key:custom[key] if custom[key] is not None else defaults[key] for key in defaults}
        assumptions[scenario]=a
        output=dcf_per_share(anchor,**a)
        if output is None:
            warnings.append(f"Hypothèses du scénario {scenario} invalides")
            continue
        model_result={k:output[k] for k in ("value","pv_flows","pv_terminal","terminal_value","terminal_share")}
        model_result.update(a)
        cumulative = 0.0
        schedule = []
        for year, flow in enumerate(output["annual_flows"], start=1):
            factor = (1 + a["discount"]) ** year
            present = flow / factor
            cumulative += present
            schedule.append({"year": year, "fcf_per_share": flow,
                             "discount_factor": factor, "pv_fcf_per_share": present,
                             "cumulative_pv": cumulative})
        model_result["projection"] = schedule
        model_result["irr"]=implied_irr(result["price"],output["annual_flows"],output["terminal_value"])
        result["scenarios"][scenario]=model_result
    cen=result["scenarios"].get("central")
    if cen:
        result["reverse_growth"]=reverse_growth(result["price"],anchor,cen["discount"],cen["terminal_growth"])
        result["theoretical_fair_price"]=cen["value"]
        result["theoretical_safety_price"]=cen["value"]*(1-MOS_EXAMPLE)
        if positive(result["price"]):
            result["margin_safety_at_price"]=1-result["price"]/cen["value"]
            result["upside_to_model"]=cen["value"]/result["price"]-1
            irr=cen["irr"]
            result["world_spread"]=irr-WORLD_REFERENCE if irr is not None else None
    result["assumptions"]=assumptions
    result["status"]="prévalorisation_indicative"
    warnings.append("DCF fondé sur FCF brut CFO-CAPEX: BFR, CAPEX soutenables, acquisitions, dette, fiscalité et dilution futurs non normalisés.")
    warnings.append("Taux de croissance, d'actualisation et marge de sécurité sont des hypothèses de sensibilité, non des estimations approuvées.")
    return result