"""Extraction périodique de faits financiers. SEC XBRL primaire si identifiant déclaré; Yahoo secondaire sinon."""
from __future__ import annotations

import os
import time
from datetime import datetime, timezone, date
from pathlib import Path

from valuation_engine import finite

SEC_BASE="https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
SEC_TICKERS="https://www.sec.gov/files/company_tickers.json"


def _datepart(x):
    return str(x.date()) if hasattr(x,"date") else str(x)[:10]


def _annual(frame,aliases):
    if frame is None or getattr(frame,"empty",True): return {}
    for label in aliases:
        if label in frame.index:
            out={}
            for key,value in frame.loc[label].items():
                n=finite(value)
                if n is not None: out[_datepart(key)]=n
            return out
    return {}


def yahoo_financials(ticker,stock=None):
    import yfinance as yf
    stock=stock or yf.Ticker(ticker)
    cf=stock.cashflow
    inc=stock.income_stmt
    cfo=_annual(cf,["Operating Cash Flow","Total Cash From Operating Activities"])
    capex=_annual(cf,["Capital Expenditure","Capital Expenditures"])
    shares=_annual(inc,["Diluted Average Shares"])
    rev=_annual(inc,["Total Revenue","Operating Revenue"])
    sbc=_annual(cf,["Stock Based Compensation","Share Based Compensation"])
    annual={}
    for end in sorted(set(cfo)|set(capex)|set(shares)):
        annual[end]={"cfo":cfo.get(end),"capex":capex.get(end),"diluted_shares":shares.get(end),
                     "revenue":rev.get(end),"sbc":sbc.get(end)}
    if not annual: raise RuntimeError("Aucun historique financier agrégé")
    info={}
    try:info=stock.info or {}
    except Exception:pass
    currency=info.get("financialCurrency")
    if not currency: raise RuntimeError("Devise des comptes indisponible; pas d'interprétation unitaire")
    return {"ticker":ticker,"annual":annual,"currency":currency,
            "source_type":"secondary","source_name":"Yahoo Finance, séries agrégées via yfinance",
            "source_url":"https://finance.yahoo.com/quote/"+ticker+"/financials/",
            "fetched_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "limitations":["États non rapprochés aux documents réglementaires", "Historique potentiellement limité à 4 exercices"]}


def _sec_records(facts,aliases,unit="USD"):
    taxonomy=facts.get("facts",{}).get("us-gaap",{})
    for tag in aliases:
        item=taxonomy.get(tag,{})
        observations=item.get("units",{}).get(unit,[])
        records={}
        for obs in observations:
            if obs.get("form") not in ("10-K","10-K/A") or obs.get("fp") not in ("FY",None):continue
            if not obs.get("start") or not obs.get("end"):continue
            try:
                length=(date.fromisoformat(obs["end"])-date.fromisoformat(obs["start"])).days
                if not 300<=length<=425:continue
            except ValueError:continue
            n=finite(obs.get("val"))
            if n is None: continue
            key=obs["end"]
            prior=records.get(key)
            if prior is None or obs.get("filed","")>prior.get("filed",""):
                records[key]=obs
        if records:
            return {end:finite(x["val"]) for end,x in records.items()}
    return {}


def sec_financials(ticker,session=None,mapping=None,agent=None):
    import requests
    agent=agent or os.environ.get("SEC_USER_AGENT")
    if not agent:
        raise RuntimeError("SEC_USER_AGENT non configuré (identité et contact pour l'accès SEC)")
    session=session or requests.Session()
    session.headers.update({"User-Agent":agent,"Accept-Encoding":"gzip, deflate","Accept":"application/json"})
    if mapping is None:
        res=session.get(SEC_TICKERS,timeout=20)
        res.raise_for_status()
        items=res.json()
        mapping={str(entry.get("ticker","")).upper():int(entry["cik_str"])
                 for entry in items.values() if isinstance(entry,dict) and entry.get("cik_str")}
    cik=mapping.get(ticker.upper())
    if not cik: raise RuntimeError("Ticker absent du répertoire de correspondance SEC")
    url=SEC_BASE.format(cik=f"{cik:010d}")
    res=session.get(url,timeout=28)
    res.raise_for_status()
    data=res.json()
    series={
        "cfo":_sec_records(data,["NetCashProvidedByUsedInOperatingActivities","NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"]),
        "capex":_sec_records(data,["PaymentsToAcquirePropertyPlantAndEquipment","PaymentsToAcquireProductiveAssets"]),
        "diluted_shares":_sec_records(data,["WeightedAverageNumberOfDilutedSharesOutstanding","WeightedAverageNumberOfShareOutstandingBasicAndDiluted"],unit="shares"),
        "revenue":_sec_records(data,["RevenueFromContractWithCustomerExcludingAssessedTax","RevenueFromContractWithCustomerIncludingAssessedTax","Revenues","SalesRevenueNet"]),
        "sbc":_sec_records(data,["ShareBasedCompensation"]),
    }
    years=sorted(set(series["cfo"])|set(series["capex"]))[-8:]
    annual={y:{name:items.get(y) for name,items in series.items()} for y in years}
    if len(annual)<3: raise RuntimeError("Série SEC annuelle inférieure à trois exercices")
    if not any(v.get("diluted_shares") for v in annual.values()):
        raise RuntimeError("Comptage des actions diluées SEC indisponible")
    return {"ticker":ticker,"annual":annual,"currency":"USD",
            "source_type":"primary","source_name":"SEC EDGAR CompanyFacts XBRL (10-K)",
            "source_url":url,"cik":cik,
            "fetched_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "limitations":["Données annuelles extraites automatiquement; normalisation économique et comparabilité de périmètre non vérifiées"]}