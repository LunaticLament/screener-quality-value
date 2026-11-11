#!/usr/bin/env python3
"""Screen-grade valuation engine. Not an investment recommendation.
Computes DCF of *equity cash flows*, never subtracts net debt again.
The FCF history is provider-standardized, not five audited and normalized years.
"""
from __future__ import annotations
import json
import math
import statistics
from datetime import date, datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"
WORLD_BENCHMARK=0.08  # User's illustrative opportunity-cost assumption, NOT an ETF forecast
CASE_DEFS={
 "prudent":{"growth":-0.01,"discount":0.125,"terminal":0.01},
 "central":{"growth":0.035,"discount":0.105,"terminal":0.02},
 "optimiste":{"growth":0.07,"discount":0.09,"terminal":0.025},
}
# Years 6-10: interpolate early growth toward perpetual terminal growth.
def dcf_equity(fcf_per_share:float,growth:float,discount:float,terminal:float,years:int=10)->float:
    if not all(math.isfinite(v) for v in (fcf_per_share,growth,discount,terminal)):
        raise ValueError("Entrée DCF non finie")
    if fcf_per_share<=0 or discount<=terminal or discount<=0 or growth<=-1 or terminal<=-1:
        raise ValueError("Paramètres DCF invalides")
    current=fcf_per_share
    pv=0.0
    for t in range(1,years+1):
        g=growth if t<=5 else growth+(terminal-growth)*(t-5)/5
        current *= 1+g
        pv += current/(1+discount)**t
    pv += (current*(1+terminal)/(discount-terminal))/(1+discount)**years
    return pv

def implied_discount(fcf_per_share,growth,terminal,price):
    if price<=0: return None
    low=max(terminal+0.0001,0.001)
    high=0.8
    try:
        if dcf_equity(fcf_per_share,growth,low,terminal)<price:
            return None
        if dcf_equity(fcf_per_share,growth,high,terminal)>price:
            return None
        for _ in range(90):
            mid=(low+high)/2
            if dcf_equity(fcf_per_share,growth,mid,terminal)>price: low=mid
            else: high=mid
        return (low+high)/2
    except (ValueError,OverflowError,ZeroDivisionError):
        return None

def number(x):
    try:
        f=float(x)
        return f if math.isfinite(f) else None
    except (TypeError,ValueError,OverflowError):
        return None

def elapsed(iso):
    try:return (date.today()-date.fromisoformat(str(iso)[:10])).days
    except (TypeError,ValueError):return None

def blocked(company,reason,warnings=None,history=None):
    return {"ticker":company["ticker"],"name":company.get("name"),"region":company.get("region"),
            "sector":company.get("sector"),"model":company.get("model"),
            "price":number(company.get("price")),"price_asof":company.get("price_asof"),
            "currency":company.get("currency"),"status":"blocked",
            "method":"Méthode sectorielle ou données non suffisantes",
            "reason":reason,"warnings":warnings or [],"historical":history or [],
            "decision_ready":False,"validated_opportunity":False,
            "fair_value":None,"scenarios":None}

