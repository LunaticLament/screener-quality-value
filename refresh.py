#!/usr/bin/env python3
"""Mise à jour du screener indépendant. Des données manquantes restent nulles."""
import argparse
import csv
import json
import logging
import math
import re
from datetime import datetime, timezone, date
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MARKET=("price","price_asof","currency","market_source","market_url","market_cap","return_5d","return_1m","return_3m")
FINANCIAL=("financial_asof","financial_currency","financial_source","financial_url","fcf_latest","fcf_previous","fcf_yield","fcfps_cagr_3y","fcf_margin","operating_margin","revenue_latest","financial_note")

def number(x):
    try:
        v=float(x)
        return v if math.isfinite(v) else None
    except (TypeError,ValueError,OverflowError):
        return None

def days(x):
    try: return (date.today()-date.fromisoformat(str(x)[:10])).days
    except (ValueError,TypeError): return None

def read_csv(name):
    with (ROOT/name).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def pct_return(values,n):
    values=[number(x) for x in values]
    values=[x for x in values if x is not None and x>0]
    return values[-1]/values[-n-1]-1 if len(values)>n else None

def research(row):
    out={}
    for k in ("quality_grade","moat","visibility","risk","research_currency","research_date","reference_url","thesis_note"):
        out[k]=row.get(k) or None
    for k in ("price_reasonable","price_mos","intrinsic_central"):
        out[k]=number(row.get(k))
    return out

def annual_series(frame,labels):
    if frame is None or frame.empty: return {}
    for k in labels:
        if k in frame.index:
            output={}
            for year,val in frame.loc[k].items():
                v=number(val)
                if v is not None: output[str(year.date()) if hasattr(year,"date") else str(year)[:10]]=v
            return output
    return {}

def fetch(ticker,model):
    import yfinance as yf
    stock=yf.Ticker(ticker)
    yahoo="https://finance.yahoo.com/quote/"+ticker+"/"
    data={"market_url":yahoo,"financial_url":yahoo}
    warnings=[]
    try:
        history=stock.history(period="6mo",auto_adjust=False,actions=False,timeout=15)
        if history is not None and not history.empty:
            closes=history["Close"].dropna()
            if len(closes):
                data.update(price=number(closes.iloc[-1]),price_asof=str(closes.index[-1].date()),market_source="Yahoo Finance via yfinance")
                values=list(closes.values)
                data.update(return_5d=pct_return(values,5),return_1m=pct_return(values,21),return_3m=pct_return(values,63))
    except Exception as exc: warnings.append("Cours: "+str(exc)[:125])
    info={}
    try: info=stock.info or {}
    except Exception as exc: warnings.append("Métadonnées: "+str(exc)[:125])
    data["currency"]=info.get("currency")
    data["market_cap"]=number(info.get("marketCap"))
    data["financial_currency"]=info.get("financialCurrency")
    if model in ("corporate","utility"):
        try:
            cf=stock.cashflow
            inc=stock.income_stmt
            cfo=annual_series(cf,["Operating Cash Flow","Total Cash From Operating Activities"])
            capex=annual_series(cf,["Capital Expenditure","Capital Expenditures"])
            rev=annual_series(inc,["Total Revenue","Operating Revenue"])
            ebit=annual_series(inc,["Operating Income"])
            shares=annual_series(inc,["Diluted Average Shares"])
            years=sorted(set(cfo)&set(capex))
            if years:
                latest=years[-1]
                fcf={y:cfo[y]-abs(capex[y]) for y in years}
                data.update(financial_asof=latest,financial_source="Yahoo Finance via yfinance, comptes agrégés non vérifiés",fcf_latest=fcf[latest],
                            fcf_previous=fcf.get(years[-2]) if len(years)>1 else None,revenue_latest=rev.get(latest),
                            financial_note="FCF brut = CFO - CAPEX, non normalisé; aucun modèle de valeur intrinsèque validé.")
                if rev.get(latest) and rev[latest]>0:
                    data["fcf_margin"]=fcf[latest]/rev[latest]
                    if latest in ebit: data["operating_margin"]=ebit[latest]/rev[latest]
                if data.get("financial_currency") and data["financial_currency"]==data.get("currency"):
                    cap=data.get("market_cap")
                    if cap and cap>0: data["fcf_yield"]=fcf[latest]/cap
                    ps={y:fcf[y]/shares[y] for y in years if shares.get(y,0)>0}
                    oldest=min(ps) if ps else None
                    if oldest and latest in ps:
                        span=(date.fromisoformat(latest)-date.fromisoformat(oldest)).days/365.25
                        if 2.8<=span<=3.3 and ps[oldest]>0 and ps[latest]>0:
                            data["fcfps_cagr_3y"]=(ps[latest]/ps[oldest])**(1/span)-1
            else: warnings.append("Flux de trésorerie/CAPEX annuels comparables absents")
        except Exception as exc: warnings.append("Comptes: "+str(exc)[:150])
    else:
        data["financial_note"]="Ratios FCF génériques inadaptés; méthode sectorielle requise."
    if warnings: data["retrieval_warning"]="; ".join(warnings)
    return {k:v for k,v in data.items() if v is not None}

