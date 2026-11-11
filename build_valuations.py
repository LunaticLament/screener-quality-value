"""Moteur de prévalorisations indépendant du site de portefeuille."""
from __future__ import annotations
import argparse
import csv
import json
import logging
import os
import time
from datetime import datetime, timezone, date
from pathlib import Path

from valuation_engine import calculate
from valuation_sources import sec_financials, yahoo_financials

ROOT=Path(__file__).resolve().parent
FIN=ROOT/'data'/'financial_history.json'
MODELS=ROOT/'data'/'models.json'
REPORT=ROOT/'data'/'valuation_run_report.json'


def load(path,default):
    if not path.exists():return default
    try:return json.loads(path.read_text(encoding='utf-8'))
    except (OSError,ValueError):return default


def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')


def configs():
    f=ROOT/'valuation_assumptions.csv'
    if not f.exists():return {}
    with f.open(newline='',encoding='utf-8-sig') as inp:
        return {r['ticker']:r for r in csv.DictReader(inp) if r.get('ticker')}


def is_us(ticker):
    return '.' not in ticker and ticker not in ('TSM',)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--offline',action='store_true',help='Utiliser les fondamentaux archivés')
    p.add_argument('--force',action='store_true',help='Rafraîchir les comptes, même si récents')
    p.add_argument('--limit',type=int,default=0)
    args=p.parse_args()
    logging.basicConfig(level=logging.INFO,format='%(message)s')
    snap=load(ROOT/'data'/'snapshot.json',{})
    companies=snap.get('companies',[])
    if args.limit:companies=companies[:args.limit]
    if not companies: raise RuntimeError('Snapshot screener absent : exécuter refresh.py auparavant')
    cache=load(FIN,{'companies':{},'generated_at':None}).get('companies',{})
    previous_models={r['ticker']:r for r in load(MODELS,{}).get('models',[]) if r.get('ticker')}
    mapping=None
    if os.environ.get('SEC_USER_AGENT') and not args.offline:
        try:
            import requests
            from valuation_sources import SEC_TICKERS
            ses=requests.Session()
            ses.headers.update({'User-Agent':os.environ['SEC_USER_AGENT'],'Accept':'application/json'})
            response=ses.get(SEC_TICKERS,timeout=20)
            response.raise_for_status()
            mapping={str(x.get('ticker','')).upper():int(x['cik_str']) for x in response.json().values()
                     if isinstance(x,dict) and x.get('cik_str')}
            logging.info('SEC : fichier CIK chargé')
        except Exception as ex:
            logging.warning('SEC indisponible: %s',str(ex)[:140])
    summaries=[]; errors={}; refreshed=0; refreshed_symbols=set(); changed=[]
    params=configs()
    now=datetime.now(timezone.utc).isoformat(timespec='seconds')
    for i,c in enumerate(companies,1):
        ticker=c['ticker']; model=c.get('model'); old=cache.get(ticker,{})
        force=args.force or not old or old.get('source_type')!='primary' and is_us(ticker) and mapping is not None
        old_date=old.get('fetched_at','')[:10]
        try:age=(date.today()-date.fromisoformat(old_date)).days
        except ValueError:age=999
        triggers=c.get('triage',{}).get('triggers',[])
        large_move=any('Variation' in s or 'Baisse' in s or 'Hausse' in s for s in triggers)
        due=force or age>=7 or (old.get("source_type")=="primary" and is_us(ticker) and age>=1) or (large_move and age>=1)
        # Financials are meaningless for bank/insurance/holding/utility without sector model.
        if model=='corporate' and due and not args.offline:
            try:
                if is_us(ticker) and mapping is not None:
                    try:
                        row=sec_financials(ticker,mapping=mapping)
                    except Exception as sec_ex:
                        logging.warning('%s SEC: %s',ticker,str(sec_ex)[:110])
                        row=yahoo_financials(ticker)
                else:
                    row=yahoo_financials(ticker)
                old=row
                cache[ticker]=row
                refreshed+=1
                refreshed_symbols.add(ticker)
            except Exception as ex:
                errors[ticker]=str(ex)[:180]
                logging.warning('%s données indisponibles: %s',ticker,str(ex)[:180])
        result=calculate(c,old,params.get(ticker))
        if ticker in errors:result['warnings'].append('Dernière collecte en échec : '+errors[ticker])
        prior=previous_models.get(ticker,{})
        earlier=prior.get('scenarios',{}).get('central',{}).get('value')
        latest=result.get('scenarios',{}).get('central',{}).get('value')
        if earlier is not None and latest is not None and abs(earlier-latest)>1e-7:
            changed.append(ticker)
        result['computed_at']=now
        result['financial_update_applied']=ticker in refreshed_symbols
        summaries.append(result)
        logging.info('[%02d/%02d] %-12s %s (%d exercices)',i,len(companies),ticker,result['status'],result['coverage_years'])
    out={'schema_version':'1.0','generated_at':now,'universe_count':len(summaries),
         'objective':'PRE-VALORISATIONS AUTOMATIQUES; aucune valeur intrinsèque validée et aucun ordre de bourse',
         'benchmark_world_assumption':0.07,
         'scope':'Univers initial limité et non exhaustif; modèles corporates seulement',
         'models':summaries}
    save(FIN,{'generated_at':now,'companies':cache})
    save(MODELS,out)
    stat={'generated_at':now,'companies':len(summaries),'financials_refreshed':refreshed,
          'indicative_models':sum(x['status']=='prévalorisation_indicative' for x in summaries),
          'sector_blocked':sum(x['status']=='modèle_sectoriel_requis' for x in summaries),
          'without_model':sum(x['status']=='non_modélisable' for x in summaries),
          'model_changes':changed,'data_errors':errors,'validated_opportunities':0,
          'method':'DCF proxy par action, scénarios illustratifs non approuvés; modèles sectoriels bloqués',
          'sec_enabled':bool(mapping),'sec_note':'SEC require SEC_USER_AGENT nominal avec contact valide, à définir dans GitHub Secrets'}
    save(REPORT,stat)
    logging.info('Prévalorisations %d, secteur spécifique %d, non calculables %d',stat['indicative_models'],stat['sector_blocked'],stat['without_model'])

if __name__=='__main__':main()