def analyze(company):
    sector=company.get("model")
    if sector!="corporate":
        return blocked(company,"Banque, assurance, utility, foncière ou holding : un DCF standard du FCF ne serait pas pertinent.",
                       ["Méthode sectorielle dédiée à développer (ROTE/TBV, capital distribuable, RAB, SOTP, AFFO selon activité)."])
    history=sorted(company.get("financial_history") or [],key=lambda z:z.get("year_end") or "")
    years=[h for h in history if number(h.get("cfo")) is not None and number(h.get("capex")) is not None]
    if len(years)<3:
        return blocked(company,"Moins de trois exercices avec CFO et CAPEX exploitables.",
                       ["L'objectif de validation reste cinq exercices et le rapprochement aux publications primaires."],years)
    price=number(company.get("price"))
    fresh=elapsed(company.get("price_asof"))
    if price is None or price<=0 or fresh is None or fresh<0 or fresh>10:
        return blocked(company,"Cours absent ou daté de plus de dix jours.",[],years)
    fin_currency=company.get("financial_currency")
    if not fin_currency or not company.get("currency") or fin_currency!=company.get("currency"):
        return blocked(company,"La devise des états financiers est différente de celle du cours, ou elle n'est pas vérifiable.",
                       ["Conversion FX documentée nécessaire pour les ADR et autres cotations croisées."],years)
    if not company.get("financial_source"):
        return blocked(company,"La provenance des chiffres financiers manque.",[],years)
    latest=years[-1]
    age=elapsed(latest["year_end"])
    if age is None or age<0 or age>550:
        return blocked(company,"Dernier exercice financier trop ancien ou non daté.",[],years)
    shares=number(company.get("shares_outstanding"))
    if not shares or shares<=0:
        shares=number(latest.get("diluted_shares"))
    if not shares or shares<=0:
        return blocked(company,"Nombre d'actions actuelles ou diluées manquant.",[],years)
    warnings=[]
    if len(years)<5: warnings.append(f"{len(years)} exercices disponibles seulement ; cinq ans non rapprochés.")
    if not company.get("reference_url") or company.get("quality_grade") not in ("A","B"):
        warnings.append("Filtre qualitatif durable non étayé par une étude documentée.")
    if number(company.get("shares_outstanding")) is None:
        warnings.append("Nombre d'actions issu du dernier exercice, pas du registre actuel.")
    else:
        d=number(latest.get("diluted_shares"))
        if d and abs(shares/d-1)>.12: warnings.append("Écart >12 % entre actions actuelles et moyennes diluées ; effets de périmètre/actions à contrôler.")
    raw=[]
    for h in years:
        cfo=number(h["cfo"]);capex=abs(number(h["capex"]))
        sbc=number(h.get("sbc"))
        wc=number(h.get("change_wc"))
        before=cfo-capex
        after=before-sbc if sbc is not None else before
        if sbc is None: warnings.append("SBC absent pour "+h["year_end"]+" : le flux conservé peut surestimer la capacité actionnariale.")
        raw.append({"year_end":h["year_end"],"cfo":cfo,"capex":capex,"sbc":sbc,
                    "wc":wc,"fcf_before_sbc":before,"fcf_after_sbc":after,
                    "fcf_ps_historical":after/number(h["diluted_shares"]) if number(h.get("diluted_shares")) and number(h["diluted_shares"])>0 else None,
                    "source_type":h.get("source_type","fact_provider_standardized"),
                    "source_name":h.get("source_name","Yahoo Finance via yfinance"),
                    "source_url":h.get("source_url") or company.get("financial_url"),
                    "currency":h.get("currency") or fin_currency})
    last3=raw[-3:]
    # This is intentionally a *statistical proxy*, never an approved FCF normalization.
    weights=[.2,.3,.5]   # greater weight on recent years
    basis=sum(w*x["fcf_after_sbc"] for w,x in zip(weights,last3))
    if basis<=0:
        return blocked(company,"FCF pondéré des trois derniers exercices non positif : le DCF de flux pérennes n'est pas fiable.",
                       warnings,raw)
    if any(x["fcf_after_sbc"]<=0 for x in last3):
        warnings.append("Au moins un FCF annuel négatif : les scénarios requièrent une revue manuelle des besoins d'investissement.")
    rev=number(latest.get("revenue"))
    if not rev or rev<=0: warnings.append("CA récent indisponible ; conversion en trésorerie non contrôlée.")
    fcfps=basis/shares
    scenarios={}
    for key,assumptions in CASE_DEFS.items():
        val=dcf_equity(fcfps,**assumptions)
        scenarios[key]={**assumptions,"value_per_share":val,
                        "potential":val/price-1,"margin_of_safety":1-price/val if val>0 else None}
    central=scenarios["central"]["value_per_share"]
    inferred=implied_discount(fcfps,CASE_DEFS["central"]["growth"],CASE_DEFS["central"]["terminal"],price)
    notes=["Base = 20 % FCF N−2 + 30 % N−1 + 50 % N, moins SBC lorsqu'elle est disponible.",
           "Ceci n'est PAS une normalisation du BFR, du CAPEX, des acquisitions et du périmètre.",
           "FCF/action traité comme flux revenant aux actionnaires après intérêts ; actualisé au coût des fonds propres.",
           "La dette nette n'est donc pas soustraite une seconde fois ; la dette et ses échéances restent à vérifier.",
           "Hypothèses de croissance et de rendement exigé génériques, NON fondées sur une analyse prospective de l'émetteur.",
           "8 % pour l'ETF Monde = hypothèse de comparaison, pas une prévision observée."]
    return {"ticker":company["ticker"],"name":company.get("name"),"region":company.get("region"),
            "sector":company.get("sector"),"model":sector,
            "price":price,"price_asof":company.get("price_asof"),"currency":company.get("currency"),
            "financial_asof":latest["year_end"],"financial_source":company.get("financial_source"),
            "source_url":company.get("financial_url"),"shares":shares,
            "shares_source":company.get("shares_source") or "Actions diluées dernier exercice",
            "years_available":len(raw),"historical":raw,
            "base_proxy_fcf":basis,"base_proxy_fcf_per_share":fcfps,
            "scenarios":scenarios,"fair_value":central,"potential":central/price-1,
            "implied_discount_central":inferred,"world_reference":WORLD_BENCHMARK,
            "status":"screen-grade","decision_ready":False,"validated_opportunity":False,
            "method":"DCF indicatif sur FCF/action; 10 ans et valeur terminale Gordon",
            "reason":"Valorisation automatique indicative exclusivement, non auditable à niveau décisionnel.",
            "warnings":sorted(set(warnings)),
            "notes":notes,"assumptions_type":"hypothèses génériques et base statistique non normalisée"}