def triage(x):
    triggers=[]; warnings=[]
    price=number(x.get("price")); five=number(x.get("return_5d")); month=number(x.get("return_1m"))
    fcf=number(x.get("fcf_latest")); yield_=number(x.get("fcf_yield"))
    grade=(x.get("quality_grade") or "").upper()
    stale=days(x.get("price_asof"))
    fy=days(x.get("financial_asof"))
    special=x.get("model") in ("bank","insurance","utility","reit","holding")
    if price is None or stale is None or stale>10 or not x.get("market_source"): warnings.append("Cours manquant ou périmé")
    if not x.get("financial_source"): warnings.append("Comptes non sourcés")
    if not grade: warnings.append("Filtre qualitatif à documenter")
    if grade and not x.get("reference_url"): warnings.append("Note qualitative sans référence documentaire")
    if five is not None and abs(five)>=.05: triggers.append("Variation sur cinq séances ≥5 % en valeur absolue — analyser la cause")
    if month is not None and month<=-.10: triggers.append("Baisse ≥10 % sur un mois")
    if month is not None and month>=.15: triggers.append("Hausse ≥15 % sur un mois")
    if yield_ is not None and yield_>=.06 and x.get("model")=="corporate": triggers.append("FCF yield historique ≥6 % (non normalisé)")
    if price is not None and x.get("research_currency")==x.get("currency"):
        for key,label in (("price_reasonable","Cours sous le prix raisonnable"),("price_mos","Cours sous le seuil de sécurité")):
            threshold=number(x.get(key))
            if threshold is not None and price<=threshold: triggers.append(label)
    if price is None or stale is None or stale>10 or not x.get("market_source"):
        status,priority,why="À vérifier","C","Cours indisponible ou ancien"
    elif special:
        status,priority,why="Analyse sectorielle","B" if triggers else "C","Étude économique spécifique requise"
    elif fcf is None or not x.get("financial_source") or (fy is not None and fy>550):
        status,priority,why="À compléter","B" if triggers else "C","Données financières insuffisantes"
    elif grade in ("C","D"):
        status,priority,why="Rejet provisoire","R","Critères qualitatifs non satisfaits"
    elif not grade or not x.get("reference_url"):
        status,priority,why="À analyser","B" if triggers else "C","Moat et avenir économique à examiner"
    elif grade in ("A","B") and triggers:
        status,priority,why="À valoriser","A","Filtre qualitatif documenté et signal quantitatif"
    else:
        status,priority,why="Surveillance","C","Pas de déclencheur documenté"
    return {"status":status,"priority":priority,"why":why,"triggers":triggers or ["Aucun déclencheur quantitatif vérifié"],"warnings":warnings}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--offline",action="store_true")
    args=ap.parse_args()
    old={}
    path=ROOT/"data"/"snapshot.json"
    if path.exists():
        try: old={r["ticker"]:r for r in json.loads(path.read_text(encoding="utf-8")).get("companies",[])}
        except (ValueError,KeyError): pass
    ideas={r["ticker"]:research(r) for r in read_csv("research.csv") if r.get("ticker")}
    rows=read_csv("universe.csv")
    companies=[]; success=0; fail=0
    for seed in rows:
        ticker=seed["ticker"]
        item={k:seed.get(k) for k in ("ticker","name","region","sector","model","currency","origin")}
        last=old.get(ticker,{})
        item.update({k:last[k] for k in MARKET+FINANCIAL if last.get(k) is not None})
        item.update(ideas.get(ticker,{}))
        if not args.offline:
            try:
                fresh=fetch(ticker,seed.get("model"))
                item.update(fresh)
                if fresh.get("market_source"): success+=1
                else: fail+=1
                if fresh.get("retrieval_warning"): item["retrieval_warning"]=fresh["retrieval_warning"]
                elif fresh.get("market_source"): item.pop("retrieval_warning",None)
            except Exception as exc:
                fail+=1;item["retrieval_warning"]="Collecte: "+str(exc)[:160]
        item["triage"]=triage(item)
        companies.append(item)
        logging.info("%s : %s",ticker,item["triage"]["status"])
    now=datetime.now(timezone.utc).isoformat(timespec="seconds")
    snapshot={"schema_version":"1.0","generated_at":now,"methodology":"Sélection préliminaire, sans recommandation de transaction",
              "universe_scope":"Liste initiale limitée de sociétés mondiales; non exhaustive",
              "data_feed":"Yahoo Finance via yfinance, source secondaire non rapprochée aux émetteurs",
              "run_mode":"offline" if args.offline else "network","source_success_count":success,
              "source_failure_count":fail,"coverage_count":len(companies),"companies":companies}
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding="utf-8")
    output=ROOT/"index.html"
    html=output.read_text(encoding="utf-8")
    embedded="const embedded="+json.dumps(snapshot,ensure_ascii=False,separators=(",",":")).replace("<","\\u003c")+";"
    html,sub_count=re.subn(r"const embedded=.*?;(?=\s*\nconst \$=)",lambda m:embedded,html,count=1,flags=re.DOTALL)
    if sub_count!=1: raise RuntimeError("Balise de données HTML introuvable — publication interrompue")
    output.write_text(html,encoding="utf-8")
    report={"generated_at":now,"universe_count":len(companies),"updated_price_count":success,"failed_price_count":fail,
            "signals":[{"ticker":x["ticker"],"triggers":x["triage"]["triggers"],"date":x.get("price_asof")}
                       for x in companies if x["triage"]["triggers"]!=["Aucun déclencheur quantitatif vérifié"]],
            "status":"no_live_price_update" if success==0 else ("partial" if fail else "completed"),
            "validated_opportunities":0,
            "caveat":"Signaux de recherche exclusivement. Sources secondaires non auditées; pas de valorisation ni ordre automatique."}
    (ROOT/"data"/"run_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    logging.info("Screener publié : %d sociétés / %d cours actualisés",len(companies),success)

if __name__=="__main__":
    logging.basicConfig(level=logging.INFO,format="%(message)s")
    main()