def generate(snapshot):
    now=datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows=[analyze(c) for c in snapshot.get("companies",[])]
    registry=ROOT/"research"/"registre.json"
    dossier_index={}
    if registry.exists():
        try:
            doc=json.loads(registry.read_text(encoding="utf-8"))
            dossier_index={d["ticker"]:d for d in doc.get("dossiers",[]) if d.get("ticker")}
        except (ValueError,OSError,KeyError,TypeError):
            dossier_index={}
    for entry in rows:
        d=dossier_index.get(entry["ticker"])
        if d:
            path=d.get("dossier_path")
            if not isinstance(path,str) or not path.startswith("research/dossiers/") or ".." in path:
                path=None
            entry["documentary_research"]={
                "date":d.get("date"),"stage":d.get("stage"),"qualitative_status":d.get("qualitative_status"),
                "thesis":d.get("thesis"),"method":d.get("method"),
                "publication_asof":d.get("publication_asof"),
                "source_urls":[u for u in d.get("source_urls",[]) if isinstance(u,str) and u.startswith("https://")][:20],
                "dossier_url":"https://github.com/LunaticLament/screener-quality-value/blob/main/"+path if path else None,
                "last_review_reason":d.get("last_review_reason")
            }
    counts={"universe":len(rows),"indicative":sum(x["status"]=="screen-grade" for x in rows),
            "blocked":sum(x["status"]=="blocked" for x in rows),"decision_ready":0}
    counts["dossiers_documentaires"]=sum(bool(x.get("documentary_research")) for x in rows)
    return {"schema_version":"1.0","generated_at":now,"coverage":"Univers suivi uniquement, non mondial exhaustif",
            "world_reference":WORLD_BENCHMARK,"scenarios_default":CASE_DEFS,
            "disclaimer":"Scénarios mécaniques non validés, pas de recommandation d'achat ni cours cible approuvé.",
            "methodology":"DCF equity cash-flow sur base proxy 3 exercices, sans normalisation complète. Validation fondamentale impossible sans sources primaires, cinq ans, CAPEX/BFR/risques et prospective.",
            "counts":counts,"models":rows}

def append_revision_events(previous,new):
    path=DATA/"model_events.json"
    old=[]
    if path.exists():
        try:old=json.loads(path.read_text(encoding="utf-8"))
        except (ValueError,OSError):old=[]
    prevs={x["ticker"]:x for x in (previous or {}).get("models",[])}
    events=list(old)
    for x in new["models"]:
        oldx=prevs.get(x["ticker"])
        if not oldx:
            events.append({"at":new["generated_at"],"ticker":x["ticker"],"event":"initial","status":x["status"],
                           "financial_asof":x.get("financial_asof")})
            continue
        changes=[]
        if x.get("status")!=oldx.get("status"):changes.append("statut")
        if x.get("financial_asof")!=oldx.get("financial_asof"):changes.append("nouvel exercice")
        a=number(x.get("base_proxy_fcf_per_share"));b=number(oldx.get("base_proxy_fcf_per_share"))
        if a and b and abs(a/b-1)>=0.03:changes.append("base FCF/action variation ≥3 %")
        if changes:events.append({"at":new["generated_at"],"ticker":x["ticker"],"event":", ".join(changes),
                                   "status":x["status"],"financial_asof":x.get("financial_asof")})
    events=events[-500:]
    path.write_text(json.dumps(events,ensure_ascii=False,indent=2),encoding="utf-8")
    return events

def main():
    snap=json.loads((DATA/"snapshot.json").read_text(encoding="utf-8"))
    old_path=DATA/"valuations.json"
    previous=json.loads(old_path.read_text(encoding="utf-8")) if old_path.exists() else None
    doc=generate(snap)
    DATA.mkdir(exist_ok=True)
    append_revision_events(previous,doc)
    old_path.write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding="utf-8")
    # Store a portable static page: one JSON payload injected in the HTML template.
    template=(ROOT/"valuation.template.html").read_text(encoding="utf-8")
    if "__VALUATION_SNAPSHOT__" not in template:raise ValueError("Balise valuation manquante")
    payload=json.dumps(doc,ensure_ascii=False,separators=(",",":")).replace("<","\\u003c")
    (ROOT/"valorisations.html").write_text(template.replace("__VALUATION_SNAPSHOT__",payload),encoding="utf-8")
    print("DCF indicative:",doc["counts"])
if __name__=="__main__":main()
